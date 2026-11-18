# HAD: Hierarchical Adversarial Defense for Network Intrusion Detection

Shuo Yang, Xinran Zheng, Jinze Li, Jinfeng Xu, Edith C. H. Ngai, Senior Member, IEEE

Abstract—Intrusion Detection Systems (IDSs) are critical for safeguarding network security but remain vulnerable to adversarial attacks that subtly manipulate traffic features to evade detection. To address this challenge, we propose HAD (Hierarchical Adversarial Defense), a robust and scalable framework designed to enhance IDS performance against adversarial threats. HAD is grounded in two key insights: adversarial perturbations are typically constrained to a limited subset of features to preserve traffic semantics, and benign traffic tends to exhibit denser feature distributions than malicious traffic. HAD consists of three integrated components. First, we introduce the Evasion Potential (EP) metric to partition features into manipulable and non-manipulable subsets, thereby identifying features that are most susceptible to adversarial exploitation. Second, we generate surrogate samples by selectively perturbing manipulable features, avoiding reliance on explicit adversarial examples. Third, we employ hierarchical contrastive learning to model the structural relationships among benign, malicious, and adversarial samples. A tailored loss function encourages compact representations for benign traffic while enforcing separation from both malicious and adversarial samples. Extensive experiments under various attack scenarios demonstrate that HAD outperforms existing methods in detecting adversarial samples while maintaining high classification accuracy. HAD supports seamless integration with existing IDSs or standalone deployment, offering an effective and adaptable defense against evolving adversarial threats.

Index Terms—Network Intrusion Detection, Adversarial Attack, Network Security.

## I. INTRODUCTION

Intrusion Detection Systems (IDSs) are essential components of modern network security [1]. In recent years, Machine Learning (ML)-based IDSs [2]–[6] have significantly enhanced detection capabilities by modeling complex traffic patterns and identifying anomalous behavior. Compared to traditional methods, ML-based systems offer improved flexibility and adaptability, allowing them to detect both known and emerging threats [7], [8]. However, their reliance on learned feature representations [9]–[11] renders them vulnerable to adversarial evasion attacks, where subtle perturbations to malicious traffic lead to misclassifications by state-of-the-art models [12]–[14].

Adversarial evasion attacks against IDSs are becoming increasingly sophisticated [15]–[17]. Recent studies have demonstrated a variety of attack strategies using generative adversarial networks (GANs) [18]–[20], reinforcement learning [21], and optimization-based techniques [22], [23], all capable of crafting effective adversarial traffic. To mitigate such threats, researchers have explored various defense mechanisms [24]– [27]. Among them, adversarial training [27] is widely adopted, wherein models are trained with adversarial samples [28] to improve robustness. While effective in computer vision and NLP domains [29], [30], its application to IDSs is limited by the difficulty of generating realistic adversarial traffic that adheres to protocol and functional constraints [31], [32]. Additionally, adversarial training is often tightly coupled with specific attack strategies, making it less effective against novel or adaptive threats [24]. Other defenses, such as gradient masking [33], [34] and defensive distillation [35], provide marginal improvements and may even introduce new vulnerabilities [36].

A promising alternative is adversarial sample detection, which can be deployed as a plug-in module without altering the original IDS. However, current methods [24], [25] often result in elevated false positive rates, degrading overall system performance [37]. This is primarily due to their inability to model the underlying divergence among benign, malicious, and adversarial samples.

To address these challenges, we propose Hierarchical Adversarial Defense (HAD<sup>1</sup>), a framework for adversarial sample detection in ML-based IDSs. HAD is grounded in two observations: (1) adversarial perturbations should be constrained in a limited feature space to preserve traffic functionality and remain imperceptible, and (2) benign traffic tends to exhibit denser feature distributions than malicious traffic. Based on these observations, HAD first partitions the feature space into manipulable and non-manipulable subspaces using the Evasion Potential (EP) metric, and then generates surrogate samples to simulate attack-agnostic evasion behaviors. HAD further models a hierarchical dispersion structure between benign and malicious traffic, where benign samples are encouraged to form compact representations and malicious samples are modeled as more dispersed. This allows HAD to identify adversarial samples that are misclassified as benign by the IDS but still exhibit dispersion patterns inconsistent with genuine benign traffic. HAD can be deployed either as a complementary detection layer for existing IDSs or as a standalone IDS model. Our contributions are summarized as follows:

• We reveal the mechanism of adversarial attacks in IDSs, where perturbations selectively target vulnerable features to evade detection. To quantify this, we introduce the Evasion Potential (EP), a metric that measures feature manipulability based on its classification importance and activation frequency in malicious samples.

• We propose HAD, a robust and adaptive framework to detect adversarial samples by capturing the hierarchical relationships among benign, malicious, and adversarial traffic. HAD leverages the distribution difference between benign and malicious traffic to guide hierarchical contrastive learning and distinguish adversarial samples from benign traffic.

• We conduct comprehensive experiments on two benchmark datasets under seven adversarial evasion attacks. Results demonstrate that HAD outperforms existing methods in detecting adversarial samples (§ VI-B) while maintaining high intrusion detection performance (§ VI-C).

• We further evaluate HAD under real-world temporal drift on AnoShift, demonstrating its effectiveness across heterogeneous IDS backbones under moderate drift and its ability to be recalibrated under severe normality drift (§ VII).

The remainder of this paper is organized as follows. § II reviews related work, while § III introduces the necessary preliminaries. In § IV, we provide a detailed description of the proposed method. The experimental setup and main results are presented in § V and § VI, respectively. § VII further evaluates HAD under real-world distribution drift. We discuss additional analyses and limitations in § VIII. Finally, we conclude the paper in § IX.

## II. RELATED WORK

## A. Network Intrusion Detection

With the advancement of Machine Learning (ML), MLbased IDSs [2]–[6] have become pivotal in safeguarding networks by identifying and mitigating malicious activities using learned ML models. Techniques such as Support Vector Machines (SVMs) [2], Random Forests [3], and deep learning architectures like LSTMs [4] and CNNs [5] are employed to model diverse traffic patterns and detect anomalies. Compared with traditional signature-based methods, ML-based IDSs are particularly attractive due to their ability to generalize and detect unknown attacks without relying on prior knowledge [1].

Despite their success, ML-based IDSs remain highly vulnerable to adversarial attacks [15]. These attacks craft adversarial samples by introducing imperceptible perturbations [13] to malicious traffic, exploiting the vulnerabilities of learned ML models. Prior research [17]–[23] demonstrates how adversaries manipulate critical features, such as packet sizes, transmission rates, and protocol attributes, to deceive IDSs into misclassifying malicious traffic as benign. For example, [18]–[20] utilized GANs to transform original malicious traffic into adversarial samples, effectively misleading IDSs. [22] employed zeroorder optimization to generate transferable adversarial samples, while [23] applied Particle Swarm Optimization and genetic algorithms to craft adversarial traffic flows. Additionally, [38] introduced a blind perturbation method designed to mislead Deep Neural Network (DNN) models across arbitrary inputs. These attack methods highlight the sophistication of adversarial techniques and their ability to compromise the robustness and reliability of IDSs, necessitating the development of effective defense mechanisms [15]–[17].

## B. Adversarial Attack Defense

The threats of adversarial attacks have driven extensive research into defense mechanisms for security-critical applications like IDSs [24]–[27]. Existing defense methods can broadly be classified into two categories: model robustness enhancement and adversarial sample detection.

Model robustness enhancement aims to improve the resilience of ML models against adversarial perturbations by reinforcing their decision-making processes. One widely adopted approach is adversarial training [27], where models are encouraged to learn robust decision boundaries [39] by exposing adversarial samples during training. While effective in fields like computer vision and NLP [29], [30], adversarial training in IDSs faces challenges: obtaining realistic adversarial network traffic is difficult [31], [32], [40], and crafting such samples demands substantial expertise and resources [15], [24]. Techniques like gradient masking [33], [34] and defensive distillation [35] tend to obscure the gradient information or smooth the decision boundaries to prevent attacks. However, these methods often provide only marginal improvements in robustness and may inadvertently introduce new vulnerabilities [36]. Adversaries can bypass these defenses by leveraging surrogate models or optimization techniques [18], [22] to craft adversarial samples, limiting their reliability in practice.

Adversarial sample detection methods add a complementary layer to IDSs without modifying their core architecture. Ensemble-based methods [14], [26] capture diverse perspectives on traffic to identify adversarial patterns, but they often require significant computational overhead. Furthermore, the transferability of adversarial samples across models can undermine ensemble defenses, as adversaries can craft inputs that simultaneously deceive multiple models [41]. Another type of method [24], [25], [42] analyzes feature distributions to detect anomalies indicative of adversarial manipulation. For example, manifold consistency evaluation [24] and traffic reconstruction methods [25] are used to identify samples exhibiting feature deviations from typical benign or malicious patterns. However, these methods often fail to detect subtle perturbations [43] and increase the false alarm rate, thereby degrading the performance of the original IDS model.

With the continual evolution of adversarial techniques, IDSs require defenses that are both adaptive and easy to deploy. HAD addresses this need by explicitly modeling hierarchical relationships among benign, malicious, and adversarial surrogate samples. It can operate either as an enhancement layer for existing IDS models or as a standalone intrusion detector, making it highly adaptable to diverse security requirements and deployment scenarios.

## III. PRELIMINARY

This section defines key terms used in this paper, introduces the problem formulation for adversarial network intrusion detection, and describes the threat model as well as the motivation for the proposed adversarial defense method.

## A. Problem Formulation

Definition 1. Network Intrusion Detection. Let $\mathbf { x } \in \mathbb { R } ^ { d }$ denote a traffic instance with d features, and let $y \in \{ 0 , 1 \}$ represent its label. Given a labeled training set $\mathcal { D } ^ { t r } = \{ ( \mathbf { x } _ { i } ^ { t r } , y _ { i } ^ { t r } ) \} _ { i = 1 } ^ { | \mathcal { D } ^ { t r } | }$ and a test set $\mathcal { D } ^ { t e } = \{ ( \mathbf { x } _ { j } ^ { t e } , y _ { j } ^ { t e } ) \} _ { j = 1 } ^ { | \bar { \mathcal { D } } ^ { t e } | }$ , where |D| represents the cardinality of ${ \mathcal { D } } ,$ , the objective of network intrusion detection is to train a model $\mathcal { F } ( \cdot ) : \mathbb { R } ^ { d }  \{ 0 , 1 \}$ that minimizes the prediction error on the test set:

$$
\mathcal {F} ^ {*} = \arg \min _ {\mathcal {F}} \frac {1}{| \mathcal {D} ^ {t e} |} \sum_ {j = 1} ^ {| \mathcal {D} ^ {t e} |} \mathbb {I} (\mathcal {F} (\mathbf {x} _ {j} ^ {t e}) \neq y _ {j} ^ {t e}),\tag{1}
$$

where I(·) is the indicator function, returning 1 if the argument is true and 0 otherwise.

Definition 2. Adversarial Sample Generation. An adversarial sample $\mathbf { x } ^ { a d v } \ = \ \mathbf { x } + \boldsymbol { \zeta } \in \mathbb { R } ^ { d }$ is a perturbed version of a malicious sample x, created to evade detection by a trained IDS model $\mathcal F ( \cdot )$ . The perturbation $\| \zeta \| _ { p }$ is bounded in magnitude under an $L _ { p } { \mathrm { - n o r m } }$ . The goal of the adversary is to cause misclassifications while keeping the perturbation imperceptible: $\zeta ^ { * } = \arg \operatorname* { m i n } _ { \zeta \in \mathbb { R } ^ { d } } \| \zeta \| _ { p } , \mathrm { s . t . } \mathcal { F } ( \mathbf { x } ) = 1 , \mathcal { F } ( \mathbf { x } + \zeta ) = 0 , \| \zeta \| _ { p } \leq \epsilon ,$

(2)

where $\epsilon > 0$ bounds the perturbation magnitude. This work focuses on adversarial evasion attacks, where malicious traffic $( y = 1 )$ is misclassified as benign.

Definition 3. Adversarial Attack Defense. Given a trained IDS model $\mathcal F ( \cdot )$ , a test dataset $\mathcal { D } ^ { t e }$ , and an adversary capable of generating adversarial samples $\mathbf { x } ^ { a d v } \in { \mathcal { D } } ^ { a d v }$ under the threat model detailed in § III-B, the goal of adversarial attack defense is to establish a defense mechanism M that works alongside ${ \mathcal F } .$ . The combined system processes input from $\mathcal { D } ^ { t e } \cup \mathcal { D } ^ { a d v }$ aiming to maximize the detection of adversarial samples while minimizing the degradation on test samples:

$$
\begin{array}{c} \mathcal {M} ^ {*} = \arg \max _ {\mathcal {M}} \frac {1}{| \mathcal {D} ^ {a d v} |} \sum_ {k = 1} ^ {| \mathcal {D} ^ {a d v} |} \mathbb {I} (\mathcal {M} \circ \mathcal {F} (\mathbf {x} _ {k} ^ {a d v}) = y _ {k} ^ {a d v}) \\ - \frac {1}{| \mathcal {D} ^ {t e} |} \sum_ {j = 1} ^ {| \mathcal {D} ^ {t e} |} \mathbb {I} (\mathcal {M} \circ \mathcal {F} (\mathbf {x} _ {j} ^ {t e}) \neq y _ {j} ^ {t e}), \end{array}\tag{3}
$$

where $y _ { k } ^ { a d v } = 1$ indicates that the adversarial sample originates from a malicious instance.

## B. Threat Model

Adversarial evasion attacks for network intrusion detection aim to subtly alter malicious traffic so that it is misclassified as benign, severely undermining the system’s effectiveness. Based on the adversary’s knowledge, adversarial attacks can be categorized as follows [44]:

• White-box Attack: Adversaries have complete knowledge of the targeted IDS model, including its architecture and parameters. This comprehensive understanding allows adversaries to craft effective adversarial samples.

• Gray-box Attack: Adversaries have partial knowledge, such as the model architecture without its parameters. They can query the model and adjust their attack strategies according to model feedback.

• Black-box Attack: Adversaries have no direct knowledge of the IDS and rely on querying the system while minimizing queries to avoid being detected.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/8841ddbc54acdca58b0bb0cc43da99a311e6b8044da02eb37cec9843258d3152.jpg)  
(a) NSL-KDD Dataset.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/ab485c17c2710a9b1e82fc35a80355b1985e66eedcf54f78b04539552148394b.jpg)  
(b) CIC-IDS Dataset.  
Fig. 1: The sample density of benign and malicious samples. Benign traffic tends to display denser and more clustered distributions compared to malicious traffic.

We consider a comprehensive threat model encompassing diverse adversarial evasion attacks designed to generate adversarial examples targeting IDSs. This model includes general white-box attacks [9], [45], [46], gray-box attack [18], and black-box approaches [22], [47], [48]. IDS-specific attacks such as IDSGAN [18] and ETA [22] impose constraints to preserve traffic functionality while achieving adversarial objectives. By integrating a wide range of attack methodologies and adversarial capabilities, our threat model establishes a robust foundation for evaluating the resilience of IDS models and defense mechanisms in challenging adversarial scenarios.

## C. Motivation of HAD

Our approach is driven by two critical observations regarding adversarial evasion attacks targeting IDSs.

1) Constrained Perturbation: Adversarial evasion attacks aim to craft adversarial traffic samples capable of bypassing IDS detection while retaining the original malicious functionality to ensure effectiveness. This requirement imposes strict constraints on perturbations applied to network flows, which should conform to the dependencies among traffic features, protocolspecific attributes, and statistical distributions of expected packets [19]. Therefore, adversarial perturbations are expected to satisfy these constraints to maintain the functional consistency and plausibility of the crafted traffic.

Additionally, adversaries prioritize maximizing attack effectiveness while minimizing detection risks [49]. To achieve this, perturbations are constrained in scope and magnitude, focusing on the most vulnerable features within the IDS’s feature space. These vulnerable features significantly influence IDS classification and are highly sensitive to small changes, making them prime targets for adversarial manipulation [18], [19], [24]. By exploiting such features, adversaries enhance the efficiency and stealth of their attacks. In contrast, features less susceptible to adversarial manipulation form a robust space. These features reflect the intrinsic properties of network traffic and contribute to its functionality, potentially serving as reliable indicators for distinguishing between benign and malicious behavior. This dichotomy between vulnerable and robust features builds the foundation of our feature space partition strategy, enabling targeted defenses against adversarial attacks.

2) Distribution Divergence: Another key observation concerns the distributional characteristics of benign and malicious traffic in feature space. Prior work [50] suggests that benign

IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY

traffic tends to form denser, more compact clusters, whereas malicious traffic is more dispersed due to its heterogeneity and behavioral irregularity. We empirically examine this trend on NSL-KDD [51] and CIC-IDS [52] by projecting 500 benign and 500 malicious samples from each dataset with t-SNE [53] and estimating their density via kernel density estimation. As shown in Fig. 1, benign samples exhibit higher density in the projected space, while malicious samples are more dispersed. Since this observation is derived under limited conditions, we regard it as a heuristic observation that guides the design of HAD rather than a general property of network traffic, and assess the resulting design in § VI-B and § VIII-B.

Adversaries often manipulate vulnerable features, such as packet size or transmission rate, to imitate benign traffic patterns, causing adversarial samples to appear denser and closer to benign samples in feature space. Quantifying this density difference can therefore help distinguish adversarial samples from benign ones. However, direct distribution estimation is computationally expensive for high-dimensional traffic features, while dimensionality reduction risks losing important information. To address this, HAD reformulates the inter-sample density divergence as an intra-sample, crosssubspace consistency measure. The compactness of benign traffic implies that its MFS and NFS views follow a coherent joint pattern and can be projected to nearby locations in a shared latent space, whereas adversarial perturbations shift the MFS view toward benign patterns while the NFS view retains malicious evidence, breaking this coherence. By learning subspace-specific encoders, HAD amplifies this divergence in the latent space and quantifies it per sample, without explicit distribution estimation or dimensionality reduction. By capturing the hierarchical relationships among benign, malicious, and adversarial traffic, our approach provides a robust foundation for adversarial detection while maintaining high intrusion detection performance.

## IV. METHODOLOGY

HAD (Hierarchical Adversarial Defense) is designed to enhance the robustness of IDSs against adversarial evasion attacks by leveraging insights into the hierarchical relationships among benign, malicious, and adversarial samples. As shown in Fig. 2, it comprises three tightly integrated stages: Feature Space Partition, Surrogate Sample Generation, and Hierarchical Contrastive Learning.

## A. Feature Space Partition

Adversarial evasion attacks operate under practical constraints: attackers aim to maximize misclassification success while minimizing perturbation cost and detection risk. As a result, attackers do not manipulate all features uniformly. Instead, they preferentially target features that yield higher attack utility, i.e., features whose modification leads to a significant change in the classifier’s decision with limited perturbation. Inspired by this, we propose partitioning the feature space into two distinct subspaces:

• Manipulable Feature Space (MFS): features that offer high empirical utility for evasion, meaning that their perturbation can substantially influence the model’s prediction.

• Non-Manipulable Feature Space (NFS): features that offer low empirical utility for evasion, whose perturbation contributes marginally to evasion success and is therefore less favored under rational attack strategies.

Here, “manipulability” in HAD does not refer to whether a traffic feature is physically editable in isolation. Likewise, NFS does not imply that the corresponding features are inherently impossible or costly to perturb. Instead, manipulability denotes evasion-relevant utility under the trained IDS: a feature is considered more manipulable if modifying it can strongly affect the IDS decision and if it frequently contributes to malicious predictions. Under this interpretation, the MFS/NFS partition provides an attack-agnostic approximation of the feature subspace that a rational adversary is more likely to exploit for efficient and stealthy evasion.

To quantify this evasion utility, we introduce the Evasion Potential $( E P )$ metric, which combines (i) the variability of a feature’s contribution to the classifier’s decision and (ii) its activation frequency in malicious samples. For a given feature $f _ { i } , E P$ is defined as:

$$
\mathbf {E P} (f _ {i}) = S H A P _ {i} \times \frac {N _ {i}}{N _ {m}}, i \in [ 1, d ],\tag{4}
$$

where $S H A P _ { i }$ represents the variability in the SHAP values [54] of feature $f _ { i } ,$ , calculated as:

$$
S H A P _ {i} = \max _ {\mathbf {x} _ {j} \in \mathcal {D} ^ {t r}} \operatorname{SHAP} (f _ {i}, \mathbf {x} _ {j}) - \min _ {\mathbf {x} _ {j} \in \mathcal {D} ^ {t r}} \operatorname{SHAP} (f _ {i}, \mathbf {x} _ {j}),\tag{5}
$$

SHAP values are grounded in cooperative game theory and attribute a feature’s marginal contribution to a model’s prediction. The range $S H A P _ { i }$ reflects how much a feature’s influence can vary across the dataset, thereby estimating the potential impact of perturbing $f _ { i }$ on model behavior.

The ratio $\frac { N _ { i } } { N _ { m } }$ captures how frequently $f _ { i }$ is activated in malicious samples, where $N _ { i }$ is defined as:

$$
N _ {i} = | \{\mathbf {x} _ {j} \in \mathcal {D} _ {m} ^ {t r} | \mathrm{SHAP} (f _ {i}, \mathbf {x} _ {j}) > 0 \} |,\tag{6}
$$

with $\mathcal { D } _ { m } ^ { t r }$ denoting the malicious sub-dataset and $N _ { m } = | \mathcal { D } _ { m } ^ { t r } |$ This term reflects the adversary’s potential gain, as features frequently contributing to malicious predictions are more attractive for manipulation.

The EP metric thus integrates both the significance and susceptibility of each feature, enabling a robust evaluation of its vulnerability to adversarial attacks. This forms the basis for partitioning the feature space into manipulable and non manipulable subspaces. Specifically, features with high $E P$ values are deemed manipulable and grouped into MFS, while features with low EP values, indicative of stability, are placed in NFS. Formally, it can be expressed as:

$$
\mathrm{MFS} = \left\{f _ {i} | \mathrm{EP} (f _ {i}) > \mu \right\}, \mathrm{NFS} = \left\{f _ {i} | \mathrm{EP} (f _ {i}) \leq \mu \right\}.\tag{7}
$$

The threshold $\mu$ is determined by an allocation ratio $\rho =$ $| \mathrm { M F S } | / d ,$ which controls the fraction of features assigned to the manipulable feature space. Specifically, features are sorted by their EP scores, and the top ρd features are assigned to MFS, while the remaining features are assigned to NFS. The sensitivity of HAD to this ratio is analyzed in § VI-E1. By explicitly modeling MFS and NFS, this partitioning provides a principled basis for adversarial defense. MFS includes high-risk features likely to be targeted, enabling fine-grained detection of subtle perturbations. NFS captures stable, functionality-related evidence with lower evasion utility, supporting robust separation of benign and malicious behavior. This structured partition also guides surrogate sample generation and serves as the basis for hierarchical contrastive learning. The analysis of feature partition results can be found in § VIII-A.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/2c985434e172f4cc7c7010206fd1a39a50336ccf4e2e500880f0a9b44af16f7f.jpg)  
Fig. 2: The overview of HAD. HAD operates through three tightly integrated stages: (1) Feature Space Partition, which separates the feature space into manipulable and non-manipulable subspaces by quantifying the vulnerability of features; (2) Surrogate Sample Generation, which simulates adversarial behaviors through structured perturbation of network traffic features; and (3) Hierarchical Contrastive Learning, which captures the hierarchical relationships among benign (Blue), malicious (Red), and adversarial (Purple) samples by modeling their dispersion across the feature subspaces.

## B. Surrogate Sample Generation

Adversarial training has been widely explored as a means to improve robustness in computer vision and NLP domains [29], [30]. However, its effectiveness in network intrusion detection systems (IDSs) is limited by two fundamental challenges. First, realistic adversarial traffic must satisfy strict functional and protocol-level constraints, making it difficult to enumerate or simulate all possible attack strategies. Second, adversarial training is often tightly coupled with specific attack algorithms, which can lead to overfitting to known perturbation patterns and poor generalization to unseen or future attacks.

To address these limitations, we introduce surrogate sample generation, which aims to model attack-agnostic evasion behavior rather than replicate perturbations produced by specific adversarial algorithms. Importantly, surrogate samples in HAD are neither adversarial examples generated by known attacks nor executable packet-level adversarial traces. Instead, they are artificially constructed feature-level proxy samples that capture the structural effect of evasion: suppressing discriminative evidence in vulnerable features while preserving non-manipulable, functionality-related characteristics. This design allows HAD to learn generalized evasion patterns without relying on attack specific knowledge.

1) Perturbation Pool Construction: We first construct a perturbation pool $D _ { p } \subset D ^ { t r }$ , which provides feature-level value candidates for surrogate generation. $D _ { p }$ is not an attack pool and contains no adversarial examples generated by specific attacks. Instead, it is built by randomly sampling benign and malicious instances from the original training set, spanning diverse attack categories without using attack-specific labels. Sampling from real traffic helps keep surrogate samples within plausible feature ranges and avoids arbitrary out-of-distribution values, while preventing the pool from encoding perturbation patterns tied to known adversarial strategies.

2) Feature Manipulation: Surrogate samples are generated by selectively manipulating features within the Manipulable Feature Space (MFS) identified in § IV-A. For each malicious training instance $\mathbf { x } _ { m } \in \mathcal { D } _ { t r } ^ { m }$ , we generate a binary mask:

$$
\begin{array}{l} \mathbf {m} = [ m _ {1}, m _ {2},..., m _ {d} ] ^ {T}; \\ \text {s.t.} m _ {i} = 0 \text {if} f _ {i} \in \mathrm{NFS}, \sum_ {i = 1} ^ {d} m _ {i} = \sigma \cdot | \mathrm{MFS} |, \end{array}\tag{8}
$$

where $\sigma \in ( 0 , 1 ]$ controls the perturbation rate. This formulation enforces that perturbations are restricted to the manipulable feature subset, while non-manipulable features—representing stable, functionality-related properties—remain unchanged.

For each feature selected by the mask, a replacement value is randomly sampled from a different instance $\mathbf { x } _ { p } \in \mathcal { D } ^ { p }$ , and combined with the original malicious sample via element-wise masking:

$$
\mathbf {x} _ {s} = \mathbf {m} \odot \mathbf {x} _ {p} + (\mathbf {1} - \mathbf {m}) \odot \mathbf {x} _ {m}.\tag{9}
$$

This randomized substitution process intentionally breaks correspondence with specific attack algorithms. Unlike adversarial training, which optimizes perturbations toward a given model’s gradients, surrogate generation introduces stochastic, attack-agnostic perturbations that approximate a broad space of evasion behaviors. The resulting surrogate samples represent malicious traffic whose discriminative features are partially suppressed, thereby mimicking the outcome of evasion rather than its exact mechanism.

To ensure minimal deviation from the original malicious instance, we further enforce an L -norm constraint on the perturbation magnitude, consistent with Eq. 2. Only surrogate samples that are misclassified as benign by the target IDS are retained, aligning with the threat model of evasion attacks.

## C. Hierarchical Contrastive Learning

In this stage, we map traffic to representation space for modeling the relationships among benign, malicious, and adversarial samples. This approach builds on the observation in § III-C2 that benign traffic shows more compact feature distributions than malicious traffic and adversarial samples, resulting in lower dispersion between feature subspaces.

1) Training Phase: As shown in Fig. 2, HAD employs a dual-encoder architecture consisting of $\mathcal { G } _ { \mathrm { M F S } }$ and $\mathcal { G } _ { \mathrm { N F S } }$ , which project the MFS and NFS into low-dimensional embeddings. For each sample $\mathbf { x } \in \mathbb { R } ^ { d }$ , we compute:

$$
\mathbf {z} _ {\mathrm{MFS}} (\mathbf {x}) = \mathcal {G} _ {\mathrm{MFS}} (\mathrm{MFS} (\mathbf {x})), \mathbf {z} _ {\mathrm{NFS}} (\mathbf {x}) = \mathcal {G} _ {\mathrm{NFS}} (\mathrm{NFS} (\mathbf {x})).\tag{10}
$$

We then define the dispersion metric as the Euclidean distance between the two subspace projections:

$$
\operatorname{DIS} (\mathbf {x}) = \left\| \mathbf {z} _ {\mathrm{MFS}} (\mathbf {x}) - \mathbf {z} _ {\mathrm{NFS}} (\mathbf {x}) \right\| _ {2}.\tag{11}
$$

Benign samples typically yield low dispersion, indicating consistent subspace distribution. Malicious samples show greater dispersion due to abnormal patterns, while adversarial samples lie in between as they mimic benign behavior while retaining malicious intent. Rather than presupposing this ordering in the raw feature space, HAD treats it as a structural prior and instills it into the representation space through Eq. 15.

To capture this hierarchical relationship, we design a hierarchical contrastive learning method for enhancing the distinguishing characteristics of different sample types by optimizing three loss functions. For benign samples, we aim to minimize the dispersion of their subspace to enhance compactness. The objective is defined as:

$$
\mathcal {L} _ {b} = \frac {1}{| \mathcal {D} _ {b} ^ {t r} |} \sum_ {\mathbf {x} _ {b} \in \mathcal {D} _ {b} ^ {t r}} \mathrm{DIS} (\mathbf {x} _ {b}).\tag{12}
$$

For surrogate samples, the hierarchical contrastive loss ensures they are distinguishable from benign samples. This is achieved by aligning surrogate samples closer to their original category (malicious) while maintaining separation from benign samples. The objective is given by:

$$
\mathcal{L}_{s} = \frac{1}{|\mathcal{D}_{b}^{tr}\| \mathcal{D}_{s}|}\sum_{\substack{\mathbf{x}_{b}\in \mathcal{D}_{b}^{tr}\\ \mathbf{x}_{s}\in \mathcal{D}_{s}}}\max (\mathrm{DIS}(\mathbf{x}_{b}) - \mathrm{DIS}(\mathbf{x}_{s}) + \delta ,0),\tag{13}
$$

where $\delta$ is a predefined margin that ensures sufficient separation of benign and surrogate samples.

Malicious samples exhibit greater dispersion compared to benign and surrogate samples. Thus, the objective for malicious samples is to maximize their separation from benign and surrogate samples in the representation space. The corresponding loss is formulated as:

$$
\mathcal{L}_{m} = \frac{1}{|\mathcal{D}_{s}||\mathcal{D}_{m}^{tr}|}\sum_{\substack{\mathbf{x}_{s}\in \mathcal{D}_{s}\\ \mathbf{x}_{m}\in \mathcal{D}_{m}^{tr}}}\max (\mathrm{DIS}(\mathbf{x}_{s}) - \mathrm{DIS}(\mathbf{x}_{m}) + \delta ,0).\tag{14}
$$

The final objective combines the three losses with balancing weights:

$$
\mathcal {L} = \lambda_ {b} \mathcal {L} _ {b} + \lambda_ {s} \mathcal {L} _ {s} + \lambda_ {m} \mathcal {L} _ {m}.\tag{15}
$$

2) Inference Phase: HAD can operate in two modes: as a supplementary detector or as a standalone IDS. In both cases, predictions are made by evaluating the sample’s dispersion relative to a threshold τ.

Supplementary Detection. HAD revisits benign outputs of the IDS model $\mathcal F ( \cdot )$

$$
\mathcal {M} \circ \mathcal {F} (\mathbf {x}) = \left\{ \begin{array}{l l} 1, & \text { if } \mathcal {F} (\mathbf {x}) = 1 \text { or } \mathcal {F} (\mathbf {x}) = 0 \land \mathrm{DIS} (\mathbf {x}) > \tau ; \\ 0, & \text { if } \mathcal {F} (\mathbf {x}) = 0 \land \mathrm{DIS} (\mathbf {x}) \leq \tau . \end{array} \right.\tag{16}
$$

Standalone Detection. HAD directly analyzes incoming traffic $\mathbf { x } \in \mathcal { D } ^ { t e } \cup \mathcal { D } ^ { a d v }$ :

$$
\mathcal {M} (\mathbf {x}) = \left\{ \begin{array}{l l} 1, & \text { if } \operatorname{DIS} (\mathbf {x}) > \tau ; \\ 0, & \text { if } \operatorname{DIS} (\mathbf {x}) \leq \tau . \end{array} \right.\tag{17}
$$

By measuring the dispersion between different feature subspaces, HAD detects adversarial behavior at a fine-grained level, improving the robustness of IDSs to adversarial attacks. The hierarchical contrastive learning builds directly on the feature partitioning and surrogate sample generation stages, resulting in a unified and scalable defense framework. The full algorithm is provided in Algorithm 1, and the computational complexity is analyzed in § VI-G.

## V. EXPERIMENTAL SETUP

In this section, we detail the experimental settings and implementation of our proposed HAD.

## A. Datasets

To evaluate the effectiveness of our method, we conduct experiments on two widely used intrusion detection benchmarks, NSL-KDD [51] and label-corrected CIC-IDS [52], [55], both of which are commonly adopted in adversarial IDS research [24]– [26]. We follow the standard experimental setup for NSL-KDD, and split CIC-IDS into training and test sets with an 80:20 ratio. Categorical features are label-encoded and numerical features are normalized using min–max scaling.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 HAD: Hierarchical Adversarial Defense
Input: training dataset $\mathcal{D}^{tr} = \mathcal{D}_b^{tr} \cup \mathcal{D}_m^{tr}$, testing dataset $\mathcal{D}^{te}$, adversarial dataset $\mathcal{D}_{adv}$, batch size $|\mathcal{B}|$, IDS model $\mathcal{F}(\cdot)$.
Output: detection result.
1: Stage 1: Feature Space Partition
2: compute SHAP values for $\mathcal{D}^{tr}$: SHAP($x_i, f_j$).
3: compute EP for each feature $f_j$ using Eq. 4.
4: partition features into MFS and NFS using Eq. 7.
5: Stage 2: Surrogate Sample Generation
6: construct perturbation pool $\mathcal{D}_p$ from $\mathcal{D}^{tr}$.
7: initialize surrogate sample set $\mathcal{D}_s$.
8: for each sample $x_m \in \mathcal{D}_m^{tr}$ do
9: generate random mask m using Eq. 8.
10: get the surrogate sample $x_s$ by manipulating the feature value using Eq. 9.
11: if $\mathcal{F}(x_s) = 0$ then
12: add $x_s$ to surrogate sample set $\mathcal{D}_s$.
13: end if
14: end for
15: Stage 3: Hierarchical Contrastive Learning
16: initialize encoders $\mathcal{G}_{\text{MFS}}$ and $\mathcal{G}_{\text{NFS}}$.
17: for sampled mini-batch $\mathcal{B} \in \mathcal{D}^{tr} \cup \mathcal{D}_s$ do
18: project samples into subspaces using Eq. 10.
19: compute dispersion using Eq. 11.
20: compute $\mathcal{L}_b, \mathcal{L}_s$ and $\mathcal{L}_m$ using Eq. 12, Eq. 13 and Eq. 14.
21: compute final loss $\mathcal{L}$ using Eq. 15.
22: optimize $\mathcal{G}_{\text{MFS}}$ and $\mathcal{G}_{\text{NFS}}$ using $\mathcal{L}$.
23: end for
24: for each sample $x \in \mathcal{D}^{te} \cup \mathcal{D}^{adv}$ do
25: compute dispersion using Eq. 11.
26: get the detection result using Eq. 16 and Eq. 17.
27: return detection result.
28: end for
</div>

NSL-KDD dataset [51] is an improved version to reduce redundancy and class imbalance. It contains benign traffic and four major attack categories—DoS, Probe, R2L, and U2R—with 125,973 training samples and 22,544 test samples, each represented by 41 features.

CIC-IDS dataset [56] reflects more realistic and contemporary network environments. It includes diverse attack scenarios such as DDoS, Brute Force, and Infiltration, and comprises over 3 million flow records with 80 features spanning multiple protocols and services. We use the label-corrected version following prior work [52].

In addition, we further evaluate HAD under real-world distribution drift using AnoShift [57], a benchmark built upon the Kyoto-2006+ traffic corpus and spanning ten years of network traffic. The detailed evaluation protocol and results are described in § VII.

## B. Metrics

We compute True Positive (TP), False Positive (FP), True Negative (TN), and False Negative (FN) for adversarial sample detection, defined as follows:

• TP: an adversarial sample correctly detected as adversarial.

• FP: a benign sample incorrectly detected as adversarial.

• TN: a benign sample correctly detected as benign.

• FN: an adversarial sample incorrectly detected as benign.

From these metrics, we derive the True Positive Rate (TPR) and False Positive Rate (FPR):

$$
\mathrm{TPR} = \frac {\mathrm{TP}}{\mathrm{TP} + \mathrm{FN}}, \mathrm{FPR} = \frac {\mathrm{FP}}{\mathrm{FP} + \mathrm{TN}}.\tag{18}
$$

The Receiver Operating Characteristic (ROC) curve is generated by plotting TPR against FPR at various threshold settings, and the area under ROC curve (AUC-ROC) is used as a performance metric. Additionally, we consider standard machine learning metrics, including Accuracy (ACC) and F1- score (F1) for intrusion detection performance evaluation.

We conduct a paired t-test against the strongest overall relevant baseline for each evaluation task. Specifically, we compare HAD with MANDA on AUC, and compare HAD with RePo on ACC and F1, as they are the strongest and most relevant detection baselines. A p-value smaller than 0.05 indicates that the improvement is statistically significant.

## C. Baseline Methods

We implement and compare five baseline methods with HAD to evaluate their defense effectiveness against the threat model discussed in § III-B. The methods include Defensive Distillation [35], MANDA [24], Apollon [26], RePo [25], and Retraining [27], [58]. Their brief introductions are as follows.

• MANDA [24] detects adversarial samples by analyzing inconsistencies between manifold evaluations and IDS predictions.

• Retraining [27] enhances IDS robustness by retraining a DNN on a mixed dataset that includes surrogate samples [27].

• Defensive Distillation [35] trains DNNs using distillation to suppress gradients.

• Apollon [26] uses a multi-armed bandit strategy to dynamically select among diverse classifiers.

• RePo [25] employs denoising autoencoders with random input masking to hinder adversarial sample crafting.

## D. Adversary Attack Methods

As described in § III-B, we evaluate our method against a comprehensive set of adversarial evasion attacks targeting both general-purpose ML models and IDS-specific systems. Specifically, we consider five widely adopted general adversarial attacks—C&W [9], FGSM [45], HSJA [47], ZOO [48], and PGD [46]—together with two attacks tailored for network intrusion detection: IDSGAN [18] and ETA [22]. IDSGAN employs generative adversarial networks in a gray-box setting to produce function-preserving adversarial traffic, while ETA operates in a black-box setting by combining cooperative game theory with perturbation strategies to identify and manipulate critical features, yielding transferable adversarial samples across different IDS models.

These attacks cover gradient, optimization, and query-based strategies, enabling a rigorous evaluation of the robustness of our defense mechanism. For general-purpose attacks, we use publicly available implementations consistent with their original formulations. For IDS-specific attacks, we follow the constraints and procedures described in the corresponding works to ensure realistic evasion scenarios. Notably, the attacker’s manipulation space is not restricted by HAD’s own MFS/NFS partition during evaluation. This setting is consistent with prior work [24]. The effectiveness of these attacks is analyzed in § VI-A, where we show that they substantially degrade IDS performance, underscoring the necessity of robust adversarial defenses.

## E. Implementation

We implemented the proposed HAD using PyTorch and conducted all experiments on a server equipped with an NVIDIA GeForce RTX 3090 GPU. The target IDS model is a multi-layer perceptron (MLP) consisting of one input layer, two hidden layers (with 64 and 32 neurons, respectively), and one output layer. The HAD encoder is a one-layer network with 16 neurons. We set the batch size and epoch to 128 and 20, respectively, with all results averaged over three independent runs. Additionally, to evaluate the transferability of adversarial samples, we also implemented standard IDS models, including Random Forest (RF) and Gaussian Naive Bayes (GNB). In our experiment, we conducted adversarial attacks to generate adversarial samples from the malicious samples in the test dataset that were correctly classified by the target IDS model. We use the median EP split as the default feature allocation, i.e., $\rho = | \mathrm { M F S } | / d = 0 . 5 .$ , which assigns approximately equal dimensions to MFS and NFS. We further evaluate asymmetric feature allocations by varying ρ in § VI-E1 to assess the sensitivity of HAD to this default choice. The loss function balance weights were uniformly set to 1, as performance remained strong when all three loss terms were jointly optimized (see § VI-F). Additional parameter settings are detailed in § VI-E.

As mentioned in § IV-C, the proposed HAD can serve as a supplementary layer to the original IDS model, detecting adversarial samples among those identified as benign. Additionally, it can also be a robust intrusion detector capable of classifying network traffic independently against adversarial attacks. Therefore, we consider the following two tasks for comprehensive evaluation:

• Adversarial Sample Detection: In this setting, we combine the successful adversarial sample with the benign samples in the test dataset to evaluate the impact of HAD on the original IDS model.

• Network Intrusion Detection: In this setting, adversarial samples are treated as malicious traffic, combined with the original test dataset, and we evaluate classification performance using metrics such as ACC and F1.

## VI. EXPERIMENTAL RESULTS

In this section, we conduct extensive experiments on two benchmark datasets to evaluate HAD under seven adversarial attacks, aiming to answer the following research questions:

• RQ1: How do various adversarial evasion attacks impact the performance of IDS models? (§ VI-A)

• RQ2: Can our method effectively detect adversarial samples without affecting the target IDS model? (§ VI-B)

• RQ3: How robust is our method for network intrusion detection under adversarial environments? (§ VI-C)

TABLE I: The transferability of various adversarial evasion attacks on the NSL-KDD dataset.

<table><tr><td rowspan="2">Attack</td><td colspan="2">DNN</td><td colspan="2">RF</td><td colspan="2">GNB</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>None</td><td>0.9259</td><td>0.9077</td><td>0.9077</td><td>0.8826</td><td>0.8162</td><td>0.7837</td></tr><tr><td>C&amp;W</td><td>0.6719</td><td>0.6172</td><td>0.6611</td><td>0.6000</td><td>0.6055</td><td>0.5637</td></tr><tr><td>FGSM</td><td>0.7113</td><td>0.6599</td><td>0.6998</td><td>0.6419</td><td>0.6271</td><td>0.5784</td></tr><tr><td>HSJA</td><td>0.6455</td><td>0.5891</td><td>0.6336</td><td>0.5698</td><td>0.5725</td><td>0.5243</td></tr><tr><td>ZOO</td><td>0.7011</td><td>0.6487</td><td>0.7029</td><td>0.6520</td><td>0.6182</td><td>0.5692</td></tr><tr><td>PGD</td><td>0.6920</td><td>0.6389</td><td>0.6794</td><td>0.6188</td><td>0.6168</td><td>0.5715</td></tr><tr><td>IDSGAN</td><td>0.7000</td><td>0.6475</td><td>0.6862</td><td>0.6257</td><td>0.6224</td><td>0.5765</td></tr><tr><td>ETA</td><td>0.8759</td><td>0.8475</td><td>0.8920</td><td>0.8700</td><td>0.7728</td><td>0.7353</td></tr></table>

TABLE II: The transferability of various adversarial evasion attacks on the CIC-IDS dataset.

<table><tr><td rowspan="2">Attack</td><td colspan="2">DNN</td><td colspan="2">RF</td><td colspan="2">GNB</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>None</td><td>0.9860</td><td>0.9861</td><td>0.9951</td><td>0.9951</td><td>0.9582</td><td>0.9594</td></tr><tr><td>C&amp;W</td><td>0.6573</td><td>0.6598</td><td>0.6635</td><td>0.6632</td><td>0.6388</td><td>0.6456</td></tr><tr><td>FGSM</td><td>0.6580</td><td>0.6605</td><td>0.6641</td><td>0.6638</td><td>0.6395</td><td>0.6462</td></tr><tr><td>HSJA</td><td>0.6573</td><td>0.6598</td><td>0.6634</td><td>0.6631</td><td>0.6388</td><td>0.6456</td></tr><tr><td>ZOO</td><td>0.6573</td><td>0.6598</td><td>0.6635</td><td>0.6632</td><td>0.6388</td><td>0.6456</td></tr><tr><td>PGD</td><td>0.6573</td><td>0.6598</td><td>0.6640</td><td>0.6639</td><td>0.6388</td><td>0.6456</td></tr><tr><td>IDSGAN</td><td>0.7104</td><td>0.7127</td><td>0.7170</td><td>0.7167</td><td>0.6909</td><td>0.6973</td></tr><tr><td>ETA</td><td>0.6859</td><td>0.6883</td><td>0.6997</td><td>0.7016</td><td>0.6666</td><td>0.6731</td></tr></table>

• RQ4: Can our method effectively defend against adaptive adversarial attacks? (§ VI-D)

• RQ5: How do the parameters and components of our method influence its performance? (§ VI-E and § VI-F)

• RQ6: How efficient is our method in terms of computational complexity and practical overhead? (§ VI-G)

## A. Transferability of Adversarial Attacks (RQ1)

We evaluated the transferability of adversarial samples across three representative models, including DNN, Random Forest (RF), and Gaussian Naive Bayes (GNB). Transferability [41] refers to the ability of adversarial samples crafted against one model (e.g., DNN) to deceive other models (e.g., RF and GNB). For white-box attacks, we employ the DNN model as the target IDS model to generate adversarial samples. The results are summarized in Tables I and II, where ‘None’ indicates the baseline performance without adversarial interference.

The results indicate that different attacks exert varying impacts on the models. Notably, IDSGAN and ETA demonstrate less detriment to IDS performance compared to other attacks. This can be attributed to their incorporation of numerous constraints aimed at preserving the functionality of network traffic, which significantly reduces the effectiveness of attacks. Furthermore, the substantial accuracy degradation observed on RF and GNB confirms the transferability of adversarial samples generated using DNN, indicating that these samples can effectively mislead models beyond the original target.

We further observe that models trained on the CIC-IDS are more vulnerable to adversarial attacks than those trained on NSL-KDD. For instance, under ‘None’ condition, the DNN achieves 92.6% accuracy on the NSL-KDD dataset and 98.6% accuracy on the CIC-IDS dataset. However, when subjected to the C&W attack, the accuracy drops by 25.4% and 32.9%, respectively. A plausible explanation is the substantially higher feature dimensionality of CIC-IDS, which provides adversaries with more opportunities to exploit vulnerable features and craft effective perturbations. This observation underscores the importance of carefully controlling the perturbation rate when generating surrogate samples to learn hierarchical relationships among traffic types. Overall, these results highlight the severity of adversarial threats to IDSs and reinforce the necessity of robust defense mechanisms.

TABLE III: Adversarial sample detection performance on the NSL-KDD dataset. Values after / denote paired t-test p-values.

<table><tr><td rowspan="3">Attack</td><td colspan="3">MANDA</td><td colspan="4">HAD (Ours)</td></tr><tr><td colspan="2">TPR@FPR</td><td rowspan="2">AUC</td><td colspan="3">TPR@FPR</td><td rowspan="2">AUC</td></tr><tr><td>5%</td><td>10%</td><td>1%</td><td>5%</td><td>10%</td></tr><tr><td>C&amp;W</td><td>0.4805</td><td>0.7109</td><td>0.9370</td><td>0.7123</td><td>0.9008</td><td>0.9197</td><td>0.9690/0.031</td></tr><tr><td>FGSM</td><td>0.6368</td><td>0.8253</td><td>0.9253</td><td>0.8385</td><td>0.9834</td><td>0.9998</td><td>0.9949/0.001</td></tr><tr><td>HSJA</td><td>0.3976</td><td>0.5300</td><td>0.8749</td><td>0.9967</td><td>0.9998</td><td>0.9998</td><td>0.9998/0.002</td></tr><tr><td>ZOO</td><td>0.8790</td><td>0.9257</td><td>0.9531</td><td>0.7992</td><td>0.9995</td><td>0.9997</td><td>0.9962/0.020</td></tr><tr><td>PGD</td><td>0.8914</td><td>0.8959</td><td>0.9577</td><td>0.7528</td><td>0.9495</td><td>0.9704</td><td>0.9888/0.016</td></tr><tr><td>IDSGAN</td><td>0.8599</td><td>0.9004</td><td>0.9459</td><td>0.4533</td><td>0.9496</td><td>0.9507</td><td>0.9870/0.007</td></tr><tr><td>ETA</td><td>0.4069</td><td>0.6758</td><td>0.8624</td><td>0.4964</td><td>0.9923</td><td>1.0000</td><td>0.9863/0.001</td></tr></table>

TABLE IV: Adversarial sample detection performance on the CIC-IDS dataset. Values after / denote paired t-test p-values.

<table><tr><td rowspan="3">Attack</td><td colspan="3">MANDA</td><td colspan="4">HAD (Ours)</td></tr><tr><td colspan="2">TPR@FPR</td><td rowspan="2">AUC</td><td colspan="3">TPR@FPR</td><td rowspan="2">AUC</td></tr><tr><td>5%</td><td>10%</td><td>1%</td><td>5%</td><td>10%</td></tr><tr><td>C&amp;W</td><td>0.1892</td><td>0.6216</td><td>0.8583</td><td>0.6534</td><td>0.9736</td><td>0.9768</td><td>0.9858/0.002</td></tr><tr><td>FGSM</td><td>0.9053</td><td>0.9560</td><td>0.9771</td><td>0.6465</td><td>0.7568</td><td>0.9563</td><td>0.9716/0.026</td></tr><tr><td>HSJA</td><td>0.2750</td><td>0.3121</td><td>0.9105</td><td>0.4071</td><td>1.0000</td><td>1.0000</td><td>0.9704/0.001</td></tr><tr><td>ZOO</td><td>0.8080</td><td>0.8527</td><td>0.9563</td><td>0.5984</td><td>0.9988</td><td>1.0000</td><td>0.9914/0.001</td></tr><tr><td>PGD</td><td>0.5484</td><td>0.8710</td><td>0.9376</td><td>0.7864</td><td>0.9856</td><td>0.9866</td><td>0.9928/0.008</td></tr><tr><td>IDSGAN</td><td>0.6860</td><td>0.6925</td><td>0.9050</td><td>0.7859</td><td>1.0000</td><td>1.0000</td><td>0.9935/0.002</td></tr><tr><td>ETA</td><td>0.8667</td><td>0.9333</td><td>0.9644</td><td>0.8700</td><td>0.9872</td><td>0.9909</td><td>0.9961/0.009</td></tr></table>

## B. Performance on Adversarial Sample Detection Task (RQ2)

To evaluate the effectiveness of our method in detecting adversarial samples, we integrate the proposed framework as a supplementary detection layer alongside the target IDS model. The evaluation specifically focuses on identifying adversarial samples that are misclassified as benign by the IDS. Following the evaluation protocol in prior work [24], we report the ROC-AUC and the TPR at fixed FPRs, providing a comprehensive assessment of detection performance. The results are summarized in Tables III and IV, where HAD’s AUC values are followed by the paired t-test p-values against MANDA. We primarily compare our method against MANDA, as most existing defenses focus on enhancing model robustness rather than explicitly detecting adversarial samples. A broader comparison with such methods is presented in § VI-C. In our framework, the decision threshold (τ) governs the trade-off between adversarial detection performance (TPR) and benign misclassification (FPR), and can be tuned empirically to meet deployment requirements [59]. A detailed parameter analysis is presented in § VI-E3.

The results demonstrate that our proposed method outperforms MANDA in detecting adversarial samples across multiple attack scenarios, with the reported p-values confirming the statistical significance of the AUC gains. For example, under the C&W attack, HAD achieves absolute AUC gains of 0.03 and 0.12 over MANDA on the NSL-KDD and CIC-IDS datasets, respectively. Furthermore, our method achieves a TPR of over 99% at a 5% FPR for attacks such as HSJA and ZOO, highlighting its ability to detect adversarial samples while minimizing the impact on the target IDS model. At the stricter 1% FPR, the TPR of HAD decreases compared with that at 5% FPR, yet HAD still outperforms MANDA operating at 5% FPR under most attacks on both datasets, demonstrating its effectiveness at lower false-alarm rates.

This performance advantage stems from a fundamental limitation of MANDA, which relies on manifold consistency evaluation and degrades when adversarial samples substantially deviate from malicious manifolds. In particular, when attackers modify a large fraction of features—up to 50% while preserving traffic functionality, as reported in recent work [22]—manifold based methods struggle to distinguish adversarial and benign samples. In contrast, our approach characterizes adversarial behavior through intra-sample dispersion across feature subspaces, rather than solely relying on inter-sample relationships. By explicitly modeling these subspace-level discrepancies, our method remains effective under strong and diverse evasion strategies, highlighting its robustness against sophisticated adversarial attacks.

## C. Performance on Network Intrusion Detection Task (RQ3)

We apply HAD to intrusion detection tasks, assessing its overall effectiveness. As shown in Tables V and VI, HAD obtains the best overall performance and outperforms existing baselines in most attack scenarios, achieving an overall ACC of 93.02% and 95.96% on the NSL-KDD and CIC-IDS datasets, respectively. In contrast, the strongest overall baseline RePo achieves only 89.87% and 86.28%. For HAD, each ACC and F1 value is followed by the paired t-test p-value against RePo, and the results show that the improvements are statistically significant across both datasets.

The superior performance of HAD can be attributed to its explicit modeling of dispersion differences across benign, malicious, and adversarial traffic. Unlike RePo, which mainly reconstructs benign samples to identify abnormal traffic, HAD jointly models benign compactness and malicious dispersion, making it more effective in distinguishing adversarial samples that are misclassified as benign by the target IDS. Other existing methods show improvements under specific attacks but are less stable across diverse evasion strategies. Defensive Distillation improves robustness against some gradient-based attacks, such as FGSM, but provides limited protection against optimization-based or IDS-specific attacks. Apollon relies on ensemble diversity, but adversarial transferability can still affect multiple classifiers and weaken its ensemble-based defense. Retraining enriches the training data with additional samples, but its effectiveness depends heavily on whether the augmented samples match future adversarial behaviors. In contrast, HAD does not optimize for a specific attack type; instead, its surrogate generation and hierarchical objective capture attackagnostic dispersion patterns.

TABLE V: Intrusion detection performance on NSL-KDD dataset. Values after / denote paired t-test p-values.

<table><tr><td rowspan="2">Attack</td><td colspan="2">None</td><td colspan="2">Defen. Distillation</td><td colspan="2">Retraining</td><td colspan="2">Apollon</td><td colspan="2">RePo</td><td colspan="2">HAD (Ours)</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>C&amp;W</td><td>0.6719</td><td>0.6172</td><td>0.6695</td><td>0.6045</td><td>0.7970</td><td>0.8396</td><td>0.6895</td><td>0.6476</td><td>0.8852</td><td>0.9013</td><td>0.9152/0.009</td><td>0.9248/0.037</td></tr><tr><td>FGSM</td><td>0.7113</td><td>0.6599</td><td>0.7980</td><td>0.7366</td><td>0.6831</td><td>0.6319</td><td>0.7265</td><td>0.6862</td><td>0.9148</td><td>0.9278</td><td>0.9416/0.010</td><td>0.9467/0.001</td></tr><tr><td>HSJA</td><td>0.6455</td><td>0.5891</td><td>0.7365</td><td>0.6692</td><td>0.6502</td><td>0.5774</td><td>0.6680</td><td>0.6111</td><td>0.9239</td><td>0.9340</td><td>0.9443/0.009</td><td>0.9510/0.003</td></tr><tr><td>ZOO</td><td>0.7011</td><td>0.6487</td><td>0.6365</td><td>0.5692</td><td>0.7083</td><td>0.6498</td><td>0.7290</td><td>0.6813</td><td>0.9177</td><td>0.9246</td><td>0.9397/0.026</td><td>0.9437/0.034</td></tr><tr><td>PGD</td><td>0.6920</td><td>0.6389</td><td>0.7259</td><td>0.6665</td><td>0.6826</td><td>0.6233</td><td>0.6897</td><td>0.6381</td><td>0.8920</td><td>0.9036</td><td>0.9098/0.011</td><td>0.9177/0.025</td></tr><tr><td>IDSGAN</td><td>0.7000</td><td>0.6475</td><td>0.6365</td><td>0.5692</td><td>0.6725</td><td>0.6030</td><td>0.6823</td><td>0.6219</td><td>0.8747</td><td>0.8962</td><td>0.9326/0.002</td><td>0.9388/0.001</td></tr><tr><td>ETA</td><td>0.8759</td><td>0.8475</td><td>0.8275</td><td>0.7835</td><td>0.8739</td><td>0.8454</td><td>0.8852</td><td>0.8622</td><td>0.8829</td><td>0.8684</td><td>0.9280/0.007</td><td>0.9188/0.002</td></tr><tr><td>Overall</td><td>0.7140</td><td>0.6641</td><td>0.7186</td><td>0.6570</td><td>0.7239</td><td>0.6815</td><td>0.7243</td><td>0.6783</td><td>0.8987</td><td>0.9080</td><td>0.9302/0.001</td><td>0.9345/0.003</td></tr></table>

TABLE VI: Intrusion detection performance on CIC-IDS dataset. Values after / denote paired t-test p-values.

<table><tr><td rowspan="2">Attack</td><td colspan="2">None</td><td colspan="2">Defen. Distillation</td><td colspan="2">Retraining</td><td colspan="2">Apollon</td><td colspan="2">RePo</td><td colspan="2">HAD (Ours)</td></tr><tr><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td><td>ACC</td><td>F1</td></tr><tr><td>C&amp;W</td><td>0.6573</td><td>0.6598</td><td>0.6368</td><td>0.6416</td><td>0.6847</td><td>0.6993</td><td>0.7277</td><td>0.7450</td><td>0.8969</td><td>0.9278</td><td>0.9622/0.003</td><td>0.9718/0.017</td></tr><tr><td>FGSM</td><td>0.6580</td><td>0.6605</td><td>0.7320</td><td>0.7376</td><td>0.6638</td><td>0.6647</td><td>0.6686</td><td>0.6712</td><td>0.8879</td><td>0.9217</td><td>0.9239/0.003</td><td>0.9426/0.023</td></tr><tr><td>HSJA</td><td>0.6573</td><td>0.6598</td><td>0.7885</td><td>0.7528</td><td>0.6594</td><td>0.6614</td><td>0.6832</td><td>0.6904</td><td>0.8873</td><td>0.9215</td><td>0.9701/0.001</td><td>0.9779/0.002</td></tr><tr><td>ZOO</td><td>0.6573</td><td>0.6598</td><td>0.6883</td><td>0.6821</td><td>0.6635</td><td>0.6641</td><td>0.5173</td><td>0.7540</td><td>0.8741</td><td>0.9130</td><td>0.9713/0.001</td><td>0.9787/0.003</td></tr><tr><td>PGD</td><td>0.6573</td><td>0.6598</td><td>0.6957</td><td>0.6914</td><td>0.9109</td><td>0.9308</td><td>0.6871</td><td>0.6948</td><td>0.9031</td><td>0.9308</td><td>0.9483/0.010</td><td>0.9613/0.021</td></tr><tr><td>IDSGAN</td><td>0.7104</td><td>0.7127</td><td>0.6762</td><td>0.6811</td><td>0.7326</td><td>0.7369</td><td>0.7214</td><td>0.7225</td><td>0.8108</td><td>0.8709</td><td>0.9684/0.001</td><td>0.9756/0.001</td></tr><tr><td>ETA</td><td>0.6859</td><td>0.6883</td><td>0.9454</td><td>0.9466</td><td>0.9762</td><td>0.9819</td><td>0.8035</td><td>0.8230</td><td>0.7797</td><td>0.8549</td><td>0.9728/0.001</td><td>0.9792/0.003</td></tr><tr><td>Overall</td><td>0.6691</td><td>0.6715</td><td>0.7376</td><td>0.7333</td><td>0.7559</td><td>0.7627</td><td>0.6870</td><td>0.7287</td><td>0.8628</td><td>0.9058</td><td>0.9596/0.001</td><td>0.9696/0.001</td></tr></table>

TABLE VII: Attack success rate of search-based adaptive attacks under different candidate budgets.

<table><tr><td rowspan="2">Attack</td><td colspan="3">NSL-KDD</td><td colspan="3">CIC-IDS</td></tr><tr><td>10</td><td>100</td><td>500</td><td>10</td><td>100</td><td>500</td></tr><tr><td>C&amp;W</td><td>1.40%</td><td>1.60%</td><td>1.60%</td><td>5.90%</td><td>5.90%</td><td>6.00%</td></tr><tr><td>FGSM</td><td>1.60%</td><td>1.90%</td><td>2.20%</td><td>3.40%</td><td>3.90%</td><td>3.90%</td></tr><tr><td>HSJA</td><td>2.60%</td><td>2.60%</td><td>2.60%</td><td>0.00%</td><td>0.00%</td><td>0.20%</td></tr><tr><td>ZOO</td><td>0.60%</td><td>0.60%</td><td>0.80%</td><td>1.90%</td><td>1.90%</td><td>2.50%</td></tr><tr><td>PGD</td><td>0.80%</td><td>1.70%</td><td>1.90%</td><td>1.80%</td><td>3.10%</td><td>3.10%</td></tr><tr><td>IDSGAN</td><td>5.70%</td><td>6.10%</td><td>6.10%</td><td>2.80%</td><td>4.00%</td><td>4.00%</td></tr><tr><td>ETA</td><td>4.20%</td><td>4.70%</td><td>4.70%</td><td>7.10%</td><td>7.30%</td><td>7.30%</td></tr></table>

Overall, these results show that HAD provides a more stable defense across diverse adversarial environments. By modeling hierarchical relationships and dispersion differences, HAD improves intrusion detection performance while maintaining strong robustness against adversarial evasion attacks.

## D. Robustness under Adaptive Attacks (RQ4)

We further evaluate HAD under a more challenging threat model where adversaries know both the original IDS model and HAD, treating them as a unified detection pipeline. Under this setting, the adversary can refine its strategy based on the combined detection outcome. We consider two adaptive attack settings: a search-based adaptive attack and a gradient-based adaptive attack.

1) Search-based adaptive attack: In the first setting, the adversary searches for low-dispersion adversarial variants. Specifically, we randomly select 1,000 samples classified as malicious by the entire pipeline. For each sample, the adversary generates multiple valid adversarial variants, computes their dispersion scores, and selects the one with the lowest dispersion score as the final adversarial sample. To evaluate the effect of search budget, we consider 10, 100, and 500 candidate variants and report the corresponding attack success rate.

The results are summarized in Table VII, where the detection threshold is set to maintain an FPR of around 5%. Increasing the candidate budget generally improves ASR, but the gain quickly saturates while the attack cost grows substantially. Increasing the budget from 10 to 500 requires generating and evaluating 50 times more variants per sample. Moreover, increasing the budget from 100 to 500 requires five times more candidates, but brings at most 0.6 percentage points additional ASR gain across all attacks and datasets, with many attacks showing no further improvement. These results indicate that HAD raises the cost of adaptive evasion, as additional search yields only limited and saturating gains.

2) Gradient-based adaptive attack: In the second setting, we consider a stronger white-box adversary with full access to the IDS classifier, HAD’s encoders, and threshold. The adversary directly optimizes the perturbation through the complete pipeline, aiming to push the sample toward the benign class while reducing its dispersion score below the threshold. The optimization objective jointly minimizes the IDS classification loss and a dispersion penalty that encourages DIS(x + ζ) to fall below τ. We instantiate this attack using projected gradient descent (PGD): at each step, the perturbation is updated by back-propagating through the complete pipeline and then projected back to the valid feature domain. Following Definition 2 and prior work [24], we vary the perturbation magnitude from 0.01 to 0.1.

As shown in Fig. 3a, ASR increases as the perturbation magnitude grows, since the adversary directly optimizes against both the IDS classification objective and HAD’s detection mechanism. Nevertheless, HAD substantially limits ASR under small perturbation magnitudes, suggesting that dispersion-based detection introduces an additional barrier beyond the original IDS decision boundary. We further evaluate the threshold effect under the largest perturbation magnitude. As shown in Fig. 3b, the threshold provides a controllable ASR–FPR trade-off: a stricter threshold rejects more adaptive adversarial samples, while a more relaxed threshold reduces false alarms. This tunability allows practitioners to adjust the operating point according to deployment requirements.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/db7f245b83cbb17d6427a6475e2520faece8c246ff1d8323f8082e0cb2ac6f6c.jpg)

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/b6a52585936372a7d440001e5af1b87e2b72cb65b62626851e2a04e24d8f69e4.jpg)  
(a) ASR vs. magnitudes.  
(b) ASR–FPR trade-off of HAD.  
Fig. 3: Attack performance of gradient-based adaptive attacks.

Overall, HAD remains effective under both adaptive settings. The search-based attack shows that increasing the number of generated variants raises the attack cost but yields diminishing returns, while the gradient-based attack stress-tests HAD under a stronger white-box setting that jointly optimizes against the classifier, representation space, and detection threshold. These results demonstrate that HAD provides a tunable defense that increases the difficulty of adaptive evasion while allowing practitioners to balance robustness and FPR according to deployment requirements.

## E. Parameter Study (RQ5)

1) The Influence of $\rho \mathrm { : }$ The partition of the feature space into MFS and NFS is controlled by the allocation ratio $\rho =$ |MFS|/d, with $\rho = 0 . 5$ (the median EP split) used by default. To assess how this choice affects performance, we vary $\rho$ from 0.20 to 0.80 and report the accuracy under the C&W attack in Table VIII, keeping all other settings fixed and re-selecting the decision threshold τ at the same target FPR for each ratio. Across both datasets, performance remains stable over a central band of $\rho$ and degrades only toward the extremes. On NSL-KDD, the accuracy is highest for $\rho$ between 0.35 and 0.50, which differ by only 0.12%, and decreases by about 4.4% and 3.2% at $\rho = 0 . 2 0$ and $\rho = 0 . 8 0$ , respectively. On CIC-IDS, the accuracy peaks at $\rho = 0 . 5 0$ and varies by less than 0.8% across $\rho \in \{ 0 . 3 5 , 0 . 5 0 , 0 . 6 5 \}$ , exhibiting a wider plateau that is consistent with its larger and more redundant feature space. The degradation at the extremes reflects two effects. An overly small MFS retains too few manipulable features, limiting the diversity of surrogate samples and weakening the dispersion signal; an overly large MFS admits low-EP features into the manipulable subspace, making the two subspaces less distinct. A more selective MFS $( \rho = 0 . 3 5 )$ attains accuracy comparable to the median split on both datasets but provides only a marginal improvement. Since $\rho = 0 . 5$ lies within the stable region for both NSL-KDD and CIC-IDS, the median EP split provides a robust, dataset-independent default, and HAD is insensitive to moderate variations in the feature allocation ratio.

TABLE VIII: Accuracy under different allocation ratios $\rho .$

<table><tr><td> $\rho$ </td><td>0.20</td><td>0.35</td><td>0.50</td><td>0.65</td><td>0.80</td></tr><tr><td>NSL-KDD</td><td>0.8713</td><td>0.9164</td><td>0.9152</td><td>0.9019</td><td>0.8836</td></tr><tr><td>CIC-IDS</td><td>0.9381</td><td>0.9545</td><td>0.9622</td><td>0.9578</td><td>0.9513</td></tr></table>

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/6b77858b4b88ba4bde41e51681b432114fc545a187936e858079a2b31672e8bd.jpg)

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/3d7133eea883a2468d33ab6fb9be38277022af73c7a7ef814364f3244e1a5718.jpg)  
(a) NSL-KDD dataset.  
(b) CIC-IDS dataset.  
Fig. 4: The influence of perturbation rate.

2) The Influence of $\sigma { : }$ To evaluate the impact of the perturbation rate $\sigma ,$ we vary σ from 0.1 to 1 and assess overall performance using the accuracy metric, with the margin δ fixed at 1. The results are illustrated in Fig. 4. Recall that σ controls the extent of adversarial features introduced into the generated surrogate samples. By incorporating these features into malicious traffic, the generated surrogate samples aim to mislead the model’s classification. However, extreme values of $\sigma$ can hinder the effectiveness of the method. Specifically, excessively high values may lead to the generation of surrogate samples that do not adequately represent true adversarial patterns, thereby reducing their utility in training. On the other hand, excessively low values may yield surrogate samples that are too similar to the original malicious instances, limiting the ability of the HAD to effectively learn the hierarchical relationships among benign, malicious, and adversarial samples.

Despite variations across datasets and attack types, some common trends emerge. For the NSL-KDD dataset, accuracy initially increases with the perturbation rate, reaching a peak before declining as σ continues to grow. In contrast, the CIC-IDS dataset shows a preference for higher perturbation rates, indicating that its larger feature space benefits from a more aggressive perturbation strategy. Based on these observations, we determined optimal perturbation rates for subsequent experiments: 0.5 for NSL-KDD and 0.9 for CIC-IDS. These settings strike a balance, ensuring that surrogate samples effectively represent adversarial behaviors without compromising the integrity of the network traffic.

3) The Influence of δ and $\tau :$ In the hierarchical contrastive learning stage, two hyperparameters play a key role in model performance: the margin δ and the decision threshold τ . The margin δ regulates the separation between benign, malicious, and surrogate samples in the representation space, while τ is applied at inference phase to determine the classification boundary. These parameters are interdependent; in particular, a smaller margin typically corresponds to a lower optimal threshold. To examine their effects, we vary the margin over $\delta \in \{ 0 . 5 , 1 , 5 , 1 0 \}$ and adjust the threshold within the range $\tau \in [ 0 . 1 \delta , 0 . 9 \delta ]$ . The results are shown in Fig. 5.

The results reveal a clear relationship between the margin and the threshold. For instance, when $\delta = 1$ , both datasets achieve optimal performance with τ in the range of 0.3δ to 0.5δ. Smaller margins, such as $\delta = 0 . 5$ on NSL-KDD, fail to enforce sufficiently distinct hierarchical relationships, resulting in degraded performance. In contrast, larger margins increase the range of viable thresholds, making parameter selection more challenging. Based on this trade-off, we set δ = 1 for both datasets, as it provides a balanced separation while maintaining a stable and manageable threshold range.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/ddb1473174e3ac1da874cb0f7a302ffdcbb82704324008a601f167302692795c.jpg)

(a) Accuracy on NSL-KDD dataset.  
![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/716a82442980e4c93aa2d2664ad621ac67c6b716ad5ccff9474c80b12f1d3d51.jpg)  
(b) Accuracy on CIC-IDS dataset.  
Fig. 5: The influence of margin and threshold.

TABLE IX: Component ablation under the C&W attack.

<table><tr><td rowspan="2">FSP</td><td rowspan="2">SSG</td><td colspan="3">HCL</td><td colspan="2">NSL-KDD</td><td colspan="2">CIC-IDS</td></tr><tr><td> $\mathcal{L}_b$ </td><td> $\mathcal{L}_s$ </td><td> $\mathcal{L}_m$ </td><td>TPR</td><td>ACC</td><td>TPR</td><td>ACC</td></tr><tr><td>○</td><td>●</td><td>●</td><td>●</td><td>●</td><td>0.3356</td><td>0.6020</td><td>0.5287</td><td>0.6645</td></tr><tr><td>●</td><td>○</td><td>●</td><td>●</td><td>●</td><td>0.8307</td><td>0.8691</td><td>0.8432</td><td>0.8558</td></tr><tr><td>●</td><td>●</td><td>○</td><td>○</td><td>●</td><td>0.0635</td><td>0.5676</td><td>0.4464</td><td>0.7163</td></tr><tr><td>●</td><td>●</td><td>○</td><td>●</td><td>○</td><td>0.7110</td><td>0.7376</td><td>0.6556</td><td>0.8268</td></tr><tr><td>●</td><td>●</td><td>●</td><td>○</td><td>○</td><td>0.8358</td><td>0.8834</td><td>0.8529</td><td>0.8662</td></tr><tr><td>●</td><td>●</td><td>○</td><td>●</td><td>●</td><td>0.8772</td><td>0.8730</td><td>0.9315</td><td>0.9298</td></tr><tr><td>●</td><td>●</td><td>●</td><td>○</td><td>●</td><td>0.8554</td><td>0.8268</td><td>0.8771</td><td>0.8638</td></tr><tr><td>●</td><td>●</td><td>●</td><td>●</td><td>○</td><td>0.8957</td><td>0.9015</td><td>0.9598</td><td>0.9462</td></tr><tr><td>●</td><td>●</td><td>●</td><td>●</td><td>●</td><td>0.9008</td><td>0.9152</td><td>0.9736</td><td>0.9622</td></tr></table>

• with, ◦ without; FSP, SSG, and HCL are abbreviations of each stage.

## F. Ablation Study (RQ5)

1) Contribution of Components: We conduct an ablation study to evaluate the contribution of different objectives to the model’s performance under the C&W attack. Specifically, we test various combinations of the loss functions $\mathcal { L } _ { b } , \mathcal { L } _ { s } ,$ and ${ \mathcal { L } } _ { m }$ , which correspond to learning relationships among benign, surrogate, and malicious samples, respectively. The results in Table IX demonstrate the necessity of modeling all three relationships for optimal performance.

When examining individual objectives, it becomes evident that modeling a single relationship is insufficient. For instance, using only ${ \mathcal { L } } _ { m }$ yields negligible accuracy on both datasets, as it fails to capture the necessary relationships with benign or surrogate samples. In contrast, incorporating $\mathcal { L } _ { b }$ significantly improves accuracy by 25.9% on NSL-KDD and 14.8% on CIC-IDS, underscoring the importance of benignsample modeling. Additionally, combining two objectives further enhances the model’s performance, providing strong evidence that the designed objectives effectively guide the learning of hierarchical relationships among different types of samples. When all three loss functions, $\mathcal { L } _ { b } , \mathcal { L } _ { s } .$ , and $\mathcal { L } _ { m } ,$ are utilized together, the model achieves the best performance. This finding demonstrates that the hierarchical relationship between benign, malicious, and adversarial (surrogate) samples is crucial for robust learning. Regarding the balance coefficient among these objectives, our experiments indicate that HAD performs best among all ablation variants when all three objectives are considered simultaneously. Thus, for simplicity and practical implementation, we recommend setting balance coefficients $\lambda _ { b } ,$ $\lambda _ { s } ,$ and $\lambda _ { m }$ to 1.

TABLE X: Robustness and validity of the EP-based feature partition. Γ and $\Omega _ { 1 0 }$ measure the agreement between each variant and the proposed EP partition, while TPR at FPR= 5% and ACC measure downstream defense performance.

<table><tr><td rowspan="2">Method</td><td colspan="4">NSL-KDD</td><td colspan="4">CIC-IDS</td></tr><tr><td> $\Gamma$ </td><td> $\Omega_{10}$ </td><td>TPR</td><td>ACC</td><td> $\Gamma$ </td><td> $\Omega_{10}$ </td><td>TPR</td><td>ACC</td></tr><tr><td>EP</td><td>1.00</td><td>1.00</td><td>0.9008</td><td>0.9152</td><td>1.00</td><td>1.00</td><td>0.9736</td><td>0.9622</td></tr><tr><td>EP-RD</td><td>0.87</td><td>0.90</td><td>0.9006</td><td>0.9147</td><td>0.91</td><td>0.80</td><td>0.9778</td><td>0.9634</td></tr><tr><td>EP-BA</td><td>0.85</td><td>0.80</td><td>0.8914</td><td>0.9012</td><td>0.83</td><td>0.60</td><td>0.9611</td><td>0.9449</td></tr><tr><td>IMP.</td><td>0.53</td><td>0.30</td><td>0.8317</td><td>0.8725</td><td>0.44</td><td>0.20</td><td>0.9043</td><td>0.8928</td></tr></table>

2) Robustness of EP: We further analyze whether the proposed Evasion Potential (EP) score provides a stable and meaningful feature partition. We keep the HAD architecture and training procedure unchanged, and only replace the feature partitioning rule with three variants. EP-RD (Robust Dispersion) replaces the max–min SHAP range with a trimmed SHAP spread, computed as the difference between the $9 5 ^ { \mathrm { t h } }$ and $5 ^ { \mathrm { t h } }$ percentiles, to test sensitivity to extreme SHAP values. EP-BA (Balanced Activation) replaces the global maliciousactivation frequency with a class-balanced activation score averaged over attack categories, to test whether rare-attack features are diluted by class imbalance. IMP. ranks features only by mean absolute SHAP values, representing a standard explainability-based feature selection baseline. For each variant, we report two agreement measures with the proposed EP partition: rank agreement Γ and top-10 overlap $\Omega _ { 1 0 }$ . We also report downstream adversarial-sample detection performance using TPR at FPR= 5%, and intrusion-detection performance using ACC. The results are shown in Table X.

The results in Table X show that EP provides a robust and practical feature partition. EP-RD produces a partition highly consistent with EP, with Γ above 0.87 on both datasets, while maintaining nearly identical downstream performance. This indicates that the partition is not mainly determined by isolated extreme SHAP values. EP-BA also yields a partition close to EP, with Γ above 0.83, and preserves competitive TPR and ACC under class-balanced activation, suggesting that the global malicious-activation term remains stable under class imbalance. Since EP does not rely on fine-grained attackcategory labels, it provides a general and deployment-friendly way to estimate the feature subspace relevant to adversarial evasion. In contrast, the importance-only baseline produces a less consistent partition and clear performance degradation. Overall, EP balances simplicity and robustness by jointly considering feature sensitivity and malicious-side activation for constructing the MFS/NFS partition.

TABLE XI: Temporal-shift generalization on AnoShift.

<table><tr><td>Attack</td><td colspan="3">None</td><td colspan="3">C&amp;W</td><td colspan="3">IDSGAN</td><td colspan="3">ETA</td><td colspan="3">Overall</td></tr><tr><td>Split</td><td>IID</td><td>NEAR</td><td>FAR</td><td>IID</td><td>NEAR</td><td>FAR</td><td>IID</td><td>NEAR</td><td>FAR</td><td>IID</td><td>NEAR</td><td>FAR</td><td>IID</td><td>NEAR</td><td>FAR</td></tr><tr><td>DNN</td><td>0.9404</td><td>0.9430</td><td>0.7662</td><td>0.6482</td><td>0.6687</td><td>0.6379</td><td>0.6893</td><td>0.6797</td><td>0.6452</td><td>0.6957</td><td>0.7008</td><td>0.6545</td><td>0.6777</td><td>0.6831</td><td>0.6459</td></tr><tr><td>DNN+HAD</td><td>0.9412</td><td>0.9447</td><td>0.7784</td><td>0.9179</td><td>0.9221</td><td>0.7201</td><td>0.9039</td><td>0.8968</td><td>0.7043</td><td>0.9280</td><td>0.8552</td><td>0.7679</td><td> $0.9166 \uparrow 0.24$ </td><td> $0.8914 \uparrow 0.21$ </td><td> $0.7308 \uparrow 0.08$ </td></tr><tr><td>RF</td><td>0.9458</td><td>0.9441</td><td>0.7666</td><td>0.7315</td><td>0.7656</td><td>0.6694</td><td>0.8193</td><td>0.7508</td><td>0.6718</td><td>0.8604</td><td>0.8472</td><td>0.7120</td><td>0.8037</td><td>0.7879</td><td>0.6844</td></tr><tr><td>RF+HAD</td><td>0.9497</td><td>0.9510</td><td>0.7790</td><td>0.9251</td><td>0.9163</td><td>0.7679</td><td>0.9348</td><td>0.9012</td><td>0.7372</td><td>0.9194</td><td>0.9116</td><td>0.7747</td><td> $0.9264 \uparrow 0.12$ </td><td> $0.9097 \uparrow 0.12$ </td><td> $0.7599 \uparrow 0.08$ </td></tr><tr><td>GNB</td><td>0.8341</td><td>0.8561</td><td>0.7997</td><td>0.7509</td><td>0.7670</td><td>0.7475</td><td>0.7062</td><td>0.7398</td><td>0.7121</td><td>0.7969</td><td>0.8115</td><td>0.7337</td><td>0.7513</td><td>0.7728</td><td>0.7311</td></tr><tr><td>GNB+HAD</td><td>0.8939</td><td>0.9386</td><td>0.7931</td><td>0.8556</td><td>0.9258</td><td>0.7724</td><td>0.8654</td><td>0.8895</td><td>0.7534</td><td>0.8886</td><td>0.9377</td><td>0.7814</td><td> $0.8699 \uparrow 0.12$ </td><td> $0.9177 \uparrow 0.14$ </td><td> $0.7691 \uparrow 0.04$ </td></tr></table>

## G. Complexity Analysis (RQ6)

We analyze the computational complexity of HAD for its three primary stages. Let n denote the number of samples and d the dimensionality of the features. In the feature space partition stage, SHAP values are computed for each feature across all training samples, with a tree-based explainer incurring a complexity of O(nd log n), while subsequent aggregation and sorting are negligible by comparison. In the surrogate sample generation stage, each malicious sample generates k surrogate samples through masked feature replacement and IDS evaluation, resulting in a complexity of $\mathcal { O } ( n _ { m } k d + n _ { m } k C _ { \mathrm { i d s } } )$ where $n _ { m }$ is the number of malicious samples and $C _ { \mathrm { i d s } }$ is the cost of one IDS evaluation. Since the cost of model evaluation $C _ { \mathrm { i d s } }$ typically exceeds that of masked feature replacement, we can simplify this complexity to $\mathcal { O } ( n _ { m } k C _ { \mathrm { i d s } } )$ . For hierarchical contrastive learning, each sample is processed through two encoders, leading to a total complexity of $\mathcal { O } ( 2 n C _ { \mathrm { e n c } } )$ for the forward passes. Here, $C _ { \mathrm { e n c } }$ denotes the computational cost associated with processing one sample through the encoders, which may include operations such as matrix multiplications and activation functions. Additional costs arise from loss calculations: $\mathcal { O } ( n _ { b } )$ for benign samples and $\mathcal { O } ( n _ { s } n _ { b } + n _ { s } n _ { m } )$ for pairwise contrastive losses. Generally, mini-batch training maintains these costs in a near-linear range in practice. During online inference, HAD requires only a forward pass through both encoders and dispersion evaluation, resulting in a persample complexity of $\mathcal { O } ( 2 C _ { \mathrm { e n c } } )$

We further measured the runtime of HAD on the NSL-KDD dataset, observing a training time of 48.5s per epoch and a total inference time of 3.8s for the entire test set with 22,544 samples. This result indicates that HAD is computationally efficient for both offline training and online inference, with a modular design that facilitates seamless integration into existing IDS pipelines at an acceptable cost.

## VII. EVALUATION UNDER REAL-WORLD DRIFT

The experiments above demonstrate the effectiveness of HAD on standard IDS benchmarks. To evaluate its robustness in realistic scenarios, we conduct an evaluation on AnoShift [57], a distribution-shift benchmark built upon ten years of realworld network traffic. This setting allows us to examine HAD under traffic evolution, where the test distribution gradually deviates from the traffic observed during training.

## A. Evaluation Protocol

AnoShift partitions the Kyoto-2006+ traffic into three temporal regimes over a ten-year period: IID (2006–2010), NEAR (2011–2013), and FAR (2014–2015). We use IID to train the IDS classifier, the HAD encoders, and the detection threshold τ, and evaluate on IID, NEAR, and FAR without re-fitting. Thus, IID and NEAR cover the first eight years of traffic evolution and represent moderate long-term drift, while FAR corresponds to a more severe temporal shift. All preprocessing transformations are fitted only on IID and then applied unchanged to NEAR and FAR. We report F1-score as the main metric. Following the threat model in § III-B, we evaluate the clean setting (None) and three representative attacks: C&W [9], IDSGAN [18], and ETA [22].

## B. Temporal Shift Generalization across Backbones

In this section, we integrate HAD with three representative backbones: DNN, RF, and GNB classifiers. The HAD encoders and threshold are trained once on the IID split and shared across all backbones.

Table XI reports the F1-score across IID, NEAR, and FAR. The results show that HAD improves the overall performance of all three backbones, with the most evident gains under adversarial settings. The original classifiers suffer substantial performance degradation under attacks, while the HAD enhanced systems retain higher F1-scores. The results also reveal the impact of temporal drift. On IID and NEAR, HAD maintains stable gains across different backbones, indicating that the learned dispersion structure remains effective under moderate traffic evolution. On FAR, however, the performance of all backbones decreases noticeably, suggesting that the traffic distribution has shifted substantially from the training period. In this setting, HAD still improves the base classifiers, but the gain becomes smaller because the underlying IDS classifiers themselves are affected by severe temporal drift. These results further indicate that HAD can be integrated with different IDS backbones, supporting its use as a flexible supplementary detection layer.

TABLE XII: Drift Adaptation under FAR split.

<table><tr><td rowspan="2">Budget</td><td colspan="4">Dispersion</td><td colspan="3">Performance</td></tr><tr><td>Benign</td><td>Surrogate</td><td>Adversarial</td><td>Malicious</td><td>C&amp;W</td><td>IDSGAN</td><td>ETA</td></tr><tr><td>0</td><td>0.846</td><td>0.449</td><td>0.574</td><td>0.969</td><td>0.7111</td><td>0.6692</td><td>0.7091</td></tr><tr><td>50</td><td>0.656</td><td>0.477</td><td>0.514</td><td>0.958</td><td>0.7869</td><td>0.7871</td><td>0.8204</td></tr><tr><td>100</td><td>0.361</td><td>0.493</td><td>0.513</td><td>0.942</td><td>0.8098</td><td>0.7836</td><td>0.8181</td></tr><tr><td>200</td><td>0.272</td><td>0.497</td><td>0.486</td><td>0.939</td><td>0.8117</td><td>0.7617</td><td>0.7817</td></tr><tr><td>500</td><td>0.219</td><td>0.489</td><td>0.481</td><td>0.895</td><td>0.7710</td><td>0.7632</td><td>0.7726</td></tr><tr><td>1000</td><td>0.139</td><td>0.485</td><td>0.471</td><td>0.875</td><td>0.7666</td><td>0.7645</td><td>0.7743</td></tr></table>

## C. Adaptation to Extreme Shift

The results in § VII-B show that HAD remains effective under moderate temporal drift, but its performance decreases on the FAR split, where the traffic distribution deviates substantially from the IID training period. To better understand this degradation, we further inspect the dispersion behavior on FAR before adaptation, corresponding to the zero-budget setting in Table XII. The results show that FAR benign traffic no longer forms a clearly compact low-dispersion reference and becomes closer to the high-dispersion region associated with malicious traffic. This indicates a normality drift [60]: over several years, the concept of benign traffic changes substantially. Such drift not only affects the underlying IDS classifiers, but also makes FAR benign traffic less aligned with the compact benign reference learned from IID. In contrast, surrogate and adversarial samples remain close in dispersion, suggesting that HAD’s characterization of evasion behavior is still largely preserved, while the benign reference distribution has shifted.

This observation motivates a lightweight drift adaptation strategy. Instead of retraining the entire defense, we re-anchor the benign reference using a small amount of benign traffic from the FAR split, with malicious samples from IID serving as the margin anchor. This strategy is practical for deployment, as benign traffic accumulates continuously and can often be collected from trusted operation windows. The adaptation budget denotes the number of FAR benign samples used for recalibration. As shown in Table XII, a small adaptation budget substantially improves the dispersion ordering: benign dispersion decreases sharply, adversarial samples remain separated from benign traffic, and the F1-score under attacks improves accordingly. However, larger budgets do not always bring further gains, suggesting that a moderate adaptation budget is preferable in practice. Overall, these results show that HAD is robust to moderate distribution drift, and that when severe drift occurs, its hierarchical relationships can still be recalibrated using only a small amount of newly collected benign traffic, without requiring labels for future attacks.

## VIII. DISCUSSION

## A. Analysis of Feature Partitions

To partition the feature space into manipulable and nonmanipulable subsets, we compute the Evasion Potential (EP) for each feature, as defined in § IV-A. Table XIII presents the five features with the highest and lowest EP values in the CIC-IDS dataset, namely H-5 and L-5, respectively.

Features with high EP, such as Bwd Packet Length, Bwd IAT Mean, and Packet Length Variance, capture behavioral patterns strongly associated with malicious traffic, including abnormal packet sizes, bursty communication, and irregular flow dynamics. These features frequently contribute to malicious predictions and are therefore more attractive for evasionoriented manipulation. In contrast, low-EP features such as Bwd PSH Flags, Bwd URG Flags, and Fwd Avg Bytes/Bulk either appear rarely or overlap substantially with benign behaviors, making them less useful for efficient evasion. This result supports the use of EP for constructing the MFS/NFS partition used in downstream hierarchical contrastive learning.

## B. Surrogate–Adversarial Alignment Analysis

The hierarchical contrastive objective in HAD assumes that surrogate samples capture the dispersion behavior of adversarial evasion. To examine this assumption, we analyze whether real adversarial samples fall into a similar dispersion region as HAD’s surrogate samples. The analysis is conducted on the AnoShift IID split with three representative attacks: C&W, IDSGAN, and ETA.

We compare surrogate samples with benign samples, real adversarial samples, and original malicious samples using two complementary measurements: distribution similarity, which measures the overlap between two dispersion distributions, and normalized distribution distance, which measures the Wasserstein distance from surrogate samples to another group normalized by the benign–surrogate distance. As shown in Fig. 6, real adversarial samples have high distribution similarity with surrogate samples and small normalized distance from them, while benign and malicious samples are much less aligned. This indicates that HAD’s surrogate samples occupy a dispersion region close to real attack-generated adversarial samples and distinct from benign or malicious traffic.

To further visualize the hierarchical relationship among different sample groups, we randomly sample 500 instances from each group and compute their dispersion scores according to Eq. 11. Figs. 6b–6d show that benign samples concentrate in the low-dispersion region, malicious samples mainly occupy the high-dispersion region, and both surrogate and real adversarial samples lie in the intermediate region with substantial overlap. This demonstrates that surrogate generation captures a general dispersion pattern of adversarial evasion, rather than an artifact specific to constructed surrogate samples.

Overall, this analysis validates the alignment between surrogate samples and real adversarial samples and supports the design of the hierarchical contrastive loss. HAD does not assume that surrogate samples exactly reproduce attack-specific perturbation traces in the original feature space. Instead, it only requires them to induce a dispersion pattern similar to that of real adversarial samples under HAD’s detection statistic. The observed alignment provides empirical evidence for this condition and justifies the use of surrogate samples to model adversarial evasion behavior.

## C. Limitations and Future Work

HAD demonstrates strong performance in detecting adversarial samples and improving IDS robustness, while its surrogate sample generation still leaves room for improvement. In this work, surrogate samples are generated over flow-level features to capture attack-agnostic evasion effects in the dispersion space, rather than to reproduce executable packet-level traces. In addition, only MFS are perturbed, as NFS are assumed to mainly reflect intrinsic, functionality-related properties of traffic that a functional evasion attack must largely preserve. Although the attacker in our evaluation is not restricted by the MFS/NFS partition, an adversary that deliberately concentrates perturbations on NFS, either by sacrificing traffic legitimacy or through functionality-preserving modifications in a specific environment, may weaken the cross-subspace consistency on which the dispersion metric relies. Future work could enhance surrogate generation by incorporating protocol-aware feature dependencies and recomputing derived traffic statistics after perturbation, as well as by allowing constrained perturbations on NFS or randomizing the MFS/NFS partition.

TABLE XIII: Feature partition results on the CIC-IDS dataset.

<table><tr><td>EP Rank</td><td>Feature Name</td><td>Description</td></tr><tr><td rowspan="5">H-5</td><td>Bwd Packet Length</td><td>The size of data packets in the backward direction (server-to-client).</td></tr><tr><td>Bwd IAT Mean</td><td>Average time interval between consecutive backward packets.</td></tr><tr><td>Bwd IAT Std</td><td>Standard deviation of backward packet inter-arrival times.</td></tr><tr><td>Packet Length Variance</td><td>Variability in packet sizes across a flow.</td></tr><tr><td>Min Packet Length</td><td>The smallest packet size observed in a flow.</td></tr><tr><td rowspan="5">L-5</td><td>Bwd PSH Flags</td><td>Frequency of &quot;Push&quot; flags in backward packets.</td></tr><tr><td>Bwd URG Flags</td><td>Frequency of &quot;Urgent&quot; flags in backward packets.</td></tr><tr><td>Fwd Avg Bytes/Bulk</td><td>Average bytes per bulk transfer in the forward direction.</td></tr><tr><td>Fwd Avg Packets/Bulk</td><td>Average packets per bulk transfer in the forward direction.</td></tr><tr><td>Fwd Avg Bulk Rate</td><td>Rate of bulk data transfers in the forward direction.</td></tr></table>

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/a248ba13194fc0fe76b57ce0d233fae7e707d6bd1d38ad567cc8a3afdbcd49d1.jpg)  
(a) Distribution-level alignment.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/3c708c0b3143f5cb0a9372db9d6542888a053f43ce3e0e6beb247e5b43878f8f.jpg)  
(b) Dispersion under C&W.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/cf6ad0de5cf2e25585dc75437d853876ef0ce10d29569a415bdbacb2b58989d5.jpg)  
(c) Dispersion under IDSGAN.

![](../01-mineru-output/2026-TIFS-HAD__Hierarchical_Adversarial_Defense_for_Network_Intrusion_Detection/images/eecbe9f0cad1bf91bac2e595b83c240dc91fff0dc097d1814c3c4fca3d2b62fd.jpg)  
(d) Dispersion under ETA.  
Fig. 6: Alignment between surrogate and adversarial samples with respect to the dispersion metric.

Furthermore, HAD leverages the heuristic observation that benign traffic often forms a more compact reference than malicious traffic, but this density pattern is not assumed to be invariant under arbitrary temporal drift. As shown in § VII, severe normality drift can weaken the compact benign reference, although HAD can be recalibrated using a small amount of newly collected benign traffic. In addition, since high-volume operational networks often require lower false-alarm rates, improving the detection sensitivity of HAD in the very-low-FPR regime remains an important direction.

Finally, LLM-assisted adversarial defense is a promising direction. LLMs and agent-based systems could help interpret traffic semantics, suggest feature constraints, or generate diverse surrogate perturbations, but they also introduce higher computational overhead and reliability risks in security-critical settings [61]. We therefore view them as complementary offline assistants, while HAD serves as a lightweight backbone for efficient online detection. Beyond network intrusion detection, the methodology of HAD, including feature space partition, surrogate modeling, and hierarchical contrastive learning, could also be extended to other security-sensitive domains such as malware detection and fraud analysis.

## IX. CONCLUSION

In this paper, we propose HAD, a novel framework that enhances the robustness of IDSs against adversarial evasion attacks. HAD is grounded in a systematic analysis of adversarial behavior and integrates three stages: feature space partition, surrogate sample generation, and hierarchical contrastive learning. By partitioning the feature space into manipulable and non-manipulable subspaces using the Evasion Potential, HAD identifies features more susceptible to manipulation. The generation of surrogate samples allows HAD to model the hierarchical relationships among benign, malicious, and adversarial traffic. Extensive experiments under various adversarial strategies demonstrate that HAD outperforms existing defense methods in detecting adversarial samples while maintaining high classification accuracy. Overall, HAD offers a significant step forward in building resilient IDSs capable of withstanding sophisticated adversarial threats.

## REFERENCES

[1] D. Chou and M. Jiang, “A survey on data-driven network intrusion detection,” ACM Computing Surveys, vol. 54, no. 9, pp. 1–36, 2021.

[2] L. Khan, M. Awad, and B. Thuraisingham, “A new intrusion detection system using support vector machines and hierarchical clustering,” The VLDB Journal, vol. 16, pp. 507–521, 2007.

[3] X. Li, W. Chen, Q. Zhang, and L. Wu, “Building auto-encoder intrusion detection system based on random forest feature selection,” Computers & Security, vol. 95, p. 101851, 2020.

[4] Y. Imrana, Y. Xiang, L. Ali, and Z. Abdul-Rauf, “A bidirectional LSTM deep learning approach for intrusion detection,” Expert Systems with Applications, vol. 185, p. 115524, 2021.

[5] L. Zhang, X. Yan, and D. Ma, “Efficient and effective in-vehicle intrusion detection system using binarized convolutional neural network,” in IEEE Conference on Computer Communications, 2024, pp. 2299–2307.

[6] S. Yang et al., “A lightweight approach for network intrusion detection based on self-knowledge distillation,” in IEEE International Conference on Communications, 2023, pp. 3000–3005.

[7] S. K. Amalapuram et al., “Augmented memory replay-based continual learning approaches for network intrusion detection,” in Advances in Neural Information Processing Systems, 2023.

[8] S. Yang, X. Zheng, J. Li, J. Xu, X. Zhang, and E. C. H. Ngai, “Selfsupervised adaptation method to concept drift for network intrusion detection,” IEEE Transactions on Dependable and Secure Computing, vol. 22, no. 6, pp. 7632–7646, 2025.

[9] N. Carlini and D. Wagner, “Towards evaluating the robustness of neural networks,” in 2017 IEEE Symposium on Security and Privacy (SP), 2017, pp. 39–57.

[10] Y. Chen, Q. Yin, Q. Li, Z. Liu, K. Xu, Y. Xu, M. Xu, Z. Liu, and J. Wu, “Learning with semantics: Towards a semantics-aware routing anomaly detection system,” in 33rd USENIX Security Symposium (USENIX Security 24), 2024, pp. 5143–5160.

[11] K. Grosse, L. Bieringer, T. R. Besold, and A. M. Alahi, “Towards more practical threat models in artificial intelligence security,” in 33rd USENIX Security Symposium (USENIX Security 24), 2024, pp. 4891–4908.

[12] D. Arp, E. Quiring, F. Pendlebury, A. Warnecke, F. Pierazzi, C. Wressnegger, L. Cavallaro, and K. Rieck, “Dos and don’ts of machine learning in computer security,” in 31st USENIX Security Symposium (USENIX Security 22), 2022, pp. 3971–3988.

[13] J. Chen, X. Gao, R. Deng, Y. He, C. Fang, and P. Cheng, “Generating adversarial examples against machine learning-based intrusion detector in industrial control systems,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 3, pp. 1810–1825, 2020.

[14] C. Zhang, X. Costa-Perez, and P. Patras, “Adversarial attacks against deep learning-based network intrusion detection systems and defense mechanisms,” IEEE/ACM Transactions on Networking, vol. 30, no. 3, pp. 1294–1311, 2022.

[15] K. He, D. D. Kim, and M. R. Asghar, “Adversarial machine learning for network intrusion detection systems: A comprehensive survey,” IEEE Communications Surveys & Tutorials, vol. 25, no. 1, pp. 538–566, 2023.

[16] I. Debicha, B. Cochez, T. Kenaza, T. Debatty, J.-M. Dricot, and W. Mees, “Adv-Bot: Realistic adversarial botnet attacks against network intrusion detection systems,” Computers & Security, vol. 129, p. 103176, 2023.

[17] A. Chernikova and A. Oprea, “FENCE: Feasible evasion attacks on neural networks in constrained environments,” ACM Transactions on Privacy and Security, vol. 25, no. 4, pp. 1–34, 2022.

[18] Z. Lin, Y. Shi, and Z. Xue, “IDSGAN: Generative adversarial networks for attack generation against intrusion detection,” in Pacific-Asia Conference on Knowledge Discovery and Data Mining, 2022, pp. 79–91.

[19] D. Han, Z. Wang, Y. Zhong, W. Chen, J. Yang, S. Lu, X. Shi, and X. Yin, “Evaluating and improving adversarial robustness of machine learning-based network intrusion detectors,” IEEE Journal on Selected Areas in Communications, vol. 39, no. 8, pp. 2632–2647, 2021.

[20] M. Wang, N. Yang, N. J. Forcade-Perkins, and N. Weng, “ProGen: Projection-based adversarial attack generation against network intrusion detection,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 5476–5491, 2024.

[21] D. Wu, B. Fang et al., “Evading machine learning botnet detection models via deep reinforcement learning,” in ICC 2019-2019 IEEE International Conference on Communications, 2019, pp. 1–6.

[22] H. Zhang, D. Han et al., “Explainable and transferable adversarial attack for ML-based network intrusion detectors,” IEEE Transactions on Dependable and Secure Computing, vol. 22, no. 5, pp. 5090–5107, 2025.

[23] E. Alhajjar, P. Maxwell, and N. Bastian, “Adversarial machine learning in network intrusion detection systems,” Expert Systems with Applications, vol. 186, p. 115782, 2021.

[24] N. Wang, Y. Chen et al., “MANDA: On adversarial example detection for network intrusion detection system,” IEEE Transactions on Dependable and Secure Computing, vol. 20, no. 2, pp. 1139–1153, 2023.

[25] M. J. Hashemi and E. Keller, “Enhancing robustness against adversarial examples in network intrusion detection systems,” in 2020 IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN), 2020, pp. 37–43.

[26] A. Paya, S. Arroni et al., “APOLLON: A robust defense system against adversarial machine learning attacks in intrusion detection systems,” Computers & Security, vol. 136, p. 103546, 2024.

[27] W. Xiong et al., “AIDTF: Adversarial training framework for network intrusion detection,” Computers & Security, vol. 128, p. 103141, 2023.

[28] S. Gowal, S.-A. Rebuffi, O. Wiles, F. Stimberg, D. A. Calian, and T. A. Mann, “Improving robustness using generated data,” in Advances in Neural Information Processing Systems, vol. 34, 2021, pp. 4218–4233.

[29] N. D. Singh, F. Croce, and M. Hein, “Revisiting adversarial training for ImageNet: Architectures, training and generalization across threat models,” in Advances in Neural Information Processing Systems, vol. 36, 2023, pp. 13 931–13 955.

[30] J. Morris, E. Lifland, J. Y. Yoo et al., “TextAttack: A framework for adversarial attacks, data augmentation, and adversarial training in NLP,”

in Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, 2020, pp. 119–126.

[31] P. T. Duy, N. H. Khoa, A. G.-T. Nguyen et al., “DIGFuPAS: Deceive IDS with GAN and function-preserving on adversarial samples in SDN enabled networks,” Computers & Security, vol. 109, p. 102367, 2021.

[32] K. He, D. D. Kim, and M. R. Asghar, “NIDS-Vis: Improving the generalized adversarial robustness of network intrusion detection system,” Computers & Security, vol. 145, p. 104028, 2024.

[33] H. C. Moon, S. Joty, and X. Chi, “GradMask: Gradient-guided token masking for textual adversarial example detection,” in Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 2022, pp. 3603–3613.

[34] A. Shafahi, M. Najibi, M. A. Ghiasi, Z. Xu, J. Dickerson, C. Studer, L. S. Davis, G. Taylor, and T. Goldstein, “Adversarial training for free!” in Advances in Neural Information Processing Systems, vol. 32, 2019.

[35] N. Papernot, P. McDaniel et al., “Distillation as a defense to adversarial perturbations against deep neural networks,” in 2016 IEEE Symposium on Security and Privacy (SP), 2016, pp. 582–597.

[36] A. Athalye et al., “Obfuscated gradients give a false sense of security: Circumventing defenses to adversarial examples,” in International Conference on Machine Learning, 2018, pp. 274–283.

[37] H. Zhang, Y. Yu et al., “Theoretically principled trade-off between robustness and accuracy,” in International Conference on Machine Learning, 2019, pp. 7472–7482.

[38] M. Nasr et al., “Defeating DNN-based traffic analysis systems in realtime with blind adversarial perturbations,” in 30th USENIX Security Symposium (USENIX Security 21), 2021, pp. 2705–2722.

[39] Y. Xu, Y. Sun et al., “Exploring and exploiting decision boundary dynamics for adversarial robustness,” in International Conference on Learning Representations, 2023.

[40] R. Sheatsley, N. Papernot, M. J. Weisman, G. Verma, and P. McDaniel, “Adversarial examples for network intrusion detection systems,” Journal of Computer Security, vol. 30, no. 5, pp. 727–752, 2022.

[41] N. Papernot, P. McDaniel, and I. Goodfellow, “Transferability in machine learning: From phenomena to black-box attacks using adversarial samples,” arXiv preprint arXiv:1605.07277, 2016.

[42] X. Yuan, S. Han et al., “A simple framework to enhance the adversarial robustness of deep learning-based intrusion detection system,” Computers & Security, vol. 137, p. 103644, 2024.

[43] W. He et al., “Decision boundary analysis of adversarial examples,” in International Conference on Learning Representations, 2018.

[44] J. Vitorino, I. Praça, and E. Maia, “SoK: Realistic adversarial attacks and defenses for intelligent network intrusion detection,” Computers & Security, vol. 134, p. 103433, 2023.

[45] I. J. Goodfellow, J. Shlens, and C. Szegedy, “Explaining and harnessing adversarial examples,” arXiv preprint arXiv:1412.6572, 2014.

[46] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu, “Towards deep learning models resistant to adversarial attacks,” in International Conference on Learning Representations, 2018.

[47] J. Chen, M. I. Jordan, and M. J. Wainwright, “HopSkipJumpAttack: A query-efficient decision-based attack,” in 2020 IEEE Symposium on Security and Privacy (SP), 2020, pp. 1277–1294.

[48] P.-Y. Chen, H. Zhang, Y. Sharma, J. Yi, and C.-J. Hsieh, “ZOO: Zeroth order optimization based black-box attacks to deep neural networks without training substitute models,” in Proceedings of the 10th ACM Workshop on Artificial Intelligence and Security, 2017, pp. 15–26.

[49] R. Sheatsley, B. Hoak, E. Pauley, and P. McDaniel, “The space of adversarial strategies,” in 32nd USENIX Security Symposium (USENIX Security 23), 2023, pp. 3745–3761.

[50] Y. Qing et al., “Low-quality training data only? a robust framework for detecting encrypted malicious network traffic,” in 31st Annual Network and Distributed System Security Symposium (NDSS), 2024.

[51] M. Tavallaee, E. Bagheri, and others., “A detailed analysis of the KDD CUP 99 data set,” in 2009 IEEE Symposium on Computational Intelligence for Security and Defense Applications, 2009, pp. 1–6.

[52] G. Engelen, V. Rimmer, and W. Joosen, “Troubleshooting an intrusion detection dataset: The CICIDS2017 case study,” in 2021 IEEE Security and Privacy Workshops (SPW), 2021, pp. 7–12.

[53] L. Van der Maaten and G. Hinton, “Visualizing data using t-SNE,” Journal of Machine Learning Research, vol. 9, no. 86, 2008.

[54] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” in Advances in Neural Information Processing Systems, 2017, pp. 4768–4777.

[55] L. Liu, G. Engelen, T. Lynar, D. Essam, and W. Joosen, “Error prevalence in NIDS datasets: A case study on CIC-IDS-2017 and CSE-CIC-IDS-2018,” in 2022 IEEE Conference on Communications and Network Security (CNS), 2022, pp. 254–262.

[56] I. Sharafaldin, A. H. Lashkari, A. A. Ghorbani et al., “Toward generating a new intrusion detection dataset and intrusion traffic characterization,” in International Conference on Information Systems Security and Privacy (ICISSP), 2018, pp. 108–116.

[57] M. Dragoi, E. Burceanu et al., “AnoShift: A distribution shift benchmark for unsupervised anomaly detection,” in Advances in Neural Information Processing Systems, vol. 35, 2022, pp. 32 854–32 867.

[58] T. Bai, J. Luo et al., “Recent advances in adversarial training for adversarial robustness,” in Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence, 2021, pp. 4312–4321.

[59] B. A. Alahmadi, L. Axon et al., “99% false positives: A qualitative study of SOC analysts’ perspectives on security alarms,” in 31st USENIX Security Symposium (USENIX Security 22), 2022, pp. 2783–2800.

[60] D. Han, Z. Wang et al., “Anomaly detection in the open world: Normality shift detection, explanation, and adaptation,” in 30th Annual Network and Distributed System Security Symposium (NDSS), 2023.

[61] S. Yang, X. Zheng, X. Zhang et al., “Large language models for network intrusion detection systems: Foundations, implementations, and future directions,” arXiv preprint arXiv:2507.04752, 2025.
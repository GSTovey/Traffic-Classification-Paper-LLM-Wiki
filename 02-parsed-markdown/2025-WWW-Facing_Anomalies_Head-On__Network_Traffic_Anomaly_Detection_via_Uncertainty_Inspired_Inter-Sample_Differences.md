# Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences

Xinglin Lian Xidian University Xi’an, China kenshin.lian24@gmail.com

Xovee Xu University of Electronic Science and Technology of China Chengdu, China xovee.xu@gmail.com

Chengtai Cao City University of Hong Kong Hong Kong, China chengtcao2-c@my.cityu.edu.hk

Yu Zheng Xidian University Xi’an, China yzheng@xidian.edu.cn

Yan Liu University of Electronic Science and Technology of China Chengdu, China yan.liu@std.uestc.edu.cn

Fan Zhou<sup>∗</sup> University of Electronic Science and Technology of China Chengdu, China fan.zhou@uestc.edu.cn

## Abstract

Network trafic anomaly detection is pivotal in cybersecurity, especially as data volume grows and security requirement intensifies. This study addresses critical limitations in existing reconstructionbased methods, which quantify anomalies relying on intra-sample diferences and struggle to detect drifted anomalies. In response, we propose a novel approach, the Uncertainty-Inspired Inter-Sample Diferences (UnDif) method, which leverages model uncertainty to enhance anomaly detection capabilities, particularly in scenarios in volving anomaly drift. By employing evidential learning, the UnDif model gathers evidence to minimize uncertainty in normal network trafic, enhancing its ability to diferentiate between normal and anomalous trafic. To overcome the limitations of intra-sample diference quantification in reconstruction-based methods, we pro pose a novel anomaly score based on inter-sample uncertainty deviation that directly quantifies the anomaly degree. Benefiting from a concise model design and parameterized uncertainty quan tification, UnDif achieves high eficiency. Extensive experiments on three benchmarks demonstrate UnDif’s superior performance in detecting both undrifted and drifted anomalies with minimal computational overhead.

## CCS Concepts

• Security and privacy → Intrusion detection systems; • Information systems → Trafic analysis.

## Keywords

Network Trafic Anomaly Detection; Uncertainty Quantification; Drifted Anomaly Detection; Zero-Positive Learning

<sup>∗</sup>Corresponding Authors.

ACM Reference Format: Xinglin Lian, Chengtai Cao, Yan Liu, Xovee Xu, Yu Zheng, and Fan Zhou. 2025. Facing Anomalies Head-On: Network Trafic Anomaly Detection via Uncertainty-Inspired Inter-Sample Diferences. In Proceedings of the ACM Web Conference 2025 (WWW ’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 10 pages. https://doi.org/10.1145/ 3696410.3714621

## 1 Introduction

Network trafic anomaly detection, a fundamental component of cybersecurity infrastructure [53], plays a pivotal role in identifying malicious activities across various network environments. As data volumes surge exponentially and security requirements are stringent, precisely identifying anomalous network trafic patterns has emerged as a critical imperative. This capability underpins multiple important applications, including enhancing the stability and reliability of network services [13, 32] and fortifying personal privacy protection mechanisms [25, 30].

Current literature on network trafic anomaly detection predominantly employs a reconstruction-based “zero-positive learning” paradigm [5, 21, 28, 53], which only reconstructs normal network trafic distributions during the training phase, typically leveraging architectures such as auto-encoder models [29]. Subsequently, during the inference phase, common practice for evaluating anomaly degrees of network trafic is to utilize a distance-based metric [3, 15, 34, 48, 53, 54], i.e., samples exhibiting significant distance deviation between their pre- and post-reconstruction representations are identified as anomalous network trafic, while those demonstrating minimal divergence are considered as normal network trafic (cf. left part of Figure 1(a)).

Despite the recent advancements in reconstruction-based methods for network trafic anomaly detection, an intrinsic limitation persists. These approaches fully rely on intra-sample diferences of pre- and post-reconstruction from an egocentric perspective while insuficiently leveraging inherent inter-sample diferences, i.e., the diverse distribution between normal and anomalous network trafic [21]. This limitation is exacerbated by the potential “identical shortcut” issue in reconstruction models [45]. Instead of capturing diferentiated characteristics of normal and anomalous patterns, reconstruction-based methods tend to converge on

![](images/95d0f5c5fc055529197c511f10a292dcdf5f52de25ffdb2aae818c9db2b03624.jpg)

(a) The limitations of existing reconstruction-based methods.  
![](images/a49fd499a80fe540c9cca8aa0867e97aa1a0befda39d368e176152f8a279b330.jpg)  
(b) The motivation of our UnDiff.  
Figure 1: Motivation for this work. (a) Existing methods en counter the “identical shortcut” issue, exemplified by the proximity of pre- and post-reconstruction drifted anomalies. (b) Our UnDif is based on uncertainty-inspired inter-sample diferences, facilitating direct anomaly identification.

Low Unce<sub>(b)</sub>Ua set of shortcut parameters that merely replicate the input as <sup>for</sup> <sup>In-Distri</sup><sub>Space</sub> <sup>c</sup>eoutput [33, 35]. This limitation becomes particularly salient in de-<sup>α</sup> intecting drifted anomalies, where the distribution of anomalous data β PHeadevolves over time. The right part of Figure 1(a) visualizes the pre-<sup>r</sup>aand post-reconstruction embedding of drifted anomalies using a <sup>High</sup> <sup>Unce</sup>t<sub>e</sub>state-of-the-art reconstruction-based model Trident [53]. Empir ical observations indicate that the pre- and post-reconstruction representations exhibit high proximity in the representation space. The intra-sample diferences do not satisfy the ideal institution of reconstruction-based methods, thereby significantly impeding the discrimination of drifted anomalies.

To address this limitation, we propose a novel Uncertainty Inspired Inter-Sample Diferences model (UnDif). UnDif leverages the concept of model uncertainty to enhance the discriminative capacity of anomaly detection systems, with particular emphasis on anomaly drift scenarios. As illustrated in Figure 1(b), the key intuition of our model is rooted in the diferential uncertainty characteristics exhibited by normal and anomalous trafic patterns. Normal samples, well-represented in the training data, manifest low model uncertainty. Conversely, anomalous samples, particularly drifted anomalies, induce higher uncertainty due to their deviation from the learned normal patterns [21]. In contrast to existing reconstruction-based methods, our proposed UnDif addresses the limitation above by directly facilitating inter-sample diferences rather than relying on the sub-optimal intra-sample quantification.

Central to our UnDif is a novel uncertainty learning module that quantifies model detection uncertainty. This module employs an evidential learning approach [6], acquiring evidence from training examples to construct an evidential distribution, facilitating robust uncertainty modeling for normal network trafic. Furthermore, we introduce explicit objectives to minimize uncertainty in normal network trafic during training. These objectives provide a more pronounced separation between normal and anomalous samples in the uncertainty space. To overcome the limitation of intra-sample disparity quantification in reconstruction-based methods, we fur ther propose an innovative uncertainty-inspired anomaly score that adequately leverages inter-sample distributional diferences for detecting anomalies. Notably, thanks to the concise design of the uncertainty learning module and the eficient parameterized uncertainty quantification technique, the enhancements we proposed above have negligible additional computational overhead. We conduct extensive experiments on real-world encrypted anomaly trafic datasets and evaluate the performance of UnDif in both undrifted and drifted anomaly detections. Empirical results verified the efectiveness of our proposed model in detection performance across both scenarios. In summary, our key contributions are threefold:

• We propose a novel uncertainty-based evidential detection framework from an inter-sample diference perspective. Unlike the suboptimal intra-sample diference quantification in existing methods, our approach better utilizes the prior knowledge that anomalies inherently deviate from normal patterns, achieving more efective anomaly detection, particularly in scenarios involving anomaly drift.

• We introduce an innovative uncertainty learning module and a new anomaly score. This module provides an eficient and robust method for capturing sample uncertainty, while the anomaly score efectively quantifies inter-sample diferences, significantly enhancing the discriminative capacity of the Normaldetection system.

• We conduct comprehensive empirical evaluations on three real-world anomaly network trafic datasets. The results <sup>Anomalous</sup>demonstrate the efectiveness of our framework, UnDif, in detecting both drifted and undrifted anomalies.

## 2 Related Work

## 2.1 Network Trafic Anomaly Detection

Anomaly detection, particularly zero-positive learning anomaly detection, has gained extensive attention. In this paradigm, only normal data are available during training, and samples that deviate from the learned model behavior are identified as anomalies during inference. Existing methods can be broadly categorized into three groups: distillation-based, statistics-based, and normalizing flow-based approaches [31]. Distillation-based methods focus on intra-sample diferences, utilizing a student-teacher architecture to compare the distilled disparities [50, 51]. Conversely, the statisticbased [4, 11] and normalizing flow-based methods [19, 37] aim to learn a mapping from an input domain to a low-dimensional distribution. These approaches quantify inter-sample diferences by analyzing deviations in the low-dimensional distribution. However, these methods, primarily designed for natural images, often encounter significant limitations when applied to trafic data. This is due to the unique characteristics of trafic images, such as redundant high-frequency information and disordered texture [29, 54].

Current network trafic anomaly detection methods mainly follow a reconstruction-based paradigm. These methods reconstruct the normal trafic during training and employ intra-sample diferences (i.e., disparities between pre- and post-reconstruction) to identify anomalies. A notable example is GANomaly [3], a prominent reconstruction framework that utilizes a discriminator network to improve normal sample modeling. MANomaly [48] introduce a dual autoencoder adversarial training strategy to enhance representation learning, while ARCADE [34] employ WGAN-GP optimization for more efective adversarial training. MFR [29] and MFAD [54] identify a critical “identical shortcut” issue in trafic reconstruction and utilize low-pass filtering to mitigate this problem. Trident [53] incorporates a U-Net structure to retain more detailed reconstruc tion information. Most anomaly detection methods for trafic data focus on enhancing the reconstruction quality of normal samples. However, these approaches often evade the “identical shortcut” issue inherent in reconstruction-based models. To overcome this limitation, we propose a novel paradigm based on inter-sample diferences. In contrast to the suboptimal intra-sample diferences employed by existing methods, we leverage the prior knowledge that anomalous samples inherently deviate from normal samples, achieving a more efective anomaly identification.

## 2.2 Uncertainty Learning

As deep learning models find increasingly widespread application across diverse domains, accuracy is no longer the only criterion for evaluation. In fields where safety is paramount, there is an urgent need for more trustworthy neural networks. Reliable uncertainty quantification emerges as a critical aspect in this context, as it measures the model’s confidence in its output.

As elucidated in the literature [1, 9, 18, 26, 36], two primary categories of uncertainties are associated with neural networks: data uncertainty and model uncertainty. Data uncertainty arises from noise or randomness in the input and can be reduced to zero with suficient training examples. For model uncertainty, Bayesian learning-based networks provide a mathematically grounded framework, albeit prohibitively expensive to implement and infer. Alter natively, Monte Carlo Dropout [17] approximates Bayesian infer ence on model parameters. Furthermore, leveraging the ensemble learning paradigm, Deep Ensemble [27] integrates multiple models for uncertainty estimation. To analyze data uncertainty, a unified Bayesian learning-based method [26] has been proposed to directly map input data to estimations of both data and model uncertainties. Uncertainty learning has also received attention in the field of anomaly detection, with approaches such as Bayesian learning [22] and its variational approximations [20, 23, 24, 46].

Recently, evidential learning has emerged as a promising uncer tainty quantification approach [22, 39, 41]. This method enables uncertainty estimation in a single model and forward pass with parameterized distributions. In this approach, a neural network outputs the hyperparameters of an evidential distribution, allowing the model to estimate both model and data uncertainties without requir ing sampling, thus enhancing the eficiency of uncertainty quantifi cation [6]. However, most existing works on evidential learning are designed for supervised learning in computer vision [22] and ne cessitate large volumes of labeled data to estimate the uncertainty distribution. This requirement does not fit the typical anomaly detection setting. Therefore, in this study, we explore the applica tion of evidential learning for quantifying the anomaly degree of network trafic in a zero-positive learning context.

## 3 Methodology

This section details our proposed uncertainty-inspired inter-sample diference method, UnDif. We describe the research problem and introduce a novel research scenario, anomaly drift. Subsequently, we explicate the requisite data processing modules. We then detail our proposed uncertainty learning module, designed to learn the uncertainty space, thereby facilitating the comparison of intersample distribution diferences. The schematic representation of our methodological pipeline is illustrated in Figure 2.

## 3.1 Problem Statement

Network Trafic Anomaly Detection. This work investigates the zero-positive learning anomaly detection problem in the context of network trafic analysis. Let ${ \cal { X } } = \{ { \bf { x } } _ { 1 } , { \bf { x } } _ { 2 } , . . . , { \bf { x } } _ { N } \}$ denote a set of � normal samples, where $\mathbf { x } _ { i } \in \mathbb { R } ^ { d }$ is a �-dimensional data instance. The objective of detection models is to learn the distributional patterns of normal samples during training. For inference, the model assigns an anomaly score to each test sample $\mathbf { x } _ { \mathrm { t e s t } } \in X _ { \mathrm { t e s t } }$ , where $\chi _ { \mathrm { t e s t } }$ represents the set of test samples. The magnitude of the anomaly score is positively correlated with the likelihood of a sample being identified as anomalous.

Drifted Anomaly Detection. The dynamic nature of network activities frequently leads to divergence in the distribution of testing data, a phenomenon known as concept drift [15]. This drift often results in the performance degradation of anomaly detection systems [21, 54]. Existing research on concept drift in anomaly detection primarily focuses on two scenarios: whole drift, where both normal and anomalous data experience drift [7, 8, 44, 53] and normal drift, where only normal data undergoes drift [21]. However, this study addresses a more realistic scenario: anomaly drift, wherein only anomalous data experience drift. This scenario is particularly relevant because, in real-world applications, normal network trafic patterns typically exhibit relative stability, whereas anomalous network trafic patterns often change due to the evolution of attack strategies. Consequently, our research emphasizes the generalization capability of the anomaly detection model when confronted with drifts in the distribution of anomalous data.

## 3.2 Data Preprocessing

Network trafic fundamentally manifests as a flow format comprising an ordered sequence of packets. In contrast to statistical features designed based on manual heuristics [34, 48], we directly utilize the original trafic packet information for network trafic modeling. This approach circumvents the introduction of bias associated with manually crafted features. A critical consideration in the data processing of network flows is the appropriate representation method, as it significantly influences the detection accuracy and computational overhead. In this study, we employ a Multi-Channel Trafic Image Construction strategy for trafic flow representation. This approach allows for a more comprehensive and nuanced capture of the multidimensional nature of network trafic.

Multi-Channel Trafic Image Construction. While image-based single packet processing has been widely adopted in network trafic anomaly detection [14, 54], the potential of flow-level image construction remains largely unexplored. Drawing inspiration from video anomaly detection methodology [49], which addresses spatiotemporal representation tasks, we propose a novel approach to network flow representation. In our method, we formulate each network flow as a multi-channel image analogous to a video frame sequence. The specific channel order is determined by the packets’ chronological arrival, preserving the flow’s temporal dimension. This approach ofers two significant advantages: (i) Dimensional

![](images/6da8fad8bb6fd6f2627221747b12c7fbcb0ee4dec41813a6a3f41906ef1755d2.jpg)  
Figure 2: Overall framework of UnDif. (a) Training: Uncertainty-Inspired Modeling Process. UnDif first extracts informative representations from normal network trafic. These refined representations are then utilized to instruct uncertainty parameters for uncertainty representation. (b) Inference: Anomaly Metric Process. UnDif directly outputs model uncertainty to quantify anomalies by assessing inter-sample diferences via a distribution prior that diferentiates normal and anomalous trafic.

Eficiency: By extending the representation along the channel di mension rather than width and height, we reduce the generation of subsequent high-dimensional feature maps. This design choice ensures enhanced inference speed. (ii) Informative Representation Preservation: Crucially, this approach adequately preserves infor mative representations as the contextual relationships between packets (represented as multi-channel images), reflecting the spa tiotemporal characteristics of network flows. This temporal and spatial information preservation is critical for capturing the nuanced patterns that may indicate anomalies. For each trafic image, we implement a low-pass filtering process to mitigate noise. This step is necessitated by the unique characteristics of trafic images, which, in contrast to natural images, exhibit a chaotic and texture less state [29, 54]. This phenomenon arises from the abundance of high-frequency components inherent in network trafic data. However, these high-frequency components often manifest as detrimental noise, impeding the model’s ability to generalize efectively due to the excessive complexity of the information.

## 3.3 Proposed UnDif

As shown in Figure 2(a), our UnDif contains two main components: an evidence extractor to extract evidence and a novel uncertainty learning module to construct an uncertainty space for subsequent anomaly quantification and detection.

3.3.1 Evidence Extractor. The autoencoder is designed to process original input trafic x, encoding it into a latent evidence represen tation z, and subsequently decoding it to produce a reconstruction of the input xˆ. Given that the input is a multi-channel image, we employ Convolutional Neural Networks (CNNs) as the encoder, following established practices in the literature [34, 54]. It is imperative to note that network trafic inherently comprises a series of packet sequences with distinct spatiotemporal characteristics [29, 52]. However, previous autoencoder-based reconstruction methods have primarily focused on enhancing reconstruction quality, often neglecting the crucial spatiotemporal relationships inherent in the network packets. To address this limitation, we introduce a spatiotemporal aware channel-spatial based attention mechanism, specifically the Convolutional Block Attention Module (CBAM) [43], into our autoencoder architecture. This approach enables us to assign higher importance to significant channel images (temporal features) and spatially relevant regions (spatial features), thereby facilitating the extraction of evidence for critical patterns in multi-channel images.

3.3.2 UncertaintyLearning Module. The predominant zero-positive learning paradigm for anomaly network trafic typically frames this task as a reconstruction problem, optimizing the similarity loss of the original input x and the reconstructed output xˆ. The intra-sample diferences between pre- and post-reconstruction from an egocentric perspective are utilized to quantify the anomaly degrees. However, this paradigm exhibits suboptimal performance due to two primary limitations. Firstly, comparing the diferences between samples before and after reconstruction does not directly address the fundamental nature of the problem: anomalous trafic is inherently defined relative to normal trafic patterns. Secondly, the classical “identical shortcut” problem inherent in autoencoder architectures significantly impacts the intra-sample diferences of anomalous samples, particularly leading to performance degradation in scenarios involving anomaly drift.

To address these issues concurrently, we propose a novel uncertainty learning module designed to construct an uncertainty space, facilitating direct inter-sample comparisons to detect anomalous network trafic. This module is based on estimating the detection uncertainty, explicitly focusing on model uncertainty, also known as epistemic uncertainty. Model uncertainty quantifies the uncertainty in estimating model parameters given the training data, effectively measuring the degree of congruity between the model and the data [1]. We posit that this model uncertainty score is intrinsically linked to anomalous patterns and can be leveraged to identify anomalies efectively. The fundamental intuition underpinning our methodology is rooted in the diferential uncertainty characteristics exhibited by normal and anomalous trafic patterns [21]. Normal samples, well-represented in the training data, typically manifest low model uncertainty. Conversely, anomalous trafic, particularly in the context of drifted anomalies, induces higher uncertainty due to its deviation from the learned normal patterns.

The uncertainty learning module comprises an encoder and a group of uncertainty parameter heads. The encoder, which shares its architectural design with the preceding encoder of the evidence extractor, is based on the reconstruction output xˆ. It processes the reconstruction xˆ as input and generates an uncertainty representation �, quantifying the model’s detection uncertainty. The uncertainty parameter heads, implemented as linear layers, translate the uncertainty representation � into their corresponding uncertainty parameters. This transformation facilitates efective uncertainty modeling. Through this mechanism, we explicitly incorporate evidential learning to quantify evidence distribution of normal network trafic. In contrast to Bayesian Neural Networks (BNNs) [26], which place pri ors on network weights, our evidential-based approach sets priors directly over the likelihood function. This methodology achieves a more computationally eficient uncertainty quantification.

Network trafic data frequently follows Gaussian distributions during standard analysis scenarios [16]. Thus, we consider the uncertainty representations z extracted from the preceding autoencoder, which encapsulates the evidential information about normal network trafic, to conform to independent homogeneous distributions from a Gaussian distribution. These distributions are characterized by their mean and variance $( \mu , \sigma ^ { 2 } )$ . These parameters to be quantified, $\mu$ and $\sigma ^ { 2 } { } _ { ; }$ , are intrinsically linked to the model un certainty that is the focus of our investigation [1]. To estimate these parameters, we employ a hierarchical Bayesian approach. Specifi cally, we utilize a Gaussian prior to estimate the mean value and place an Inverse-Gamma prior on the variance. This choice of priors is motivated by their conjugate relationship with the Gaussian like lihood, facilitating closed-form posterior updates. The hierarchical model can be expressed as follows:

$$
\mathbf {z} \sim \mathcal {N} (\mu , \sigma^ {2}) \qquad \mu \sim \mathcal {N} (\gamma , \sigma^ {2} v ^ {- 1}) \qquad \sigma^ {2} \sim \Gamma^ {- 1} (\alpha , \beta),\tag{1}
$$

where Γ(·) denotes the Gamma function, $\gamma$ represents the uncertainty space to be estimated, $v > 0 , \alpha > 1$ and $\beta > 0$ . We aim to estimate a posterior distribution $q ( { \boldsymbol { \mu } } , \sigma ^ { 2 } | \mathbf { z } )$ . Following the approach described in work [6], we employ a factorization of the estimated distribution such that $q ( \mu , \sigma ^ { 2 } ) = q ( \mu ) q ( \sigma ^ { 2 } )$ . This factorization al lows for a tractable approximation of the posterior distribution. Our approximation takes the form of the Gaussian conjugate prior, specifically the Normal Inverse-Gamma (NIG) distribution:

$$
p (\{\mu , \sigma^ {2} \} \mid \Omega) = \frac {\beta^ {\alpha} \sqrt {v}}{\Gamma (\alpha) \sqrt {2 \pi \sigma^ {2}}} \left(\frac {1}{\sigma^ {2}}\right) ^ {\alpha + 1} \exp \left\{- \frac {2 \beta + v (\gamma - \mu) ^ {2}}{2 \sigma^ {2}} \right\},\tag{2}
$$

where $\Omega = \{ \gamma , v , \alpha , \beta \}$ denotes the set of uncertainty parameters we aim to estimate. Given a NIG distribution parameterized by $\Omega _ { : }$ we can compute the uncertainty space and model uncertainty:

$$
\underbrace {\mathbb {E} [ \mu ] = \gamma} _ {\text { uncertainty   space }} \quad \underbrace {\operatorname{Var} [ \mu ] = \frac {\beta}{v (\alpha - 1)}} _ {\text { model   uncertainty }}.\tag{3}
$$

This mathematical formulation delineates the theoretical framework underpinning our approach to uncertainty quantification. The evidential learning paradigm we have introduced essentially con stitutes an uncertainty estimation methodology based on the likeli hood function. This approach involves training a neural network to output the hyperparameters for fitting an evidential distribution.

Next, we outline our method for obtaining evidential parameters. Our training process is designed to optimize a dual-objective function that simultaneously addresses two critical aspects: (i) in creasing model evidence to support the training samples, which in this context represent normal network trafic patterns, and (ii) reducing evidence when uncertainty space exhibits inconsistencies or inaccuracies. Objective (i) can be conceptualized as a mechanism for adapting our data to the evidential model, while objective (ii) serves to enforce a prior that mitigates inaccurate evidence and amplifies uncertainty where appropriate.

Objective (i): Maximizing the Normal Evidence. In accordance with Bayesian probability theory, the “model evidence” is defined as the likelihood of an observation, given the evidential distribution parameters Ω. This is computed by marginalizing over the likelihood parameters $( \mu , \sigma ^ { 2 } )$ :

$$
p \left(\mathbf {z} \mid \Omega\right) = \int_ {\sigma^ {2} = 0} ^ {\infty} \int_ {\mu = - \infty} ^ {\infty} p \left(\mathbf {z} \mid \mu , \sigma^ {2}\right) p \left(\mu , \sigma^ {2} \mid \Omega\right) \mathrm{d} \mu \mathrm{d} \sigma^ {2}.\tag{4}
$$

The direct fitting of the evidential model parameters Ω to this likelihood distribution presents significant computational challenges. However, by applying a Normal Inverse-Gamma (NIG) evidential prior to the Gaussian likelihood function, we can derive an analytical solution, as demonstrated in work [6]:

$$
p \left(\mathbf {z} \mid \Omega\right) = \mathrm{St} \left(\mathbf {z}; \gamma , \frac {\beta (1 + v)}{v \alpha}, 2 \alpha\right),\tag{5}
$$

where $\mathrm { S t } ( \cdot ; \mu _ { \mathrm { S t } } , \sigma _ { \mathrm { S t } } ^ { 2 } , v _ { \mathrm { S t } } )$ denotes the Student’s t-distribution evaluated at location parameter $\mu _ { \mathrm { S t } }$ , scale parameter $\sigma _ { \mathrm { S t } } ^ { 2 } ,$ , and degrees of freedom $v _ { S \mathrm { t } }$ . To optimize the model’s representation of normal network trafic, we maximize the logarithm of the model evidence, which is equivalent to minimizing its negative. This objective guides the uncertainty parameter heads to output the parameters of a NIG distribution that best fits the distribution of normal network trafic. Formally, we define the training objective $\mathcal { L } ^ { \mathrm { N L L } }$ for maximizing the normal evidence as:

$$
\begin{array}{l} \mathcal {L} ^ {\mathrm{NLL}} = \frac {1}{2} \log \left(\frac {\pi}{v}\right) - \alpha \log (\omega) + \log \left(\frac {\Gamma (\alpha)}{\Gamma \left(\alpha + \frac {1}{2}\right)}\right) \\ \qquad + \left(\alpha + \frac {1}{2}\right) \log \left((\mathbf {z} - \gamma) ^ {2} v + \omega\right), \end{array}\tag{6}
$$

where $\omega = 2 \beta ( 1 + v )$

Objective (ii): Minimizing Evidence on Errors. In addition to maximizing the evidence for normal patterns, we incorporate a regularization term that imposes a high uncertainty prior to penalize incorrect evidence in the uncertainty space. The fundamental principle underlying this regularization is that it should attenuate the weight of evidence where the uncertainty space deviates significantly from the true evidence while having minimal impact on evidence predictions that closely align with the instructive evidence $\mathbf { z } .$ To achieve this, we formulate an evidence regularizer [6] $\mathcal { L } ^ { \mathrm { R } }$ as:

$$
\mathcal {L} ^ {\mathrm{R}} = | \mathbf {z} - \gamma | \cdot (2 v + \alpha).\tag{7}
$$

3.3.3 Training. Our training loss function comprises three principal components: $\mathcal { L } ^ { \mathrm { N L L } } , \mathcal { L } ^ { \mathrm { R } }$ , and $\mathcal { L } ^ { \mathrm { R e c } }$ :

$$
\mathcal {L} = \mathcal {L} ^ {\mathrm{Rec}} \cdot \lambda_ {\mathrm{Rec}} + \mathcal {L} ^ {\mathrm{NLL}} \cdot \lambda_ {\mathrm{NLL}} + \mathcal {L} ^ {\mathrm{R}} \cdot \lambda_ {\mathrm{R}},\tag{8}
$$

where $\lambda .$ is the hyperparameter to control the contribution of each component. $\mathcal { L } ^ { \mathrm { R e c } }$ is the reconstruction loss for the autoencoder:.

$$
\mathcal {L} ^ {\mathrm{Rec}} = | | \mathbf {x} - \hat {\mathbf {x}} | | _ {1},\tag{9}
$$

where $| | \cdot | | _ { 1 }$ denotes the L1 norm. The inclusion of this term ensures the preservation of the autoencoder’s fundamental reconstruction capability, enabling the generation of meaningful latent representations. These representations serve as efective evidence instructors for the subsequent uncertainty quantification.

Table 1: Performance comparisons (%) for undrifted anomaly detection on the DataCon2020, CIC-IDS2017, and USTC-TFC2016 datasets. The best results are in bold, and the runner-up results are underlined.

<table><tr><td rowspan="2">Model</td><td colspan="3">DataCon2020</td><td colspan="3">CIC-IDS2017</td><td colspan="3">USTC-TFC2016</td></tr><tr><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td></tr><tr><td>PaDim</td><td> $61.01 \pm 0.5$ </td><td> $55.07 \pm 0.2$ </td><td> $67.23 \pm 0.2$ </td><td> $57.74 \pm 0.4$ </td><td> $55.06 \pm 0.1$ </td><td> $68.16 \pm 0.1$ </td><td> $98.79 \pm 0.0$ </td><td> $96.93 \pm 0.1$ </td><td> $96.85 \pm 0.1$ </td></tr><tr><td>DFM</td><td> $83.03 \pm 0.3$ </td><td> $78.67 \pm 0.3$ </td><td> $78.85 \pm 0.3$ </td><td> $69.91 \pm 0.2$ </td><td> $63.89 \pm 0.3$ </td><td> $66.87 \pm 0.1$ </td><td> $94.94 \pm 0.3$ </td><td> $93.03 \pm 0.3$ </td><td> $92.63 \pm 0.3$ </td></tr><tr><td>DFKDE</td><td> $72.85 \pm 0.5$ </td><td> $64.37 \pm 0.3$ </td><td> $71.86 \pm 0.2$ </td><td> $67.67 \pm 0.6$ </td><td> $63.62 \pm 0.3$ </td><td> $68.61 \pm 0.2$ </td><td> $91.63 \pm 2.4$ </td><td> $93.38 \pm 0.2$ </td><td> $93.79 \pm 0.2$ </td></tr><tr><td>Fastflow</td><td> $69.98 \pm 0.5$ </td><td> $63.93 \pm 0.3$ </td><td> $71.65 \pm 0.3$ </td><td> $78.25 \pm 0.3$ </td><td> $74.82 \pm 0.4$ </td><td> $76.39 \pm 0.4$ </td><td> $99.14 \pm 0.0$ </td><td> $95.60 \pm 0.2$ </td><td> $95.42 \pm 0.2$ </td></tr><tr><td>Cflow</td><td> $68.69 \pm 1.6$ </td><td> $64.14 \pm 1.0$ </td><td> $72.40 \pm 0.8$ </td><td> $66.42 \pm 0.9$ </td><td> $69.46 \pm 0.6$ </td><td> $69.41 \pm 0.5$ </td><td> $97.22 \pm 0.2$ </td><td> $96.76 \pm 0.2$ </td><td> $96.68 \pm 0.2$ </td></tr><tr><td>STFPM</td><td> $82.37 \pm 0.6$ </td><td> $80.44 \pm 2.1$ </td><td> $\underline{80.93 \pm 1.7}$ </td><td> $85.89 \pm 1.7$ </td><td> $80.00 \pm 2.1$ </td><td> $81.50 \pm 1.1$ </td><td> $91.63 \pm 2.4$ </td><td> $89.02 \pm 1.3$ </td><td> $89.71 \pm 1.3$ </td></tr><tr><td>ReverDis</td><td> $74.53 \pm 2.4$ </td><td> $68.80 \pm 3.1$ </td><td> $75.30 \pm 1.1$ </td><td> $82.22 \pm 0.3$ </td><td> $77.87 \pm 0.4$ </td><td> $76.62 \pm 0.4$ </td><td> $98.05 \pm 0.5$ </td><td> $95.21 \pm 0.9$ </td><td> $95.07 \pm 0.9$ </td></tr><tr><td>MMR</td><td> $80.60 \pm 2.1$ </td><td> $78.85 \pm 2.1$ </td><td> $79.64 \pm 1.3$ </td><td> $85.87 \pm 1.2$ </td><td> $74.36 \pm 1.1$ </td><td> $74.40 \pm 1.0$ </td><td> $99.44 \pm 0.0$ </td><td> $96.15 \pm 0.2$ </td><td> $96.04 \pm 0.2$ </td></tr><tr><td>GANomaly</td><td> $81.50 \pm 1.0$ </td><td> $79.40 \pm 2.1$ </td><td> $79.95 \pm 1.6$ </td><td> $82.75 \pm 4.7$ </td><td> $80.85 \pm 1.7$ </td><td> $81.21 \pm 0.9$ </td><td> $95.36 \pm 1.0$ </td><td> $91.27 \pm 2.9$ </td><td> $91.07 \pm 3.2$ </td></tr><tr><td>ARCADE</td><td> $81.98 \pm 4.1$ </td><td> $\underline{81.48 \pm 2.0}$ </td><td> $80.31 \pm 3.4$ </td><td> $84.85 \pm 2.6$ </td><td> $80.15 \pm 1.6$ </td><td> $82.78 \pm 1.0$ </td><td> $88.62 \pm 2.2$ </td><td> $93.13 \pm 0.1$ </td><td> $93.57 \pm 0.1$ </td></tr><tr><td>MFAD</td><td> $\underline{83.16 \pm 1.9}$ </td><td> $76.28 \pm 2.4$ </td><td> $78.59 \pm 1.1$ </td><td> $\underline{86.02 \pm 0.8}$ </td><td> $\underline{81.66 \pm 1.9}$ </td><td> $\underline{83.67 \pm 1.7}$ </td><td> $\underline{99.73 \pm 0.0}$ </td><td> $\underline{97.45 \pm 0.4}$ </td><td> $\underline{97.43 \pm 0.4}$ </td></tr><tr><td>Trident</td><td> $63.89 \pm 0.5$ </td><td> $73.67 \pm 0.3$ </td><td> $78.37 \pm 0.3$ </td><td> $82.99 \pm 0.1$ </td><td> $77.42 \pm 0.2$ </td><td> $75.17 \pm 0.2$ </td><td> $96.19 \pm 0.2$ </td><td> $89.86 \pm 0.3$ </td><td> $89.47 \pm 0.3$ </td></tr><tr><td>UnDiff</td><td> $86.93 \pm 0.3$ </td><td> $83.16 \pm 0.2$ </td><td> $82.78 \pm 0.2$ </td><td> $88.88 \pm 0.4$ </td><td> $83.31 \pm 0.4$ </td><td> $83.72 \pm 0.4$ </td><td> $99.90 \pm 0.0$ </td><td> $99.47 \pm 0.2$ </td><td> $99.47 \pm 0.2$ </td></tr></table>

3.3.4 Inference. The anomaly detection process fundamentally re lies on an anomaly score to quantify the degree of deviation from normality. Given that our model is trained exclusively on normal network trafic, the proposed UnDif naturally assigns low uncertainty to patterns consistent with normal network behavior. Our approach is motivated by the well-established principle that there exists a distributional divergence between normal and anomalous network trafic, encompassing both undrifted and drifted anomalies [8, 21, 54]. Leveraging this insight, we adopt an inter-sample diferences method, utilizing model uncertainty as a direct proxy for anomaly scoring. This approach is underpinned by the widely accepted notion in uncertainty learning that deviant samples inherently induce higher model uncertainty [22]. As depicted in Figure 2(b), our method yields an efective and computationally efi cient uncertainty-inspired anomaly score. This score is character ized by its ability to generate high uncertainty values for anomalous samples (i.e., out-of-distribution instances relative to the training set) while maintaining low uncertainty for normal samples (i.e., in-distribution instances relative to the training set). In contrast to traditional reconstruction-based anomaly quantification methods, which we categorize as intra-sample diference approaches, Un Dif capitalizes on the intrinsic distributional divergence between normal and anomalous network trafic. Formally, we define our anomaly score as follows:

$$
\text { Anomaly   Score } = \operatorname{Var} [ \mu ] = \frac {\beta}{v (\alpha - 1)}.\tag{10}
$$

## 4 Experiments

## 4.1 Experimental Setting

Dataset. We use three publicly available network trafic anomaly detection datasets for evaluation: (i) DataCon2020 [10] is an en crypted network trafic dataset comprising normal and malicious trafic, with the latter consisting of encrypted malware communications; (ii) CIC-IDS2017 [38] is a network intrusion detection dataset that includes seven common attacks; (iii) USTC-TFC2016 [42] is malware trafic detection dataset with malicious trafic from public sources and normal trafic from eight application types. For consistent evaluation, we randomly sample 10,000 normal network flows for training and 5,000 normal plus 5,000 anomalous flows for testing across all datasets.

Baselines. We evaluate UnDif with 12 state-of-the-art baselines, categorized into two groups as follows: (i) Network Trafic Anomaly Detection: GANomaly [3], ARCADE [34], MFAD [54], and Trident [53]; (ii) Other Advanced Anomaly Detection: PaDim [11], DFM [2], DFKDE [4], FastFlow [47], CFlow [19], STFPM [40], ReverDis [12], and MMR [51].

Evaluation Metrics. In alignment with recent models in network trafic anomaly detection [34, 54], we employ three commonly used metrics: AUC, Accuracy (ACC), and F1-Score (F1). Practical detection accuracy is defined as the performance achieved under the optimal F1-Score value.

Drifted Anomaly. We assess model’s robustness to anomaly drift by conducting cross-dataset evaluations. Specifically, we train one model on one dataset and evaluate this model’s performance on anomalous samples from other datasets. This approach allows us to investigate model’s generalization capability and resilience to potential concept shifts in network trafic, thereby assessing model’s eficacy in detecting drifted anomalies in real-world environments. Implementation Details. All experiments are conducted on an NVIDIA GeForce RTX 3090 GPU. We use the Adam optimizer with learning rates of $1 e ^ { - 4 } , 1 e ^ { - 3 } , 1 e ^ { - 6 }$ for DataCon2020, CIC-IDS2017, and USTC-TFC2016, respectively. Loss coeficient (�<sub>Rec</sub>, �<sub>NLL</sub>, �<sub>R</sub>) are set as $( 1 , 1 e ^ { - 2 } , 1 e ^ { - 4 } ) , ( 1 , 5 e ^ { - 2 } , 5 e ^ { - 5 } )$ and $( 1 , 1 , 1 e ^ { - 2 } )$ , while the low-pass filter uses a cutof radius of 5. Training proceeds with a batch size of 128 for a maximum of 50 epochs, with early stopping implemented to mitigate overfitting. To ensure statistical robustness, we perform five independent runs with diferent random seeds, reporting mean results with standard deviations. To facilitate reproducibility, the model code for our UnDif is available at https://github.com/ikun0124/UnDif and will be made public.

## 4.2 Anomaly Detection on Benchmark

To assess UnDif’s eficacy in typical anomaly trafic detection scenarios (i.e., undrifted anomalies), we conducted a comprehensive comparison of our model against 12 competitive baselines on three datasets. The results, as presented in Table 1, demonstrate that our model consistently outperforms baselines across all three datasets. Notably, on the DataCon2020 and CIC-IDS2017 datasets, UnDif exhibits significant performance improvements over the best-performing baseline MFAD, with enhancements of 3.7% and 2.8% in AUC, respectively. The underlying strength of our method <sup>lies</sup> <sup>in</sup> <sup>its</sup> <sup>innovative</sup> <sup>utilization</sup> <sup>of</sup> <sup>uncertainty</sup> <sup>measures</sup> <sup>to</sup> <sup>directly</sup>UID quantify inter-sample diferences, thereby facilitating more accu rate discrimination of anomalous network trafic patterns.

Table 2: Performance comparisons (%) for drifted anomaly detection on the DataCon2020, CIC-IDS2017, and USTC-TFC2016ARCADE n<sup>s</sup> datasets. The abbreviations are explained as follows: D: DataCon2020, I: CIC-IDS2017, and U: USTC-TFC2016.<sup>D</sup>

<table><tr><td rowspan="2">Model</td><td colspan="3">D-&gt;I</td><td colspan="3">D-&gt;U</td><td colspan="3">I-&gt;D</td><td colspan="3">I-&gt;U</td><td colspan="3">U-&gt;D</td><td colspan="3">U-&gt;I</td></tr><tr><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td><td>AUC</td><td>ACC</td><td>F1</td></tr><tr><td>GANomaly</td><td>50.73</td><td>50.99</td><td>66.86</td><td>60.96</td><td>75.82</td><td>79.68</td><td>56.58</td><td>72.35</td><td>75.76</td><td>74.92</td><td>72.32</td><td>77.49</td><td>90.30</td><td>90.70</td><td>91.25</td><td>96.01</td><td>88.67</td><td>87.95</td></tr><tr><td>ARCADE</td><td>49.99</td><td>49.99</td><td>66.66</td><td>57.87</td><td>74.83</td><td>78.74</td><td>67.47</td><td>79.24</td><td>80.94</td><td>49.60</td><td>59.74</td><td>69.60</td><td>97.87</td><td>93.44</td><td>93.84</td><td>88.61</td><td>90.67</td><td>91.44</td></tr><tr><td>MFAD</td><td>62.28</td><td>51.09</td><td>67.01</td><td>79.50</td><td>72.76</td><td>77.90</td><td>77.90</td><td>70.56</td><td>74.60</td><td>82.18</td><td>75.84</td><td>78.02</td><td>98.20</td><td>95.27</td><td>95.43</td><td>98.62</td><td>93.92</td><td>94.19</td></tr><tr><td>Trident</td><td>55.11</td><td>49.90</td><td>66.66</td><td>66.08</td><td>78.99</td><td>81.77</td><td>51.20</td><td>57.90</td><td>70.07</td><td>67.47</td><td>66.24</td><td>72.57</td><td>97.47</td><td>98.28</td><td>98.31</td><td>98.83</td><td>97.57</td><td>97.62</td></tr><tr><td>UnDiff-AE</td><td>64.48</td><td>70.57</td><td>77.10</td><td>71.08</td><td>76.97</td><td>80.73</td><td>81.48</td><td>79.21</td><td>80.47</td><td>61.88</td><td>62.27</td><td>71.91</td><td>99.57</td><td>98.92</td><td>98.92</td><td>98.75</td><td>92.80</td><td>93.27</td></tr><tr><td>UnDiff</td><td>84.10</td><td>76.14</td><td>80.46</td><td>96.08</td><td>87.95</td><td>88.66</td><td>93.70</td><td>88.65</td><td>88.57</td><td>91.18</td><td>86.43</td><td>86.69</td><td>99.83</td><td>99.59</td><td>99.59</td><td>99.76</td><td>98.07</td><td>98.07</td></tr></table>

![](images/0074e0f79f4c1dc1690c5e9ddf568887e42cf657c8974b6ee6d97a861a0dd27f.jpg)  
Figure 3: Statistics of the uncertainty-based anomaly scores for UnDif under the undrifted anomaly scenario.UID-AE

While statistics-based methods such as PaDim, DFM, and DFKDE, as well as normalizing flow-based approaches like FastFlow and CFlow, attempt to compute distribution deviations by exploiting inter-sample diferences, their comparative spaces lack the discriminative power of our uncertainty space. Our approach, built upon the informative reconstruction of latent variables and guided by evidential learning, constructs a more robust and discerning comparative framework. Moreover, distillation-based methods in anomaly detection, including STFPM, ReverDis, and MMR, are con strained by the limitation in efective feature extraction. In contrast, approaches specific to anomaly network trafic detection, while not requiring additional feature extractors, quantify anomalies through intra-sample reconstruction diferences. However, these methods, including GANomaly, ARCADE, MFAD, and Trident, sufer from the “identical shortcut” issue, which may significantly compromise the intra-sample diferences of anomalies, leading to suboptimal performance. Our uncertainty-inspired framework addresses these limitations by efectively leveraging distributional diferences between normal and anomalous samples. By quantifying anomalies from an inter-sample diferences perspective, UnDif provides a more nuanced and robust approach to anomaly detection.

To further corroborate the feasibility of our UnDif framework, we present a detailed analysis of the anomaly score distributions in Figure 3. The graphical representation reveals a marked bimodal distribution, with a clear separation between the scores associated with normal and anomalous samples. This pronounced divergence in score distributions provides compelling evidence for the discrim inative power of our uncertainty-inspired anomaly metric. The clear detachment between normal and anomalous samples also underscores the method’s ability to generate highly informative indicators, facilitating more accurate and reliable anomaly detection.

![](images/54ba8d2e73fcef97336ab4402fe526535894d3e88988c2b4df825a6c15d325bf.jpg)  
UnDiff nFigure 4: Anomaly score distribution for Trident, UnDif-AE, <sup>D</sup>and UnDif under the anomaly drift scenario.

## 4.3 Drifted Anomaly Detection

To assess the eficacy in addressing drifted anomalies, we compare our UnDif with state-of-the-art network trafic anomaly detection baselines and a variant of our method – UnDif-AE, which employs a pure auto-encoder architecture without uncertainty learning. As evidenced in Table 2, these approaches have suboptimal performance, particularly in the drifted experiments from DataCon2020 (D) to CIC-IDS2017 (I), D to USTC-TFC2016 (U), I to D, and I to U. These empirical observations highlight the critical necessity for robust drifted anomaly detection methodologies. The primary limitation of these baselines stems from their reliance on an intrasample diference paradigm, which is inherently susceptible to the “identical shortcut” issue prevalent in reconstruction-based models. Therefore, the divergence in anomaly scores between normal and anomalous samples is suppressed and obfuscated. We visualize the detailed anomaly scores for Trident and UnDif-AE in Figure 4 to elucidate this phenomenon. The anomaly score distribution for Trident exhibits significant overlap between normal and anomalous samples, with anomalous samples occasionally scoring lower than normal samples. This observation indicates that the “identical shortcut” issue profoundly compromises the eficacy of intra-sample diferences in detecting drifted anomalies. In contrast,

![](images/5e0dce4c91ea05603bcb8810b5550f799bdef33768c8669cebb3afa6c6c359f7.jpg)  
Trident: Intra-Sample Differences UnDiff: Inter-Sample Differences  
Figure 5: The t-SNE visualization comparison between intra sample and inter-sample diferences.

UnDif achieves apparent distinction in the distribution between normal and drifted anomaly samples, thereby validating the effectiveness of our inter-sample diferences approach. Notably, the comparative analysis with UnDif-AE shows that the substantial improvement in UnDif’s performance is predominantly attributable to the uncertainty-inspired inter-sample diferences rather than the fundamental auto-encoder architecture.

## 4.4 Qualitative Study

We now elucidate the underlying mechanisms contributing to Un Dif’s enhanced performance by two �-SNE visualizations. As il lustrated in Figure 5, we observe a degree of confusion between the pre- and post-reconstruction embeddings of anomalous samples on Trident, manifested as certain overlaps and approximate profiles with minimal distance. We posit that this phenomenon arises from the “identical shortcut” issue, an inherent limitation in reconstruction-based approaches. This limitation leads to well reconstructed representations even for anomalous samples, a phenomenon that contradicts the fundamental detection motivation of reconstruction methods. Consequently, this results in indistinguish able intra-sample diferences between normal and anomalous traf fic patterns, compromising the eficacy of traditional approaches. In contrast, UnDif is based on a novel inter-sample diferences perspective, efectively leveraging the axiom that anomalous sam ples inherently deviate from normal samples in the feature space. The representation within our uncertainty space demonstrates the feasibility and efectiveness of uncertainty-inspired modeling and detection. This approach makes the discrimination by exploiting inter-sample diferences, thereby overcoming the limitations inher ent in intra-sample comparison methods.

## 4.5 Ablation Study

To evaluate the contributions of each component in our UnDif, we conduct an ablation study comprising four variants. These variants are constructed by removing one of the key components in UnDif: the reconstruction loss $\mathcal { L } ^ { \mathrm { R e c } } \left( \mathrm { w } / \mathrm { o } \mathcal { L } ^ { \mathrm { R e c } } \right)$ , the regularization loss $\mathcal { L } ^ { \mathrm { R } }$ (w/o $\mathcal { L } ^ { \mathrm { R } } ) _ { : }$ the uncertainty-based anomaly score (w/o AS), and both the uncertainty-based modeling and anomaly score (w/o T&AS). As illustrated in Table 3, the removal of $\mathcal { L } ^ { \mathrm { R e c } }$ results in substantial per formance degradation, underscoring the critical role of reconstruction loss in ensuring a refined representation of normal network trafic. Furthermore, we observe a notable decline in performance upon removal of $\mathcal { L } ^ { \mathrm { R } }$ , indicating its eficacy as a regularization con straint in preventing the formation of erroneous evidence spaces during the uncertainty quantification process. While removing the uncertainty-based anomaly score (w/o AS) and both uncertaintybased modeling and anomaly score (w/o T&AS) resulted in performance degradation, our complete UnDif model demonstrates optimal performance in drifted anomaly detection. This suggests that the uncertainty-based modeling and inter-sample diference de tection components efectively leverage prior diferences between normal and anomalous samples, mitigating the inherent limitations of purely reconstruction-based methods.

Anom<sub>Table 3: Ablation studies for drifted and undrifted anomaly</sub> Anomaly embedding <sub>detection (AUC). The gray color denotes undrifted detection.</sub>

<table><tr><td rowspan="2">Variant</td><td colspan="3">DataCon2020</td><td colspan="3">CIC-IDS2017</td><td colspan="3">USTC-TFC2016</td></tr><tr><td>D</td><td>I</td><td>U</td><td>D</td><td>I</td><td>U</td><td>D</td><td>I</td><td>U</td></tr><tr><td>w/o  $\mathcal{L}^{\text{Rec}}$ </td><td>83.44</td><td>61.79</td><td>80.26</td><td>78.46</td><td>76.22</td><td>59.41</td><td>98.95</td><td>80.97</td><td>98.25</td></tr><tr><td>w/o  $\mathcal{L}^{\text{R}}$ </td><td>84.80</td><td>71.48</td><td>72.50</td><td>85.31</td><td>86.80</td><td>81.12</td><td>99.55</td><td>99.39</td><td>99.78</td></tr><tr><td>w/o AS</td><td>85.66</td><td>82.52</td><td>83.25</td><td>83.28</td><td>87.67</td><td>86.15</td><td>99.74</td><td>98.81</td><td>99.84</td></tr><tr><td>w/o T&amp;AS</td><td>85.55</td><td>64.48</td><td>71.08</td><td>81.48</td><td>86.02</td><td>61.88</td><td>99.51</td><td>98.75</td><td>99.71</td></tr><tr><td>UnDiff</td><td>86.93</td><td>84.10</td><td>96.08</td><td>93.70</td><td>88.88</td><td>91.18</td><td>99.83</td><td>99.76</td><td>99.90</td></tr></table>

Table 4: Overhead comparison for inference.

<table><tr><td></td><td>GANomaly</td><td>ARCADE</td><td>MFAD</td><td>Trident</td><td>UnDiff</td></tr><tr><td>MACs (G)</td><td>0.98</td><td>0.82</td><td>0.99</td><td>0.03</td><td>0.25</td></tr><tr><td>#Paras (M)</td><td>9.66</td><td>6.7</td><td>10.07</td><td>27.61</td><td>2.55</td></tr></table>

## 4.6 Overhead Evaluation

We conduct an analysis of model eficiency, focusing on multiplyaccumulate operations per second (MACs) and the number of model parameters (#Paras) during inference. The results of this analysis are summarized in Table 4. Our UnDif demonstrates excellent performance with favorable computational overhead compared to alternative baselines. This eficiency can be attributed to strategic design choices, such as the multi-channel image representation, a low-parameter evidence extractor, and a set of concise uncertainty parameter heads. Notably, UnDif balances performance and computational requirements, rendering it particularly suitable for practical deployment in network trafic anomaly detection scenarios.

## 5 Conclusion

This study presents a pioneering approach to network trafic anomaly detection by developing an inter-sample diferences method based on uncertainty. This novel methodology directly addresses the challenges of anomaly detection while circumventing the “identical shortcut” issue inherent in existing methods that rely on intrasample diferences between pre- and post-reconstruction representations. Our proposed UnDif efectively leverages the prior knowledge that anomalous samples inherently deviate from normal samples. This enables learning a more discriminative uncertainty space, facilitating optimal detection performance. Comprehensive empirical evaluations across three benchmark datasets demonstrate UnDif’s superior performance in detecting undrifted and drifted anomalies with minimal additional computational overhead.

## Acknowledgments

This work was supported by National Natural Science Foundation of China (Grant No.62176043, No.62072077 and No.U22A2097).

## References

[1] Moloud Abdar, Farhad Pourpanah, Sadiq Hussain, Dana Rezazadegan, Li Liu, Mohammad Ghavamzadeh, Paul W. Fieguth, Xiaochun Cao, Abbas Khosravi, U. Rajendra Acharya, Vladimir Makarenkov, and Saeid Nahavandi. 2021. A review of uncertainty quantification in deep learning: Techniques, applications and challenges. Information Fusion 76 (2021), 243–297.

[2] Nilesh A. Ahuja, IbrahimaJ. Ndiour, Trushant Kalyanpur, and Omesh Tickoo. 2019. Probabilistic Modeling of Deep Features for Out-of-Distribution and Adversarial Detection. arXiv:1909.11786 (2019).

[3] Samet Akcay, Amir Atapour Abarghouei, and Toby P. Breckon. 2018. GANomaly: Semi-supervised Anomaly Detection via Adversarial Training. In Asian Conference on Computer Vision (ACCV). 622–637.

[4] Samet Akcay, Dick Ameln, Ashwin Vaidya, Barath Lakshmanan, Nilesh A. Ahuja, and Ergin Utku Genc. 2022. Anomalib: A Deep Learning Library for Anomaly Detection. In IEEE International Conference on Image Processing (ICIP). 1706–1710

[5] Mejbah Alam, Justin Gottschlich, Nesime Tatbul, Javier S Turek, Tim Mattson, and Abdullah Muzahid. 2019. A Zero-Positive Learning Approach for Diagnosing Software Performance Regressions. In Annual Conference on Neural Information Processing Systems (NeurIPS).

[6] Alexander Amini, Wilko Schwarting, Ava Soleimany, and Daniela Rus. 2020. Deep Evidential Regression. In Annual Conference on Neural Information Processing Systems (NeurIPS). 14927–14937.

[7] Federico Barbero, Feargus Pendlebury, Fabio Pierazzi, and Lorenzo Cavallaro. 2022. Transcending TRANSCEND: Revisiting Malware Classification in the Presence of Concept Drift. In Symposium on Security and Privacy (S&P). IEEE, 805–823.

[8] Saihua Cai, Han Tang, Jinfu Chen, Yikai Hu, and Wuhao Guo. 2025. CDDA-MD: An eficient malicious trafic detection method based on concept drift detection and adaptation technique. Computers & Security 148 (2025), 104121.

[9] Chengtai Cao, Xinhong Chen, Jianping Wang, Qun Song, Rui Tan, and Yung-Hui Li. 2024. CCTR: Calibrating Trajectory Prediction for Uncertainty-Aware Motion Planning in Autonomous Driving. In AAAI Conference on Artificial Intelligence (AAAI). 20949–20957.

[10] Community DataCon. 2020. DataCon: open dataset DataCon2020- encrypted malicious trafic dataset direction open dataset. https://datacon.qianxin.com/opendata.

[11] Thomas Defard, Aleksandr Setkov, Angelique Loesch, and Romaric Audigier. 2020. PaDiM: A Patch Distribution Modeling Framework for Anomaly Detection and Localization. In International Conference on Pattern Recognition (ICPR). 475–489.

[12] Hanqiu Deng and Xingyu Li. 2022. Anomaly Detection via Reverse Distillation from One-Class Embedding. In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 9727–9736.

[13] Xianwen Deng, Yijun Wang, and Zhi Xue. 2024. AN-Net: an Anti-Noise Network for Anonymous Trafic Classification. In The ACM Web Conference (WWW). 4417–4428.

[14] Yasir Ali Farrukh, Syed Wali, Irfan Khan, and Nathaniel D. Bastian. 2023. SeNet-I: An approach for detecting network intrusions through serialized network trafic images. Engineering Applications of Artificial Intelligence 126, Part D (2023) 107169.

[15] Chuanpu Fu, Qi Li, and Ke Xu. 2023. Detecting Unknown Encrypted Malicious Trafic in Real Time via Flow Interaction Graph Analysis. In Network and Distributed System Security Symposium (NDSS). The Internet Society.

[16] Chuanpu Fu, Qi Li, Ke Xu, and Jianping Wu. 2023. Point Cloud Analysis for ML-Based Malicious Trafic Detection: Reducing Majorities of False Positive Alarms. In ACM SIGSAC Conference on Computer and Communications Security (CCS). 1005–1019.

[17] Yarin Gal and Zoubin Ghahramani. 2016. Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. In International Conference on Machine Learning (ICML). 1050–1059.

[18] Jakob Gawlikowski, Cedrique Rovile Njieutcheu Tassi, Mohsin Ali, Jongseok Lee, Matthias Humt, Jianxiang Feng, Anna M. Kruspe, Rudolph Triebel, Peter Jung, Ribana Roscher, Muhammad Shahzad, Wen Yang, Richard Bamler, and Xiaoxiang Zhu. 2023. A survey of uncertainty in deep neural networks. Artificial Intelligence Review 56, S1 (2023), 1513–1589.

[19] Denis A. Gudovskiy, Shun Ishizaka, and Kazuki Kozuka. 2022. CFLOW-AD: Real-Time Unsupervised Anomaly Detection with Localization via Conditional Normalizing Flows. In IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). 1819–1828.

[20] Maryam Habibpour, Hassan Gharoun, Mohammadreza Mehdipour, AmirReza Tajally, Hamzeh Asgharnezhad, Afshar Shamsi Jokandan, Abbas Khosravi, and Saeid Nahavandi. 2023. Uncertainty-aware credit card fraud detection using deep learning. Engineering Applications ofArtificial Intelligence 123, Part A (2023), 106248.

[21] Dongqi Han, Zhiliang Wang, Wenqi Chen, Kai Wang, Rui Yu, Su Wang, Han Zhang, Zhihua Wang, Minghui Jin, Jiahai Yang, Xingang Shi, and Xia Yin. 2023. Anomaly Detection in the Open World: Normality Shift Detection, Explanation, and Adaptation. In Network and Distributed System Security Symposium (NDSS).

The Internet Society.

[22] Zongbo Han, Changqing Zhang, Huazhu Fu, and Joey Tianyi Zhou. 2023. Trusted Multi-View Classification With Dynamic Evidential Fusion. IEEE Transactions on Pattern Analysis and Machine Intelligenc (TPAMI) 45, 2 (2023), 2551–2566.

[23] Chao Huang, Chengliang Liu, Zheng Zhang, Zhihao Wu, Jie Wen, Qiuping Jiang, and Yong Xu. 2022. Pixel-Level Anomaly Detection via Uncertainty-aware Prototypical Transformer. In ACM International Conference on Multimedia (MM). 521–530.

[24] Chao Huang, Yushu Shi, Bob Zhang, and Ke Lyu. 2024. Uncertainty-aware prototypical learning for anomaly detection in medical images. Neural Networks 175 (2024), 106284.

[25] Shuodi Hui, Huandong Wang, Zhenhua Wang, Xinghao Yang, Zhongjin Liu, DepengJin, and Yong Li. 2022. Knowledge Enhanced GAN for IoT Trafic Generation. In The ACM Web Conference (WWW). 3336–3346.

[26] Alex Kendall and Yarin Gal. 2017. What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?. In Annual Conference on Neural Information Processing Systems (NIPS). 5574–5584.

[27] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. 2017. Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles. In Annual Conference on Neural Information Processing Systems (NIPS). 6402–6413.

[28] Tae Jun Lee, Justin Gottschlich, Nesime Tatbul, Eric Metcalf, and Stan Zdonik. 2018. Greenhouse: A Zero-Positive Machine Learning System for Time-Series Anomaly Detection. arXiv:1801.03168 (2018).

[29] Xinglin Lian, Yu Zheng, Zhangxuan Dang, Chunlei Peng, and Xinbo Gao. 2025. Semi-supervised anomaly trafic detection via multi-frequency reconstruction. Pattern Recognition 161 (2025), 111215.

[30] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Trafic Classification. In The ACM Web Conference (WWW). 633–642.

[31] Jiaqi Liu, Guoyang Xie, Jin-Bao Wang, Shangnian Li, Chengjie Wang, Feng Zheng, and Yaochu Jin. 2024. Deep Industrial Image Anomaly Detection: A Survey. Machine Intelligence Research 21, 1 (2024), 104–135.

[32] Ximeng Liu, Shizhen Zhao, Yong Cui, and Xinbing Wang. 2024. FIGRET: Fine-Grained Robustness-Enhanced Trafic Engineering. In ACMSIGCOMMConference (SIGCOMM). 117–135.

[33] Ruiying Lu, Yujie Wu, Long Tian, Dongsheng Wang, Bo Chen, Xiyang Liu, and Ruimin Hu. 2023. Hierarchical Vector Quantized Transformer for Multi-class Unsupervised Anomaly Detection. In Annual Conference on Neural Information Processing Systems (NeurIPS). 8487–8500.

[34] Willian Tessaro Lunardi, Martin Andreoni Lopez, and Jean Pierre Giacalone. 2023. ARCADE: Adversarially Regularized Convolutional Autoencoder for Network Anomaly Detection. IEEE Transactions on Network and Service Management (TNSM) 20, 2 (2023), 1305–1318.

[35] Neelu Madan, Nicolae-Catalin Ristea, Kamal Nasrollahi, Thomas B. Moeslund, and Radu Tudor Ionescu. 2024. CL-MAE: Curriculum-Learned Masked Autoencoders. In IEEE/CVF Winter Conference on Applications of Computer Vision (WACV). 2480– 2490.

[36] Andrey Malinin and Mark J. F. Gales. 2018. Predictive Uncertainty Estimation via Prior Networks. In Annual Conference on Neural Information Processing Systems (NeurIPS). 7047–7058.

[37] Marco Rudolph, Tom Wehrbein, Bodo Rosenhahn, and Bastian Wandt. 2022. Fully Convolutional Cross-Scale-Flows for Image-based Defect Detection. In IEEE/CVF Winter Conference on Applications ofComputer Vision (WACV). 1829–1838.

[38] Iman Sharafaldin, Arash Habibi Lashkari, and Ali A. Ghorbani. 2018. Toward Generating a New Intrusion Detection Dataset and Intrusion Trafic Characterization. In International Conference on Information Systems Security and Privacy (ICISSP). 108–116.

[39] Wenxin Tai, Bin Chen, Fan Zhou, Ting Zhong, Goce Trajcevski, Yong Wang, and Kai Chen. 2023. TrustGeo: Uncertainty-Aware Dynamic Graph Learning for Trustworthy IP Geolocation. In ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD). 4862–4871.

[40] Guodong Wang, Shumin Han, Errui Ding, and Di Huang. 2021. Student-Teacher Feature Pyramid Matching for Anomaly Detection. In British Machine Vision Conference (BMVC). 306.

[41] Meng Wang, Tian Lin, Lianyu Wang, Aidi Lin, Ke Zou, Xinxing Xu, Yi Zhou, Yuanyuan Peng, Qingquan Meng, Yiming Qian, et al. 2023. Uncertainty-inspired open set learning for retinal anomaly identification. Nature Communications 14, 1 (2023), 6757.

[42] Wei Wang, Ming Zhu, Xuewen Zeng, Xiaozhou Ye, and Yiqiang Sheng. 2017. Malware trafic classification using convolutional neural network for representation learning. In International Conference on Information Networking (ICOIN). 712–717.

[43] Sanghyun Woo, Jongchan Park, Joon-Young Lee, and In So Kweon. 2018. CBAM: Convolutional Block Attention Module. In European conference on computer vision (ECCV). 3–19.

[44] Limin Yang, Wenbo Guo, Qingying Hao, Arridhana Ciptadi, Ali Ahmadzadeh, Xinyu Xing, and Gang Wang. 2021. CADE: Detecting and Explaining Concept

Drift Samples for Security Applications. In USENIX Security Symposium (USENIX Security). USENIX Association, 2327–2344.

[45] Xincheng Yao, Chongyang Zhang, Ruoqi Li, Jun Sun, and Zhenyu Liu. 2023. One for-All: Proposal Masked Cross-Class Anomaly Detection. In AAAI Conference on Artificial Intelligence (AAAI). 4792–4800.

[46] Bang Xiang Yong and Alexandra Brintrup. 2022. Bayesian autoencoders with uncertainty quantification: Towards trustworthy anomaly detection. Expert Systems with Applications 209 (2022), 118196.

[47] Jiawei Yu, Ye Zheng, Xiang Wang, Wei Li, Yushuang Wu, Rui Zhao, and Liwei Wu. 2021. FastFlow: Unsupervised Anomaly Detection and Localization via 2D Normalizing Flows. arXiv:2111.07677 (2021).

[48] Lianming Zhang, Xiaowei Xie, Kai Xiao, Wenji Bai, Kui Liu, and Pingping Dong. 2022. MANomaly: Mutual adversarial networks for semi-supervised anomaly detection. Information Sciences 611 (2022), 65–80.

[49] Menghao Zhang, Jingyu Wang, Qi Qi, Haifeng Sun, Zirui Zhuang, Pengfei Ren, Ruilong Ma, and Jianxin Liao. 2024. Multi-Scale Video Anomaly Detection by Multi-Grained Spatio-Temporal Representation Learning. In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 17385–17394.

[50] Xuan Zhang, Shiyu Li, Xi Li, Ping Huang, Jiulong Shan, and Ting Chen. 2023. DeSTSeg: Segmentation Guided Denoising Student-Teacher for Anomaly Detection. In IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 3914–3923.

[51] Zilong Zhang, Zhibin Zhao, Xingwu Zhang, Chuang Sun, and Xuefeng Chen. 2023. Industrial anomaly detection with domain shift: A real-world dataset and masked multi-scale reconstruction. Computers in Industry 151 (2023), 103990.

[52] Ruijie Zhao, Mingwei Zhan, Xianwen Deng, Yanhao Wang, Yijun Wang, Guan Gui, and Zhi Xue. 2023. Yet Another Trafic Classifier: A Masked Autoencoder Based Trafic Transformer with Multi-Level Flow Representation. In AAAI Conference on Artificial Intelligence (AAAI). 5420–5427.

[53] Ziming Zhao, Zhaoxuan Li, Zhuoxue Song, Wenhao Li, and Fan Zhang. 2024. Trident: A Universal Framework for Fine-Grained and Class-Incremental Unknown Trafic Detection. In The ACM Web Conference (WWW). 1608–1619.

[54] Yu Zheng, Xinglin Lian, Zhangxuan Dang, Chunlei Peng, Chao Yang, andJianfeng Ma. 2023. A Semi-Supervised Anomaly Network Trafic Detection Framework via Multimodal Trafic Information Fusion. In ACM International Conference on Information and Knowledge Management (CIKM). 4455–4459.
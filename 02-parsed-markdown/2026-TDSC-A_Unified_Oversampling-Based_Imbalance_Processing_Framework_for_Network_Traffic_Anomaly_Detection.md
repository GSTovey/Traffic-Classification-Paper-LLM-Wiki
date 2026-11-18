# A Unified Oversampling-Based Imbalance Processing Framework for Network Traffic Anomaly Detection

Ying Zhong, Zhiliang Wang, Xingang Shi, Jiahai Yang, and Keqin Li Fellow, IEEE

Abstract—Network anomaly detection can provide good protection for network devices. As a mainstream detection algorithm, machine learning/deep learning based intrusion detection systems face the serious impact of imbalanced network traffic training data. A large number of oversampling algorithms have been proposed for the augmentation of network anomaly detection algorithms, but the following problems still exist. In binary classification, it is difficult to learn the complete distribution of attack categories based on the existing imbalanced training set. In multiclassification, there is a problem of class overlap on top of the difficulty of learning the complete distribution. In the case where the generated traffic can be replayed, it is difficult to find a solution in the problem space that can cope with the imbalance based on effective feature space augmentation samples.

For these reasons, we propose the HeteAUG model. On feature space augmentation, we combine interpolation-based and convolutional generative adversarial networks-based augmentation results in a heterogeneous form. For problem space augmentation, a heuristic search algorithm with constraints is used on the basis of effective feature space augmentation samples. Experiments show that our augmentation model outperforms other state-of-the-art (SOTA) models. Specifically, taking the complex Kitsune dataset as an example and using accuracy after augmentation as an evaluation metric, in binary augmentation, we outperform the SOTA algorithm by at least 6.1%. In multiclassification augmentation, we outperform the SOTA algorithm by at most 12.1%. In the augmentation of the binary classification problem space, we compare the accuracy of the classifiers before and after augmentation, and we outperform the imbalanced state by 33.5%. In addition, we discuss the on-the-ground deployment of the model and demonstrate its feasibility.

Index Terms—Network anomaly detection, Oversampling, Interpolation-based augmentation, Generative adversarial networks, Problem space.

## I. INTRODUCTION

ETWORK attacks have caused a great threat to network security<sup>1</sup>. These attacks include denial-of-service (DoS) attack, distributed denial-of-service (DDoS) attack, worm propagation, port scanning, etc. The first intrusion detection system (IDS) [1] is proposed for host intrusion detection. Then, rule matching based network intrusion detection algorithms represented by Snort [2] and Suricata [3] are proposed. However, this class of algorithms cannot detect attacks outside the scope of rules. For this reason, machine learning/deep learning based anomaly detection methods are booming [4]. Machine learning/deep learning can be categorized into three main groups: unsupervised, semi-supervised, and supervised. Unsupervised detection performance is generally worse than supervised [5], [6], [7]. Semi-supervised learning based methods are effective only if there are a large number of unlabeled attack samples, which is sometimes not the case. Supervised learning based intrusion detection systems [8], [9] generally have good detection performance, but are more susceptible to imbalanced training data. We focus on addressing this issue. The following are two common scenarios where imbalance needs to be considered: 1) the attack to be detected itself has a small number of samples and it is difficult for the model to learn an effective detection pattern; 2) collecting samples is time-consuming and laborious, so there is a limited number of samples of attacks to collect.

The basic methods to solve the imbalance problem are oversampling, undersampling, and ensemble learning [10]. Oversampling refers to balancing the proportion of categories in the training dataset by increasing the number of samples from a few categories. Due to the rapid development of generative models [11], the advantages of oversampling augmentation algorithms are more obvious. The two main types of oversampling methods are Generative Adversarial Networks (GAN) [45] and Synthetic Minority Over-sampling Technique (SMOTE) [44]. A large number of oversampling algorithms [39], [40], [41] have been proposed for the augmentation of network anomaly detection algorithms, but the following problems still exist.

Challenge 1: In binary classification anomaly detection<sup>2</sup>, how to minimize the impact of missing distributions on attack augmentation is a difficult problem. Obvious, it is difficult to learn the complete distribution of attack categories based on the existing imbalanced training set. A complete distribution means that samples arriving from the subsequent test set can fall within the distribution of the training set after augmentation. In this way the test set and the training set are more closely matched and thus have better detection capability [12]. Existing augmentation methods all suffer from obvious distributional missing.

(1) GAN-based augmentation methods [31], [32], [33], [34], [35], [36], [37], [38], [39], [40], [41]. First, a GAN model learned based on a small number of attack samples has a high probability of inferring a localized distribution when generating samples for augmentation [13], [14]. Although some valid samples can be inferred, it is difficult to have the effect of converging to a complete distribution. Second, convolution has a function in enriching diversity among data generation for GANs (See TABLE

IV), which is hardly reflected in existing work. Third, very little work considers selecting high-confidence samples for augmentation. High confidence means that the current augmentation sample is recognized as an attack by the well-trained discriminator with high probability. Specifically, most of the work uses a well-trained generator to directly generate augmented data and no longer uses discriminator filtering.

(2) SMOTE-based augmentation method [27], [28], [29]. The idea of SMOTE is to interpolate between two attack samples to get a new attack sample. First, there are fewer existing attack samples, which makes it possible that after SMOTE interpolation only the area enclosed by the existing attack samples can be covered. The attack distribution obtained from this augmentation scenario may be incomplete. Second, the existing attack samples may also be at different locations in the complete distribution. If these attack samples are close to each other in the complete distribution and form a smaller region, this is likely to be missing the larger distribution, as shown in Fig. 1. Third, network traffic data is generally high dimensional after feature extraction. Thus, the interpolation between points becomes sparse, making it even more difficult to cover the complete attack distribution.

![](images/145c92f1014af86f1379b458c717ff388cf0c487824aa36a49bc2a3e257f7009.jpg)  
Fig. 1. Example of SMOTE missing distribution.

Challenge 2: In multiclassification anomaly detection<sup>3</sup>, in addition to the problem of missing attack distributions, there is also the problem of class overlap. Existing augmentation methods have no effective solution to solve these two problems.

(1) GAN-based multi-classification augmentation methods [34], [40]. There are two main types. 1) Train one generator for each type of attack [40]. Each generator learns the classification boundaries between a single specific attack and benign traffic, which misses the global perspective. The goal of multiclassification is to learn the optimal classification boundaries from a global perspective. Thus, this case learns no effective multiclassification bounds. 2) Train one generator for all attacks and the GAN is trained without benign data [34]. This case loses the effect of benign traffic on the boundaries. These two types suffer from the problem of not being able to learn the full distribution of the data generated by the GAN as mentioned earlier. Meanwhile, these methods are multiclassification augmentations, so there is a problem of class overlap [30].

(2) SMOTE-based method for multiclassification augmentation [27], [29]. There are two main types as follows. 1) Considering interpolation augmentation in special regions (multi-

BordlineSMOTE [29]). Some attack data cannot generate augmented samples due to the absence of corresponding special regions. The special region refers to the set formed by the boundary points between benign traffic and attacks. 2) Disregarding interpolation augmentation in special regions (multi-SMOTE [27]). The distributions of multiclassification are generally overlapping [30]. If all attack samples for each attack category are interpolated, this leads to a more severe problem of class overlap. Both types suffer from the problem of not being able to learn the full distribution of the data generated by SMOTE as mentioned before.

Challenge 3: It is difficult to find a corresponding solution in the problem space based on the effective augmentation of samples in the feature space, and the solution can be used for traffic replay. At present, there is no corresponding research work to solve this problem.

(1) Samples in the feature space cannot find correspondences in the problem space, which lacks interpretability at the semantic level [15]. Feature space refers to the space where the network traffic is located after feature extraction. Problem space refers to the original network traffic space. The root cause is that the feature extraction algorithm for network traffic anomaly detection is irreversible [16].

(2) Even if the correspondence between the feature space and the problem space is found, it is difficult to generate samples that not only solve the imbalance problem, but also realize replay [17], which can then be used for data sharing.

Based on the above challenges, we propose the HeteAUG model (a heterogeneous augmentation oversampling framework for feature space and problem space).

To address Challenge 1, we propose the HeteAUG-bi model. This model consists of a complementary convolution-based DCGAN(Deep Convolutional Generative Adversarial Network) model and an interpolation-based SMOTE. The SMOTE can refine the distributions in the vicinity of the existing attack data. The DCGAN model learns the potential attack distributions, and its convolution can increase the diversity of the generated data. Further, we select high-quality samples from DCGANgenerated data. In particular, we give the exploratory structure SMOTE+GAN+X(HeteAUG-bi-X), and X is used for adaptation to environmental differences. Both HeteAUG-bi and HeteAUGbi-X are designed to explore augmentation models that make the distribution more complete. It is not always possible to achieve a complete attack distribution after augmentation, but it is possible to continuously minimize the impact of missing distributions.

To address Challenge 2, we propose the HeteAUG-multi model. This model consists of the complementary convolution-based ACGAN(Auxiliary Classifier Generative Adversarial Network) model and the interpolation-based BordlineSMOTE. The combination of convolutional GAN and interpolative augmentation in the HeteAUG-multi model can effectively minimize the effect of distributional missing. To cope with the class overlap problem, SMOTE is replaced with BordlineSMOTE, DCGAN is replaced with jointly distributed ACGAN, and HeteAUG-multi is trained using only a small amount of benign traffic. After the replacement, both BordlineSMOTE and ACGAN consider the boundary of multiclassification, which is the core of solving the overlap problem. Specifically, BordlineSMOTE performs data augmentation in an attack category that satisfies a condition. A condition means that the attack category has sample points in the boundary region. Sample augmentation in the boundary region improves the generalization ability of the classification model and reduces the risk of overfitting. The ACGAN is used to generate diverse data across all attack categories. Since the conditions for BordlineSMOTE to augment the data are more strict, the second function of ACGAN is to complement the generation of attack categories that BordlineSMOTE cannot augment.

To address Challenge 3, we propose the HeteAUG-P model. The main idea of this model is to find a solution to the corresponding problem space using a heuristic search with constraints based on effectively augmented samples in the feature space. First, the relationship between the feature space and the problem space is established by a genetic algorithm, which makes it possible to jump out of the irreversible problems caused by the feature extraction. Second, we seek samples of the problem space that are closest to the valid feature space augmentation sample, which allows the found samples of the problem space to solve the imbalance problem. The reason is that samples that are close together in feature space have a high probability of belonging to the same distribution. Third, search with constraints in the problem space is an expandable framework. We can relax or continue to add constraints according to our requirements.

Ultimately, to address the augmentation of feature space and problem space, HeteAUG-bi, HeteAUG-multi, and HeteAUG-P form our complete HeteAUG framework. HeteAUG-multi is an upgrade of HeteAUG-bi, considering the class overlap problem. HeteAUG-P is a solution formed on the basis of the solution in the feature space. Additionally, interpolation-based augmentation complemented with convolution-based GAN is the primary design concept. Search with constraints allows this idea to be further generalized to the problem space.

The contributions of our paper are summarized below.

• Novel perspectives on augmentation in feature space and problem space. We propose the HeteAUG model, which is formed by HeteAUG-bi, HeteAUG-multi, and HeteAUG-P. To the best of our knowledge, this is the first oversampling augmentation framework to minimize the impact of missing distributions of attack classes from the perspective of distributional complementation. On feature space augmentation, we combine interpolation-based and convolutional GANbased augmentation results in a heterogeneous form. For problem space augmentation, a heuristic search algorithm with constraints is used based on effective feature space augmentation samples. Meanwhile, considering the variability of attack environments, we exploratively propose the structure of SMOTE+GAN+X. SMOTE+GAN is a generalized structure, and X is used to adapt to the variability of environments.

• Multi-aspects improvements in performance metrics. We test our model on several data sets (TON [50], UKM [52], Kitsune [51]). Experiments show that our model performs better than SOTA binary classification augmentation models (SGM [27], ODDS [32], WCGAN [33], TMG-GAN [40], RAPIER [41]) and multiclassification augmentation models (multi-BorderlineSMOTE [27], TACGAN [34], TMG-GAN [40]), and also we can find replayable solutions in the problem space that can be used for data sharing. Taking the complex Kitsune dataset as an example and using accuracy after augmentation as an evaluation metric, in binary augmentation, we outperform the SOTA algorithm by at least 6.1%. In multiclassification augmentation, we outperform the SOTA algorithm by at most 12.1%. In the augmentation of the binary classification problem space, we compare the accuracy of the classifiers before and after augmentation, and we outperform the imbalanced state by 33.5%. Also, our HeteAUG model has good generalization.

• Complete multi-scenario applicable oversampling framework and open source<sup>4</sup>. For the network traffic anomaly detection system, we implement an open-source oversampling augmentation framework and discuss the grounded deployment of the augmentation framework and prove its feasibility.

The rest of the paper is organized as follows. We summarize the related work in Section II. Background and problem scope is provided in Section III. Section IV introduces our HeteAUG model. This section also describes the three sub-models HeteAUGbi, HeteAUG-multi, and HeteAUG-P in detail. We present the experimental evaluation and analysis in Section V. In Section VI, we first introduce modeling-related issues. Then, we present the limitations and future work. Section VII concludes our work.

## II. RELATED WORK

Network intrusion detection systems are critical in the complex and changing environment of network attacks. Mainstream machine learning/deep learning-based detection systems face the impact of imbalanced data distribution. A large amount of work has been proposed to address this problem [10], [18]. We present related work in three aspects. The first point is imbalanced learning and its application to IDS. The second point is the application of oversampling in IDS. The third point is problem space and data sharing. The last point is large language model and data augmentation.

## A. Imbalanced learning and its application to IDS

Imbalanced learning (IBL) mainly refers to the situation where one class of data in a dataset is much more numerous than the others. Methods for solving the Imbalanced learning problem are divided into three main categories: data-level methods, algorithmlevel methods, and hybrid methods [10]. Data-level methods mainly include undersampling and oversampling methods. Undersampling selects some of the samples from a large class of samples to reduce their number. Oversampling enriches the sample space of small samples by generating new samples. Algorithmic-level approaches to deal with the imbalance problem by modifying the algorithm itself, and the main methods include costly learning methods and model ensemble methods. A hybrid approach considers multiple solutions to imbalance at the same time. The continuous development of imbalance learning also holds promise for the imbalance problem in intrusion detection systems. At the data level, research works based on oversampling [31], [32] , [33] and undersampling [19], [20] have been proposed. [5] presented a data synthesis method for synthesizing distributions of unseen (or future) robot behavior. The synthesis method is distributionaware and uses two different generators in a generative adversarial network to synthesize data for clustered and outlier regions in the feature space. This work is used in bot detection. Three data-based research schemes are constructed step-by-step in [20], namely, data equalization scheme based on conditional VAE, data enhancement scheme based on variance autoencoder (VAE), and data equalization scheme based on random undersampling and conditional VAE. At the algorithmic-level, a number of costsensitive and ensemble learning-based works have been proposed [21], [22], [23], [28]. [21] proposed CSE-IDS, a three-layer NIDS based on cost-sensitive deep learning and ensemble algorithms. Layer 1 of CSE-IDS uses a cost-sensitive deep neural network to differentiate normal traffic from suspicious network traffic. The remaining two layers are further classified correctly using the extreme gradient boosting algorithm and random forest algorithm, respectively. These works have contributed to solving the imbalance problem in IDS. The continuous development of generative modeling has led us to pay more attention to the application of oversampling algorithms in IDS.

TABLE I  
DETAILED COMPARISON OF EXISTING OVERSAMPLING ALGORITHMS FOR NETWORK INTRUSION DETECTION SCENARIOS.

<table><tr><td>Categories</td><td>Model</td><td>MDL</td><td>Problem space</td><td>multi-S</td><td>Generality</td><td>Code</td></tr><tr><td rowspan="3">SMOTE based</td><td>SMOTE/SGM [27]</td><td>no</td><td>no</td><td>yes</td><td>good</td><td>yes</td></tr><tr><td>ADASYN [28]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>yes</td></tr><tr><td>BorderlineSMOTE [29]</td><td>no</td><td>no</td><td>yes</td><td>good</td><td>yes</td></tr><tr><td rowspan="11">GAN based</td><td>G-IDS [31]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no(classic)</td></tr><tr><td>ODDS [32]</td><td>yes</td><td>no</td><td>no</td><td>most</td><td>no(representative)</td></tr><tr><td>WCGAN [33]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no(classic)</td></tr><tr><td>TACGAN [34]</td><td>no</td><td>no</td><td>yes</td><td>most</td><td>no</td></tr><tr><td>B-GAN [35]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no</td></tr><tr><td>MAGNETO [36]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no</td></tr><tr><td>DAE-GAN [37]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no</td></tr><tr><td>WGAN-IDR [38]</td><td>no</td><td>no</td><td>no</td><td>most</td><td>no</td></tr><tr><td>Pedro et al. [39]</td><td>no</td><td>no</td><td>no</td><td>some</td><td>no</td></tr><tr><td>TMG-GAN [40]</td><td>yes</td><td>no</td><td>yes</td><td>good</td><td>yes</td></tr><tr><td>RAPIER [41]</td><td>yes</td><td>no</td><td>no</td><td>most</td><td>yes</td></tr><tr><td>Hybrid</td><td>Our model</td><td>yes</td><td>yes</td><td>yes</td><td>good</td><td>yes</td></tr></table>

1) Multi-distributed learning (MDL) suggests that augmentation algorithm considers multiple situations that can be augmented, or there are multiple sources of models for augmented data. 2) Multi-S means augmentation method supports both multiclassification and bi-classification 3) Generality can be categorized into three types: some indicates augmentation method is effective in at least one network traffic attack detection scenario; most means that the augmentation method is effective in most of the network attack detection scenarios; good represents that the augmentation method is effective in various network traffic attack scenarios including multiclassification.

## B. Application of oversampling in IDS

With the continuous development of generative modeling, oversampling methods continue to emerge. Oversampling methods in IDS systems are mainly categorized into SMOTE-based [27], [28], [29] and GAN-based [31], [32] , [33], [34], [35], [36], [37], [38], [39], [40], [41]. As shown in TABLE I, we compare these algorithms in five aspects. These include whether there is multi-distribution learning, whether they return a problem space, and whether they support multi-classification. Specifically, [27] proposed a novel class imbalance processing technique for largescale datasets, referred to as SGM, which combines the synthetic minority over-sampling technique (SMOTE) and undersampling clustering based on Gaussian Mixture Model (GMM). [28] proposed a network intrusion detection system based on Adaptive Synthesis (ADASYN) oversampling technique and LightGBM. The ADASYN sampling technique adds few samples to address the problem of low detection rate of few attacks due to imbalanced training data. The LightGBM ensemble learning model is applied to reduce the system’s time complexity further while ensuring the accuracy of detection. [40] proposed a data augmentation based intrusion detection method, namely TMG-IDS. Firstly, TMG-GAN has a multi-generator structure that can be used to generate different types of attack data simultaneously. Second, calculating the cosine similarity of the generated samples with the original samples and other types of generated samples as the generator loss can further improve the quality of the generated samples and reduce the class overlap region between the distributions of various generated samples. RAPIER’s idea of addressing imbalances is distributional estimation [41]. RAPIER [41] used the distribution estimation method MADE (masked autoencoder for distribution estimation). Three distributions were estimated: the distribution of malicious samples close to the benign boundary, the distribution of samples outside the training set, and the distribution of benign samples. These types of data distribution are then learned and augmented using the corresponding three generators of the GAN network. These algorithms try to find a pattern that can generalize the true distribution of network traffic. The interpolation-based SMOTE loses potential augmentations that cannot be inferred from data that has already arrived. GAN-based algorithms have powerful learning and inference capabilities, but training sets with few samples are not effective for augmentation because of insufficient information learned. Also, these works do not consider regressing augmentation samples to the traffic space, which is useful for analyzing and detecting attacks. We would like to design the oversampling algorithm from the perspective of distributional inference complementation so that the augmentation can be as close as possible to the real-world equilibrium.

## C. Problem space and data sharing

Problem space is a topic of constant interest for network attack detection. [16] made a formal representation of the problem space. [17] proposed an adversarial attack model in the problem space, and the attack traffic can be replayed in the present network. Rosetta [25] is a TCP semantics-based approach to augmentation on the problem space. For example, subsequent packet replication augmentation is achieved by fast retransmission. This applies to the field of malicious traffic detection. On the other hand, the development of generative modeling has led to new advances in the sharing of network data. [24] presented STAN (synthetic network traffic generation with autoregressive neural models), a tool to generate realistic synthetic network traffic datasets for subsequent downstream applications. [26] explored the use of GAN to automatically learn generative models for generating synthetic packets and traffic header traces for network tasks (e.g., telemetry, anomaly detection). These works inspire us that augmentation samples that can be returned to the problem space have greater proximity to the real world for attack detection.

## D. Large language model and data augmentation

There is no related work in the field of network traffic anomaly detection that uses large language models for data augmentation. We present work in other areas that use large language models for data augmentation [66] [67] [68] [69] [70]. Such methods are suitable for scenarios where natural language is easy to understand, such as banking data, while network traffic data is relatively complex and not well-suited for this approach. Specifically, [66] proposed the use of effective prompt words to generate few samples to solve the problem of imbalanced tabular data classification. [67] proposed the use of prompt words to solve the problem of imbalanced node classification in textual attribute graphs. [68] did a theoretical and practical level analysis of using large language models for data augmentation. As described in the work [66], if these prompt samples do not fully represent the distribution of the original data, the data generated by the large language model may be incomplete and of low quality. This problem is exactly what exists in network traffic anomaly detection and what needs to be addressed in the challenge part of our paper. Moreover, the data generated by the large language model is based on a black box, which is poorly interpretable to some extent. In future work, we can consider using large language models more rationally. For example, large language models can be used to inference the missing distribution of network traffic to effectively augment the data.

## E. Transformer-based time-Series oversampling and diffusion model-based oversampling

Initially, we introduce transformer-based time-series oversampling [71], [72]. [71] proposed using Transformers to enhance GAN-based augmentation, which can be applied to the future optimization of our model. Since this type of work is not in the IDS domain, and the standalone GAN model suffers from distribution missing issues, we do not adopt it as a comparison algorithm. We then introduce diffusion model for augmentation [73] [74]. [73] proposed directly using diffusion models to address imbalance problems, while [75] proposed combining diffusion models with other methods. Finally, we introduce diffusion models for IDS detection [76] [77]. Such studies are few and their augmentation effects are not significant, as diffusion model research primarily focuses on generating better images. For example, experiments on the CICIDS dataset show that the augmentation method proposed in [76] does not outperform classical baseline algorithms in many scenarios. Therefore, diffusion-related works are not considered as baselines. In summary, as a generative model, diffusion needs more optimization and improvement to perform well in IDS augmentation.

Based on the above analysis, we would like to propose a new oversampling framework based on the heterogeneous approach. This framework can try to infer the distribution of complete attack classes based on the existing imbalanced data, and it can also be applied to binary and multi-classification scenarios. Then, these oversampled samples can also find correspondences in the problem space to realize data replay and sharing.

## III. BACKGROUND AND PROBLEM SCOPE

In this section, we first define the research question. Then, we describe the motivation in terms of solving the challenge. Finally, we analyze the infrastructure SMOTE+GAN.

![](images/d47ff47a8ab75f7471b7b72c6959d345bb5335f123314705053513b3755f3942.jpg)  
Fig. 2. Flowchart of the study scope of the augmentation model in the field of IDS.

## A. Problem Definition

The network attack landscape changes all the time, with new attacks appearing all the time. We do not know when a new attack will appear or if the number of attacks is sufficient to train anomaly detection models. Moreover, there are two common scenarios for detection models: binary classification and multiple classification. Furthermore, in the case of insufficient attack samples, it would be convenient to realize data sharing for analysis and use in subsequent tasks.

Based on the above analysis, our research problem is defined as follows. Our goal is that the detection effect of IDS can be improved by oversampling augmentation in the feature space, no matter binary classification or multiclassification, in the absence of attack data. Meanwhile, for our generated samples, we can find the corresponding solutions in the problem space for data sharing and analysis. As shown in Fig. 2, we perform an augmentation study on feature space and problem space.

## B. Research Hypothesis

Similar to other related works [27], [32] , we make the following key assumptions in handling imbalanced network traffic data:

Assumption 1: Data Imbalance. The number of attack samples (minority class) that need augmentation is relatively small, while the number of benign samples (majority class) is relatively large.

Assumption 2: Effectiveness of Generated Data. Synthetic data generated through interpolation methods (such as SMOTE) or generative adversarial networks (GANs) can effectively enrich the training set, enabling classifiers to learn more robust decision boundaries.

## C. Motivation

Previous work on IDS augmentation has focused on the continuous improvement of a particular augmentation model, which obviously reaches the upper bound of that augmentation model. We propose a new augmentation framework that can broaden the boundary of augmentation and complement the distribution. Various good augmentation techniques can be incorporated into our framework. Specifically, on feature space augmentation, we combine interpolation-based and convolutional GAN-based augmentation results in a heterogeneous form. For problem space augmentation, a heuristic search algorithm with constraints is used on the basis of effective feature space augmentation samples. We state our motivation in terms of solving challenges.

![](images/94c16c1551cbadcc002d3614315364b578b858c16122b3a3e401c6f0c9cf36f7.jpg)  
Fig. 3. Corresponding motivation chart for challenge 1.

TABLE II  
MULTIPLE DISTRIBUTION EXTRACTION OF ATTACK DATA IN THE TRAINING SET. (TON-S DATA SET)

<table><tr><td></td><td>Case</td><td>Balance</td><td>Imbalance</td><td>SMOTE</td><td>DCGAN</td><td>ours</td></tr><tr><td rowspan="3">ACC</td><td>c11</td><td>1.000</td><td>0.504</td><td>0.884</td><td>0.575</td><td>0.954</td></tr><tr><td>c12</td><td>1.000</td><td>0.504</td><td>0.984</td><td>0.582</td><td>0.992</td></tr><tr><td>c13</td><td>1.000</td><td>0.504</td><td>0.894</td><td>0.580</td><td>0.961</td></tr><tr><td rowspan="3">F1</td><td>c11</td><td>1.000</td><td>0.337</td><td>0.882</td><td>0.480</td><td>0.954</td></tr><tr><td>c12</td><td>1.000</td><td>0.337</td><td>0.984</td><td>0.490</td><td>0.992</td></tr><tr><td>c13</td><td>1.000</td><td>0.337</td><td>0.893</td><td>0.488</td><td>0.961</td></tr></table>

• ours means SMOTE+DCGAN here.

![](images/0a0581d684783891aeda431205229c5ee1a61a06cda98a1027a49fe384dc8a77.jpg)  
Fig. 4. Corresponding motivation chart for challenge 3.

TABLE III  
MULTIPLE DISTRIBUTIONS OF TEST SETS ARE EXTRACTED. (TON-S DATA SET)

<table><tr><td></td><td>Case</td><td>Balance</td><td>Imbalance</td><td>SMOTE</td><td>DCGAN</td><td>ours</td></tr><tr><td rowspan="3">ACC</td><td>c11</td><td>1.000</td><td>0.504</td><td>0.884</td><td>0.575</td><td>0.954</td></tr><tr><td>c22</td><td>1.000</td><td>0.667</td><td>0.923</td><td>0.721</td><td>0.967</td></tr><tr><td>c33</td><td>1.000</td><td>0.667</td><td>0.916</td><td>0.720</td><td>0.958</td></tr><tr><td rowspan="3">F1</td><td>c11</td><td>1.000</td><td>0.337</td><td>0.882</td><td>0.480</td><td>0.954</td></tr><tr><td>c22</td><td>1.000</td><td>0.534</td><td>0.922</td><td>0.645</td><td>0.967</td></tr><tr><td>c33</td><td>1.000</td><td>0.534</td><td>0.915</td><td>0.642</td><td>0.958</td></tr></table>

• ours means SMOTE+DCGAN here.

TABLE IV  
CALCULATE THE KL DIVERGENCE OF THE DATA GENERATED BY THE VARIOUS OVERSAMPLING METHODS. (TON-S DATA SET)

<table><tr><td>Case</td><td>Divergence</td></tr><tr><td>SMOTE/BordlineSMOTE</td><td>0.606</td></tr><tr><td>SMOTE /Linear GAN</td><td>0.978</td></tr><tr><td>SMOTE/ DCGAN</td><td>8.684</td></tr><tr><td>Linear GAN/DCGAN</td><td>4.631</td></tr></table>

To address Challenge 1, we propose SMOTE+GAN infrastructures with complementary characteristics. As shown in Fig. 3, both SMOTE and GAN have their own augmentation patterns. With the continuous enrichment of augmentation sources, the classification boundary is constantly rationalized. Next, we discuss from the experimental point of view. About the classifier, [40] and [41] use DNN as an evaluation model. So, we mainly use DNN as a classification model for IDS.

We use the TON-s data set [50] for our experiments. The details of the dataset are as follows. The training set of TONs is [’backdoor’, ’ddos’, ’dos’, ’injection’, ’normal’, ’password’, ’scanning’, ’xss’] [ 800, 800, 800, 800, 5600, 800, 800, 800] and the test set is [ 200, 200, 200, 200, 1400, 200, 200, 200]. The imbalanced training set is [2, 2, 2, 2, 5600, 2, 2, 2]. We treat attacks as a class for binary classification augmentation. The evaluation metrics are the results of testing after training using the augmented dataset. Accuracy (ACC) and F1-score (F1) [42] are used here. As shown in TABLE II and TABLE III, our SMOTE+DCGAN has better augmentation performance in all distribution cases. In

TABLE II, the attack extraction in the training set is changed and the benign distribution remains unchanged. c11, c12 and c13 correspond to the attack extraction which is the front-middle-back part of the attack data respectively. The test set is unchanged. Take the ’backdoor’ attack as an example, assume that k consecutive samples are intercepted, where the front-middle-back part refers to k samples starting from the 0th, k samples starting from the 400th, and k samples starting from the (800-k)th. In TABLE III, the distribution of the test set is changed. c11, c22, and c33 correspond to the complete, first half, and second half of the test set, respectively. The training set remains unchanged.

Also, to give diversity to the augmentation data, we emphasize the use of DCGAN with convolution. Convolution belongs to the nonlinear operators, which increases the diversity. To keep the discussion more focused, we will not discuss other nonlinear operators here. We use Kullback-Leibler (KL) divergence [42] to evaluate the diversity. The KL divergence of the data distribution generated by the augmentation method AA and augmentation method BB is calculated here.

As shown in TABLE IV, the divergence of SMOTE with DC-GAN is larger than the divergence of SMOTE with linear GAN. This diversity makes SMOTE with DCGAN better for detection (See Section V). Further, it also shows that convolutional GAN has more variability for linear GAN. Finally, since each attack environment is very different, for example, the edge network with critical services may have more DDoS attacks, while the campus network may have more scanning attacks. This leads to the distribution of attacks can vary widely. Therefore, we explore the proposed representation structure of SMOTE+DCGAN+X. SMOTE+DCGAN serves as the common infrastructure. And X serves as a differential representation of the attack environment. The feasibility of this X structure will be analyzed in the discussion section.

To address Challenge 2, we change the interpolation-based SMOTE to BordlineSMOTE, which is more sensitive to classification boundaries as well as augmentation only in critical regions. The problem of class overlap occurs in multiclassification, so the use of BordlineSMOTE is emphasized. In biclassification problems, either SMOTE or BordlineSMOTE can be selected, and the default choice is to use SMOTE. We change the convolutionbased from DCGAN to ACGAN because the learning of multicategorized data distribution requires the incorporation of finegrained labels. In order to make the learned classification boundaries more reasonable, a moderate amount of benign traffic needs to be added to the training. Meanwhile, BordlineSMOTE may face the situation of some attack categories not satisfying the augmentation conditions. We can use ACGAN to supplement augmentation.

Regarding the solution to Challenge 3, our core idea is to find the augmentation samples in the problem space with the closest distance to the valid augmentation samples in the feature space. As shown in Fig. 4, we take the samples augmented by SMOTE+DCGAN as the set of valid augmentation samples. This is due to the high probability that very close points in the feature space belong to the same distribution. In addition, we number the string-type field data in the network traffic history repository, determine the upper and lower bounds of the numerical data, and then traverse them with constraints, which create conditions for heuristic search. This heuristic search is conducted in the traffic space. Finally, our search is based on effective augmentation samples in the feature space, which gives direction to the search. In summary, our proposed HeteAUG model can better cope with the above three challenges.

## D. Analysis on SMOTE+GAN Infrastructure

1) Effectiveness analysis of SMOTE and GAN in feature space: SMOTE: From a distributional point of view, samples that are close together have a higher probability of belonging to the same category. The samples generated by interpolation are close to two samples from the same distribution. Then, there is a high probability that this generated sample also belongs to this distribution.

GAN: From a classification point of view, classification is equivalent to pattern recognition, which puts samples with similar attributes into a category. The samples after feature extraction are more likely to be recognized by the classifier as a specified type. The generator of a GAN is essentially a classifier. So, the augmentation of GAN is the generation of samples with similar patterns. Based on this premise, our analysis is as follows. ⃝1 Why are samples generated using generators useful? GAN models learned using a small number of malicious attack samples have linear and nonlinear operators. Noise (inputs to GAN’s generator) falls in the neighborhood of the feature space of real samples through these variations. Why is it in the neighborhood of the real samples? This can be explained by the adversarial learning of the generator and discriminator and the distance property of the loss. So, the process is essentially that any noise that passes through the hidden layer can end up in the neighborhood of the original sample and be recognized as malicious by the discriminator. In summary, the generated samples fall in the vicinity of the original attack samples and are recognized as attacks. This indicates that the augmentation of the generator is useful. ⃝2 Why is it necessary to use discriminator selection for the data generated by the generator? Due to limited training data, the generator learns imperfect patterns and needs to select high-confidence samples through discriminators.

2) Why does the combination of SMOTE and GAN enhance detection: The idea of SMOTE augmentation is to interpolate on a straight line formed by two sample points. Assuming that the GAN also always interpolates on a straight line, this conflicts with the fact that the GAN input is noise. The explanation is as follows. The input to the GAN satisfies the mapping relationship with linear interpolation, i.e., the input to the GAN is no longer noise. This can be counterfactually obtained by the fact that the GAN can always generate data that is heterogeneous with SMOTE. Based on the literature in the related work section, both GAN and SMOTE can achieve effective augmentation in separate cases to cope with the imbalance problem to some extent. From the perspective of distributional complementation, the detection performance can be improved when two effective and heterogeneous methods are combined.

Furthermore, if, after feature extraction, the data distribution only exactly matches the distribution of the generated data of SMOTE or GAN, contrary to the randomness of the arriving attacks, this further justifies the combination. As an example, a small amount of attack data is augmented by SMOTE to obtain a more complete simulated data distribution. This simulated data distribution will not be exactly the same as the real attack distribution. This is because the true and complete attack distribution is unpredictable.

![](images/ba44751f855fd0d0036eaeac5f6a8444e2ab0b81d0ef00175b0889de66593d15.jpg)  
Fig. 5. The augmentation workflow of HeteAUG.

![](images/617b3022ab99be2cea6ea115cc97fa9e3fb486e4b2696bee4ec40359f0d444c3.jpg)  
Fig. 6. The specific details of the HeteAUG framework.

3) How to understand that the difference between SMOTE and DCGAN is greater than the difference between SMOTE and linear GAN: KL divergence is an asymmetric measure of the difference between two probability distributions. As the two distributions become more similar, the KL divergence becomes smaller. SMOTE and linear GAN are both linear structures. From the definition of KL divergence, SMOTE and linear GAN generate more similar data, i.e., the distribution of the generated data is more similar, as well as the KL divergence is smaller (as shown in the TABLE IV). That is, the KL divergence is small, and the difference is small. DCGAN comes with the structure of convolution. So, the data generated by SMOTE and DCGAN are more different and have greater KL divergence.

## IV. HETEAUG MODEL

In this section, we first introduce the logical framework of the overall model. Next, the details of each sub-model are presented. We propose the HeteAUG model, which is formed by HeteAUGbi, HeteAUG-multi, and HeteAUG-P.

## A. The augmentation workflow of HeteAUG model

Fig. 5 illustrates the augmentation workflow of HeteAUG framework. Starting from the original imbalanced network traffic dataset, feature extraction is first performed. Then, data augmentation is carried out through two modules: HeteAUG-bi for binary classification and HeteAUG-multi for multi-class classification, producing augmented samples. These samples are subsequently used in two parallel paths. On one hand, they form a balanced feature-space dataset for model training, ultimately yielding more robust intrusion detection classifiers. On the other hand, they are fed into HeteAUG-P (problem space mapping) to generate replayable real network traffic packets or flows.

## B. HeteAUG-bi model

As shown in Fig. 6 (left), our HeteAUG-bi model is described in detail. This model consists of DCGAN and SMOTE. We use only attack data for augmentation in this part. First, SMOTE is augmented by interpolation to obtain AUG-bi-1 (augment sample1). Next, we use the attack data to train the DCGAN model. The corresponding attack augmentation data is then generated using the generator. These directly generated samples need to pass through the discriminator. If the probability of discriminating as a malicious attack is greater than a certain threshold, then it is selected as an augmentation sample. The samples augmented by DCGAN are called AUG-bi-2 (augment sample2). AUG-bi-1 and AUG-bi-2 together serve as the final augmentation samples. The theoretical foundations of SMOTE and DCGAN are shown below.

SMOTE [44]: Step 1: Randomly select two samples $s _ { 1 } , \ s _ { 2 }$ from the attack data. Step 2: Randomly select a variable λ from [0,1]. Step 3: Use λ to interpolate in $s _ { 1 }$ and $s _ { 2 }$ to get a new augmentation sample. We can implement SMOTE using a tool library [43].

DCGAN [45]: In order to learn the distribution $p _ { g }$ of the generator over the data x, a priori value of the input noise variable $p _ { z } ( z )$ is first defined, and then the mapping to data space is denoted as $G \left( z ; \delta _ { g } \right)$ . Where $G$ is composed of inverse convolutional operators parameterized by $\delta _ { g }$ . Next, $D \left( \pmb { x } ; \delta _ { d } \right)$ is defined based on convolutional operators, which outputs a single scalar. $D ( \pmb { x } )$ denotes the probability that x comes from the data distribution $p _ { d a t a }$ instead of the $p _ { g } .$ We train $D$ to maximize the probability of assigning correct labels to the training instances and the samples generated by $p _ { g }$ . We also train $G$ to minimize log $\left( 1 - D ( G ( z ) ) \right)$ . That is to say, D and $G$ are playing the following two-player minimization game with value function $V A ( G , D )$

$$
\begin{array}{l} \min _ {G} \max _ {D} V A (D, G) = \mathbb {E} _ {\boldsymbol {x} \sim p _ {\mathrm{data}} (\boldsymbol {x})} [ \log D (\boldsymbol {x}) ] \\ + \mathbb {E} _ {\boldsymbol {z} \sim p _ {\boldsymbol {z}} (\boldsymbol {z})} [ \log (1 - D (G (\boldsymbol {z}))) ] \end{array}\tag{1}
$$

## C. HeteAUG-multi model

In order to better cope with the class overlap problem of multiclassification, the BorderlineSMOTE, which interpolates within the attacking classes, and the convolution-based ACGAN, which considers label generation, are chosen. As shown in Fig. 6 (center), our HeteAUG-multi model is described in detail.

This model consists of ACGAN and BordlineSMOTE. The classification boundary of multi-classification is also affected by benign traffic. The augmentation of this case is used for both benign and attack samples. Here, BordlineSMOTE is designed for multi-classification; we also call it multi-BordlineSMOTE. The core idea of multi-BordlineSMOTE is as follows. First, we differentiate the attack data according to fine-grained labels. For the attack category attack , find the set of these samples that satisfy the Danger property. Then, the SMOTE algorithm will be used for interpolation augmentation in this set. The labels of these augmentation data are also the attack categories currently analyzed. The Danger property here refers to the case where more than half of the surrounding samples are majority-class samples but not all majority-class samples. We use multi-BordlineSMOTE to get the augmentation data AUG-multi-1. Then, we use some of the benign data and all of the attack data as the training data for ACGAN. After ACGAN is trained, we use the generator to generate augmentation samples for each category and get AUGmulti-2. Here, the input to the generator needs to be labeled to specify the category of augmentation. Next, we check the augmentation data in AUG-multi-1. If there are attack categories for which no augmentation samples are generated due to the absence of the Danger property, then we use ACGAN to supplement the augmentation of these categories further. We call this AUG-multi-3. AUG-multi-1, AUG-multi-2, and AUG-multi-3 together serve as the final augmentation samples. The theoretical foundations of BordlineSMOTE and ACGAN are shown below.

BordlineSMOTE [46]: Step 1: For each $a _ { i } ( i \ = \ 1 , 2 , . . . ,$ a num ) in the minority attack category A, we compute its $k$ nearest neighbors from the entire training set Tr. Among these $k$ nearest neighbors, the number of most examples is denoted as $k ^ { \prime }$ $( k ^ { \prime } \left( 0 \leq k ^ { \prime } \leq k \right) )$ .

Step 2: If $k ^ { \prime } = k , \mathrm { i . e . }$ , all k near neighbors of $a _ { i }$ are majority examples, $a _ { i }$ is treated as noise and there are no following steps. If $k / 2 \le k ^ { \prime } < k .$ namely the number of $\arcsin$ majority nearest neighbors is greater than the number of its minority nearest neighbors, $a _ { i }$ is considered to be vulnerable to misclassification and is placed in the DANGER set. If $0 \leq k ^ { \prime } < k / 2 , a _ { i }$ is safe and need not participate in the following steps.

Step 3: The example in DANGER is the borderline data for the minority attack category A. It can be seen that $D A N G E R \subseteq A$ Specifically,

$$
\text { DANGER } = \left\{a _ {1} ^ {\prime}, a _ {2} ^ {\prime}, \dots , a _ {\text { d\_num }} ^ {\prime} \right\}, \quad 0 \leq \text { d\_num } \leq \text { a\_num }\tag{2}
$$

For each example in DANGER, we compute its nearest kk neighbors from A.

Step 4: Augmentation of selected samples in DANGER using the SMOTE algorithm.

ACGAN [47]: In auxiliary classifier GAN (ACGAN), each generated sample has a corresponding class label $c \sim p _ { c }$ and a noise z. The generated data requires the use of both, $\mathrm { i . e . , } x _ { \mathrm { f a k e } } ~ =$ $G ( c , z )$ . The discriminator gives both a probability distribution over sources and a probability distribution over the class labels, $P ( S S \mid x ) , P ( C C \mid x ) = D ( x )$ . D and $G$ are the discriminator and generator, respectively.

The objective function consists of two parts: the log probability of the correct source, $L _ { S S }$ , and the log probability of the correct class, $L _ { C C }$

$$
\begin{array}{l} L _ {S S} = E \left[ \log P \left(S S = \text {real} \mid x _ {\text {real}}\right) \right] + \\ E \left[ \log P \left(S S = \text {fake} \mid x _ {\text {fake}}\right) \right] \\ L _ {C C} = E \left[ \log P \left(C C = c \mid x _ {\text {real}}\right) \right] + \\ E \left[ \log P \left(C C = c \mid x _ {\text {fake}}\right) \right] \end{array}\tag{3}
$$

The training objective of $D$ is to maximize $L _ { S } + L _ { C }$ , while the training objective of G is to maximize $L _ { C } - L _ { S }$ . ACGAN learns a class label-independent representation for z.

## D. HeteAUG-p model

As shown in Fig. 6 (right), our HeteAUG-P model is described in detail. In the augmentation model for binary classification, we obtain the final augmentation samples AUG-bi-1 and AUG-bi-2 in the feature space. We categorize the corresponding fields of all columns of the 2D data table formed by network packets, or network flows in the problem space into numeric and string types. For the string type, we save the records to the specified database according to the history. The records are de-duplicated and numbered. For example, to form a source IP address database. For numeric types, we give reasonable upper and lower bounds. For example, the source port can be 1-65535. After processing down here, all the fields are traversable. Then, we use a genetic algorithm for searching, and each field corresponds to one variable. The fitness function of the genetic algorithm is the minimum distance between the searched samples after feature extraction and the existing and valid augmentation samples (AUGbi-1 and AUG-bi-2) in the feature space. While searching, we have to put constraints on the searched samples so that they fulfill the requirement that the network traffic can be replayed. Our constraint can be “If the protocol is TCP, then the UDP protocol-related fields are empty.” A record in the problem space can be “1487598190, 192.168.3.2, 192.168.100.2, 2, ... ”. The specific algorithmic flow of HeteAUG can be found in Part 5 of the Appendix. The process of genetic algorithm is as follows.

Genetic algorithm<sup>5</sup> [48]: The feature space and problem space of network traffic are irreversible, and solving them requires the use of optimization algorithms [49]. We use the genetic algorithm as a search algorithm. The basic steps are as follows: Coding: All fields of each packet act as a chromosome. Each field represents a gene. For example, the source port is a gene with a value range of 1-65535. Gene location 8080 is its source port. Initialization: Randomly generate N chromosomes to form the initial population, N is set to 50. Fitness function: The Euclidean distance between a sample on the problem space after feature extraction and a valid augmentation sample on the feature space. Selection: Select the search sample whose fitness function returns a small value. Crossover: Individuals participating in the crossover are selected according to the probability $P _ { c }$ . Mutation: According to the mutation rate $P _ { m } ,$ some individuals in the offspring will be randomly changed in a certain position. Termination: After T generations, the genetic algorithm selects the best combination of fields. The parameters of the genetic algorithm are set as follows: the initial population size is set to 50, the number of generations T is set to 10, the crossover probability $P _ { c }$ is set to 0.6, and the mutation probability $P _ { m }$ is set to 0.02.

## E. Convergence and unity analysis of HeteAUG

HeteAUG-bi and HeteAUG-multi can be analyzed together. SMOTE and Borderline-SMOTE, as interpolation algorithms, have inherently guaranteed convergence. Our main discussion focuses on the DCGAN and ACGAN components. The training convergence of GANs can be characterized through Nash equilibrium—the generator and discriminator are optimized alternately through a minimax game. In practice, various optimization strategies can be employed to improve convergence stability [48]. HeteAUG-P performs problem space search based on genetic algorithms. According to the convergence theory of genetic algorithms [48], when employing an elitist preservation strategy, the algorithm will converge to the global optimal solution.

Next, we analyze the unity of the HeteAUG framework. All modules collaboratively serve the common goal of optimizing downstream classifier detection performance from different perspectives, with each module complementing the others. Information flows exist between optimization objectives and modules, as well as between modules themselves. This demonstrates that coupling relationships exist among the modules.

## V. EXPERIMENTAL EVALUATION AND ANALYSIS

To explore the effectiveness of our augmentation model, we conduct a series of experiments. We first present the data set and experimental configurations. Then, we use a rational experimental design to validate our model. Meanwhile, we analyze the experimental results in the order of the main research questions to further reveal the insights behind the experimental results. The code of our algorithm is available for download. The main problems of our research are as follows.

• How does our augmentation model perform in binary classification?

• How does our augmentation model perform in other classifiers?

• How does our augmentation model perform in multiclassification?

• How does our augmentation model perform in the problem space?

• Is the component selection of our augmentation model effective?

## A. Datasets

We use three data sets, ToN IoT2019 [50], Kitsune2018 [51], and UKM2020 [52]. These three datasets represent relatively new pcap-based and relatively new flow-based network attack detection datasets. There is variability in the attacks contained within these three datasets. This makes the selected datasets better heterogeneous and representative. The ToN IoT2019 dataset is a next generation Industry 4.0/Internet of Things (IoT) and Industrial Internet of Things (IIoT) dataset. We have selected 8 attacks for our experiments. This includes injection, password, ransomware, etc. We are using flow format for this dataset. Specifically, we select 21 fields with fewer missing values from the complete flow data. Then, we normalize the data after selection. ToN IoT2019 dataset can be notated as TON.

Kitsune2018 includes four main categories of attacks: reconnaissance, botnets, denial of service, and man-in-the-middle. A more fine-grained categorization will be shown in the dataset introduction. The feature extraction method used here is Kitsune’s own. The dataset is raw network traffic. The dimension after feature extraction is 100. This dataset is used for traffic replay experiments in the problem space. Kitsune2018 is also notated as Kitsune.

UKM2020 is a relatively new dataset. It contains four types of attacks, namely DoS, ARP poisoning, vulnerability exploitation and scanning. This dataset can reflect attacks in new network environments. We use 46 fields from the original flow as features after normalization. UKM2020 can also be denoted as UKM.

## B. Evaluation Metrics

The accuracy of classification is the main metric evaluated. We abbreviate accuracy as ACC. For a more comprehensive assessment, we also use other metrics [42]: AUC, P a, R a, F1 a, Gmean a, TPR, FPR, F1, AUROC, AUPRC. We categorize the above indicators into three categories. The first category is ACC for both the binary and multiple classifications. In the second category, common assessment metrics that apply only to binary classification. These metrics are TPR (true positive rate), FPR (false positive rate), F1, AUC (area under curve), AU-ROC(Area Under the Receiver Operating Characteristic Curve), AUPRC(Area Under the Precision-Recall Curve). F1 is the reconciled average of precision and recall. AUC is defined as the area under the ROC curve enclosed with the axes. The third category is applicable to both the binary and multiple classifications, but these indicators are calculated by averaging across categories. These metrics are avg Precision which means weighted avg Precision as P a, avg Recall as R a, avg F<sub>1</sub> as F1 a, and avg Gmean as G a. Weighted averaging means calculating the metrics for each label and averaging them out weighted by support(the number of instances for each label). avg Gmean is the geometric mean of the performance metrics that identify all positive and negative examples. $\mathrm { F 1 \_ a , G \_ a , }$ and F1 are often used to evaluate imbalanced classification problems. Lower FPR is better. For other metrics, the higher the value, the better. See Part 8 of the Appendix for details.

## C. Experimental Settings

1) Specific Experimental Environment: Python is used to im plement our model and comparison algorithm. We extract imbalanced data according to the first arriving data. Each subclass of attacks is extracted. Our core experiments have three main data sets. The specific information is given below. The training set of TON is [’backdoor’, ’ddos’, ’dos’, ’injection’, ’normal’, ’password’, ’scanning’, ’xss’] [ 16000, 16000, 16000, 16000, 130000, 16000, 16000, 16000] and the test set is [4000, 4000, 4000, 4000, 20000, 4000, 4000, 4000]. The imbalanced training set is [10, 10, 10, 10, 130000, 10, 10, 10]. Values represent the number of corresponding attacks. The training set of UKM is [’ARP poisining’, ’BeEF HTTP exploits’,’Mass HTTP requests’,’Metasploit exploits’, ’Normal’,’Port scanning’,’TCP flood’,’UDP data flood’] [476, 404, 461, 441, 7141, 474, 467, 445] and the test set is [ 116, 96, 140, 106, 1768, 123, 121, 108]. The imbalanced training set is [2, 2, 2, 2, 7141, 2, 2, 2]. The training set of Kitsune is [’Normal’, ’Mirai’, ’Fuzzing’, ’SSDP Flood’, ’ARP MitM’, ’Active Wiretap’, ’SSL Renegotiation’, ’SYN DoS’, ’OS Scan’, ’Video Injection’] [601349, 20001, 18147, 27856, 28513, 37716, 10595, 6951, 29709, 29163] and the test set is [38585, 10000, 4647, 9849, 9492, 9541, 10, 87, 4447, 3342]. The imbalanced training set is [601349, 300, 300, 300, 300, 300, 300, 300, 300, 300]. For different data distributions, we extract the smaller dataset TON-s. The training set of TON-s is [’backdoor’, ’ddos’, ’dos’, ’injection’, ’normal’, ’password’, ’scanning’, ’xss’] [ 800, 800, 800, 800, 5600, 800, 800, 800] and the test set is [ 200, 200, 200, 200, 1400, 200, 200, 200]. The imbalanced training set is [2, 2, 2, 2, 5600, 2, 2, 2]. Each instance is a labeled record of the data set. For time series data, we use the hold-out method. The hold-out method directly splits the data set DD into two mutually exclusive sets. One of them serves as the training set tr and the other as the test set te. That is, DD = tr ∪te and tr ∩te = ϕ. All the samples in the training set are ahead of the test set in the time order. For binary classification experiments, we can simply treat the attack class as one big class. For multi-classification experiments, we can use these data sets directly. For the problem space, we experiment with some of the individual data subsets from the Kitsune data set. For complex problem space data sets, we use the configuration of the Kitsune data set at the time of binary classification, i.e., we treat the attack category as a class. The results of all experiments are averaged over five trials. We use a server with AMD EPYC 7402 24-Core Processor and 256G of RAM as the device. The type of GPU we use is GTX 3090. The hardware and software configurations are shown in Part 6 of the Appendix.

2) Hyperparameter configuration of our model: Our parameters are divided into three main parts, corresponding to HeteAUGbi, HeteAUG-multi, and HeteAUG-P. The specific meanings of the parameters and their referenced assignments are listed below. ⃝1 HeteAUG-bi : Nearest neighbor parameter of SMOTE k=5, Noise vector dimension of DCGAN z dim=100, Learning rate of DCGAN lr= 0.0001, High-quality decision thresholds for DCGAN-generated data 0.525; ⃝2 HeteAUG-multi: Nearest neighbor parameter of BordlineSMOTE kk=5, Noise vector dimension of ACGAN z dim2=100, Learning rate of ACGAN lr2= 0.0002, Percentage of ACGAN benign data used BEP=0.1; ⃝3 HeteAUG-P: Number of contextually benign samples=100.

## D. Baseline model

For a fairer comparison, we only compare the oversampling algorithms. If the algorithm has other measures to solve the imbalance, we only select the oversampling part for comparison. This is because other imbalance measures can be used in our model and other models as well. The comparison experiments use the same features.

1) Binary classification: For IDS-based models, we only compare the oversampling parts. Our comparison algorithms are SGM/SMOTE [27], ADASYN [28], BorderlineSMOTE [29], G-IDS [31], ODDS [32], WCGAN [33], TMGGAN [40], and RAPIER [41]. To further demonstrate the superiority of our algorithm, we also compare it with excellent non-IDS algorithms. The comparative non-IDS models are BFGAN [53], SMOTE-GAN [54], SMOTified-GAN [55]. The details are described in Part 9 of the Appendix.

2) Multi-classification classification: For IDS-based models, we only compare the oversampling parts. Our comparison algorithms are multi-SMOTE [27], multi-BorderlineSMOTE [29], TACGAN [34] (denoted as ACGAN⊖ with JDA), and TMG-GAN [40]. Similarly, we compare non-IDS algorithms. The non-IDS model used for comparison is EOS [56]. A detailed description is in Part 9 of the Appendix.

## E. Answers to key questions and analysis of experimental results

In this section, we conduct a series of experiments to verify our model.

1) How does our augmentation model perform in binary classification: We evaluate the effectiveness of our model in binary augmentation in the following three aspects.

In the first aspect, we compare with IDS-based SOTA binary classification augmentation methods. The comparison algorithms mainly include GAN-based and SMOTE-based related algorithms. As shown in TABLE V, our algorithms achieve the best augmentation results on each dataset. In particular, on the complex Kitsune dataset, the accuracy of our augmentation algorithm is 0.871. The second-place algorithm, WCGAN, has an accuracy of 0.810. We have improved the accuracy by at least 6.1% on this dataset.

We conduct a detailed analysis. First, we conduct a general analysis. In order to better represent the effect of augmentation, we first observe the detection effect of balanced and unbalanced states. It can be seen that the TON and Kitsune datasets are more seriously affected by the imbalance, while the UKM dataset has little effect. This has a strong correlation with the collection form of the dataset and the data distribution after feature extraction. The analysis reveals that the GAN-based algorithm performs better on the Kitsune-based dataset. The SMOTE-based algorithm performs better on the flow-based TON and UKM datasets. This indicates that there are differences in terms of the performance of different augmentation algorithms for different distributions.

TABLE V  
COMPARISON OF IDS-RELATED OVERSAMPLING METHODS IN BINARY CLASSIFICATION. (ACC)

<table><tr><td>model</td><td>TON</td><td>UKM</td><td>Kitsune</td></tr><tr><td>imbalance</td><td>0.512</td><td>0.952</td><td>0.513</td></tr><tr><td>balance</td><td>0.930</td><td>0.998</td><td>0.928</td></tr><tr><td>SMOTE/SGM [27]</td><td>0.738</td><td>0.968</td><td>0.757</td></tr><tr><td>ADASYN [28]</td><td>0.744 $\triangle$ </td><td>0.971</td><td>0.670</td></tr><tr><td>B-S [29]</td><td>0.807 $\triangle$ </td><td>0.972</td><td>0.579</td></tr><tr><td>G-IDS [31]</td><td>0.579</td><td>0.963</td><td>0.570</td></tr><tr><td>ODDS [32]</td><td>0.669</td><td>0.967</td><td>0.784</td></tr><tr><td>WCGAN [33]</td><td>0.576</td><td>0.964</td><td>0.810</td></tr><tr><td>TMG-GAN [40]</td><td>0.662</td><td>0.961</td><td>0.614</td></tr><tr><td>RAPIER [41]</td><td>0.614</td><td>0.965</td><td>0.656</td></tr><tr><td>ours</td><td>0.835 $\triangle$ </td><td>0.979</td><td>0.871</td></tr></table>

• ours means HeteAUG-bi.  
• B-S refers BorderlineSMOTE.  
•△ denotes the Top3 algorithm.

Second, the performance of each algorithm is analyzed. With continuous improvement, SMOTE-related algorithms have significantly improved their detection on the TON dataset. For example, BordlineSMOTE has better detection than SMOTE. However, this is the opposite of the Kitsune dataset. The dimension of the TON dataset is 21 dimensions.The feature extraction algorithm of the Kitsune dataset is more complex and the dimension of the features has increased to 100 dimensions. Also the type and number of attacks on Kitsune has increased in comparison. The original version of the GAN was a linear GAN, represented as G-IDS. It is clear that there is an improvement in detection compared to imbalance, but it is still limited. ODDS uses two generators to learn more optimal distributions, with a noticeable improvement. WCGAN incorporates benign data into the model training, which is effective for the Kitsune dataset but not for TON and UKM. TMG-GAN uses cosine similarity to give diversity to the generated samples but does not complement missing distributions outside of GAN. RAPIER first estimates distributions using MADE and then augmentation in the two abnormal and benign species. the MADE dataset learns distributions with a large bias in the imbalanced dataset, which affects the final detection results. Various forms of improvement of GAN and SMOTE always fall short of our detection results, which illustrates the problem of missing distributions. This shows the importance of distribution complementation and the effectiveness of HeteAUG-bi.

The second aspect is our comparison with non-IDS augmentation algorithms. SMOTified-GAN essentially takes the SMOTE augmentation data as the noise input to the GAN. BFGAN has benign traffic added to the model training, and the concept of importance has been proposed. However, these two are still limited by the disadvantage of missing distribution. SMOTE+L is a combination of SMOTE and linear GAN, which can supplement the distribution to some extent. The comparison with our model illustrates the role of convolution in generating sample diversity. As shown in TABLE VI, our model has the best augmentation effect.

In the third aspect, we put the above comparison algorithms on the TON dataset to observe various metrics. As shown in TABLE VII, our augmentation model has the best performance.

2) How does our augmentation model perform in other classifiers: To verify the performance of our algorithm on other classifiers, we conduct experiments on five classifiers, including DNN. We use the TON-s dataset for our experiments. The other four classifiers are classifiers from various IDS systems. These include CNN [57], onedcnn [58], DNN-KNN [59], DNN+CL [9]. Meanwhile, we test the Top 3 algorithms on each classifier. As shown in TABLE VIII, our augmentation algorithm has the best augmentation effect on each classifier. Among them, we achieve the optimal augmentation in the latest classifier, DNN+CL. Obviously, compared to other classifiers, CNN is more severely affected by imbalance after augmentation.

In conclusion, our augmentation model is effective on all classifiers.

3) How does our augmentation model perform in multiclassification: To validate the detection effectiveness of our model in multiclassification augmentation, we compare it with four IDSbased multiclassification augmentation algorithms. These include multi-SMOTE [27], multi-BorderlineSMOTE [29], ACGAN⊖ with JDA [34], and TMG-GAN [40]. We also compare with non-IDS EOS [56]. Multi-classification augmentation is a difficult problem in imbalanced augmentation, and we mainly observe the improvement of augmentation performance. We conduct experiments in the following two aspects.

The first aspect is experimented on three datasets. As shown in TABLE IX, our augmentation model performs best on each dataset. Here, HeteAUG-multi means ACGAN with JDA+multi-BorderlineSMOTE. ⊖ indicates that the corresponding ACGAN training did not use benign data. In particular, our accuracy in the Kitsune dataset is 0.623, while that of ACGAN⊖ with JDA is 0.502. In comparison, we improve it by 12.1%. We perform a detailed analysis. It can be seen that SMOTE-related algorithms still perform better on the TON dataset. ACGAN with benign traffic performs better on the Kitsune dataset. It is worth noting that on the UKM dataset, there are only two attack samples in each category, and many augmentation algorithms play a side effect. The EOS algorithm, which is essentially an improved algorithm of SMOTE, performs mediocrely on the Kitsune dataset but achieves a good detection effect on UKM, which indicates that the distribution of the UKM dataset just meets the conditions of the selection of augmentation samples for EOS. HeteAUG-multi adds a moderate amount of benign data to HeteAUG-multi⊖ to join the training. This demonstrates the importance of adding a moderate amount of benign data for learning better classification boundaries.

In the second aspect, we compare with the comparison algorithms on various metrics. As shown in TABLE X, our algorithm achieves the best performance. AUC is not significant in multiclassification so it is not used here. AUROC and AUPRC are used •S+L denotes combination of SMOTE •and linear GAN. ours means HeteAUG-bi

TABLE VI  
TABLE VII  
COMPARISON OF BINARY OVERSAMPLING METHODS UNDER MULTIPLE METRICS. (TON DATA SET)  
COMPARISON OF NON-IDS-RELATED OVERSAMPLING METHODS IN BINARY CLASSIFICATION. (ACC)

<table><tr><td>model</td><td>TON</td><td>UKM</td><td>Kitsune</td></tr><tr><td>imbalance</td><td>0.512</td><td>0.952</td><td>0.513</td></tr><tr><td>balance</td><td>0.930</td><td>0.998</td><td>0.928</td></tr><tr><td>BFGAN [53]</td><td>0.593</td><td>0.965</td><td>0.753</td></tr><tr><td>SMO-G [55]</td><td>0.753</td><td>0.965</td><td>0.593</td></tr><tr><td>S+L [54]</td><td>0.784</td><td>0.970</td><td>0.772</td></tr><tr><td>ours</td><td>0.835</td><td>0.979</td><td>0.871</td></tr></table>

•SMO-G refers SMOTified-GAN.

<table><tr><td>model</td><td>P_a</td><td>R_a</td><td>F1_a</td><td>AUC</td><td>ACC</td><td>G_a</td><td>AUROC</td><td>AUPRC</td></tr><tr><td>SMOTE [27]</td><td>0.744</td><td>0.738</td><td>0.740</td><td>0.738</td><td>0.738</td><td>0.738</td><td>0.769</td><td>0.799</td></tr><tr><td>ADASYN [28]</td><td>0.819</td><td>0.744</td><td>0.741</td><td>0.775</td><td>0.744</td><td>0.752</td><td>0.774</td><td>0.801</td></tr><tr><td>B-S [29]</td><td>0.843</td><td>0.807</td><td>0.807</td><td>0.826</td><td>0.807</td><td>0.818</td><td>0.817</td><td>0.835</td></tr><tr><td>G-IDS [31]</td><td>0.791</td><td>0.579</td><td>0.531</td><td>0.639</td><td>0.579</td><td>0.527</td><td>0.643</td><td>0.699</td></tr><tr><td>ODDS [32]</td><td>0.816</td><td>0.669</td><td>0.651</td><td>0.716</td><td>0.669</td><td>0.657</td><td>0.716</td><td>0.763</td></tr><tr><td>WCGAN [33]</td><td>0.763</td><td>0.576</td><td>0.531</td><td>0.633</td><td>0.576</td><td>0.530</td><td>0.638</td><td>0.698</td></tr><tr><td>TMGGAN [40]</td><td>0.814</td><td>0.662</td><td>0.642</td><td>0.710</td><td>0.662</td><td>0.649</td><td>0.711</td><td>0.759</td></tr><tr><td>RAPIER [41]</td><td>0.650</td><td>0.614</td><td>0.614</td><td>0.632</td><td>0.614</td><td>0.623</td><td>0.668</td><td>0.723</td></tr><tr><td>BFGAN [53]*</td><td>0.794</td><td>0.593</td><td>0.550</td><td>0.651</td><td>0.593</td><td>0.549</td><td>0.647</td><td>0.706</td></tr><tr><td>SMO-G [55]*</td><td>0.775</td><td>0.753</td><td>0.754</td><td>0.765</td><td>0.753</td><td>0.761</td><td>0.767</td><td>0.776</td></tr><tr><td>S+L [54]*</td><td>0.784</td><td>0.784</td><td>0.784</td><td>0.776</td><td>0.784</td><td>0.775</td><td>0.807</td><td>0.830</td></tr><tr><td>HeteAUG-bi</td><td>0.873</td><td>0.835</td><td>0.836</td><td>0.856</td><td>0.835</td><td>0.847</td><td>0.856</td><td>0.874</td></tr></table>

•∗ means that it is not an IDS-related oversampling method. SMOTE refers SMOTE/SGM.

TABLE VIII  
PERFORMANCE OF TOP3’S OVERSAMPLING METHOD IN VARIOUS IDS SYSTEMS. (TON-S DATA SET, ACC)

<table><tr><td>model</td><td>DNN</td><td>CNN [57]</td><td>onedcnn [58]</td><td>DNN-KNN [59]</td><td>DNN+CL [9]</td></tr><tr><td>imbalance</td><td>0.504</td><td>0.507</td><td>0.764</td><td>0.793</td><td>0.505</td></tr><tr><td>balance</td><td>1.000</td><td>1.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ADASYN</td><td>0.884</td><td>0.816</td><td>0.912</td><td>0.905</td><td>0.876</td></tr><tr><td>B-S</td><td>0.807</td><td>0.863</td><td>0.903</td><td>0.845</td><td>0.941</td></tr><tr><td>ours</td><td>0.952</td><td>0.884</td><td>0.921</td><td>0.954</td><td>0.962</td></tr></table>

• ours means HeteAUG-bi. Top3 means △ in TABLE V.

TABLE IX  
COMPARISON OF OVERSAMPLING METHODS IN MULTICLASSIFICATION. (ACC)

<table><tr><td>model</td><td>TON</td><td>UKM</td><td>Kitsune</td></tr><tr><td>balance</td><td>0.930</td><td>0.998</td><td>0.928</td></tr><tr><td>imbalance</td><td>0.423</td><td>0.927</td><td>0.499</td></tr><tr><td>multi-SMOTE [27]</td><td>0.647</td><td>0.928</td><td>0.500</td></tr><tr><td>multi-BorderlineSMOTE [29]</td><td>0.669</td><td>0.901</td><td>0.531</td></tr><tr><td>ACGAN $\ominus$  with JDA [34]</td><td>0.510</td><td>0.905</td><td>0.502</td></tr><tr><td>ACGAN with JDA</td><td>0.526</td><td>0.908</td><td>0.558</td></tr><tr><td>TMG-GAN [40]</td><td>0.529</td><td>0.917</td><td>0.537</td></tr><tr><td>EOS [56] *</td><td>0.624</td><td>0.945</td><td>0.517</td></tr><tr><td>HeteAUG-multi $\ominus$ </td><td>0.701</td><td>0.945</td><td>0.576</td></tr><tr><td>HeteAUG-multi</td><td>0.705</td><td>0.946</td><td>0.623</td></tr></table>

• ∗ means that it is not an IDS-related oversampling method.

for evaluating binary classification. Therefore, they are not used here.

4) How does our augmentation model perform in the problem space: In order to verify the effectiveness of the problem algorithm, we set up three sets of experiments. First, we want to verify the performance of problem space augmentation under a single dataset. We select four data subsets from the Kitsune dataset, as shown in TABLE XI. Trainb denotes benign data in the training set. Trainba denotes attacks in the balanced state. Trainia denotes attacks in the unbalanced state. Testb and Testm denote the benign and attacks in the test set, respectively. SSDPs refers to part of SSDP Flood data set. In order to make the data distribution reflect the variability, we also extract the smaller dataset SSDP-s. As shown in TABLE XII, our HeteAUG-P model searches the problem space well for solutions.

TABLE X  
PERFORMANCE OF MULTICLASSIFICATION OVERSAMPLING METHODS UNDER MULTIPLE METRICS. (TON DATA SET)

<table><tr><td>model</td><td>P_a</td><td>R_a</td><td>F1_a</td><td>ACC</td><td>G_a</td></tr><tr><td>multi-SMOTE [27]</td><td>0.637</td><td>0.647</td><td>0.611</td><td>0.647</td><td>0.632</td></tr><tr><td>multi-BS [29]</td><td>0.689</td><td>0.669</td><td>0.608</td><td>0.669</td><td>0.617</td></tr><tr><td>AC-J $\ominus$  [34]</td><td>0.352</td><td>0.510</td><td>0.380</td><td>0.510</td><td>0.260</td></tr><tr><td>AC-J</td><td>0.414</td><td>0.526</td><td>0.409</td><td>0.526</td><td>0.352</td></tr><tr><td>TMG-GAN [40]</td><td>0.463</td><td>0.529</td><td>0.420</td><td>0.529</td><td>0.372</td></tr><tr><td>EOS [56] *</td><td>0.650</td><td>0.624</td><td>0.552</td><td>0.624</td><td>0.533</td></tr><tr><td>ours $\ominus$ </td><td>0.726</td><td>0.701</td><td>0.638</td><td>0.701</td><td>0.646</td></tr><tr><td>ours</td><td>0.727</td><td>0.705</td><td>0.645</td><td>0.705</td><td>0.649</td></tr></table>

• multi-BS means multi-BorderlineSMOTE.  
• AC-J means ACGAN with JDA.  
• ours means HeteAUG-multi.

The second set of experiments follows. We experiment on the full complex Kitsune dataset. This experiment uses the configuration from the binary classification comparison experiment in feature space. As shown in TABLE XIII, HeteAUG-P-10 represents 10 iterations of the genetic algorithm. Our Hete-AUG-10 model improves 33.5% in accuracy over the imbalanced state. But the FPR has increased over the imbalanced state. It can be seen that data augmentation introduces some false positives for the model. As the number of iterations increases, the effect of augmentation becomes better and the FPR decreases. This shows that our HeteAUG-P model is also effective for augmentation in complex datasets but requires more iterations.

In the third set of experiments, we focus on whether the generated samples can be replayed and how long it takes. As shown in TABLE XIV, the replay time is very short. We introduce sample replay using TCP packets as an example. We introduce the Ether, IP, TCP, wrpcap function library from Scapy. The payload is randomly generated according to specific bytes. packet = Ether()/IP(src=”192.168.2.1”,dst=”192.168.2.7”)/TCP(sport=srcp, dport=8080, seq=seqnum, ack=acknum)/payload. This is the basic format. srcp, seqnum, acknum, and other parameters represent the source port, sequence number, and acknowledgment number. These can be logically numbered in a certain way. packet[Ether].src = ”18:db:f2:01:09:33” and packet[Ether].dst = ”ff:ff:ff:ff:ff:ff:ff” can be used to further determine the physical address. Other specific information, such as packet.time, can be similarly assigned. Other protocols are similarly encapsulated. Finally, it is converted to a pcap packet using wrpcap and then replayed using Tcprepaly.

In conclusion, our problem space augmentation algorithm HeteAUG-P is feasible and effective. If a more accurate solution is needed, increase the number of searches as well as make more threads parallel.

TABLE XI  
DISTRIBUTION OF A SINGLE DATASET IN PROBLEM SPACE ASSESSMENT. (SUBSET OF KITSUNE DATA SET)

<table><tr><td>Data set</td><td>Trainb</td><td>Trainba</td><td>Trainia</td><td>Testb</td><td>Testm</td></tr><tr><td>OS Scan</td><td>5013</td><td>3987</td><td>10</td><td>540</td><td>460</td></tr><tr><td>SSL Renegotiation</td><td>7306</td><td>1694</td><td>6</td><td>816</td><td>184</td></tr><tr><td>SYN DoS</td><td>7307</td><td>1693</td><td>10</td><td>801</td><td>199</td></tr><tr><td>SSDP Flood</td><td>5118</td><td>4882</td><td>10</td><td>600</td><td>400</td></tr><tr><td>SSDP-s</td><td>1840</td><td>1160</td><td>10</td><td>200</td><td>200</td></tr></table>

TABLE XII  
SINGLE DATASET AUGMENTATION PERFORMANCE IN PROBLEM SPACE.

<table><tr><td></td><td>Case</td><td>TPR</td><td>FPR</td><td>F1</td><td>ACC</td><td>AUC</td></tr><tr><td rowspan="3">OSscan</td><td>imbalance</td><td>0.000</td><td>0.000</td><td>0.000</td><td>0.555</td><td>0.500</td></tr><tr><td>balance</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td rowspan="3">SSL</td><td>imbalance</td><td>0.000</td><td>0.000</td><td>0.000</td><td>0.820</td><td>0.500</td></tr><tr><td>balance</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td rowspan="3">SYN</td><td>imbalance</td><td>0.971</td><td>0.000</td><td>0.985</td><td>0.994</td><td>0.985</td></tr><tr><td>balance</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td rowspan="3">SSDP</td><td>imbalance</td><td>0.000</td><td>0.000</td><td>0.000</td><td>0.607</td><td>0.500</td></tr><tr><td>balance</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td rowspan="3">SSDP-s</td><td>imbalance</td><td>0.000</td><td>0.000</td><td>0.000</td><td>0.497</td><td>0.500</td></tr><tr><td>balance</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr></table>

• SSL Renegotiation(SSL), SYN DoS(SYN), SSDP Flood(SSDP). • ours means HeteAUG-P.

TABLE XIII  
PERFORMANCE OF PROBLEM SPACE AUGMENTATION ALGORITHMS ON THECOMPLEX KITSUNE DATASET IN A BINARY CLASSIFICATION SCENARIO.

<table><tr><td>model</td><td>TPR</td><td>FPR</td><td>F1</td><td>ACC</td><td>AUC</td><td>@AR</td><td>@AP</td></tr><tr><td>imb</td><td>0.168</td><td>0.028</td><td>0.283</td><td>0.513</td><td>0.570</td><td>0.570</td><td>0.624</td></tr><tr><td>He1</td><td>0.802</td><td>0.317</td><td>0.786</td><td>0.751</td><td>0.742</td><td>0.742</td><td>0.731</td></tr><tr><td>He10</td><td>0.898</td><td>0.220</td><td>0.871</td><td>0.848</td><td>0.839</td><td>0.839</td><td>0.816</td></tr></table>

• Here, imb means imbalance;He10 means HeteAUG-P-10. •@AR means AUROC;@AP means AUPRC.

TABLE XIV  
ANALYZING THE REPLAY OF AUGMENTATION DATA FOR HETEAUG-P MODEL.

<table><tr><td>Data set</td><td>Number of samples augmented</td><td>replay time</td></tr><tr><td>OS Scan</td><td>1861</td><td> $\sim 0.2s$ </td></tr><tr><td>SSL Renegotiation</td><td>76</td><td> $\sim 0.2s$ </td></tr><tr><td>SYN DoS</td><td>451</td><td> $\sim 0.2s$ </td></tr><tr><td>SSDP Flood</td><td>3412</td><td> $\sim 0.2s$ </td></tr><tr><td>SSDP-s</td><td>1658</td><td> $\sim 0.2s$ </td></tr></table>

5) Is the component selection of our augmentation model effective: In this section, we focus on verifying whether the components of our augmentation model are effective. We conduct experiments in both binary classification and multiclassification. To more clearly demonstrate the advantages of a suitable complementary structure, TABLE XV and TABLE XVI show ablation experiments as well as extended experiments. Extended experiments reflect design considerations. The first is the binary classification augmentation. As shown in TABLE XV, we present a comparison of 15 cases. Here, drop outlier indicates that HBOS is used to filter points outside the distribution. The first five rows we analyzed earlier. The sixth row is the classical DCGAN. It is clear that the learned distribution is missing. The seventh through ninth rows are a combination of our DCGAN with threshold plus several other SMOTEs. The advantages of these combinations are not obvious. Rows ten and eleven are based on our model using the HBOS algorithm to remove outliers from the augmentation sample distribution. These lose some distributions compared to our augmentation model. The twelfth and thirteenth rows show that the combination of WCGAN and SMOTE is very close to our detection performance. The fourteenth line is SMOTE+Linear GAN, whose detection accuracy is 0.784. This shows that Linear GAN is weak in providing the diversity needed for augmentation. The above proves the rationality of the component design of our binary augmentation model. Meanwhile, it can be observed that multiple SMOTE and GAN combinations can achieve good performance. For the specific selection of which combination, it is recommended to comprehensively consider the following factors: dataset characteristics (e.g., hard-to-detect attacks), feature engineering methods (e.g., time-decay), and validation set performance (e.g., accuracy after augmentation).

The second is multi-classification augmentation. As shown in TABLE XVI, we present a comparison of 13 cases. ⊕ indicates that the corresponding ACGAN training uses an excess of benign data. The first five rows we analyzed before. The sixth and seventh rows illustrate that edge-distributed GAN and multi-BorderlineSMOTE do not improve the results of a single optimum. The eighth through tenth rows illustrate that adding an appropriate amount of benign training to ACGAN can improve detection. In particular, an excess of benign has a greater impact than not using benign. Rows eleven and twelve illustrate that choosing multi-BorderlineSMOTE is better than multi-SMOTE. Rows twelve and thirteen illustrate that our model requires a moderate amount of benign data to be added for training. The above proves the rationality of the component design of our multiclassification augmentation model.

TABLE XV

ABLATION EXPERIMENTS (INCLUDE EXTENDED EXPERIMENTS) WITH THE BINARY CLASSIFICATION AUGMENTATION MODEL HETEAUG-BI. (TON DATA SET)

<table><tr><td></td><td>Case</td><td>ACC</td></tr><tr><td>1)</td><td>imbalance</td><td>0.512</td></tr><tr><td>2)</td><td>balance</td><td>0.996</td></tr><tr><td>3)</td><td>SMOTE</td><td>0.738</td></tr><tr><td>4)</td><td>ADASYN</td><td>0.744</td></tr><tr><td>5)</td><td>BorderlineSMOTE</td><td>0.807</td></tr><tr><td>6)</td><td>DCGAN</td><td>0.667</td></tr><tr><td>7)</td><td>DCGAN with threshold +BorderlineSMOTE</td><td>0.750</td></tr><tr><td>8)</td><td>DCGAN with threshold+ADASYN</td><td>0.767</td></tr><tr><td>9)</td><td>DCGAN with threshold+Three SMOTEs</td><td>0.808</td></tr><tr><td>10)</td><td>DCGAN with threshold+SMOTE+drop outlier(0.01)</td><td>0.770</td></tr><tr><td>11)</td><td>DCGAN with threshold+SMOTE+drop outlier(0.1)</td><td>0.781</td></tr><tr><td>12)</td><td>WCGAN+SMOTE</td><td>0.816</td></tr><tr><td>13)</td><td>WCGAN</td><td>0.576</td></tr><tr><td>14)</td><td>Linear GAN+SMOTE</td><td>0.784</td></tr><tr><td>15)</td><td>HeteAUG-bi</td><td>0.835</td></tr></table>

•Three SMOTEs means SMOTE+BorderlineSMOTE+ADASYN. •HBOS [60] means Histogram-based Outlier Score.

TABLE XVI  
ABLATION EXPERIMENTS (INCLUDE EXTENDED EXPERIMENTS) WITH THE MULTICLASSIFICATION AUGMENTATION MODEL HETEAUG-MULTI. (TON DATA SET)

<table><tr><td></td><td>Case</td><td>ACC</td></tr><tr><td>1)</td><td>imbalance</td><td>0.423</td></tr><tr><td>2)</td><td>balance</td><td>0.930</td></tr><tr><td>3)</td><td>multi-SMOTE</td><td>0.647</td></tr><tr><td>4)</td><td>multi-ADASYN</td><td>-</td></tr><tr><td>5)</td><td>multi-BorderlineSMOTE</td><td>0.669</td></tr><tr><td>6)</td><td>ACGAN with MDA</td><td>0.495</td></tr><tr><td>7)</td><td>ACGAN with MDA+multi-SMOTE</td><td>0.606</td></tr><tr><td>8)</td><td>ACGAN $\ominus$  with JDA</td><td>0.510</td></tr><tr><td>9)</td><td>ACGAN with JDA</td><td>0.526</td></tr><tr><td>10)</td><td>ACGAN $\oplus$  with JDA</td><td>0.482</td></tr><tr><td>11)</td><td>ACGAN $\ominus$  with JDA+multi-SMOTE</td><td>0.677</td></tr><tr><td>12)</td><td>ACGAN $\ominus$  with JDA+multi-BorderlineSMOTE</td><td>0.701</td></tr><tr><td>13)</td><td>HeteAUG-multi</td><td>0.705</td></tr></table>

•Not any neigbours belong to the majority class. Thus,  
multi-ADASYN is not suited for this specific data set.

## F. Model deployment and runtime efficiency.

1) Running efficiency of augmentation algorithms: We use a server with AMD EPYC 7402 24-Core Processor and 256G of RAM as the device. The type of GPU we use is GTX 3090. We test the performance of each of the three models of the framework. HeteAUG-bi and HeteAUG-multi use the TON dataset. HeteAUG-P uses the SSDP dataset. We record the maximum values of CPU and memory usage. For example, SMOTE takes only 0.418s to generate 30,000 samples. As can be seen from TABLE XVII, our model requires a lower percentage of memory and a slightly higher CPU, which is acceptable. Since our augmentation algorithm is offline, we are not doing performance comparisons with other algorithms. In particular, the last row of the table, the SSDP search problem, uses a single thread, which is more time-consuming. Because each sample is not affected by the search, we can divide the search into multiple simultaneous searches. In this way, the time will also be greatly reduced. We measured the GPU memory usage of both HeteAUG-bi and HeteAUG-multi models (using SMOTE and BorderlineSMOTE from the imbalanced-learn codebase without GPU support) during training and generation phases using the nvidia-smi tool (batch size = 1). The results are shown in TABLE XVIII. The above results represent memory usage when processing a single sample, with both models requiring less than 0.5 GB of GPU memory. In practical applications, users can flexibly adjust the batch size according to their GPU capabilities. The algorithm complexity of HeteAUG can be found in the Appendix.

2) How our models are deployed: As shown in Fig. 7, in the case of insufficient data, we use augmentation data to train the model and deploy it after feature extraction. When there is sufficient data, the model is trained using real samples and deployed for detection.

![](images/644bb898a0563f1a189411c7795f3f82bf2c1af5488e2bb1aae88bdad1b7bdf7.jpg)  
Fig. 7. Deployment diagram of our HeteAUG model.

3) How our data is shared: Leveraging generated data to facilitate data sharing is a significant and continuously evolving research direction [24], [26], [61]. In data sharing, if we give the feature extracted files directly, it is difficult for others to analyze and model this data. We can provide a small number of feature files and augmented problem space traffic in the form of sharing. In this way, the user of the data can’t deduce the real attack situation of the traffic data in reverse. But, it can be good for modeling work. Further, augmentation modeling can also reduce the effort of data set collection. For example, a user of the augmentation model conducts attack and defense experiments on his network and acquires a small number of attacks. Problem augmentation algorithms can be used to generate a large number of similar forms of attacks and satisfy different traffic field characteristics.

4) Does the model need to be retrained after using the augmentation method?: Since the model trained by augmentation of samples always has errors compared to the model trained using real data, try to retrain the model as much as possible when enough data is collected for the attack class.

## VI. DISCUSSIONS

In this section, we first discuss issues related to the model. Then, we discuss the limitations and future work.

## A. Discussion of Model-Related Issues

Q1: Should the augmentation model be in problem space or feature space? The augmentation method is ultimately reflected in the feature space. So, no matter which level, the augmentation model is fine as long as it is valid in the feature space. We discuss the problem space in order to address the simultaneous data sharing under imbalance. Then, the samples in the problem space can somewhat explain the samples generated in the feature space, which can lead to a better understanding of the new attacks. Data sharing with IP address-based anonymization has shortcomings, which not only does not solve the imbalance problem, but also fails to share more varied samples.

TABLE XVII  
PERFORMANCE REQUIREMENTS FOR EACH AUGMENTATION MODEL.

<table><tr><td>model</td><td>Component</td><td>Action</td><td>Memory</td><td>Memory (%)</td><td>CPU (%)</td><td>Time(epoch)</td></tr><tr><td rowspan="3">HeteAUG-bi</td><td>SMOTE</td><td>Generate 30,000 samples</td><td>1,280.2MB</td><td>0.5%</td><td>8.3%</td><td>0.418s(-)</td></tr><tr><td>DCGAN-train</td><td>Train 70 attack samples</td><td>19,200.6MB</td><td>7.5%</td><td>10.4%</td><td>2.087s(2)</td></tr><tr><td>DCGAN-test</td><td>Traverse 31742 samples</td><td>5,120.3MB</td><td>2.0%</td><td>1.1%</td><td>93.572s(-)</td></tr><tr><td rowspan="3">HeteAUG-multi</td><td>BordlineSMOTE</td><td>Generate 48000 samples</td><td>1,280.1MB</td><td>0.5%</td><td>13.1%</td><td>0.703s(-)</td></tr><tr><td>ACGAN-train</td><td>Train 13070 attack samples</td><td>34,560.7MB</td><td>13.5%</td><td>6.1%</td><td>562.108s(2)</td></tr><tr><td>ACGAN-test</td><td>Generate 70,000 samples</td><td>5,632.5MB</td><td>2.2%</td><td>1.0%</td><td>7.612s(-)</td></tr><tr><td>HeteAUG-P</td><td>Problem space search</td><td>(iter=1, 1658 samples)</td><td>1,536.3MB</td><td>0.6%</td><td>3.2%</td><td>7866s(-)</td></tr></table>

• HeteAUG-bi and HeteAUG-multi use TON dataset. HeteAUG-P uses SSDP dataset.

TABLE XVIII  
GPU MEMORY USAGE MEASUREMENTS (TON DATA SET, BATCH SIZE = 1)

<table><tr><td>Model</td><td>Training Phase</td><td>Generation Phase</td></tr><tr><td>DCGAN</td><td>405 MiB/ 24576 MiB</td><td>349 MiB/ 24576 MiB</td></tr><tr><td>ACGAN</td><td>451 MiB/ 24576 MiB</td><td>361 MiB/ 24576 MiB</td></tr></table>

Q2: How does our augmentation model perform in the case of large data sets?

We validate the performance of our augmentation algorithm on the full SSDP dataset. As shown in TABLE XIX, our algorithm achieves good augmentation results in the case of large data sets.

TABLE XIX  
VALIDATING THE PERFORMANCE OF OUR MODEL ON LARGE FULL SSDP DATA SET.

<table><tr><td>model</td><td>TPR</td><td>FPR</td><td>F1</td><td>ACC</td><td>AUC</td></tr><tr><td>imbalance</td><td>0.000</td><td>0.000</td><td>0.000</td><td>0.009</td><td>0.500</td></tr><tr><td>ours</td><td>1.000</td><td>0.000</td><td>1.000</td><td>1.000</td><td>1.000</td></tr><tr><td colspan="6">Total data set: 4077,266; benign 2,637,662, attack 1,439,604Real training set: benign 2634,058, attack 1,000Real testing set: benign 3,604, attack 404,123</td></tr></table>

• Here, ours means HeteAUG-bi.

Q3: Comparison of our algorithm with top 3 algorithms in CPU-only environments.

For a fair comparison, we evaluate the Top3 algorithm in a pure CPU environment and observe that the results match those obtained in the GPU environment, as shown in TABLE XX. This indicates that the effectiveness of data augmentation is independent of GPU usage. The GPU merely accelerates model training. Furthermore, we conduct a cost-sensitive experiment using the formula Cost = 10\*FN + 1\*FP. Notably, our algorithm achieves the lowest Cost while also maintaining the lowest FPR.

## B. Limitation and Future Work

For space reasons, some of our model-related and deploymentrelated issues were not included in the design framework. This leaves our framework extensible.

TABLE XX  
COMPARISON OF TOP-3 ALGORITHMS IN CPU-ONLY ENVIRONMENT. (TON DATA SET)

<table><tr><td>Model</td><td>ACC</td><td>Cost</td><td>FPR</td></tr><tr><td>ADASYN [28]</td><td>0.765</td><td>84235</td><td>0.158</td></tr><tr><td>B-S [29]</td><td>0.781</td><td>91155</td><td>0.077</td></tr><tr><td>HeAUG-bi-CPU</td><td>0.835</td><td>74800</td><td>0.022</td></tr><tr><td>HeAUG-bi-GPU*</td><td>0.835</td><td>74800</td><td>0.022</td></tr></table>

• HeAUG-bi-GPU\* results are shown for reference.

To begin with, we discuss model-related issues. The first issue is how to better cope with the open world problem. We can further optimize our augmentation framework in conjunction with openset domain adaptation algorithms [62]. The second issue is how to better explain the solution to the imbalance problem. We can analyze it by combining some existing explainable methods. These interpretation methods can be the basic global interpretable SHAP [64] and local interpretable LIME [63], or the latest interpretation model x-NIDS based [65].

After that, we discuss the potential threats in model deployment: First, if a certain type of attack cannot be effectively represented by existing feature extraction methods, then augmentation may not be effective; Second, noise is prone to occur during the real labeling process, and using noisy samples for augmentation will introduce errors. To address these two limitations, we can combine feature engineering methods and noise identification algorithms to assist in model deployment.

## VII. CONCLUSION

Network anomaly detection is an important network management task. Machine learning/deep learning based IDSs face the impact of imbalanced training data. Oversampling as a promising technique to address imbalance also suffers from the following two problems. The first is the inability to learn a more complete speculative distribution. The second is that augmentation data cannot correspond to the problem space. For these reasons, we propose the HeteAUG model. On feature space augmentation, we combine interpolation-based and convolutional GAN-based augmentation results in a heterogeneous form. For problem space augmentation, a heuristic search algorithm with constraints is used on the basis of effective feature space augmentation samples. Experiments show that our augmentation model outperforms other SOTA models and can be well used in practical grounded scenarios. Specifically, taking the complex Kitsune dataset as an example and using accuracy after augmentation as an evaluation metric, in binary augmentation, we outperform the SOTA algorithm by at least 6.1%. In multiclassification augmentation, we outperform the SOTA algorithm by at most 12.1%. In the augmentation of the binary classification problem space, we compare the accuracy of the classifiers before and after augmentation, and we outperform the imbalanced state by 33.5%. Our future work focuses on automated combination optimization of augmentation strategies. Additionally, we will attempt to extend the application of the HeteAUG augmentation model to other domains.

## ACKNOWLEDGMENT

The authors would like to express their gratitude to the anonymous reviewers whose constructive comments have greatly helped to improve this manuscript. This work is supported by the National Key Research and Development Program of China under Grant No. 2022YFB3102902.

## REFERENCES

[1] D. E. Denning, “An Intrusion-Detection Model,” IEEE Transactions on Software Engineering, vol. SE-13, no. 2, pp. 222-232, Feb. 1987.

[2] SNORT. Snort 2.9.7.6. [Online]. Available:https://www.snort.org/, 2019.

[3] OISF. Suricata 4.0.4. [Online]. Available: https://suricataids.org/about/, 2018.

[4] P. Mishra, V. Varadharajan, U. Tupakula and E. S. Pilli, “A Detailed Investigation and Analysis of Using Machine Learning Techniques for Intrusion Detection,” IEEE Communications Surveys & Tutorials, vol. 21, no. 1, pp. 686-728, Firstquarter 2019.

[5] Ying Zhong, Wenqi Chen, Zhiliang Wang, et. al., “HELAD: A novel network anomaly detection model based on heterogeneous ensemble learning,” Computer Networks, Volume 169, pp. 107049, 2020.

[6] Alec F. Diallo, Paul Patras. “Adaptive Clustering-based Malicious Traffic Classification at the Network Edge,” INFOCOM, pp. 1-10, 2021.

[7] Alec F. Diallo, Paul Patras. “Cluster and Conquer: Malicious Traffic Classification at the Edge,” IEEE Trans. Netw. Serv. Manag., vol. 21, no. 3, pp. 2700-2714, 2024.

[8] Cristiano Antonio de Souza et al. “Hybrid approach to intrusion detection in fog-based IoT environments,” Comput. Networks, 2020.

[9] Zhong et al., “RFG-HELAD: A Robust Fine-Grained Network Traffic Anomaly Detection Model Based on Heterogeneous Ensemble Learning,” TIFS, 2024.

[10] Swagatam Das, Sankha Subhra Mullick, Ivan Zelinka. “On Supervised Class-Imbalanced Learning: An Updated Perspective and Some Key Challenges,” IEEE Trans. Artif. Intell., vol. 3, no. 6, pp. 973-993, 2022.

[11] Eoin Brophy, Zhengwei Wang, Qi She, Tomas Ward. “Generative Adversarial´ Networks in Time Series: A Systematic Literature Review,” ACM Comput. Surv., vol. 55, no. 10, pp. 1-31, 2023.

[12] Mohammadreza et al. “Unified Survey on Anomaly, Novelty, Open-Set, and Out of-Distribution Detection: Solutions and Future Challenges,” Trans. Mach Learn. Res., 2022.

[13] Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron C. Courville, Yoshua Bengio. “Generative Adversarial Nets,” NIPS, pp. 2672-2680, 2014.

[14] Kumari, Nupur et al. “Ensembling Off-the-shelf Models for GAN Training,” CVPR, pp. 10641-10652, 2022.

[15] Sommer R , Paxson V. “Outside the Closed World: On Using Machine Learning for Network Intrusion Detection,” IEEE Symposium on Security and Privacy, 2010.

[16] Fabio Pierazzi, Feargus Pendlebury, Jacopo Cortellazzi, Lorenzo Cavallaro, “Intriguing Properties of Adversarial ML Attacks in the Problem Space”, in IEEE Symposium on Security and Privacy, pp. 1332-1349, 2020.

[17] Dongqi Han et al., “Evaluating and Improving Adversarial Robustness of Machine Learning-Based Network Intrusion Detectors,” JSAC, 2021.

[18] Aayush Bansal, Rewa Sharma, Mamta Kathuria, “A Systematic Review on Data Scarcity Problem in Deep Learning: Solution and Applications,” ACM Comput. Surv., vol. 54, no. 208, pp.1-29, 2022.

[19] Najmeh Abedzadeh and Matthew Jacobs, “A Reinforcement Learning Framework with Oversampling and Undersampling Algorithms for Intrusion Detection System,” Applied Sciences, 2023.

[20] Chang Liu, Ruslan Antypenko, Iryna Sushko, Oksana Zakharchenko, “ Intrusion Detection System After Data Augmentation Schemes Based on the VAE and CVAE,” IEEE Trans. Reliab., vol. 71, no. 2, pp. 1000-1010, 2022.

[21] Neha Gupta, Vinita Jindal, Punam Bedi, “ CSE-IDS: Using cost-sensitive deep learning and ensemble algorithms to handle class imbalance in networkbased intrusion detection systems,” Comput. Secur., vol. 112, pp. 102499, 2022.

[22] Akbar Telikani, Amir H. Gandomi, “ Cost-sensitive stacked auto-encoders for intrusion detection in the Internet of Things,” Internet Things, vol. 14, pp. 100122, 2021.

[23] Ying Zhou, Thomas A. Mazzuchi, Shahram Sarkani, “ M-AdaBoost-A based ensemble system for network intrusion detection,” Expert Syst. Appl., vol. 162, pp. 113864, 2020.

[24] Shengzhe Xu and Manish Marwah and Martin F. Arlitt and Naren Ramakrishnan, “STAN: Synthetic Network Traffic Generation with Generative Neural Models“, in Deployable Machine Learning for Security Defense, 2020.

[25] Renjie Xie, Jiahao Cao, Enhuan Dong, Mingwei Xu, Kun Sun, Qi Li, Licheng Shen, Menghao Zhang, “Rosetta: Enabling Robust TLS Encrypted Traffic Classification in Diverse Network Environments with TCP-Aware Traffic Augmentation”, in USENIX Security Symposium, pp. 625-642, 2023.

[26] Yucheng Yin, Zinan Lin, Minhao Jin, Giulia Fanti, Vyas Sekar, “Practical GAN-based synthetic IP header trace generation using NetShare“, in SIG-COMM, pp. 458-472, 2022.

[27] Hongpo Zhang, Lulu Huang, Chase Q. Wu, Zhanbo Li, “An effective convolutional neural network based on SMOTE and Gaussian mixture model for intrusion detection in imbalanced dataset“, in Comput. Networks, vl. 177. no. 107315, 2020.

[28] Jingmei Liu, Yuanbo Gao, Fengjie Hu, “A fast network intrusion detection system using adaptive synthetic oversampling and LightGBM“, in Comput. Secur., vol. 106, no. 102289, 2021.

[29] Ying Zhang, Qiang Liu, “On IoT intrusion detection based on data augmentation for enhancing learning on unbalanced samples“, in Future Gener. Comput. Syst., vol. 133, pp. 213-227, 2022.

[30] Qi Dai, Long-hui Wang, Kai-long Xu, Tony Du, Li-fang Chen, “Classoverlap detection based on heterogeneous clustering ensemble for multi-class imbalance problem“, in Expert Syst. Appl., vol. 255, 2024.

[31] Md Hasan Shahriar, Nur Imtiazul Haque, Mohammad Ashiqur Rahman, Miguel Alonso Jr., “G-IDS: Generative Adversarial Networks Assisted Intrusion Detection System“, in COMPSAC, pp. 376-385, 2020.

[32] Steve T. K. Jan, Qingying Hao, Tianrui Hu, Jiameng Pu, Sonal Oswal, Gang Wang, Bimal Viswanath, “Throwing Darts in the Dark? Detecting Bots with Limited Data using Neural Data Augmentation“, in S&P, pp. 1190-1206, 2020.

[33] Vikash Kumar, Ditipriya Sinha, “Synthetic attack data generation model applying generative adversarial network for intrusion detection“, in Comput. Secur., pp. 125, vol. 103054, 2023.

[34] Hongwei Ding, Leiyang Chen, Liang Dong, Zhongwang Fu, Xiaohui Cui, “Imbalanced data classification: A KNN and generative adversarial networksbased hybrid approach for intrusion detection“, in Future Gener. Comput. Syst. vol. 131, pp. 240-254, 2022.

[35] Lixiang Yuan, Siyang Yu, ZhiBang Yang, Mingxing Duan, Kenli Li, “A data balancing approach based on generative adversarial network“, in Future Gener. Comput. Syst., vol. 141, pp. 768-776, 2023.

[36] Giuseppina Andresini, Annalisa Appice, Luca De Rose, Donato Malerba, “GAN augmentation to deal with imbalance in imaging-based intrusion detection“, in Future Gener. Comput. Syst., vol. 123, pp. 108-127, 2021.

[37] Zecheng Li, Shengyuan Chen, Hongshu Dai, Dunyuan Xu, Cheng-Kang Chu, Bin Xiao, “Abnormal Traffic Detection: Traffic Feature Extraction and DAE-GAN With Efficient Data Augmentation“, in IEEE Trans. Reliab. vol. 72, no. 2, pp. 498-510, 2023.

[38] Radhika Chapaneri, Seema Shah, “Enhanced detection of imbalanced malicious network traffic with regularized Generative Adversarial Networks“, in J. Netw. Comput. Appl., vol. 202, no. 103368, 2022.

[39] Pedro Horchulhack, Eduardo K. Viegas, Altair O. Santin, Jhonatan Geremias, “Intrusion Detection Model Updates Through GAN Data Augmentation and Transfer Learning“, in GLOBECOM, pp. 2668-2673, 2022.

[40] Hongwei Ding, Yu Sun, Nana Huang, Zhidong Shen, Xiaohui Cui, “TMG-GAN: Generative Adversarial Networks-Based Imbalanced Learning for Network Intrusion Detection”, in IEEE Trans. Inf. Forensics Secur., vol. 19, pp. 1156-1167, 2024.

[41] Yuqi Qing, Qilei Yin, Xinhao Deng, Yihao Chen, Zhuotao Liu, Kun Sun, Ke Xu, Jia Zhang, Qi Li, “Low-Quality Training Data Only? A Robust Framework for Detecting Encrypted Malicious Network Traffic”, in NDSS, 2024.

[42] Zhi-Hua Zhou, “Machine Learning,” Springer, pp. 1-459, 2021.

[43] Guillaume et al., “Imbalanced-learn: A Python Toolbox to Tackle the Curse of Imbalanced Datasets in Machine Learning,” Journal of Machine Learning Research, pp. 1-5, 2017.

[44] Nitesh V. Chawla, Kevin W. Bowyer, Lawrence O. Hall, W. Philip Kegelmeyer, “SMOTE: Synthetic Minority Over-sampling Technique,” J. Artif. Intell. Res., vol. 16, pp. 321-357, 2002.

[45] Alec Radford, Luke Metz, Soumith Chintala, “Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks,” ICLR, 2016.

[46] Hui Han, Wenyuan Wang, Binghuan Mao, “Borderline-SMOTE: A New Over-Sampling Method in Imbalanced Data Sets Learning,” ICIC, vol. 1, pp. 878-887, 2005.

[47] Augustus Odena, Christopher Olah, Jonathon Shlens, “Conditional Image Synthesis with Auxiliary Classifier GANs,” ICML, pp. 2642-2651, 2017.

[48] B. Venkatesh and J. Anuradha. “A review of Feature Selection and its methods,” Cybern. Inf. Technol., vol. 19, no. 1, pp. 3-26, 2019.

[49] D. Chandramohan, Ankur Dumka, Dhilipkumar V., Loganathan Jayakumar. “Data dissemination for green-VANETs communication: an opportunistic optimization approach,” Int. J. Pervasive Comput. Commun., vol. 17, no. 1, pp. 89-108, 2021.

[50] Nour Moustafa, “A new distributed architecture for evaluating AI-based security systems at the edge: Network TON IoT datasets,” Sustainable Cities and Society, vol. 72, 2021.

[51] Mirsky Y, Doitshman T, Elovici Y, et al., “Kitsune: An Ensemble of Autoencoders for Online Network Intrusion Detection,” NDSS, 2018.

[52] Muataz Salam Al Daweri, Salwani Abdullah, Khairul Akram Zainol Ariffin, “An adaptive method and a new dataset, UKM-IDS20, for the network intrusion detection system” in Comput. Commun., pp. 57-76, 2021.

[53] Han Kyu Lee, Jiyoon Lee, Seoung Bum Kim, “Boundary-Focused Generative Adversarial Networks for Imbalanced and Multimodal Time Series“, in IEEE Trans. Knowl. Data Eng., vol. 34, no. 9, pp. 4102-4118, 2022.

[54] Patience Chew Yee Cheah and Yue Yang and Boon-Giin Lee, “Enhancing Financial Fraud Detection through Addressing Class Imbalance Using Hybrid SMOTE-GAN Techniques”, in International Journal of Financial Studies, 2023.

[55] Anuraganand Sharma and Prabhat Kumar Singh and Rohitash Chandra, “SMOTified-GAN for Class Imbalanced Pattern Classification Problems”, in IEEE Access, vol. 10, pp. 30655-30665, 2021.

[56] Damien A. Dablain, Colin Bellinger, Bartosz Krawczyk, Nitesh V. Chawla, “Efficient Augmentation for Imbalanced Deep Learning“, in ICDE, pp. 1433- 1446, 2023.

[57] Omar Elghalhoud, Kshirasagar Naik, Marzia Zaman, Ricardo Manzano S., “Data Balancing and CNN based Network Intrusion Detection System“, in WCNC, pp. 1-6, 2023.

[58] Moshe Kravchik, Asaf Shabtai, “Efficient Cyber Attack Detection in Industrial Control Systems Using Lightweight Neural Networks and PCA”, in IEEE Trans. Dependable Secur. Comput, vol. 19, no. 4, pp. 2179-2197, 2022.

[59] Cristiano Antonio de Souza et al., “Hybrid approach to intrusion detection in fog-based IoT environments”, Comput. Networks, 2020.

[60] Goldstein, M. and Dengel, A., “Histogram-based outlier score (hbos):A fast unsupervised anomaly detection algorithm”, InKI, pp.59-63, 2012.

[61] Xi Jiang et. al, “NetDiffusion: Network Data Augmentation Through Protocol-Constrained Traffic Generation” in Proc. ACM Meas. Anal. Comput. Syst., no. 8, vol. 1, pp. 1-32, 2024.

[62] Jinghan Ru, Jun Tian, Chengwei Xiao, Jingjing Li, Heng Tao Shen, “Imbalanced Open Set Domain Adaptation via Moving-Threshold Estimation and Gradual Alignment“, in IEEE Trans. Multim., vol. 26, pp. 2504-2514, 2024.

[63] Marco Tulio Ribeiro, Sameer Singh, Carlos Guestrin, “Why Should I Trust´ You?: Explaining the Predictions of Any Classifie“, in KDD, pp. 1135-1144, 2016.

[64] Scott M. Lundberg, Su-In Lee, “A Unified Approach to Interpreting Model Predictions“, in NIPS, pp. 4765-4774, 2017.

[65] Feng Wei, Hongda Li, Ziming Zhao, Hongxin Hu, “xNIDS: Explaining Deep Learning-based Network Intrusion Detection Systems for Active Intrusion Responses“, in USENIX Security Symposium, pp. 4337-4354, 2023.

[66] Jinhee Kim, Taesung Kim, Jaegul Choo,“EPIC: Effective Prompting for Imbalanced-Class Data Synthesis in Tabular Data Classification via Large Language Models“, in NeurIPS, 2024.

[67] Leyao Wang, Yu Wang, Bo Ni, Yuying Zhao, Tyler Derr, “Large Language Model-based Augmentation for Imbalanced Node Classification on Text-Attributed Graphs“, in CoRR abs/2410.16882, 2024.

[68] Ryumei Nakada, Yichen Xu, Lexin Li, Linjun Zhang,“Synthetic Oversampling: Theory and A Practical Approach Using LLMs to Address Data Imbalance“, in CoRR abs/2406.03628, 2024.

[69] Dang Nguyen et al.,“Large Language Models for Imbalanced Classification: Diversity makes the difference“, in CoRR abs/2510.09783, 2025.

[70] Tokimasa Isomuraet al.,“LLMOverTab: Tabular data augmentation with language model-driven oversampling“, in Expert Syst. Appl., vol. 264, no. 125852, 2025.

[71] Mousavi, Vahid, et al.,“Transformer-based time-series GAN for data augmentation in bridge digital twins“, in Automation in Construction, vol. 175, no. 106208, 2025.

[72] Xiaomin Li, Anne Hee Hiong Ngu, Vangelis Metsis,“TTS-CGAN: A Transformer Time-Series Conditional GAN for Biosignal Data Augmentation“, in CoRR abs/2206.13676, 2022.

[73] Emmanuel Yangue, Ethan O’Connor, Chenang Liu,“Addressing Class Imbalance in Diabetic Retinopathy Detection: An Enhanced Diffusion-Resampling Data Augmentation Approach“, in CASE, pp. 1323-1329, 2025.

[74] Fan Zhang, Quan Yuan, Xinhong Zhang,“Mamba-DDPM-BSA: Diffusion model based boundary sampling algorithm for imbalanced classification“, in Expert Syst. Appl., vol. 274, no. 126926, 2025.

[75] Raj Kumar, Yong-Woon Kim, Yung-Cheol Byun,“Hybrid Framework Combining Diffusion-Based Image Augmentation and Feature Level SMOTE for Addressing Extreme Class Imbalance“, in IEEE Access, vol. 13, pp. 154623- 154646, 2025.

[76] Chaoling Wang, Jiang Wu, Liang Wang,“LRT-DDPM: A Diffusion Model-Based Approach for Network Traffic Data Generation in Intrusion Detection“, in IEEE Access, vol. 13, pp. 149054-149070, 2025.

[77] Peng Wang et al.,“DIFT: A Diffusion-Transformer for Intrusion Detection of IoT with Imbalanced Learning“, in J. Netw. Syst. Manag., vol. 33, no. 3, 2025.

![](images/a3fd29c249f5d5d820cd9069e99e318ba191b1920aa14b18448ab13a47c43e8b.jpg)

Ying Zhong received master degree at the College of Information Science and Engineering, Hunan University, China. Then, He received Ph.D. degree at the Institute for Network Sciences and Cyberspace at Tsinghua University. He is currently working in the Zhongguancun Laboratory, Beijing, China. His research interests include the machine learning, big data, network security, data analysis and their parallel implementation.

![](images/1ff77a74b3c903b4c16fef883c47e4841495768c762ec5a1f28fd22111b25139.jpg)

Zhiliang Wang received the B.E., M.E. and Ph.D. degrees in computer science from Tsinghua University, China in 2001, 2003 and 2006 respectively. Currently he is an Associate Professor in the Institute for Network Sciences and Cyberspace at Tsinghua University. His research interests include formal methods and protocol testing, next generation Internet, network measurement.

![](images/757e546df9a54b8c47b9fa816f02b0f6328de6e9e371b3ffa75b0f1b64818573.jpg)

Xingang Shi received his B.S. degree from Tsinghua University and his Ph.D. degree from The Chinese University of Hong Kong. He is now working at the Institute for Network Sciences and Cyberspace at Tsinghua University. His research interests include network measurement and routing protocols.

![](images/69a58e761031c5c017ef24ad025bc4b409a8557e7dfaeedec247d242a82c312a.jpg)

Jiahai Yang received his M.S. and Ph.D. degrees in computer science from Tsinghua University, Beijing, P.R.China, in 1992 and 2003, respectively. He is now a professor of Tsinghua University. Jiahai¡¯s research interests include Internet architecture and its protocols, IP routing technology, network measurement, network management, cloud computing, big data, etc.

![](images/9502690db2d59687143d1119dbc14b8e5eb6b6218adf6e34f5106b051bba5d2c.jpg)

Keqin Li is a SUNY Distinguished Professor of computer science with the State University of New York. He is also a Distinguished Professor at Hunan University, China. His current research interests include cloud computing, computer networking, machine learning, intelligent and soft computing. He has published over 1280 journal articles, book chapters, and refereed conference papers, and has received several best paper awards. He is an IEEE Fellow.
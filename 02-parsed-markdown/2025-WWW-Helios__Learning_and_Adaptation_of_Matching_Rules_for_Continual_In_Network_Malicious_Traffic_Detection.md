# Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection

Zhenning Shi Tsinghua University Shenzhen, China Peng Cheng Laboratory Shenzhen, China shizn23@mails.tsinghua.edu.cn

Guorui Xie Peng Cheng Laboratory Shenzhen, China xiegr@pcl.ac.cn

Dan Zhao<sup>∗</sup> Peng Cheng Laboratory Shenzhen, China zhaod01@pcl.ac.cn

Qing Li Peng Cheng Laboratory Shenzhen, China liq@pcl.ac.cn

Yijia Zhu Xidian University School of Artificial Intelligence Xian, China 22009200697@stu.xidian.edu.cn

Yong Jiang<sup>∗</sup> Tsinghua University Shenzhen, China Peng Cheng Laboratory Shenzhen, China jiangy@sz.tsinghua.edu.cn

## Abstract

Network Intrusion Detection Systems (NIDS) are critical for web security by identifying and blocking malicious trafic. In-network NIDS leverage programmable switches for high-speed trafic pro cessing. However, they are unable to reconcile the fine-grained classification of known classes and the identification of unseen attacks. Moreover, they lack support for incremental updates. In this paper, we propose Helios, an in-network malicious trafic detection system, for continual adaptation in attack-incremental scenarios. First, we design a novel Supervised Mixture Prototypical Learning (SMPL) method combined with clustering initialization to learn prototypes that encapsulate the knowledge, based on the weighted infinity norm distance. SMPL enables known class classification and unseen attack identification through similarity comparison between prototypes and samples. Then, we design boundary calibration and overlap refinement to transform learned prototypes into priority guided matching rules, ensuring precise and eficient in-network deployment. Additionally, Helios supports incremental prototype learning and rule updates, achieving low-cost hardware reconfigu ration. We implement Helios on a Tofino switch and evaluation on three datasets shows that Helios achieves superior performance in classifying known classes (92%+ in ACC and F1) as well as identi fying unseen attacks (62% - 98% in TPR). Helios has also reduced resource consumption and reconfiguration time, demonstrating its scalability and eficiency for real-world deployment.

## CCS Concepts

• Security and privacy → Network security.

<sup>∗</sup>Dan Zhao and Yong Jiang are the corresponding authors.

## Keywords

Malicious trafic detection, Programmable switches, Prototypical learning

ACM Reference Format: Zhenning Shi, Dan Zhao, Yijia Zhu, Guorui Xie, Qing Li, and Yong Jiang. 2025. Helios: Learning and Adaptation of Matching Rules for Continual In-Network Malicious Trafic Detection. In Proceedings of the ACM Web Conference 2025 (WWW’25), April 28–May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 11 pages. https://doi.org/10.1145/3696410.3714742

## 1 Introduction

Network Intrusion Detection Systems (NIDS) are essential for securing web services, as they classify malicious trafic from mixed user trafic to preserve network integrity. However, traditional NIDS, such as those based on Deep Packet Inspection (DPI), overly rely on experts to manually mine the attack fingerprints and struggle to accurately detect increasingly sophisticated cyber threats [5, 30]. Recently, deep learning (DL)-based supervised [10, 36, 43] and unsupervised [16, 20, 35, 37] methods have emerged, leveraging the powerful feature extraction capabilities of neural networks to uncover hidden patterns in network trafic for accurate attack identification. However, their high computational complexity necessitates uploading trafic from the network environment to the control plane (e.g., x86 servers equipped with GPUs) for processing, resulting in significant network bandwidth consumption and processing delays that hinder timely attack detection and can lead to financial losses [8, 25], particularly in large-scale data centers. Furthermore, while an increase in model parameters improves classification accuracy, it also increases training time and restricts eficient updates.

In response to the increasing demand for real-time and highspeed trafic processing, the in-network trafic classification paradigm has emerged [24, 39, 41, 45]. Unlike DL-based NIDS, which are typically deployed on GPUs, the in-network paradigm utilizes programmable switches to directly perform inference within the data plane. This deployment enables terabit-per-second (Tbps) throughput while maintaining nanosecond-level latency. However, programmable switches rely on match-action logic and support only simple instructions [34, 38], such as integer addition and bit shifts, making it infeasible to deploy DL-based models which heavily require floating-point operations [16, 43]. To overcome the computational limitations of programmable switches, for example, [1, 11, 41, 44, 45] transform tree-based machine learning models into match-action rules, while [21, 22] directly extract rules from data. In [39, 40], knowledge distillation is used to distill neural networks into a lightweight binary decision tree (BDT). Addition ally, [42] achieves a conversion between regular expressions (RE) and byte-level recurrent neural networks (BRNN).

However, most existing in-network methods lack consideration of continual model updates. They may fail to identify unseen attacks because they completely partition the feature space based on existing classes, leaving no space for unseen attack types. Moreover, they require full retraining to update the model. In real network scenarios, continual updating and maintenance of NIDS after its initial deployment are essential as zero-day attacks emerge contin uously [2, 31]. This attack-incremental nature of networks necessitates that NIDS refine its countermeasures over time. Although some of the latest unsupervised methods [11, 21, 22] can identify previously unseen attacks, and [22] supports incremental model updates, they are limited to binary classification tasks and fail to meet the fine-grained classification demands of NIDS [43].

In this paper, we aim to design a new in-network NIDS that meets the following requirements: 1) proficient classification ability: The system should perform robust classification on both known and new attacks. It should achieve high accuracy in multi class classification for known classes while efectively identifying unseen attacks without prior knowledge. 2) scalable hardware deployment: Given the limited computational resources and memory of programmable switches, the system should eficiently manage hardware resources to achieve high-throughput trafic processing without incurring excessive overhead. 3) incremental model up dates: The system should support incremental updates without requiring full retraining when adapting to new classes (i.e., admin istrator’s changing requirements like newly detected attacks). This reduces model retraining time and minimizes switch interruption caused by reconfiguration, which is critical in high-speed environments (e.g., large web service provider networks serving millions of users). Despite advancements, none of the current state-of-the-art in-network solutions meet all of these requirements simultaneously.

We propose Helios<sup>1</sup>, a framework designed for continual innetwork malicious trafic detection in attack-incremental scenarios. Helios consists of three key modules: Attack Knowledge Prototyping, Priority-Guided Rule Transformation and Continual Rule Adaptation.

Attack Knowledge Prototyping learns a set of prototypes that en capsulate the knowledge of classes (including benign and known attacks). We propose Supervised Mixture Prototypical Learning (SMPL), based on Supervised Prototypical Learning (SPL) [6] and incorporat ing clustering-based initialization to achieve precise classification. Unlike most SPL methods [12, 26] that rely on complex transformations incompatible with programmable switches and compact each class into a single prototype, Helios operates directly on raw features and assigns multiple prototypes to each class in order to efectively capture diverse patterns. Specifically, Helios uses the weighted infinity norm to measure similarity, which aligns with the matching capabilities of programmable switches.

We design the Priority-Guided Rule Transformation method to convert the learned prototypes into range-based matching rules after completing prototype training, enabling eficient deployment on switches for high-speed packet processing. Specifically, Helios calibrates the acceptance boundaries of prototypes to enhance generalization ability. Then, Helios computes and assigns priorities to the existing prototype-transformed rules, while also introducing higher-priority rules for extended coverage, thereby ensuring optimal classification results in all overlapping regions.

During operations, when a new attack appears and network administrators collect and label data samples for the new attack, the Continual Rule Adaptation module performs incremental rule updates. We retain existing rules that are not matched by any new attack samples and then conduct incremental prototype learning on the updated training set. The newly learned rules are incrementally incorporated, ensuring low-cost hardware reconfiguration.

We implement Helios using the P4<sub>16</sub> [9] language and deploy it on a real Tofino switch for hardware evaluation, achieving a packet processing of 100Gbps per port. To evaluate the performance of Helios, we conduct experiments across three public attack traffic datasets [3, 27, 28]. The experimental results show that Helios achieves high accuracy for known classes (95.78%) while efectively identifying unseen attacks (98.21%). Furthermore, Helios achieves reduced switch resource consumption and less table entry reconfiguration time compared to baselines [40, 41, 44, 45] (up to 4.5x faster), demonstrating its scalability and eficiency for real deployment.

In summary, we make the following contributions:

• We propose Helios, the first in-network solution for continual malicious trafic detection in attack-incremental scenarios, capable of accurately identifying known classes and unseen attacks.

• We develop an innovative learning method that integrates Supervised Mixture Prototypical Learning (SMPL) with clustering initialization, specifically designed to enhance performance.

• We develop a Priority-Guided Rule Transformation method to resolve overlapping between rules. We also design an incremental update mechanism to enable eficient switch reconfiguration.

• We prototype Helios and perform comprehensive experiments to demonstrate its performance<sup>2</sup>.

## 2 Background and Motivation

Network Intrusion Detection Systems (NIDS) are essential for detecting malicious activities and anomalies. Traditional NIDS, such as those based on feature engineering or deep packet inspection (DPI), rely heavily on expert knowledge, limiting their adaptability to evolving threats. The advent of deep learning-based NIDS has significantly improved detection accuracy but at the cost of higher computational complexity and latency. For instance, even real-time NIDS [15] are constrained to throughput rates around 10 Gbps, far below the 100+ Gbps requirements of large-scale cloud and web service networks.

Programmable switches, built on the P4 language [4] and Protocol Independent Switch Architecture (PISA), ofer a solution for high-speed packet processing directly within the data plane. They support custom table-based match-action pipelines deployed on switch ASICs, enabling network functions to operate at line rate. However, programmable switches are limited in computational capability, supporting only basic operations like integer addition and bit shifts, without support for loops or floating-point computations. This makes it challenging to deploy DL-based NIDS directly on switches, as they often require complex calculations and logic to efectively detect attacks [16, 43].

Existing methods address the challenges through two primary approaches. The first focuses on directly deploying tree-based mod els by converting them into rules that programmable switches can execute. For example, IIsy [41] introduces a mapping strategy to ofload a decision tree (DT), while NetBeacon [45] ofloads random forests (RF) by combining feature encoding and decision tables. Similarly, Flowrest [1] implements flow-level inference using RF. The second aims to develop models that are inherently suitable to the computational limitations of programmable switches by in corporating advanced machine learning techniques. For example, Mousika [39] leverages knowledge distillation to train the ternary matching-based binary decision tree (BDT) with the assistance of neural networks, enabling lightweight resource usage on switches. Metis [42] transforms regular expressions into trainable byte-level recurrent neural networks (BRNN), preserving domain-specific ex pert knowledge while allowing supervised optimization.

These methodologies mark notable progress in in-network at tack detection, enabling precise and high-speed trafic processing. However, they still face several challenges, as detailed below.

C1: proficient classification ability. As highlighted in [43], an ideal model should be capable of both multi-class classification of known classes and identification of unknown attacks. This provides fine-grained classification results that enable administrators to take more targeted countermeasures and enhance system reliability by ensuring robustness against zero-day attacks. However, most existing supervised solutions [39–42, 44, 45] assume a fixed set of attack types, with the expectation that trafic data for all attack classes is available in advance. As demonstrated in section 5.2, despite our best eforts to extend these models, they still struggle to efectively detect unseen attacks. Furthermore, while unsupervised methods [11, 21, 22] can identify unseen attacks, they are limited to binary classification tasks and lack support for fine-grained malicious detection.

C2: scalable hardware deployment. To achieve high throughput packet processing, the model should enable in-network deployment. While some recent NIDS [20, 43] can detect unseen attacks, they rely heavily on floating-point operations and complex logical com putations, making them impractical for deployment on resourceconstrained network devices (e.g., programmable switches). Addi tionally, some rule-learning methods [29, 32] based on interpretabil ity have been proposed, but they still require weighted probability adjustments after rule matching, which hinders their deployment. Additionally, the deployment should reduce hardware resource usage to preserve capacity for other essential network functions (e.g., routing). Although Metis [42] can be deployed on the switch, it consumes excessive hardware resources, occupying nearly all pipeline stages (i.e., 11 out of 12) even for binary classification tasks, thus restricting its scalability.

C3: incremental model update. The model should support incremental updates and eficient hardware reconfiguration to reduce retraining costs and avoid disruption to the attack detection. Most existing methods require full model retraining (i.e., learning from scratch), which necessitates updating all hardware table entries. This is particularly problematic in high-speed networks, where even a brief interruption can afect large volumes of trafic. Among in-network methods, only Genos [22] supports incremental updates. However, as mentioned earlier, it is limited to binary classification.

In summary, state-of-the-art NIDS fail to address all of the aforementioned challenges. Therefore, we propose Helios, which leverages learning techniques such as Supervised Prototypical Learning (SPL) and boosting to enable continual in-network malicious trafic detection.

## 3 Overview

In this paper, we propose Helios, a framework for learning and adaptation of matching rules for incremental attack classes, and achieving continual in-network malicious trafic detection. We design a novel Supervised Mixture Prototypical Learning (SMPL) method to encapsulate the knowledge of known classes (including benign trafic and known attacks) into a set of prototypes. Each prototype corresponds to a centroid of its class in the trafic feature space. By calculating the similarity between the input sample and prototypes, Helios achieves multi-class classification of known classes and identification of unseen attacks. As illustrated in Figure 1, Helios consists of three modules: attack knowledge prototyping, priority-guided rule transformation, and class-incremental rule adaptation.

Attack Knowledge Prototyping. The attack knowledge prototyping module distills prototypes that encapsulate the knowledge of each known class. To improve inter-prototype discrimination, Helios leverages the density-based clustering method DBSCAN [13] for prototype initialization, ensuring that each class is assigned a number of prototypes proportional to its data complexity. Helios employs the weighted infinity norm distance as the similarity metric to facilitate the subsequent rule conversion. During SMPL, Helios uses gradient descent to increase the similarity between each prototype and the features of samples from the same class while reducing similarity with features of samples from diferent classes. After training, if a test sample exhibits low similarity to all prototypes, it is classified as unknown.

Priority-Guided Rule Transformation. The priority-guided rule transformation module first converts the trained prototypes into range-based matching rules. Specifically, Helios partitions the feature space by leveraging the sample-prototype associations and calibrates the boundaries to generate prototype-generated rules. To resolve overlaps between these rules, which may cause issues when multiple switch table entries are matched simultaneously, Helios calculates the priorities of these rules using topological sorting. Additionally, Helios introduces the overlapping regions that do not achieve optimal classification results as higher-priority rules. Finally, Helios iteratively performs boosting on misclassified residual samples, re-prototyping them. After each iteration, the resulting rules are merged and all rule priorities are reassigned.

![](images/ad19a5b2ad4f42c222e812b66787f8bcae33bea3f2ba8d3048a0e05b8d4a04a4.jpg)  
Figure 1: The workflow of Helios.

Class-Incremental Rule Adaptation. The class-incremental rule adaptation module performs incremental prototype learning and rule updates when a new attack class emerges (e.g., identified by the network administrator). Helios only makes necessary modifications to the existing rules, retaining those that are not matched by any new attack samples. On this basis, the new training set includes both new attack instances and existing misclassified residual samples. Similar to the boosting process, Helios then conducts incremental learning on the updated training set. The newly learned rules are incrementally incorporated, ensuring low-cost reconfiguration of hardware table entries.

## 4 Methodology

In this section, we present the details of Helios, including the attack knowledge prototyping module, the priority-guided rule transformation module, and the class-incremental rule adaptation module.

## 4.1 Attack Knowledge Prototyping

Existing prototypical learning methods typically assign only a sin gle prototype per class. This is efective in GPU-based servers due to the integration of powerful feature extraction modules (e.g., deep neural networks) in an end-to-end learning manner, resulting in minimal overlap. However, programmable switches do not support extended feature transformations, as they involve floating-point operations and require complex computational logic. In Helios, we directly compare the raw features with prototypes and assign multi ple prototypes to each class with an innovative supervised mixture prototypical learning (SMPL) method. Algorithm 1 illustrates the overall process.

Let $D = \{ ( x _ { i } , y _ { i } ) \} _ { i = 1 } ^ { N }$ represent the training dataset, where $x _ { i } \in$ $\mathbb { R } ^ { d }$ is the feature vector of the �-th sample, and $y _ { i } \in C$ is the corresponding label from the set of known classes (including benign and known attacks). Due to the large range of feature values (e.g., 0 to 65535), we apply min-max normalization to standardize them before inputting them into the model.

Prototype Initialization. Proper prototype initialization is critical to reflect data complexity. Insuficient prototypes fail to capture essential patterns, while excessive ones lead to overfitting. Additionally, careful initialization promotes eficient parameter convergence. Helios utilizes unsupervised clustering to initialize prototypes around cluster centers. Instead of using �-means [17], which requires specifying the number of clusters in advance, we adopt DBSCAN [13] for its ability to identify clusters based on data density. DBSCAN defines clusters using two parameters: the radius of neighborhoods, and the minimum number of points required to form a core cluster.

Specifically, for the �-th class, the initial value of the �-th prototype $P _ { i j }$ is set as the average of the �-th cluster obtained by applying DBSCAN on the training samples labeled as class �: $P _ { i j } =$ $\begin{array} { r } { { \frac { 1 } { | U _ { i j } | } } \sum _ { x _ { k } \in U _ { i j } } x _ { k } } \end{array}$ , where $U _ { i j }$ is the �-th cluster from DBSCAN on {�<sub>�</sub> $\mid y _ { k } = i \}$ . Initializing prototypes from cluster centers facilitates better convergence and enhances representational capacity.

Supervised Mixture Prototypical Learning. To measure the similarity between features and prototypes, a classic choice is to use the Euclidean distance. However, the programmable data plane does not eficiently support square computations. Therefore, we adopt the infinity norm ∥ · ∥<sub>∞</sub>, which calculates the maximum diference between the feature vector and the prototype across all dimensions. This approach aligns well with the nature of the upper and lower bounds in matching rules. Additionally, we introduce a feature weight parameter $w _ { i j }$ for each prototype $P _ { i j }$ , which scales the diferences across dimensions to handle feature values more flexibly. The initial values of the weight parameters � are set to 1, which means that the input remains unchanged without any scaling or transformation at the beginning. By taking the absolute value of original diferences and weights, we ensure the final distance is positive. Consequently, the distance metric is defined as follows:

$$
\mathrm{Dist} (x, P _ {i j}) = \left\| \left| \frac {x - x _ {m i n}}{x _ {m a x} - x _ {m i n}} - P _ {i j} \right| \cdot | w _ {i j} | \right\| _ {\infty},\tag{1}
$$

where $x _ { m i n }$ and $x _ { m a x }$ denote the minimum and maximum values of the features, respectively. $P _ { i j }$ represents the �-th prototype of the �-th class, and $w _ { i j }$ is the corresponding feature weight parameter.

To determine the classification probability distribution for a given sample, we first calculate the distance between the sample feature vector and all prototypes using distance metric (1). We then define the sample’s distance to a specific class as the minimum distance to all prototypes within that class. The classification proba bility distribution is then obtained by applying the softmax function to these distances. Additionally, we introduce a temperature param eter � to control the smoothness of the probability distribution [19]. It scales the distances before applying the softmax function, thereby enhancing the convergence of prototype training. Consequently, the classification probability for the �-th class is as follows:

$$
\operatorname{Prob} (y = i \mid x) = \frac {\exp \left(\min _ {j} \operatorname{Dist} \left(x , P _ {i j}\right) / T\right)}{\sum_ {k} \exp \left(\min _ {j} \operatorname{Dist} \left(x , P _ {k j}\right) / T\right)}.\tag{2}
$$

We use the cross-entropy loss to simultaneously train prototypes � and weight parameters � via gradient descent. Therefore, in each iteration of training for a sample, only the nearest prototype of each class participates in the probability calculation and undergoes corresponding gradient updates. Among these prototypes, the one with the same label as the sample is pulled closer, while those from other classes are pushed away. This ensures that prototypes unrelated to the current training sample remain unafected.

## 4.2 Priority-Guided Rule Transformation

The trained prototypes need to be deployed on the data plane to assign labels for incoming trafic samples. The basic idea is to com pare the input sample with the prototypes of all classes and find the nearest one according to the distance metric. If the minimum dis tance falls below the acceptance threshold, the sample is assigned to the corresponding class of this prototype. Otherwise, it is identified as a new attack type. However, directly deploying this inference process on switches is impractical since distance calculations and comparisons are dificult to implement within the limited stages of the switch pipeline. To address this, Helios design a priority-guided method that transforms the inference process of prototypes into range-based rule matching, making it more suitable for deployment. Algorithm 2 illustrates the overall process of rule transformation.

Boundary Calibration. Since each sample is accepted by its nearest prototype, it is essential to set acceptance thresholds for each prototype to identify unseen attacks. One straightforward approach is to set the threshold as the maximum distance among all accepted samples. However, overly large acceptance boundaries can reduce the generalization ability. We observe that most accepted samples are relatively close to their prototypes in practice, with only a few outliers. Therefore, in Helios, we define the threshold as the mean distance of the accepted training samples, resulting in a tighter boundary. This approach provides a robust threshold by ensuring that the acceptance boundary is dominated by closer samples, thereby preventing it from being influenced by a few distant outliers. The corresponding formulas are given below:

$$
D _ {P _ {i j}} = \left\{x _ {k} \mid y _ {k} = i \wedge \operatorname{Dist} \left(x _ {k}, P _ {i j}\right) \leq \operatorname{Dist} \left(x _ {k}, P _ {i ^ {\prime} j ^ {\prime}}\right), \forall P _ {i ^ {\prime} j ^ {\prime}} \right\},\tag{3}
$$

$$
\operatorname{Threshold} \left(P _ {i j}\right) = \frac {1}{\left| D _ {P _ {i j}} \right|} \sum_ {x _ {k} \in D _ {P _ {i j}}} \operatorname{Dist} \left(x _ {k}, P _ {i j}\right),\tag{4}
$$

where $D _ { P _ { i j } }$ represents the set of samples accepted by $P _ { i j }$ Rule Transformation. After calibrating the acceptance boundaries, Helios transforms the prototype inference process into rangebased matching rules, which are directly supported by programmable switches. For a range rule with � dimensions, an input sample is considered a match if it falls within the specified bounds for each dimension. If the sample exceeds the bounds in any dimension, it is treated as a miss. The formal expression is given below:

$$
\operatorname{Match} (x _ {i}, l, u) = \bigwedge_ {v = 1} ^ {d} (l _ {v} \leq x _ {i v} \leq u _ {v}),\tag{5}
$$

where $l _ { v }$ and $u _ { v }$ represent the lower and upper bounds for dimension $v ,$ and $x _ { i v }$ is the �-th dimension of the input sample $x _ { i }$

Using the acceptance relationship between samples and prototypes, Helios partitions the feature space and transforms each prototype into a corresponding rule. Specifically, the bounds for each feature dimension in the rule are determined by the minimum and maximum values of all accepted samples within the prototype’s acceptance threshold. Formally, for the �-th feature dimension, the bounds of the rule corresponding to prototype $P _ { i j }$ are defined as:

$$
\left\{l _ {v}, u _ {v} \right\} = \left\{\min _ {x _ {r} \in D _ {P _ {i j}}} x _ {r v}, \max _ {x _ {s} \in D _ {P _ {i j}}} x _ {s v} \right\}, \quad v = 1, 2, \ldots , d,\tag{6}
$$

where � and � represent the lower and upper bounds, respectively. Overlap Refinement and Priority Assignment. Since SMPL generates multiple prototypes, overlap issues inevitably arise. When rules overlap, their classification results may conflict, and the optimal class for an overlapping region may not align with any of the original rules that generated it. Given that overlapping regions represent a finer partition of the feature space, refining these regions can further improve performance. Ideally, each region should have an optimal classification result, defined as the class containing the largest number of samples within that region. Fortunately, programmable switches support a priority mechanism that can resolve conflicts by returning the result of the highest priority rule. Therefore, to mitigate these conflicts and maximize classification performance, Helios prioritizes the rules generated by prototypes and introduces additional higher-priority rules to cover the remaining overlapping regions that still do not achieve optimal classification.

First, all samples in the training set are matched against the rules to generate conflict sets. Each conflict set $S _ { i }$ consists of a group of overlapping rules $\{ R _ { i 1 } , R _ { i 2 } , \dots , R _ { i m } \}$ , where $R _ { i j }$ denotes the �-th rule in the �-th conflict set. The class $C _ { i }$ with the highest number of samples in the overlapping region is selected as the representative class for $S _ { i } .$ . Next, a directed acyclic graph (DAG) � is constructed. The conflict sets are then sorted in ascending order based on their sizes, and each conflict set is processed sequentially. For each $S _ { i : }$ directed edges $( R _ { i j }  R _ { i k } )$ are inserted to � from all rules $R _ { i j } \in S _ { i }$ belonging to class $C _ { i }$ to all other rules $R _ { i k } \in S _ { i }$ that do not belong to class $C _ { i } .$ . If a path already exists from $R _ { i k } \mathrm { t o } R _ { i j }$ , the insertion of this edge is skipped. Finally, the priorities of the prototype-generated rules are assigned in descending order based on the results of topological sorting on $G ,$ starting from 1. For any conflict set $S _ { k }$ that remains unresolved, we introduce the corresponding overlapping regions as additional rules. These rules are assigned a priority of $1 0 0 0 0 + \left| S _ { k } \right|$ , where |�<sub>�</sub> | denotes the size of conflict set $S _ { k } .$ This ensures that their priority surpasses all prototype-generated rules, allowing for complete coverage. Additionally, we observe that some rules accept only a small number of samples, making them less cost efective. We prune these rules to mitigate overfitting, which also reduces the switch’s resource consumption.

Rule Boosting. After completing the initial round of prototype training and rule transformation (including refinement), Helios utilizes the misclassified residual training samples based on the current rules to perform rule boosting. New prototypes are trained on these residual samples, and the resulting rules are merged into the existing rule set. Following this, Helios applies overlap refine ment and priority assignment to the combined set of rules and then iteratively proceeds to the next round ofboosting. Recall that Helios employs tight boundary calibration, which, in combination with boosting, maximizes the fit to the sample distribution and enhances overall classification performance.

## 4.3 Class-Incremental Rule Adaptation

For the initial classes, Helios is trained and deployed for the first time. When an unseen attack emerges, if a sample does not match any of the rules, it is identified as an unseen attack class. The classi fication results from the data plane provide network administrators with timely feedback and alerts. After network administrators col lect and label new attack samples, Helios performs incremental learning on the updated dataset, enabling eficient rule updates and lightweight switch reconfiguration. Algorithm 3 illustrates the overall process of rule adaptation.

Isolated Rule Retention. During rule updates, a totally incremental approach would retain all existing rules while adding new ones learned from the new attack. However, this may lead to significant conflicts between merged rules, reducing learning capability and deployment eficiency. Thus, existing rules need to be adjusted nec essarily, such as modifying their boundaries or splitting them [22]. Specifically, Helios retains those isolated rules that are not matched by any new attack samples in the training set, that is,

$$
R _ {i} \text {   is   retained   if   } \forall x _ {k} \in D _ {\text { new   attack }}, \neg \text { Match } (x _ {k}, R _ {i}).\tag{7}
$$

By retaining rules that are unafected by new attack samples, Helios achieves the trade-of between minimizing unnecessary changes and maintaining flexibility for updates.

Incremental Rule Update. After retaining the existing isolated rules, Helios performs incremental learning on the new dataset, which includes misclassified residual samples and new attack sam ples. Similar to the boosting-based SMPL, new rules are generated and incrementally merged into the existing set. Helios then applies overlap refinement and priority assignment across all rules. For the newly added rules, only incremental deployment to the switch is required, ensuring eficient reconfiguration. For retained prototype generated rules, some may need priority adjustments based on the updated topological sorting results, unless they do not conflict with any new rules and thus remain unchanged. Additionally, if the op timal classification results change, corresponding modifications are also necessary. Compared to adding or deleting rules, modifying priorities or updating classification results is more eficient.

## 5 Experiments

## 5.1 Settings

Datasets. (1) CICIDS2018 [28], which includes network trafic generated within a simulated enterprise environment, featuring various attacks such as Distributed Denial of Service (DDoS) attacks (including LOIC and HOIC methods), Denial of Service (DoS) attacks (e.g., GoldenEye, Hulk, Slowloris), and SSH brute force attempts. (2) TON-IoT [3], specifically designed for Internet of Things (IoT) applications, incorporating benign trafic alongside nine distinct attack scenarios. (3) UNSW-NB15 [27], which integrates real normal activities with synthetic contemporary attack behaviors, featuring benign trafic and encompassing nine types of attacks.

Baselines. Given that methods supporting only binary classification are unsuitable for class-incremental learning scenarios, we select four state-of-the-art multi-classification in-network methods as baselines: 1) IIsy [41], which designs a feature encoding approach for deploying decision trees; 2) Planter [44] and Netbeacon [45], which utilize diferent ensemble encoding methods for ofloading random forests; and 3) Mousikav2 [40], a lightweight method based on knowledge distillation.

Configurations. We divide the training and updating process into several tasks, each consisting of classification for the currently known classes and the identification of an unseen attack. We set the training epochs for each task to 50 and use the Adam optimizer with a learning rate of 0.001. The default values for other key hyper-parameters are provided in Section A. Considering the limited well-labeled samples in the real-world environment, we set a 2:8 ratio of training set and testing set to simulate few-shot learning scenarios. Additionally, since the baselines do not inherently support unknown class identification, we extend them in a manner similar to previous out-of-distribution detection arts [18, 23, 33] by employing a threshold on the classification probabilities. Specifically, if the classification probabilities for all classes fall below the threshold, the input sample is classified as unknown. We calculate the optimal threshold for each baseline by maximizing 5×ACC+TPR while ensuring that the ACC remains no lower than 85%.

## 5.2 Classification Performance Evaluation

We compare the classification performance of Helios with enhanced baseline methods across three datasets, as shown in Table 1. The tasks are divided based on the number of classes in each dataset, with the specific attack details in Table 3. Initially (Task 1), the model classifies the initial classes (including benign and one attack) and identifies the first unseen attack. In each subsequent task, the unseen attack from its previous task is added as known, while a new attack is introduced as unseen for that task. Finally (Task ALL), ACC and F1 represent performance across all classes, while TPR is calculated as the weighted average of all previous tasks, representing the overall identification rate for unseen attacks.

For overall performance in Task ALL, Helios achieves the highest ACC and F1 across all datasets, as well as the best TPR on CI-CIDS2018 and UNSW-NB15, demonstrating superior classification precision. For individual tasks, Helios shows more stable performance compared to the baselines, highlighting its ability to handle continually emerging unseen attacks. In summary, even after optimizing the existing state-of-the-art in-network methods and selecting their optimal thresholds, Helios consistently outperforms them in classifying known classes and identifying unseen attacks.

Table 1: Comparisons of Helios with prior arts on each task in terms of classification performance. Here, $\mathbf { A C C } , \mathbf { F 1 } ,$ and TPR represent the Accuracy (%), F1-score (%) of known class classification, and the True Positive Rate (%) of new attack identification.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Task</td><td colspan="3">Planter</td><td colspan="3">Netbeacon</td><td colspan="3">Mousikav2</td><td colspan="3">IIsy</td><td colspan="3">Helios</td></tr><tr><td>ACC</td><td>F1</td><td>TPR</td><td>ACC</td><td>F1</td><td>TPR</td><td>ACC</td><td>F1</td><td>TPR</td><td>ACC</td><td>F1</td><td>TPR</td><td>ACC</td><td>F1</td><td>TPR</td></tr><tr><td rowspan="10">IDS</td><td>1</td><td>100.00</td><td>100.00</td><td>0.00</td><td>100.00</td><td>100.00</td><td>0.00</td><td>98.86</td><td>99.39</td><td>75.85</td><td>99.98</td><td>99.98</td><td>0.00</td><td>99.18</td><td>99.59</td><td>100.00</td></tr><tr><td>2</td><td>99.95</td><td>99.95</td><td>0.00</td><td>99.95</td><td>99.95</td><td>0.00</td><td>99.80</td><td>99.80</td><td>0.00</td><td>99.97</td><td>99.97</td><td>0.00</td><td>99.27</td><td>99.63</td><td>100.00</td></tr><tr><td>3</td><td>99.91</td><td>99.95</td><td>98.30</td><td>99.91</td><td>99.95</td><td>98.30</td><td>99.88</td><td>99.91</td><td>35.10</td><td>99.96</td><td>99.96</td><td>0.00</td><td>99.33</td><td>99.66</td><td>100.00</td></tr><tr><td>4</td><td>99.74</td><td>99.86</td><td>22.85</td><td>99.74</td><td>99.86</td><td>22.85</td><td>99.83</td><td>99.83</td><td>0.00</td><td>99.94</td><td>99.94</td><td>0.00</td><td>98.84</td><td>99.41</td><td>56.54</td></tr><tr><td>5</td><td>90.76</td><td>93.73</td><td>59.10</td><td>88.87</td><td>92.40</td><td>59.10</td><td>91.50</td><td>91.50</td><td>0.00</td><td>94.89</td><td>94.83</td><td>0.00</td><td>92.50</td><td>92.86</td><td>100.00</td></tr><tr><td>6</td><td>95.43</td><td>95.37</td><td>0.00</td><td>94.59</td><td>94.53</td><td>0.00</td><td>92.74</td><td>92.74</td><td>0.00</td><td>95.52</td><td>95.46</td><td>0.00</td><td>93.73</td><td>94.08</td><td>100.00</td></tr><tr><td>7</td><td>89.05</td><td>92.85</td><td>100.00</td><td>88.99</td><td>92.72</td><td>100.00</td><td>93.73</td><td>93.73</td><td>0.00</td><td>95.35</td><td>95.30</td><td>0.00</td><td>94.69</td><td>95.01</td><td>100.00</td></tr><tr><td>8</td><td>89.90</td><td>93.44</td><td>92.31</td><td>89.67</td><td>92.96</td><td>82.05</td><td>93.59</td><td>93.60</td><td>10.26</td><td>95.35</td><td>95.30</td><td>0.00</td><td>95.85</td><td>96.04</td><td>100.00</td></tr><tr><td>9</td><td>90.47</td><td>93.81</td><td>98.47</td><td>94.57</td><td>94.40</td><td>97.71</td><td>86.12</td><td>89.75</td><td>99.24</td><td>95.33</td><td>95.28</td><td>0.00</td><td>95.79</td><td>95.98</td><td>100.00</td></tr><tr><td>ALL</td><td>92.11</td><td>94.71</td><td>26.78</td><td>94.25</td><td>94.06</td><td>26.76</td><td>93.54</td><td>93.45</td><td>33.21</td><td>95.27</td><td>95.23</td><td>0.00</td><td>95.78</td><td>95.98</td><td>98.21</td></tr><tr><td rowspan="9">IoT</td><td>1</td><td>99.91</td><td>99.95</td><td>50.22</td><td>99.91</td><td>99.95</td><td>50.22</td><td>97.20</td><td>95.83</td><td>0.00</td><td>100.00</td><td>100.00</td><td>0.00</td><td>95.77</td><td>96.48</td><td>100.00</td></tr><tr><td>2</td><td>96.04</td><td>97.47</td><td>92.05</td><td>95.93</td><td>97.37</td><td>91.95</td><td>95.84</td><td>96.46</td><td>11.79</td><td>98.48</td><td>98.53</td><td>0.00</td><td>94.96</td><td>96.56</td><td>100.00</td></tr><tr><td>3</td><td>98.89</td><td>98.89</td><td>98.79</td><td>97.41</td><td>98.19</td><td>98.83</td><td>94.28</td><td>94.76</td><td>58.75</td><td>98.92</td><td>98.89</td><td>0.00</td><td>95.52</td><td>96.91</td><td>99.16</td></tr><tr><td>4</td><td>97.83</td><td>98.40</td><td>60.41</td><td>97.68</td><td>98.35</td><td>99.01</td><td>97.09</td><td>97.55</td><td>43.83</td><td>98.87</td><td>98.87</td><td>0.11</td><td>97.05</td><td>97.97</td><td>23.63</td></tr><tr><td>5</td><td>98.73</td><td>99.10</td><td>89.19</td><td>98.61</td><td>98.99</td><td>89.63</td><td>99.03</td><td>99.07</td><td>4.87</td><td>99.29</td><td>99.28</td><td>0.71</td><td>97.74</td><td>98.47</td><td>92.62</td></tr><tr><td>6</td><td>96.47</td><td>97.69</td><td>39.01</td><td>92.89</td><td>96.04</td><td>56.07</td><td>97.11</td><td>97.23</td><td>7.27</td><td>97.43</td><td>98.19</td><td>12.74</td><td>96.26</td><td>97.18</td><td>45.36</td></tr><tr><td>7</td><td>85.59</td><td>91.16</td><td>99.96</td><td>85.30</td><td>90.58</td><td>99.85</td><td>93.42</td><td>93.36</td><td>0.00</td><td>97.91</td><td>97.90</td><td>0.00</td><td>95.74</td><td>96.34</td><td>99.80</td></tr><tr><td>8</td><td>88.98</td><td>92.89</td><td>54.99</td><td>91.94</td><td>94.02</td><td>40.54</td><td>91.25</td><td>93.64</td><td>31.28</td><td>96.61</td><td>97.78</td><td>25.95</td><td>97.04</td><td>97.68</td><td>25.84</td></tr><tr><td>ALL</td><td>88.60</td><td>88.43</td><td>71.83</td><td>86.58</td><td>86.53</td><td>79.06</td><td>83.01</td><td>87.01</td><td>21.19</td><td>91.72</td><td>91.72</td><td>6.87</td><td>92.20</td><td>92.99</td><td>62.93</td></tr><tr><td rowspan="9">NB15</td><td>1</td><td>97.38</td><td>98.57</td><td>55.59</td><td>98.05</td><td>98.48</td><td>73.84</td><td>95.37</td><td>97.08</td><td>71.79</td><td>99.10</td><td>99.10</td><td>0.00</td><td>94.42</td><td>96.96</td><td>99.09</td></tr><tr><td>2</td><td>96.35</td><td>97.95</td><td>21.30</td><td>98.09</td><td>98.19</td><td>1.94</td><td>88.10</td><td>89.71</td><td>38.31</td><td>99.35</td><td>99.34</td><td>0.00</td><td>91.86</td><td>95.20</td><td>63.13</td></tr><tr><td>3</td><td>91.80</td><td>95.24</td><td>57.35</td><td>95.30</td><td>95.16</td><td>0.00</td><td>87.90</td><td>90.89</td><td>17.15</td><td>97.76</td><td>97.75</td><td>0.00</td><td>90.68</td><td>94.03</td><td>86.14</td></tr><tr><td>4</td><td>88.21</td><td>92.78</td><td>58.77</td><td>88.18</td><td>87.67</td><td>0.00</td><td>90.40</td><td>91.37</td><td>3.57</td><td>96.78</td><td>96.77</td><td>0.00</td><td>90.51</td><td>93.87</td><td>55.35</td></tr><tr><td>5</td><td>85.78</td><td>91.44</td><td>87.68</td><td>79.61</td><td>77.02</td><td>0.00</td><td>85.07</td><td>85.21</td><td>0.16</td><td>95.29</td><td>95.28</td><td>0.00</td><td>86.37</td><td>89.92</td><td>73.19</td></tr><tr><td>6</td><td>86.08</td><td>91.58</td><td>90.77</td><td>80.30</td><td>78.33</td><td>0.00</td><td>85.71</td><td>86.50</td><td>1.78</td><td>95.54</td><td>95.54</td><td>0.00</td><td>89.43</td><td>92.65</td><td>66.59</td></tr><tr><td>7</td><td>91.00</td><td>93.08</td><td>27.78</td><td>69.30</td><td>67.74</td><td>0.00</td><td>82.14</td><td>82.24</td><td>0.00</td><td>93.07</td><td>93.04</td><td>0.00</td><td>89.44</td><td>92.50</td><td>62.43</td></tr><tr><td>8</td><td>91.12</td><td>92.28</td><td>45.71</td><td>73.74</td><td>72.20</td><td>0.00</td><td>83.84</td><td>83.22</td><td>0.00</td><td>92.08</td><td>92.08</td><td>0.00</td><td>91.53</td><td>93.11</td><td>69.30</td></tr><tr><td>ALL</td><td>81.79</td><td>88.79</td><td>62.65</td><td>75.64</td><td>73.55</td><td>1.22</td><td>79.88</td><td>81.60</td><td>6.02</td><td>91.83</td><td>91.83</td><td>0.00</td><td>92.91</td><td>94.19</td><td>69.15</td></tr></table>

![](images/89774395a87ecdca510035c7766575224c6a0ee531c6dd8df94bdd8002564a9e.jpg)  
(a) CICIDS2018 dataset

![](images/ac84e0abce3738019bb55d8aca81f1fc0daab1efab05aba28b299342ea2e5825.jpg)  
10(b) UNSW-NB15 dataset

![](images/d81b53a1727ef943547578f626d8894694dbd5af389decd5d505de9f0dc7ef1e.jpg)  
(c) TON-IoT dataset  
Figure 2: Receiver Operating Characteristic (ROC) curve of new attacks identification on three datasets.

To further demonstrate the model’s capability in identifying unseen attacks under diferent threshold settings, we plot ROC curves, as shown in Figure 2. Across all datasets, Helios outperforms the baseline methods, achieving higher TPR while maintaining lower FPR. On CICIDS2018, Helios achieves an AUC of 0.98, significantly outperforming the second-best method, Planter, which achieves 0.59. On TON-IoT and UNSW-NB15, Helios also surpasses its top competitors, with AUC of0.90 and 0.88, compared to 0.88 for Netbea con on TON-IoT and 0.81 for Planter on UNSW-NB15, respectively.

## 5.3 Reconfiguration Time Evaluation

We conduct training on servers equipped with Intel (R) Xeon (R) Silver 4210 CPU @ 2.20GHz and V100 GPUs, and deploy the model on a commodity Tofino switch (Edgecore Wedge100BF-65X<sup>3</sup>). Figure 3 presents the average switch table reconfiguration time for diferent methods, along with the number of rules learned on total classes. Overall, Helios outperforms the most lightweight but less accurate method, Mousikav2, while significantly surpassing other methods. As shown in Figure 3(a), Helios achieves minimal rule update time overhead, ranging from 0.8 to 3.1 seconds. This result can be attributed to the number of rules learned, as depicted in Figure 3(b), where Helios demonstrates higher learning eficiency by requiring fewer rules. Additionally, due to its incremental update mechanism, Helios achieves a 13.4% to 37.3% reduction in rule deployment, further reducing time overhead. In conclusion, Helios enables eficient switch reconfiguration and minimizes switch interruption time.

## 5.4 Ablation Study

To further validate the design of Helios, we conducted ablation studies on the TON-IoT dataset to assess the contribution of each module, as detailed in Table 2. First, initializing prototypes with

CICIDS2018 TON-IoT UNSW-NB15

![](images/35a46db71f06431091642d42b78d9d496aa0eebb014b354c7156c613bbc3f253.jpg)  
e(a) The switch reconfiguration time overhead of methods

![](images/9b6fa745c8129b274ed80b8cc3f564c72cb15d44e554ea5233ad6d626b593eae.jpg)  
(b) The number of rules learned by diferent methods  
Figure 3: Comparison of switch reconfiguration time and the number of learned rules between Helios and the baseline methods across three datasets. For Helios, the dashed portion of the bar represents the savings during incremental updates.

DBSCAN yields significant improvements in both ACC and TPR compared to Normal or Uniform initialization, and it also surpasses �-means initialization (we set suficient clusters for �-means to ensure consistency). Second, using Euclidean distance decreases ACC, suggesting that $l _ { \infty }$ distance provides a better delineation of deci sion boundaries and is more suitable for conversion to range-based rules. Next, initializing prototypes without subsequent boosting, or performing only a single training iteration after initialization, fails to achieve high ACC. While continual boosting without SMPL im proves ACC, it significantly lowers TPR. These results demonstrate that both SMPL and boosting are efective methods for enhancing performance. Finally, without boundary calibration, although slightly increasing ACC, results in a notable decrease in TPR. This highlights the importance of refining the accepting boundary of prototypes. Overall, Helios achieves an optimal balance between ACC and TPR, ensuring high precision in classifying known classes while efectively identifying unknown attacks.

## 5.5 Hardware Performance

The hardware performance of Helios is depicted in Figure 4. Figure 4(a) illustrates the memory consumption, showing that Helios typ ically consumes less than 10% of TCAM and SRAM. Even for the most complex dataset, UNSW-NB15, Helios requires only around 40% of TCAM. This eficiency ensures suficient resources remain available for other essential network functions, such as routing.

Table 2: The ablation study of key components in Helios, where NOR represents the number of rules.

<table><tr><td>Method</td><td>ACC(%)</td><td>TPR(%)</td><td>NOR</td></tr><tr><td>w/ Normal init.</td><td>76.91</td><td>36.38</td><td>90</td></tr><tr><td>w/ Uniform init.</td><td>82.00</td><td>33.18</td><td>61</td></tr><tr><td>w/ K-means</td><td>91.46</td><td>58.30</td><td>394</td></tr><tr><td>w/ Euclidean dist.</td><td>90.08</td><td>64.66</td><td>306</td></tr><tr><td>w/o SMPL and Boosting</td><td>66.08</td><td>87.76</td><td>161</td></tr><tr><td>w/o Boosting</td><td>70.39</td><td>78.18</td><td>146</td></tr><tr><td>w/o SMPL</td><td>88.52</td><td>38.39</td><td>325</td></tr><tr><td>w/o Boundary Calibration</td><td>92.48</td><td>38.91</td><td>528</td></tr><tr><td>Helios</td><td>92.20</td><td>62.93</td><td>321</td></tr></table>

Additionally, we use a trafic generator (SPIRENT N11U<sup>4</sup>) to simulate high-speed network trafic at 10 Gbps, 50 Gbps, and 100 Gbps, with the throughput and latency results presented in Figure 4(b). As shown, Helios achieves high-speed processing without packet loss, while maintaining notably low latency (around 0.66 ��) across varying input trafic rates. Therefore, Helios enables high-throughput, low-latency detection of malicious trafic.

![](images/bdc8bb413d2c8c48d2797d6202d6090d8b679f9fa1442af5dbbac30fe36b2786.jpg)

![](images/85f4480f72f01f43718873238d5ba555901f0394f394eb46d047be5e2917cc86.jpg)  
(a) Resource consumption  
(b) Throughput and latency  
Figure 4: Hardware performance of Helios.

## 6 Conclusion

In this paper, we propose Helios, a continual in-network malicious trafic detection framework for attack-incremental scenarios. Specifically, Helios integrates supervised mixture prototypical learning with boosting to derive prototypes that represent the knowledge of each class, facilitating the classification of known classes and the identification of unknown attacks. The inference process of prototypes is then transformed into priority-based rule matching, ensuring accurate and eficient switch deployment. Helios also supports incremental prototype learning and rule updates when new attacks are incorporated, achieving low-cost hardware reconfiguration. Extensive evaluations of Helios using three datasets demonstrate its efectiveness in identifying unknown attacks and performing eficient updates.

## 7 Acknowledgement

This work is supported by the Major Key Project of PCL under grant No. PCL2023A06, the National Key Research and Development Program of China under grant No. 2022YFB3105000, and the Shenzhen Key Lab of Software Defined Networking under grant No. ZDSYS20140509172959989.

## References

[1] Aristide Tanyi-Jong Akem, Michele Gucciardo, and Marco Fiore. 2023. Flowrest: Practical flow-level inference in programmable switches with random forests. In Proceedings ofthe International Conference on Computer Communications. IEEE, 1–10.

[2] Leyla Bilge and Tudor Dumitraş. 2012. Before we knew it: an empirical study of zero-day attacks in the real world. In Proceedings ofthe 2012 ACM conference on Computer and communications security. 833–844.

[3] Tim M Booij, Irina Chiscop, Erik Meeuwissen, Nour Moustafa, and Frank TH Den Hartog. 2021. ToN\_IoT: The role of heterogeneity and the need for stan dardization of features and attack types in IoT network intrusion data sets. IEEE Internet ofThings Journal 9, 1 (2021), 485–496

[4] Pat Bosshart, Dan Daly, Glen Gibb, Martin Izzard, Nick McKeown, Jennifer Rexford, Cole Schlesinger, Dan Talayco, Amin Vahdat, George Varghese, et al. 2014. P4: Programming protocol-independent packet processors. ACM SIGCOMM Computer Communication Review 44, 3 (2014), 87–95.

[5] Anna L Buczak and Erhan Guven. 2015. A survey of data mining and machine learning methods for cyber security intrusion detection. IEEE Communications surveys & tutorials 18, 2 (2015), 1153–1176.

[6] Chaofan Chen, Oscar Li, Daniel Tao, Alina Barnett, Cynthia Rudin, andJonathan K Su. 2019. This looks like that: deep learning for interpretable image recognition. Advances in neural information processing systems 32 (2019).

[7] Tianqi Chen and Carlos Guestrin. 2016. Xgboost: A scalable tree boosting system. In Proceedings of the 22nd acm sigkdd international conference on knowledge discovery and data mining. 785–794.

[8] Catalin Cimpanu. [n. d.]. Australian banks targeted by DDoS extortionists. https: //www.zdnet.com/article/australian-banks-targeted-by-ddos-extortionists/. Ac cessed: 2024-08-04.

[9] The P4 Language Consortium. [n. d.]. P4<sub>16</sub> Language Specification. https://p4. org/p4-spec/docs/P4-16-v1.0.0-spec.html. Accessed: 2024-06-10..

[10] Mahendra Data and Masayoshi Aritsugi. 2021. T-DFNN: an incremental learning algorithm for intrusion detection systems. IEEE Access 9 (2021), 154156–154171.

[11] Yutao Dong, Qing Li, Kaidong Wu, Ruoyu Li, Dan Zhao, Gareth Tyson, Junkun Peng, Yong Jiang, Shutao Xia, and Mingwei Xu. 2023. {HorusEye}: A Realtime {IoT} Malicious Trafic Detection Framework using Programmable Switches. In Proceedings ofthe 32nd USENIX Security Symposium. 571–588.

[12] Xuefeng Du, Gabriel Gozum, Yifei Ming, and Yixuan Li. 2022. Siren: Shaping representations for detecting out-of-distribution objects. Advances in Neural Information Processing Systems 35 (2022), 20434–20449.

[13] Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu, et al. 1996. A density based algorithm for discovering clusters in large spatial databases with noise. In Proceedings ofthe International Conference on Knowledge Discovery and Data Mining, Vol. 96. 226–231.

[14] Jerome H Friedman. 2001. Greedy function approximation: a gradient boosting machine. Annals ofstatistics (2001), 1189–1232.

[15] Chuanpu Fu, Qi Li, Meng Shen, and Ke Xu. 2021. Realtime robust malicious trafic detection via frequency domain analysis. In Proceedings ofthe 2021 ACM SIGSAC Conference on Computer and Communications Security. 3431–3446.

[16] Xueying Han, Susu Cui, Jian Qin, Song Liu, Bo Jiang, Cong Dong, Zhigang Lu, and Baoxu Liu. 2024. ContraMTD: An Unsupervised Malicious Network Trafic Detection Method based on Contrastive Learning. In Proceedings ofthe ACM on Web Conference 2024. 1680–1689.

[17] John A Hartigan and Manchek A Wong. 1979. Algorithm AS 136: A k-means clustering algorithm. Journal of the royal statistical society. series c (applied statistics) 28, 1 (1979), 100–108.

[18] Dan Hendrycks and Kevin Gimpel. 2016. A baseline for detecting misclassified and out-of-distribution examples in neural networks. arXiv preprint arXiv:1610.02136 (2016).

[19] Geofrey Hinton. 2015. Distilling the Knowledge in a Neural Network. arXiv preprint arXiv:1503.02531 (2015).

[20] Peiyang Li, Ye Wang, Qi Li, Zhuotao Liu, Ke Xu, Ju Ren, Zhiying Liu, and Ruilin Lin. 2023. Learning from Limited Heterogeneous Training Data: Meta-Learning for Unsupervised Zero-Day Web Attack Detection across Web Domains. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 1020–1034.

[21] Ruoyu Li, Qing Li, Yu Zhang, Dan Zhao, Yong Jiang, and Yong Yang. 2024. Interpreting unsupervised anomaly detection in security via rule extraction. Advances in Neural Information Processing Systems 36 (2024).

[22] Ruoyu Li, Qing Li, Yu Zhang, Dan Zhao, Xi Xiao, and Yong Jiang. 2024. Genos: General In-Network Unsupervised Intrusion Detection by Rule Extraction. arXiv preprint arXiv:2403.19248 (2024).

[23] Xixi Liu, Yaroslava Lochman, and Christopher Zach. 2023. Gen: Pushing the limits of softmax-based out-of-distribution detection. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition. 23946–23955.

[24] Zaoxing Liu, Hun Namkung, Georgios Nikolaidis, Jeongkeun Lee, Changhoon Kim, Xin Jin, Vladimir Braverman, Minlan Yu, and Vyas Sekar. 2021. Jaqen: A {High-Performance} {Switch-Native} approach for detecting and mitigating

volumetric {DDoS} attacks with programmable switches. In Proceedings ofthe 30th USENIX Security Symposium. 3829–3846.

[25] Grainne McKeever. [n. d.]. Imperva releases its Global DDoS Threat Landscape Report 2023. https://www.imperva.com/blog/imperva-releases-its-global-ddosthreat-landscape-report-2023/. Accessed: 2024-08-04.

[26] Yifei Ming, Yiyou Sun, Ousmane Dia, and Yixuan Li. 2023. How to Exploit Hyperspherical Embeddings for Out-of-Distribution Detection?. In Proceedings ofthe Eleventh International Conference on Learning Representations.

[27] Nour Moustafa and Jill Slay. 2015. UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 network data set). In Proceedings ofthe 2015 Military Communications and Information Systems Conference. IEEE, 1–6.

[28] Iman Sharafaldin, Arash Habibi Lashkari, Ali A Ghorbani, et al. 2018. Toward generating a new intrusion detection dataset and intrusion trafic characterization. ICISSp 1 (2018), 108–116.

[29] Shaoyun Shi, Yuexiang Xie, Zhen Wang, Bolin Ding, Yaliang Li, and Min Zhang. 2022. Explainable neural rule learning. In Proceedings ofthe ACM Web Conference 2022. 3031–3041.

[30] Nathan Shone, Tran Nguyen Ngoc, Vu Dinh Phai, and Qi Shi. 2018. A deep learning approach to network intrusion detection. IEEE transactions on emerging topics in computational intelligence 2, 1 (2018), 41–50.

[31] Ruming Tang, Zheng Yang, Zeyan Li, Weibin Meng, Haixin Wang, Qi Li, Yongqian Sun, Dan Pei, Tao Wei, Yanfei Xu, et al. 2020. Zerowall: Detecting zero-day web attacks through encoder-decoder recurrent neural networks. In Proceedings of the IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2479–2488.

[32] Zhuo Wang, Wei Zhang, Ning Liu, and Jianyong Wang. 2021. Scalable rulebased representation learning for interpretable classification. Advances in Neural Information Processing Systems 34 (2021), 30479–30491.

[33] Hongxin Wei, Renchunzi Xie, Hao Cheng, Lei Feng, Bo An, and Yixuan Li. 2022. Mitigating neural network overconfidence with logit normalization. In Proceedings ofthe International conference on machine learning. PMLR, 23631–23644.

[34] Jingyu Xiao, Qing Li, Dan Zhao, Xudong Zuo, Wenxin Tang, and Yong Jiang. 2024. Themis: A passive-active hybrid framework with in-network intelligence for lightweight failure localization. Computer Networks 255 (2024), 110836.

[35] Jingyu Xiao, Zhiyao Xu, Qingsong Zou, Qing Li, Dan Zhao, Dong Fang, Ruoyu Li, Wenxin Tang, Kang Li, Xudong Zuo, Penghui Hu, Yong Jiang, Zixuan Weng, and Michael R. Lyu. 2024. Make Your Home Safe: Time-aware Unsupervised User Behavior Anomaly Detection in Smart Homes via Loss-guided Mask. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining. 3551–3562.

[36] Jingyu Xiao, Qingsong Zou, Qing Li, Dan Zhao, Kang Li, Wenxin Tang, Runjie Zhou, and Yong Jiang. 2023. User Device Interaction Prediction via Relational Gated Graph Attention Network and Intent-aware Encoder. In Proceedings of the 2023 International Conference on Autonomous Agents and Multiagent Systems (AAMAS). 1634–1642.

[37] Jingyu Xiao, Qingsong Zou, Qing Li, Dan Zhao, Kang Li, Zixuan Weng, Ruoyu Li, and Yong Jiang. 2023. I Know Your Intent: Graph-enhanced Intent-aware User Device Interaction Prediction via Contrastive Learning. Proceedings ofthe ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (IMUWT/UbiComp) 7, 3 (2023), 1–28.

[38] Jingyu Xiao, Xudong Zuo, Qing Li, Dan Zhao, Hanyu Zhao, Yong Jiang, Jiyong Sun, Bin Chen, Yong Liang, and Jie Li. 2023. FlexNF: Flexible Network Function Orchestration for Scalable On-Path Service Chain Serving. IEEE/ACM Transactions on Networking (ToN) (2023).

[39] Guorui Xie, Qing Li, Yutao Dong, Guanglin Duan, Yong Jiang, and Jingpu Duan. 2022. Mousika: Enable general in-network intelligence in programmable switches by knowledge distillation. In Proceedings ofthe International Conference on Computer Communications. IEEE, 1938–1947.

[40] Guorui Xie, Qing Li, Guanglin Duan,Jiaye Lin, Yutao Dong, YongJiang, Dan Zhao, and Yuan Yang. 2023. Empowering in-network classification in programmable switches by binary decision tree and knowledge distillation. IEEE/ACM Transactions on Networking 32, 1 (2023), 382–395.

[41] Zhaoqi Xiong and Noa Zilberman. 2019. Do switches dream of machine learning? toward in-network classification. In Proceedings of the 18th ACM workshop on hot topics in networks. 25–33.

[42] Zhengxin Zhang, Yucheng Huang, Guanglin Duan, Qing Li, Dan Zhao, Yong Jiang, Lianbo Ma, Xi Xiao, and Hengyang Xu. 2024. Metis: understanding and enhancing in-network regular expressions. Advances in Neural Information Processing Systems 36 (2024).

[43] Ziming Zhao, Zhaoxuan Li, Zhuoxue Song, Wenhao Li, and Fan Zhang. 2024. Trident: A Universal Framework for Fine-Grained and Class-Incremental Unknown Trafic Detection. In Proceedings ofthe ACM on Web Conference 2024. 1608–1619.

[44] Changgang Zheng and Noa Zilberman. 2021. Planter: seeding trees within switches. In Proceedings ofthe SIGCOMM’21 Poster and Demo Sessions. 12–14.

[45] Guangmeng Zhou, Zhuotao Liu, Chuanpu Fu, Qi Li, and Ke Xu. 2023. An eficient design of intelligent network data plane. In Proceedings of the 32nd USENIX Security Symposium. 6203–6220.

## A Parameters Analysis

We analyze the impact of three key parameters on the performance of Helios: boosting iteration, pruning lower bound, and calibration threshold. The experimental results are presented in Figure 5.

Boosting iteration. As shown in Figure 5(a), increasing boosting iterations initially improves ACC as the model handles misclassified samples better. However, beyond a certain point, both ACC and TPR reach a state of convergence, indicating suficient learning. To pre vent overfitting and excessive rule generation, the default boosting iteration is set to 4, balancing accuracy and model complexity.

Pruning lower bound. Figure 5(b) shows that without pruning, both ACC and TPR are lower compared to when a smaller pruning lower bound (e.g., 10) is applied. This is because overfitted rules from the training set reduce generalization on the test set and occupy unnecessary feature space. As the pruning lower bound increases, rule complexity decreases, but ACC also declines. There fore, a smaller pruning lower bound provides better results, and the default value is set to 10.

Calibration threshold. Recall that we use the mean distance of a prototype’s accepted samples as the threshold (Section 4.2), and here we multiply this threshold by a scaling weight for parameter analysis. As shown in Figure 5(c), when the scaling weight is below 1.0, ACC increases significantly because smaller thresholds fail to capture all relevant data. When the scaling weight exceeds 1.0, ACC stops improving, while TPR decreases due to overly broad rules influenced by noisy samples. Therefore, consistent with Eq.(4), the default value is set to 1.0.

## B Matching Table Implementation

As illustrated in Listing 1, features are used as keys for the match ing table, and table entries are processed sequentially according to their assigned priorities. When a match is found, the correspond ing Set\_class action is executed, classifying the sample as either a known attack or benign trafic. If no table entry matches, the Set\_as\_unseen\_attack action is triggered, classifying the sample as an unseen attack. This mechanism ensures that new or unknown trafic is properly flagged for further analysis in the control plane.

```txt
Listing 1: The P4 matching table.
table Helios {
    key = {
    meta.feature_1: range; // Range-based matching
    meta.feature_2: range;
    ...
    meta.feature_m: range;
    }
    actions = {Set_class_1; ..., Set_class_n;} // Hit
    default_action = {Set_as_unseen_attack;} // Miss
}
```

## C Pseudocode of Algorithms

We present the pseudocode for various modules of Helios, includ ing the attack knowledge prototyping module (Algorithm 1), the priority-guided rule transformation module (Algorithm 2), and the class-incremental rule adaptation module (Algorithm 3). These modules collectively enable Helios to achieve high classification performance while maintaining eficient switch reconfiguration.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Attack Knowledge Prototyping
Input: Training set  $D = \{(x_i, y_i)\}_{i=1}^N$ 
Output: Prototypes P, Weight parameters w
1 Run DBSCAN on D to initialize P as cluster centroids;
2  $w \leftarrow 1$ ;
3 for each epoch do
4    for each mini-batch  $\{(x_k, y_k)\}$  in D do
5    $\hat{y}_k \leftarrow \text{Prob}(x_k)$  via Eq.(2);
6    $L \leftarrow \text{Loss}(\hat{y}_k, y_k)$ ;
7    Update P and w using gradients  $\nabla_P L$ ,  $\nabla_w L$ ;
8    end
9 end
10 return P, w;
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Priority-Guided Rule Transformation

Input: Training set  $D = \{(x_i, y_i)\}_{i=1}^N$ 

Output: Range-based matching rules R

1 Initialize prototype-generated rules  $R_{gen}$  as empty;
2  $D_{now} \leftarrow D$ ;
3 for each boosting iteration do
4    $P \leftarrow$  Perform Algorithm 1 on  $D_{now}$ ;
5    for  $P_{ij}$  in P do
6    Compute  $DP_{ij}$  via Eq.(3);
7    Compute Threshold $_{ij}$  via Eq.(4);
8    Compute boundaries ( $L_{ij}, U_{ij}$ ) for  $P_{ij}$  via Eq.(6);
9    Add ( $L_{ij}, U_{ij}$ ) to  $R_{gen}$ ;
10    end
11    Refine the optimal class for all overlapping regions in  $R_{gen}$ ;
12    Perform topological sorting on  $R_{gen}$  and assign priorities;
13    $R_{overlap} \leftarrow$  Introduce regions still not achieve optimal;
14    Prune low cost-effective rules in  $R_{gen}$  and  $R_{overlap}$ ;
15    $D_{now} \leftarrow$  Residual samples of  $D_{now}$  based on  $R_{gen}$  and  $R_{overlap}$ ;
16 end
17  $R_{overlap} \leftarrow$  Overlap refinement and priority assignment on  $R_{gen}$ ;
18  $R \leftarrow R_{gen} \cup R_{overlap}$ ;
19 return R;
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: Class-Incremental Rule Adaptation

Input: Known class samples  $D_{known}$ , new attack samples  $D_{new}$ , rules learned on known class samples  $R_{exist}$ 

1  $D_{update} \leftarrow D_{known} \cup D_{new};$ 

2  $R_{isolate} \leftarrow R_{exist} \setminus \{rules that match any x_k \in D_{new}\};$ 

3  $D_{residual} \leftarrow \{x \in D_{update} \mid x \text{ is misclassified by } R_{isolate}\};$ 

4  $R_{new} \leftarrow Perform Algorithm 2(D_{residual}, R_{exist});$ 

5  $R_{retain} \leftarrow R_{exist} \cap R_{new};$ 

6  $R_{modify} \leftarrow \{r \in R_{retain} \mid priority(r) \neq priority(R_{new})\};$ 

7  $R_{delete} \leftarrow R \setminus R_{retain};$ 

8  $R_{add} \leftarrow R_{new} \setminus R_{retain};$ 

9 Perform the corresponding switch table-entry reconfiguration for  $R_{modify}$ ,  $R_{delete}$  and  $R_{add}$ ;

10 return;
</div>

![](images/a52ba4668eae93e55ebede77b08a6093e13d48e1c8616203314789ae8ce47800.jpg)  
(a) Iterations of boosting

![](images/ce4d3713928e46dccb4904bbb6d127d0b68e0b0de5d9403e589ae9bc128f281e.jpg)  
(b) Lower bound of pruning

![](images/c6f765c1e6a3946e19176fd8b3a88f873debc861a929d290262f614a06bd0b2b.jpg)  
Prune Number<sub>(c)</sub> <sub>Scaling</sub> <sub>weight</sub> <sub>of</sub> <sub>boundary</sub> <sub>calibration</sub>  
Figure 5: Analysis of key hyper-parameters for Helios.

## D Learning Techniques

Supervised Prototypical learning. In prototypical learning [6], a sample is classified into the class of the prototype to which it is most similar in the hidden space. If a sample shows little similarity to any prototype, it is classified as an out-of-distribution (OOD) sample, and therefore considered as belonging to an unseen class. Existing methods [12, 26] typically assign a single prototype to each class, which works well because the features are processed by neural networks, allowing a single prototype to efectively diferentiate between classes with minimal overlap in acceptance ranges.

However, in the context of the data plane, which does not sup port feature processing (e.g., linear or nonlinear transformations), prototypes need to directly compare with original features. Consequently, we assign multiple prototypes to each class to enhance representation capability. However, this introduces new challenges, as the acceptance boundaries for prototypes become dificult to define, and an increase in the number of prototypes can lead to considerable overlaps. We address these issues in Section 4.2.

Boosting. Boosting is a powerful learning technique commonly used in machine learning [7, 14] to enhance model accuracy by iteratively correcting the errors of weak classifiers. At each itera tion, it focuses on the misclassified samples from previous rounds and trains a new model that better captures these challenging in stances. By combining the strengths of multiple weak models, it produces a robust classifier with improved accuracy and general ization. Since Helios is essentially a rule learner, which also acts as a weak classifier, we combine SMPL with boosting to further enhance classification performance.

## E Dataset Details

Table 3 presents the attack classes assigned to each task across datasets. Initially, each dataset begins with benign trafic and a sin gle attack. As tasks progress, additional attack classes are introduced incrementally, simulating a continually evolving network environ ment. This incremental setup efectively evaluates the methods ability to handle both known classes and newly emerging threats, reflecting the attack-incremental nature of real-world scenarios.

Table 4 presents the extracted trafic features used in our experiments. For UNSW-NB15, we extract features across various levels, including IPv4 (e.g., length, flags, TTL, protocol, and ports), TCP (e.g., ofset, flags, and window size), and UDP (e.g., length).

If a packet is of the TCP type, the UDP fields are padded with zeros, and vice versa. For TON-IoT, features such as total packet size and inter-arrival time are considered, with average, maximum, and minimum values captured to characterize the flow. Additionally, packet-level attributes such as packet count, protocol, and destination port are included. For CICIDS2018, flow-level features such as forward and backward packet sizes are extracted, along with packet-level attributes.

Table 3: Task-specific class details for each dataset.

<table><tr><td>Task</td><td>CICIDS2018</td><td>TON-IoT</td><td>UNSW-NB15</td></tr><tr><td>Init</td><td>Benign</td><td>Benign</td><td>Benign</td></tr><tr><td>Init</td><td>DDoS LOIC HTTP</td><td>Mitm</td><td>Analysis</td></tr><tr><td>1</td><td>DDoS HOIC</td><td>DoS</td><td>Worms</td></tr><tr><td>2</td><td>DDoS LOIC UDP</td><td>Runsomware</td><td>Backdoor</td></tr><tr><td>3</td><td>DoS GoldenEye</td><td>Backdoor</td><td>DoS</td></tr><tr><td>4</td><td>DoS Hulk</td><td>Injection</td><td>Exploits</td></tr><tr><td>5</td><td>DoS Slowloris</td><td>DDoS</td><td>Fuzzers</td></tr><tr><td>6</td><td>SSH BruteForce</td><td>Password</td><td>Generic</td></tr><tr><td>7</td><td>Web Attack XSS</td><td>Scanning</td><td>Reconnaissance</td></tr><tr><td>8</td><td>Web Attack SQL</td><td>XSS</td><td>Shellcode</td></tr><tr><td>9</td><td>Web Attack Brute Force</td><td>-</td><td>-</td></tr></table>

Table 4: Detailed features extracted from diferent fields, including both packet-level and flow-level features.

<table><tr><td>Dataset</td><td>Field</td><td>Features</td></tr><tr><td rowspan="3">NB15</td><td>IPv4</td><td>length, flags, TTL, protocol, sr-cport, dstport</td></tr><tr><td>TCP</td><td>offset, flags, window_size</td></tr><tr><td>UDP</td><td>length</td></tr><tr><td rowspan="3">IoT</td><td>Total Packet Size</td><td>avg, max, min</td></tr><tr><td>Inter-Arrival Time</td><td>avg, max, min</td></tr><tr><td>Packet-Level</td><td>pkt_count, protocol, dstport</td></tr><tr><td rowspan="3">IDS</td><td>Forward Packet Size</td><td>avg, max, min</td></tr><tr><td>Backward Packet Size</td><td>avg, max, min</td></tr><tr><td>Packet-Level</td><td>pkt_count, protocol</td></tr></table>
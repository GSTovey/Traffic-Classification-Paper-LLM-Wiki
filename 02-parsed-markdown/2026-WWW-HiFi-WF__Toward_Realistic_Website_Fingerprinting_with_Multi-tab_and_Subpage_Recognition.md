# HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition

Songyang Wu Nanjing University of Science and Technology Nanjing, Jiangsu, China wusongyang@njust.edu.cn

Long Yuan Wuhan University of Technology Wuhan, Hubei, China longyuan@whut.edu.cn

Chuan Ma<sup>∗</sup> Chongqing University Chongqing, China chuan.ma@cqu.edu.cn

Biwen Chen Chongqing University Chongqing, China macrochen@cqu.edu.cn

Tao Xiang Chongqing University Chongqing, China txiang@cqu.edu.cn

Ming Ding Data 61, CSIRO, Sydney Sydney, Australia ming.ding@data61.csiro.au

Yuwen Qian Nanjing University of Science and Technology Nanjing, Jiangsu, China admon@njust.edu.cn

## Abstract

Website Fingerprinting (WF) is an emerging trafic analysis technique that enables a passive adversary to infer which websites a user visits. However, most existing studies, whether in single tab or multi-tab settings, rely on the unrealistic assumption that users only access website homepages, diverging significantly from real-world browsing behavior. Even recent works extending WF to subpages primarily focus on website-level identification, with out distinguishing which specific subpages are visited, thereby limiting the attack’s granularity and scope. In this paper, we propose HiFi-WF (Hierarchical Fine-grained Website Fingerprinting), a novel framework that breaks the homepage-only assumption and extends WF to multi-tab recognition and fine-grained subpage identification. We formulate the task as a hierarchical multi-label classification problem, jointly modeling the distinctions and correlations between homepages and subpages. To this end, HiFi-WF integrates a unified CNN-based extractor and layered encoder with a Feature Interaction Module based on multi-head cross-attention to capture inter-level dependencies. An Enhanced SubHead enforces hierarchical constraints to suppress invalid subpage predictions, while a cascaded channel–spatial attention mechanism refines discriminative features for precise hierarchical identification. Experi mental results demonstrate that HiFi-WF achieves state-of-the-art performance at both hierarchical levels, attaining F1-scores of 92.1% (homepage) and 81.9% (subpage), thereby validating its efective ness in advancing WF attacks toward realistic, fine-grained, and multi-tab browsing scenarios. Related codes and datasets can be found in https://github.com/wusongyang02-blip/HiFi-WF.

## CCS Concepts

• Security and privacy → Security services; • Networks → Network privacy and anonymity.

## Keywords

Multi-tab Website Fingerprinting, Deep Learning, Hierarchical Multi task Learning, Tor

## ACM Reference Format:

Songyang Wu, Chuan Ma, Ming Ding, Long Yuan, Biwen Chen, Yuwen Qian, and Tao Xiang. 2026. HiFi-WF: Toward Realistic Website Fingerprinting with Multi-tab and Subpage Recognition. In Proceedings ofthe ACM Web Conference 2026 (WWW ’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3774904.3792412

## 1 Introduction

Nowadays, web browsers have become one of the most ubiquitous tools for accessing the Internet. However, browsing activities often leave discernible traces that may compromise user privacy. Despite the ongoing advancement of privacy-enhancing technologies, the risk of information leakage remains non-negligible due to the rapid development of techniques such as Website Fingerprinting (WF). These methods are capable of circumventing existing protections to infer a user’s browsing behavior, thereby posing a substantial and escalating threat to personal privacy and security. Although the Tor network (The Onion Router), currently the most widely used anonymity system, forwards trafic through multiple relays and reshapes packets into uniform sizes, website fingerprinting techniques can still determine which websites a user visits by training models to extract distinguishing trafic patterns from the encrypted data streams [10].

With the rapid advancement of deep learning, Website Finger printing (WF) attacks have demonstrated striking accuracy [1, 6, 17, 26, 28, 31]. However, most existing studies remain confined to simplified scenarios that analyze trafic from single websites, typically restricted to their homepages, an assumption that diverges sharply from real-world browsing behavior. Although several stud ies [8, 14, 16, 18, 33] have extended WF to mixed trafic from multi ple websites, these works still treat homepages as the sole represen tative of each site. Recent eforts have begun to explore subpage trafic, but only in constrained settings where trafic consists of mixtures of subpages from the same site. Crucially, these methods remain at website-level identification and do not enable fine-grained recognition of which subpage was visited. Subpage-level WF raises greater privacy and ethical risks, as it can infer more fine-grained user interests and intentions, potentially remaining efective even in anonymity systems like Tor due to persistent trafic metadata [24]. This gap is significant because subpages exhibit substantially greater structural and content diversity than homepages, and visits are often driven by specific interests (e.g., a product page or a news article). Without modeling this diversity, WF attacks face greater uncertainty when inferring both the website and the exact subpage.

To empirically validate the significance of subpage-level identifi cation highlighted above, we conducted experiments to examine how well existing WF models generalize beyond homepage traffic. We collected trafic traces from the homepages and selected subpages of 50 websites. Using homepage data for training, we evaluated three state-of-the-art WF models: DF [28], Var-CNN [3], and RF [27], on two test sets: one comprising homepage traces and the other consisting of subpage traces. As shown in Figure 1, all models maintained high accuracy on homepages but dropped sharply on subpages. Notably, RF, despite being recognized for its robustness, experienced an accuracy reduction of approximately 35%. Furthermore, employing a ’Homepage + Subpage’ multi-tab mixed trafic dataset for both training and testing, we observe that the model still exhibits substantial performance disparities between homepage and subpage classifications. These findings empirically demonstrate that models trained exclusively on homepage trafic fail to generalize efectively to subpage scenarios, highlighting a critical limitation in current WF approaches.

![](images/d18077b3ccb991dbc58b24501fd3fb1ce6d6f6089e6f31aebbd1c4cb4ebf195a.jpg)  
Figure 1: Comparison of WF Attacks on Homepage and Sub page for Accuracy in Single Table Scenario (Left) and F1-Score in Two Table Scenario (Right).

To extend the scope of existing WF attacks and address the gap in targeting subpages, we propose HiFi-WF (Hierarchical Finegrained Website Fingerprinting). Its core idea is to formulate the classification ofwebsites containing subpage trafic as a hierarchical multi-label classification problem. Specifically, we treat the website as a main label and its subpages as sub-labels belonging to that main label. The goal of HiFi-WF is not only to identify which websites are present in mixed trafic but also to recognize the subpages associated with these websites. We softly partition the trafic features into two components, focusing on homepages and subpages respectively, and design an improved cross-interactive attention mechanism that allows homepages and subpages to interact with each other both as subjects and objects. By leveraging the distinctions and relationships between main pages and subpages to the fullest extent, we can accurately identify not only the websites but also their corresponding subpages.

The main contributions of this paper are as follows:

• We propose HiFi-WF, the first website fingerprinting attack designed for multi-label websites and their subpages. By leveraging the feature interactions between website homepages and subpages to capture their distinctions and underlying relationships, our method enables hierarchical multilabel classification of both homepages and subpages.

• We designed a novel cross-attention mechanism for HiFi-WF to facilitate fine-grained hierarchical feature learning. After feature extraction via the CNN, dual lightweight attention modules are applied to enhance the representations, which are then softly partitioned into homepage- and subpagebiased features. These two representations interact through a cross-attention-based feature interaction module, allowing mutual information exchange. Through this bidirectional fusion, HiFi-WF derives highly discriminative, hierarchically structured features, enabling precise recognition of both website- and subpage-level labels.

• We constructed and released the first hierarchical multi-label dataset incorporating subpage trafic, containing over 40,000 samples, each annotated with both main and sub-labels across Chrome and Tor browsers. We then evaluated HiFi-WF on this dataset under both 2-tab and 3-tab website-level identification settings, and our model consistently outperformed all baselines. When extending all baseline methods with suitable subpage classifiers for page-level identification, where subpage recognition becomes essential, HiFi-WF achieved an F1-score of 81.9% in the 2-tab scenario, dramatically surpassing the best baseline [18], which attained only about 10%.

## 2 Background

## 2.1 Threat Model

We adopt a threat model consistent with prior web trafic analysis studies [2, 8, 15, 19, 31, 32], in which the adversary is modeled as a local passive eavesdropper situated along the communication path between the user’s device and the web server. This adversary can monitor and record trafic but lacks active capabilities such as modifying, injecting, deleting, delaying, or decrypting packets. In the baseline scenario, its objective is to determine whether the user is visiting a monitored website and, if so, to identify which one. To bridge the granularity gap in existing models, which typically overlook distinctions among pages within the same site, we extend the framework to a finer-grained setting. As illustrated in Figure 2, the eavesdropper now seeks not only to identify websites but also to diferentiate between specific pages (e.g., homepages and subpages). To more accurately reflect real-world browsing patterns, we collected trafic traces from both homepages and a representative selection of subpages, incorporating continuous sequences that span navigation between them to better emulate natural user browsing behavior (details provided in Section 4.1).

![](images/78b6370a249eca5a5b342475aed3a81a4cca6705d4a4afc5bf330349d4d01ea2.jpg)  
Figure 2: Threat Model of HiFi-WF.

## 2.2 WF Attacks

Single-tab WF Attacks. The study of website fingerprinting (WF) traces back to 1996, when Wagner and Schneier [30] first observed that packet length sequences could leak information from encrypted trafic [4]. As deep learning (DL) advanced, it began to reshape WF research. Abe and Goto [1] pioneered the use of DL in this domain with a stacked denoising autoencoder (SDAE). Their approach demonstrated exceptional performance in the closed-world setting, showing that website fingerprinting could bypass the need for labor-intensive manual feature engineering by relying on models to automatically learn feature representations directly from raw data.

Sirinam et al. [28] subsequently introduced Deep Fingerprint ing (DF), a convolutional neural network (CNN) architecture that used multi-layer convolutional blocks to capture richer trafic fea tures, attaining state-of-the-art results in both closed-world and open-world settings. To reduce the dependence on large datasets, Bhat et al. [3] proposed Var-CNN, which incorporated a ResNet-18 backbone to widen the receptive field and improve learning eficiency. Notably, Var-CNN achieved high performance with limited training samples, mitigating a key constraint of earlier DL-based WF attacks; yet, in response to a new set of challenges posed by in creasingly sophisticated WF defences, Shen et al. [27] proposed RF, which enhances attack resilience against defensive noise through time-frequency analysis, significantly improving robustness and accuracy under strong protection. Furthermore, website content in the real world undergoes frequent updates—a phenomenon known as concept drift. Several recent studies [5, 9, 11, 12, 21, 35] have sought to address this challenge, bringing WF attacks closer to practical deployment.

Multi-tab WF Attacks. To more accurately simulate real user browsing behavior, a growing body of research has begun to focus on multi-tab website fingerprinting attacks, as users generally do not visit only one website in a single browsing session. Recent studies [8, 14, 18, 33, 34, 36, 37] have leveraged the Transformer architecture to extract both global and local patterns in trafic, enabling the model to perform well even when faced with complex mixed trafic, achieving a significant leap from single-tab to multitab identification.

However, both single-tab and multi-tab website fingerprinting attacks treat the homepage as representative trafic of a website, neglecting subpage trafic. Deng et al. noted this issue and collected real-world 5-tab subpage trafic in [8], where trafic from diferent subpages of the same website was assigned the same label for multi-tab classification. In more recent work, Mitseva and Panchenko [24] treated multiple subpages of a website as mixed trafic for single-label website fingerprinting. Nevertheless, current preliminary attempts to address this challenge sufer from fundamental limitations. Such an approach compromises the model’s ability to learn distinctive features by forcing it to acquire a blurred and "averaged" representation of website characteristics, thereby sacrificing critical discriminative information. This issue becomes particularly pronounced when trafic from diferent subpages of various websites is interwoven, leading to a significant decline in identification accuracy.

Crucially, subpage-level identification amplifies privacy risks: beyond revealing which websites a user visits, it enables attackers to infer specific behaviors, personal interests, and even intentions, representing a far more severe threat to user privacy.Specifically, such fine granularity goes beyond coarse website-level tracking and can expose sensitive user intentions. This form of inference undermines informational autonomy, a widely recognized privacy principle, by revealing personal attributes that users may not intend to disclose. In contrast to traditional website-level WF, subpagelevel attacks can circumvent common privacy protections such as cookie blocking and may remain efective even in anonymous networks (e.g., Tor), since trafic patterns characterized by packet timing and size can still be distinguishable. This observation is consistent with Bacis et al. [2], who argue that fine-grained WF substantially increases privacy harm by enabling targeted exploitation, including price discrimination and phishing.

Technically, this task is considerably more challenging than conventional website-level fingerprinting. Models must simultaneously distinguish between a vast number of subpages within the same site, introducing substantial intra-class variability, and diferentiate between highly similar subpages across diferent sites, posing finegrained inter-class ambiguity. Moreover, the inherent hierarchical relationship between websites and their subpages further complicates feature learning, rendering traditional flat or single-label architectures inadequate. Addressing these intertwined challenges requires a model capable of capturing multi-level dependencies, balancing coarse-grained website recognition with fine-grained subpage discrimination. To this end, we propose a hierarchical multi-label fingerprinting framework that explicitly models these dependencies, enabling robust and accurate identification across both website and subpage levels.

![](images/4d8c0e2dc00b5d54f7f800e4428710234bf0f0e5cedcafef94b953f0c48ed5aa.jpg)  
Figure 3: The overview of HiFi-WF.

## 3 Methodology

This section presents the architecture and detailed design of HiFi-WF. Prior to delving into its individual components, we first provide an overview of the entire system.

## 3.1 Overview

As illustrated in Figure 3, HiFi-WF is a hierarchical webpage fin gerprinting framework that integrates four tightly coupled compo nents to achieve fine-grained and robust trafic analysis. It begins with a novel two-row trafic representation that explicitly separates outgoing and incoming packets, preserving precise size and timing information to facilitate direction-aware feature learning. A feature processor then extracts and refines these signals through a CNN-based extractor and a dual-attention enhancer, capturing both temporal dependencies and salient discriminative cues. To address the overlap and imbalance between homepage and subpage patterns, a dual-path segmentation and hierarchical feature interaction module softly partitions features into homepage- and subpage-oriented streams and models their dependencies through self-attention, yielding enriched hierarchical representations. Finally, a dual-path classifier leverages mutually enhanced features for homepage recognition and employs hierarchical constraints to guide subpage prediction, ensuring consistency and improving accuracy. Collectively, these innovations enable HiFi-WF to deliver state-of-the-art performance in hierarchical webpage identification while efectively handling the complexity of real-world trafic.

## 3.2 Data Preprocess

Inspired by the Trafic Aggregation Matrix (TAM) [27], we propose a novel two-row matrix representation for trafic data. As illustrated in Figure 4, packet sizes are arranged chronologically, with the first row containing outgoing packets and the second row containing incoming packets. Each column includes at least one zero, indicating the absence of a packet in that direction at a given timestep.

Unlike TAM, which aggregates packets into bins for statistical analysis, our approach preserves the exact sequential sizes and timings of individual packets. This precise representation enables the model to capture fine-grained information, at the expense of the robustness ofered by aggregation-based methods. By explicitly separating trafic directions, the model avoids decoding combined sign-value representations and allows the convolutional network to eficiently learn direction-specific features or their interdependencies, enhancing both learning eficiency and hierarchical webpage identification performance. Specific implementation details are described in Appendix A.

## 3.3 Design of HiFi-WF

The HiFi-WF model is primarily composed of four key components: Feature Processor, Dual-Path Segmentation, Hierarchical Feature Interaction, and Dual-Path Classifier.

Feature Processor. The core of HiFi-WF lies in a specialized Feature Processor that integrates two synergistic modules: a CNNbased Feature Extractor and a Dual-Attention Feature Enhancer. Together, they are designed to capture both fine-grained trafic pat terns and contextual dependencies critical for hierarchical website fingerprinting.

Unlike prior works that rely solely on CNNs or temporal models[16, 23, 28], our framework first exploits a two-channel temporal representation of network trafic, explicitly separating outgoing and incoming packet sequences. This structured input allows the CNNbased extractor to eficiently learn direction-specific features while simultaneously modeling interdependencies across trafic flows. By progressively reducing temporal resolution and expanding channel dimensions, the extractor constructs a compact yet expressive representation that preserves both directionality and sequential dynamics. To overcome the limitations of conventional CNN features, which often treat all channels and time steps uniformly, we introduce a two-stage Dual-Attention Enhancer. The channel attention module adaptively prioritizes the most informative feature maps, while the temporal attention module identifies critical time steps that carry discriminative cues. This design explicitly answers both what features are important and when they matter, enabling the model to capture long-range temporal dependencies without sacrificing local detail. By combining directional CNN feature learning with dual-stage attention refinement, HiFi-WF achieves stronger discriminability and generalization than existing WF architectures, particularly in complex multi-site and subpage recognition tasks.

Dual-Path Segmentation. Although enhanced feature maps are available, distinguishing between main and sub-websites remains challenging due to two factors: (i) the number of subpages is far greater than homepages, leading to label sparsity and data imbalance; and (ii) their features largely overlap in the representation space, making them non-separable. To address these issues, we design a Dual-Path Segmentation module that performs soft segmentation of features rather than rigid, label-based partitioning.

The module employs a lightweight attention mechanism to adap tively generate two sets of weights, highlighting temporal regions most indicative of homepages or subpages. This produces two spe cialized feature maps, $\mathbf { F } _ { \mathrm { m a i n } }$ and $\mathbf { F _ { \mathrm { { s u b } } } } .$ each biased toward its re spective classification task, while preserving the overall structural integrity of the original features. This soft, adaptive separation alleviates data imbalance and overlapping-feature challenges, providing more discriminative signals for subsequent processing (An illustration example is provided in Figure 5 in the Appendix B).

Hierarchical Feature Interaction. To exploit dependencies between homepages and subpages, we introduce a Hierarchical Feature Interaction module. The specialized feature maps (Fmain and Fsub) are projected into a shared semantic space and compressed into one-dimensional vectors. These are then processed with a multi-head self-attention mechanism [29]:

$$
\mathrm{Attention} (Q, K, V) = \mathrm{softmax} \left(\frac {Q K ^ {T}}{\sqrt {d _ {k}}}\right) V,\tag{1}
$$

where $Q , K ,$ and � represent the query, key, and value matrices derived from the combined feature representations, and $d _ { k }$ is the dimension of the key vectors.

Through this process, the module enables each category-specific feature to adaptively attend to and integrate information from both main and sub-categories, resulting in more robust and informative representations for downstream classification.

Dual-Path Classifier. HiFi-WF introduces a parallel dual-branch classifier tailored for hierarchical webpage identification, featuring dedicated classification heads for both homepage and subpage prediction. This architecture operates upon enriched feature rep resentations derived from cross-modal interactions between main page and subpage features, thereby enabling a more profound and holistic contextual comprehension.

For homepage classification, the framework employs two independent MLP-based classifiers, each processing mutually enhanced feature representations. The first classifier attends to mainpage fea tures enriched with subpage contextual signals, while the second focuses on subpage features augmented with mainpage context. This dual-perspective design allows homepage predictions to harness complementary information from both page levels, with their outputs subsequently integrated through a fusion mechanism to yield a robust and context-aware homepage classification. For sub page classification, a parallel structure is employed, augmented with a hierarchical constraint mechanism. Each subpage classifier incor porates preliminary homepage predictions via parent-information injection layers, explicitly encoding the dependencies between hierarchical categories. Furthermore, dynamically generated constraint masks, derived from homepage outputs, are applied to refine sub page predictions, thereby enforcing logical coherence across the hierarchy. This refined mechanism not only enhances predictive accuracy but also alleviates challenges posed by data imbalance, as reliable homepage predictions serve to guide and constrain the more intricate task of fine-grained subpage recognition. Altogether, the Dual-Path Classifier confers significant advantages in navigating the intricacies of hierarchical webpage structures, where the symbiotic interplay between homepage and subpage content provides indispensable contextual cues for precise and consistent classification.

Due to space constraints, the details of the workflow are elaborated in Appendix B.

## 4 Experimental Evaluation

## 4.1 Datasets

In the current context where no suitable public datasets are available for subpage WF research, we have created and released the first real-world dataset containing trafic data for both homepages and their corresponding subpages, encompassing over 40,000 web page access records on the Chrome and Tor browsers. More details about the dataset are provided in the link provided in the abstract and Appendix C.

## 4.2 Experimental Setup

4.2.1 Baseline. For a comprehensive and fair comparison, we selected six representative attack methods. This includes three models originally designed for single-tab trafic analysis (DF [28], Var-CNN [3], and RF [27]) and three models designed for multi-tab trafic (BAPM [14], ARES [8], and TMWF [18]). To ensure fairness, all models were evaluated under the same multi-tab scenario. Consequently, we adapted the three single-tab models by extending them into their multi-tab counterparts, referred to as Multi-DF, Multi-VarCNN, and Multi-RF, based on the code provided by Deng et al. [7]. To enable subpage-level evaluation, we further enhanced all the aforementioned baseline models by replacing their classification heads with a dual-head structure comprising a main classifier and a sub-classifier.

4.2.2 Metrics. In a closed-world website fingerprinting attack, traffic traces involving multiple simultaneously open websites (i.e., multi-tab trafic) formulate the problem as a multi-label, multi-class classification task. For model performance evaluation, we adopted metrics specifically tailored to multi-label classification, including Precision at K (P@K) and Mean Average Precision at K (MAP@K). These are complemented by traditional metrics (Precision, Recall, and F1-score) to ensure a comprehensive assessment. Furthermore, as detailed in Section 4.4, these metrics are categorized into homepage-level and subpage-level metrics. This dual perspective allows us to evaluate the model’s ability to simultaneously identify both homepages and their corresponding subpages. A detailed description is provided in Appendix D.

## 4.3 WF Attacks in the Close World without Subpage Attacks

In this experiment, we first evaluate HiFi-WF on classifying websites against Multi-DF [28], Multi-VarCNN [3], Multi-RF [27], BAPM [14], ARES [8], and TMWF [18].

Table 1: Two-Table without subpage attack

<table><tr><td>Attacks</td><td>Precision</td><td>Recall</td><td>F1-Score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>Multi-DF</td><td>0.651</td><td>0.782</td><td>0.711</td><td>0.805</td><td>0.799</td></tr><tr><td>Multi-VarCNN</td><td>0.903</td><td>0.765</td><td>0.828</td><td>0.822</td><td>0.815</td></tr><tr><td>BAPM</td><td>0.682</td><td>0.753</td><td>0.716</td><td>0.699</td><td>0.826</td></tr><tr><td>ARES</td><td>0.946</td><td>0.779</td><td>0.854</td><td>0.822</td><td>0.819</td></tr><tr><td>TMWF</td><td>0.886</td><td>0.798</td><td>0.840</td><td>0.829</td><td>0.821</td></tr><tr><td>Multi-RF</td><td>0.951</td><td>0.788</td><td>0.862</td><td>0.853</td><td>0.852</td></tr><tr><td>HiFi-WF (Ours)</td><td>0.956</td><td>0.817</td><td>0.881</td><td>0.863</td><td>0.861</td></tr></table>

We first evaluate model performance in the 2-tab scenario. As summarized in Table 1, among existing methods, the Multi-RF model, with its deep convolutional architecture and efective feature extraction modules, achieves competitive performance, reaching an F1-Score of 86.2%. In contrast, the proposed HiFi-WF achieves the highest scores across all evaluation metrics. Specifically, HiFi-WF attains a recall of 81.7%, making it the only method to surpass 80% in this measure, while also achieving the best P@2 and MAP@2 scores, both exceeding 86%. These results demonstrate the model’s strong capability in accurate classification and efective ranking. We attribute this performance to HiFi-WF’s robust handling of long trafic sequences and its hierarchical dual-path architecture, which jointly captures and utilizes both homepage and subpage feature interactions to enhance main website recognition.

## 4.4 WF Attacks in the Close World with Subpage Attacks

Since previous experiments did not involve recognizing subpages within websites, we extended all baseline methods by replacing their standard classification heads with hierarchical ones, consist ing of both a main-label and a sub-label classifier, to enable a fair comparison. In this experiment, we therefore evaluate each model’s ability to jointly identify both websites and their corresponding subpages. Moreover, we propose a Hierarchical Focal Loss function, derived from the conventional Focal Loss [22], which enforces consistency between main and sub-label predictions while mitigating the impact of sparse positive samples. To ensure fairness, all baseline WF attack models are retrained using this Hierarchical Focal Loss as the unified objective. Detailed formulations and implementation details are provided in Appendix E.

Two-table evaluation (recognizing subpages). As shown in Table 2, our method achieves outstanding performance in both main page and subpage identification under the two-tab scenario. For the main page recognition, HiFi-WF attains an F1-Score of 92.1%, representing a 37% relative improvement over the best baseline (TMWF, 67.4%). The improvement is even more pronounced in subpage identification, where HiFi-WF achieves an F1-Score of 81.9%, over eight times higher than TMWF’s 9.8%, corresponding to a relative gain of over 730%. HiFi-WF also obtains the highest scores in ranking metrics, with P@2 and MAP@2 reaching 91.5%, 91.3% for homepages and 81.0%, 79.1% for subpages, nearly matching TMWF’s 81.4% and 80.2%, highlighting strong top-ranking capability.

These significant gains can be attributed to HiFi-WF’s hierarchi cal interaction mechanism, which explicitly models dependencies between main pages and subpages. The feature interaction module enables mutual refinement of features across levels, while hierarchical prediction uses main page predictions to guide subpage identification, efectively leveraging structural priors in the data. In contrast, baseline models treat the two tasks independently, lacking interactivity and thus failing to handle severe data sparsity and class imbalance at the subpage level. As a result, their subpage identification performance falls far short of HiFi-WF’s. These results underscore the importance of explicit hierarchical modeling for fine-grained website fingerprinting.

Three-table evaluation. We also evaluated the attack capability of each model in a 3-tab scenario. As shown in Table 2, compared to the 2-tab scenario, the performance of all models declined. This decline is expected, as the interleaving of trafic from the main pages and sub-pages of three websites undoubtedly presents a significantly greater challenge. While HiFi-WF demonstrates superior performance across most metrics, particularly in subpage recognition, where it significantly outperforms all baselines, we observe that TMWF achieves marginally higher P@3 and MAP@3 on homepage classification in the 3-tab scenario. This slight diference can be attributed to HiFi-WF’s design prioritization: We prioritize hierarchical consistency and subpage accuracy since they are critical for inferring user intentions, which naturally involves more complex feature interactions that may slightly dilute the confidence ranking for top-K homepage predictions. Therefore, F1-score is the key metric in our setting. HiFi-WF achieves SOTA F1-score for both homepages and subpages, while its slightly lower P@k/MAP@k is acceptable. Moreover, in the two-homepage segment, we obtain the best, while the subpage is only about 1% below SOTA(TMWF).

Tor datasets evaluation. As shown in Table 3, HiFi-WF achieves leading performance across key classification metrics—Precision, Recall, and F1-score—for both homepages and subpages, while TMWF performs better in ranking-based metrics (P@2 and MAP@2). This divergence stems from TMWF’s single-branch design and loss optimization prioritize ranking the most confident predictions rather than ensuring comprehensive classification. Consequently, it achieves higher top-ranked accuracy but lower overall recall and consistency, as many correct low-confidence samples are excluded. In contrast, HiFi-WF adopts a balanced strategy emphasizing classification completeness and hierarchical consistency, thereby achieving superior overall accuracy despite slightly lower ranking-oriented scores.

## 4.5 Open World Evaluation

To evaluate the proposed model’s performance in open-world website fingerprinting scenarios, where the key challenges include accurately identifying monitored websites, efectively rejecting unmonitored ones, and distinguishing fine-grained diferences between main and subpages, we adopt a carefully designed data-splitting strategy. Specifically, the training set comprises 70% of the 2-tab SP-MA dataset and 30% of open-world data, allowing the model to learn both the feature distributions of known classes and the decision boundary between known and unknown classes. The remaining data are divided into validation and test sets to emulate the data distribution of realistic open-world environments. Evaluation is conducted using three key metrics: $\mathrm { A U C } _ { M }$ and $\mathrm { A U C } _ { N }$ for assessing open-world identification and rejection capabilities, and MAP@2 for measuring fine-grained classification performance across main and subpages.

Table 2: Performance of Website Fingerprinting Attacks on Homepages and Subpages under two-table and three-table Scenarios

<table><tr><td rowspan="2">Attacks</td><td rowspan="2">Scenario</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@k</td><td>MAP@k</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@k</td><td>MAP@k</td></tr><tr><td rowspan="2">Multi-DF [7]</td><td>2-tab</td><td>0.671</td><td>0.669</td><td>0.662</td><td>0.898</td><td>0.891</td><td>0.094</td><td>0.094</td><td>0.094</td><td>0.746</td><td>0.728</td></tr><tr><td>3-tab</td><td>0.598</td><td>0.504</td><td>0.547</td><td>0.754</td><td>0.746</td><td>0.077</td><td>0.076</td><td>0.076</td><td>0.577</td><td>0.535</td></tr><tr><td rowspan="2">Multi-VarCNN [7]</td><td>2-tab</td><td>0.670</td><td>0.669</td><td>0.662</td><td>0.918</td><td>0.912</td><td>0.095</td><td>0.094</td><td>0.094</td><td>0.725</td><td>0.742</td></tr><tr><td>3-tab</td><td>0.533</td><td>0.437</td><td>0.456</td><td>0.645</td><td>0.613</td><td>0.059</td><td>0.057</td><td>0.057</td><td>0.426</td><td>0.380</td></tr><tr><td rowspan="2">BAPM [14]</td><td>2-tab</td><td>0.541</td><td>0.546</td><td>0.524</td><td>0.745</td><td>0.732</td><td>0.011</td><td>0.012</td><td>0.011</td><td>0.023</td><td>0.019</td></tr><tr><td>3-tab</td><td>0.449</td><td>0.387</td><td>0.391</td><td>0.568</td><td>0.522</td><td>0.007</td><td>0.008</td><td>0.007</td><td>0.015</td><td>0.011</td></tr><tr><td rowspan="2">ARES [8]</td><td>2-tab</td><td>0.661</td><td>0.658</td><td>0.651</td><td>0.901</td><td>0.897</td><td>0.090</td><td>0.090</td><td>0.090</td><td>0.731</td><td>0.714</td></tr><tr><td>3-tab</td><td>0.616</td><td>0.501</td><td>0.531</td><td>0.802</td><td>0.782</td><td>0.084</td><td>0.081</td><td>0.820</td><td>0.689</td><td>0.650</td></tr><tr><td rowspan="2">TMWF [18]</td><td>2-tab</td><td>0.680</td><td>0.680</td><td>0.674</td><td>0.910</td><td>0.908</td><td>0.099</td><td>0.098</td><td>0.098</td><td>0.814</td><td>0.802</td></tr><tr><td>3-tab</td><td>0.644</td><td>0.517</td><td>0.553</td><td>0.864</td><td>0.852</td><td>0.091</td><td>0.089</td><td>0.089</td><td>0.708</td><td>0.694</td></tr><tr><td rowspan="2">Multi-RF [7]</td><td>2-tab</td><td>0.539</td><td>0.536</td><td>0.518</td><td>0.733</td><td>0.715</td><td>0.046</td><td>0.047</td><td>0.046</td><td>0.326</td><td>0.287</td></tr><tr><td>3-tab</td><td>0.298</td><td>0.287</td><td>0.267</td><td>0.411</td><td>0.357</td><td>0.015</td><td>0.016</td><td>0.015</td><td>0.103</td><td>0.072</td></tr><tr><td rowspan="2">HiFi-WF (Ours)</td><td>2-tab</td><td>0.954</td><td>0.879</td><td>0.915</td><td>0.915</td><td>0.913</td><td>0.853</td><td>0.775</td><td>0.819</td><td>0.810</td><td>0.791</td></tr><tr><td>3-tab</td><td>0.798</td><td>0.719</td><td>0.757</td><td>0.771</td><td>0.754</td><td>0.806</td><td>0.628</td><td>0.706</td><td>0.712</td><td>0.685</td></tr></table>

Table 3: Performance of Multi-tab Website Fingerprinting Attacks on Homepages and Subpages with Tor Datasets

<table><tr><td rowspan="2">Attacks</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>ARES</td><td>0.317</td><td>0.319</td><td>0.295</td><td>0.510</td><td>0.481</td><td>0.035</td><td>0.036</td><td>0.035</td><td>0.306</td><td>0.284</td></tr><tr><td>TMWF</td><td>0.450</td><td>0.454</td><td>0.436</td><td>0.729</td><td>0.714</td><td>0.058</td><td>0.059</td><td>0.058</td><td>0.495</td><td>0.460</td></tr><tr><td>HiFi-WF (Ours)</td><td>0.545</td><td>0.531</td><td>0.538</td><td>0.539</td><td>0.512</td><td>0.475</td><td>0.347</td><td>0.401</td><td>0.415</td><td>0.395</td></tr></table>

Table 4: Comparison of WF Attacks on Homepages and Sub pages in 2-tab Open-world Scenario

<table><tr><td>Attacks</td><td> $AUC_M$ </td><td> $AUC_N$ </td><td>MAP@2 (Homepage)</td><td>MAP@2 (Subpage)</td></tr><tr><td>Multi-DF</td><td>0.998</td><td>0.998</td><td>0.238</td><td>0.179</td></tr><tr><td>Multi-VarCNN</td><td>0.998</td><td>0.998</td><td>0.237</td><td>0.177</td></tr><tr><td>BAPM</td><td>0.901</td><td>0.899</td><td>0.206</td><td>0.007</td></tr><tr><td>ARES</td><td>0.996</td><td>0.996</td><td>0.232</td><td>0.177</td></tr><tr><td>TMWF</td><td>0.997</td><td>0.997</td><td>0.246</td><td>0.206</td></tr><tr><td>Multi-RF</td><td>0.957</td><td>0.957</td><td>0.151</td><td>0.069</td></tr><tr><td>HiFi-WF(Ours)</td><td>0.997</td><td>0.997</td><td>0.906</td><td>0.708</td></tr></table>

As shown in Table 4, all models achieved consistently outstanding performance in terms of both $\mathrm { A U C } _ { M }$ and $\mathsf { A U C } _ { N } ,$ while BAPM and Multi-RF, although achieving approximately 90% and 95% respectively, still fall short compared to other models, all of which exceed 99% in both $\mathsf { A U C } _ { M }$ and $\operatorname { A U C } _ { N }$ . This can be attributed to BAPM’s relatively weak feature extraction module and Multi-RF’s limited ability to capture temporal dependencies. Notably, our model significantly outperforms all others in the open-world sce nario, achieving the best MAP@2 scores of 90.6% on homepages and 70.8% on subpages. The experimental results demonstrate that

HiFi-WF can accurately identify the websites visited by users, even when those websites are previously unknown.

## 4.6 Evaluation under WF Defense

Although our method requires the extraction of fine-grained features to achieve subpage identification, this could potentially reduce HiFi-WF’s robustness against noise from WF defenses. We have accordingly conducted an empirical evaluation of the model’s performance under such defenses. We evaluated the performance of HiFi-WF in a 2-tab scenario under the defense methods of random [25], WTFPAD [20], and Front [13]. As shown in Table 5, although HiFi-WF experiences a performance decline when confronted with defense methods involving noise packet insertion, due to its need to capture fine-grained features, it nonetheless remains efective in identifying both the main page and sub-pages.

## 4.7 Ablation Experiment

To validate the critical contributions of the Feature Enhancer, Hierarchical Feature Interaction, and EnhanceSubHead modules to HiFi-WF, we conduct an ablation study for evaluation.

Experiment 1: Removing Feature Enhancer. For the first ablation experiment, we remove the Feature Enhancer module and directly perform soft segmentation on the extracted features (from the scanner module) to proceed with subsequent model processing. A comparison of the results in Table 2 and Table 6 reveals that the Feature Enhancer contributes the most substantial performance gain to the model. In particular, the performance metrics for homepage identification, including Recall, Precision@2, and MAP@2, decrease markedly by over 12% in its absence, while subpage performance also experiences a noticeable decline. This outcome can be attributed to the module’s ability to filter out noise that obscures temporal characteristics and enhance discriminative features.

Table 5: Two-tab Performance on Homepage and Subpage under Defense of HiFi-WF

<table><tr><td rowspan="2">Defense</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>Random [25]</td><td>0.902</td><td>0.806</td><td>0.852</td><td>0.860</td><td>0.853</td><td>0.788</td><td>0.725</td><td>0.755</td><td>0.760</td><td>0.741</td></tr><tr><td>WTF-PAD [20]</td><td>0.831</td><td>0.723</td><td>0.773</td><td>0.775</td><td>0.761</td><td>0.711</td><td>0.602</td><td>0.652</td><td>0.632</td><td>0.607</td></tr><tr><td>Front [13]</td><td>0.785</td><td>0.661</td><td>0.718</td><td>0.724</td><td>0.708</td><td>0.554</td><td>0.544</td><td>0.549</td><td>0.588</td><td>0.566</td></tr></table>

Table 6: Ablation Experiments on Hierarchical Classification in 2-tab Scenarios of HiFi-WF

<table><tr><td rowspan="2">Ablation Module</td><td colspan="5">Homepage</td><td colspan="5">Subpage</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>P@2</td><td>MAP@2</td></tr><tr><td>w/o Feature Enhancer</td><td>0.959</td><td>0.748</td><td>0.841</td><td>0.788</td><td>0.785</td><td>0.894</td><td>0.711</td><td>0.792</td><td>0.759</td><td>0.751</td></tr><tr><td>w/o Hierarchical Feature Interaction</td><td>0.985</td><td>0.772</td><td>0.866</td><td>0.823</td><td>0.819</td><td>0.824</td><td>0.753</td><td>0.787</td><td>0.785</td><td>0.771</td></tr><tr><td>w/o Enhanced Sub-Head</td><td>0.952</td><td>0.862</td><td>0.905</td><td>0.905</td><td>0.900</td><td>0.869</td><td>0.762</td><td>0.812</td><td>0.799</td><td>0.791</td></tr></table>

Experiment 2: Removing HFI (Hierarchical Feature Interaction). We subsequently removed the Hierarchical Feature Interaction module, thereby eliminating interaction between the resulting dual-channel features. It can be observed that the performance met rics for homepage identification decreased by approximately 10%, while those for subpages declined by about 3%. This outcome can be explained by the fact that, without supplementary features from subpages to aid in homepage recognition, the performance degra dation on homepages is more pronounced. In contrast, although subpage identification loses the auxiliary constraints provided by homepage features, the model still relies primarily on their own intrinsic characteristics for recognition, resulting in a relatively minor decline in performance.

Experiment 3: Removing Enhanced Sub-Head. In this ablation experiment, we substituted the Enhanced Sub-Head in the model with an MLP structure identical to that of the main classifica tion head. As inferred from our previous ablation experiment, since the model primarily relies on feature representation for classifica tion, the constraining influence of homepage features on subpage identification does not substantially afect the model’s recognition capability. The Enhanced Sub-Head module mainly functions by leveraging the predictions of the main label to refine the output for sub-labels, thereby playing a fine-tuning role rather than serving as a decisive component. Consistent with this reasoning, the empirical results indicate only a marginal performance degradation, which is not statistically significant.

## 5 Conclusion and Future Work

In this work, we have introduced HiFi-WF, a website fingerprinting attack model designed to identify both websites and their subpages, thereby expanding the scope of existing attacks, which largely focus on homepage identification. By employing feature interaction and self-interaction mechanisms across homepages and subpages, our approach achieves hierarchical multi-label classification even with sparse training samples, making WF attacks both more realistic and significantly finer-grained. Experimental results demonstrate that HiFi-WF excels in multi-label website identification within mixed trafic scenarios and efectively addresses the challenge of subpage recognition.

Looking ahead, we plan to broaden the scope of subpage monitoring, extend our study across multiple browsers, and evaluate performance under diverse network conditions, with the goal of accurately identifying websites and individual subpages in increasingly complex mixed-trafic environments. Moreover, because subpage identification relies on finer-grained features, strengthening subpage recognition under WF defenses remains an important direction for future work. In addition, the intrinsic distinctions and relationships between homepages and subpages, as well as among subpages themselves, can guide the design of defenses against subpage fingerprinting. For instance, selectively inserting or removing packets to make one subpage’s trafic resemble another may reduce the model’s ability to pinpoint specific subpages. Overall, these eforts are expected to broaden the landscape of WF research and open new avenues for both attack and defense.

## Acknowledgments

This work is supported by Science and Technology Innovation Key R&D Program of Chongqing CSTB2025TIAD-STX0032, and by National Natural Science Foundation of China 62572083, 62472225, 62572079 and 62472056, and by Hubei Province QB Program 2025lzz0043 and by New Chongqing Innovative Young Talent Support Program, CSTB2025YITP-QCRCX0018.

## References

[1] Abe, K., and Goto, S. Fingerprinting attack on tor anonymity using deep learning. Proceedings of the Asia-Pacific Advanced Network 42, 0 (2016), 15–20.

[2] Bacis, E., Bilogrevic, I., Busa-Fekete, R., Herath, A., Sartori, A., and Syed, U. Assessing web fingerprinting risk. In Companion Proceedings ofthe ACM Web Conference 2024 (2024), pp. 245–254.

[3] Bhat, S., Lu, D., Kwon, A., and Devadas, S. Var-cnn: A data-eficient website fingerprinting attack based on deep learning. arXiv preprint arXiv:1802.10215 (2018).

[4] Cheng, Y., Zhu, Y., Li, B., Sun, P., Ding, Y., Deng, X., and Liu, Q. Holmes & watson: A robust and lightweight https website fingerprinting through http version parallelism. In Proceedings ofthe ACM on Web Conference 2025 (2025), pp. 1078–1092.

[5] Cui, J., Xu, T., Zhao, L., and Han, S. A website fingerprinting attack based on parameter prediction model for conceptual drift. In 2024 IEEE International Conference on Software System and Information Processing (ICSSIP) (2024), IEEE, pp. 116–122.

[6] Cui, W., Chen, T., Fields, C., Chen, J., Sierra, A., and Chan-Tin, E. Revisiting assumptions for website fingerprinting attacks. In Proceedings ofthe 2019 ACM asia conference on computer and communications security (2019), pp. 328–339.

[7] Deng, X., Li, Q., and Xu, K. Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security (2024), pp. 1997–2011.

[8] Deng, X., Yin, Q., Liu, Z., Zhao, X., Li, Q., Xu, M., Xu, K., and Wu, J. Robust multi-tab website fingerprinting attacks in the wild. In 2023 IEEE symposium on security and privacy (SP) (2023), IEEE, pp. 1005–1022.

[9] Ding, Y., and Hu, B. A multi-granularity features representation and dimension ality reduction network for website fingerprinting. IEEE Access (2024).

[10] Dingledine, R., Mathewson, N., and Syverson, P. Tor: The second-generation onion router.

[11] Gao, B., Liu, W., Liu, G., and Nie, F. Resource knowledge-driven heterogeneous graph learning for website fingerprinting. IEEE Transactions on Cognitive Communications and Networking 10, 3 (2024), 968–981.

[12] Gao, B., Liu, W., Liu, G., Nie, F., and Huang, J. Multi-level resource-coherented graph learning for website fingerprinting attacks. IEEE Transactions on Information Forensics and Security (2024).

[13] Gong, J., and Wang, T. Zero-delay lightweight defenses against website fin gerprinting. In 29th USENIX Security Symposium (USENIX Security 20) (2020), pp. 717–734.

[14] Guan, Z., Xiong, G., Gou, G., Li, Z., Cui, M., and Liu, C. Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor. In Proceedings of the 37th Annual Computer Security Applications Conference (2021), pp. 248–259.

[15] Hayes, J., and Danezis, G. k-fingerprinting: A robust scalable website fingerprinting technique. In 25th USENIX Security Symposium (USENIX Security 16) (2016), pp. 1187–1203.

[16] Hong, X., Ma, X., Li, S., Cai, Y., and Liu, B. Ssbm: A spatially separated boxesbased multi-tab website fingerprinting model. Journal ofNetwork and Computer Applications 232 (2024), 104023.

[17] Huang, G., Ma, C., Ding, M., Qian, Y., Ge, C., Fang, L., and Liu, Z. Eficient and low overhead website fingerprinting attacks and defenses based on tcp/ip trafic. In Proceedings ofthe ACM Web Conference 2023 (2023), pp. 1991–1999.

[18] Jin, Z., Lu, T., Luo, S., and Shang, J. Transformer-based model for multi-tab website fingerprinting attack. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security (2023), pp. 1050–1064.

[19] Juarez, M., Afroz, S., Acar, G., Diaz, C., and Greenstadt, R. A critical evalua tion of website fingerprinting attacks. In Proceedings of the 2014 ACM SIGSAC conference on computer and communications security (2014), pp. 263–274.

[20] Juárez, M., Imani, M., Perry, M., Diaz, C., and Wright, M. Wtf-pad: toward an eficient website fingerprinting defense for tor. CoRR, abs/1512.00524 (2015).

[21] Li, J., Wang, D., Liu, Y., Gao, Y., Zhang, X., Lin, Z., Ma, X., Luo, X., and Guan, X. Cross-environmental website fingerprinting. In IEEE INFOCOM 2025-IEEE Conference on Computer Communications (2025), IEEE, pp. 1–10.

[22] Lin, T.-Y., Goyal, P., Girshick, R., He, K., and Dollár, P. Focal loss for dense object detection. In Proceedings of the IEEE international conference on computer vision (2017), pp. 2980–2988.

[23] Meng, W., Ma, C., Ding, M., Ge, C., Qian, Y., and Xiang, T. Beyond single tabs: A transformative few-shot approach to multi-tab website fingerprinting attacks. In Proceedings ofthe ACM on Web Conference 2025 (2025), pp. 1068–1077.

[24] Mitseva, A., and Panchenko, A. Stop, don’t click here anymore: boosting website fingerprinting by considering sets of subpages. In 33rd USENIX Security Symposium (USENIX Security 24) (2024), pp. 4139–4156.

[25] Qian, Y., Huang, G., Ma, C., Ding, M., Yuan, L., Chen, Z., and Wang, K. En hancing resilience in website fingerprinting: Novel adversary strategies for noisy trafic environments. IEEE Transactions on Information Forensics and Security (2024).

[26] Rimmer, V., Preuveneers, D., Juarez, M., Van Goethem, T., and Joosen,

W. Automated website fingerprinting through deep learning. arXiv preprint arXiv:1708.06376 (2017).

[27] Shen, M., Ji, K., Gao, Z., Li, Q., Zhu, L., and Xu, K. Subverting website fingerprinting defenses with robust trafic representation. In 32nd USENIX Security Symposium (USENIX Security 23) (2023), pp. 607–624

[28] Sirinam, P., Imani, M., Juarez, M., and Wright, M. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings ofthe 2018 ACM SIGSAC conference on computer and communications security (2018), pp. 1928–1943.

[29] Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. Advances in neural information processing systems 30 (2017).

[30] Wagner, D., Schneier, B., et al. Analysis of the ssl 3.0 protocol. In The second USENIX workshop on electronic commerce proceedings (1996), vol. 1, pp. 29–40.

[31] Wang, T., and Goldberg, I. On realistically attacking tor with website fingerprinting. Proceedings on Privacy Enhancing Technologies (2016).

[32] Xie, Y., Feng,J., Huang, W., Zhang, Y., Sun, X., Chen, X., and Luo, X. Contrastive fingerprinting: A novel website fingerprinting attack over few-shot traces. In Proceedings ofthe ACM Web Conference 2024 (2024), pp. 1203–1214.

[33] Xu, Y., Wang, T., Li, Q., Gong, Q., Chen, Y., and Jiang, Y. A multi-tab website fingerprinting attack. In Proceedings of the 34th Annual Computer Security Applications Conference (2018), pp. 327–341.

[34] Yin, Q., Liu, Z., Li, Q., Wang, T., Wang, Q., Shen, C., and Xu, Y. An automated multi-tab website fingerprinting attack. IEEE Transactions on Dependable and Secure Computing 19, 6 (2021), 3656–3670.

[35] Yuan, Y., Du, Y., and Cheng, G. Class incremental website fingerprinting attack based on dynamic expansion architecture. IEEE Transactions on Network and Service Management (2025).

[36] Yuan, Y., Zou, W., and Cheng, G. Mw3f: Improved multi-tab website fingerprinting attacks with transformer-based feature fusion. Journal of Network and Computer Applications 236 (2025), 104125.

[37] Zou, H., Su, J., Wei, Z., Chen, S., Yang, C., and Chen, M. Toward an efective few-shot website fingerprinting attack with quadruplet networks and deep local fingerprinting features. IEEE Transactions on Dependable and Secure Computing (2025).

## A Data Preprocess

As illustrated in Figure 4, we reformulate each trafic sample into a 2-row matrix to adapt to the dual-channel input of HiFi-WF.

![](images/8237f31332ee16a456542ba21334c4bce5eaa5f94170861e8eebccf4a67c20a3.jpg)

<table><tr><td>Outgoing</td><td>86</td><td>0</td><td>1494</td><td>444</td><td>0</td><td>...</td></tr><tr><td>Incoming</td><td>0</td><td>82</td><td>0</td><td>0</td><td>1494</td><td>...</td></tr></table>

Figure 4: Trafic Sequences are Converted into a Dual-channel Input Matrix.

This explicit spatial separation of directions provides a critical inductive bias for the task of hierarchical webpage identification. By segregating trafic directions into dedicated channels, the model is relieved from learning to decode a combined sign-value representation (where sign indicates direction and absolute value indicates size). Consequently, the subsequent convolutional network can immediately and eficiently operate on these separate "outgoing" and "incoming" channels, either independently to learn directionspecific features or conjointly to capture their inter-dependencies, significantly enhancing learning eficiency and final performance

![](images/3311797ef4e08201a4b80e3a8be7e049b65014b5a82ee8a42524eeddd3d2fdc6.jpg)  
Figure 5: The architecture of Dual-Path Segmentation. A compact network derives two weight vectors from the features.

## B Complete Model Execution Process

Feature Processor. The HiFi-WF model employs a specialized feature processor, which integrates two core components: a Feature Extractor built upon Convolutional Neural Networks (CNNs) and a Feature Enhancer leveraging dual attention mechanisms—channel attention and temporal attention.

The extractor consists of an initial convolutional block followed by three identical blocks and a final projection block. The process progressively reduces the temporal dimension to 64 while expanding channels to 256, creating a rich feature map $\mathbf { F } ^ { \prime } \in \mathbb { R } ^ { }$ �×256×64 optimal for subsequent processing:

$$
\mathbf {H} _ {1} = \operatorname{ReLU} (\mathrm{BN} (\operatorname{Conv1D} _ {k = 7, s = 2} (\mathbf {X}))),\tag{2}
$$

$$
\mathbf {H} _ {1} ^ {\prime} = \operatorname{MaxPool1d} _ {k = 3, s = 2} (\mathbf {H} _ {1}),\tag{3}
$$

$$
\mathbf {H} _ {i} = \operatorname{ReLU} \left(\mathrm{BN} \left(\operatorname{Conv1D} _ {k = 3, s = 1} \left(\mathbf {H} _ {i - 1} ^ {\prime}\right)\right)\right), \quad i \in \{2, 3, 4 \},\tag{4}
$$

$$
\mathbf {H} _ {i} ^ {\prime} = \operatorname{MaxPool1d} _ {k = 2, s = 2} (\mathbf {H} _ {i}),\tag{5}
$$

$$
\mathbf {F} = \operatorname{ReLU} \left(\mathrm{BN} \left(\operatorname{Conv1D} _ {k = 3, s = 1, c = 2 5 6} \left(\mathbf {H} _ {4} ^ {\prime}\right)\right)\right) \text { and }\tag{6}
$$

$$
\mathbf {F} ^ {\prime} = \mathrm{AdaptiveAvgPool1d} _ {l = 6 4} (\mathbf {F}).\tag{7}
$$

Comprising two sequential attention mechanisms, the feature enhancer then processes the feature maps $\mathbf { F ^ { \prime } } _ { \mathbf { \lambda } }$ . The channel atten tion module first performs channel-wise recalibration, amplifying salient features across the 256 channels. This operation can be formulated as:

$$
\mathbf {F} _ {\mathrm{ca}} ^ {\prime} = \mathbf {F} ^ {\prime} \odot \sigma (f _ {\mathrm{MLP}} (\bar {\mathbf {F}} ^ {\prime})),\tag{8}
$$

where $\mathbf { F ^ { \prime } }$ is the input feature map, $\bar { \mathbf { F ^ { \prime } } } \in \mathbb { R } ^ { B \times C }$ is obtained by squeezing the spatial dimension via global average pooling, �<sub>MLP</sub> denotes a shared multi-layer perceptron, � is the sigmoid activation function, and ⊙ denotes element-wise multiplication.

Dual-Path Segmentation. As discussed in Section 3.3, this module achieves "soft segmentation" of the feature maps.

The feature maps are fed into a compact network, as illustrated in Figure 5. This network employs Softmax to ensure the weights of the two channels sum to 1 at each spatial location, while outputting two attention weight vectors $t _ { w 1 }$ and $t _ { w 2 }$ that generate weighted feature representations emphasizing the homepage and subpage perspectives, respectively. The process can be formulated as:

$$
\left[ \mathbf {t} _ {w 1}, \mathbf {t} _ {w 2} \right] = \sigma (g (\mathbf {F} _ {\mathrm{en}} ^ {\prime})),\tag{9}
$$

where $g ( \cdot )$ is the small network shown in Figure 6 and $\sigma ( \cdot )$ is the softmax function applied along the second dimension. This ensures that for each timestep, the weights sum to one:

$$
\mathbf {t} _ {w 1} ^ {(b, l)} + \mathbf {t} _ {w 2} ^ {(b, l)} = 1,\tag{10}
$$

These weight vectors are subsequently multiplied element-wise with the feature maps X processed by the Feature Processor:

$$
\mathbf {F} _ {\mathrm{main}} = \mathbf {F} _ {\mathrm{en}} ^ {\prime} \odot \mathbf {t} _ {w 1}, \quad \mathbf {F} _ {\mathrm{sub}} = \mathbf {F} _ {\mathrm{en}} ^ {\prime} \odot \mathbf {t} _ {w 2}.\tag{11}
$$

where ⊙ denotes element-wise multiplication between the feature map $F$ and the attention weight vectors $t _ { w 1 }$ and $t _ { w 2 }$ , respectively.

These two vectors represent the learned weight parameters that the model considers more important for identifying the homepages and subpages, respectively. As the outputs are passed through a softmax layer, the weights corresponding to each timestep sum to 1, indicating that the feature at each timestep contributes predominantly to either homepage or subpage identification. These weight vectors are subsequently multiplied element-wise with the feature maps processed by the Feature Processor, resulting in two distinct feature maps: one biased toward homepage recognition and the other toward subpage recognition, both retaining the same shape as the input feature maps. In this way, soft segmentation of trafic patterns is efectively achieved.

Hierarchical Feature Interaction. The Feature Interaction Module is designed to facilitate interaction between the two separately weighted feature maps, $\mathbf { F } _ { \mathrm { m a i n } }$ and $\mathbf { F } _ { \mathrm { s u b } }$ , obtained from the previous step. This enables the model to efectively capture the hierarchical dependencies between main and sub-categories, resulting in a final set of refined, context-aware features. Initially, these two feature maps are processed by a shared encoder to project them into a common semantic space, yielding the transformed representations $Z _ { \mathrm { m a i n } }$ and ${ \bf { Z } } _ { \mathrm { { s u b } } }$ , as formalized below:

$$
\mathbf {Z} _ {\mathrm{main}} = \operatorname{Encoder} (\mathbf {F} _ {\mathrm{main}}),\tag{12}
$$

$$
\mathbf {Z} _ {\text { sub }} = \operatorname{Encoder} (\mathbf {F} _ {\text { sub }}).\tag{13}
$$

Subsequently, the encoded feature maps $Z _ { \mathrm { m a i n } }$ and ${ \bf { Z } } _ { \mathrm { { s u b } } }$ are transformed into one-dimensional vector representations via a flattening operation to prepare them for the subsequent interaction mechanism:

$$
\mathbf {z} _ {\text { main }} = \text { Flatten } (\mathbf {Z} _ {\text { main }}),
$$

$$
\mathbf {z} _ {\mathrm{sub}} = \operatorname{Flatten} (\mathbf {Z} _ {\mathrm{sub}}).\tag{14}
$$

(15)

The core ofthis module is a multi-head attention mechanism. The two input vectors are first concatenated along the sequence dimension to form a combined representation $\mathbf { Z } _ { \mathrm { c o m b i n e d } } = \left[ \mathbf { z } _ { \mathrm { m a i n } } , \mathbf { z } _ { \mathrm { s u b } } \right]$ which serves as the Query (Q), Key (K), and Value (V) for a selfattention calculation. This allows each feature to attend to all elements in the combined sequence, efectively enabling cross-feature information exchange:

$$
\operatorname{Attention} (Q, K, V) = \operatorname{softmax} \left(\frac {Q K ^ {T}}{\sqrt {d _ {k}}}\right) V,\tag{16}
$$

where $d _ { k }$ is the dimension of the key vectors. The output of the attention block is then processed through a feed-forward network (FFN) with residual connections and layer normalization. Finally, the enhanced sequence is split and fused with the original inputs via learnable gating parameters (� and $\beta )$ to produce the final refined outputs:

$$
\mathbf {z} _ {\mathrm{main}} ^ {\prime} = \boldsymbol {\alpha} \cdot \mathbf {z} _ {\mathrm{main}} + (1 - \boldsymbol {\alpha}) \cdot \mathbf {h} _ {\mathrm{main}},\tag{17}
$$

$$
\mathbf {z} _ {\mathrm{sub}} ^ {\prime} = \boldsymbol {\beta} \cdot \mathbf {z} _ {\mathrm{sub}} + (1 - \boldsymbol {\beta}) \cdot \mathbf {h} _ {\mathrm{sub}}.\tag{18}
$$

where $\mathbf { h } _ { \mathrm { m a i n } }$ and $\mathbf { h } _ { \mathrm { s u b } }$ are the enhanced features for the main and sub categories, respectively, extracted from the interaction module’s output sequence. At this stage, $\mathbf { z } _ { \mathrm { m a i n } } ^ { \prime }$ has been infused with features from the subpages, while similarly, $\mathbf { z } _ { \mathrm { s u b } } ^ { \prime }$ has incorporated information from the homepage.

Dual-Path Classifier. Both homepage classification heads are implemented as multi-layer perceptrons (MLPs). They take the feature vectors $\mathbf { z } _ { \mathrm { m a i n } } ^ { \prime }$ and $\mathbf { z } _ { \mathrm { s u b } } ^ { \prime }$ as inputs, respectively. Note that $\mathbf { z } _ { \mathrm { m a i n } } ^ { \prime }$ contains both homepage features and contextual information from subpages, while $\mathbf { z } _ { \mathrm { s u b } } ^ { \prime }$ also incorporates homepage-related features. These enriched representations are processed independently by the two classifiers, and their outputs are aggregated to produce the final homepage prediction:

$$
\hat {\mathbf {y}} _ {\mathrm{main}} = \mathcal {A} \left(\mathcal {H} _ {1} (\mathbf {z} _ {\mathrm{main}} ^ {\prime}), \mathcal {H} _ {2} (\mathbf {z} _ {\mathrm{sub}} ^ {\prime})\right),
$$

where $\mathcal { H } _ { 1 }$ and $\mathcal { H } _ { 2 }$ denote the two MLP-based classifiers, and A is an aggregation function such as averaging or weighted fusion.

The subpage classification heads also consist of two classifiers. However, their design incorporates an additional hierarchical constraint mechanism. Owing to the fact that the number of traf fic traces associated with a subpage is substantially smaller than that of homepages, and given the intrinsic hierarchical dependency between subpages and homepages, the preliminary homepage pre diction is utilized to guide the subpage classification. Formally, the outputs from the Hierarchical Feature Interaction module are fused with the homepage prediction logits to generate a constraint mask M<sub>constraint</sub>. This mask is subsequently employed to condition the subpage classifier:

$$
\hat {\mathbf {y}} _ {\mathrm{sub}} = \mathcal {S} \left(\mathbf {z} _ {\mathrm{sub}} ^ {\prime} \oplus \mathbf {z} _ {\mathrm{main}} ^ {\prime}\right) \odot \sigma \left(\mathbf {M} _ {\mathrm{constraint}} (\hat {\mathbf {y}} _ {\mathrm{main}})\right),
$$

where $s$ denotes the subpage classification head, ⊕ signifies a feature fusion operation, ⊙ represents element-wise multiplication, and � is a sigmoid activation function.

## C Datasets Details

Chrome datasets. Based on the ranking of the most popular websites<sup>1</sup>, we randomly selected 50 websites from the top 200 and, for each, randomly selected 10 subpages directly accessible from their homepage. A hierarchical labeling scheme is employed: all trafic within a continuous access sequence from a homepage to one of its subpages is annotated with the main website label, while individual subpages are distinguished with specific sub-labels. As mentioned in the Introduction, while the trafic patterns of a homepage and its subpages difer, they are inherently related to the same website. This design ensures that each of the 50 monitored websites in our dataset is represented by 10 distinct types of trafic patterns.

MP-SA (Multi-Permutation, Single-Access) datasets: We con structed our dataset using 500 monitored homepage–subpage pairs derived from 50 websites, each contributing 10 unique subpages directly accessible from its homepage. A single 2-tab browsing instance was defined as trafic generated from four consecutive page visits, representing a non-repeating sequence composed of two website pairs. To build the dataset, we randomly sampled from the 500 homepage-subpage pairs without replacement to form individual browsing sessions. Each session comprised visits to four webpages in sequence: the homepage and a corresponding subpage from one website, followed by the homepage and a subpage from another distinct website. This design efectively simulated 2-tab trafic (covering four distinct webpages) without intermediate browser termination, thereby preserving realistic continuity. The random sampling process was repeated 20 times to ensure diversity, with each permutation generating a unique browsing sequence. In total, this procedure produced 10,000 distinct trafic instances, forming a comprehensive dataset for hierarchical website and subpage analysis.

SP-MA (Single-Permutation, Multi-Access) datasets: While maintaining the core experimental setup of the 2-tab-MP-SA dataset, including the use of 500 homepage–subpage pairs and the same definition for a 2-tab browsing instance, the primary diference lies in the permutation and access procedure. Here, the 500 pairs were permuted a single time, and the resulting sequence was repeatedly executed 20 times, producing a total of 10,000 instances. Additionally, under an analogous configuration, we collected a 3-tab trafic dataset, where each instance comprises continuous visits to three distinct homepage–subpage pairs, yielding 5,000 instances. Collectively, these two datasets form the SP-MA datasets, providing comprehensive coverage for multi-tab hierarchical trafic analysis. Open-World datasets: To construct the dataset, we randomly selected 12,000 websites from the top-50,000 sites in the Tranco ranking<sup>2</sup>, excluding our set of 50 monitored websites. Each of these websites may or may not include trafic from their subpages, thereby increasing the complexity of the mixed trafic. Following the same protocol as for the MP-SA datasets, we performed random permutations at the four-tab level, retaining only one trafic instance per unique sequence. This process yielded a total of 12,000 instances, which constitute our open-world dataset.

Tor dataset. We utilized a Vultr Cloud server deployed in New York, United States, to randomly select 50 websites from the top 200 of the Tranco ranking (none of which overlapped with any websites in the Chrome datasets or the open-world datasets). Following the same configuration as the 2-tab SP-MA datasets, but with only 10 repeated executions, we collected a total of 2,500 trafic instances, which constitute our Tor datasets.

## D Threshold-Based Inference Strategy

For our proposed HiFi-WF, we design a threshold-based inference strategy tailored to the hierarchical task. This strategy dynamically selects positive predictions by maximizing micro-F1 across global thresholds, which naturally handles the variable number of positive subpage labels and avoids heuristic constraints (e.g., fixed top-k selection). This design is a key part of our solution to the new scenario.

For baseline models discussed in Section 4.2.1, these models are originally designed for multi-level classification (either homepage or subpage alone) and lack native support for hierarchical dependencies. We adopt hard-label inference (e.g., fixed top-2 homepage selection + top-1 subpage selection within constrained ranges) for them, which aligns with their original design logic and reflects their intrinsic capability when adapted to the new scenario, without in troducing over-customized modifications that deviate from their original intent.

## E Hierarchical Focal Loss

We propose a hierarchical loss function that combines multi-label focal loss with hierarchical constraints to address class imbalance and enforce logical dependencies between parent and child categories.

## E.1 Multi-Label Focal Loss

The focal loss component addresses class imbalance by downweighting well-classified examples:

$$
\mathcal {L} _ {\mathrm{focal}} (z, y) = \frac {1}{N} \sum_ {i = 1} ^ {N} \left[ \alpha_ {t} (1 - p _ {t}) ^ {\gamma} \mathrm{BCE} (z _ {i}, y _ {i}) \right],\tag{19}
$$

where:

• � represents the logits, � denotes the ground truth labels;

$\mathrm { B C E } ( z _ { i } , y _ { i } ) = - [ y _ { i } \log ( \sigma ( z _ { i } ) ) + ( 1 - y _ { i } ) \log ( 1 - \sigma ( z _ { i } ) ) ]$ is the binary cross-entropy;

$\begin{array} { r } { \sigma ( z _ { i } ) = \frac { 1 } { 1 + e ^ { - z _ { i } } } } \end{array}$ is the sigmoid activation function;

$p _ { t } = \sigma ( z ) \cdot y + ( 1 - \sigma ( z ) ) \cdot ( 1 - y )$ represents the predicted probability for the true class;

$\alpha = 0 . 7 5$ balances positive/negative examples, $\gamma = 5 . 0$ is the focusing parameter;

$\alpha _ { t } = \alpha \cdot y + \left( 1 - \alpha \right) \cdot \left( 1 - y \right)$ is the class-balanced weighting factor.

## E.2 Hierarchical Constraint Loss

The hierarchical constraint ensures logical consistency between parent $\left( z _ { m } \right)$ and child $( z _ { s } )$ categories:

$$
\mathcal {L} _ {\text { constraint }} (z _ {m}, z _ {s}) = \lambda_ {1} \mathcal {L} _ {\text { inactive }} + \lambda_ {2} \mathcal {L} _ {\text { active }} + \lambda_ {3} \mathcal {L} _ {\text { consistency }},\tag{20}
$$

where $\lambda _ { 1 } = 0 . 3 , \lambda _ { 2 } = 0 . 2 , \lambda _ { 3 } = 0 . 3$ are balancing coeficients.

Inactive Parent Constraint. When parent categories are inactive $( p _ { m } < 0 . 3 )$ , child categories should be suppressed:

$$
\mathcal {L} _ {\text { inactive }} = \frac {1}{N \cdot K} \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {K} \mathbb {I} _ {[ p _ {m} ^ {(i, j)} <   0. 3 ]} \cdot \mathrm{BCE} (z _ {s} ^ {(i, j)}, 0),\tag{21}
$$

where $p _ { m } = \sigma ( z _ { m } )$ , � is the number of child categories per parent, and I is the indicator function.

Active Parent Constraint. When parent categories are active $( p _ { m } > 0 . 7 )$ , child categories should maintain reasonable values:

$$
\mathcal {L} _ {\text {active}} = \frac {1}{N \cdot K} \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {K} \mathbb {I} _ {[ p _ {m} ^ {(i, j)} > 0. 7 ]} \cdot \left(p _ {s} ^ {(i, j)} - p _ {m} ^ {(i, j)}\right) ^ {2},\tag{22}
$$

where $\begin{array} { r } { p _ { s } = \sigma ( z _ { s } ) } \end{array}$

Consistency Constraint. Activated child categories must have activated parent categories:

$$
\mathcal {L} _ {\text { consistency }} = \frac {1}{N \cdot K} \sum_ {i = 1} ^ {N} \sum_ {j = 1} ^ {K} \mathrm{BCE} (z _ {m} ^ {(i, j)}, \mathbb {I} _ {[ p _ {s} ^ {(i, j)} > 0. 5 ]}),\tag{23}
$$

## E.3 Complete Hierarchical Loss

The complete loss function combines both components:

$$
\mathcal {L} _ {\text { total }} = \beta_ {1} \mathcal {L} _ {\text { main }} + \beta_ {2} \mathcal {L} _ {\text { sub }} + \beta_ {3} \mathcal {L} _ {\text { constraint }},\tag{24}
$$

where $\beta _ { 1 } = 2 . 5 , \beta _ { 2 } = 1 . 0 , \beta _ { 3 } = 0 . 3$ are task-balancing coeficients, and:

$\begin{array} { r } { \mathcal { L } _ { \mathrm { m a i n } } = \mathcal { L } _ { \mathrm { f o c a l } } ( z _ { m } , y _ { m } ) ; } \end{array}$ : Main category loss.

$\mathcal { L } _ { \mathrm { s u b } } = \mathcal { L } _ { \mathrm { f o c a l } } ( z _ { s } , y _ { s } )$ : Sub-category loss.

This formulation ensures both efective multi-label classification and hierarchical consistency between parent-child category relationships.
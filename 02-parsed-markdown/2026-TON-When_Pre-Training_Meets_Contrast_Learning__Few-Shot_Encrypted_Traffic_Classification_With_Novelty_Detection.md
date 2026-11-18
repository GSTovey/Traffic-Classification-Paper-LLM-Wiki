# When Pre-Training Meets Contrast Learning: Few-Shot Encrypted Trafic Classification With Novelty Detection

Lixin Zhao , Changhao Wu, and Aimin Yu

Abstract—Encrypted trafic classification plays an important role on network security and network management. However, existing methods face two key limitations: they require large volumes of labeled data and are typically designed under the closed-world assumption. This paper presents a novel approach combining pre-training techniques with contrast learning to address the challenges of open-world encrypted trafic classification. Our method utilizes a BERT-based pre-training model to learn generic trafic representations from large-scale unlabeled encrypted trafic. In this stage, two pre-training tasks, the Masked BURST Model (MBM) and BURST Context Prediction (BCP), are introduced to capture both structural and contextual features of the trafic. Following this, a contrast learning strategy is applied on a small labeled dataset to learn a discriminative feature space, where trafic from the same category is clustered closely, and trafic from diferent categories is largely separated. This strong discriminative property enables high-accuracy classification of known trafic categories while detecting novel ones. Experimental results on five encrypted trafic classification tasks demonstrate that: 1) under full data conditions, our approach outperforms state-of-the-art methods with up to an 11.60% improvement in F1 score in both closedand open-world scenarios; 2) even when working in a few-shot mode, our method achieves the best performance in three out of five tasks in the closed-world setting and consistently outperforms the best methods by up to 9.99% in terms of F1 score in the open-world scenario.

Index Terms—Encrypted trafic classification, pre-training, contrast learning, open-world classification.

## I. INTRODUCTION

N <sup>ETWORK</sup> <sup>trafic</sup> <sup>classification,</sup> <sup>which</sup> <sup>identifies</sup> <sup>trafic</sup> types originating from diferent applications and web services, serves as a cornerstone for managing and securing networks. It underpins critical functions such as intrusion detection [11], quality of service (QoS) optimization [36], user experience enhancement [9], and overall network visibility [1]. However, the widespread adoption of encryption (e.g.,

TLS 1.3, VPN, Tor) also allows malware and unauthorized services to evade detection, presenting significant challenges to traditional classification methods.

To address the issue of encrypted trafic classification, research has shifted from early machine learning (ML) with handcrafted features [4], [31] [32], [33], [42] to deep learning (DL) models that automatically extract patterns from raw trafic [26], [38] [39]. While efective, DL models typically require massive labeled datasets, which are dificult to obtain due to the need for expert knowledge and the rapid evolution of trafic patterns.

In recent years, pre-training techiques have gained great success on the fields of natural language processing [8] and computer vision [10]. The pre-training based methods usually use unlabeled data to learn general knowledge in a self-supervised learning way and then fine-tuning on limited amount of labeled data to adapt the specific down-stream tasks. Some attempts, such as PERT [18], ET-BERT [25], and YaTC [51] etc. have been made in trafic classification based on pre-training techniques. However, these existing works only explore the trafic representation ability provided by pretraining techniques in closed-world setting, that means all the categories of the downstream tasks are known and fixed. As a matter of fact, due to the openness of the real world, new encrypted trafic categories will constantly emerge (e.g. newly released applications with trafic encryption technology). Therefore, in order to accommodate the real-world scenarios, the encrypted trafic classification system should be (1) built on limited labeled trafic data (i.e., few-shot condition) and (2) performs high-precision classification for known trafic categories and (3) has the ability to detect novel trafic categories.

Existing works have explored few-shot learning and novel class detection, such as FC-Net [46] and TraficGPT [15], but address only isolated aspects of network trafic analysis. FC-Net targets few-shot classification for intrusion detection in closed-world settings, leveraging small samples but failing to handle unseen classes, limiting its applicability to dynamic network environments where new applications or threats emerge frequently. Similarly, TraficGPT leverages GPT-2 for openworld encrypted trafic classification, demonstrating improved generalization to unknown trafic types. However, its efectiveness depends on large-scale training data and lacks dedicated few-shot learning mechanisms. Thus, the primary motivation of our work is to address the dual challenge of classifying encrypted trafic with limited labeled data (few-shot) while detecting unseen classes in open-world scenarios, a combination not fully addressed by existing methods.

The core insight of our work is that efective few-shot openworld encrypted trafic classification necessitates a protocolaware hierarchical representation, rather than treating trafic as generic byte streams. Unlike prior Transformer-based approaches that treat trafic as flat token sequences (e.g., ET-BERT [25]), we explicitly model the inherent hierarchical structure of network trafic. In protocols such as TLS 1.3 or complex tunneling schemes (VPN/Tor), semantically meaningful units (BURSTs, defined as consecutive packets in the same direction) naturally correspond to application-layer request/response transactions. This structural prior acts as a critical inductive bias, enabling robust generalization under few-shot and open-world conditions.

To materialize this insight, we introduce a synergistic pretraining framework centered on the BURST concept. Our framework jointly optimizes two complementary objectives: the Masked BURST Model (MBM) task, which captures intra-BURST syntactic patterns, and the BURST Context Prediction (BCP) task, which learns inter-BURST semantic relationships. This hierarchical modeling strategy yields a robust representation foundation that serves as a strong initialization for downstream adaptation. Furthermore, to address the theoretical gap in open-world trafic classification, we refine these representations through a theoretically grounded supervised contrastive learning (SCL) stage. As analyzed in Proposition 1, this explicitly optimizes the intra-class compactness and interclass separation in the embedding space, thereby minimizing the open-world risk bound.

We evaluate the performance of our approach on five encrypted trafic classification tasks. Experimental results demonstrate that: (1) under full data conditions, our approach outperforms existing methods across all five tasks, achieving improvements of 11.60%, 0.92%, 8.83%, 5.60% and 2.16% in F1 score in the closed-world scenario, and 11.74%, 6.44%, 8.04%, 15.96% and 13.91% in the open-world scenario; (2) in the few-shot setting, our method achieves the best performance on the GEAC, ETCV, and EACT tasks, with only a marginal gap compared to state-of-the-art methods, which operate under full data conditions, on the EMC and EAC-1.3 tasks in the closed-world scenario. Notably, compared to specialized few-shot trafic classification approaches, our method yields a maximum improvement of 49.32% across all five tasks. Furthermore, in the open-world scenario, our approach (i.e., in few-shot condition) consistently outperforms the best existing methods (i.e., in full data condition) by 3.22%, 2.22%, 0.50%, 9.99% and 0.69% respectively in F1 score.

In summary, the contributions of this paper are as follows: • Integrated Framework for Open-World Analysis: We explore the synergy between pre-training techniques and contrast learning to address the dual challenges of fewshot classification and novel class detection in encrypted trafic.

• Hierarchical Pre-training Scheme: We design two domain-specific pre-training tasks to capture intra-BURST structural patterns and inter-BURST contextual logic, respectively. Their joint optimization yields a robust foundation for few-shot adaptation.

• Optimized Metric Space via SCL: We customize a supervised contrastive learning (SCL) strategy that explicitly enforces intra-class compactness and inter-class separation, which is theoretically justified to reduce the open-world classification risk.

Theoretical Foundation: We provide a theoretical analysis (Proposition 1) that quantifies how the quality of the learned embedding space bounds the performance of the nearest mean novelty detector, ofering insights into the method’s efectiveness.

• Extensive Validation: We conduct comprehensive evaluations across five encrypted trafic classification tasks. Results show that our approach consistently outperforms state-of-the-art methods in both closed-world and openworld scenarios, particularly under few-shot constraints.

## II. RELATED WORK

## A. Encrypted Trafic Classification

Existing encrypted trafic classification methods can be divided into two main categories: ML-based methods and DLbased methods. Table I provides a summary and comparison of existing trafic classification methods, with detailed descrip tions presented in the following section.

ML-based methods. The dominant ML-based methods [4], [31] [32], [33], [42] commonly employ algorithms such as SVM, KNN, and Naive Bayes to classify encrypted trafic. They typically rely on manually extracted features, such as packet count, packet size, and packet inter-arrival time etc. Recent work like [47] employs advanced handcrafted path signature features for encrypted trafic analysis, demonstrating the ongoing potential of feature engineering. The performance of these approaches hinges on the ability to extract discriminative features that efectively capture the diferences among trafic categories. However, this feature extraction process is heavily dependent on domain expertise, posing challenges to the scalability and adaptability. Whisper [12] detects malicious trafic, including zero-day attacks, by leveraging frequency domain features. However, from a trafic classification perspective, while it can identify novel classes, its capability is limited to binary classification rather than fine-grained multi-class classification. FOSS [23] employs a tree-based framework for fine-grained unknown attack detection in open-world network intrusion scenarios, but it cannot efectively adapt to few-shot scenarios.

DL-based methods. DL-based methods automatically learn complex feature patterns from the raw trafic and perform classification. Multiple deep learning models are adopted by diferent studies, including CNN-based models [29], [38], [40], RNN-based models [26], [41] and GNN-based models [20], [39]. Besides, some works [7], [28], [50] also solve the problem of open-world trafic classification based on deep learning techniques. Although DL-based methods eliminate tedious feature engineering, they depend on a large amount of labeled trafic data for model training to learn valid features. However, it is time-consuming and error-prone to perform large-scale trafic labeling. It should be noted that some DL-based methods [46], [48], [49] focus on few-shot trafic classification, a scenario that aligns with our focus. However, these studies lack novelty detection ability. In contrast, our approach performs open-world trafic classification without requiring large amounts of labeled data.

TABLE I  
COMPARISON OF THE EXISTING NETWORK TRAFFIC CLASSIFICATION METHODS

<table><tr><td>Category of Methods</td><td>Technique Roadmap</td><td>Multi-class Classification</td><td>Feature Generality</td><td>Few-shot Condition</td><td>Novelty Detection</td></tr><tr><td rowspan="3">ML-based</td><td>Statistics-related features [32],[42]</td><td>Yes</td><td>No</td><td>No</td><td>No</td></tr><tr><td>Frequency domain analysis [12]</td><td>No</td><td>No</td><td>No</td><td>Yes</td></tr><tr><td>Graph propagation [23]</td><td>Yes</td><td>No</td><td>No</td><td>Yes</td></tr><tr><td rowspan="5">DL-based</td><td>Meta-learning [46], [48]</td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td></tr><tr><td>Pre-training [18],[25],[6],[54]</td><td>Yes</td><td>Yes</td><td>No</td><td>No</td></tr><tr><td>Transfer learning [49]</td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td></tr><tr><td>One-class learning [53]</td><td>Yes</td><td>No</td><td>No</td><td>Yes</td></tr><tr><td>ours</td><td>Yes</td><td>Yes</td><td>Yes</td><td>Yes</td></tr></table>

## B. Pre-Training Techniques

Pre-training, also known as self-supervised pre-training, is an approach that involves training a model on a large amount of unlabeled data before fine-tuning it on a specific downstream task with labeled data. Pre-trained models, such as BERT [8] and its variants [21], [27], [37], have demonstrated a powerful ability to capture generic patterns from largescale unlabeled data, significantly enhancing performance in downstream tasks. In the field of trafic classification, PERT [18] was the first to adapt ALBERT for the task of encrypted trafic classification, demonstrating promising performance. However, it lacks a tailored design for encrypted trafic representation and pre-training tasks, which constrains its generalization to emerging encryption technologies. To address these limitations, ET-BERT [25] introduces a novel representation method for encrypted trafic and redesigns two pre-training tasks. Similarly, TraficFormer [54] develops a more fine-grained and complex pre-training task, termed the Same Origin-Direction-Flow (SODF) task. TraficLLM [6] introduces a dual-stage tuning framework leveraging LLMs for network trafic analysis, using trafic-domain tokenization along with EA-PEFT to enhance detection and generation tasks. However, all these methods require extensive fine-tuning data and are confined to closed-world assumptions, failing to generalize to novel classes outside the training distribution. For open-world scenarios, OWCP [24] synthesizes new classes in a spherical space for N+ 1 classification, yet risks overfitting due to the complexity of sampling from an infinite class space. TraficGPT [15] utilizes GPT-2 [35] combined with the K-LND [7] distance metric for novelty detection. However, as demonstrated in Section V-E, generic pre-trained features without explicit discriminative constraints often lack suficient class separability. Unlike these approaches, we explicitly impose a supervised metric learning objective to enforce a compact and discriminative manifold, which is critical for robust few-shot and open-world classification.

## C. Contrast Learning

Contrast learning is a key approach in self-supervised representation learning, aiming to bring similar samples closer in feature space while pushing dissimilar ones apart. While it has achieved significant success in computer vision (e.g. SimCLR [5], MoCo [19], BYOL [17]) and natural language processing (e.g. SimCSE [13]), applying it to network trafic remains challenging due to the multi-source heterogeneity and semantic ambiguity of raw trafic data. In this paper, we bridge pretraining with contrast learning to better characterize encrypted trafic. Unlike self-supervised paradigms such as SimCLR or MoCo, which rely on data augmentations and lack explicit label guidance, our contrastive learning strategy is based on the Supervised Contrastive Learning (SCL) framework. Moreover, existing studies mainly adopt contrastive learning in a heuristic manner, without ofering theoretical guarantees in open-world settings. This limitation motivates our formulation of SCL tailored for encrypted trafic, which explicitly optimizes discriminability under few-shot and novelty-aware constraints.

## III. METHODOLOGY

## A. Model Overview

The overall framework of our approach is shown in Fig. 1, which consists of two stages: pre-training and contrast learning. The goal of pre-training is to learn generic patterns for each trafic flow from large-scale unlabeled encrypted trafic, and the pre-trained model is then used as a feature extractor to obtain high-quality initial feature vector representations to conduct contrast learning. In the contrast learning stage, given the limited labeled trafic data, it performs similarity learning under the supervision of a customized contrastive loss function to obtain an embedding space, in where an open-world nearest mean classifier is applied.

## B. Pre-Training Stage

In the pre-training stage, the model is trained on a massive unlabeled trafic dataset. The raw trafic data is first converted into tokens (tokenization), and then constructed into the input for the pre-training tasks. There are two pre-training tasks: Masked BURST Model (MBM) task and BURST Context Prediction (BCP) task.

1) Data Preprocessing: Unlike natural language text which contains explicit semantic units, trafic data is a pure byte stream on the network. In order to efectively leverage the pre-training technique for generic trafic patterns learning, we perform the follow data preprocessing steps: (1) Flow-to-BURST, (2) BURST Tokenization, (3) Token Embedding.

(1) Flow-to-BURST: Give the raw trafic data, we first split out flows with the same 5-tuple (i.e., source IP, source port, destination IP, destination port, and protocol), which includes packets in both directions. Then, each flow is converted into multiple BURSTs each of which contains a sequence of consecutive packets transmitted along the same direction [34]. BURST arises from application-layer behavior and underlying protocol dynamics and it typically represents a distinct logical unit of data exchange. In modern web services, the interaction between client and server often involves segmented resource requests and responses, driven by the need to fetch multiple objects such as scripts, stylesheets, or media files. These segmented transfers are shaped by the concurrency mechanisms of application-layer protocols like HTTP/2 and transport-layer features like TCP’s congestion control management. As a result, a BURST reflects both the structure of application data and the temporal characteristics of its transmission, ofering insights into the operational patterns of the specific application.

![](images/8ace76d9f3270fa098742fc603c46938fd496ca9e95c547b15f7f448db9694f2.jpg)  
Fig. 1. Overview of the whole framework.

(2) BURST Tokenization: In order to transform the BURSTs into the token representations for pre-training, we draw an analogy between trafic flows and documents in natural language. From this perspective, BURSTs in flows can be mapped to sentences in documents. To transform BURSTs into tokenized representations, we decompose each BURST into a sequence of units analogous to words in natural language. Considering that BURST is composed of a string of hexadecimal numbers such as 802b04d732, a 2-gram model is employed to segment hexadecimal BURST data into units consisting of 2 adjacent bytes. For the above example, after segmentation, the results are 802b 2b04 04d7 d732. We empirically set the size of segment unit to 2 to limit the corpus size, since a large corpus space will significantly increase computational cost. These units are further tokenized using the Byte-Pair Encoding tokenizer, with a maximum corpus size constrained to 65536 tokens. In addition to the BURST units, special tokens such as [CLS], [SEP], [MASK] and [PAD] are included in the corpus. [CLS] is used for classification tasks. [SEP] is used to separate diferent BURSTs in the BCP task. [MASK] is used to replace the masked tokens in the MBM task. [PAD] is used to pad the input to the maximum length.

(3) Token Embedding: We select BERT as the base model for pre-training. Since the encoder of the BERT lacks convolutional or recurrent components, it is essential to incorporate additional information that enables the model to capture the positional relationships within the input data. Additionally, to facilitate the BCP task, it is necessary to include supplementary identifiers that encode the BURST segment information. These two steps are referred to as positional embedding and segment embedding, respectively. Furthermore, the process of transforming BURSTs into tokenized representations is known as token embedding. Collectively, these three embedding processes–positional, segment, and token embedding constitute the input representation required for pre-training.

![](images/5bd0ab7eecd5b94cdc211769d0a840494e8e1480aeab30a06cda1be9a6f6b8df.jpg)  
Fig. 2. Illustration of the two pre-training tasks for generic trafic feature learning.

2) Pre-Training Tasks: As shown in Fig. 2, we design two pre-training tasks, namely MBM task and BCP task, to efectively capture the internal relationships between bytes within a single BURST and the interrelations between BURSTs originating from the same flow or across diferent flows. The motivation for this two-task design is to learn a comprehensive representation of trafic flows by capturing both low-level byte patterns within individual protocol data units (BURSTs) and high-level contextual relationships between these units. These two tasks are jointly optimized to enable the model to comprehend both intra-BURST structures and inter-BURST correlations, thus facilitating the learning of more generic feature representations for each flow.

• MBM TASK. Similar to the Masked Language Modeling and the Masked Image Modeling introduced in BERT [8] and BEiT [2] respectively, the MBM task is utilized to learn the internal byte dependencies within BURSTs by predicting randomly masked tokens. This task forces the model to understand the syntactic structure and internal correlations of a BURST, which is often determined by specific network protocols (e.g., the structure of a TLS handshake record or an HTTP header). For example, in a BURST containing a TLS Client Hello message, the values of certain bytes (e.g., version, cipher suites, extensions) are highly correlated. If the bytes indicating the TLS version are masked, the model must infer their value based on the surrounding context bytes that define the TLS handshake structure. In detail, as shown in the upper part of Fig. 2, we first randomly select tokens to be masked in the input BURST. Then, for each of the masked tokens, one of the following actions is performed: (1) Replace it with the [MASK] token with 80% probability. (2) Replace it with another token with 10% probability. (3) Do nothing with 10% probability. Finally, a BERT-based model is trained to predict [MASK] based on the preceding and following bytes within the BURST. If there are k tokens are randomly masked in the input BURST S , the loss function for the MBM task L can be defined as:

$$
L _ {M B M} = - \sum_ {i = 1} ^ {k} \log (P (M A S K _ {i} = t o k e n _ {i} | \hat {S}; \theta))\tag{1}
$$

where $\theta$ is the set of trainable parameters of Transformer encoder and $P$ is the probability function modeled by θ. S<sup>ˆ</sup> is the representation of BURST S after masking and MAS K is the masked token at the $i _ { t h }$ position in BURST S .

• BCP TASK. The MBM task discussed above focuses on learning intra-BURST byte dependencies within individual trafic units. However, modeling isolated BURSTs alone is insuficient to capture the generic behavioral patterns of complete trafic flows. To this end, we design the BURST Context Prediction (BCP) task to learn contextual dependencies across BURSTs at the flow level.

Unlike Next Sentence Prediction (NSP) in natural language processing or the Same-origin Burst Prediction (SBP) task adopted in prior work such as ET-BERT [25], our BCP task is explicitly grounded in the structural characteristics of network trafic. In ET-BERT, segment-level prediction is typically constructed by splitting packet sequences at predefined or arbitrary boundaries, which is efective for capturing local co-occurrence patterns but does not explicitly model how semantically meaningful transmission units interact over time. In contrast, we adopt the BURST, which naturally delimited by changes in packet direction, as the basic semantic unit. A BURST often corresponds to a complete request or response at the application layer, thereby preserving protocol-level transactional integrity.

Based on this formulation, the BCP task aims to capture higher-order, flow-level semantics by modeling whether two BURSTs are contextually related within the same communication session. Such relationships are often indicative of application behavior. For example, in a video streaming flow, a small request BURST from the client is typically followed by a large response BURST from the server containing video data. By learning to distinguish whether two BURSTs originate from the same flow or from unrelated flows, the model is encouraged to encode inter-BURST interaction patterns, including request-response coupling, protocol handshake structure, and transactional rhythms that are invariant to payload encryption. These flow-level semantics are dificult to capture using packet-level or intra-BURST prediction objectives alone, yet they are critical for representing complex encrypted tunnels such as TLS 1.3 and Tor trafic.

Concretely, the BCP task is formulated as a binary classification problem. As illustrated in the lower part of Fig. 2, during pre-training, two BURSTs are randomly selected to form a BURST pair. These paired BURSTs are labeled as $B U R S T – a$ and BURST-b through segment embedding. With a probability of 50%, BURST-b is sampled from the same flow as $B U R S T – a ;$ otherwise, it is sampled from a diferent flow. Given a BURST pair $B _ { i } = ( { \mathrm { B U R S T } } { \mathrm { - a } } _ { i }$ BURST-b<sub>i</sub>) and its groundtruth label $y _ { i } \in \{ 0 , 1 \}$ , where $y _ { i } ~ = ~ 1$ indicates that the two BURSTs originate from the same flow, the loss function of the BCP task is defined as:

$$
L _ {B C P} = - \sum_ {i = 1} ^ {n} \log (P (1 - y _ {i} | B _ {i}; \theta))\tag{2}
$$

In the end, as shown in Equation 3, a weighted sum of $L _ { M B M }$ and $L _ { B C P }$ is used as the final loss function for pre-training. Here, λ is a hyperparameter for balancing the loss values of the two tasks.

$$
L = \lambda * L _ {M B M} + L _ {B C P}\tag{3}
$$

In essence, the MBM task learns the syntax of trafic (the structure of individual BURSTs), while the BCP task learns the storyline (how BURSTs logically connect to form a meaningful flow). Their combination provides a robust and general-purpose representation for encrypted trafic flows.

## C. Contrast Learning Stage

In traditional methods based on pre-training techniques, they usually perform fine-tuning by first initializing with the parameters of the pre-trained model and then continue to train on the data of the specific task. Unlike these methods, we use the trained model as a feature extractor to get robust initial feature vector representations for trafic flows and these feature vectors are further used as the input for contrast learning. This decoupled two-stage formulation provides superior scalability in practical deployment, because it avoids repeatedly finetuning the large pre-trained backbone and enables eficient updates through retraining only the small contrastive module when new classes emerge. To be more specific, when the pretraining stage is finished, the parameters are frozen and the raw trafic data for contrast learning are processed into the same form as the pre-training stage. Through multi-layer nonlinear transformation, we obtain the last hidden state as inputs of the contrast learning stage.

1) Contrast Learning Strategy: Based on the feature representations output from the pre-trained model, this contrast learning module aims at learning a contrast embedding space where instances (i.e. trafic flows) have small intra-class scatter and big inter-class separation. To this end, give each paired training instances $( \hat { x } _ { i } = f ( x _ { i } ; \theta ) , \hat { x } _ { j } = f ( x _ { j } ; \theta ) )$ , where $x _ { i }$ and $x _ { j }$ denote raw trafic flows after preprocessing and $f ( \cdot ; \theta )$ is a nonlinear mapping modeled by the pre-trained model, the pair-wise feature distance metric of $( \hat { x } _ { i } , \hat { x } _ { j } )$ can be measured by computing the Euclidean distance between their feature representations in the contrast embedding space, which can be defined as follows:

![](images/e4d1aba26b0bb69bcda8bb83bf83b637df03700d7f5775f136a1dc12db5a8d96.jpg)  
Fig. 3. Illustration of our proposed contrast learning strategy. (a) original feature space. (b) contrast embedding space.

$$
D (\hat {x} _ {i}, \hat {x} _ {j}) = \| g (\hat {x} _ {i}; \hat {\theta}) - g (\hat {x} _ {j}; \hat {\theta}) \| _ {2}\tag{4}
$$

where $g ( \cdot ; \hat { \theta } )$ is modeled by a neural network.

In order to obtain more discriminative feature representations in the contrast embedding space, we expect that the distances between similar pairs are smaller than those between dissimilar pairs and there is a large margin between the similar pairs and dissimilar ones. In our supervised contrast learning paradigm, the similar and dissimilar pairs are constructed according to the trafic classes in the downstream tasks. Specifically, if two instances belong to the same trafic class, they will be considered a similar pair; otherwise, they will be considered a dissimilar pair. In addition, to avoid the problem of data imbalance, we downsample dissimilar pairs to match the number of similar pairs. In this regard, if $\hat { x } _ { i }$ and $\hat { x _ { j } }$ are from the same trafic class, their contrast embedding feature distance $D ( \hat { x } _ { i } , \hat { x } _ { j } )$ should be smaller than an up-margin $\tau _ { 1 } ;$ if $\hat { x } _ { i }$ and $\hat { x _ { j } }$ are from diferent trafic classes, $D ( \hat { x } _ { i } , \hat { x } _ { j } )$ should be bigger than a down-margin $\tau _ { 2 }$ . This can be formulated as:

$$
\left\{ \begin{array}{l} D ^ {2} (\hat {x} _ {i}, \hat {x} _ {j}) <   \tau_ {1}, y _ {i} = y _ {j} \\ D ^ {2} (\hat {x} _ {i}, \hat {x} _ {j}) > \tau_ {2}, y _ {i} \neq y _ {j} \end{array} \right.\tag{5}
$$

where $\tau _ { 2 }$ should be bigger than $\tau _ { 1 }$ to enforce the discriminative feature learning. Furthermore, we introduce an intermediate parameter τ to reduce the number of free parameters. Specifically, we set $\tau _ { 1 } = \tau - 1$ and $\tau _ { 2 } = \tau + 1$ , thus the constraint in (5) can be simplified as:

$$
1 - y _ {i j} (\tau - D ^ {2} (\hat {x} _ {i}, \hat {x} _ {j})) <   0\tag{6}
$$

where $y _ { i j }$ denotes whether the paired instances $( \hat { x } _ { i } , \hat { x } _ { j } )$ come from the same class, which is defined as follows:

$$
y _ {i j} = \left\{ \begin{array}{l} 1, y _ {i} = y _ {j} \\ - 1, y _ {i} \neq y _ {j} \end{array} \right.\tag{7}
$$

An intuitive illustration of our proposed contrast learning strategy is shown in Fig. 3. It can be seen that, with the constrain in (6), there will be an explicit margin between the similar and dissimilar pairs in the learned contrast embedding space. Through imposing this constrain on each similar and dissimilar pair in the training set, we can define the loss function for contrast learning as follows:

$$
L _ {C L} = \sum_ {i, j} h (1 - y _ {i j} (\tau - \| g (\hat {x} _ {i}; \hat {\theta}) - g (\hat {x} _ {j}; \hat {\theta}) \| _ {2} ^ {2}))\tag{8}
$$

where $h ( x ) ~ = ~ m a x ( 0 , x )$ is the hinge loss function. It is worth noting that, thanks to the generic feature representations produced by the pre-trained model, only a small amount of instances need to be labeled (i.e. few-shot) for contrast learning to obtain a discriminative feature space which contributes to performing open-world classification.

2) Open-World Classification: In traditional pre-training based trafic classification methods, a classifier is commonly fine-tuned under a closed-world assumption where the number of possible labels associated with instances at evaluation stage is known and fixed. However, in real-world scenarios, this assumption does not hold. In our problem setting, instances from previously unknown categories may appear after the classifier is built. Inspired by the Nearest Mean Classifier utilized in [30], we compute a novelty class detection threshold $T _ { i }$ for each known class i to reject novel class’s instances and classify instances belonging to known classes. Here, to determine the optimum threshold value $T _ { i }$ for each class $i ,$ we assume that the instances of each class i follow a normal distribution in the contrast embedding space, characterized by a specific mean value $\mu _ { i }$ and variance value $\sigma _ { i } ^ { 2 }$ . Through applying the average intra-class distance with a narrow range of float, we obtain the threshold $T _ { i }$ for each class i. This can be formulated as:

$$
T _ {i} = \left(\frac {1}{\| M _ {i} \|} \sum_ {\hat {x} \in M _ {i}} \| g (\hat {x}; \hat {\theta}) - \mu_ {i} \| _ {2} ^ {2}\right) + \eta \sigma_ {i}\tag{9}
$$

where $M _ { i }$ is the training set of class i and $\lVert M _ { i } \rVert$ denotes the number of instances in $M _ { i } , \eta$ is a hyperparameter to control the classification boundary for each known class.

Finally, to predict the label $y _ { i }$ for a raw trafic flow $x _ { i } ,$ we first transform $x _ { i }$ through $f ( \cdot ; \theta )$ to get its initial feature representation ${ \hat { x } } _ { i } .$ . Then, we further project $\hat { x } _ { i }$ to the contrast embedding space through $g ( \cdot ; \hat { \theta } )$ . In the contrast embedding space, we compute the distance set $\bar { D } _ { \hat { x } _ { i } , j }$ from $g ( \hat { x } _ { i } ; \hat { \theta } )$ to the class center of each known class $j .$ Lastly, we select the minimum distance min $\hat { D } _ { \hat { x } _ { i } , j }$ from $\hat { D } _ { \hat { x } _ { i } , j }$ and obtain the corresponding class label $y _ { j }$ . If min $\bar { D } _ { \hat { x } _ { i } , j }$ is less than the threshold $T _ { j } ,$ the predicted label for $x _ { i }$ is $y _ { j }$ . Otherwise, x<sub>i</sub> will be identified as an instance from novel class. This can be formulated as:

$$
y _ {i} = \left\{ \begin{array}{l l} a r g m i n \bar {D} _ {\hat {x} _ {i}, j}, & \text { if } m i n \bar {D} _ {\hat {x} _ {i}, j} <   T _ {j} \\ \text { j = 1,2,...,C } \\ - 1, & \text { otherwise } \end{array} \right.\tag{10}
$$

where $C$ is the number of known classes and −1 denotes the label of novel class.

## D. Theoretical Justification

This section provides the analytical foundation for our methodology, specifically addressing why SCL facilitates novelty detection. We formalize the open-world setting and derive a generalization bound based on class separation.

Setting. Let $\mathcal { P } _ { 1 } , . . . , \mathcal { P } _ { C }$ be the distributions of the C known classes, and $\mathcal { P } _ { \mathrm { n o v e 1 } }$ the unknown novel class distribution. At training time we observe n labeled instances from $\textstyle \bigcup _ { c = 1 } ^ { C } \mathcal { P } _ { c }$ only; $\mathcal { P } _ { \mathrm { n o v e l } }$ is revealed only at test time. Denote by $\Sigma _ { \mathrm { i n } } =$ $\begin{array} { r } { \mathbb { E } _ { c = 1 . . C } \mathbb { E } _ { x \sim \mathcal { P } _ { c } } \big [ ( g ( x ) - \mu _ { c } ) ( g ( x ) - \mu _ { c } ) ^ { \top } \big ] } \end{array}$ the intra-class covariance, and by $\Sigma _ { \mathrm { o u t } } \mathsf { \bar { \Pi } } = \mathbb { E } _ { c = 1 . . c } \mathsf { \bar { f } } ( \mu _ { c } - \bar { \mu } ) ( \mu _ { c } - \bar { \mu } ) ^ { \top } \bigr ]$ the inter-class covariance, where $\mu _ { c } = \mathbb { E } _ { x \sim \mathcal { P } _ { c } } [ g ( x ) ]$ and $\bar { \mu } = \mathbf { \bar { \mathcal { E } } } _ { c = 1 . . C } [ \mu _ { c } ]$

Proposition 1: Assume $\Sigma _ { \mathrm { i n } } \preceq \bar { \lambda } \Sigma _ { \mathrm { o u t } }$ with $\bar { \lambda } < 1$ . Then the expected 0-1 risk of the nearest-mean classifier h satisfies

$$
\mathcal {R} (h) \leq \mathcal {R} _ {\mathrm{OW}} ^ {*} + \frac {4 \bar {\lambda} \operatorname{Tr} (\Sigma_ {\text { out }})}{\tau^ {2}} + \mathcal {O} \left(\frac {d \log n}{n}\right)\tag{11}
$$

where ${ \mathcal { R } } _ { \mathrm { { O W } } } ^ { * }$ is the minimum attainable risk under the above open-world protocol, d the embedding dimension, and τ the margin in (8).

Proof: For any test sample x drawn from one of the $C + 1$ distributions, define the margin

$$
\gamma (x) = \min _ {c ^ {\prime} \in \{1, \dots , C, \text {novel} \}} \left(\| g (x) - \mu_ {c ^ {\prime}} \| - \| g (x) - \mu_ {c} \|\right)\tag{12}
$$

where c is the true class of x. A classification error occurs if and only if $\gamma ( x ) < 0$ . By Chebyshev’s inequality,

$$
\mathbb {P} (\gamma <   0) \leq \frac {\operatorname{Var} (\gamma)}{(\mathbb {E} \gamma) ^ {2}}\tag{13}
$$

Under the covariance assumption $\Sigma _ { \mathrm { i n } } \preceq \bar { \lambda } \Sigma _ { \mathrm { o u t } }$ we have

$$
\operatorname{Var} (\gamma) \leq 4 \operatorname{Tr} \left(\Sigma_ {\text {in}}\right) \leq 4 \bar {\lambda} \operatorname{Tr} \left(\Sigma_ {\text {out}}\right)\tag{14}
$$

The margin loss (8) drives the embedding such that $\mathbb { E } \gamma \geq \tau$ in population. With finite instances we only achieve $\mathbb { E } \gamma \geq \tau -$ $\varepsilon ( n )$ , where $\varepsilon ( n ) = \mathcal { O } \big ( \sqrt { d / n } \big )$ is the uniform-deviation bound yielded by the Rademacher complexity of the d-dimensional linear nearest-mean rule [3]. Inserting this lower bound into Chebyshev’s inequality gives

$$
\begin{array}{l} \mathbb {P} (\gamma <   0) \leq \frac {\operatorname{Var} (\gamma)}{(\mathbb {E} \gamma) ^ {2}} \leq \frac {4 \bar {\lambda} \operatorname{Tr} (\Sigma_ {\text {out}})}{(\tau - \varepsilon (n)) ^ {2}} \\ = \frac {4 \bar {\lambda} \operatorname{Tr} (\Sigma_ {\text {out}})}{\tau^ {2}} \left(1 + \mathcal {O} \left(\frac {\varepsilon (n)}{\tau}\right)\right) \\ = \frac {4 \bar {\lambda} \operatorname{Tr} (\Sigma_ {\text {out}})}{\tau^ {2}} + \mathcal {O} \left(\frac {d \log n}{n}\right) \end{array}\tag{15}
$$

where the last step uses $\varepsilon ( n ) = \mathcal { O } ( \sqrt { d / n } )$ and Taylor expansion under $\varepsilon ( n ) \ll \tau$ . Since $\mathcal { R } ( h ) - \mathcal { R } _ { \mathrm { O W } } ^ { * } \leq \mathbb { P } ( \gamma < 0 )$ , the proposition follows. 

Interpretation. The MBM+BCP pre-training furnishes generic and robust initial embeddings in which contrastive learning can sculpt a highly discriminative space; empirically, this yields intra-class covariance $\Sigma _ { \mathrm { i n } }$ that is markedly smaller than inter-class covariance $\Sigma _ { \mathrm { o u t } }$ . The derived bound confirms that this compactness, which captured by a small ${ \bar { \lambda } } ,$ directly tightens the risk upper-bound for the nearest-mean classifier, all without requiring any novel class instances during training.

## IV. EXPERIMENTAL SETUP

## A. Datasets and Tasks

We conduct five encrypted trafic classification tasks based on seven public available datasets to evaluate our approach.

The overall statistics and description about the tasks and the corresponding datasets are shown in Table II. Before using these datasets, we remove packets that are irrelevant to actual data transmission, such as packets using ARP protocol and DHCP protocol. In addition, to avoid model bias caused by strong correlation information in each trafic flow, we remove the Ethernet header, the IP address from the IP header and the protocol port from the TCP/UDP header.

## B. Datasets Usage Settings

• Pre-training Dataset. We select approximately 10GB of unlabeled trafic data from the ISCX-VPN [14] dataset for pretraining. This dataset provides network trafic captured from popular applications, including Skype, YouTube, Facebook, and others. It includes both VPN and non-VPN trafic, ofering a balanced representation of encrypted and unencrypted scenarios.

• Closed-world Settings. To verify the efectiveness of our approach and compare with other baseline studies in closedworld scenario, each dataset is randomly divided into the training set, the validation set and the test set in a ratio of 8: 1: 1. Among them, the training set is used to conduct contrast learning and the validation set is used for optimal hyperparameter selection and the test set is used to measure the quality of classification results.

• Open-world Settings. Similarly, to verify the efectiveness of various methods in open-world scenario, we make the follow settings: for each dataset, 80% of the classes are randomly selected as known classes, while the remaining 20% are designated as novel classes. The instances from the known classes are further divided into the training set, the validation set, and the test set in a ratio of 8: 1: 1. The test set of the known classes combined with all instances from the novel classes constitutes the complete test set.

## C. Implementation

We implemented our approach on a server equipped with one NVIDIA RTX4090-24G GPU and an AMD 7542 CPU (14 vCPUs), 112 GB of memory. The main network architecture of pre-training model consists of multiple layers of bidirectional Transformer blocks, each composed of multi-head self-attention layers [44]. In detail, the network is composed of 12 Transformer blocks, with each self-attention layer including 12 attention heads. We set the dimension of each input token to 128, and the number of input tokens is 512. In the pretraining stage, we set the balancing coeficient λ to 1. The batch size is set to 32 and the total steps is set to 500 000. The learning rate is $2 \times 1 0 ^ { - 5 }$ , and the warmup ratio is 0.1. A residual network architecture is applied for conducting contrast learning. Specifically, the network consists of four residual blocks, where each block contains 2 convolutional layers, followed by a skip connection that allows the input to bypass the convolutional operations and be added directly to the output. In the contrast learning stage, we set the batch size to 32, the total epochs to 20 and the learning rate to 0.001. In addition, the margin τ is set to 5, and the threshold adjustment coeficient η is set to 2, both of which are determined through optimal hyperparameter search on the validation set of the EMC task. These values are fixed for all subsequent experiments.

TABLE II  
OVERVIEW OF THE TASKS AND DATASETS. THE DESCRIPTION OF EACH TASK IS DETAILED IN THE DESCRIPTION COLUMN

<table><tr><td>Task</td><td>Dataset</td><td>#Flow</td><td>#Label</td><td>Description</td></tr><tr><td>GEAC</td><td>Cross-Platform (iOS) [43]Cross-Platform (Android) [43]</td><td>20,85827,846</td><td>196215</td><td>The General Encrypted Application Classification (GEAC) task is focused on classifying application traffic that is encrypted using standard protocols. This task is conducted on two datasets which contain 196 and 215 applications respectively.</td></tr><tr><td>EMC</td><td>USTC-TFC [45]</td><td>9,853</td><td>20</td><td>The Encrypted Malware Classification (EMC) task focuses on classifying encrypted traffic originating from both malware and benign applications. This task is conducted on USTC-TFC dataset which contains 10 malware and 10 benign applications.</td></tr><tr><td>ETCV</td><td>ISCX-VPN (Service) [14]ISCX-VPN (App) [14]</td><td>3,4862,204</td><td>513</td><td>The Encrypted Traffic Classification on VPN (ETCV) task aims to classify encrypted traffic transmitting over Virtual Private Networks (VPNs). This task is conducted on ISCX-VPN dataset, which includes traffic captured from VPNs. This dataset is categorized into ISCX-VPN(Service), with 5 service categories, and ISCX-VPN(App), with 13 application categories.</td></tr><tr><td>EACT</td><td>ISCX-Tor [22]</td><td>3,122</td><td>16</td><td>The Encrypted Application Classification on Tor (EACT) task focuses on classifying encrypted traffic transmitting over Tor network. This task is conducted on ISCX-Tor dataset, which includes traffic from 16 applications. Tor&#x27;s distributed routing makes encrypted traffic classification more challenging.</td></tr><tr><td>EAC-1.3</td><td>CSTNET-TLS 1.3 [25]</td><td>46,372</td><td>120</td><td>The Encrypted Application Classification on TLS 1.3 (EAC-1.3) task aims to classify encrypted traffic using the TLS 1.3 protocol. This task is conducted on CSTNET-TLS 1.3 dataset, which contains traffic data from 120 websites using TLS 1.3 protocol.</td></tr></table>

TABLE III

PERFORMANCE METRICS FOR DIFFERENT TASKS WITH VARYING K-SHOTS IN CLOSED-WORLD SETTING

<table><tr><td>Tasks</td><td colspan="4">GEAC</td><td colspan="4">EMC</td><td colspan="4">ETCV</td><td colspan="4">EACT</td><td colspan="4">EAC-1.3</td></tr><tr><td>K</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>K=1</td><td>0.188</td><td>0.204</td><td>0.128</td><td>0.151</td><td>0.509</td><td>0.489</td><td>0.456</td><td>0.469</td><td>0.447</td><td>0.389</td><td>0.486</td><td>0.427</td><td>0.451</td><td>0.402</td><td>0.366</td><td>0.376</td><td>0.231</td><td>0.221</td><td>0.198</td><td>0.202</td></tr><tr><td>K=10</td><td>0.505</td><td>0.494</td><td>0.418</td><td>0.449</td><td>0.893</td><td>0.868</td><td>0.805</td><td>0.831</td><td>0.749</td><td>0.711</td><td>0.707</td><td>0.709</td><td>0.803</td><td>0.798</td><td>0.757</td><td>0.772</td><td>0.686</td><td>0.641</td><td>0.612</td><td>0.620</td></tr><tr><td>K=20</td><td>0.653</td><td>0.582</td><td>0.549</td><td>0.551</td><td>0.974</td><td>0.975</td><td>0.973</td><td>0.974</td><td>0.882</td><td>0.861</td><td>0.827</td><td>0.839</td><td>0.945</td><td>0.946</td><td>0.939</td><td>0.940</td><td>0.818</td><td>0.815</td><td>0.811</td><td>0.812</td></tr><tr><td>K=50</td><td>0.661</td><td>0.602</td><td>0.568</td><td>0.574</td><td>0.983</td><td>0.986</td><td>0.982</td><td>0.983</td><td>0.908</td><td>0.902</td><td>0.896</td><td>0.898</td><td>0.962</td><td>0.959</td><td>0.963</td><td>0.959</td><td>0.837</td><td>0.832</td><td>0.824</td><td>0.829</td></tr><tr><td>K=100</td><td>0.708</td><td>0.645</td><td>0.601</td><td>0.606</td><td>0.993</td><td>0.994</td><td>0.992</td><td>0.992</td><td>0.926</td><td>0.919</td><td>0.910</td><td>0.912</td><td>0.989</td><td>0.986</td><td>0.979</td><td>0.980</td><td>0.876</td><td>0.863</td><td>0.849</td><td>0.852</td></tr></table>

## V. EVALUATION

In this section, we evaluate our approach on five encrypted trafic classification tasks to answer the following questions:

• RQ1: How efective is our approach under diferent k-shot settings?

• RQ2: How does our approach compare to existing methods under both closed-world and open-world settings?

• RQ3: Is the proposed components efective in enhancing the overall performance?

• RQ4: Do the two proposed pre-training tasks contribute to learning generic and robust feature representations, rather than simply benefiting from increased model capacity?

• RQ5: How does our approach perform in terms of time overhead and system resource consumption?

## A. Evaluation Metrics

We assess and compare the performance of the various methods through four typical metrics, including Accuracy (AC), Precision (PR), Recall (RC), and F1 score. To avoid biases caused by data imbalance, we calculate macro average for each metric. Moreover, for the GEAC task, we report the macro average results across the Cross-Platform (iOS) and Cross-Platform (Android) datasets for brevity. Similarly, for the ETCV task, we provide the macro average over the ISCX-VPN (Service) and ISCX-VPN (App) datasets.

## B. K-Shot Classification

In this section, we demonstrate the performance of our approach under diferent K-shot settings. We verify it on both closed-world and open-world scenarios. Here, the symbol K in K-shot is not the absolute number of instances in each class used for training. Instead, K means K% of instances are randomly selected from each class of the training set to conduct contrast learning (e.g. 10-shot indicates that we randomly select 10% of instances from each class in training set). The results are detailed in Table III and Table IV.

Closed-world: As shown in Table III, when K = 1, the performance across all the five tasks is worst because too few training instances contain limited information about the diversity of encrypted trafic, which leads to the model being in an under-fitting state. As the value of K increases, the classification performance is becoming better and better. This is not surprising since more information of the training classes is incorporated into the training phase as K increases. Specifically, as K grows to 10, the F1 score improves to 0.449, 0.831, 0.709, 0.772 and 0.620 respectively on the five tasks. When K reaches 20, the classification performance can be close to the optimal results achieved in K = 100, with the F1 score gaps only 9.08%, 1.81%, 8.00%, 4.08% and 4.69% respectively across the five tasks. This can be attributed to the generic initial feature representations obtained from the customized pre-training model for trafic flows. These representations enable the subsequent contrast learning task to learn discriminative features even with only a few instances. The classification performance of GEAC task is relatively low (i.e., F1 score is 0.606 when K = 100 and 0.551 when

TABLE IV  
PERFORMANCE METRICS FOR DIFFERENT TASKS WITH VARYING K-SHOTS IN OPEN-WORLD SETTING

<table><tr><td>Tasks</td><td colspan="4">GEAC</td><td colspan="4">EMC</td><td colspan="4">ETCV</td><td colspan="4">EACT</td><td colspan="4">EAC-1.3</td></tr><tr><td>K</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>K=1</td><td>0.167</td><td>0.185</td><td>0.122</td><td>0.149</td><td>0.431</td><td>0.422</td><td>0.401</td><td>0.406</td><td>0.345</td><td>0.357</td><td>0.296</td><td>0.311</td><td>0.281</td><td>0.295</td><td>0.306</td><td>0.295</td><td>0.190</td><td>0.191</td><td>0.183</td><td>0.179</td></tr><tr><td>K=10</td><td>0.416</td><td>0.424</td><td>0.388</td><td>0.401</td><td>0.801</td><td>0.808</td><td>0.791</td><td>0.793</td><td>0.638</td><td>0.621</td><td>0.589</td><td>0.608</td><td>0.747</td><td>0.738</td><td>0.746</td><td>0.739</td><td>0.602</td><td>0.591</td><td>0.562</td><td>0.571</td></tr><tr><td>K=20</td><td>0.619</td><td>0.579</td><td>0.538</td><td>0.545</td><td>0.922</td><td>0.925</td><td>0.920</td><td>0.921</td><td>0.831</td><td>0.819</td><td>0.808</td><td>0.812</td><td>0.905</td><td>0.908</td><td>0.911</td><td>0.903</td><td>0.751</td><td>0.718</td><td>0.739</td><td>0.724</td></tr><tr><td>K=50</td><td>0.634</td><td>0.599</td><td>0.555</td><td>0.562</td><td>0.943</td><td>0.944</td><td>0.942</td><td>0.941</td><td>0.855</td><td>0.842</td><td>0.830</td><td>0.831</td><td>0.932</td><td>0.929</td><td>0.933</td><td>0.928</td><td>0.782</td><td>0.791</td><td>0.784</td><td>0.785</td></tr><tr><td>K=100</td><td>0.683</td><td>0.612</td><td>0.582</td><td>0.590</td><td>0.962</td><td>0.959</td><td>0.963</td><td>0.959</td><td>0.905</td><td>0.900</td><td>0.861</td><td>0.873</td><td>0.957</td><td>0.951</td><td>0.961</td><td>0.952</td><td>0.829</td><td>0.831</td><td>0.811</td><td>0.819</td></tr></table>

K = 20). Apart from the large number of categories of GEAC task, we analyze the reasons for the category similarities, which contribute to the task’s dificulty, including: (1) Similar application behaviors—applications of same type (e.g. stream media applications such as Youku, Tencent Video, iQiyi etc. or social media applications such as Wechat, QQ etc.) exhibit overlapping trafic patterns and similar burst characteristics (e.g., frequent, short bursts for messaging), reducing inter-class discriminability. (2) Shared third-party domains—multiple applications connect to common third-party domains for shared services, such as googleadservices.com for advertising, appsflyer.com for mobile attribution and marketing analytics, and googleapis.com for various Google API services, further blurring category boundaries. However, although the classification accuracy is lower compared to other tasks, we still achieved the best results compared to other related works, which is discussed in section V-C.

Open-world: As shown in Table IV, compared to the closed-world setting, the classification performance has slightly decreased in the open-world setting, e.g., 2.64%, 3.33%, 4.28%, 2.86% and 3.87% decrease in F1 score respectively across the five tasks when K = 100. This decrease is in accordance with expectation because open-world classification requires model to obtain more discriminative features and has stronger generalization ability. Specifically, in the closed-world setting, the training set and test set both come from known categories, so the model is easy to learn the characteristics of each category and achieve good results on the test set. In comparison, in the open-world scenario, the model should have the ability to adapt to the instances of unknown categories. However, it is worth noting that our approach still achieves high classification performance across the five tasks when K reaches 20 (i.e., F1 scores of 0.545, 0.921, 0.812, 0.903, 0.724) and it achieves the best results with F1 scores of 0.590, 0.959, 0.873, 0.952 and 0.819 when K = 100. To demonstrate the advantage of our approach for few-shot encrypted trafic classification, we will mainly compare the results obtained at K = 20 with baselines in the following sections.

## C. Comparison Under Closed-World Setting

For the comparison under the closed-world setting, we evaluate a diverse set of baselines, comprising two MLbased methods: AppScanner [42] and BIND [32], two DL-based methods: FS-Net [26] and Deeppacket [29], and four pre-training based methods: PERT [18], ET-BERT [25], TraficFormer [54], and TraficLLM [6]. Since these methods are not optimized for few-shot learning, we train them on the entire training set for each task to demonstrate their best performance. For pre-training based approaches, we adhere to the dataset selection protocols outlined in their respective papers. Additionally, we incorporate three recent few-shot learning methods–FC-Net [46], MetaMRE [48], and FS-MTC [49]–evaluated under a consistent 20-shot condition for fair comparison. The experimental results are shown in Table V.

• GEAC Task. The results for the GEAC task are shown in the leftmost part of Table V, We can observe that the pre-training based methods are consistently better than both ML-based and DL-based methods. The reason is that the pretraining based methods obtain essential packet or flow features from large-scale unlabeled trafic data which contributes a lot to the built of target classifier. Among all pre-training based methods, PERT has the worst performance since it has not designed specific task to learn the transmission structure of trafic. ET-BERT and TraficFormer perform better than PERT by respectively introducing well-designed pre-training task for trafic feature learning. TraficLLM, which uses LLMs for generic trafic representation, achieves competitive results but underperforms TraficFormer in this task, with an F1 score of 0.522 compared to 0.543. Our approach surpasses the stateof-the-art TraficFormer by 1.47% in F1 score, highlighting the eficacy of contrast learning in enhancing feature discriminability across trafic categories. Among few-shot methods, FC-Net, MetaMRE, and FS-MTC exhibit poor performance (F1 scores below 0.370, approximately 49.32% lower than ours), highlighting their limited capacity to learn discriminative features from small datasets when dealing with large, similar trafic categories.

• EMC Task. The results for the EMC task are shown in the second column group of Table V. In this task, the pre-training based methods are also superior to those of ML-based and DL-based ones. PERT still performs worst in all pre-training methods. TraficLLM performs strongly, achieving an F1 score of 0.982, close to TraficFormer’s 0.983, benefiting from its LLM-based representation learning for malware trafic patterns. Our approach achieves marginal improvements of 0.10% across all metrics compared to ET-BERT but lags behind TrafficFormer by 0.81%, 0.91%, 1.02%, and 0.91% in accuracy, precision, recall, and F1 score, respectively. However, with 50% of training instances (K = 50) incorporated into our contrastive model, performance aligns with TraficFormer, and with 100% incorporation, it exceeds TraficFormer by 1.12%, 1.02%, 0.91%, and 0.91% in the respective metrics. The strong performance of baselines may be attributed to unencrypted trafic in the malware dataset, providing additional plaintext information. Among few-shot methods, FC-Net and

TABLE V  
THE RESULTS OF DIFFERENT APPROACHES ON GEAC, EMC, ETCV, EACT AND EAC-1.3 TASKS UNDER CLOSED-WORLD SETTING

<table><tr><td rowspan="2">Tasks Approaches</td><td colspan="4">GEAC</td><td colspan="4">EMC</td><td colspan="4">ETCV</td><td colspan="4">EACT</td><td colspan="4">EAC-1.3</td></tr><tr><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>Appscanner [42]</td><td>0.416</td><td>0.490</td><td>0.354</td><td>0.395</td><td>0.894</td><td>0.898</td><td>0.897</td><td>0.889</td><td>0.673</td><td>0.610</td><td>0.621</td><td>0.612</td><td>0.672</td><td>0.468</td><td>0.442</td><td>0.445</td><td>0.616</td><td>0.624</td><td>0.633</td><td>0.620</td></tr><tr><td>BIND [32]</td><td>0.303</td><td>0.279</td><td>0.271</td><td>0.252</td><td>0.846</td><td>0.868</td><td>0.838</td><td>0.839</td><td>0.715</td><td>0.637</td><td>0.632</td><td>0.633</td><td>0.718</td><td>0.460</td><td>0.452</td><td>0.451</td><td>0.796</td><td>0.781</td><td>0.745</td><td>0.751</td></tr><tr><td>FS-Net [26]</td><td>0.431</td><td>0.321</td><td>0.307</td><td>0.301</td><td>0.885</td><td>0.885</td><td>0.892</td><td>0.884</td><td>0.693</td><td>0.616</td><td>0.604</td><td>0.606</td><td>0.607</td><td>0.508</td><td>0.535</td><td>0.459</td><td>0.793</td><td>0.799</td><td>0.788</td><td>0.791</td></tr><tr><td>Deeppacket [29]</td><td>0.399</td><td>0.346</td><td>0.419</td><td>0.357</td><td>0.814</td><td>0.815</td><td>0.813</td><td>0.812</td><td>0.703</td><td>0.662</td><td>0.674</td><td>0.658</td><td>0.745</td><td>0.755</td><td>0.740</td><td>0.742</td><td>0.402</td><td>0.432</td><td>0.269</td><td>0.399</td></tr><tr><td>PERT [18]</td><td>0.612</td><td>0.524</td><td>0.508</td><td>0.512</td><td>0.967</td><td>0.970</td><td>0.965</td><td>0.966</td><td>0.786</td><td>0.716</td><td>0.721</td><td>0.705</td><td>0.768</td><td>0.442</td><td>0.445</td><td>0.435</td><td>0.801</td><td>0.716</td><td>0.767</td><td>0.723</td></tr><tr><td>ET-BERT [25]</td><td>0.625</td><td>0.545</td><td>0.516</td><td>0.516</td><td>0.970</td><td>0.974</td><td>0.972</td><td>0.973</td><td>0.871</td><td>0.812</td><td>0.828</td><td>0.814</td><td>0.831</td><td>0.556</td><td>0.645</td><td>0.589</td><td>0.812</td><td>0.799</td><td>0.789</td><td>0.788</td></tr><tr><td>TrafficFormer [54]</td><td>0.667</td><td>0.570</td><td>0.545</td><td>0.543</td><td>0.982</td><td>0.984</td><td>0.983</td><td>0.983</td><td>0.876</td><td>0.858</td><td>0.825</td><td>0.836</td><td>0.922</td><td>0.915</td><td>0.909</td><td>0.911</td><td>0.848</td><td>0.837</td><td>0.835</td><td>0.834</td></tr><tr><td>TrafficLLM [6]</td><td>0.619</td><td>0.521</td><td>0.532</td><td>0.522</td><td>0.984</td><td>0.985</td><td>0.979</td><td>0.982</td><td>0.883</td><td>0.856</td><td>0.832</td><td>0.838</td><td>0.942</td><td>0.933</td><td>0.910</td><td>0.928</td><td>0.816</td><td>0.813</td><td>0.795</td><td>0.801</td></tr><tr><td>FC-Net [46]</td><td>0.416</td><td>0.352</td><td>0.301</td><td>0.313</td><td>0.877</td><td>0.852</td><td>0.846</td><td>0.848</td><td>0.695</td><td>0.699</td><td>0.598</td><td>0.636</td><td>0.601</td><td>0.511</td><td>0.565</td><td>0.518</td><td>0.556</td><td>0.522</td><td>0.493</td><td>0.499</td></tr><tr><td>MetaMRE [48]</td><td>0.424</td><td>0.391</td><td>0.322</td><td>0.341</td><td>0.886</td><td>0.881</td><td>0.837</td><td>0.853</td><td>0.761</td><td>0.789</td><td>0.626</td><td>0.703</td><td>0.666</td><td>0.603</td><td>0.507</td><td>0.524</td><td>0.588</td><td>0.571</td><td>0.555</td><td>0.559</td></tr><tr><td>FS-MTC [49]</td><td>0.431</td><td>0.387</td><td>0.368</td><td>0.369</td><td>0.922</td><td>0.928</td><td>0.879</td><td>0.904</td><td>0.744</td><td>0.749</td><td>0.602</td><td>0.661</td><td>0.802</td><td>0.778</td><td>0.738</td><td>0.757</td><td>0.592</td><td>0.547</td><td>0.583</td><td>0.568</td></tr><tr><td>Ours</td><td>0.653</td><td>0.582</td><td>0.549</td><td>0.551</td><td>0.974</td><td>0.975</td><td>0.973</td><td>0.974</td><td>0.882</td><td>0.861</td><td>0.827</td><td>0.839</td><td>0.945</td><td>0.946</td><td>0.939</td><td>0.940</td><td>0.818</td><td>0.815</td><td>0.811</td><td>0.812</td></tr><tr><td>Ours:100-shot</td><td>0.708</td><td>0.645</td><td>0.601</td><td>0.606</td><td>0.993</td><td>0.994</td><td>0.992</td><td>0.992</td><td>0.926</td><td>0.919</td><td>0.910</td><td>0.912</td><td>0.989</td><td>0.986</td><td>0.979</td><td>0.980</td><td>0.876</td><td>0.863</td><td>0.849</td><td>0.852</td></tr></table>

MetaMRE achieve performance comparable to ML- and DL-based approaches but remain inferior to pre-training-based methods. FS-MTC, benefiting from preliminary knowledge derived from auxiliary dataset, achieves a higher F1 score than FC-Net and MetaMRE, yet still trails our method by 7.74%.

• ETCV Task. The results for the ETCV task are shown in the third column group of Table V, from where we can see that the classification performance of ML-based methods and DL-based methods is comparable and consistently inferior to that of the pre-training based methods. Among the baselines, TraficLLM achieves F1 = 0 838 and TraficFormer achieves 0.836, both of which are comparable to our method (F1 = 0 839). Nevertheless, with 100-shot data, the F1 score of our method rises to 0.912, which surpasses TraficLLM and TraficFormer by 8.83% and 9.09% respectively. Fewshot methods such as MetaMRE $( \mathrm { F } 1 = 0 . 7 0 3 )$ and FS-MTC (F1 = 0 661) remain notably below pre-training based methods (i.e., 19.34% lower than ours), confirming the importance of large-scale representation learning for imbalanced datasets like ETCV task. In addition, our contrast learning strategy further mitigates the problem of class imbalance by emphasizing instance similarity in the embedding space, improving representation of minority classes.

• EACT Task. The results for the EACT task, shown in the fourth column group of Table V, highlight poor performance across most baselines except TraficFormer and TraficLLM, due to Tor’s multi-layer encryption and routing, which obscure consistent patterns. Trafic features like packet size and timing, relied upon by ML-based methods, are rendered inefective. TraficFormer applies a trafic data augmentation method to reduce the model’s reliance on irrelevant information and enrich the training instances, which contributes a lot to the classification performance. TraficLLM excels with an F1 score of 0.928, outperforming other baselines, thanks to its LLM-driven contextual representation for anonymized trafic. Our approach achieves 0.940, improving over TraficFormer and TraficLLM by 3.18% and 1.29% respectively. With 100-shot instances, our method further rises to 0.980, which is 6.95% higher than TraficFormer and 5.60% higher than TraficLLM. In contrast, few-shot baselines (e.g., MetaMRE 0.524, FC-Net 0.518) lag significantly, highlighting the advantage of pre-training combined with contrast learning under heavy obfuscation conditions.

• EAC-1.3 Task. The results for the EAC-1.3 task are shown in the rightmost part in Table V. Our approach performs better than all ML-based and DL-based methods. It improves by 8.12% and 2.65% in F1 score over the best ML-based method BIND and DL-based method FS-Net respectively. Among pre-training methods, we surpass PERT and ET-BERT with gains of 8.9% and 2.4% in F1 score, respectively. TraficLLM (F1 = 0 801) performs competitively but falls short of TraficFormer (F1 = 0 834) by 3.3%, while our method narrows this gap, trailing TraficFormer by 2.2%. With full training data (100-shot), our approach further excels, surpassing TraficFormer by 2.16% in F1 score. The slight underperformance under 20-shot conditions is justified by the practical costs of trafic labeling. Among few-shot methods, they exhibit significant performance gaps. While FS-MTC, benefiting from auxiliary dataset, achieves the best results, it still underperforms our method by 24.4%, highlighting the inherent limitations of existing few-shot approaches in handling large volumes of TLS 1.3 trafic–where they struggle to learn suficiently discriminative features.

## D. Comparison Under Open-World Setting

We select eight baselines for the comparison in open-world setting. Among these baselines, there are three ML-based methods: Whisper [12], FOSS [52], ProGraph [23], three DL-based methods: Prototype [50], K-LND [7], Trident [53], and two pre-training based methods: OWCP [24] and TrafficGPT [15]. It is worth noting that Whisper [12] does not possess multi-class classification capabilities. However, given its ability to detect unknown categories, it is still included as a comparative baseline. All evaluation metrics of Whisper are reported under the binary classification setting of known categories versus novel categories. We train all baseline models on the entire training set for each task to show their best performance. The experimental results are shown in Tables VI. Whisper demonstrates strengths in detecting unknown categories with F1 scores ranging from 0.477 to 0.903 across tasks, leveraging frequency domain analysis for robust realtime detection, but its lack of multi-class support limits its applicability in complex open-world scenarios. The following analysis will primarily focus on comparisons with other baselines in the multi-class context.

TABLE VI  
THE RESULTS OF DIFFERENT APPROACHES ON GEAC, EMC, ETCV, EACT AND EAC-1.3 TASKS UNDER OPEN-WORLD SETTING

<table><tr><td rowspan="2">Tasks Approaches</td><td colspan="4">GEAC</td><td colspan="4">EMC</td><td colspan="4">ETCV</td><td colspan="4">EACT</td><td colspan="4">EAC-1.3</td></tr><tr><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>Whisper [12]</td><td>0.502</td><td>0.488</td><td>0.475</td><td>0.477</td><td>0.911</td><td>0.914</td><td>0.896</td><td>0.903</td><td>0.812</td><td>0.806</td><td>0.798</td><td>0.801</td><td>0.867</td><td>0.858</td><td>0.836</td><td>0.842</td><td>0.762</td><td>0.728</td><td>0.746</td><td>0.733</td></tr><tr><td>FOSS [52]</td><td>0.393</td><td>0.344</td><td>0.305</td><td>0.311</td><td>0.798</td><td>0.807</td><td>0.754</td><td>0.766</td><td>0.615</td><td>0.606</td><td>0.589</td><td>0.595</td><td>0.686</td><td>0.701</td><td>0.637</td><td>0.645</td><td>0.494</td><td>0.488</td><td>0.465</td><td>0.469</td></tr><tr><td>ProGraph [23]</td><td>0.425</td><td>0.387</td><td>0.327</td><td>0.332</td><td>0.801</td><td>0.783</td><td>0.772</td><td>0.774</td><td>0.621</td><td>0.598</td><td>0.642</td><td>0.616</td><td>0.688</td><td>0.743</td><td>0.628</td><td>0.672</td><td>0.534</td><td>0.548</td><td>0.472</td><td>0.503</td></tr><tr><td>Prototype [50]</td><td>0.453</td><td>0.392</td><td>0.344</td><td>0.359</td><td>0.821</td><td>0.833</td><td>0.826</td><td>0.828</td><td>0.777</td><td>0.782</td><td>0.756</td><td>0.766</td><td>0.801</td><td>0.789</td><td>0.703</td><td>0.718</td><td>0.622</td><td>0.613</td><td>0.591</td><td>0.595</td></tr><tr><td>k-LND [7]</td><td>0.389</td><td>0.321</td><td>0.288</td><td>0.294</td><td>0.810</td><td>0.819</td><td>0.813</td><td>0.814</td><td>0.723</td><td>0.716</td><td>0.701</td><td>0.707</td><td>0.705</td><td>0.664</td><td>0.622</td><td>0.631</td><td>0.511</td><td>0.498</td><td>0.486</td><td>0.488</td></tr><tr><td>Trident [53]</td><td>0.456</td><td>0.481</td><td>0.395</td><td>0.406</td><td>0.838</td><td>0.845</td><td>0.827</td><td>0.832</td><td>0.762</td><td>0.771</td><td>0.750</td><td>0.758</td><td>0.796</td><td>0.753</td><td>0.807</td><td>0.774</td><td>0.668</td><td>0.671</td><td>0.654</td><td>0.658</td></tr><tr><td>OWCP [24]</td><td>0.574</td><td>0.504</td><td>0.435</td><td>0.462</td><td>0.867</td><td>0.872</td><td>0.869</td><td>0.870</td><td>0.824</td><td>0.801</td><td>0.765</td><td>0.771</td><td>0.848</td><td>0.827</td><td>0.816</td><td>0.821</td><td>0.635</td><td>0.652</td><td>0.598</td><td>0.601</td></tr><tr><td>TrafficGPT [15]</td><td>0.604</td><td>0.594</td><td>0.494</td><td>0.528</td><td>0.902</td><td>0.909</td><td>0.898</td><td>0.901</td><td>0.832</td><td>0.815</td><td>0.801</td><td>0.808</td><td>0.819</td><td>0.816</td><td>0.805</td><td>0.808</td><td>0.742</td><td>0.715</td><td>0.733</td><td>0.719</td></tr><tr><td>Ours</td><td>0.619</td><td>0.579</td><td>0.538</td><td>0.545</td><td>0.922</td><td>0.925</td><td>0.920</td><td>0.921</td><td>0.831</td><td>0.819</td><td>0.808</td><td>0.812</td><td>0.905</td><td>0.908</td><td>0.911</td><td>0.903</td><td>0.751</td><td>0.718</td><td>0.739</td><td>0.724</td></tr><tr><td>Ours:100-shot</td><td>0.683</td><td>0.612</td><td>0.582</td><td>0.590</td><td>0.962</td><td>0.959</td><td>0.963</td><td>0.959</td><td>0.905</td><td>0.900</td><td>0.861</td><td>0.873</td><td>0.957</td><td>0.951</td><td>0.961</td><td>0.952</td><td>0.829</td><td>0.831</td><td>0.811</td><td>0.819</td></tr></table>

• GEAC Task (open). The results for the GEAC task are shown in the leftmost part of Table VI. The pretraining based methods demonstrate better results compared to ML-based and DL-based methods. This superiority suggests the necessity of obtaining robust feature representations from pre-trained models for the open-world classification task. For the pre-training based methods, our approach improves 7.84%, 14.88%, 23.68%, 17.97% in terms of accuracy, precision, recall and F1 score over OWCP. The reason for the poor performance of OWCP is that it synthesizes new instances that around the boundaries of known classes and use them as the training instances from novel class, but these synthesized instances may not conform to the actual novel class distribution. In contrast, we make no assumptions about the distribution of new classes; instead, we focus on learning more discriminative features based on the available instances from the known classes. Our approach perform better than TraficGPT in terms of accuracy (+ 2.48%), recall (+ 8.91%) and F1 score (+ 3.22%) but worse in precision (-2.53%). We attribute this to the insuficient training instances for contrast learning, as when 100% training instances are used (K = 100), the precision will be 3.03% higher than TraficGPT.

• EMC Task (open). The results for the EMC task are shown in the second column group of Table VI. Our approach achieves the best performance across all evaluation metrics, demonstrating its efectiveness in this domain. Specifically, it outperforms the best-performing DL-based method Trident by 10.69% in F1 score and surpasses the top pre-training based method TraficGPT by 2.22% in F1 score. These substantial improvements highlight the robustness and adaptability of our approach in handling the challenges associated with encrypted malware classification. The superior performance indicates that our method efectively captures discriminative features, enabling more accurate detection of known and novel malware. This underscores the potential of our approach as a valuable tool for real-world malware detection tasks.

• ETCV Task (open). The results for the ETCV task are shown in the third column group of Table VI. In this task, pre-training based methods demonstrate superior performance compared to the ML- and DL-based approaches. Specifically, our approach achieves improvements of 31.82%, 6.00% and 0.50% in F1 score over the state-of-the-art ML-based method Prograph, DL-based method Prototype and the pre-training based method TraficGPT respectively. Addressing the data imbalance challenge inherent to this task, our approach efectively mitigates the issue by: (1) capturing byte-level dependencies within BURSTs as well as the correlations between BURSTs, and (2) learning a similarity metric rather than directly searching for class boundaries. While our approach records a slightly lower accuracy (−0.12%) compared to TraficGPT, it is important to note that TraficGPT relies on dataset-specific fine-tuning in a closed-world setting to extract features prior to open-world classification. This process is less practical in real-world scenarios. By contrast, the generic feature representations derived from the pre-trained model in our approach are dataset-independent, making it more applicable to real-world situations and better aligned with practical requirements.

• EACT Task (open). The results for the EACT task are shown in the fourth column group of Table VI. Our approach achieves consistent improvements across all evaluation metrics, surpassing the existing best results obtained by OWCP by 6.72%, 9.79%, 11.64%, 9.99% in accuracy, precision, recall and F1 score respectively. This demonstrates the efectiveness of our method in addressing the challenges posed by multi-layer encrypted trafic. Such trafic introduces significant dificulties due to the obfuscation and encryption mechanisms inherent in the Tor protocol. OWCP tackles this challenge by firstly conducting contrastive pre-training to extract discriminative features and then synthesizing flows of novel class in the feature space to enrich the training instances. In contrast, we design explicit pre-training tasks to learn robust and generic feature representations that are better suited for encrypted trafic. These features are further refined and enhanced through a contrastive learning strategy, leading to improved discriminative capability. This combination enables our approach to handle the complexities of encrypted Tor trafic and perform open-world Tor trafic classification efectively.

• EAC-1.3 Task (open). The results for the EAC-1.3 task, presented in the rightmost part of Table VI, reveal that while pre-training methods typically lead, the DL-based method Trident surpasses the pre-training method OWCP by 9.48% in F1 score, benefiting from its decoupled one-class learning framework for fine-grained detection. Nevertheless, Trident still trails our approach by 10.03% in F1 score. Our approach outperforms the best baseline, TraficGPT, achieving improvements of 1.21%, 0.42%, 0.82%, and 0.69% in accuracy, precision, recall, and F1 score, respectively. These results suggest that our method’s ability to learn generic yet discriminative features through task-specific pre-training, combined with contrast learning strategies, allows it to generalize better to complex and highly encrypted trafic. Furthermore, the superiority of our approach highlights its practical value for handling real-world encrypted application classification tasks, especially under the constraints posed by modern encryption protocols such as TLS 1.3.

![](images/091e78cfe29b2d4f129ceaf61e5c321915703e10378c08fda12b272eba4d7e7b.jpg)  
(a) Original feature space

![](images/abe1ecaf78df37a73950d966a34372af1e0d285ad253544892aeb69666c9f577.jpg)  
(b) No-CL feature space

![](images/93cd013ff456757543b94a19f3996bbd1fa7cb99e1d82f2f66102ebbed95122d.jpg)  
(c) No-PT feature space

![](images/9536359af1c54d86687e502d93e5744688785a6c23cb9c1726a634648ad9094e.jpg)  
(d) Ours-Full feature space

Fig. 4. The visualization for trafic flows on EMC task in diferent feature space.  
TABLE VII  
ABLATION RESULTS ON EMC TASK

<table><tr><td rowspan="2">Settings Approaches</td><td colspan="4">closed-world</td><td colspan="4">open-world</td></tr><tr><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>No-PT</td><td>0.762</td><td>0.768</td><td>0.735</td><td>0.744</td><td>0.724</td><td>0.731</td><td>0.723</td><td>0.725</td></tr><tr><td>No-CL</td><td>0.532</td><td>0.575</td><td>0.498</td><td>0.521</td><td>0.455</td><td>0.482</td><td>0.437</td><td>0.451</td></tr><tr><td>ET-BERT+CL</td><td>0.968</td><td>0.965</td><td>0.963</td><td>0.964</td><td>0.918</td><td>0.914</td><td>0.912</td><td>0.913</td></tr><tr><td>TrafficFormer+CL</td><td>0.975</td><td>0.977</td><td>0.971</td><td>0.974</td><td>0.924</td><td>0.923</td><td>0.921</td><td>0.922</td></tr><tr><td>Ours</td><td>0.974</td><td>0.975</td><td>0.973</td><td>0.974</td><td>0.922</td><td>0.925</td><td>0.920</td><td>0.921</td></tr></table>

## E. Ablation Study

To address RQ3 and RQ4, we analyze the contributions of pre-training and contrast learning, and further examine the efectiveness of our two pre-training tasks as well as the impact of model capacity.

1) Impact of Components: To examine the impact of pre-training and contrast learning components, we set up four baselines as follows: (1) NO Pre-Training (NO-PT): raw bytes of the first 4 packets (32 bytes each) after sanitizing biased fields are used for contrast learning. (2) No Contrast Learning (NO-CL): applying our openworld classification on features from the pre-trained model. (3) ET-BERT+CL: replacing our pre-training model with ET-BERT. (4) TraficFormer+CL: replacing our pre-training model with TraficFormer.

Results on the EMC task (Table VII) show that methods combining both pre-training and contrast learning consistently outperform those using only one component, confirming their complementary roles. NO-CL yields the worst performance, indicating that contrast learning is crucial for obtaining discriminative representations. NO-PT performs better than NO-CL but still lags behind other baselines, showing that pre-training benefits generic feature extraction and facilitates subsequent discriminative learning. Compared with ET-BERT+CL, our approach improves F1 score by 1.04% and 0.88% in closed- and open-world settings, respectively. ET-BERT only considers intra-BURST correlations, whereas our MBM and BCP jointly capture both intra- and inter-BURST relationships. Our method also matches Trafic-Former+CL despite TraficFormer using a more complex SODF task, demonstrating that our simpler MBM+BCP design is both eficient and efective.

To provide a more intuitive comparison, we visualize the distributions of trafic flows on EMC task by projecting them onto a two-dimensional feature space using t-SNE. As illustrated in Fig. 4, the plots have instances from 16 known classes, indicated from 0 to 15 in diferent colors, and a set of instances from novel class (i.e., the remaining 4 categories of EMC task) indicated in black color. Fig. 4a shows the distribution of raw trafic. This is achieved by selecting the first 4 packets from each flow and the first 32 bytes from each packet. The resulting 4×32-dimensional feature vector is then reduced to two dimensions after sanitizing biased fields. Meanwhile, Fig. 4b illustrates the distribution of trafic flows output by NO-CL, Fig. 4c is the output of NO-PT and Fig. 4d displays the output of our complete method. Clearly, the instances are completely inseparable in the original feature space. After through the pre-training model, the instance distribution is more dispersed, but the separability is still poor. Directly apply contrast learning strategy on the raw trafic can obtain features with a certain degree of discriminability compared to No-CL or original input, but the instance clusters from diferent classes still have a high degree of overlap. In contrast, the output of our complete method has more distinct groups of instance clusters for diferent classes compared to both No-CL and No-PT and instances from novel classes are well separated from other clusters containing known class instances. This also indicates that both the pre-training and contrast learning component play crucial roles in our approach and complement each other. In particular, the pre-training component help extract robust initial feature representations and the contrast learning component make these feature representations more discriminative to adapt to the open-world encrypted trafic classification problem.

2) Efectiveness of Pre-Training Tasks: Furthermore, to verify the efectiveness of our proposed pre-training tasks (MBM and BCP) in learning generic and robust feature representations, we perform an ablation study using adversarial samples generated via the Fast Gradient Sign Method (FGSM) [16]. FGSM introduces controlled perturbations to the original trafic representations, mimicking real-world noise such as packet error or network jitter, thereby enabling an evaluation of the learned features’ resilience.

![](images/dccf65827da4b49e584976dcb6ed89c499d31d729264665f4f5888358e529715.jpg)  
Fig. 5. F1 score variation with increasing  on ETCV task.

Adversarial samples are generated on the test set using the FGSM formulation:

$$
x ^ {\prime} = x + \epsilon \cdot \operatorname{sign} (\nabla_ {x} L (\theta , x, y))\tag{16}
$$

where x represents the embedded representation of a BURST–a sequence of tokenized trafic units derived from raw flows via our preprocessing pipeline. Here,  controls the perturbation magnitude (evaluated at 0, 0.01, 0.1, and 0.5), L is the loss function, and sign denotes the sign function. The perturbations are applied to the token embeddings of BURSTs, which are processed by the BERT-based model. We compare three configurations on the ETCV task, where models are finetuned with a softmax classifier and then tested on the perturbed test set. The three configurations are as follows:

• Configuration 1: Pre-training with only MBM, which reconstructs masked byte sequences within a BURST to learn generic structural patterns.

• Configuration 2: Pre-training with only BCP, which predicts contextual relationships between BURSTs to enhance robustness.

• Configuration 3: Pre-training with both MBM and BCP (our proposed model).

Fig. 5 illustrates the variation in F1 scores across three configurations under diferent perturbation magnitudes . Without perturbation, Configuration 1 exhibits an F1 score 12.3% lower than Configuration 3, and its performance deteriorates sharply with minor perturbation $( \epsilon = 0 . 0 1 )$ . Under significant perturbation, the F1 score drops to 0.392, suggesting that while the MBM task facilitates efective feature learning, features derived solely from MBM lack robustness. Conversely, Configuration 2 yields the lowest F1 score (below 0.543) even without perturbation, indicating that learning contextual relationships between BURSTs alone does not yield generic features. In contrast, Configuration 3 shows minimal F1 score degradation (1.43% drop) with minor perturbation. As  increases, the F1 score remains relatively stable, retaining a value above 0.780 even at $\epsilon = 0 . 5$ , underscoring the synergistic role of MBM and BCP pre-training tasks in ensuring the acquisition of generic and robust feature representations.

In addition, to further evaluate whether the generic and robust features stem from increased model capacity, we configure the pre-training model with varying architectures as follows:

• Cap. 1: 2 Transformer block with model dimension 32.

• Cap. 2: 12 Transformer block with model dimension 32.

• Cap. 3: 2 Transformer block with model dimension 128.

• Cap. 4: 12 Transformer block with model dimension 128.

• Cap. 5: 24 Transformer block with model dimension 256.

![](images/64f0b9b0a8b728d6e5ec81d94c7ae383a1ec07b98e8a28c7e9ba6c3ea4228667.jpg)  
Fig. 6. F1 score variation on EMC task.

The model capacity increases progressively from Cap. 1 to Cap. 5. Fig. 6 depicts the variation in F1 scores across these five configurations on the EMC task, where fine-tuning is performed using a softmax classifier following pre-training. The results indicate that the F1 score improvement plateaus from Cap. 2 to Cap. 5. Notably, despite Cap. 3 having a larger model capacity than Cap. 2, its F1 score decreases by 1.82%. Furthermore, comparisons between Cap. 2 and Cap. 4, and between Cap. 4 and Cap. 5, reveal that merely increasing model width or depth yields marginal gains, with F1 score improvements of only 1.68% and 0.31%, respectively. These findings underscore that simply augmenting model capacity does not significantly contribute to acquiring generic and robust feature representations; rather, such representations are the result of the synergistic interplay between our pre-training tasks MBM and BCP.

## F. Overhead Analysis

In this section, we first give the model parameter quantity and then perform an overhead analysis of our approach, measuring training time (s/100 batches), inference time (ms/flow) and GPU memory usage during both training and testing. The pre-training model parameter mainly consists of four parts: token embeddings, positional embeddings, Transformer encoders and output layers. According to our implementation settings, the approximate number of parameters is as follows:

$$
\begin{array}{r l} \# \text { Param1 } & \approx \underbrace {V \times D} _ {\text { token   emb }} + \underbrace {\hat {L} \times D} _ {\text { pos   emb }} \\ & + \underbrace {N \times (1 2 D ^ {2} + 1 3 D)} _ {\text { 12 - layer   encoder }} + \underbrace {(V + 1) \times D} _ {\text { output }} \\ & = 6 5, 5 3 6 \times 1 2 8 + 5 1 2 \times 1 2 8 \\ & + 1 2 \times (1 2 \times 1 2 8 ^ {2} + 1 3 \times 1 2 8) \\ & + (6 5, 5 3 6 + 1) \times 1 2 8 \\ & \approx \mathbf {1 9 . 3 M p a r a m e t e r s}. \end{array}\tag{17}
$$

where V denotes the vocabulary size; D denotes the model dimension; L<sup>ˆ</sup> denotes the maximum sequence length; N denotes the number of Transformer blocks. Similarly, the model of contrast learning mainly comes from two parts: the convolutional layers in the residual blocks (including their shortcut connections), and the fully connected layers. The approximate number of parameters is calculated as follows:

$$
\# \text { Param2 } \approx \underbrace {\sum_ {i = 1} ^ {8} \left(3 \times C _ {\text { in }} ^ {(i)} C _ {\text { out }} ^ {(i)} + C _ {\text { out }} ^ {(i)}\right)} _ {\text { 1D conv   (8   layers) }}
$$

TABLE VIII  
OVERHEAD STATISTICS OF OUR APPROACH

<table><tr><td rowspan="2"></td><td colspan="2">Time Overhead</td><td colspan="2">GPU Memory</td></tr><tr><td>Training (s/100 batches)</td><td>Inference (ms/flow)</td><td>Training (MB)</td><td>Inference (MB)</td></tr><tr><td>Pre-training</td><td>5.31</td><td>1.12</td><td>9719</td><td>3773</td></tr><tr><td>Contrast Learning</td><td>2.64</td><td>0.05</td><td>46</td><td>12</td></tr><tr><td>Total</td><td>7.95</td><td>1.17</td><td>9765</td><td>3785</td></tr></table>

$$
\begin{array}{l} + \underbrace {\sum_ {j = 1} ^ {4} \left(1 \times C _ {\text { in }} ^ {(j)} C _ {\text { out }} ^ {(j)} + C _ {\text { out }} ^ {(j)}\right)} _ {1 \times 1 \text {   shortcut   (4   layers) }} \\ + \underbrace {\sum_ {k = 1} ^ {3} \left(D _ {\text { in }} ^ {(k)} \cdot D _ {\text { out }} ^ {(k)} + D _ {\text { out }} ^ {(k)}\right)} _ {\text { fully   connected   layers   (fc1 - fc3) }} \\ = \underbrace {5 9 , 9 6 8} _ {\text { conv   layers }} + \underbrace {6 , 6 5 6} _ {\text { shortcut   layers }} + \underbrace {1 9 8 , 9 1 4} _ {\text { FC   layers }} \\ \approx \mathbf {2 6 5 . 5 K p a r a m e t e r s} \end{array}\tag{18}
$$

where $C _ { \mathrm { i n } } ^ { ( i ) }$ and $C _ { \mathrm { o u t } } ^ { ( i ) }$ denote the input and output channels of the i-th convolution layer; $C _ { \mathrm { i n } } ^ { ( j ) }$ and $\bar { C _ { \mathrm { o u t } } ^ { ( j ) } }$ denote the input and output channels of the j-th shortcut convolution; $D _ { \mathrm { i n } } ^ { ( k ) }$ and $D _ { \mathrm { o u t } } ^ { ( k ) }$ denote the input and output dimensions of the k-th fully connected layer.

The overhead statistics based on the above model capacity are shown in Table VIII. To ensure accurate measurements, we restricted the system such that when a model task was executed, it remained the only CPU- and GPU-intensive job on the machine. Training time was calculated by recording the total time required to process the entire training set, dividing by the total number of batches, and then multiplying by 100. As we can see from the first column of Table VIII, our method takes 5.31s and 2.64s respectively in the pre-training and contrast learning stage, totally 7.95s. To calculate the inference time, we recorded the total time taken by the model to infer the entire test set and then divided by the number of test flows. Our approach takes 1 12 ms and 0 05 ms per flow respectively during the pre-training and contrast learning stage, totally 1 17 ms, which are shown in the second column of Table VIII. The last two columns show the GPU memory usage during both training and testing. The pre-training model’s GPU memory consumption during training is relatively high (9719MB) due to the need to learn attention-based token embedding representations for tokens derived from BURSTs, which involves extensive forward and backward calculations across Transformer blocks and generates a large number of intermediate variables. However, during testing, the GPU memory usage drops to 3773MB since gradient calculations and back propagation are not required. In comparison, for contrast learning, the GPU memories are low during both training (46MB) and testing (12MB) phase, because only the small contrast embedding network requires gradient computation and parameter updates, which significantly reduces the memory footprint.

![](images/07d044208967d1a4872fe9290876a8fb970ec7d075b0b5c6718733795a3ff396.jpg)  
Fig. 7. Comparison of model update cost during emergence of novel classes on EMC task.

## G. Operational Considerations

In this section, we discuss the practical considerations involved in deploying our approach in a production environment. Two primary challenges arise in operational settings: i) the computational cost of pre-training, and ii) the ability to eficiently update the model when new categories emerge.

One-time pre-training cost. The pre-training stage is designed to be a one-time ofline process that captures generalizable patterns across a wide range of trafic types. Retraining the pre-trained model is typically unnecessary unless the underlying trafic distribution undergoes substantial and persistent shifts, such as the introduction of new encryption standards, major application-layer protocol redesigns, or fundamental changes in trafic composition. In such cases, updating the pre-trained model with newly collected unlabeled trafic restores representational relevance while keeping longterm maintenance manageable.

Fast and lightweight model updates. The second operational challenge concerns incremental updates when novel trafic classes appear. Traditional softmax-based models, such as ET-BERT, sufer from architectural coupling, where the output layer is tied to a fixed number of classes. Consequently, the emergence of a novel class necessitates a structural modification of the classification head followed by a complete fine-tuning of the entire model, a process that is both disruptive and time-consuming (i.e., the update cost is orders of magnitude higher than ours as shown in Fig. 7). In contrast, our approach utilizes a gradient-isolated update strategy. Since the pre-trained backbone is frozen, only the lightweight contrastive module requires updating. As illustrated in Fig. 7, our approach achieves “plug-and-play” adaptation, completing the model refresh in less than 15 seconds with a negligible memory footprint (<50 MB), regardless of the number of novel classes. These findings confirm that our framework is substantially more scalable in real-world environments where new trafic categories emerge frequently and rapid adaptation is essential.

Recommended deployment workflow. Based on the above considerations, our approach may be deployed in practice following the workflow: i) collect unlabeled trafic data from the target environment and conduct one-time pre-training; ii) label a small number of samples for the downstream task and perform contrast learning; iii) carry out online classification using the trained model; iv) maintain a candidate pool of trafic instances predicted as novel classes; and v) periodically label a small subset from the candidate pool to refresh the contrastive module.

## VI. DISCUSSION

In this section, we discuss some limitations of our approach and its potential impact on further research in this field. i) BURST division. Our BURST division employs a primary criterion: grouping consecutive packets in the same direction. However, we acknowledge that network attributes such as inter-packet delays and idle times can influence the logical segmentation of trafic. Even within the same direction, prolonged intervals between packets may signify distinct applicationlayer operations, such as separate resource requests, which could justify further segmentation. We note that the BCP task is designed to learn contextual relationships between BURSTs. This capability helps mitigate the impact of imperfect segmentation by enabling the model to discern whether BURSTs belong to the same flow or represent unrelated operations, thereby preserving structural characteristics at a higher contextual level. ii) Flow-level classification. We learn robust feature representation for each flow and perform classification task at singe-flow level. We have not taken the multi-flow relations into consideration, which may degrade the performance under multi-flow scenarios (e.g. P2P network usually generate multi-flows to transmit files between peers). Meanwhile, we cannot perform fine-grained classification at the packet level as well. iii) Fairness of comparison. Our approach relies on a pre-training stage, whereas several baselines do not. We acknowledge that this asymmetry may raise concerns regarding fairness. However, to the best of our knowledge, no existing method simultaneously supports pre-training, fewshot learning, and novel class detection. As a result, it is dificult to compare against a single unified baseline that covers all three capabilities. Instead, we selected multiple representative methods, each corresponding to a diferent subset of these capabilities (pre-training based classifiers, few-shot learners, and novelty detectors). This design ensures that every dimension of our method is evaluated against the strongest available alternatives. Future research may explore unified benchmarks that incorporate pre-training for all candidate methods, enabling more strictly controlled comparisons.

## VII. CONCLUSION

In this paper, we propose an eficient open-world encrypted trafic classification approach, which achieves few-shot classification by combining pre-training techniques with contrast learning. In the pre-training stage, we design two pre-training tasks: MBM task and BCP task, one learns the byte dependencies within BURSTs and the other learns the relationships between BURSTs, together they guarantee the robust initial feature representations of trafic flows. In the contrast learning stage, a discriminative feature space is learned based on the customized contrast learning strategy. The characteristic of intra-class compactness and inter-class separability within this feature space allows us to employ a distance-based metric for classifying known categories and detecting novel ones. We evaluate our approach on five encrypted trafic classification tasks and the results demonstrate that our approach achieves consistently better performance than baseline studies in both closed- and open-world settings.

## REFERENCES

[1] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “DISTILLER:´ Encrypted trafic classification via multimodal multitask deep learning,” J. Netw. Comput. Appl., vols. 183–184, Jun. 2021, Art. no. 102985.

[2] H. Bao, L. Dong, S. Piao, and F. Wei, “BEiT: BERT pre-training of image transformers,” 2021, arXiv:2106.08254.

[3] P. L. Bartlett and S. Mendelson, “Rademacher and Gaussian complexities: Risk bounds and structural results,” J. Mach. Learn. Res., vol. 3, pp. 463–482, Nov. 2002.

[4] L. Bernaille, R. Teixeira, I. Akodkenou, A. Soule, and K. Salamatian, “Trafic classification on the fly,” ACM SIGCOMM Comput. Commun. Rev., vol. 36, no. 2, pp. 23–26, Apr. 2006.

[5] T. Chen, S. Kornblith, M. Norouzi, and G. Hinton, “A simple framework for contrastive learning of visual representations,” in Proc. Int. Conf. Mach. Learn., 2020, pp. 1597–1607.

[6] T. Cui et al., “TraficLLM: Enhancing large language models for network trafic analysis with generic trafic representation,” 2025, arXiv:2504.04222.

[7] T. Dahanayaka, Y. Ginige, Y. Huang, G. Jourjon, and S. Seneviratne, “Robust open-set classification for encrypted trafic fingerprinting,” Comput. Netw., vol. 236, Nov. 2023, Art. no. 109991.

[8] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers for language understanding,” 2018, arXiv:1810.04805.

[9] I. Din, N. A. Saqib, and A. Baig, “Passive analysis of web trafic characteristics for estimating quality of experience,” in Proc. IEEE Globecom Workshops, Nov. 2008, pp. 1–5.

[10] A. Dosovitskiy et al., “An image is worth 16×16 words: Transformers for image recognition at scale,” 2020, arXiv:2010.11929.

[11] Z. M. Fadlullah, T. Taleb, A. V. Vasilakos, M. Guizani, and N. Kato, “DTRAB: Combating against attacks on encrypted protocols through trafic-feature analysis,” IEEE/ACM Trans. Netw., vol. 18, no. 4, pp. 1234–1247, Aug. 2010.

[12] C. Fu, Q. Li, M. Shen, and K. Xu, “Realtime robust malicious trafic detection via frequency domain analysis,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2021, pp. 3431–3446.

[13] T. Gao, X. Yao, and D. Chen, “SimCSE: Simple contrastive learning of sentence embeddings,” 2021, arXiv:2104.08821.

[14] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016, pp. 407–414.

[15] Y. Ginige, T. Dahanayaka, and S. Seneviratne, “TraficGPT: An LLM approach for open-set encrypted trafic classification,” in Proc. 19th Asian Internet Eng. Conf., Aug. 2024, pp. 26–35.

[16] I. J. Goodfellow, J. Shlens, and C. Szegedy, “Explaining and harnessing adversarial examples,” 2014, arXiv:1412.6572.

[17] J.-B. Grill et al., “Bootstrap your own latent-a new approach to selfsupervised learning,” in Proc. 34th Int. Conf. Neural Inf. Process. Syst., 2020, pp. 21271–21284.

[18] H. Y. He, Z. Guo Yang, and X. N. Chen, “PERT: Payload encoding representation from transformer for encrypted trafic classification,” in Proc. ITU Kaleidoscope, Ind.-Driven Digit. Transformation (ITU K), Dec. 2020, pp. 1–8.

[19] K. He, H. Fan, Y. Wu, S. Xie, and R. Girshick, “Momentum contrast for unsupervised visual representation learning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2020, pp. 9729–9738.

[20] T.-L. Huoh, Y. Luo, P. Li, and T. Zhang, “Flow-based encrypted network trafic classification with graph neural networks,” IEEE Trans. Netw. Service Manage., vol. 20, no. 2, pp. 1224–1237, Jun. 2023.

[21] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, “ALBERT: A lite BERT for self-supervised learning of language representations,” 2019, arXiv:1909.11942.

[22] A. H. Lashkari, G. D. Gil, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of Tor trafic using time based features,” in Proc. 3rd Int. Conf. Inf. Syst. Secur. Privacy (ICISSP), Porto, Portugal, Feb. 2017, pp. 253–262.

[23] W. Li, X.-Y. Zhang, H. Bao, H. Shi, and Q. Wang, “ProGraph: Robust network trafic identification with graph propagation,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1385–1399, Jun. 2023.

[24] X. Li, B. Feng, T. Zang, X. Xu, S. Zhao, and J. Ma, “Facing unknown: Open-world encrypted trafic classification based on contrastive pretraining,” in Proc. IEEE Symp. Comput. Commun. (ISCC), Jul. 2023, pp. 1255–1260.

[25] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., Apr. 2022, pp. 633–642.

[26] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-Net: A flow sequence network for encrypted trafic classification,” in Proc. IEEE INFOCOM Conf. Comput. Commun., Apr. 2019, pp. 1171–1179.

[27] Y. Liu et al., “RoBERTa: A robustly optimized BERT pretraining approach,” 2019, arXiv:1907.11692.

[28] Z. Liu, L. Cai, L. Zhao, A. Yu, and D. Meng, “Towards open world trafic classification,” in Proc. Inf. Commun. Security: 23rd Int. Conf., Chongqing, China, Nov. 2021, pp. 331–347.

[29] M. Lotfollahi, M. J. Siavoshani, R. S. H. Zade, and M. Saberian, “Deep packet: A novel approach for encrypted trafic classification using deep learning,” Soft Comput., vol. 24, no. 3, pp. 1999–2012, Feb. 2020.

[30] T. Mitchell et al., “Never-ending learning,” Commun. ACM, vol. 61, no. 5, pp. 103–115, 2018.

[31] A. W. Moore and D. Zuev, “Internet trafic classification using Bayesian analysis techniques,” in Proc. ACM SIGMETRICS Int. Conf. Meas. Model. Comput. Syst., Jun. 2005, pp. 50–60.

[32] K. Al-Naami et al., “Adaptive encrypted trafic fingerprinting with bidirectional dependence,” in Proc. 32nd Annu. Conf. Comput. Secur. Appl., Dec. 2016, pp. 177–188.

[33] A. Panchenko et al., “Website fingerprinting at internet scale,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2016, pp. 1–15.

[34] A. Panchenko, L. Niessen, A. Zinnen, and T. Engel, “Website fingerprinting in onion routing based anonymization networks,” in Proc. 10th Annu. ACM workshop Privacy Electron. Soc., Oct. 2011, pp. 103–114.

[35] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever, “Language models are unsupervised multitask learners,” OpenAI Blog, vol. 1, no. 8, p. 9, 2019.

[36] M. Roughan, S. Sen, O. Spatscheck, and N. Dufield, “Class-of-service mapping for QoS: A statistical signature-based approach to IP trafic classification,” in Proc. 4th ACM SIGCOMM Conf. Internet Meas., Oct. 2004, pp. 135–148.

[37] V. Sanh, L. Debut, J. Chaumond, and T. Wolf, “DistilBERT, a distilled version of BERT: Smaller, faster, cheaper and lighter,” 2019, arXiv:1910.01108.

[38] T. Shapira and Y. Shavitt, “FlowPic: Encrypted internet trafic classification is as easy as image recognition,” in Proc. IEEE INFOCOM Conf. Comput. Commun. Workshops (INFOCOM WKSHPS), Apr. 2019, pp. 680–687.

[39] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted trafic analysis using graph neural networks,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 2367–2380, 2021.

[40] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Toronto, ON, Canada, Oct. 2018, pp. 1928–1943.

[41] Z. Song et al., “I<sup>2</sup> RNN: An incremental and interpretable recurrent neural network for encrypted trafic classification,” IEEE Trans. Depend. Secure Comput., early access, 2023, doi: 10.1109/TDSC.2023.3245411.

[42] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Robust smartphone app identification via encrypted network trafic analysis,” IEEE Trans. Inf. Forensics Security, vol. 13, no. 1, pp. 63–78, Jan. 2018.

[43] T. van Ede et al., “FlowPrint: Semi-supervised mobile-app fingerprinting on encrypted network trafic,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2020, pp. 1–18.

[44] A. Vaswani, “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst. (NeurIPS), 2017, pp. 1–11.

[45] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Jan. 2017, pp. 712–717.

[46] C. Xu, J. Shen, and X. Du, “A method of few-shot network intrusion detection based on meta-learning framework,” IEEE Trans. Inf. Forensics Security, vol. 15, pp. 3540–3552, 2020.

[47] S.-J. Xu, G.-G. Geng, X.-B. Jin, D.-J. Liu, and J. Weng, “Seeing trafic paths: Encrypted trafic classification with path signature features,” IEEE Trans. Inf. Forensics Security, vol. 17, pp. 2166–2181, 2022.

[48] C. Yang et al., “Few-shot encrypted trafic classification via multi-task representation enhanced meta-learning,” Comput. Netw., vol. 228, Jun. 2023, Art. no. 109731.

[49] X. Zhang et al., “Enhanced few-shot malware trafic classification via integrating knowledge transfer with neural architecture search,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 5245–5256, 2024.

[50] L. Zhao, L. Cai, A. Yu, Z. Xu, and D. Meng, “Prototype-based malware trafic classification with novelty detection,” in Proc. Inf. Commun. Security: 21st Int. Conf., Beijing, China, Dec. 2020, pp. 3–17.

[51] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., 2023, vol. 37, no. 4, pp. 5420–5427.

[52] Z. Zhao et al., “FOSS: Towards fine-grained unknown class detection against the open-set attack spectrum with variable legitimate trafic,” IEEE/ACM Trans. Netw., vol. 32, no. 5, pp. 3945–3960, Oct. 2024.

[53] Z. Zhao, Z. Li, Z. Song, W. Li, and F. Zhang, “Trident: A universal framework for fine-grained and class-incremental unknown trafic detection,” in Proc. ACM Web Conf., May 2024, pp. 1608–1619.

[54] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

![](images/957f6abcfbbb81929702bf537dd09ec34f9e01dbeec67bb46d64f7b4579f90d8.jpg)  
Lixin Zhao received the B.S. degree from Nankai University in 2013 and the Ph.D. degree in computer sciences from the University of Chinese Academy of Sciences in 2020. He is currently a Research Assistant with the Institute of Information Engineering, Chinese Academy of Sciences. His research interests include network security and data security.

![](images/be53c4ad8861f88c822d7766a5e572eab9a52f6ed57984fb98319e8fd1b9e5d9.jpg)  
Changhao Wu received the B.S. degree from Nankai University in 2022 and the M.S. degree in cyberspace security from the Institute of Information Engineering, Chinese Academy of Sciences, in 2025. His research interests include network security and intrusion detection.

![](images/d525dc89500a68638f04c36d78d1cd864c36ce1d6d63190b058eb40b00c29cef.jpg)

Aimin Yu received the B.S. degree from Nankai University and the Ph.D. degree from the Institute of Software, Chinese Academy of Sciences, in 2011. He is currently a Professor with the Institute of Information Engineering, Chinese Academy of Sciences. His research interests include system security and trust computing.
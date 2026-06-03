# FlowRefiner: A Robust Traffic Classification Framework against Label Noise

Mingwei Zhan1, Ruijie Zhao2\*, Xianwen Deng1, Zhi Xue1†, Qi Li3, Zhuotao Liu3, Guang Cheng2, Ke Xu3†

1Shanghai Jiao Tong University 2Southeast University 3Tsinghua University {mw.zhan,2594306528,zxue}@sjtu.edu.cn {ruijiezhao,chengguang}@seu.edu.cn {qli01,zhuotaoliu,xuke}@tsinghua.edu.cn

# Abstract

Network traffic classification is essential for network management and security. In recent years, deep learning (DL) algorithms have emerged as essential tools for classifying complex traffic. However, they rely heavily on high-quality labeled training data. In practice, traffic data is often noisy due to human error or inaccurate automated labeling, which could render classification unreliable and lead to severe consequences. Although some studies have alleviated the label noise issue in specific scenarios, they are difficult to generalize to general traffic classification tasks due to the inherent semantic complexity of traffic data. In this paper, we propose FLOWREFINER, a robust and general traffic classification framework against label noise. FLOWREFINER consists of three core components: a traffic semantics-driven noise detector, a confidence-guided label correction mechanism, and a cross-granularity robust classifier. First, the noise detector utilizes traffic semantics extracted from a pre-trained encoder to identify mislabeled flows. Next, the confidence-guided label correction module fine-tunes a label predictor to correct noisy labels and construct refined flows. Finally, the cross-granularity robust classifier learns generalized patterns of both flow-level and packet-level, improving classification robustness against noisy labels. We evaluate our method on four traffic datasets with various classification scenarios across varying noise ratios. Experimental results demonstrate that FLOWREFINER mitigates the impact of label noise and consistently outperforms state-of-the-art baselines by a large margin. The code is available at https://github.com/NSSL-SJTU/FlowRefiner.

# 1 Introduction

Network traffic classification is a fundamental task for the management, security, and optimization of modern networks. It enables critical capabilities such as identifying malicious behaviors (1; 2; 3), enforcing quality-of-service (QoS) policies (4; 5; 6), and monitoring application usage (7). It can also support user-centric analysis such as profiling in social network applications by fine-grained inference of user actions (8; 9). As network applications and protocols continue to evolve, traffic data have become increasingly complex, reflecting not only protocol interactions but also diverse user behaviors and service patterns (10). These complexities make automated traffic classification both more important and more challenging (11; 12; 13).

In recent years, deep learning (DL) algorithms have emerged as powerful tools for traffic analysis for handling such complexity (14; 15; 16; 17; 18). By leveraging large-scale labeled raw traffic data, DL-based models can automatically extract discriminative representations and achieve accurate classification performance. However, the success of DL-based methods heavily relies on the quality of labeled training data, and their performance can degrade significantly in the presence of label noise (19). On the other hand, label noise, caused by incorrect, ambiguous, or inconsistent annotations, is especially a critical issue in traffic analysis tasks. Erroneous labels can hinder generalization in real-world scenarios and lead to severe consequences, such as failing to detect malicious traffic as suspicious or misclassifying latency-sensitive applications in QoS enforcement. Unfortunately, label noise is especially common in realistic traffic due to the complexity and variability of real-world environments and the flaws of automated labeling techniques (20; 21). Though labels of lab-generated traffic could be refined through controlled environments and manual annotation processes, the label quality of realistic traffic is still challenging since the automated labeling is prone to errors (22).

Despite its significance, the issue of label quality is rarely noticed and discussed in existing DL-based traffic classification methods. Only a few studies (23; 24) explicitly target label noise in the context of malicious traffic, a specific subfield of traffic analysis focused primarily on intrusion detection. However, these approaches can hardly generalize to general traffic classification tasks, as some (23) are limited to binary classification, while others (24) rely on strong benign–malicious separability that does not hold in more diverse traffic scenarios. In addition, though various methods (25; 26; 27; 28) have been developed to address label noise in other fields (e.g., computer vision), they still struggle in traffic classification due to the inherent structural complexity and obfuscated semantics of traffic data. Thus, dealing with label noise in general traffic data remains a crucial and unresolved issue.

In this paper, we propose FLOWREFINER, a robust and general traffic classification framework against label noise. Unlike existing approaches from computer vision or malicious traffic detection, FLOWREFINER is tailored to the unique characteristics of traffic data and supports general classification across diverse scenarios. FLOWREFINER effectively detects, corrects, and classifies traffic with noisy labels in a uniform framework, achieving high performance without relying on high-quality labeled data, which are costly and difficult to obtain in increasingly complex network environments. Moreover, by accurately identifying mislabeled flows, FLOWREFINER provides valuable feedback to assist network administrators and annotators in improving traffic data quality. Specifically, FLOWREFINER consists of three key components: a traffic semantics-driven noise detector, a confidence-guided label correction mechanism, and a cross-granularity robust classifier. First, we deploy a pre-trained traffic encoder to extract latent traffic semantic representations for noisy flow isolation. Then, the majority labels within each cluster guide the division of flows into clean flows and noisy flows. Next, the confidence-guided label correction refines the noisy flows by fine-tuning a traffic label predictor on clean data and correcting mislabeled samples based on predicted confidence scores, thus reintroducing the corrected noisy flows into the clean flows to form the refined flows. Finally, our cross-granularity robust classifier integrates both flow-level and packet-level classification, enabling the model to capture generalized patterns rather than focusing on noise-driven isolated features. It ensures robustness and improves classification performance even in the presence of noisy labels. In summary, our contributions are as follows:

• We introduce FLOWREFINER, a robust method for general traffic classification that effectively detects, corrects, and classifies traffic with noisy labels. To the best of our knowledge, this is the first work to address the label noise issues across diverse traffic classification tasks.   
• We propose a traffic semantics-driven noise detector. It leverages the traffic semantics extracted by the pre-trained traffic encoder to detect outlier labels as noise, where the raw flows are divided into clean flows and noisy flows.   
• We fine-tune a traffic label predictor based on isolated clean flows to perform confidence-guided label correction of detected noisy flows. The correction results can assist network administrators and annotators to improve traffic label quality.   
• We design a cross-granularity robust classifier that integrates both flow-level and packet-level classification tasks to improve robustness, preventing the encoder from overfitting to noisy labels.   
• We evaluate FLOWREFINER on four real-world traffic datasets with different noise ratios. Results show that our method can achieve robust traffic classification against label noise and significantly outperforms the state-of-the-art baselines.

# 2 Related Work

Traffic Classification Methods. In traffic analysis, traditional rule-based methods initially relied on fixed attributes like port numbers and protocols to classify traffic. However, with the rise of encryption protocols such as SSL and TLS, their effectiveness has gradually decreased because these protocols conceal key traffic characteristics (29; 7). To overcome these limitations, machine learning (ML) techniques, including support vector machine (SVM) and random forest (RF), leveraged statistical features from traffic data to automate feature selection and improve classification accuracy (30; 7). Although these ML-based methods marked a significant advancement, they heavily depend on handcrafted features, which limits adaptability across various traffic types (13).

![](images/52831cad5e4932f4653338bda994604df24635f8f8c541330a3cb56c926f953c.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Raw Flows"] --> B["Feature Vectors"]
    C["Label Noise"] --> B
    D["Manual Annotated Traffic"] --> E["x_i"]
    D --> F["y_i"]
    B --> G["Traffic Encoder"]
    G --> H["Fine-grained Clustering"]
    H --> I["Outlier Labels"]
    I --> J["Clean Flows"]
    J --> K["Label Predictor"]
    K --> L["Refined Flows"]
    M["Test Mode"] --> N["Label Predictor"]
    O["Test Mode"] --> P["High Confidence"]
    Q["Test Mode"] --> R["Low Confidence"]
    S["Target"] --> K
    T["Noisy Flows"] --> U["x_i"]
    T --> V["Label Predictor"]
    W["Confidence-Guided Label Correction"] --> X["Target"]
    Y["Cross-Granularity Robust Classifier"] --> Z["Random Select"]
    AA["Packet"] --> AB["Packet-level"]
    AC["Target"] --> AD["Random Select"]
    AE["Packet-level"] --> AF["Packet-level"]
```
</details>

Figure 1: The overview of FLOWREFINER.

Deep learning (DL) methods have brought a shift towards automatic feature extraction from raw traffic data, with convolutional neural networks (CNNs), recurrent neural networks (RNNs), and Transformers being widely adopted for learning hierarchical representations (16; 14). Recent arts have also explored pre-training techniques, with PERT and ET-BERT (31; 32) applying NLP-inspired BERT models (33) to encrypted traffic classification, and Flow-MAE (34), YaTC (35) using masked autoencoders (MAE) (36) to improve robustness in feature extraction under encryption. However, they are particularly prone to label noise, as their high capacity allows them to overfit incorrect labels (37; 19). Some works (24; 38; 39; 40) have noticed the label noise issue in deep learning-based intrusion detection systems, and propose corresponding methods for malicious traffic. However, they lack generalizability to more general traffic classification tasks. It is urgent to propose an effective method to resist noisy labels for general traffic analysis tasks.

Label Noise Learning Methods. Various methods have been developed to address label noise in other fields such as computer vision. A series of approaches like Generalized Cross-Entropy (GCE) (27) and Symmetric Cross-Entropy (SCE) (28) modify traditional loss functions to better handle noisy labels. GCE combines cross-entropy with mean absolute error to make learning more noise-resistant, while SCE balances penalization of misclassified samples. In addition, some works (26) (25) investigate filtering noisy samples that rely on the loss value distribution. On the other hand, data augmentation technique has been wild used against label noise. As a classic robust augmentation, Mixup (41) applies interpolation between samples to generate robust training data. But it struggles when applied to the structured nature of encrypted traffic flows, where such interpolations may not produce meaningful results. Recent methods like Manifold DivideMix (42), which incorporate contrastive learning, offer improved robustness to severe noise. However, they rely on well-defined meaningful data augmentation, which is hardly performed in structured traffic data, limiting their ability to handle label noise within traffic flows.

In summary, while these label noise learning methods offer powerful mechanisms in other fields, the traffic classification still lacks effective solutions that can robustly handle noisy labels. To fill this gap, we propose FLOWREFINER, a robust framework specifically designed to detect, correct, and classify traffic with noisy labels, offering a comprehensive solution for label noise in general traffic classification.

# 3 FLOWREFINER

We introduce FLOWREFINER, a robust method for general traffic classification that effectively detects, corrects, and classifies traffic with noisy labels. Our framework starts with traffic semantics extracted by the advanced pre-trained encoder could reflect the similarities and diversity of flow characteristics, providing a basis for detecting label-noisy flows (detailed in Sec. 3.1). After that, a predictor is fine-tuned via detected clean flows to correct noisy labels and construct refined flows with low-level label noise(detailed in Sec. 3.2). Finally, a traffic classifier with a cross-granularity structure is designed to perform robust general traffic classification against label noise (detailed in Sec. 3.3).

# 3.1 Traffic Semantics-Driven Noise Detector

Traffic semantics-driven noise detector aims to identify and isolate noisy labels in traffic data effectively. It achieves effective noisy flow detection by leveraging the traffic semantics extracted from the flows and combining their similarity with label distribution.

Traffic Semantics Extraction. We first build a traffic semantics-oriented encoder via the pretraining paradigm to extract the latent representation of traffic data. Benefiting from the learned semantics from the unlabeled traffic data in pre-training, the pre-trained traffic encoder can effectively extract traffic semantics (32), while remaining immune to interference from potential noisy labels.

We adopt the Masked Autoencoder (MAE) (36) style pre-training paradigm to enable the encoder to capture the traffic semantics by randomly masking input and reconstructing the missing portions (which is further detailed in Appendix A). In addition, the encoder deploys the Transformer architecture as the backbone for feature extraction. Formally, let $X = \{ x _ { 1 } , \overset { \cdot } { x _ { 2 } } , \overset { } { \dots } , x _ { N } \}$ represent the dataset, where $x _ { i }$ is an individual flow sample. The pre-trained encoder, denoted as $f _ { \mathrm { e n c } } ( \cdot )$ , processes each sample $x _ { i }$ and produces a d-dimensional feature vector: $z _ { i } = f _ { \mathrm { e n c } } ( x _ { i } ) , \quad z _ { i } \in \mathbb { R } ^ { d }$ .

# Noise Detection based on Traffic Semantics.

The distances between traffic semantics embeddings can effectively reflect the similarities in flow content and function. These similarities have the potential to highlight instances of label noise, as similar flows with discrete labels are likely candidates for noisy labels. However, as we visualized via t-SNE in Figure 2, since the traffic semantics have not yet been aligned with the correct labels, there are two main concerns that should be considered during noise detection: There are two main challenges in detecting label

![](images/176274b66cc7353f4813e4d3ef93ed15a3a9abce42f074c13ce9086897d6cd57.jpg)

<details>
<summary>text_image</summary>

Extracted Traffic Semantics
via Pre-training
Group I
Class 1 Class 2 Class 3
Group II
Class 1 Class 4
Similar Semantics from
Diverse Classes
Diverse Semantics from
the Same Class
</details>

Figure 2: The t-SNE visualization of the traffic semantics.

noise via similarities: (1) Traffic data in the same class may not exhibit consistent behaviors, forming diverse compact clusters in the latent space; (2) Traffic data from different classes may appear semantically similar, leading to groups of mixed-category flows. Therefore, we designed a fine-grained clustering and defined majority labels for each cluster to address the above issues and detect noisy labels.

To capture the different behaviors inside the same class, we further cluster the semantics similarity between flows with a more fine-grained level than categories. Specifically, we partition extracted flow samples into K clusters, according to their extracted feature vectors $\{ z _ { 1 } , z _ { 2 } , \dots , z _ { N } \}$ by the K-means algorithm, where each flow sample is grouped based on its semantic proximity to other samples. Especially, the number of clusters is defined as $K = n \times C$ , where $C$ represents the total number of classes and n is an integer hyperparameter introduced to control the granularity of the clustering. The objective function for K-means clustering is to minimize the sum of squared distances between the feature vectors and the corresponding cluster centroids:

$$
\min _ {\mu_ {k}} \sum_ {i = 1} ^ {N} \sum_ {k = 1} ^ {K} \mathbb {1} (z _ {i} \in C _ {k}) \| z _ {i} - \mu_ {k} \| ^ {2}, \tag {1}
$$

where $\mu _ { k }$ is the centroid of the k-th cluster, and $\mathbb { H } ( z _ { i } \in C _ { k } )$ is an indicator function that assigns $z _ { i }$ to the nearest cluster $C _ { k }$ . Subsequently, flows within the same cluster share the most similar semantics, and the presence of inconsistent labels within each cluster is regarded as potential noise.

Considering the potential similar activity of flows from different categories, we define the majority labels for each cluster to represent the inside overlapped true classes. Let $L _ { k }$ be the set of labels for the samples in cluster $C _ { k }$ . The majority label $L _ { k } ^ { \mathrm { m a j o r } }$ is determined as the top m most frequent labels in the cluster. Samples with labels that are not among the majority labels $L _ { k } ^ { \mathrm { m a j o r } }$ in their cluster are treated as statistical outliers, and their labels are considered noisy.

Finally, we detect and divide the raw flows into a clean flow set and a noisy flow set:

$$
\mathcal {D} _ {\text { clean }} = \{(x _ {i}, y _ {i}) \mid x _ {i} \in C _ {k}, y _ {i} \in L _ {k} ^ {\text { major }} \}, \mathcal {D} _ {\text { noisy }} = \{(x _ {i}, y _ {i}) \mid x _ {i} \in C _ {k}, y _ {i} \notin L _ {k} ^ {\text { major }} \}, \tag {2}
$$

where $y _ { i }$ is the raw label for sample $x _ { i } ,$ , and $L _ { k } ^ { \mathrm { m a j o t } }$ r is the majotity label of cluster $C _ { k }$ . The clean flows $\mathcal { D } _ { \mathrm { c l e a n } }$ can be used to support further training, while the noisy flows $\mathcal { D } _ { \mathrm { n o i s y } }$ can be flagged and reported to the manager or annotator for review.

# 3.2 Confidence-Guided Label Correction

Through the semantic-driven noise detector, most noisy flows are identified and isolated from the clean flows according to their label-independent traffic semantics. Furthermore, this clean flow set can provide valid supervision to further correct the label distribution of the noisy flows and expand the available training data. For this purpose, we design the confidence-guided label correction module to correct flow labels in the noisy flow set based on prediction confidence.

Traffic Label Predictor Fine-tuning. In this stage, we aim to fine-tune the latent representations of flows to align with the labels of selected clean flows $\mathcal { D } _ { \mathrm { c l e a n } }$ , thereby obtaining a confidenceaware traffic label predictor that can assess the category of selected noisy flows $\mathcal { D } _ { \mathrm { n o i s y } }$ based on confidence scores. Formally, let $X _ { \mathrm { c l e a n } } = \{ x _ { 1 } , x _ { 2 } , \hat { . } . . \hat { . } , x _ { N _ { c } } \}$ be the set of clean flow samples in $\mathcal { D } _ { \mathrm { c l e a n } } ,$ and $y _ { \mathrm { c l e a n } } = \{ y _ { 1 } , y _ { 2 } , . . . , y _ { N _ { c } } \}$ be their corresponding labels. Then, we leverage the supervised learning paradigm to fine-tune our label predictor $f _ { \mathrm { p r d } } ^ { - } ( x )$ , which consists of the pretrained encoder and an added classification head, aiming to minimize the cross-entropy loss: $\mathcal { L } _ { \mathrm { C E } } =$ $\begin{array} { r l } { \textstyle - \sum _ { i = 1 } ^ { N _ { c } } y _ { i } \log ( f _ { \mathrm { p r d } } ( x _ { i } ) ) } & { { } } \end{array}$ .

Our well-trained label predictor provides confidence scores, $p _ { i } = \operatorname* { m a x } ( f \mathrm { p r d } ( x _ { i } ) )$ ), which represent the predictor’s certainty regarding the predicted class. These confidence scores serve as the basis for further label correction of noisy flows.

Noise Label Correction. To refine the available flows with label noise and avoid losing valuable diversified information, we correct the original labels of noisy flows based on the predicted confidence scores. Specifically, for each noisy flow sample and its label $( x _ { i } , y _ { i } ) \in D _ { \mathrm { n o i s y } }$ , the predictor outputs a predicted label $\hat { y } _ { i }$ along with its confidence score $p _ { i } = \operatorname* { m a x } ( f _ { \mathrm { p r d } } ( x _ { i } ) )$ , which is the highest softmax probability from the label predictor. Based on these confidence scores, we refine the labels of noisy flows into two categories (as examples in Figure 6 of the Appendix B):

(1) High-Confidence Flow Labels $( p _ { i } \geq \tau _ { h } ) \colon$ These samples have high confidence in their predicted labels and are thus assumed to share a similar distribution with the clean set. Thus, we correct their labels with the predicted labels $\hat { y } _ { i }$ and merge them into the refined flows.

(2) Low-Confidence Flow Labels $( p _ { i } \leq \tau _ { l } )$ : These samples have low confidence and likely lie outside the semantic distribution of the clean set. Since they are difficult for the classifier to categorize, we retain their original labels and introduce them to the refined flows to maintain diversity and expand the semantic distribution of samples.

Note that $\tau _ { h }$ and $\tau _ { l }$ represent the thresholds for refining high and low confidence flow labels, respectively. Combined with the clean flows, the obtained refined flows $\mathcal { D } _ { \mathrm { r e f i n e d } }$ contain fewer noisy labels but preserve a more representative semantic distribution of the raw data, including samples that lie outside the initial clean flows’s boundaries. The final refined flows are formulated as follows:

$$
\mathcal {D} _ {\text { refined }} = \mathcal {D} _ {\text { clean }} \cup \{(x _ {i}, \hat {y} _ {i}) \mid p _ {i} > \tau_ {h} \} \cup \{(x _ {i}, y _ {i}) \mid p _ {i} <   \tau_ {l} \}, \tag {3}
$$

where the $\mathcal { D } _ { \mathrm { c l e a n } }$ represent clean flows from the semantic-driven noise detector, the $x _ { i }$ is each sample of noisy flows $D _ { \mathrm { n o i s y } } , \hat { y } _ { i }$ is the predict label, $y _ { i }$ is the raw label, and $p _ { i }$ is the confidence score.

# 3.3 Cross-Granularity Robust Classifier

Based on the refined flows with low-level label noise, we perform traffic encoder fine-tuning for robust traffic classification. Due to strong fitting capabilities, deep learning models are prone to memorize mislabeled samples themself, rather than capturing generalizable patterns (43; 44). To avoid the encoder memorizing specific flows with false labels, we propose a cross-granularity robust classifier that integrates both flow-level and packet-level traffic classification tasks. Thus, our classifier can capture generalized patterns that are valid on both tasks, rather than attention to isolated invalid features that are misdirected by noisy labels.

The robust traffic classifier contains two parallel shared weight encoders and classification heads, which could be formulaically treated as a single encoder and denoted as $f _ { \mathrm { e n c } }$ and $f _ { \mathrm { h e a d } }$ . The structure and explanation of the shared-weight classifier that can handle both flow and traffic samples are detailed in Appendix C. The encoder is also based on the Transformer and loads the parameters pre-trained by MAE. It first processes each flow $x _ { i }$ by dividing it into sequential packets then selects one packet $x _ { i } ^ { \bar { p } }$ randomly to serve as the other input sample:

$$
x _ {i} ^ {p} = \text { RandomSelect } (\{p a c _ {i} ^ {1}, p a c _ {i} ^ {2}, \dots \mid x _ {i} \}). \tag {4}
$$

Next, the flow sample $x _ { i }$ is inputted to the encoder and linear heads to generate $\hat { y } _ { i } ,$ , a flow-level prediction of the label. Following the above process, the flow classification task is performed with the flow sample $x _ { i }$ and label $y _ { i }$ from the refined flows by minimizing the cross-entropy loss. Then, the packet classification task is trained subsequentially during each epoch. Similarly, the randomly selected packet sample is inputted to the encoder and classification head, and obtains the packet level prediction $\hat { y } _ { i } ^ { p }$ . By associating packet sample $\boldsymbol { x } _ { i } ^ { p }$ with the flow label $y _ { i }$ via the cross-entropy loss, the classifier performs packet classification and learns traffic patterns on another granularity.

By the cross-granularity classification tasks, the classifier can utilize both global (flow-level) and local (packet-level) features within the refined flows, providing more varied input against label noise. Specifically, by introducing randomness in the packet selection, the classifier obtains different sample variants in each epoch, thus avoiding the memorization of specific flows with false labels. In addition, the trained cross-granularity robust classifier can serve for both flow-level or packet-level traffic classification under the label noise according to the practical needs, bringing not only robustness but also flexibility.

# 4 Experiments

# 4.1 Experiment Settings

Datasets. We conduct our experiments on four real-world traffic datasets: ISCXVPN (45), Cross-Platform (46), USTC-TFC (16), and Malware (47), each representing different traffic scenarios. Each dataset sample in our experiments corresponds to a network flow, which is obtained via session-aware splitting according to the standard 5-tuple (source IP, destination IP, source port, destination port, and protocol). In FLOWREFINER, we process each flow into a formatted matrix via the MFR algorithm (35). To comprehensively evaluate the robustness of our methods against label noise, we generate noisy datasets for each scenario with different noise ratios (5%, 10%, 20%, 40%, 60%). The details of these datasets are shown in Appendix D.

Baselines. To evaluate the performance of FLOWREFINER, we compare it with six state-of-the-art traffic classification methods. These include two traditional ML- and DL-based methods, Appscanner (7) and FS-Net (14); three advanced pre-training methods, ET-BERT (32), MAE (34), and YaTC (35); and the malicious traffic label noise method, MCRe (24). In addition, we introduce three packet classification baselines (48; 16; 32) and six general label noise learning baselines , CE, LSR (49), Mixup (41), GCE (27), SCE (28), Co-teaching (26), and Dividemix (25), to further extend the evaluations.

Implementation Details. In the training stage, we set the batch size as 64, the epochs as 20, and the learning rate as $4 * 1 0 ^ { - 3 }$ with the AdamW optimizer (50). In noise detection, we set the parameter of clustering granularity as $n = 5$ , and the top $m = 2$ most frequent labels in the cluster are defined as the majority labels. The high and low confidence thresh- olds are setted as $\tau _ { h } = 0 . 9$ and $\tau _ { l } = 0 . 7$ . All experiments are implemented in four NVIDIA GeForce RTX3090 GPUs with PyTorch 1.9.0. We summarize the hyperparameter settings in Appendix F.

Table 1: Performance Comparison with Traffic Classification Baselines under Different Noise Ratios. 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Noise</td><td colspan="2">Appscanner</td><td colspan="2">FS-Net</td><td colspan="2">ET-BERT</td><td colspan="2">MAE</td><td colspan="2">YaTC</td><td colspan="2">MCRe</td><td colspan="2">Ours</td></tr><tr><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td></tr><tr><td rowspan="5">ISCXVPN</td><td>5%</td><td>81.49</td><td>82.12</td><td>87.97</td><td>88.05</td><td>86.12</td><td>86.11</td><td>91.04</td><td>91.08</td><td>92.44</td><td>92.35</td><td>83.01</td><td>83.63</td><td>93.67</td><td>93.34</td></tr><tr><td>10%</td><td>79.22</td><td>79.63</td><td>85.47</td><td>85.49</td><td>85.24</td><td>85.18</td><td>89.81</td><td>89.80</td><td>89.28</td><td>89.03</td><td>81.05</td><td>81.63</td><td>91.04</td><td>90.48</td></tr><tr><td>20%</td><td>77.27</td><td>77.95</td><td>82.57</td><td>82.57</td><td>78.91</td><td>79.07</td><td>79.26</td><td>79.29</td><td>82.60</td><td>82.49</td><td>79.88</td><td>80.64</td><td>90.86</td><td>90.15</td></tr><tr><td>40%</td><td>73.70</td><td>73.85</td><td>74.37</td><td>75.08</td><td>59.92</td><td>61.78</td><td>63.62</td><td>64.21</td><td>66.43</td><td>67.15</td><td>76.56</td><td>76.62</td><td>85.06</td><td>84.19</td></tr><tr><td>60%</td><td>57.14</td><td>57.89</td><td>56.40</td><td>58.24</td><td>34.79</td><td>36.21</td><td>42.00</td><td>43.19</td><td>43.23</td><td>45.37</td><td>69.92</td><td>70.55</td><td>73.29</td><td>72.90</td></tr><tr><td rowspan="5">CrossPlatform</td><td>5%</td><td>68.00</td><td>67.34</td><td>61.88</td><td>61.04</td><td>98.97</td><td>98.99</td><td>97.67</td><td>97.69</td><td>98.91</td><td>98.91</td><td>67.66</td><td>67.59</td><td>99.71</td><td>99.71</td></tr><tr><td>10%</td><td>66.40</td><td>65.92</td><td>59.61</td><td>59.62</td><td>98.39</td><td>98.41</td><td>95.19</td><td>95.24</td><td>98.32</td><td>98.32</td><td>63.67</td><td>63.45</td><td>99.56</td><td>99.55</td></tr><tr><td>20%</td><td>62.53</td><td>62.39</td><td>57.89</td><td>58.07</td><td>94.46</td><td>94.49</td><td>90.67</td><td>90.75</td><td>93.51</td><td>93.58</td><td>61.48</td><td>61.14</td><td>98.76</td><td>98.75</td></tr><tr><td>40%</td><td>55.32</td><td>55.51</td><td>50.54</td><td>50.49</td><td>78.42</td><td>79.30</td><td>73.98</td><td>75.12</td><td>80.47</td><td>80.92</td><td>53.91</td><td>52.44</td><td>95.34</td><td>95.20</td></tr><tr><td>60%</td><td>43.29</td><td>44.76</td><td>39.76</td><td>41.21</td><td>56.26</td><td>59.04</td><td>48.54</td><td>50.62</td><td>57.22</td><td>58.94</td><td>43.44</td><td>40.76</td><td>84.33</td><td>84.29</td></tr><tr><td rowspan="5">USTC-TFC</td><td>5%</td><td>62.40</td><td>57.64</td><td>87.50</td><td>87.61</td><td>95.03</td><td>94.98</td><td>94.82</td><td>94.82</td><td>94.62</td><td>94.58</td><td>93.75</td><td>94.91</td><td>96.07</td><td>96.02</td></tr><tr><td>10%</td><td>63.94</td><td>60.83</td><td>86.95</td><td>86.89</td><td>93.79</td><td>93.77</td><td>94.00</td><td>93.95</td><td>93.79</td><td>93.99</td><td>93.36</td><td>94.71</td><td>95.65</td><td>95.60</td></tr><tr><td>20%</td><td>62.65</td><td>59.95</td><td>84.76</td><td>84.70</td><td>92.33</td><td>92.34</td><td>86.13</td><td>86.46</td><td>89.86</td><td>89.75</td><td>91.02</td><td>92.91</td><td>94.20</td><td>93.93</td></tr><tr><td>40%</td><td>56.26</td><td>50.56</td><td>77.89</td><td>77.52</td><td>81.98</td><td>81.69</td><td>74.12</td><td>73.82</td><td>80.54</td><td>80.11</td><td>89.06</td><td>91.41</td><td>91.72</td><td>91.69</td></tr><tr><td>60%</td><td>51.73</td><td>50.98</td><td>70.62</td><td>70.22</td><td>58.59</td><td>58.09</td><td>47.62</td><td>48.11</td><td>56.31</td><td>56.57</td><td>75.78</td><td>75.02</td><td>78.88</td><td>78.71</td></tr><tr><td rowspan="5">Malware</td><td>5%</td><td>78.16</td><td>77.86</td><td>77.81</td><td>77.90</td><td>85.95</td><td>86.01</td><td>92.57</td><td>92.59</td><td>93.11</td><td>93.11</td><td>65.62</td><td>66.77</td><td>93.38</td><td>93.33</td></tr><tr><td>10%</td><td>76.63</td><td>76.36</td><td>76.71</td><td>76.67</td><td>84.46</td><td>84.34</td><td>90.54</td><td>90.56</td><td>90.95</td><td>90.94</td><td>63.28</td><td>64.85</td><td>91.35</td><td>91.28</td></tr><tr><td>20%</td><td>76.43</td><td>76.14</td><td>75.78</td><td>75.83</td><td>77.83</td><td>78.03</td><td>81.49</td><td>81.43</td><td>83.51</td><td>83.50</td><td>62.50</td><td>64.19</td><td>88.24</td><td>88.03</td></tr><tr><td>40%</td><td>71.26</td><td>70.67</td><td>71.40</td><td>71.08</td><td>61.35</td><td>61.49</td><td>65.27</td><td>65.39</td><td>67.97</td><td>68.49</td><td>57.23</td><td>58.83</td><td>83.51</td><td>83.33</td></tr><tr><td>60%</td><td>63.02</td><td>62.71</td><td>57.81</td><td>57.13</td><td>42.43</td><td>43.83</td><td>46.08</td><td>47.16</td><td>46.35</td><td>46.45</td><td>55.47</td><td>56.21</td><td>73.11</td><td>72.61</td></tr></table>

# 4.2 Comparison with Baselines

Traffic Classification Baselines. The performance of our method and other traffic analysis methods on the four traffic datasets under different noise ratios is shown in Table 1. Overall, the performance of all baselines degrades significantly as the label noise rate increases, which highlights the substantial impact of label noise on DL-based methods. Traditional models such as Appscanner and FS-Net are particularly vulnerable, showing rapid performance drops even under moderate noise. Although advanced pre-training methods such as ET-BERT, MAE, and YaTC perform well under low-noise settings such as 5% and 10%, their robustness deteriorates noticeably as the noise level increases. MCRe, which is designed for handling label noise in malicious traffic, shows strong robustness on the USTC-TFC that includes multiple benign and malicious traffic categories. However, its performance degrades significantly on other general classification tasks, such as VPN or mobile app traffic, as well as on the Malware dataset, which contains only recent malware families, due to its reliance on distinct benign-malicious separability.

We can observe that FLOWREFINER consistently outperforms all baselines across datasets and noise levels. Our traffic semantics-driven noise detector and confidence-guided label correction can validly isolate noisy labels and refine the raw flows. Then, the cross-granularity robust classifier can capture meaningful hierarchical semantics and avoid remembering specific noisy flows. As a result, our method consistently achieves accuracy and F1 scores exceeding 70% even at a 60% label noise ratio, where the majority of training samples are incorrectly labeled. Besides, FLOWREFINER also shows better packet-level classification performance compared to the advanced packet classifiers in Appendix G. It can be concluded that our method provides a robust traffic classification framework against label noise to achieve superior performance on various traffic datasets under noisy label conditions.

Label Noise Learning Baselines. We further reproduce six general label noise learning methods from other fields on traffic data with consistent encoders for fair comparison, as illustrated in Table 2. LSR and SCE show almost no improvement over CE (i.e., the baseline), while Mixup and GCE can handle label noise relatively effectively due to the interpolating and adaptive loss design. More advanced methods, such as Co-teaching and Dividemix, achieve competitive performance. However, Co-teaching relies on a fixed forgetting rate to select small-loss samples as noise, which could not satisfy various noise conditions. DivideMix, on the other hand, uses a Gaussian mixture model based on loss value distribution to distinguish noise, but it fails when clean or noisy samples are too few to support reliable modeling. In contrast, our method detects noisy flows by modeling traffic semantics rather than relying on loss value distribution, making it more aligned with the nature of traffic data. The results show that FLOWREFINER achieves high performance under different noise ratios and leads the noisy label learning baseline by a large margin.

Table 2: Comparison of F1 Scores with Label Noise Learning Baselines under Different Noise Ratios. 

<table><tr><td rowspan="2">Method</td><td colspan="5">ISCXVPN</td><td colspan="5">CrossPlatform</td><td colspan="5">USTC-TFC</td><td colspan="5">Malware</td></tr><tr><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td></tr><tr><td>CE</td><td>78.38</td><td>77.66</td><td>74.65</td><td>56.42</td><td>39.95</td><td>93.29</td><td>92.20</td><td>85.75</td><td>70.86</td><td>48.07</td><td>86.67</td><td>83.58</td><td>80.56</td><td>66.25</td><td>50.76</td><td>78.60</td><td>78.11</td><td>78.78</td><td>64.93</td><td>52.94</td></tr><tr><td>LSR</td><td>78.22</td><td>76.29</td><td>75.65</td><td>58.03</td><td>41.43</td><td>94.56</td><td>90.45</td><td>87.45</td><td>70.81</td><td>48.41</td><td>88.73</td><td>84.93</td><td>78.36</td><td>67.52</td><td>55.27</td><td>87.91</td><td>83.74</td><td>81.93</td><td>65.58</td><td>55.03</td></tr><tr><td>Mixup</td><td>79.33</td><td>77.79</td><td>79.10</td><td>66.46</td><td>48.31</td><td>90.83</td><td>89.05</td><td>86.58</td><td>78.48</td><td>61.59</td><td>91.89</td><td>90.29</td><td>87.40</td><td>73.77</td><td>64.12</td><td>89.77</td><td>88.12</td><td>82.22</td><td>73.33</td><td>62.63</td></tr><tr><td>GCE</td><td>75.39</td><td>74.59</td><td>71.80</td><td>65.08</td><td>49.05</td><td>93.29</td><td>92.81</td><td>92.19</td><td>90.19</td><td>79.69</td><td>82.28</td><td>80.38</td><td>78.42</td><td>77.00</td><td>68.01</td><td>86.22</td><td>81.76</td><td>80.15</td><td>74.59</td><td>64.46</td></tr><tr><td>SCE</td><td>77.04</td><td>73.80</td><td>73.44</td><td>59.49</td><td>40.68</td><td>94.04</td><td>93.41</td><td>87.12</td><td>76.82</td><td>60.33</td><td>86.74</td><td>85.10</td><td>85.04</td><td>73.84</td><td>56.54</td><td>88.87</td><td>83.90</td><td>77.93</td><td>67.79</td><td>56.61</td></tr><tr><td>Co-teaching</td><td>78.24</td><td>84.14</td><td>87.65</td><td>76.69</td><td>55.89</td><td>82.29</td><td>87.83</td><td>92.04</td><td>83.93</td><td>62.61</td><td>86.24</td><td>88.16</td><td>81.21</td><td>81.21</td><td>57.22</td><td>86.85</td><td>88.20</td><td>84.20</td><td>80.80</td><td>60.29</td></tr><tr><td>Dividemix</td><td>81.93</td><td>83.79</td><td>81.24</td><td>76.61</td><td>68.88</td><td>84.48</td><td>86.72</td><td>86.63</td><td>81.62</td><td>75.34</td><td>89.16</td><td>87.77</td><td>91.11</td><td>84.84</td><td>78.43</td><td>85.91</td><td>86.15</td><td>83.47</td><td>82.41</td><td>70.34</td></tr><tr><td>Ours</td><td>93.34</td><td>90.48</td><td>90.15</td><td>84.19</td><td>72.90</td><td>99.71</td><td>99.55</td><td>98.75</td><td>95.20</td><td>84.29</td><td>96.02</td><td>95.60</td><td>93.93</td><td>91.69</td><td>78.71</td><td>93.33</td><td>91.28</td><td>88.03</td><td>83.33</td><td>72.61</td></tr></table>

Table 3: Comparison of F1 Scores on Class-dependent Noise Scenarios. 

<table><tr><td>Method</td><td>ISCXVPN</td><td>USTC-TFC</td></tr><tr><td>YaTC</td><td>77.01%</td><td>86.01%</td></tr><tr><td>MCRe</td><td>76.76%</td><td>80.47%</td></tr><tr><td>Co-teaching</td><td>76.80%</td><td>76.17%</td></tr><tr><td>DivideMix</td><td>74.14%</td><td>85.94%</td></tr><tr><td>Mixup</td><td>69.86%</td><td>78.56%</td></tr><tr><td>Ours</td><td>80.97%</td><td>88.40%</td></tr></table>

![](images/998a573feb474af46077e6d9c67ef2017869e1944fc683a405fed3c1cb83cc4a.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | ISCXVPN | CrossPlatform | USTC-TFC | Malware |
| --------------- | ------- | ------------- | -------- | ------- |
| 5               | 80      | 90            | 85       | 80      |
| 10              | 80      | 90            | 85       | 80      |
| 20              | 80      | 90            | 85       | 80      |
| 40              | 80      | 90            | 85       | 80      |
| 60              | 80      | 90            | 85       | 80      |
</details>

![](images/6b234993d73656a9456de871a9f5fbd49cb47780b9e35276b35e8383019ee8b7.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | ISCXVPN | CrossPlatform | USTC-TFC | Malware |
| --------------- | ------- | ------------- | -------- | ------- |
| 5               | 80      | 95            | 95       | 80      |
| 10              | 85      | 95            | 95       | 85      |
| 20              | 90      | 95            | 95       | 90      |
| 40              | 95      | 95            | 95       | 95      |
| 60              | 95      | 95            | 95       | 95      |
</details>

![](images/5d421c9e940a5104238e0bc88a65b305c726baddf6f135abca9727b845533276.jpg)

<details>
<summary>bar</summary>

|        | MCRe  | Ours  |
| ------ | ----- | ----- |
| Detection | 47.31 | 84.61 |
| Correction | 59.23 | 81.92 |
</details>

Figure 3: Performance of (a) noise detection, (b) noise correction, and (c) real-world evaluation.

Class-dependent Noise Evaluation. Class-dependent noise occurs when the probability of label corruption is not uniform across classes, meaning certain classes are more prone to having mislabeled samples than others. We perform the evaluation on ISCXVPN and USTC-TFC with different ratios of class-dependent noise, where categories with similar patterns are more likely to be mislabeled as each other. The average F1 scores among noise ratios of FLOWREFINER and optimal baselines are shown in Figure 3. The complete results of all baselines and noise ratios are detailed in Appendix H. It can be observed that all methods perform worse compared to the complete random noise setting, since the class-dependent noise leads to more severe category confusion and shifted decision boundaries. Note that our method can still achieve significant performance advantages over the optimal baseline, demonstrating better robustness under different noise types.

# 4.3 Label Noise Evaluation

Noise Detection Performance. We evaluate the performance of the traffic semantics-driven noise detector in Figure 3 (a). The detector consistently identifies a large portion of noisy-labeled flows across all datasets, with the detection ratio, i.e., the proportion of detected noise among all noisy samples, remaining above 75% even at 60% noise. This robustness is particularly valuable in securitysensitive tasks such as malware detection, where undetected noise may lead to critical failures. These results confirm the detector’s effectiveness in isolating noisy flows and supporting reliable traffic annotation and management.

Noise Correction Performance. The confidence-guided label correction is responsible for correcting the labels of the previously selected noisy flows. The correction ratio, i.e. accuracy of the noisy flow correction, is shown in Figure 3 (b). It can be seen that our method can accurately select and assign the correct labels to noisy flows based on prediction confidence, consistently achieving a correction accuracy of over 80% in most scenarios. Particularly on the CrossPlatform and USTC-TFC datasets, labels are almost all correctly assigned to the selected noisy flows, demonstrating the notable performance of the label predictor in this module.

Real-World Noisy Dataset Evaluation. Previous studies (20; 21) have revealed significant label noise in the CICIDS2017 dataset (51), and provide a corrected version with revised flow labels. Based on the dataset, we conduct a real-world evaluation, where the training set retains the original noisy labels, and the test set is relabeled according to (20). MCRe, the other traffic label noise method and the only baseline capable of both detecting and correcting label noise, is introduced to the comparison. As shown in Figure 3 (c), our method successfully identifies 84.61% of the noisy flows in training set, significantly outperforming MCRe. Furthermore, the accuracy of our noise detection is 81.92%, achieving high agreement with the expert relabeling.

Table 4: Ablation Study of F1 Scores on The Four Traffic Datasets. The abbreviations are explained as follows: TSND: Traffic Semantics-Driven Noise Detector, CLC: Confidence-Guided Label Correction Module, CRC: Cross-Granularity Robust Classifier. 

<table><tr><td rowspan="2">Method</td><td colspan="5">ISCXVPN</td><td colspan="5">CrossPlatform</td><td colspan="5">USTC-TFC</td><td colspan="5">Malware</td></tr><tr><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td><td>5%</td><td>10%</td><td>20%</td><td>40%</td><td>60%</td></tr><tr><td>Ours</td><td>93.34</td><td>90.48</td><td>90.15</td><td>84.19</td><td>72.90</td><td>99.71</td><td>99.55</td><td>98.75</td><td>95.20</td><td>84.29</td><td>96.02</td><td>95.60</td><td>93.93</td><td>91.69</td><td>78.71</td><td>93.33</td><td>91.28</td><td>88.03</td><td>83.33</td><td>72.61</td></tr><tr><td>w/o TSND</td><td>93.00</td><td>88.99</td><td>84.10</td><td>64.27</td><td>48.60</td><td>97.69</td><td>95.93</td><td>88.52</td><td>68.84</td><td>46.85</td><td>95.99</td><td>93.87</td><td>91.43</td><td>75.66</td><td>48.95</td><td>93.14</td><td>92.27</td><td>84.14</td><td>67.65</td><td>47.42</td></tr><tr><td>w/o CLC</td><td>88.85</td><td>85.09</td><td>80.12</td><td>77.76</td><td>69.71</td><td>92.81</td><td>90.84</td><td>89.69</td><td>86.35</td><td>78.01</td><td>94.88</td><td>93.26</td><td>92.78</td><td>89.70</td><td>77.59</td><td>80.32</td><td>79.15</td><td>79.11</td><td>74.78</td><td>65.29</td></tr><tr><td>w/o CRC</td><td>91.33</td><td>88.39</td><td>85.05</td><td>78.42</td><td>65.16</td><td>97.99</td><td>98.07</td><td>95.41</td><td>88.23</td><td>70.04</td><td>95.55</td><td>95.40</td><td>93.38</td><td>90.01</td><td>74.60</td><td>86.95</td><td>89.56</td><td>83.85</td><td>78.68</td><td>63.87</td></tr></table>

# 4.4 Ablation Study

The ablation study is conducted to evaluate the contribution of each component in FLOWREFINER. As shown in Table 4, the performance declines consistently on all traffic datasets when any of the key components is removed. In particular, the removal of the traffic semantics-driven noise detector (TSND) results in the most severe performance degradation under high noise ratios. For example, on the ISCXVPN dataset with 60% noise, removing TSND leads to a significant drop in accuracy from 73.29% to 47.62%. Similarly, on the CrossPlatform dataset, accuracy drops from 84.33% to 44.89%. This highlights the critical role of the TSND in accurately identifying and isolating noisy flows, which ensures that the subsequent components operate with more reliable data. When the confidence-guided label correction (CLC) is ablated, the performance also degrades, suggesting that this component can effectively against label noise by handling difficult cases and expanding the clean set. Note that our method has less performance degradation on the USTC-TFC dataset compared to other datasets under the ablation of CLC. This is because our noise detector has detected most of the noisy flows in USTC-TFC according to Figure 3, offering a highly clean flow set for traffic classifier training. Finally, the removal of the structure of cross-granularity robust classifier (CRC) results in stable performance reductions under all datasets and noise ratios. It proves that the joint task of both flow and packet classification could improve the robustness under different noise ratios.

# 4.5 Discussions

The Impact of Parameters. We investigate the effect of two key parameters in our noise detection module: the clustering granularity n and the majority label count. The clustering granularity n defines the total number of clusters $K = n \times C$ , where C is the number of classes. It controls how finely label-independent semantics are modeled. As shown in Figure 4, on the ISCXVPN dataset, increasing n from 1 to 5 notably improves the F1 score. A setting of $n = 5$ achieves optimal performance by balancing semantic sensitivity and robustness, whereas higher values $( \mathbf { e } . \mathbf { g } . , n = 7 )$ ) lead to over-segmentation and misclassification of clean samples as noise. The majority label count determines how many of the most frequent labels in each cluster are retained as clean. Using only the top-1 label (count = 1) can misclassify semantically similar clean flows as noise, while larger counts may retain actual noisy samples. As shown in Figure 4, a count of 2 provides the best trade-off across noise ratios by tolerating intra-cluster semantic variation without sacrificing detection precision. Overall, both parameters play a critical role in balancing noise detection sensitivity and robustness, with $n = 5$ and majority label count = 2 yielding consistently strong performance across settings.

![](images/30204cfc7584d5d03593c4e46579752d92842fb9e407b68473841c43187f6ff4.jpg)

<details>
<summary>line</summary>

| Clustering Granularity | 5%   | 10%  | 20%  | 40%  | 60%  |
| ---------------------- | ---- | ---- | ---- | ---- | ---- |
| 1                      | 90   | 88   | 86   | 84   | 82   |
| 3                      | 92   | 90   | 88   | 86   | 84   |
| 5                      | 94   | 92   | 90   | 88   | 86   |
| 7                      | 95   | 93   | 91   | 89   | 87   |
</details>

![](images/8590d2eb1189f15f4c85fa9e691f34b33fa74a82e426ce20daffab94ba685ff9.jpg)

<details>
<summary>line</summary>

| Majority Label Count | 5%   | 10%  | 20%  | 40%  | 60%  |
| -------------------- | ---- | ---- | ---- | ---- | ---- |
| 1                    | 75   | 85   | 65   | 65   | 55   |
| 2                    | 95   | 88   | 88   | 85   | 60   |
| 3                    | 95   | 90   | 88   | 85   | 60   |
| 4                    | 95   | 90   | 88   | 75   | 60   |
</details>

Figure 4: Parameters Impact.

Limitations. As a deep learning-based method, FLOWREFINER requires substantial computational resources for efficient training, preferably with GPU acceleration. Our framework currently takes about 3 minutes on an RTX 3090 GPU with 2.79 GB of memory for training. In future work, we will continue to optimize the training pipeline to reduce computational overhead and improve accessibility, while also leveraging ongoing progress in lightweight inference and dedicated hardware accelerators, which are expected to further enhance the practicality and scalability of FLOWREFINER in real-world deployments.

# 5 Conclusion

In this paper, we proposed FLOWREFINER, a robust framework for general traffic classification under noisy label conditions. Our method addresses the significant challenges of label noise, including its detection, correction, and robust classification, thus reducing dependency on high-quality labeled data. Through the integration of a semantic-driven noise detector, confidence-guided label correction, and a cross-granularity robust classifier, FLOWREFINER effectively leverages noisy traffic to improve classification performance. Our experimental results across various datasets and scenarios demonstrate the ability of FLOWREFINER to outperform state-of-the-art methods in both accuracy and resilience to noise. This framework provides a valuable solution for enhancing general traffic analysis, particularly in environments where high-quality labels are difficult to obtain, and sets the stage for future advancements in traffic classification under noisy conditions.

# 6 Acknowledgement

The authors thank the anonymous reviewers for their valuable comments and suggestions that helped improve this paper. This work was supported in part by China National Funds for Distinguished Young Scientists under Grant 62425201; in part by the National Key Research and Development Program of China under Grant 2023YFB3107100; in part by the National Natural Science Foundation of China under Grant 62502089, Grant 62172093, Grant 62132011, and Grant U22B2025; in part by Basic Research Program of Jiangsu under Grant BK20251353; in part by Fundamental and Interdisciplinary Disciplines Breakthrough Plan of the Ministry of Education of China under Grant JYB2025XDXM114; and in part by Beijing-Tianjin-Hebei Natural Science Foundation Cooperation Project under Grant 25JJJJC0003.

# References

[1] C. Fu, Q. Li, M. Shen, and K. Xu, “Frequency domain feature based robust malicious traffic detection,” IEEE/ACM Transactions on Networking, vol. 31, no. 1, pp. 452–467, 2023.   
[2] Y. Mirsky, T. Doitshman, Y. Elovici, and A. Shabtai, “Kitsune: An ensemble of autoencoders for online network intrusion detection,” in Network and Distributed System Security Symposium (NDSS), 2018.   
[3] C. Fu, Q. Li, and K. Xu, “Detecting unknown encrypted malicious traffic in real time via flow interaction graph analysis,” in Network and Distributed System Security Symposium (NDSS), 2023.   
[4] E. Papadogiannaki and S. Ioannidis, “A survey on encrypted network traffic analysis applications, techniques, and countermeasures,” ACM Computing Surveys, vol. 54, no. 6, 2021.   
[5] G. Zhou, Z. Liu, C. Fu, Q. Li, and K. Xu, “An efficient design of intelligent network data plane,” in 32nd USENIX Security Symposium (USENIX Security), 2023.   
[6] R. Xie, J. Cao, E. Dong, M. Xu, K. Sun, Q. Li, L. Shen, and M. Zhang, “Rosetta: Enabling robust TLS encrypted traffic classification in diverse network environments with tcp-aware traffic augmentation,” in 32nd USENIX Security Symposium (USENIX Security), 2023, pp. 625–642.   
[7] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2016, pp. 439–454.   
[8] F. Al-Obaidy, S. Momtahen, M. F. Hossain, and F. Mohammadi, “Encrypted traffic classification based ml for identifying different social media applications,” in 2019 IEEE Canadian Conference of Electrical and Computer Engineering (CCECE). IEEE, 2019, pp. 1–5.   
[9] M. Conti, L. V. Mancini, R. Spolaor, and N. V. Verde, “Analyzing android encrypted network traffic to identify user actions,” IEEE Transactions on Information Forensics and Security, vol. 11, no. 1, pp. 114–125, 2015.

[10] P. Velan, M. Cermák, P. ˇ Celeda, and M. Drašar, “A survey of methods for encrypted traffic ˇ classification and analysis,” International Journal of Network Management, vol. 25, no. 5, pp. 355–374, 2015.   
[11] Z. Cao, G. Xiong, Y. Zhao, Z. Li, and L. Guo, “A survey on encrypted traffic classification,” in International Conference on Applications and Techniques in Information Security, 2014, pp. 73–81.   
[12] M. Shen, K. Ye, X. Liu, L. Zhu, J. Kang, S. Yu, Q. Li, and K. Xu, “Machine learning-powered encrypted network traffic analysis: A comprehensive survey,” IEEE Commun. Surv. Tutorials, vol. 25, no. 1, pp. 791–824, 2023.   
[13] M. Shen, Y. Liu, L. Zhu, K. Xu, X. Du, and N. Guizani, “Optimizing feature selection for efficient encrypted traffic classification: A systematic approach,” IEEE Network, vol. 34, no. 4, pp. 20–27, 2020.   
[14] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE Conference on Computer Communications (INFOCOM), 2019, pp. 1171–1179.   
[15] Y. Zeng, H. Gu, W. Wei, and Y. Guo, “Deep-full-range: a deep learning based network encrypted traffic classification and intrusion detection framework,” IEEE Access, vol. 7, pp. 45 182–45 190, 2019.   
[16] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in 2017 International conference on information networking (ICOIN), 2017, pp. 712–717.   
[17] J. Zhang, F. Li, F. Ye, and H. Wu, “Autonomous unknown-application filtering and labeling for dl-based traffic classifier update,” in IEEE Conference on Computer Communications (INFOCOM), 2020, pp. 397–405.   
[18] K. Lin, X. Xu, and H. Gao, “Tscrnn: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of iiot,” Computer Networks, vol. 190, p. 107974, 2021.   
[19] H. Song, M. Kim, D. Park, Y. Shin, and J.-G. Lee, “Learning from noisy labels with deep neural networks: A survey,” IEEE Transactions on Neural Networks and Learning Systems, vol. 34, no. 11, pp. 8135–8153, 2022.   
[20] G. Engelen, V. Rimmer, and W. Joosen, “Troubleshooting an intrusion detection dataset: the CICIDS2017 case study,” in IEEE Security and Privacy Workshops. IEEE, 2021, pp. 7–12.   
[21] L. Liu, G. Engelen, T. M. Lynar, D. Essam, and W. Joosen, “Error prevalence in NIDS datasets: A case study on CIC-IDS-2017 and CSE-CIC-IDS-2018,” in IEEE Conference on Communications and Network Security, 2022, pp. 254–262.   
[22] J. L. Guerra, C. Catania, and E. Veas, “Datasets are not enough: Challenges in labeling network traffic,” Computers & Security, vol. 120, p. 102810, 2022.   
[23] Y. Qing, Q. Yin, X. Deng, Y. Chen, Z. Liu, K. Sun, K. Xu, J. Zhang, and Q. Li, “Low-quality training data only? a robust framework for detecting encrypted malicious network traffic,” in NDSS, 2024.   
[24] Q. Yuan, G. Gou, Y. Zhu, Y. Zhu, G. Xiong, and Y. Wang, “Mcre: A unified framework for handling malicious traffic with noise labels based on multidimensional constraint representation,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 133–147, 2023.   
[25] J. Li, R. Socher, and S. C. Hoi, “Dividemix: Learning with noisy labels as semi-supervised learning,” in International Conference on Learning Representations (ICLR), 2020.   
[26] B. Han, Q. Yao, X. Yu, G. Niu, M. Xu, W. Hu, I. Tsang, and M. Sugiyama, “Co-teaching: Robust training of deep neural networks with extremely noisy labels,” Advances in neural information processing systems, vol. 31, 2018.

[27] Z. Zhang and M. Sabuncu, “Generalized cross entropy loss for training deep neural networks with noisy labels,” Advances in neural information processing systems, vol. 31, 2018.   
[28] Y. Wang, X. Ma, Z. Chen, Y. Luo, J. Yi, and J. Bailey, “Symmetric cross entropy for robust learning with noisy labels,” in IEEE/CVF International Conference on Computer Vision, 2019, pp. 322–330.   
[29] T. T. Nguyen and G. Armitage, “A survey of techniques for internet traffic classification using machine learning,” IEEE Communications Surveys & Tutorials, vol. 10, no. 4, pp. 56–76, 2008.   
[30] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, 2016.   
[31] H. He, Z. Yang, and X. Chen, “Pert: Payload encoding representation from transformer for encrypted traffic classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation, 2020, pp. 1–8.   
[32] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in ACM Web Conference (WWW), 2022, pp. 633–642.   
[33] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” in North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT), 2019, pp. 4171– 4186.   
[34] Z. Hang, Y. Lu, Y. Wang, and Y. Xie, “Flow-mae: Leveraging masked autoencoder for accurate, efficient and robust malicious traffic classification,” in Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses, 2023, pp. 297–314.   
[35] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation,” in Thirty-Seventh AAAI Conference on Artificial Intelligence (AAAI), 2023, pp. 5420–5427.   
[36] K. He, X. Chen, S. Xie, Y. Li, P. Dollár, and R. Girshick, “Masked autoencoders are scalable vision learners,” in IEEE/CVF conference on computer vision and pattern recognition, 2022, pp. 16 000–16 009.   
[37] C. Zhang, S. Bengio, M. Hardt, B. Recht, and O. Vinyals, “Understanding deep learning (still) requires rethinking generalization,” Communications of the ACM, vol. 64, no. 3, pp. 107–115, 2021.   
[38] Q. Yuan, C. Liu, W. Yu, Y. Zhu, G. Xiong, Y. Wang, and G. Gou, “Boau: Malicious traffic detection with noise labels based on boundary augmentation,” Computers & Security, vol. 131, p. 103300, 2023.   
[39] Q. Yuan, Y. Zhu, G. Xiong, Y. Wang, W. Yu, B. Lu, and G. Gou, “Uldc: Unsupervised learningbased data cleaning for malicious traffic with high noise,” The Computer Journal, vol. 67, no. 3, pp. 976–987, 2024.   
[40] Y. Qing, Q. Yin, X. Deng, Y. Chen, Z. Liu, K. Sun, K. Xu, J. Zhang, and Q. Li, “Low-quality training data only? A robust framework for detecting encrypted malicious network traffic,” 2024.   
[41] H. Zhang, M. Cissé, Y. N. Dauphin, and D. Lopez-Paz, “mixup: Beyond empirical risk minimization,” in International Conference on Learning Representations (ICLR), 2018.   
[42] F. Fooladgar, M. N. N. To, P. Mousavi, and P. Abolmaesumi, “Manifold dividemix: A semisupervised contrastive learning framework for severe label noise,” in IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops, 2024, pp. 4012–4021.   
[43] D. Arpit, S. Jastrz˛ebski, N. Ballas, D. Krueger, E. Bengio, M. S. Kanwal, T. Maharaj, A. Fischer, A. Courville, Y. Bengio et al., “A closer look at memorization in deep networks,” in International conference on machine learning. PMLR, 2017, pp. 233–242.

[44] S. Liu, J. Niles-Weed, N. Razavian, and C. Fernandez-Granda, “Early-learning regularization prevents memorization of noisy labels,” Advances in neural information processing systems, vol. 33, pp. 20 331–20 342, 2020.   
[45] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP), 2016, pp. 407–414.   
[46] T. Van Ede, R. Bortolameotti, A. Continella, J. Ren, D. J. Dubois, M. Lindorfer, D. Choffnes, M. van Steen, and A. Peter, “Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic,” in Network and distributed system security symposium (NDSS), vol. 27, 2020.   
[47] Malware2023 Dataset, “A source for packet capture (pcap) files and malware samples,” https: //malware-traffic-analysis.net/, accessed 2023.   
[48] M. Lotfollahi, M. Jafari Siavoshani, R. Shirali Hossein Zade, and M. Saberian, “Deep packet: A novel approach for encrypted traffic classification using deep learning,” Soft Computing, vol. 24, no. 3, pp. 1999–2012, 2020.   
[49] M. Lukasik, S. Bhojanapalli, A. Menon, and S. Kumar, “Does label smoothing mitigate label noise?” in International Conference on Machine Learning, 2020, pp. 6448–6458.   
[50] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,” in International Conference on Learning Representations (ICLR), 2019.   
[51] I. Sharafaldin, A. Gharib, A. H. Lashkari, A. A. Ghorbani et al., “Towards a reliable intrusion detection benchmark dataset,” Software Networking, vol. 2018, no. 1, pp. 177–200, 2018.

# Appendix

# A Building of the Traffic Semantics-oriented Encoder

Figure 5 depicts the process of building the traffic semantics-oriented encoder with the pre-training paradigm of a masked autoencoder (MAE). Initially, the network traffic data captured from Pcap files undergoes preprocessing to extract and resize the flow content, ensuring the data is in a suitable format for model training. The processed traffic data is then intentionally masked, and input into the traffic encoder, which employs the principles of an MAE by aiming to recover the original data from its corrupted form. The encoder learns to extract robust feature representations by focusing on the structure left intact by the masking process. Finally, the encoded features are passed through a decoder that attempts to reconstruct the original input, thereby enabling the model to learn critical data characteristics effectively and allowing the encoder to extract effective traffic semantics.

![](images/a9eed4c2c72b08fa128bcebbe0c9ea056781481a95acd1ed1efb3a2bcd4df463.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Traffic Pcap"] --> B["x_i"]
    B --> C["Flow Content"]
    C --> D["Resized Content"]
    D --> E["Masked"]
    E --> F["Traffic Encoder"]
    F --> G["Feature Vector"]
    G --> H["Decoder"]
    H --> I["Target"]
    I --> F
    F --> J["For Noise Detector"]
```
</details>

Figure 5: The pre-training paradigm of masked autoencoder for building traffic semantics-oriented encoder.

# B Two Categories of the Predicted Labels from the Traffic Label Predictor

Based on the label predictor fine-tuned on the clean flows, we could obtain the predicted labels of detected noisy flows. As shown in Figure 6, we refine the labels of noisy flows into two categories, i.e., high-confidence flow labels and low-confidence flow labels. The samples with high-confidence labels share a similar distribution with the clean set, and we use the prediction results to correct their labels. The samples with low-confidence flow labels represent difficult instances for the predictor. Thus, we retain their original labels and introduce them to the refined flows to maintain diversity and expand the semantic distribution of samples.

![](images/68a0223f87bc8b42a0385a3c54e374a0d560fb314ebc7f276f2633468756b883.jpg)

<details>
<summary>bar</summary>

| Class | Confidence |
|---|---|
| Class 1 | Low |
| Class 2 | Low |
| Class 3 | Low |
| Class 4 | High |
| Class 5 | Low |
| Class 6 | Low |
| Class 7 | Low |
</details>

Figure 6: Two categories of the predicted labels from the traffic label predictor.

# C The Structure Detail of the Cross-Granularity Robust Classifier

Figure 7 presents the structure of the Cross-Granularity Robust Classifier, which is designed to classify network traffic at both the packet and flow levels. In the flow-level traffic classifier, multiple parallel packet encoders process each individual packet from the flow. These encoders share weights,

indicating that they operate under a unified framework to maintain consistency in feature extraction across different packets. The encoded packet features are then aggregated to form a comprehensive representation of the flow, which is subsequently used to perform the flow-level traffic classification for the entire flow. This structure of parallel packet encoders of the flowlevel classifier enables a share-weight individual packet encoder to process packet-level input and thus perform packet-level classification. In detail, a packet is selected randomly from the flow sample, and then classified by the packetlevel traffic classifier. This dual approach allows the system to leverage fine-grained packet-level data along with aggregated flow-level information, enhancing the robustness and accuracy of the traffic classification.

![](images/a38ad98b171f705837861f3ccecff1174e2ec6f6f6ef4cd4f6695ca86fa847f2.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Flow"] --> B["Packet"]
    B --> C["Random Select"]
    C --> D["Packet"]
    D --> E["Packet-level Traffic Classifier"]
    E --> F["Packet-level Traffic Classifier"]
    F --> G["Aggregator"]
    G --> H["Flow-level Classification"]
    I["Packet"] --> J["Packet"]
    J --> K["Packet-level Traffic Classifier"]
    K --> L["Packet-level Classification"]
    M["Random Select"] --> N["Packet"]
    N --> O["Packet-level Traffic Classifier"]
    O --> P["Aggregator"]
    P --> Q["\tilde{y}_i"]
    R["Packet"] --> S["Packet"]
    S --> T["Packet-level Traffic Classifier"]
    T --> U["Aggregator"]
    U --> V["\tilde{y}_i^p"]
    style A fill:#f9f,stroke:#333
    style B fill:#ccf,stroke:#333
    style C fill:#cfc,stroke:#333
    style D fill:#fcc,stroke:#333
    style E fill:#cff,stroke:#333
    style F fill:#ffc,stroke:#333
    style G fill:#fcf,stroke:#333
    style H fill:#cff,stroke:#333
    style I fill:#ffc,stroke:#333
    style J fill:#cfc,stroke:#333
    style K fill:#cfc,stroke:#333
    style L fill:#cfc,stroke:#333
    style M fill:#fcc,stroke:#333
    style N fill:#cfc,stroke:#333
    style O fill:#cfc,stroke:#333
    style P fill:#cfc,stroke:#333
    style Q fill:#cfc,stroke:#333
```
</details>

Figure 7: The structure detail of the crossgranularity robust classifier.

# D Dataset Information

The details of the four real-world traffic datasets used in this work are shown as follows:

• ISCXVPN (45) contains 7 categories of encrypted traffic, collected by the Canadian Institute for Cybersecurity via OpenVPN. The dataset consists of 2,275 training samples and 569 test samples.   
• CrossPlatform (46) includes encrypted traffic data from various platforms. In our experiments, we use IOS application traffic in the China region, comprising 30 different categories. The dataset consists of 5,429 training samples and 1,372 test samples.   
• USTC-TFC (16) is a traffic dataset with 10 categories of benign application traffic and 10 categories of malware traffic. The dataset consists of 1,914 training samples and 483 test samples.   
• Malware (47) is a recently published dataset featuring traffic from 10 malware families, available at https://malware-traffic-analysis.net/about.html. The dataset consists of 2,938 training samples and 740 test samples.

# E Baselines

To evaluate the performance of our method, we use six state-of-the-art traffic classification methods and five label noise learning methods as baselines. The following traffic classification baselines include one traditional machine learning method, three traditional deep learning methods, and three advanced pre-training methods.

• Appscanner (7): A traditional machine learning tool that classifies traffic using handcrafted flow-based features, often less resilient to noisy or encrypted data.   
• FS-Net (14): A flow-based model incorporating both classification and reconstruction tasks, enhancing its robustness to noise and improving semantic feature extraction.   
• ET-BERT (32): A BERT-like Transformer pre-trained model, leveraging self-supervised learning to capture flow-level semantic patterns, offering strong resilience to label noise.   
• MAE (34): A self-supervised traffic classifier based on Masked Autoencoder (MAE), masking parts of traffic flows and reconstructing them, which makes it robust in noisy conditions.   
• YaTC (35): A hybrid traffic classification model combining supervised and self-supervised learning, balancing noise handling and effective traffic feature extraction.   
• MCRe (24): A state-of-the-art traffic analysis method focuses on malicious traffic label noise learning.

In addition, we introduce the following label noise learning baselines, all of which use the same encoder structure for fair comparison.

![](images/f0b425f80ed6b4d92843574436b7cbac3e957b436081bf375ab315d45713b782.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | Deeppacket | CNN  | ET-BERT | Ours |
| --------------- | ---------- | ---- | ------- | ---- |
| 5               | 70         | 70   | 70      | 90   |
| 10              | 60         | 65   | 65      | 85   |
| 40              | 50         | 55   | 50      | 75   |
| 60              | 40         | 45   | 30      | 60   |
</details>

![](images/fc0295ac5c0c5d9a70a0a66f28539fe2795d6f39b34597b144d32202678f8520.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | Deeppacket | CNN  | ET-BERT | Ours |
| --------------- | ---------- | ---- | ------- | ---- |
| 5               | 30         | 65   | 85      | 95   |
| 10              | 25         | 60   | 80      | 90   |
| 20              | 20         | 55   | 70      | 85   |
| 40              | 15         | 45   | 60      | 80   |
| 60              | 10         | 35   | 40      | 70   |
</details>

![](images/5db83a88c9c138dae865c58a2cbb6cf4166ef522c6022934c481f7bbd27eeb55.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | Deeppacket | ET-BERT | CNN  | Ours |
| --------------- | ---------- | ------- | ---- | ---- |
| 5               | 75         | 75      | 70   | 90   |
| 10              | 70         | 70      | 65   | 85   |
| 20              | 65         | 65      | 60   | 80   |
| 40              | 60         | 60      | 55   | 75   |
| 60              | 55         | 55      | 50   | 70   |
</details>

![](images/fbd223b1c370d91ca60b489ab4c5c84ce9741f0bd28dda11d2aeb2292bd88240.jpg)

<details>
<summary>line</summary>

| Noise Ratio (%) | Deeppacket | ET-BERT | CNN | Ours |
| --------------- | ---------- | ------- | --- | ---- |
| 5               | 50         | 45      | 70  | 85   |
| 10              | 50         | 40      | 65  | 80   |
| 20              | 50         | 35      | 60  | 75   |
| 40              | 45         | 30      | 50  | 70   |
| 60              | 40         | 25      | 40  | 60   |
</details>

Figure 8: Comparison of packet classification performance with packet-level baselines.

• CE: A standard cross-entropy loss used in classification tasks, which can be sensitive to label noise as it directly penalizes incorrect predictions.   
• LSR (49): Label Smoothing Regularization reduces model overconfidence by distributing probability mass to incorrect labels, making the model more robust to noise.   
• Mixup (41): A data augmentation technique that generates synthetic samples by interpolating between two samples and their labels, helping the model generalize better under noisy conditions.   
• GCE (27): Generalized Cross-Entropy blends the advantages of MAE and CE to address label noise, making it more robust by adjusting the loss function dynamically.   
• SCE (28): Symmetric Cross-Entropy introduces a correction term to balance the standard CE loss, aiming to better handle noisy labels by mitigating over-penalization of incorrect predictions.   
• Co-teaching (26): Trains two networks simultaneously and lets them teach each other by selecting small-loss samples, assuming that clean samples have lower loss values. This helps filter out noisy labels during training.   
• DivideMix (25): Uses a Gaussian mixture model to divide samples into clean and noisy sets based on loss values, then applies semi-supervised learning to train the model using both labeled and unlabeled data.

# F Hyperparameter Information

In all experiments, we use a batch size of 64, train for 20 epochs, and optimize with AdamW (50) using a learning rate of $4 \times 1 0 ^ { - 3 }$ . For noise detection, we set the clustering granularity to $n = 5$ , with the top $m = 2$ most frequent labels in each cluster considered as majority labels. Confidence thresholds are set at $\tau _ { h } = 0 . 9$ and $\tau _ { l } = 0 . 7$ to balance precision and recall in noise filtering. Importantly, we apply the same hyperparameter settings across all datasets, demonstrating that our method achieves strong performance without extensive tuning, highlighting its robustness to hyperparameter choices.

Table 5: Hyperparameter settings in our experiments. 

<table><tr><td>Parameter</td><td>Setting</td></tr><tr><td>Batch size</td><td>64</td></tr><tr><td>Epochs</td><td>20</td></tr><tr><td>Learning rate</td><td> $4 \times 10^{-3}$ </td></tr><tr><td>Optimizer</td><td>AdamW (50)</td></tr><tr><td>Clustering granularity (n)</td><td>5</td></tr><tr><td>Majority label count (m)</td><td>2</td></tr><tr><td>High confidence threshold ( $\tau_h$ )</td><td>0.9</td></tr><tr><td>Low confidence threshold ( $\tau_l$ )</td><td>0.7</td></tr></table>

# G Packet Classification Ability

The proposed cross-granularity robust classifier integrates both flow-level and packet-level traffic classification tasks against label noise, bringing the ability to serve as a robust packet classifier. We compare the packet-level classification performance with advanced packet classifiers, including Deeppacket (48), CNN (16), and ET-BERT (32). As shown in Figure 8, in packet-level traffic analysis tasks, where each sample contains less information, the classification methods suffer from label noise more. Only FLOWREFINER can achieve F1 scores higher than 80% under 20% noise ratio, while other packet-level baselines can hardly achieve 60%. It demonstrates that FLOWREFINER could obtain two levels of robust encrypted traffic classifier at once and adapt to different requirements.

Table 6: Comparison with Traffic Classification Baselines on Class-dependent Noise Scenarios. 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Noise</td><td colspan="2">Appscanner</td><td colspan="2">FS-Net</td><td colspan="2">ET-BERT</td><td colspan="2">MAE</td><td colspan="2">YaTC</td><td colspan="2">MCRe</td><td colspan="2">Ours</td></tr><tr><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td></tr><tr><td rowspan="5">ISCXVPN</td><td>5%</td><td>81.49</td><td>82.07</td><td>87.42</td><td>87.58</td><td>85.76</td><td>85.77</td><td>91.39</td><td>91.36</td><td>93.15</td><td>92.98</td><td>80.86</td><td>81.72</td><td>93.32</td><td>92.98</td></tr><tr><td>10%</td><td>81.16</td><td>81.70</td><td>85.78</td><td>86.21</td><td>81.90</td><td>81.69</td><td>90.51</td><td>90.45</td><td>91.21</td><td>91.13</td><td>78.52</td><td>79.29</td><td>92.62</td><td>92.28</td></tr><tr><td>20%</td><td>80.51</td><td>80.36</td><td>83.04</td><td>83.33</td><td>80.49</td><td>80.52</td><td>84.35</td><td>84.44</td><td>88.75</td><td>88.64</td><td>77.54</td><td>77.38</td><td>89.45</td><td>88.90</td></tr><tr><td>40%</td><td>67.20</td><td>68.15</td><td>69.14</td><td>70.29</td><td>55.18</td><td>55.99</td><td>68.71</td><td>69.50</td><td>67.31</td><td>68.28</td><td>74.61</td><td>74.75</td><td>78.03</td><td>77.29</td></tr><tr><td>60%</td><td>49.67</td><td>51.14</td><td>47.10</td><td>47.95</td><td>46.04</td><td>48.23</td><td>46.74</td><td>48.35</td><td>42.00</td><td>44.03</td><td>45.51</td><td>46.29</td><td>52.72</td><td>53.38</td></tr><tr><td rowspan="5">USTC-TFC</td><td>5%</td><td>62.14</td><td>62.15</td><td>86.33</td><td>86.53</td><td>94.20</td><td>94.18</td><td>93.58</td><td>93.52</td><td>95.24</td><td>94.20</td><td>94.12</td><td>94.25</td><td>94.62</td><td>94.50</td></tr><tr><td>10%</td><td>61.38</td><td>61.38</td><td>85.78</td><td>85.98</td><td>92.96</td><td>93.07</td><td>93.79</td><td>93.75</td><td>93.17</td><td>93.18</td><td>90.23</td><td>92.40</td><td>94.20</td><td>94.16</td></tr><tr><td>20%</td><td>60.86</td><td>55.61</td><td>80.39</td><td>79.97</td><td>91.51</td><td>91.52</td><td>88.61</td><td>88.62</td><td>90.68</td><td>90.65</td><td>89.45</td><td>91.80</td><td>92.13</td><td>92.15</td></tr><tr><td>40%</td><td>54.98</td><td>50.17</td><td>76.56</td><td>77.01</td><td>75.98</td><td>76.41</td><td>78.88</td><td>79.99</td><td>83.43</td><td>83.73</td><td>82.03</td><td>83.87</td><td>84.47</td><td>84.90</td></tr><tr><td>60%</td><td>42.19</td><td>41.75</td><td>62.34</td><td>62.52</td><td>54.65</td><td>57.11</td><td>56.10</td><td>57.27</td><td>66.87</td><td>68.28</td><td>35.55</td><td>40.02</td><td>75.36</td><td>76.30</td></tr></table>

Table 7: Comparison with Label Noise Learning Baselines on Class-dependent Noise Scenarios. 

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Noise</td><td colspan="2">CE</td><td colspan="2">LSR</td><td colspan="2">Mixup</td><td colspan="2">GCE</td><td colspan="2">SCE</td><td colspan="2">Co-teaching</td><td colspan="2">DividMix</td><td colspan="2">Ours</td></tr><tr><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td><td>Acc</td><td>F1</td></tr><tr><td rowspan="5">ISCXVPN</td><td>5%</td><td>78.91</td><td>79.06</td><td>79.61</td><td>79.66</td><td>82.95</td><td>82.74</td><td>76.09</td><td>74.58</td><td>79.09</td><td>79.06</td><td>85.41</td><td>84.44</td><td>85.24</td><td>85.37</td><td>93.32</td><td>92.98</td></tr><tr><td>10%</td><td>76.09</td><td>75.31</td><td>77.85</td><td>77.34</td><td>78.91</td><td>78.76</td><td>75.04</td><td>73.88</td><td>77.50</td><td>76.47</td><td>86.46</td><td>85.74</td><td>80.84</td><td>81.37</td><td>92.62</td><td>92.28</td></tr><tr><td>20%</td><td>76.44</td><td>76.12</td><td>74.34</td><td>74.02</td><td>76.80</td><td>76.67</td><td>72.93</td><td>71.89</td><td>74.34</td><td>74.77</td><td>87.69</td><td>87.37</td><td>79.61</td><td>80.15</td><td>89.45</td><td>88.90</td></tr><tr><td>40%</td><td>58.52</td><td>59.16</td><td>59.75</td><td>59.91</td><td>67.48</td><td>67.39</td><td>68.18</td><td>67.23</td><td>64.49</td><td>64.37</td><td>75.57</td><td>75.50</td><td>76.63</td><td>77.00</td><td>78.03</td><td>77.29</td></tr><tr><td>60%</td><td>38.84</td><td>40.05</td><td>34.62</td><td>36.01</td><td>43.76</td><td>45.73</td><td>42.88</td><td>42.03</td><td>41.82</td><td>44.02</td><td>51.85</td><td>50.94</td><td>50.44</td><td>53.44</td><td>53.25</td><td>53.62</td></tr><tr><td rowspan="5">USTC-TFC</td><td>5%</td><td>87.16</td><td>86.73</td><td>86.33</td><td>85.67</td><td>90.68</td><td>90.45</td><td>80.12</td><td>78.79</td><td>86.75</td><td>86.45</td><td>76.81</td><td>73.84</td><td>85.92</td><td>85.72</td><td>94.62</td><td>94.50</td></tr><tr><td>10%</td><td>85.92</td><td>86.06</td><td>83.85</td><td>83.31</td><td>89.23</td><td>88.51</td><td>79.50</td><td>78.66</td><td>85.92</td><td>85.86</td><td>77.64</td><td>74.63</td><td>90.48</td><td>90.41</td><td>94.20</td><td>94.16</td></tr><tr><td>20%</td><td>81.78</td><td>81.27</td><td>82.81</td><td>82.27</td><td>83.22</td><td>82.49</td><td>78.67</td><td>76.84</td><td>80.12</td><td>79.90</td><td>83.44</td><td>80.90</td><td>89.23</td><td>88.98</td><td>92.13</td><td>92.15</td></tr><tr><td>40%</td><td>65.21</td><td>65.18</td><td>66.04</td><td>66.20</td><td>74.12</td><td>74.41</td><td>71.42</td><td>70.16</td><td>71.22</td><td>70.62</td><td>82.40</td><td>81.75</td><td>81.78</td><td>82.25</td><td>84.47</td><td>84.90</td></tr><tr><td>60%</td><td>58.17</td><td>58.86</td><td>51.55</td><td>51.65</td><td>55.69</td><td>56.93</td><td>64.80</td><td>65.05</td><td>48.44</td><td>49.47</td><td>68.12</td><td>69.73</td><td>65.22</td><td>66.35</td><td>75.36</td><td>76.30</td></tr></table>

# H Class-dependent Noise Evaluation

Class-dependent noise occurs when the probability of label corruption is not uniform across classes, meaning certain classes are more prone to having mislabeled samples than others.

For instance, in VPN traffic categories, VOIP and Streaming are often mislabeled due to their similar real-time transmission metrics, such as packet sizes and intervals, once encrypted. FTP and MAIL, which exhibit prolonged, high-volume traffic traits during large file transfers, are frequently miscategorized as p2p. Likewise, BROWSING and CHAT, with their frequent interactions and small packet sizes, become indistinguishable when encrypted, leading to frequent mislabeling. Thus we injected class-dependent noise into the ISCXVPN dataset to mirror these common mislabeling scenarios.

On the other hand, in the USTC-TFC malware traffic dataset, FTP and SMB often get confused due to their similar file transfer behaviors. Both protocols involve significant data packet exchanges which can appear alike under traffic analysis. Similarly, Gmail and Outlook, both being email services, often exhibit interchangeable traffic patterns due to similar data flow structures, leading to potential mislabeling. Services like Skype and Facetime, which both facilitate VoIP communications, show closely related network signatures that can easily be mistaken for one another when encrypted. Additionally, applications like WorldOfWarcraft and Skype may be misclassified due to their real-time interaction requirements, which create similar traffic spikes. BitTorrent, known for peer-to-peer file sharing, and FTP, used for direct file transfers, also share large file movement characteristics that can be confused under automated analysis. Furthermore, malware such as Zeus and Cridex, or Nsis-ay and Virut, exhibit overlapping behaviors in terms of their network communication patterns, making accurate classification challenging. Thus, we injected these class-dependent noises into the USTC-TFC dataset to closely simulate these realistic mislabeling scenarios.

We comprehensively performed a comparison with both traffic classification methods and label noise methods under class-dependent noise, which are shown in Table 6 and Table 7. Results show that our method can achieve significant performance advantages over the baselines in the class-dependent noise scenario.

# NeurIPS Paper Checklist

# 1. Claims

Question: Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope?

Answer: [Yes]

Justification: In the abstract and introduction, we stated that this work proposes a robust and general traffic classification framework against label noise.

Guidelines:

• The answer NA means that the abstract and introduction do not include the claims made in the paper.   
• The abstract and/or introduction should clearly state the claims made, including the contributions made in the paper and important assumptions and limitations. A No or NA answer to this question will not be perceived well by the reviewers.   
• The claims made should match theoretical and experimental results, and reflect how much the results can be expected to generalize to other settings.   
• It is fine to include aspirational goals as motivation as long as it is clear that these goals are not attained by the paper.

# 2. Limitations

Question: Does the paper discuss the limitations of the work performed by the authors?

Answer: [Yes]

Justification: This paper discusses the limitations in Section 4.5.

Guidelines:

• The answer NA means that the paper has no limitation while the answer No means that the paper has limitations, but those are not discussed in the paper.   
• The authors are encouraged to create a separate "Limitations" section in their paper.   
• The paper should point out any strong assumptions and how robust the results are to violations of these assumptions (e.g., independence assumptions, noiseless settings, model well-specification, asymptotic approximations only holding locally). The authors should reflect on how these assumptions might be violated in practice and what the implications would be.   
• The authors should reflect on the scope of the claims made, e.g., if the approach was only tested on a few datasets or with a few runs. In general, empirical results often depend on implicit assumptions, which should be articulated.   
• The authors should reflect on the factors that influence the performance of the approach. For example, a facial recognition algorithm may perform poorly when image resolution is low or images are taken in low lighting. Or a speech-to-text system might not be used reliably to provide closed captions for online lectures because it fails to handle technical jargon.   
• The authors should discuss the computational efficiency of the proposed algorithms and how they scale with dataset size.   
• If applicable, the authors should discuss possible limitations of their approach to address problems of privacy and fairness.   
• While the authors might fear that complete honesty about limitations might be used by reviewers as grounds for rejection, a worse outcome might be that reviewers discover limitations that aren’t acknowledged in the paper. The authors should use their best judgment and recognize that individual actions in favor of transparency play an important role in developing norms that preserve the integrity of the community. Reviewers will be specifically instructed to not penalize honesty concerning limitations.

# 3. Theory assumptions and proofs

Question: For each theoretical result, does the paper provide the full set of assumptions and a complete (and correct) proof?

Answer: [NA]

Justification: We do not provide the theoretical result in the paper.

# Guidelines:

• The answer NA means that the paper does not include theoretical results.   
• All the theorems, formulas, and proofs in the paper should be numbered and crossreferenced.   
• All assumptions should be clearly stated or referenced in the statement of any theorems.   
• The proofs can either appear in the main paper or the supplemental material, but if they appear in the supplemental material, the authors are encouraged to provide a short proof sketch to provide intuition.   
• Inversely, any informal proof provided in the core of the paper should be complemented by formal proofs provided in appendix or supplemental material.   
• Theorems and Lemmas that the proof relies upon should be properly referenced.

# 4. Experimental result reproducibility

Question: Does the paper fully disclose all the information needed to reproduce the main experimental results of the paper to the extent that it affects the main claims and/or conclusions of the paper (regardless of whether the code and data are provided or not)?

Answer: [Yes]

Justification: We provide the details of the proposed method and experimental setting.

Besides, the source code and the experiment data will be released upon publication.

# Guidelines:

• The answer NA means that the paper does not include experiments.   
• If the paper includes experiments, a No answer to this question will not be perceived well by the reviewers: Making the paper reproducible is important, regardless of whether the code and data are provided or not.   
• If the contribution is a dataset and/or model, the authors should describe the steps taken to make their results reproducible or verifiable.   
• Depending on the contribution, reproducibility can be accomplished in various ways. For example, if the contribution is a novel architecture, describing the architecture fully might suffice, or if the contribution is a specific model and empirical evaluation, it may be necessary to either make it possible for others to replicate the model with the same dataset, or provide access to the model. In general. releasing code and data is often one good way to accomplish this, but reproducibility can also be provided via detailed instructions for how to replicate the results, access to a hosted model (e.g., in the case of a large language model), releasing of a model checkpoint, or other means that are appropriate to the research performed.   
• While NeurIPS does not require releasing code, the conference does require all submissions to provide some reasonable avenue for reproducibility, which may depend on the nature of the contribution. For example   
(a) If the contribution is primarily a new algorithm, the paper should make it clear how to reproduce that algorithm.   
(b) If the contribution is primarily a new model architecture, the paper should describe the architecture clearly and fully.   
(c) If the contribution is a new model (e.g., a large language model), then there should either be a way to access this model for reproducing the results or a way to reproduce the model (e.g., with an open-source dataset or instructions for how to construct the dataset).   
(d) We recognize that reproducibility may be tricky in some cases, in which case authors are welcome to describe the particular way they provide for reproducibility. In the case of closed-source models, it may be that access to the model is limited in some way (e.g., to registered users), but it should be possible for other researchers to have some path to reproducing or verifying the results.

# 5. Open access to data and code

Question: Does the paper provide open access to the data and code, with sufficient instructions to faithfully reproduce the main experimental results, as described in supplemental material?

# Answer: [Yes]

Justification: Datasets used in this paper are publicly available. The code will be opensourced upon publication.

# Guidelines:

• The answer NA means that paper does not include experiments requiring code.   
• Please see the NeurIPS code and data submission guidelines (https://nips.cc/ public/guides/CodeSubmissionPolicy) for more details.   
• While we encourage the release of code and data, we understand that this might not be possible, so “No” is an acceptable answer. Papers cannot be rejected simply for not including code, unless this is central to the contribution (e.g., for a new open-source benchmark).   
• The instructions should contain the exact command and environment needed to run to reproduce the results. See the NeurIPS code and data submission guidelines (https: //nips.cc/public/guides/CodeSubmissionPolicy) for more details.   
• The authors should provide instructions on data access and preparation, including how to access the raw data, preprocessed data, intermediate data, and generated data, etc.   
• The authors should provide scripts to reproduce all experimental results for the new proposed method and baselines. If only a subset of experiments are reproducible, they should state which ones are omitted from the script and why.   
• At submission time, to preserve anonymity, the authors should release anonymized versions (if applicable).   
• Providing as much information as possible in supplemental material (appended to the paper) is recommended, but including URLs to data and code is permitted.

# 6. Experimental setting/details

Question: Does the paper specify all the training and test details (e.g., data splits, hyperparameters, how they were chosen, type of optimizer, etc.) necessary to understand the results?

# Answer: [Yes]

Justification: We give the training and test details in the Experiment section and the Appendix.

# Guidelines:

• The answer NA means that the paper does not include experiments.   
• The experimental setting should be presented in the core of the paper to a level of detail that is necessary to appreciate the results and make sense of them.   
• The full details can be provided either with the code, in appendix, or as supplemental material.

# 7. Experiment statistical significance

Question: Does the paper report error bars suitably and correctly defined or other appropriate information about the statistical significance of the experiments?

# Answer: [No]

Justification: The paper presents the results from a single run for each experiment, which is consistent with previous works on traffic classification.

# Guidelines:

• The answer NA means that the paper does not include experiments.   
• The authors should answer "Yes" if the results are accompanied by error bars, confidence intervals, or statistical significance tests, at least for the experiments that support the main claims of the paper.   
• The factors of variability that the error bars are capturing should be clearly stated (for example, train/test split, initialization, random drawing of some parameter, or overall run with given experimental conditions).   
• The method for calculating the error bars should be explained (closed form formula, call to a library function, bootstrap, etc.)

• The assumptions made should be given (e.g., Normally distributed errors).   
• It should be clear whether the error bar is the standard deviation or the standard error of the mean.   
• It is OK to report 1-sigma error bars, but one should state it. The authors should preferably report a 2-sigma error bar than state that they have a 96% CI, if the hypothesis of Normality of errors is not verified.   
• For asymmetric distributions, the authors should be careful not to show in tables or figures symmetric error bars that would yield results that are out of range (e.g. negative error rates).   
• If error bars are reported in tables or plots, The authors should explain in the text how they were calculated and reference the corresponding figures or tables in the text.

# 8. Experiments compute resources

Question: For each experiment, does the paper provide sufficient information on the computer resources (type of compute workers, memory, time of execution) needed to reproduce the experiments?

Answer: [Yes]

Justification: This work provides the computer resources needed to reproduce the experiment in Section 4.1.

Guidelines:

• The answer NA means that the paper does not include experiments.   
• The paper should indicate the type of compute workers CPU or GPU, internal cluster, or cloud provider, including relevant memory and storage.   
• The paper should provide the amount of compute required for each of the individual experimental runs as well as estimate the total compute.   
• The paper should disclose whether the full research project required more compute than the experiments reported in the paper (e.g., preliminary or failed experiments that didn’t make it into the paper).

# 9. Code of ethics

Question: Does the research conducted in the paper conform, in every respect, with the NeurIPS Code of Ethics https://neurips.cc/public/EthicsGuidelines?

Answer: [Yes]

Justification: The research conducted in the paper adheres to the NeurIPS Code of Ethics, ensuring that all aspects of the work, including the methodology, data handling, and reporting, conform to the ethical guidelines provided.

Guidelines:

• The answer NA means that the authors have not reviewed the NeurIPS Code of Ethics.   
• If the authors answer No, they should explain the special circumstances that require a deviation from the Code of Ethics.   
• The authors should make sure to preserve anonymity (e.g., if there is a special consideration due to laws or regulations in their jurisdiction).

# 10. Broader impacts

Question: Does the paper discuss both potential positive societal impacts and negative societal impacts of the work performed?

Answer: [Yes]

Justification: This work introduces the importance of traffic analysis techniques to protect network security and improve the quality of service in Section 1. Furthermore, traffic analysis techniques have minimal negative social impact.

Guidelines:

• The answer NA means that there is no societal impact of the work performed.   
• If the authors answer NA or No, they should explain why their work has no societal impact or why the paper does not address societal impact.

• Examples of negative societal impacts include potential malicious or unintended uses (e.g., disinformation, generating fake profiles, surveillance), fairness considerations (e.g., deployment of technologies that could make decisions that unfairly impact specific groups), privacy considerations, and security considerations.   
• The conference expects that many papers will be foundational research and not tied to particular applications, let alone deployments. However, if there is a direct path to any negative applications, the authors should point it out. For example, it is legitimate to point out that an improvement in the quality of generative models could be used to generate deepfakes for disinformation. On the other hand, it is not needed to point out that a generic algorithm for optimizing neural networks could enable people to train models that generate Deepfakes faster.   
• The authors should consider possible harms that could arise when the technology is being used as intended and functioning correctly, harms that could arise when the technology is being used as intended but gives incorrect results, and harms following from (intentional or unintentional) misuse of the technology.   
• If there are negative societal impacts, the authors could also discuss possible mitigation strategies (e.g., gated release of models, providing defenses in addition to attacks, mechanisms for monitoring misuse, mechanisms to monitor how a system learns from feedback over time, improving the efficiency and accessibility of ML).

# 11. Safeguards

Question: Does the paper describe safeguards that have been put in place for responsible release of data or models that have a high risk for misuse (e.g., pretrained language models, image generators, or scraped datasets)?

Answer: [NA]

Justification: The paper poses no such risks.

# Guidelines:

• The answer NA means that the paper poses no such risks.   
• Released models that have a high risk for misuse or dual-use should be released with necessary safeguards to allow for controlled use of the model, for example by requiring that users adhere to usage guidelines or restrictions to access the model or implementing safety filters.   
• Datasets that have been scraped from the Internet could pose safety risks. The authors should describe how they avoided releasing unsafe images.   
• We recognize that providing effective safeguards is challenging, and many papers do not require this, but we encourage authors to take this into account and make a best faith effort.

# 12. Licenses for existing assets

Question: Are the creators or original owners of assets (e.g., code, data, models), used in the paper, properly credited and are the license and terms of use explicitly mentioned and properly respected?

Answer: [Yes]

Justification: This paper clearly introduces existing assets and complies with terms of use in Section 4.1.

# Guidelines:

• The answer NA means that the paper does not use existing assets.   
• The authors should cite the original paper that produced the code package or dataset.   
• The authors should state which version of the asset is used and, if possible, include a URL.   
• The name of the license (e.g., CC-BY 4.0) should be included for each asset.   
• For scraped data from a particular source (e.g., website), the copyright and terms of service of that source should be provided.

• If assets are released, the license, copyright information, and terms of use in the package should be provided. For popular datasets, paperswithcode.com/datasets has curated licenses for some datasets. Their licensing guide can help determine the license of a dataset.   
• For existing datasets that are re-packaged, both the original license and the license of the derived asset (if it has changed) should be provided.   
• If this information is not available online, the authors are encouraged to reach out to the asset’s creators.

# 13. New assets

Question: Are new assets introduced in the paper well documented and is the documentation provided alongside the assets?

Answer: [NA]

Justification: The paper does not introduce any new assets.

Guidelines:

• The answer NA means that the paper does not release new assets.   
• Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates. This includes details about training, license, limitations, etc.   
• The paper should discuss whether and how consent was obtained from people whose asset is used.   
• At submission time, remember to anonymize your assets (if applicable). You can either create an anonymized URL or include an anonymized zip file.

# 14. Crowdsourcing and research with human subjects

Question: For crowdsourcing experiments and research with human subjects, does the paper include the full text of instructions given to participants and screenshots, if applicable, as well as details about compensation (if any)?

Answer: [NA]

Justification: The paper does not involve crowdsourcing or human subjects research.

Guidelines:

• The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.   
• Including this information in the supplemental material is fine, but if the main contribution of the paper involves human subjects, then as much detail as possible should be included in the main paper.   
• According to the NeurIPS Code of Ethics, workers involved in data collection, curation, or other labor should be paid at least the minimum wage in the country of the data collector.

# 15. Institutional review board (IRB) approvals or equivalent for research with human subjects

Question: Does the paper describe potential risks incurred by study participants, whether such risks were disclosed to the subjects, and whether Institutional Review Board (IRB) approvals (or an equivalent approval/review based on the requirements of your country or institution) were obtained?

Answer: [NA]

Justification: The paper does not involve crowdsourcing or human subjects research.

Guidelines:

• The answer NA means that the paper does not involve crowdsourcing nor research with human subjects.   
• Depending on the country in which research is conducted, IRB approval (or equivalent) may be required for any human subjects research. If you obtained IRB approval, you should clearly state this in the paper.

• We recognize that the procedures for this may vary significantly between institutions and locations, and we expect authors to adhere to the NeurIPS Code of Ethics and the guidelines for their institution.   
• For initial submissions, do not include any information that would break anonymity (if applicable), such as the institution conducting the review.

# 16. Declaration of LLM usage

Question: Does the paper describe the usage of LLMs if it is an important, original, or non-standard component of the core methods in this research? Note that if the LLM is used only for writing, editing, or formatting purposes and does not impact the core methodology, scientific rigorousness, or originality of the research, declaration is not required.

Answer: [NA]

Justification: The core method development in this research does not involve LLMs as any important, original, or non-standard components.

Guidelines:

• The answer NA means that the core method development in this research does not involve LLMs as any important, original, or non-standard components.   
• Please refer to our LLM policy (https://neurips.cc/Conferences/2025/LLM) for what should or should not be described.
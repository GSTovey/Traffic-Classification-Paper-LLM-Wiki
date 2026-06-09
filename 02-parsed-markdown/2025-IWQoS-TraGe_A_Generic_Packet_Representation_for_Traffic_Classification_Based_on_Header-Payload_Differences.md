# TraGe: A Generic Packet Representation for Traffic Classification Based on Header-Payload Differences

Chungang Lin†‡∥, Yilong Jiang†‡∥, Weiyao Zhang†, Xuying Meng†§∗, Tianyu Zuo‡, Yujun Zhang†‡¶∗

†Institute of Computing Technology, Chinese Academy of Sciences, China.

‡University of Chinese Academy of Sciences, China.

§Purple Mountain Laboratories, China.

¶Nanjing Institute of InforSuperBahn, China.

{linchungang22s, jiangyilong23s, zhangweiyao17z, mengxuying, zuotianyu22s, nrcyujun}@ict.ac.cn

Abstract—Traffic classification has a significant impact on maintaining the Quality of Service (QoS) of the network. Since traditional methods heavily rely on feature extraction and largescale labeled data, some recent pre-trained models manage to reduce the dependency by utilizing different pre-training tasks to train generic representations for network packets. However, existing pre-trained models typically adopt pre-training tasks developed for image or text data, which are not tailored to traffic data. As a result, the obtained traffic representations fail to fully reflect the information contained in the traffic, and may even disrupt the protocol information. To address this, we propose TraGe, a novel generic packet representation model for traffic classification. Based on the differences between the header and payload—the two fundamental components of a network packetwe perform differentiated pre-training according to the byte sequence variations (continuous in the header vs. discontinuous in the payload). A dynamic masking strategy is further introduced to prevent overfitting to fixed byte positions. Once the generic packet representation is obtained, TraGe can be finetuned for diverse traffic classification tasks using limited labeled data. Experimental results demonstrate that TraGe significantly outperforms state-of-the-art methods on two traffic classification tasks, with up to a 6.97% performance improvement. Moreover, TraGe exhibits superior robustness under parameter fluctuations and variations in sampling configurations.

Index Terms—traffic classification, pre-training technology, generic packet representation, header-payload differences.

## I. INTRODUCTION

Traffic classification aims to organize network traffic into different categories (e.g., application and service), which is a fundamental and vital technology in network management and Quality of Service (QoS) [1]–[6]. For instance, in an enterprise network, traffic may include email, voice calls, and file transfers. By effectively classifying these traffic categories, network administrators can implement QoS policies to ensure critical traffic like voice calls receive sufficient bandwidth, low latency, and prioritized network resources [7], [8].

Traditional statistical feature-based methods [9]–[12], such as FlowPrint [9] and AppScanner [10], rely on manual traffic feature extraction, where the extracted features are then fed into machine learning models. In contrast, deep learning-based

∥ Both authors contributed equally to this research.  
∗ Corresponding author.

979-8-3315-4940-4/25/\$31.00 © 2025 IEEE methods [13]–[15] automate the learning of traffic features through deep learning models, reducing the need for manual feature extraction. However, deep learning models depend heavily on large-scale labeled data. To address this, some recent pre-trained models [5], [6], [16], [17] leverage largescale unlabeled raw byte sequences from packets, rather than extracted statistical features, to learn generic representations, requiring only small-scale labeled data for fine-tuning and thereby reducing the reliance on both feature extraction and large-scale labels.

However, existing pre-trained models mainly apply pretraining tasks originating from other domains, such as computer vision (CV) and natural language processing (NLP). These pre-trained tasks are tailored to domain-specific data formats—image data in CV and text data in NLP—which differ significantly from the traffic data in the network domain, making them less effective in learning a generic representation for network traffic. A network packet comprises two fundamentally components: the header and the payload. In contrast to image or text data, which are typically modeled as uniform data, the header and payload exhibit significant structural differences. Specifically, unlike the payload, the header contains structured protocol fields with continuous byte sequences that are essential for recognizing traffic patterns. For instance, the TCP sequence number can reveal program behavior and support anomaly detection [18]. Yet, existing pretrained models overlook the header byte continuity by either classifying traffic based solely on the payload (e.g., PERT [16], ET-BERT [5]) or by treating the header and payload uniformly, thus disrupting this continuity (e.g., NetGPT [17], YaTC [6]).

To address the above limitations, in this paper, we propose TraGe, a novel pre-trained model for traffic classification with a generic packet representation. This representation is derived by fully considering the header-payload differences of network packets. Specifically, TraGe performs differentiated pre-training based on the byte sequence variations (continuous vs. discontinuous) between the header and payload, with a dynamic masking strategy applied to avoid overfitting to fixed byte positions. Together, these components enable TraGe to obtain a generic packet representation, which can then be fine-tuned for various traffic classification tasks with limited labeled data. Extensive experiments conducted on publicly available datasets demonstrate the effectiveness and the robustness of TraGe. The comparison results show that TraGe outperforms state-of-the-art pre-trained models, achieving up to a 6.97% improvement in classification performance. In addition, analyses of parameter sensitivity and sampling variability demonstrate TraGe’s robustness to both parameter fluctuations and variations in sampling configurations.

The main contributions of this paper are as follows:

• We propose TraGe, a novel pre-trained model with a generic packet representation for traffic classification based on header-payload differences.  
• We design two pre-training tasks (i.e., MLM-FM and MLM-RM) for the header and payload of network packets to obtain generic packet representations.  
• We conduct extensive experiments on two traffic classification tasks to evaluate the effectiveness and the robustness of TraGe.

## II. RELATED WORK

According to the utilized features, model structure, and pretraining technology, related works can be divided into methods based on statistical features, deep learning, and pre-training technology.

## A. Methods based on Statistics Features

Statistical feature-based methods rely on manually extracting traffic features for model training. For example, FlowPrint [19] uses packet inter-arrival times and applies clustering with cross-correlation for classification. AppScanner [10] trains a random forest classifier using packet size statistics, while DTree [11] incorporates size and timing features in a decision tree model. Although these methods demonstrate reasonable effectiveness, their reliance on handcrafted features restricts the model’s ability to learn comprehensive network patterns.

## B. Methods based on Deep Learning

Deep learning-based methods automate feature extraction by directly processing raw traffic data through neural networks, eliminating the need for handcrafted features. For example, FS-Net [13] uses recurrent neural networks (RNNs) to learn representations from raw packet length sequences. EBSNN [14] also leverages RNNs but instead operates on raw byte sequences, with two variants: EBSNN-L (based on LSTM) and EBSNN-G (based on GRU). TFE-GNN [15] further explores this direction by modeling byte sequences as graphs and applying graph neural networks (GNNs) for classification. Despite their effectiveness, these methods typically demand large amounts of labeled data, which is often impractical in real-world deployment scenarios [5], [16], [20].

## C. Methods based on Pre-training Technology

Pre-trained models leverage self-supervised learning on large-scale unlabeled traffic to learn generalizable representations, which are then fine-tuned using a smaller set of task-specific labeled data. This strategy reduces reliance on extensive annotations by enabling effective classification with limited labeled samples. For example, ET-BERT [5] treats payload byte sequences as word-like inputs and applies two NLP-inspired pre-training tasks: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP). Likewise, YaTC [6] models packet byte sequences—including headers and payloads—as images and uses Masked Image Modeling (MIM), a task from the computer vision domain, to capture inter-traffic relationships. However, current pre-trained models predominantly adopt pre-training tasks from CV and NLP, which are designed for structured image or text data. These data types differ significantly from network traffic, limiting the effectiveness of such tasks in capturing traffic-specific representations.

## III. METHODOLOGY

We propose TraGe to fully exploit the traffic characteristics for learning general packet representations, thereby improving model performance in different network traffic classification tasks. Specifically, TraGe leverages the explicit byte distribution differences between the header and the payload to perform header-payload differentiated pre-training (Section III-A). This approach enables the model to obtain a generic packet representation, which facilitates effective model finetuning (Section III-B) across diverse traffic classification tasks. The overall framework of TraGe is shown in Fig. 1.

## A. Header-Payload Differentiated Pre-training

The header and payload of a packet both consist of byte sequences, but the same byte sequence can represent different meanings. For instance, as shown in Fig. 1, the byte sequence “b11eac20”1 denotes a sequence number in the header, indicating the position of the packet within a TCP flow. In contrast, in the payload, “b11eac20” could represent a specific data value or instruction, depending on the context of the application and protocol. If identical byte sequences in the header and payload are processed uniformly without considering their distinct meanings, the model may struggle to correctly extract relevant information, which can hinder its learning performance.

Given the differences between the header and payload, we propose header-payload differentiated pre-training based on the byte distribution (continuous vs. discontinuous), as shown in Fig. 1. This approach introduces two pre-training tasks—MLM-FM for the header and MLM-RM for the payload—which together form the foundation of the final generic packet representation. To further enhance pre-training effectiveness, we incorporate a Dynamic Masking (DM) strategy to mitigate model overfitting.

a) Pre-training Task for Header: The network packet header comprises protocol header fields, with each field consisting of continuous byte sequences. Existing pre-training models primarily employ Masked Language Modeling (MLM) pre-training task [5], [16], where random byte sequences are masked during model pre-training. The model then learns to predict these masked bytes, thereby forming a generic packet representation. However, the random masking approach disrupts the continuity of the header fields. For example, a byte sequence like “b11eac20” may represent specific network information, such as a sequence number. Random masking could mask only part of the sequence (e.g., just the byte $\mathbf { \vec { \tau } } ^ { 6 1 } \vec { \mathbf { \tau } } )$ , preventing the model from fully capturing the intended network context. As a result, the model’s ability to learn a generic packet representation is compromised.

![](images/4d299cf6859e07bcfb0c4a4157a73cf0ee8265702aa19da48a529453aae0b0f9.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    subgraph PreTrainingPhase[① Pre-training Phase]
  A1["b1le"] --> B1["ac20"]
  B1 --> C1["TCP Header Field Sequence Number"]
  C1 --> D1["Transformer Encoder"]
  D1 --> E1["8afd"]
  D1 --> F1["Mask"]
  D1 --> G1["Mask"]
  D1 --> H1["edce"]
  D1 --> I1["..."]
  D1 --> J1["7346"]
  D1 --> K1["Mask"]
  D1 --> L1["6420"]
  D1 --> M1["Mask"]
  M1 --> N1["Random Masking"]
  N1 --> O1["8afd"]
  N1 --> P1["b1le"]
  N1 --> Q1["ac20"]
  N1 --> R1["edce"]
  N1 --> S1["..."]
  N1 --> T1["7346"]
  N1 --> U1["5450"]
  N1 --> V1["6420"]
  N1 --> W1["3229"]
    end

    subgraph FineTuningPhase[② Fine-tuning Phase]
  X["Service Identification"] --> Y["Transformer Encoder"]
  Y --> Z["..."]
  AA["Application Classification"] --> AB["Transformer Encoder"]
    end

  B1 --> X
  F1 --> Y
  G1 --> AB
  H1 --> AB
  I1 --> AB
  J1 --> AB
  K1 --> AB
  L1 --> AB
  M1 --> AB
  N1 --> AB
  O1 --> AB
  P1 --> AB
  Q1 --> AB
  R1 --> AB
  S1 --> AB
  T1 --> AB
  U1 --> AB
  V1 --> AB
  W1 --> AB
```
</details>

Fig. 1. The framework of TraGe.

![](images/26dee1f2a50e422fa8e55a479cb12b8c203ce149984298d5d485a60cfbd4731d.jpg)

<details>
<summary>bar chart</summary>

| Header Field Length | Probability |
| ------------------- | ----------- |
| 1                   | 0.7         |
| 2                   | 0.15        |
| 3                   | 0.1         |
| 4                   | 0.0         |
| 5                   | 0.0         |
| 6                   | 0.0         |
| 7                   | 0.0         |
| 8                   | 0.0         |
| 9                   | 0.0         |
| 10                  | 0.0         |
</details>

(a) Real-world Distribution

![](images/a45772a3fa6a0dec9f2e2510b94a6fd1cadc0020b123c5418a36bc78ac7426ae.jpg)

<details>
<summary>bar chart</summary>

| I ~ Geo(p) | Probability |
| ---------- | ----------- |
| 1          | 0.7         |
| 2          | 0.2         |
| 3          | 0.08        |
| 4          | 0.03        |
| 5          | 0.01        |
| 6          | 0.01        |
| 7          | 0.01        |
| 8          | 0.01        |
| 9          | 0.01        |
| 10         | 0.01        |
</details>

(b) Geometric Distribution  
Fig. 2. A case study on header field length distribution on the ISCX-VPN dataset and geometric distribution.

Therefore, we introduce field-level masking to continuously mask byte sequences, thereby improving the model’s ability to learn generic packet representations. A feasible approach to implementing field-level masking is to parse each packet’s header in advance to identify the location of each protocol header field, followed by masking the relevant fields. However, parsing packets can be computationally expensive, and not all protocol headers are easily parsed. To address this, we propose an alternative approach using a geometric distribution. Specifically, we sample the length of the masked byte sequence based on a geometric distribution, drawing inspiration from the observed similarity between the length distribution of header fields and a geometric distribution. As shown in Fig. 2, the distribution of header protocol field lengths in the ISCX-VPN [21] dataset closely aligns with the geometric distribution $\ell \sim \operatorname { G e o } ( p )$ . This similarity supports the feasibility of using a geometric distribution for field-level masking.2

During the pre-training of the transformer encoder for the packet header, we first sample a length l using a geometric distribution $\ell \sim \operatorname { G e o } ( p )$ . Next, we continuously select l tokens from the input sequence, with each token consisting of two consecutive bytes, following the approach in ET-BERT [5]. As shown in Fig. 1, for packet #k, these tokens are masked with the special token [MASK], and the transformer encoder is trained by predicting the masked tokens based on the context. The loss function is based on negative log-likelihood, formally defined as:

$$
L _ {M L M - F M} = - \sum_ {i = 1} ^ {l} \log \left(P \left(M A S K _ {i} = t o k e n _ {i} \mid \theta_ {H}\right)\right) \tag {1}
$$

where $\theta _ { H }$ represents the model parameters of the encoder. We pre-train the transformer encoder through Masked Language Modeling (MLM) based on Field-level Masking (FM).

b) Pre-training Task for Payload: Unlike the header, the payload lacks explicit continuity between its bytes. This is primarily due to the nature of the payload, which often carries application-layer data or encrypted content. During transmission, this data is typically fragmented, rearranged, or encrypted, causing the byte order to lose its direct connection to the original data structure. Furthermore, encryption disrupts the continuity between bytes, increasing processing complexity. Therefore, we directly use Masked Language Modeling based on Random Masking (MLM-RM). Compared with fieldlevel masking, random masking randomly selects r tokens in the input token sequence. The loss function is defined as:

$$
L _ {M L M - R M} = - \sum_ {i = 1} ^ {r} \log \left(P \left(M A S K _ {i} = t o k e n _ {i} \mid \theta_ {P}\right)\right) \tag {2}
$$

where $\theta _ { P }$ represents the set of parameters of the transformer encoder. RM means Random Masking.

c) Dynamic Masking for Model Pretraining: Traditional pre-training models typically adopt static masking, where a fixed subset of tokens is selected for prediction during the data preprocessing stage [5], [16]. These masked positions remain unchanged throughout model pre-training, leading the model to repeatedly encounter the same masking pattern. This approach restricts the model’s exposure to diverse traffic information and encourages memorization of specific positions rather than learning generic traffic representations, ultimately limiting generalization. To address this limitation, we adopt a dynamic masking strategy that generates masked positions dynamically during model pre-training. This approach allows the model to observe varied byte combinations across training iterations, thereby improving the generalization and robustness of the learned traffic representations.

## B. Model Fine-tuning

The objective of model fine-tuning is to classify a given network flow into a specific traffic category. Based on the obtained generic packet representation, we can perform different traffic classification tasks. We utilize multiple linear layers and the softmax function to predict the probabilities of the network flow belonging to different traffic categories. Note that there is no need to design separate models for each traffic classification task. This is because traffic characteristics can be fully exploited through header-payload differentiated pretraining to generate a generic packet representation, which then supports various traffic classification tasks.

## IV. EVALUATION

In this section, we first introduce the selected datasets, baselines, and the detailed implementation of TraGe. Subsequently, we evaluate TraGe on two traffic classification tasks. Our evaluation aims to answer four research questions:

RQ1. Can TraGe outperform state-of-the-art (SoTA) traffic classification models?

RQ2. What contribution does each TraGe component make?

RQ3. How do parameter changes affect TraGe’s classification performance?

RQ4. How does data sampling variability affect the performance stability of TraGe?

## A. Experiment Setup

a) Datasets: We select three datasets from diverse sources for pre-training and fine-tuning, including ISCX-VPN [21], USTC-TFC [22], and CIC-IoT [23]. The ISCX-VPN dataset captures traffic from various behaviors across multiple applications and services within VPN environments, such as browsing, email, audio, video, and file transfer. The USTC-TFC dataset contains 10 categories of benign traffic and 10 categories of malicious traffic, primarily from smart grid infrastructures. The CIC-IoT dataset is an IoT traffic dataset designed for behavioral analysis and intrusion detection.

We use a portion of these datasets for model pre-training and the remaining data for model fine-tuning. Two traffic classification tasks on the ISCX-VPN dataset are performed, i.e., application classification and service identification. The application classification and service identification tasks focus on encrypted traffic in VPN environments. To evaluate the model’s ability to classify applications and services in detail, we further categorize the ISCX-VPN dataset according to applications and services, i.e., ISCX-VPN (App) and ISCX-VPN (Service), ultimately forming a 17-class application classification task and a 12-class service identification task. Table I presents the specific traffic category distribution for the two traffic classification tasks.

b) Implementation Details and Baselines: We implement TraGe and all baselines by using Python 3.10.14 with libraries including NumPy 1.26.14, PyTorch 2.3.0, and CUDA 12.4. For model pre-training, we use BERT [24] as the transformer encoder. We perform pre-training for 100,000 steps, with a learning rate of 1e-3. During field-level masking, we apply a geometric distribution with parameters p = 0.7. Here, p controls the shape of the distribution. During model finetuning, we set the number of epochs to 10, with a learning rate of 2e-5. In the stage of model fine-tuning, we select a maximum of 5 packets per flow for traffic classification. We randomly select at most 5000 flows from each traffic category for all tasks. Each sampled dataset is then divided into the training set, the validation set, and the testing set according to the ratio of 8 : 1 : 1.

TABLE I THE CATEGORY INFORMATION OF THE FINE-TUNING TASKS.

<table><tr><td>Task</td><td>Traffic Category</td><td>#label</td></tr><tr><td>Application Classification</td><td>ftps, spotify, vimeo, hangout, ICQ, netflix, gmail, AIM, YouTube, voipbuster, sftp email-client, scp, skype, Torrent, Facebook, Tor</td><td>17</td></tr><tr><td>Service Identification</td><td>Chat, VPN-Chat, VPN-P2P, P2P, Voip, VPN-Voip, FT, VPN-FT, Email, VPN-Email, Streaming, VPN-Streaming</td><td>12</td></tr></table>

To ensure a fair comparison, we use three typical metrics, i.e., Precision, Recall, and F1-Score. We select twelve baselines, including (1) four statistics features based models, i.e., FlowPrint [9], AppScanner [10], XGBoost [12], and DTree [11]; (2) four deep learning based models, i.e., FS-Net [13], EBSNN-L [14], EBSNN-G [14], TFE-GNN [15]; and (3) four pre-trained models, i.e., PERT [16], ET-BERT [5], NetGPT [17], and YaTC [6].

## B. Overall Classification Performance (RQ1)

We show the classification performance of TraGe and all baselines on two traffic classification tasks in TABLE II and TABLE III. Bold text indicates the best results, and underlined text indicates the second-best results among all models. It can be seen that TraGe outperforms all baselines with significant margins across both tasks. As shown in Table II, it obtains a Precision of 0.7517, a Recall of 0.7541, and an F1-Score of 0.7484 on the application classification task. Similarly, Table III shows that TraGe achieves a Precision of 0.9333, a Recall of 0.9335, and an F1-Score of 0.9331 on the service identification task. These results surpass the secondbest results (0.7421, 0.7187, 0.7182, 0.9250, 0.9192, and 0.9207) by 1.29%, 4.93%, 4.20%, 0.90%, 1.56%, and 1.35%, respectively. Besides, we observe that the second-best results are all achieved by pre-trained models rather than statistics features-based and deep learning-based models. Further, the results show that TraGe outperforms these four pre-trained models, with average performance improvements of 4.21%, 4.08%, 2.57%, and 6.97% on two tasks. This is because TraGe fully exploits the characteristics of network traffic data to learn a generic packet representation, thereby supporting the best classification results on different traffic classification tasks. In contrast, the baselines fail to fully account for these traffic characteristics, resulting in less generic representations that limit their classification performance.

TABLE II CLASSIFICATION PERFORMANCE COMPARISON OF DIFFERENT METHODS ON APPLICATION CLASSIFICATION TASK.

<table><tr><td>Method</td><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td>FlowPrint [25]</td><td>0.5904</td><td>0.4304</td><td>0.4494</td></tr><tr><td>AppScanner [10]</td><td>0.7289</td><td>0.5361</td><td>0.5803</td></tr><tr><td>XGBoost [12]</td><td>0.5177</td><td>0.4151</td><td>0.4304</td></tr><tr><td>DTree [11]</td><td>0.4844</td><td>0.4483</td><td>0.4462</td></tr><tr><td>FS-Net [13]</td><td>0.4990</td><td>0.3996</td><td>0.4060</td></tr><tr><td>EBSNN-L [14]</td><td>0.7176</td><td>0.6691</td><td>0.6781</td></tr><tr><td>EBSNN-G [14]</td><td>0.7285</td><td>0.6780</td><td>0.6882</td></tr><tr><td>TFE-GNN [15]</td><td>0.6720</td><td>0.6060</td><td>0.6180</td></tr><tr><td>PERT [16]</td><td>0.7218</td><td>0.6971</td><td>0.6955</td></tr><tr><td>ET-BERT [5]</td><td>0.7118</td><td>0.7027</td><td>0.6990</td></tr><tr><td>NetGPT [17]</td><td>0.7336</td><td> $\underline{0.7187}$ </td><td> $\underline{0.7182}$ </td></tr><tr><td>YaTC [6]</td><td> $\underline{0.7421}$ </td><td> $\underline{0.6746}$ </td><td> $\underline{0.6870}$ </td></tr><tr><td>TraGe</td><td> $\underline{0.7517}$ </td><td> $\underline{0.7541}$ </td><td> $\underline{0.7484}$ </td></tr></table>

TABLE III CLASSIFICATION PERFORMANCE COMPARISON OF DIFFERENT METHODS ON SERVICE IDENTIFICATION TASK.

<table><tr><td>Method</td><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td>FlowPrint [25]</td><td>0.7021</td><td>0.6662</td><td>0.6451</td></tr><tr><td>AppScanner [10]</td><td>0.8599</td><td>0.7567</td><td>0.7913</td></tr><tr><td>XGBoost [12]</td><td>0.7094</td><td>0.7160</td><td>0.7032</td></tr><tr><td>DTree [11]</td><td>0.7026</td><td>0.7090</td><td>0.6997</td></tr><tr><td>FS-Net [13]</td><td>0.7161</td><td>0.6363</td><td>0.6418</td></tr><tr><td>EBSNN-L [14]</td><td>0.9000</td><td>0.8672</td><td>0.8771</td></tr><tr><td>EBSNN-G [14]</td><td>0.9013</td><td>0.8784</td><td>0.8845</td></tr><tr><td>TFE-GNN [15]</td><td>0.8597</td><td>0.8095</td><td>0.8214</td></tr><tr><td>PERT [16]</td><td>0.9213</td><td>0.9148</td><td>0.9149</td></tr><tr><td>ET-BERT [5]</td><td>0.9214</td><td>0.9182</td><td>0.9191</td></tr><tr><td>NetGPT [17]</td><td>0.9250</td><td>0.9192</td><td>0.9207</td></tr><tr><td>YaTC [6]</td><td>0.9053</td><td>0.8565</td><td>0.8663</td></tr><tr><td>TraGe</td><td>0.9333</td><td>0.9335</td><td>0.9331</td></tr></table>

## C. Ablation Study (RQ2)

In this subsection, we present the results of an ablation study of TraGe on the application classification and service identification tasks, as shown in TABLE IV. To streamline the presentation, we use the following abbreviations: ‘FM’ for field-level masking, ‘DM’ for dynamic masking. When FM is not applied, random masking is used by default. Similarly, in the absence of DM, static masking is employed.

As shown in TABLE IV, the results for both the application classification and the service identification tasks show that removing either field-level masking or dynamic masking significantly degrades model performance. Specifically, eliminating field-level masking leads to a 5.88% decrease in F1-score for the application classification task, while removing dynamic masking causes a 1.62% reduction. Similar trends are observed in both Precision and Recall. Overall, the results demonstrate that TraGe’s header-payload differentiated pre-training enables the formation of a generic packet representation, which in turn improves model classification performance across different traffic classification tasks.

TABLE IV ABLATION STUDY OF KEY COMPONENTS IN TRAGE ON THE APPLICATION CLASSIFICATION AND SERVICE IDENTIFICATION TASKS.

<table><tr><td rowspan="2">Method</td><td colspan="3">Application Classification</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td>Ours (TraGe)</td><td>0.7517</td><td>0.7541</td><td>0.7484</td></tr><tr><td>Ours w/o FM</td><td>0.7318</td><td>0.7044</td><td>0.7044</td></tr><tr><td>Ours w/o DM</td><td>0.7489</td><td>0.7349</td><td>0.7363</td></tr><tr><td>Ours w/o FM &amp; DM</td><td>0.7234</td><td>0.7106</td><td>0.7086</td></tr><tr><td rowspan="2">Method</td><td colspan="3">Service Identification</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-Score</td></tr><tr><td>Ours (TraGe)</td><td>0.9333</td><td>0.9335</td><td>0.9331</td></tr><tr><td>Ours w/o FM</td><td>0.9275</td><td>0.9226</td><td>0.9242</td></tr><tr><td>Ours w/o DM</td><td>0.9316</td><td>0.9302</td><td>0.9305</td></tr><tr><td>Ours w/o FM &amp; DM</td><td>0.9241</td><td>0.9240</td><td>0.9236</td></tr></table>

## D. Parameter Sensitivity Analysis (RQ3)

In this subsection, we evaluate the impact of various parameter settings in the header-payload differentiated pre-training on the effectiveness of TraGe. In the pre-training of the transformer encoder, we utilize field-level masking to exploit the continuity of header fields. Specifically, the length of the masked sequence is sampled from a geometric distribution $\ell \sim \operatorname { G e o } ( p )$ , where the parameter p controls the masking length probability. By adjusting the value of p, we aim to assess how sensitive the model is to the parameter of fieldlevel masking. As shown in Fig. 3, TraGe exhibits stable classification performance on both application classification and service identification tasks across various values of p. For instance, on the service identification task, the F1-Score fluctuates only slightly within the range of 0.9275 to 0.9323, yielding a maximum difference of just 0.0048. These results demonstrate that TraGe is robust to changes in this masking parameter and that its effectiveness does not rely heavily on the configuration of the field-level masking.

## E. Sampling Variability Analysis (RQ4)

In this subsection, we evaluate the robustness of TraGe to variations in dataset sampling by evaluating its performance across multiple sampled datasets. To simulate different training conditions, we randomly select up to 5,000 samples from each traffic category using a range of random seeds. Specifically, we vary the random seed from 1 to 20, generating 20 distinct training and test set configurations. Fig. 4 presents the classification performance of TraGe under these different sampling datasets. The results show that TraGe maintains stable performance across both the application classification and service identification tasks, regardless of the specific sampling instance. For example, on the service identification task, the F1-Score varies only slightly between 0.9198 and 0.9414, with a maximum difference of just 0.0216. This consistent performance across diverse sampled datasets demonstrates the robustness of TraGe to changes in sampling settings.

## V. CONCLUSION

In this paper, we propose TraGe, a novel traffic classification model based on pre-training technology. Targeting the header-payload differences, TraGe effectively forms a generic packet representation adaptable to various traffic classification tasks. An overall comparison, along with detailed evaluations—encompassing ablation study, parameter sensitivity analysis, and sampling variability analysis—is provided, demonstrating the effectiveness of TraGe. The experimental results show that TraGe outperforms state-of-the-art methods on two traffic classification tasks. Moreover, TraGe demonstrates strong robustness in both parameter sensitivity and sampling variability analyses.

![](images/c1d6cae9d9bc9880de5700bfa1d464bc56ae0b3cdd1087c66bb8e932a8ff6f93.jpg)

<details>
<summary>line chart</summary>

| p of Geometric Distribution Geo(p) | Precision | Recall | F1-Score |
| ---------------------------------- | --------- | ------ | -------- |
| 0.1                                | 0.765     | 0.755  | 0.750    |
| 0.2                                | 0.755     | 0.750  | 0.745    |
| 0.3                                | 0.765     | 0.755  | 0.750    |
| 0.4                                | 0.760     | 0.755  | 0.750    |
| 0.5                                | 0.765     | 0.755  | 0.755    |
| 0.6                                | 0.760     | 0.755  | 0.760    |
| 0.7                                | 0.755     | 0.750  | 0.745    |
| 0.8                                | 0.750     | 0.745  | 0.745    |
| 0.9                                | 0.745     | 0.745  | 0.745    |
</details>

(a) Application Classification

![](images/b511067eb4c2964c205e6ab3dd5cb9109666ec1909b4e8a1a38f90875050ea16.jpg)

<details>
<summary>line chart</summary>

| p of Geometric Distribution Geo(p) | Precision | Recall | F1-Score |
| ---------------------------------- | --------- | ------ | -------- |
| 0.1                                | 0.935     | 0.930  | 0.930    |
| 0.2                                | 0.935     | 0.930  | 0.930    |
| 0.3                                | 0.935     | 0.930  | 0.930    |
| 0.4                                | 0.935     | 0.930  | 0.930    |
| 0.5                                | 0.935     | 0.930  | 0.930    |
| 0.6                                | 0.935     | 0.930  | 0.930    |
| 0.7                                | 0.935     | 0.930  | 0.930    |
| 0.8                                | 0.935     | 0.930  | 0.930    |
| 0.9                                | 0.935     | 0.930  | 0.930    |
</details>

(b) Service Identification

Fig. 3. Parameter analysis on field-level masking.  
![](images/888fb340b836488b149cda626585775bd8262fb1ed057d61348f37a70b6af349.jpg)

<details>
<summary>line chart</summary>

| Random Seed | Precision | Recall | F1-Score |
|-------------|-----------|--------|----------|
| 1           | 0.800     | 0.750  | 0.750    |
| 2           | 0.780     | 0.760  | 0.760    |
| 3           | 0.790     | 0.770  | 0.770    |
| 4           | 0.770     | 0.760  | 0.760    |
| 5           | 0.780     | 0.770  | 0.770    |
| 6           | 0.790     | 0.780  | 0.780    |
| 7           | 0.780     | 0.770  | 0.770    |
| 8           | 0.790     | 0.780  | 0.780    |
| 9           | 0.780     | 0.770  | 0.770    |
| 10          | 0.790     | 0.780  | 0.780    |
| 11          | 0.780     | 0.770  | 0.770    |
| 12          | 0.790     | 0.780  | 0.780    |
| 13          | 0.780     | 0.770  | 0.770    |
| 14          | 0.790     | 0.780  | 0.780    |
| 15          | 0.800     | 0.790  | 0.790    |
| 16          | 0.790     | 0.780  | 0.780    |
| 17          | 0.810     | 0.800  | 0.810    |
| 18          | 0.820     | 0.810  | 0.820    |
| 19          | 0.810     | 0.820  | 0.830    |
| 20          | 0.820     | 0.830  | 0.840    |
</details>

(a) Application Classification

![](images/3c67a9b5d6f75de413785d7ec0f46ec246106368c95f5ef79426eb4fa0884dc3.jpg)

<details>
<summary>line chart</summary>

| Random Seed | Precision | Recall | F1-Score |
| ----------- | --------- | ------ | -------- |
| 1           | 0.93      | 0.92   | 0.93     |
| 2           | 0.93      | 0.92   | 0.93     |
| 3           | 0.93      | 0.92   | 0.93     |
| 4           | 0.93      | 0.92   | 0.93     |
| 5           | 0.93      | 0.92   | 0.93     |
| 6           | 0.93      | 0.92   | 0.93     |
| 7           | 0.93      | 0.92   | 0.93     |
| 8           | 0.93      | 0.92   | 0.93     |
| 9           | 0.93      | 0.92   | 0.93     |
| 10          | 0.93      | 0.92   | 0.93     |
| 11          | 0.93      | 0.92   | 0.93     |
| 12          | 0.93      | 0.92   | 0.93     |
| 13          | 0.93      | 0.92   | 0.93     |
| 14          | 0.93      | 0.92   | 0.93     |
| 15          | 0.93      | 0.92   | 0.93     |
| 16          | 0.93      | 0.92   | 0.93     |
| 17          | 0.93      | 0.92   | 0.93     |
| 18          | 0.93      | 0.92   | 0.93     |
| 19          | 0.93      | 0.92   | 0.93     |
| 20          | 0.93      | 0.92   | 0.93     |
</details>

(b) Service Identification  
Fig. 4. Classification Performance under different sampling datasets.

## ACKNOWLEDGMENT

This work was supported in whole or in part, by National Natural Science Foundation of China (62372429, U24B6012 and U2333201), the Innovation Funding of ICT, CAS under Grant No. E461040, Pilot for Major Scientific Research Facility of Jiangsu Province of China (No.BM2021800).

## REFERENCES

[1] M. Shen, Z. Gao, L. Zhu, and K. Xu, “Efficient fine-grained website fingerprinting via encrypted traffic analysis with deep learning,” in 2021 IEEE/ACM 29th International Symposium on Quality of Service (IWQOS). IEEE, 2021, pp. 1–10.  
[2] L. Yang, Y. Wang, L. Liu, J. Huang, and S. Fu, “Expmd: an explainable framework for traffic identification based on multi-domain features,” in 2024 IEEE/ACM 32nd International Symposium on Quality of Service (IWQoS). IEEE, 2024, pp. 1–10.  
[3] K. Mao, X. Xiao, G. Hu, X. Luo, B. Zhang, and S. Xia, “Byte-label joint attention learning for packet-grained network traffic classification,” in 2021 IEEE/ACM 29th International Symposium on Quality of Service (IWQOS). IEEE, 2021, pp. 1–10.  
[4] W. Wang, S. Zhu, Z. Wu, L. Lu, Z. Li, H. Yang, and Y. Zhang, “Radd: A real-time and accurate method for ddos detection based on in-network computing,” in ICC 2024-IEEE International Conference on Communications. IEEE, 2024, pp. 3316–3321.  
[5] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, 2022, pp. 633–642.  
[6] R. Zhao, M. Zhan, X. Deng, F. Li, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “A novel self-supervised framework based on masked autoencoder for traffic classification,” IEEE/ACM Transactions on Networking, 2024.  
[7] M. Karakus and A. Durresi, “Quality of service (qos) in software defined networking (sdn): A survey,” Journal of Network and Computer Applications, vol. 80, pp. 200–218, 2017.  
[8] L. Wang, M. Wang, C. Lin, and Y. Zhang, “Accelerating traffic engineering optimization for segment routing: A recommendation perspective,” Computer Networks, vol. 264, p. 111224, 2025.  
[9] T. Van Ede, R. Bortolameotti, A. Continella, J. Ren, D. J. Dubois, M. Lindorfer, D. Choffnes, M. van Steen, and A. Peter, “Flowprint: Semi-supervised mobile-app fingerprinting on encrypted network traffic,” in Network and distributed system security symposium (NDSS), vol. 27, 2020.  
[10] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic,” in 2016 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2016, pp. 439–454.  
[11] J. Dai, Y. Chen, Y. Chen, and A. Meng, “An analysis of network traffic identification based on decision tree,” in 2021 International Conference on Artificial Intelligence and Electromechanical Automation (AIEA). IEEE, 2021, pp. 308–311.  
[12] I. L. Cherif and A. Kortebi, “On using extreme gradient boosting (xgboost) machine learning algorithm for home network traffic classification,” in 2019 Wireless Days (WD). IEEE, 2019, pp. 1–6.  
[13] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “Fs-net: A flow sequence network for encrypted traffic classification,” in IEEE INFOCOM 2019- IEEE Conference On Computer Communications. IEEE, 2019, pp. 1171–1179.  
[14] X. Xiao, W. Xiao, R. Li, X. Luo, H. Zheng, and S. Xia, “Ebsnn: Extended byte segment neural network for network traffic classification,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 5, pp. 3521–3538, 2021.  
[15] H. Zhang, L. Yu, X. Xiao, Q. Li, F. Mercaldo, X. Luo, and Q. Liu, “Tfe-gnn: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification,” in Proceedings of the ACM Web Conference 2023, 2023, pp. 2066–2075.  
[16] H. Y. He, Z. G. Yang, and X. N. Chen, “Pert: Payload encoding representation from transformer for encrypted traffic classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K). IEEE, 2020, pp. 1–8.  
[17] X. Meng, C. Lin, Y. Wang, and Y. Zhang, “Netgpt: Generative pretrained transformer for network traffic,” arXiv preprint arXiv:2304.09513, 2023.  
[18] S. Zhang, M. Gao, L. Wang, S. Xu, W. Shao, and R. Kuang, “A malwaredetection method using deep learning to fully extract api sequence features,” Electronics, vol. 14, no. 1, p. 167, 2025.  
[19] E. Horowicz, T. Shapira, and Y. Shavitt, “A few shots traffic classification with mini-flowpic augmentations,” in Proceedings of the 22nd ACM Internet Measurement Conference, 2022, pp. 647–654.  
[20] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1035–1049.  
[21] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP), 2016, pp. 407–414.  
[22] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware traffic classification using convolutional neural network for representation learning,” in 2017 International conference on information networking (ICOIN). IEEE, 2017, pp. 712–717.  
[23] S. Dadkhah, H. Mahdikhani, P. K. Danso, A. Zohourian, K. A. Truong, and A. A. Ghorbani, “Towards the development of a realistic multidimensional iot profiling dataset,” in 2022 19th Annual International Conference on Privacy, Security & Trust (PST). IEEE, 2022, pp. 1–11.  
[24] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training of deep bidirectional transformers for language understanding,” arXiv preprint arXiv:1810.04805, 2018.  
[25] X. Han, G. Xu, M. Zhang, Z. Yang, Z. Yu, W. Huang, and C. Meng, “Degnn: Dual embedding with graph neural network for fine-grained encrypted traffic classification,” Computer Networks, vol. 245, p. 110372, 2024.
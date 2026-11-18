# HF-Transformer: A Non-Pretrained Encrypted Network Traffic Classification Model Based on Packet Header Fields

Zhenzhen Yan<sup>1,\*</sup>, Lizhi Peng<sup>2,3</sup>, Peiqiang Liu<sup>1</sup>, Yingshuo Bao<sup>4</sup>, and Bo Yang<sup>2,3</sup>

<sup>1</sup>Shandong Technology and Business University

<sup>2</sup>Shandong Key Laboratory of Ubiquitous Intelligent Computing, University of Jinan

<sup>3</sup>Quancheng Laboratory

<sup>4</sup>Beijing Normal University, Zhuhai

Abstract—Network traffic classification, aiming to classify network traffic into distinct management groups, plays an indispensable role in network monitoring, QoS, and intrusion detection. The widespread of encryption techniques applied to networks has made accurate traffic classification increasingly challenging. In recent years, raw traffic data as input to deep learning models has been widely adopted due to its high classification accuracy and low reliance on human-engineered features. Yet, a critical challenge remains: different bytes within a packet carry varying levels of discriminative information, and no consensus exists on the optimal representation unit for model input.

In this paper, deep analysis of encrypted network traffic data is conducted, and our studies show that as the input to deep learning models, (1) byte-level representation outperforms bit-level encoding; (2) unigram byte features surpass the other ’n’-gram variants (halfgram, bigram, and trigram); (3) packet header bytes are significantly more discriminative than payload bytes, especially in highly encrypted datasets; and (4) certain header fields exhibit higher informativeness. Based on these findings, we propose HF-Transformer, a lightweight, non-pretrained model that leverages optimal header fields for classification. Evaluated across six datasets, HF-Transformer achieves up to 6.04% higher F1-score than SOTA alternatives, demonstrating its efficacy for encrypted traffic classification.

Index Terms—encrypted network traffic classification, deep learning, Transformers, bytes, unigram, packet headers.

## I. INTRODUCTION

HE increasing demand for data security and user pri-T vacy has driven widespread adoption of network traffic encryption. For instance, encryption across Google’s services has surged from 50% to 98% in the past decade [1]. While this trend has protected Internet users and data to a great extent, it also introduces significant challenges for traffic classification. Cybercriminals and malware increasingly exploit advanced encryption protocols, such as TLS and VPNs, to bypass security measures like firewalls, IPS, and IDS. Consequently, accurate traffic classification has become indispensable for maintaining robust network security.

There are three main categories of methods for network traffic classification: port-based, Deep Packet Inspection (DPI)- based, and Machine Learning (ML)-based [2]. Port-based methods suffer from low accuracy due to port obfuscation and dynamic port allocation. DPI-based methods have become increasingly ineffective due to the prevalence of network traffic encryption [3]. ML-based approaches can be categorized into two classes of models [4]: (1) The divide-andconquer approach requires manual feature engineering, where domain experts select and extract packet/flow features from raw traffic as model inputs, the effectiveness of this approach is constrained by the quality of hand-selected or hand-designed features and often suffers from generalization limitations due to human bias. (2) The end-to-end approach processes raw traffic data directly without manual feature extraction, eliminating expert dependency. Deep Learning (DL) techniques, such as Convolutional Neural Networks (CNNs) [4]–[6], Recurrent Neural Networks (RNNs) [7], Graph Neural Networks (GNNs) [8]–[10], and a combination of these techinques [2] [11]–[13], have demonstrated superior classification accuracy, establishing them as state-of-the-art (SOTA) solutions until the advent of Transformer-based frameworks.

In recent years, Transformer-based deep learning frameworks have revolutionized various domains, including Natural Language Processing (NLP) [14]–[16], Computer Vision (CV) [17], speech processing [18], and multimodal learning [19]. This success has inspired their application to encrypted network traffic classification, leveraging the similarities between languages and traffic byte sequences. Current approaches typically transform unlabeled traffic to pattern-preserved tokens for pre-training, followed by fine-tuning with limited labeled data. While these methods outperform traditional deep learning models, several critical challenges remain unaddressed.

1) Related literature mainly adopts bigram as the traffic representation unit [20]–[22], primarily due to its 65,536 possible values, a scale analogous to natural language vocabularies. However, this analogy is debatable under encryption: encrypted payloads are randomized, which can be treated as ”garbled text”, leaving only packet headers as interpretable data. Unlike languages, these header bytes lack semantic meaning. Consequently, using bigram as the default representation unit needs reexamination.

2) Current deep learning approaches typically feed fixedlength byte sequences (e.g., 64 bytes [21], [22], 320 bytes [23], or 784 bytes [2], [4], [24], [25]) into models without reasoning for these selections. This raises two critical issues under encryption: (1) payload bytes become uninterpretable, making their inclusion questionable, and (2) even within packet headers, different fields exhibit varying discriminative information for traffic classification. Further investigation is therefore needed to determine which bytes should constitute model inputs.

3) SOTA Transformer-based models usually adopt two phases: pre-training and fine-tuning [21], [22], [26]. While this methodology proves essential in domains like NLP, where models learn fundamental linguistic structures and semantic relationships, its effectiveness for encrypted traffic analysis remains a question. Unlike languages, packet headers lack inherent semantic meaning, and patterns learned from one header group may not generalize to others. Given the substantial computational overhead of pre-training, this raises concerns about its practical utility for network traffic classification.

To address the above issues, we perform comprehensive analyses of encrypted traffic representation at two granularities: (1) byte-level (halfgram, unigram, bigram, trigram) and (2) bit-level (Run Length Encoding, popcount). We evaluate the discriminative power of each header field versus payload bytes. Building on these insights, we propose HeaderField-Transformer (HF-Transformer), a non-pretrained encrypted network traffic classification model that selectively leverages the most informative header fields for classification. Our main contributions include:

• Our experiments demonstrate that byte-level representations (particularly unigram) have superiority over bit-level representation, despite the theoretically finer granularity of bit-wise features. This advantage stems from fundamental network protocol design: header fields are natively byte-structured, with values explicitly defined as singlebyte or multi-byte sequences in protocol specifications.

• Our analysis confirms that packet headers contain significantly more information than payloads for traffic classification, with this advantage becoming more pronounced as the percentage of encryption increases. And some particular fields, such as ”Total length”, ”Time to live” from the IP header, and ”Sequence number”, ”Ack number”, ”Window” from the TCP header, are more discriminative than others.

• We propose HF-Transformer, a non-pretrained encrypted network traffic classification model. By selecting only the most discriminative header fields (reducing input requirements by at least 80% compared to the existing DLbased models), HF-Transformer demonstrates the ”less is more” principle in traffic analysis, attaining up to a 6.04% improvement in F1-score over SOTA methods.

The rest of the paper is organized as follows. Section II presents the input representation and field selection of network data. In Section III, we detail our proposed HF-Transformer architecture. Section IV provides comparative evaluations between HF-Transformer and SOTA models, while Section V discusses relevant prior research. We conclude the paper in Section VI.

## II. INPUT ANALYSIS

This section presents a comprehensive evaluation across six datasets to answer two questions:

1) What is the optimal representation for network traffic?

2) Do all bytes contribute equally to its traffic class? If not, which specific bytes are most discriminative?

Given the demonstrated superiority of Transformer-based architectures over alternative approaches, all experiments employ our HF-Transformer framework (detailed in Section III).

## A. Datasets

TABLE I: Datasets

<table><tr><td>Dataset</td><td>Size (GB)</td><td># Flows</td><td>Selected protocols</td><td># Labels</td></tr><tr><td>ISCX VPN-nonVPN [27]</td><td>27.7</td><td>220533</td><td>TLSv1.2, GQUIC SFTP, SSDP</td><td>20</td></tr><tr><td>CSTNET-TLS1.3 [21]</td><td>9.1</td><td>46372</td><td>TLSv1.3</td><td>120</td></tr><tr><td>USTC-TFC [28]</td><td>3.71</td><td>9853</td><td>TLSv1.2, SSLv3 NBSS, SSDP</td><td>20</td></tr><tr><td>Streaming(application)</td><td>4.5</td><td>59103</td><td>TLSv1.2, TLSv1 DTLSv1.2</td><td>8</td></tr><tr><td>Streaming and File Transfer</td><td>5.3</td><td>224447</td><td>TLSv1.2, SSL</td><td>6</td></tr><tr><td>Streaming(content)</td><td>6.7</td><td>142724</td><td>TLSv1.2</td><td>3</td></tr></table>

Table I summarizes the six datasets used in our tasks. The first three datasets are publicly available, while the remaining three are our collections. A subset of special protocols is listed in the fourth column, common protocols (e.g., TCP, UDP, HTTP) are not included for brevity.

1) Dataset I: ISCX: The first dataset is the ISCX VPNnonVPN traffic dataset [27], a publicly available collection of 27.7 GB network traffic data. It contains packets from 13 services (7 VPN and 6 NonVPN) generated by 16 distinct applications. For certain services, we further segmented the data by application, resulting in 20 unique labels.

2) Dataset II: CSTNET-TLS1.3: The second dataset is the publicly available CSTNET-TLS 1.3 dataset [21], collected from the China Science and Technology Network (CSTNET) [29]. This 9.1 GB dataset consists of encrypted traffic using the TLS 1.3 protocol, covering 120 distinct applications, so the number of labels of this dataset is 120.

3) Dataset III: USTC-TFC: The third dataset is the publicly available USTC-TFC dataset [28], comprising 3.71 GB of network traffic. It includes 10 malware traffic types and 10 normal traffic types, yielding 20 distinct labels.

![](images/fff54063a6e6cd944e2667724441635eea42a80c3007a61517ac5ea65e71f884.jpg)  
(e) Run Length Encoding  
Fig. 1: Input Representation Units  
(f) Popcount

4) Dataset IV: Streaming(application): Over the past decade, streaming applications have experienced exponential growth in popularity. According to Cisco’s Visual Networking Index [30], live video traffic now constitutes 82% of global Internet traffic, posing significant network management challenges. To support streaming traffic analysis research, we collected a dataset of streaming traffic from January to March 2024. This fourth dataset (4.5 GB) captures flows from eight dominant Chinese streaming applications: Bilibili, Douyin, WeChat, Taobao, JD, Meituan, Weibo, and Zhihu, providing eight distinct traffic classes.

5) Dataset V: Streaming and File Transfer: The fifth dataset comprises 5.3 GB of network traffic collected in March 2024, featuring two distinct service types from three major providers: 1) Streaming traffic: YouTube, WeChat Live, and Baidu Live. 2) File transfer traffic: Google Cloud, Tencent Cloud, and Baidu Cloud. This collection yields 6 labeled traffic classes (two services × three providers), enabling comparative analysis across different network service paradigms.

6) Dataset VI: Streaming(content): Our sixth dataset addresses the understudied challenge of streaming content classification. While prior work has primarily focused on the idenfication of whether a flow is streaming or not [31] [32], with limited research on content-type identification [33], we present a 6.7 GB dataset capturing three distinct streaming genres (chat, game, outdoor) from Bilibili collected in April 2023, so the number of labels is 3.

## B. Network Traffic Representation

In natural languages, words serve as the fundamental semantic unit, a natural choice since they carry inherent meaning and systematically combine to form phrases, sentences, and documents. The story is completely different in the network traffic scenario, since every bit, byte, or ’n’ bytes does not preserve any semantic information, which makes it hard to determine a meaningful basic representation unit.

In our study, six network traffic representation units are attempted, namely halfgram, unigram, bigram, trigram, Run Length Encoding (RLE), and popcount. Halfgram converts every four bits to a hexadecimal digit. Unigram, bigram, and trigram convert every one byte, two bytes, and three bytes to 2-digit, 4-digit, and 6-digit hexadecimal numbers, respectively. All these representations can be implemented using a sliding window mechanism, as shown in Fig. 1, with window size and stride being (4 bits, 4 bits) for halfgram, (8 bits, 8 bits) for unigram, (16 bits, 16 bits) for bigram, and (24 bits, 24 bits) for trigram.

The RLE representation processes network traffic at the most fundamental level by preserving the original bitstream structure. As illustrated in Fig. 1e, our implementation first converts raw traffic into continuous bit streams, and then computes RLE for consecutive ’1’s and ’0’s, finally, represents each segment as (count, bit-value) pairs. This approach preserves the complete temporal structure of the original bitstream without requiring any human-defined segmentation of consecutive bit patterns at 8-bit boundaries. For example, consider the 48-bit input: 111000110001000000000000110111011100001101000111, unigram and RLE generate completely different encodings.

• Unigram: e3 10 00 dd c3 47

• RLE: 1f 1e 15 1e b 78 15 a 1f a 1f 28 15 a b 1e 1f

The popcount representation shown in Fig. 1f computes the Hamming weight of each byte, counting the number of set bits (’1’s) while discarding positional information, unlike RLE, which preserves bit sequence patterns.

![](images/06e134b82d6b8de3e4922580f2c9da5ba2e7f4417134fa896ac6da3dc1f651f1.jpg)  
(a) ISCX

![](images/d629697d1a2d562807da46d542651c9df63e0a02af8b9beed0d8c97adb4a8517.jpg)  
(b) CSTNET

![](images/0b644c4b70a61b729afcd0c79f278ee66051b9e7bf72ebfa527a0d6f02c7a7e5.jpg)  
(c) USTC-TFC

![](images/c45af1d42582b88a230c4be09d10379ca5e6b6a7a331b315081e4c531fa51c5c.jpg)  
(d) Streaming(application)

![](images/d002537362764819e2d9a6b9e30e07afbdd43c2e771ea3fe16f7e95647871300.jpg)  
(e) Streaming and File Transfer

![](images/b714174babc801acb891067b27d10a18b7e4f079daf5962cfd7f640651a3e2a2.jpg)  
(f) Streaming(content)

Fig. 2: Input Representation Performance Across Six Datasets  
![](images/ff183da2e1b63e3fe0639192663474825ce0ab6f2ea5b3cc4a263f74e6bf9f17.jpg)  
Fig. 3: Byte Samples from Packet Headers and Content

In encrypted network traffic, the communication contents are randomized, which means the byte values of packet payloads do not convey the original payload information, but the packet headers stay intact. In our analysis of the input data unit, the Ethernet header is removed, since it only contains information for frame forwarding within each link. We analyze three packet headers separately, i.e., IP header, transport layer header, and application layer header. The IP header and transport layer header are unencrypted, and the application layer header is encrypted, since the Transport Layer Security (TLS) lies above the transport layer and under the application layer. The IP addresses and TCP/UDP port numbers are masked to avoid biased interference in a finite set [11] [34] [21]. Twenty bytes are selected for each of these three headers, as shown in Fig. 3. This figure mainly illustrates the TCP cases that do not have an option field. For comparison purposes, we also pick twenty bytes right next to the twenty bytes of the application header and twenty bytes at the end of the payload.

We evaluate six input representations across five 20-byte segments (1st-4th and final 20 bytes of L3) from six datasets. Fig. 2 compares the classification performance of six input representations across five 20-byte packet segments. Our analysis reveals that unigram representations consistently achieve superior results, primarily because unigrams directly correspond to the fundamental design of network headers, where most fields are byte-aligned in protocol specifications. While RLE provides finer bit-level granularity, it artificially combines bits across different header fields, violating the logical boundaries established by protocol designers. Unigrams maintain the original field structure of packets, enabling the model to learn authentic header field patterns rather than synthetic bit groupings.

The commonly adopted bigram offers 65,536 possible encodings (vs. unigram’s 256), it counterintuitively demonstrates inferior performance because a bigram is two unigrams plus relative bit position information, and in HF-Transformer, with position embeddings added to token embeddings, the temporal relations among all the byte tokens are learned, so no byte or position information is lost in the unigram representation. For Bigram, with 256 times more possible tokens, it suffers from substantially lower token recurrence rates, requiring more training data to learn meaningful patterns. Unigram provides richer input features, as the higher recurrence probability of 256 tokens enables better modeling of both byte values and their temporal relationships.

Fig. 2 also shows that the 1st and 2nd 20-byte segments (IP/transport headers) exhibit significantly higher discriminative power compared to payload bytes. This gap widens with encryption rate, e.g., fully encrypted payloads such as CSTNET, the 3rd and last 20 bytes are mainly payload, and these bytes are 80% less informative than the 1st and 2nd 20 bytes. While popcount maintains more consistent scores across segments (only 15% drop on the CSTNET dataset), its absolute performance remains poor. This shows popcount’s inability to capture class-relevant patterns.

![](images/322388ed38806851116628e7f70e3a9ee6ce77e4b387e89f10020410d86732be.jpg)  
Fig. 4: Evaluation of Selected IP Header Fields on Six Datasets

Based on these findings, we use unigrams to represent traffic and focus on packet headers for classification.

## C. Input Fields Selection

In this section, we dive deeper to study the fields of IP and TCP headers. The purpose of this analysis is to investigate whether there exist any particular fields that play an important role in classifying network traffic. For the IP header, we choose the ”Type of service”, ”Total length”, ”Flags and Fragment offset”, ”Time to live”, and ”Protocol” fields. For the TCP header, ”Sequence number”, ”Ack number”, ”Data offset” together with ”Reserved” and ”Control bits”, ”Window”, and ”Urgent pointer” are picked. For the UDP header, the fields ”Length” and ”Checksum” are combined to make a 32-bit segment, so that it can be compared with the ”Sequence number” field of the TCP header. The unincluded fields, such as ”checksum” and ”identification,” can be treated as irrelevant for classification as they are used for packet processing and error checking [35].

Based on the performance evaluation illustrated in Fig. 4, ”Total length” and ”Time to live” are more informative than the other fields, yielding 79.89% and 80.17% accuracy on average, respectively, much higher than the ”Flags and FragmentOffset” and ”Protocol” fields, whose accuracy are only 42.66% and 48.83%.

Similarly, the TCP header fields analysis shown in Fig.5 indicates that the ”Sequence number”, ”Ack number”, and ”Window” fields have stronger classification power, yielding 81.57%, 88.12%, and 90.49% accuracy, respectively.

Based on the header fields analysis, we adopt ”Total length” and ”Time to live” from the IP header and ”Sequence number”, ”Ack number”, and ”Window” fields from the TCP header as our model input, while excluding less informative ones.

## III. HF-TRANSFORMER

Based on the analysis on network traffic representation and input fields selection, we propose HF-Transformer, a nonpretrained network traffic classification model. Unlike related Transformer-based models, HF-Transformer learns directly from labeled top-performing fields of packet headers, without the need for a pre-training step. Due to the widely applied encrypted techniques, the payload of encrypted traffic is less informative compared to the unencrypted packet headers, and only a few fields in packet headers are discriminative in traffic classification tasks. These fields, only 13 bytes, can be quickly learnt by the training phase of downstream tasks. One major difference between natural languages and encrypted network traffic is that the vocabulary of a language can be over 600,000, whereas the ”vocabulary” of network traffic is only 256 using the unigram representation. In natural languages, the pretraining step aims to expedite future downstream tasks by learning phrases, grammar rules, and idiomatic expressions, etc., beforehand, so that the pretrained model is languageequipped. In network traffic, however, the limited ”vocabulary” removes the necessity of pre-training.

(e) Streaming and File Transfer  
![](images/2ebbb788689d475547a6df43246904b7df8bb8b0cbff1ed84de69fe42b8168fb.jpg)  
(d) Streaming(application)  
Fig. 5: Evaluation of Selected TCP Header Fields on Six Datasets

The framework of our proposed HF-Transformer is shown in Fig. 6. We transform the selected top-performing header fields into tokens as the input to the HF-Transformer model. The main architecture of the HF-Transformer model is a multilayer Transformer encoder [14] [21] that consists of 12 layers with 12 self-attention heads per layer. The hidden size and sequence length are set to 768 and 512, respectively.

## A. Raw Traffic to Tokens

The raw network traffic in .pcap or .pcapng format undergoes an initial cleaning process to eliminate noise and anomalies. Subsequently, the processed traffic is grouped into flows or sessions according to task-specific criteria. A flow is defined as a sequence of packets sharing the same 5-tuple: source/destination IP addresses, source/destination ports, and the transport layer protocol identifier. $f l o w ^ { i } \ =$ $\{ p _ { 1 } ^ { i } , p _ { 2 } ^ { i } , . . . , p _ { n } ^ { i } , i , n \in \mathbb { Z } ^ { + } \}$ . A session is defined as a pair of flows where the source and destination IP addresses and port numbers are reversed, representing a bidirectional conversation between two endpoints. $s e s s i o n \sp i =$ $\{ f l o w _ { ( s r c - d s t ) } ^ { i } , f l o w _ { ( d s t - s r c ) } ^ { i } , \ i \in \mathbb { Z } ^ { + } \}$ . Flows are unidirectional, whereas sessions represent bidirectional communication. After aggregating traffic into sessions, a slicing operation divides them into sequential bursts [21]:

$$
\begin{array}{r l} & b u r s t ^ {i} = \left\{ \begin{array}{l} b u r s t _ {(s r c - d s t)} ^ {i} = \{p _ {(s r c - d s t), 1} ^ {i},..., p _ {(s r c - d s t), k} ^ {i} \} \\ b u r s t _ {(d s t - s r c)} ^ {i} = \{p _ {(d s t - s r c), 1} ^ {i},..., p _ {(d s t - s r c), l} ^ {i} \}, \end{array} \right. \\ & i, k, l \in \mathbb {Z} ^ {+}, \quad p ^ {i} \in s e s s i o n ^ {i}, \quad b u r s t ^ {i} \subseteq s e s s i o n ^ {i} \end{array}\tag{1}
$$

where k and l denote that there are k packets from $f l o w _ { ( s r c - d s t ) }$ , and l packets from $f l o w _ { ( d s t - s r c ) }$ in this burst. In this model, we set $k + l = 1 0 0 .$ , so each burst has 100 packets, and a burst is a subset of a session. Next, the ”Total length” and ”Time to live” fields from the IP header and the ”Sequence number”, ”Ack number”, and ”Window” fields from the TCP header are kept. In the end, processed traffic bursts are transformed into word-like hexadecimal unigram tokens similar to natural languages. A special classification token [CLS] is prepended, and it is used as a sequence-level representation for classification in the final hidden layer. The token sequence is illustrated in equation (2). Finally, labels are attached to the token sequences, which are then split into training, validation, and testing datasets in the ratio of 8:1:1.

$$
\begin{array}{r l} & T o k e n S e q u e n c e ^ {i} = \{[ C L S ], T L _ {1} ^ {i}, T L _ {2} ^ {i}, T T L _ {1} ^ {i}, S e q N _ {1} ^ {i}, \\ & S e q N _ {2} ^ {i}, S e q N _ {3} ^ {i}, S e q N _ {4} ^ {i}, A c k N _ {1} ^ {i}, A c k N _ {2} ^ {i}, A c k N _ {3} ^ {i}, A c k N _ {4} ^ {i}, \\ & W _ {1} ^ {i}, W _ {2} ^ {i} \}, \quad i \in \mathbb {Z} ^ {+} \end{array}\tag{2}
$$

![](images/f4bba04999ba6028eda818f62abce0baa4f36cebd746bbafb39893ce2b73e51d.jpg)  
Fig. 6: HF-Transformer Framework

## B. Training HF-Transformer

Both the input tokens and their positional indices are embedded into vectors of dimension d=768. The final embedding for each token is obtained by summing its token embedding and positional embedding, combining token and position information into a single representation. The token embeddings encode salient features from top-performing packet header fields, while the position embeddings capture their sequential and temporal dependencies. For positional encoding, we adopt the sine and cosine functions of varying frequencies, as originally proposed in the Transformer paper [14].

The HF-Transformer model is trained using the final labeled embeddings. At the core of the Transformer’s self-attention mechanism is the computation of scaled dot-product attention. This involves: Firstly, calculating the scaled dot product attention between the Query (Q) and Key (K). Secondly, applying a softmax function to normalize the scaled attention scores (ensuring they sum to 1). Finally, computing the dot product of attention weights and Value matrix (V ), as defined in equation (3), to get the matrix of attention outputs.

$$
\begin{array}{l} \text {Attention} (Q, K, V) = \text {softmax} \left(\frac {Q K ^ {T}}{\sqrt {d _ {k}}}\right) V \\ d _ {k} \text {is the dimension of queries and keys} \end{array}\tag{3}
$$

The Query (Q), Key (K), and Value (V ) matrices are derived by applying linear transformations to the same input matrix X using three learned weight matrices $W _ { Q } , W _ { K }$ , and $W _ { V }$ , respectively. The output of the 12 transformer layers is fed into a fully connected layer, followed by a softmax function to produce the predicted classification probabilities.

During training, the model optimizes its parameters by minimizing the cross-entropy loss (Equation (4)), where y denotes the one-hot encoded ground-truth label and $\hat { y }$ represents the predicted probability vector, both of dimension q (number of classes).

$$
l (\pmb {y}, \hat {\pmb {y}}) = - \sum_ {i = 1} ^ {q} y _ {i} \log \hat {y} _ {i}\tag{4}
$$

## IV. COMPARISON EXPERIMENTS

In this section, the performance of HF-Transformer is compared with six SOTA models across the six datasets introduced in Section II-A.

Recent studies [20]–[23] [26] demonstrate that Transformerbased pre-training models consistently outperform traditional approaches, including fingerprint-based, feature-engineered, and conventional DL methods, on multiple public datasets. Accordingly, we select four representative Transformer models for comparison: PERT [20], ET-BERT [21], TrafficFormer [22], and YaTC [23]. To ensure a comprehensive evaluation, we also include one DL baseline: GraphDApp [8] and one hybrid DL-Transformer baseline: ConViTML [24]. All models are trained to convergence, and all inputs are standardized through our preprocessing pipeline (Section III-A) to ensure fair comparison.

Table II shows which of the six datasets (presented in Table I) were used for pre-training six SOTA traffic classification models. ET-BERT, TrafficFormer, and YaTC used Dataset I (Section II-A1) for pre-training, while ET-BERT additionally used Dataset II (Section II-A2) and YaTC used Dataset III (Section II-A3). Datasets IV–VI (Sections II-A4–II-A6) were not used in any model’s pre-training phase.

Our implementation details are described in Section IV-A. The comparison results are analyzed in Section IV-B. Additionally, Section IV-C presents a convergence speed analysis, showing that HF-Transformer incurs negligible overhead despite removing the pre-training phase.

TABLE II: Previously Seen Datasets for Traffic Classification Models

<table><tr><td>Models</td><td>Dataset I: ISCX</td><td>Dataset II: CSTNET-TLS1.3</td><td>Dataset III: USTC-TFC</td><td>Dataset IV: Streaming (application)</td><td>Dataset V: Streaming and File Transfer</td><td>Dataset VI: Streaming (content)</td></tr><tr><td>GraphDApp [8]</td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>ConViTML [24]</td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>PERT [20]</td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>ET-BERT [21]</td><td> $\checkmark$ </td><td> $\checkmark$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>TrafficFormer [22]</td><td> $\checkmark$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>YaTC [23]</td><td> $\checkmark$ </td><td> $\times$ </td><td> $\checkmark$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr><tr><td>HF-Transformer</td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td><td> $\times$ </td></tr></table>

TABLE III: Comparison Results on ISCX, CSTNET-TLS1.3, and USTC-TFC Datasets

<table><tr><td>Dataset</td><td colspan="4">Dataset I: ISCX</td><td colspan="4">Dataset II: CSTNET-TLS1.3</td><td colspan="4">Dataset III: USTC-TFC</td></tr><tr><td>Model</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>GraphDApp [8]</td><td>0.7608</td><td>0.8262</td><td>0.7613</td><td>0.7436</td><td>0.6049</td><td>0.6545</td><td>0.6055</td><td>0.6086</td><td>0.8837</td><td>0.8818</td><td>0.8843</td><td>0.8756</td></tr><tr><td>ConViTML [24]</td><td>0.9647</td><td>0.9661</td><td>0.9647</td><td>0.9648</td><td>0.7065</td><td>0.7060</td><td>0.7065</td><td>0.7007</td><td>0.9237</td><td>0.9308</td><td>0.9237</td><td>0.9227</td></tr><tr><td>PERT [20]</td><td>0.9553</td><td>0.9560</td><td>0.9556</td><td>0.9551</td><td>0.7551</td><td>0.7577</td><td>0.7553</td><td>0.7549</td><td>0.9484</td><td>0.9441</td><td>0.9412</td><td>0.9411</td></tr><tr><td>ET-BERT [21]</td><td>0.9927</td><td>0.9929</td><td>0.9928</td><td>0.9926</td><td>0.7997</td><td>0.8069</td><td>0.7999</td><td>0.8006</td><td>0.9645</td><td>0.9615</td><td>0.9622</td><td>0.9594</td></tr><tr><td>TrafficFormer [22]</td><td>0.9901</td><td>0.9902</td><td>0.9902</td><td>0.9899</td><td>0.7727</td><td>0.7787</td><td>0.7730</td><td>0.7721</td><td>0.9613</td><td>0.9595</td><td>0.9579</td><td>0.9542</td></tr><tr><td>YaTC [23]</td><td>0.9912</td><td>0.9914</td><td>0.9912</td><td>0.9912</td><td>0.8545</td><td>0.8577</td><td>0.8545</td><td>0.8546</td><td>0.9596</td><td>0.9620</td><td>0.9596</td><td>0.9598</td></tr><tr><td>HF-Transformer</td><td>0.9953</td><td>0.9954</td><td>0.9954</td><td>0.9954</td><td>0.9148</td><td>0.9174</td><td>0.9149</td><td>0.9150</td><td>0.9709</td><td>0.9667</td><td>0.9671</td><td>0.9663</td></tr></table>

TABLE IV: Comparison Results on Streaming(application), Streaming and File Transfer, and Streaming(content) Datasets

<table><tr><td>Dataset</td><td colspan="4">Dataset IV: Streaming(application)</td><td colspan="4">Dataset V: Streaming and File Transfer</td><td colspan="4">Dataset VI: Streaming(content)</td></tr><tr><td>Model</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td></tr><tr><td>GraphDApp [8]</td><td>0.9160</td><td>0.9222</td><td>0.9162</td><td>0.9166</td><td>0.9808</td><td>0.9810</td><td>0.9808</td><td>0.9807</td><td>0.6335</td><td>0.6347</td><td>0.6338</td><td>0.6330</td></tr><tr><td>ConViTML [24]</td><td>0.9781</td><td>0.9787</td><td>0.9781</td><td>0.9782</td><td>0.9574</td><td>0.9615</td><td>0.9574</td><td>0.9573</td><td>0.9563</td><td>0.9564</td><td>0.9563</td><td>0.9563</td></tr><tr><td>PERT [20]</td><td>0.9811</td><td>0.9812</td><td>0.9811</td><td>0.9811</td><td>0.9659</td><td>0.9662</td><td>0.9660</td><td>0.9658</td><td>0.9742</td><td>0.9747</td><td>0.9741</td><td>0.9740</td></tr><tr><td>ET-BERT [21]</td><td>0.9845</td><td>0.9843</td><td>0.9843</td><td>0.9843</td><td>0.9770</td><td>0.9798</td><td>0.9771</td><td>0.9771</td><td>0.9744</td><td>0.9750</td><td>0.9743</td><td>0.9746</td></tr><tr><td>TrafficFormer [22]</td><td>0.9829</td><td>0.9834</td><td>0.9828</td><td>0.9829</td><td>0.9847</td><td>0.9848</td><td>0.9848</td><td>0.9848</td><td>0.9789</td><td>0.9790</td><td>0.9787</td><td>0.9790</td></tr><tr><td>YaTC [23]</td><td>0.9844</td><td>0.9846</td><td>0.9844</td><td>0.9844</td><td>0.9885</td><td>0.9887</td><td>0.9885</td><td>0.9885</td><td>0.9773</td><td>0.9778</td><td>0.9773</td><td>0.9774</td></tr><tr><td>HF-Transformer</td><td>0.9922</td><td>0.9923</td><td>0.9923</td><td>0.9923</td><td>0.9885</td><td>0.9891</td><td>0.9883</td><td>0.9886</td><td>0.9940</td><td>0.9940</td><td>0.9937</td><td>0.9940</td></tr></table>

## A. Implementation and Evaluation Details

Our experiments are implemented with PyTorch 2.0.1, UER [36], and ET-BERT [21]. The jobs are run on NVIDIA GeForce RTX 4090 GPUs. The AdamW optimizer is adopted in the training phase, and the learning rate is set to $2 \times 1 0 ^ { - 5 }$ the batch size is 32, and the dropout rate is 0.5.

Four evaluation metrics: micro accuracy, macro precision, macro recall, and macro F1 [26] are used to evaluate the performance.

## B. Comparison Results

From the results presented in Table III and Table IV, HF-Transformer outperforms the SOTA models by pushing the F1 score up by at least 0.42% - 6.04% on five out of six datasets, and the effectiveness increases with encryption percentage, e.g., the F1 score gain is 6.04% and 1.5% for the fully encrypted CSTNET and Streaming(content) datasets. This superior performance is achieved by requiring only 13 bytes of header data - a dramatic reduction compared to SOTA methods that process tens to hundreds of bytes from both headers and payloads. Fig. 2 of Section II also illustrates that the payload bytes for CSTNET and Streaming(content) datasets fail to provide any information about traffic class, i.e., the classification accuracy is below 10% and 40% (40% is low, considering only 3 labels for the Streaming(content) dataset) for these two datasets, respectively.

Unlike fully encrypted traffic, datasets like USTC-TFC and Streaming and File Transfer include some proportion of unencrypted traffic (e.g., HTTP and TCP), the plaintext payload aids in traffic classification. As a result, the advantage of HF-Transformer is less pronounced compared to fully or highly encrypted datasets.

Evaluation on the ISCX dataset shows that HF-Transformer outperforms ET-BERT, TrafficFormer, and YaTC, despite their usage of this dataset for pre-training, achieving at least a 0.42 F1-score improvement. While pretrained models are expected to enhance the accuracy of downstream tasks, pre-training on non-discriminative byte-level features fails to deliver this intended benefit.

HF-Transformer focuses exclusively on top-performing header fields while eliminating non-discriminative or encrypted payload bytes and avoids pre-training on randomized data that provides no transferable patterns. We believe that as network encryption approaches ubiquity (100% penetration), HF-Transformer’s header-fields-focused architecture will demonstrate increasingly significant advantages.

## C. Convergence Study of the Training step (with pretrained model vs. without pretrained model)

Since accuracy and speed are two benefits that pretrained models aim to bring to the downstream tasks, accuracy is discussed in the above sections, in this section, the convergence speed of the training phase is studied using the CSTNET-TLS1.3 dataset. Experiments on the other datasets exhibit similar patterns.

![](images/4c471390c246b7b66129415b87348bbcab398501766049efad920597a329e9fd.jpg)  
Fig. 7: Convergence Study of the Training Step on the CSTNET-TLS1.3 Dataset

From Figure 7, we can tell that the pretrained model gives the downstream task a good start: pretrained ET-BERT achieves 0.4624 initial accuracy after epoch 1, benefiting from its prior pre-training on this dataset, as shown in Table II. However, HF-Transformer shows a steeper learning curve, surpassing ET-BERT by epoch 11 with 0.8112 accuracy. After this point, HF-Transformer’s training accuracy keeps growing until it ultimately reaches 0.9228 at epoch 35 (not shown in the figure), demonstrating that pre-training provides no ultimate accuracy benefit.

## V. RELATED WORK

Deep learning methods. In 2017, Wang et al. pioneered the use of CNNs to automatically learn features from raw network traffic [4], [28]. This approach inspired numerous subsequent studies applying DL models to traffic analysis. For instance, Sirinam et al. employed CNNs to extract features from raw packet direction sequences [6], while Liu et al. utilized RNNs to learn representations from raw flow data [7]. Further advancements involved hybrid architectures combining CNNs and RNNs to capture both packet-level and flow-level features [2], [13], [37], [38] or to model spatial and temporal characteristics simultaneously [12]. Additionally, GNNs were introduced to process raw traffic data and derive structural packet/flow features [8], [9], [39]. These DL-based methods have achieved superior performance until the attempt to apply

Transformer-based models to the network traffic classification field is made.

Transformer models. ConViTML [24] employs CNNs to process byte images generated from the first 784 bytes of packets, splitting them into patches that are flattened and fed into Transformer. Similarly, YaTC [23] converts each flow into a multi-level flow representation matrix. While these methods embed traffic data (bytes, packets, or flows) into fixed-size images, they do not account for the varying discriminative power of different pixels. For instance, encrypted payload pixels may contribute less to classification accuracy than header pixels. Other approaches, such as PERT [20], ET-BERT [21], and TrafficFormer [22], adopt bigram encoding to represent raw hexadecimal byte sequences as their input to Transformer. These works primarily focus on aligning their input range with typical NLP vocabulary sizes, neglecting the inherent properties of encrypted traffic. Notably, they do not evaluate whether their byte-level representations are optimal or whether all packet fields are equally informative for classification.

To the best of our knowledge, existing Transformer-based models follow the standard pre-training and fine-tuning framework. In this approach, a model is first pretrained on large scale unlabeled traffic data to learn contextual representations, typically using techniques like token masking [15]. During fine-tuning, task-specific models leverage these pre-trained representations to reduce demand for labeled input data and computing power. However, a critical distinction between natural language and network traffic lies in the generalizability of learned representations. While NLP models often transfer well across diverse tasks, the representations learned from encrypted traffic may not be as reusable or effective for downstream applications. This raises concerns about whether pretrained traffic models can adequately generalize to future traffic classification tasks, given the unique challenges posed by encrypted data.

## VI. CONCLUSION

This paper investigates encrypted network traffic representation and input field selection, and introduces a nonpretrained encrypted network traffic classification model: HF-Transformer. Experimental results show that HF-Transformer outperforms SOTA methods, particularly in high-encryption scenarios (up to 6.04% F1 improvement), while requiring no pre-training phase and at least 80% less input data. In future work, we plan to apply HF-Transformer in the intrusion and malware detection field to further test its effectiveness and generalization ability.

## REFERENCES

[1] Google, “Google Transparancy Report,” https://transparencyreport. google.com/https/overview?hl=en, 2025, [Online; accessed 23-July-2025].

[2] Z. Zou, J. Ge, H. Zheng, Y. Wu, C. Han, and Z. Yao, “Encrypted Traffic Classification with a Convolutional Long Short-Term Memory Neural Network,” in 2018 IEEE 20th International Conference on High Performance Computing and Communications; IEEE 16th International Conference on Smart City; IEEE 4th International Conference on Data Science and Systems (HPCC/SmartCity/DSS), 2018, pp. 329–334.

[3] S. Rezaei and X. Liu, “Deep Learning for Encrypted Traffic Classification: An Overview,” IEEE Communications Magazine, vol. 57, no. 5, pp. 76–81, 2019.

[4] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end Encrypted Traffic Classification with One-dimensional Convolution Neural Networks,” in 2017 IEEE International Conference on Intelligence and Security Informatics (ISI), 2017, pp. 43–48.

[5] N. Malekghaini, E. Akbari, M. A. Salahuddin, N. Limam, R. Boutaba, B. Mathieu, S. Moteau, and S. Tuffin, “AutoML4ETC: Automated Neural Architecture Search for Real-World Encrypted Traffic Classification,” IEEE Transactions on Network and Service Management, vol. 21, no. 3, pp. 2715–2730, 2024.

[6] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning,” in Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, ser. CCS ’18. New York, NY, USA: Association for Computing Machinery, 2018, pp. 1928–1943.

[7] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-Net: A Flow Sequence Network For Encrypted Traffic Classification,” in IEEE INFOCOM 2019 - IEEE Conference on Computer Communications, 2019, pp. 1171–1179.

[8] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate Decentralized Application Identification via Encrypted Traffic Analysis Using Graph Neural Networks,” IEEE Transactions on Information Forensics and Security, pp. 2367–2380, 2021.

[9] T.-L. Huoh, Y. Luo, P. Li, and T. Zhang, “Flow-Based Encrypted Network Traffic Classification With Graph Neural Networks,” IEEE Transactions on Network and Service Management, vol. 20, no. 2, pp. 1224–1237, 2023.

[10] H. Xu, C. Si, S. Li, Z. Cheng, C. Wang, J. Xie, P. Sun, and Q. Liu, “FlowMiner: A Powerful Model Based on Flow Correlation Mining for Encrypted Traffic Classification,” in IEEE INFOCOM 2025 - IEEE Conference on Computer Communications, 2025.

[11] X. Wang, S. Chen, and J. Su, “App-Net: A Hybrid Neural Network for Encrypted Mobile Traffic Classification,” in IEEE INFOCOM 2020 - IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS), 2020, pp. 424–429.

[12] K. Lin, X. Xu, and H. Gao, “TSCRNN: A novel classification scheme of encrypted traffic based on flow spatiotemporal features for efficient management of IIoT,” Comput. Networks, vol. 190, 2021.

[13] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescape, “Improving Performance, Reliability, and Feasibility in Mul-´ timodal Multitask Traffic Classification with XAI,” IEEE Transactions on Network and Service Management, vol. 20, no. 2, pp. 1267–1289, 2023.

[14] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention Is All You Need,” in Proceedings of the 31st International Conference on Neural Information Processing Systems. Red Hook, NY, USA: Curran Associates Inc., 2017, pp. 6000– 6010.

[15] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding,” in Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, NAACL-HLT 2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers). Association for Computational Linguistics, 2019, pp. 4171–4186.

[16] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, “ALBERT: A Lite BERT for Self-supervised Learning of Language Representations,” in International Conference On Learning Representaions (ICLR), 2020.

[17] A. Dosovitskiy, L. Beyer, A. Kolesnikov, D. Weissenborn, X. Zhai, T. Unterthiner, M. Dehghani, M. Minderer, G. Heigold, S. Gelly, J. Uszkoreit, and N. Houlsby, “An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale,” in 9th International Conference on Learning Representations, ICLR 2021, Virtual Event, Austria, May 3-7, 2021, 2021.

[18] A. Gulati, J. Qin, C.-C. Chiu, N. Parmar, Y. Zhang, J. Yu, W. Han, S. Wang, Z. Zhang, Y. Wu, and R. Pang, “Conformer: Convolutionaugmented Transformer for Speech Recognition,” in Proc. Interspeech 2020, 2020, pp. 5036–5040.

[19] A. Shin, M. Ishii, and T. Narihira, “Perspectives and Prospects on Transformer Architecture for Cross-Modal Tasks with Language and Vision,” International Journal of Computer Vision, vol. 130, no. 2, pp. 435–454, Feb 2022.

[20] H. Y. He, Z. Guo Yang, and X. N. Chen, “PERT: Payload Encoding Representation from Transformer for Encrypted Traffic Classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K), 2020, pp. 1–8.

[21] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Traffic Classification,” in Proceedings of the ACM Web Conference 2022, New York, NY, USA, 2022, pp. 633–642.

[22] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “ TrafficFormer: An Efficient Pre-trained Model for Traffic Data ,” in 2025 IEEE Symposium on Security and Privacy (SP), May 2025.

[23] R. Zhao, M. Zhan, X. Deng, Y. Wang, Y. Wang, G. Gui, and Z. Xue, “Yet Another Traffic Classifier: A Masked Autoencoder Based Traffic Transformer with Multi-Level Flow Representation,” in Proceedings of the AAAI Conference on Artificial Intelligence, vol. 37, no. 4, 2023, pp. 5420–5427.

[24] L. Yang, S. Guo, D. Liu, Y. Zeng, X. Jiao, and Y. Zhou, “ConViTML: A Convolutional Vision Transformer-Based Meta-Learning Framework for Real-Time Edge Network Traffic Classification,” IEEE Transactions on Network and Service Management, vol. 21, no. 3, pp. 3344–3357, 2024.

[25] J. Dai, X. Xu, and F. Xiao, “GLADS: A global-local attention data selection model for multimodal multitask encrypted traffic classification of IoT,” Computer Networks, vol. 225, 2023.

[26] P. Lin, K. Ye, Y. Hu, Y. Lin, and C.-Z. Xu, “A Novel Multimodal Deep Learning Framework for Encrypted Traffic Classification,” IEEE/ACM Transactions on Networking, vol. 31, no. 3, pp. 1369–1384, 2023.

[27] G. Draper-Gil, A. H. Lashkari, M. Mamun, and A. A. Ghorbani, “Characterization of Encrypted and VPN Traffic using Time-related Features,” in Proceedings of the 2nd international conference on information systems security and privacy (ICISSP 2016), 2016, pp. 407–414.

[28] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware Traffic Classification Using Convolutional Neural Network for Representation Learning,” in 2017 International Conference on Information Networking (ICOIN), 2017, pp. 712–717.

[29] “CSTNET,” https://www.cstnet.cn/, [Online; accessed 18-May-2025].

[30] “Visual Network Index (VNI) complete prediction,” https://www.cisco. com/c/zh cn/solutions/service-provider/visual-networking-index-vni/ index.html.

[31] Y.-N. Dong, J.-J. Zhao, and J. Jin, “Novel feature selection and classification of Internet video traffic based on a hierarchical scheme,” Computer Networks, vol. 119, p. 102–111, 2017.

[32] X. Mu and W. Wu, “A Parallelized Network Traffic Classification Based on Hidden Markov Model,” in 2011 International Conference on Cyber-Enabled Distributed Computing and Knowledge Discovery, 2011, pp. 107–112.

[33] Y. Xie, H. Deng, L. Peng, and Z. Chen, “Accurate Identification of Internet Video Traffic Using Byte Code Distribution Features,” in International Conference on Algorithms and Architectures for Parallel Processing, 2018, pp. 46–58.

[34] M. Lotfollahi, M. J. Siavoshani, R. S. H. Zade, and M. Saberian, “Deep Packet: A Novel Approach For Encrypted Traffic Classification Using Deep Learning,” Soft Computing, vol. 24, pp. 1999 – 2012, 2017.

[35] G. Xie, Q. Li, and Y. Jiang, “Self-attentive deep learning method for online traffic classification and its interpretability,” Computer Networks, vol. 196, 2021.

[36] Z. Zhao, H. Chen, J. Zhang, X. Zhao, T. Liu, W. Lu, X. Chen, H. Deng, Q. Ju, and X. Du, “UER: An Open-Source Toolkit for Pre-training Models,” in Conference on Empirical Methods in Natural Language Processing, 2019.

[37] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescape, “XAI Meets Mobile Traffic Classification: Understanding´ and Improving Multimodal Deep Learning Architectures,” IEEE Transactions on Network and Service Management, vol. 18, no. 4, pp. 4225– 4246, 2021.

[38] I. Guarino, G. Aceto, D. Ciuonzo, A. Montieri, V. Persico, and A. Pescape, “Contextual counters and multimodal Deep Learning for\` activity-level traffic classification of mobile communication apps during COVID-19 pandemic,” Computer Networks, vol. 219, 2022.

[39] K. Xu, W. Hu, J. Leskovec, and S. Jegelka, “How Powerful are Graph Neural Networks?” in 7th International Conference on Learning Representations (ICLR), 2019.
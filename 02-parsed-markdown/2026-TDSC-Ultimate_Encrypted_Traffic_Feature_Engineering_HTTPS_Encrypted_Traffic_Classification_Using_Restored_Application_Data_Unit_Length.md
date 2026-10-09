# Ultimate Encrypted Traffic Feature Engineering: HTTPS Encrypted Traffic Classification Using Restored Application Data Unit Length

Zihan Chen , Member, IEEE, Guang Cheng , Member, IEEE, Dandan Niu , Student Member, IEEE, Yuyu Zhao , Member, IEEE, Yuyang Zhou , Member, IEEE, and Shanqing Jiang , Member, IEEE

Abstract—Over-the-top (OTT) applications mainly communicate through HTTPS, the most famous encryption protocol family on the Internet. The classification of HTTPS encrypted traffic can effectively obtain fine-grained OTT application information for network management and cyber security. As the most expressive feature, the side-channel length sequence is widely used by current research, especially the packet length sequence. However, these attempts ignored interferences from protocol piecewise decoupling and encryption covering, leading to poor performance. Based on the application layer feature engineering theory, we proposed a new metric called Application Data Unit (ADU) length to eliminate the interferences. However, ADU length cannot be obtained directly from packets as the TLS encryption protocol covers the entire application layer, which contains an intrusive and variable HTTP header. Hence, we designed a Length-Correction Multiple Regression Neural Network (LC-MRNN) algorithm to restore the real ADU length sequences accurately. Exhaustive experiments in two scenarios ofthe real CERNET network show that no matter the HTTP-1.1 or HTTP-2.0 protocol, the LC-MRNN model can achieve significantly accurate ADU length restoration. In classification, with the assistance of the LS-LSTM classifier, our method outperforms the state-of-the-art methods with about 4.2% improvement in F1-score (93.52%).

Index Terms—Encrypted traffic classification, application layer feature engineering, application data unit, length-correction multiple regression neural network, HTTPS.

## I. INTRODUCTION

NCRYPTED traffic has become an inevitable trend, led (Transport Layer Security)) encryption protocol family [1].

According to the Google Transparency Report [2], as of October 2023, the percentage of Chrome Web pages that are encrypted has reached 98%, and almost 100% of traffic across all Google products and services is encrypted. Despite the fact that QUIC (Quick UDP Internet Connections, i.e. HTTP-3.0) has been embraced by certain applications, HTTP-TLS-TCP ecosystem still constitutes the mainstream at present. Encrypted traffic provides users and companies with data security and privacy protection [3]. However, it brings trouble to Internet Service Providers (ISPs) in network management (e.g. traffic acceleration), information forensics (e.g., behavior auditing), and cyber security (e.g., intrusion blocking), especially for Over-the-top (OTT) services and applications. Traffic encryption makes it difficult to use the traditional Deep Packet Inspection (DPI) [4] method based on plaintext. Therefore, current research on encrypted traffic classification focuses on HTTPS traffic, which is also the main concern of this paper.

To tackle this problem, the academic realm has put forward encrypted traffic classification methods [5] to uphold the merits of timeliness, large-scale processing, transparency, and privacy protection in traffic-side analysis. These methods make use of features that are not obscured by encryption to categorize or identify the actual kinds of Internet services, applications, functions, and malicious intent underlying the current traffic. They are capable of offering effective intelligence support for currently impaired network management and security. Nonetheless, distinct from natural language and images, encrypted traffic is structured sequence data in a non-Euclidean space [6]. Packets serve as the fundamental transmission unit, and flows act as the atomized service support. As a typical supervised learning problem, when disregarding data sources, encrypted traffic classification currently confronts two of the most formidable challenges: (1) In the context of ever-evolving protocols, network environments, and applications, which features should be employed for classification? (2) Which model is most appropriate for representing these features? At present, the research in this domain predominantly centers on feature engineering and classifier optimization.

Considering that features establish the upper bound of classification performance, while models merely strive to approximate it, the most critical aspect in the realm of encrypted traffic analysis persists as feature engineering. Although the accuracy upper limit is classifier-dependent [7], the gradual improvement of classification accuracy shows that the limit of feature information disclosure is also gradually increasing. In other words, improving classification accuracy, especially the lower limit of classification accuracy, requires the input features to contain as much information disclosure as possible. At present, feature engineering for encrypted traffic predominantly centers around three categories of features: residual plaintext header features, inter-arrival time distribution features, and length sequence features. Regarding generalization capabilities, length sequence features have been empirically demonstrated to exhibit superior performance in the majority of classification scenarios associated with data behavior [8].

![](images/d9a1f952b48d51cbbc96f1f8212789802c7432978b9bcb45143d63c28073cb84.jpg)  
Fig. 1. HTTPS encrypted traffic transmitting protocol stack and source of interference.

However, the current encrypted traffic classification methods predominantly utilize packets as the input unit. Only a limited number of studies have employed Protocol Data Units (PDUs) of high-level protocols (e.g., TLS) as input units [9], [10]. From the perspective of protocol engineering design, higher-level protocols are more intricately associated with the application’s behavior, whereas lower-level protocols are more closely related to the network environment. The encrypted traffic classification methods based on the length sequence of packets or TLS segments encounter feature interference resulting from piecewise decoupling. For instance, in the case of HTTPS, the data generated by OTT applications is successively encapsulated and segmented by the HTTP, TLS, TCP, and IP protocols. Consequently, when packets or TLS segment sequences are used as the source for encrypted traffic feature extraction, the disclosure of information regarding encrypted traffic features is restricted compared to the original data. This is mainly because the encrypted traffic introduces two instances of segmentation and one instance ofencryption interference, as depicted in Fig. 1. As a result, there is inconsistency between the actual data volume and the total length of the packets, which causes errors in classification.

In this paper, we focus on the ultimate encrypted traffic feature engineering, aiming to classify encrypted traffic using the features most relevant to the data transmitted by encrypted traffic in the protocol stack. The work we have done is shown in Fig. 2 from the perspective of the HTTPS network protocol stack. Based on the Application Layer Feature Engineering (ALFE) and Application Data Unit (ADU) length sequence feature proposed earlier [11], we instantiate the concept of ADU under HTTPS protocol and theoretically prove the superiority of the ADU length sequence feature under HTTPS encrypted traffic classification. Furthermore, aiming at the problem that the real ADU length is disturbed by TLS encryption and underlying HTTP header with variable length, we study the sources of interference, including systematic error and random error. Based on removing systematic errors, we propose the Length-Correction Multiple Regression Neural Networks (LC-MRNN) algorithm for random error reduction to restore the real ADU length sequences from the TLS segment length sequences. We further instantiate LC-MRNN with the state-of-the-art LS-LSTM classifier [9] into the LC-MRNN with Application Classification (LC-MRNN-AC) model in HTTPS scenarios with both the HTTP-1.1 and HTTP-2.0 application layer protocol. Finally, the application classification of encrypted traffic with high precision is realized.

![](images/3b3bec16a36b24b9492ef79ca482718e48e323a8870a2ad8a8bbd9b72504fa40.jpg)  
Fig. 2. Procedures in encrypted traffic classification with the current research focuses.

Our main contributions are summarized as follows:

On the basis of previous work ALFE [11], we have broken through the concept of BBP’s (Bit-Per-Peak) description of application transmission data under streaming media [12], and innovatively defined the concept of ADU - a new metric of encrypted traffic inputs in the HTTPS scenario and use the ADU length sequence to classify encrypted traffic. By further proposing three new evaluation criteria, we prove the theoretical advantages of ADU in encrypted traffic classification compared with TLS segment and TCP packet.

We design LC-MRNN, a transformer-based ADU length restoration algorithm, which can accurately restore the ADU length sequence of HTTPS traffic (both HTTP-1.1 and HTTP-2.0 protocols are included). The restoration of ADU length through decoding the application layer segmentation semantics becomes the key to breaking through the bottleneck of classification accuracy for encrypted traffic - this is precisely the core contribution of this paper.

TABLE I  
ALL THE ACRONYMS USED IN THIS PAPER

<table><tr><td>Acronyms</td><td>Full Name</td><td>Acronyms</td><td>Full Name</td><td>Acronyms</td><td>Full Name</td></tr><tr><td>OTT</td><td>Over The Top</td><td>DPI</td><td>Deep Packet Inspection</td><td>MTU</td><td>Maximum Transmission Unit</td></tr><tr><td>ADU</td><td>Application Data Unit</td><td>PDU</td><td>Protocol Data Unit</td><td>PJR</td><td>ProJection Ratio</td></tr><tr><td>TLS</td><td>Transport Layer Security</td><td>TCP</td><td>Transmission Control Protocol</td><td>OPR</td><td>OccuPation Ratio</td></tr><tr><td>HTTP</td><td>HyperText Transfer Protocol</td><td>BBP</td><td>Bit Per Peak</td><td>FEC</td><td>Feature Efficiency Coefficient</td></tr><tr><td>HTTPS</td><td>HTTP over TLS</td><td>ALFE</td><td>Application Layer Feature Engineering</td><td>NLP</td><td>Neuro-Linguistic Programming</td></tr><tr><td>LC-MRNN</td><td>Length-Correction Multiple Regression Neural Network</td><td>MLP</td><td>MultiLayer Perceptron</td><td>LC-MRNN -AC</td><td>LC-MRNN with Application Classification</td></tr><tr><td>CERNET</td><td>China Education and Research NETwork</td><td>CNN</td><td>Convolutional Neural Network</td><td>MATR</td><td>Maximum ADU Threshold Rate</td></tr><tr><td>LS-LSTM</td><td>Length Sensitive-Long Short-Term Memory</td><td>RNN</td><td>Recurrent Neural Network</td><td>GGNN</td><td>Gated Graph Neural Networks</td></tr><tr><td>ISP</td><td>Internet Service Provider</td><td>DHCP</td><td>Dynamic Host Configuration Protocol</td><td>QUIC</td><td>Quick UDP Internet Connections</td></tr></table>

Moreover, we further instantiate LC-MRNN with our previous work LS-LSTM classifier [9] and A3C system [13] into the LC-MRNN-AC model. It guarantees that the classification can be realized effectively and efficiently.

We have deepened the open-world scenario and proposed the concept of the small world and the big world. We then collect and publish real-world HTTPS data in the largescale CERNET environment with pure real application labels and corresponding decrypted HTTP plaintext data in reassembled data form. Experiments conducted in the big and small worlds show that LC-MRNN can effectively restore the real ADU length sequence and greatly improve the classification effect of existing encrypted traffic classifiers. LC-MRNN-AC outperforms state-of-the-art methods.

The rest of the paper is shown as follows. Section II introduces the main research directions of existing encrypted traffic from two perspectives: classifier and length feature engineering. In Section III, we theoretically prove the ADU length sequence’s effectiveness and formalize this paper’s research problems. Section IV puts forward the LC-MRNN algorithm and implements it concretely in HTTP-1.1 and HTTP-2.0 scenarios. In Section V, we conduct experiments from two perspectives to prove the method’s effectiveness. Finally, we summarize our research and discuss the existing problems and further research in Section VI. All the abbreviations mentioned in this paper are shown in Table I.

## II. RELATED WORK

Encrypted traffic classification pursues good performance, and the evaluation indexes can be accuracy, precision, recall, etc. The optimization of these indexes is reflected in each procedure of encrypted traffic classification.

## A. Classifiers of Encrypted Traffic

Encrypted traffic classification is a typical supervised learning problem for which the labeled sample dataset is critical [14]. In the classification of encrypted traffic, the current mainstream classification methods have transitioned from machine learning methods to deep learning methods. These deep learning classifiers can be divided into three categories: single base model, model overlay, and model fusion.

In the single base model, the most classical CNN was pioneered for encrypted traffic classification [15] to take advantage of its end-to-end learning features. And then, MLP [16], RNN (LSTM) [17], Text-CNN [18], CapsNet [19] are used in encrypted traffic classification to deal with the problem of poor representation of sequential data features by CNN. These methods use the binary or byte information of the raw packet for classification.

However, the automatic feature extraction ability of a single deep learning model is limited, which is manifested in the different attention to the classification accuracy of different categories [20]. Therefore, with the development of semi-supervised learning and hardware computing power, some studies tend to use multiple deep learning models to classify encrypted traffic to improve the classification effect. The most direct way is the model overlay. It uses multiple models (usually models with different structures) to make up for the feature presentation shortcomings of a single model.

In the model overlay, the representive ones are STNN [21] (LSTM and 3d-CNN), TEST [22] (CNN and LSTM), CNN and LSTM combined with distributed training [23], DISTILLER [6] (CNN and MLP), CENTIME [24] (ResNet and AutoEncoder).

Another way to combine multiple models is the model fusion, which combines multiple base model elements into a new neural network classifier. It includes CLD-NET [25] (serialized CNN, LSTM and Fully-Connected Network (FCN)), ICLSTM [26] (Inception CNN juxtaposed with LSTM), SAM [27] (self-attention combined with CNN), tree-RNNs [28], I<sup>2</sup>RNN [29] (using each round of output during the iteration of an LSTM classifier as a fingerprint), ensemble Graph Neural Networks (GNN) [20]. Model fusion can further coordinate the feature expression capabilities of different neural network elements but relies more on expert knowledge.

A summary of the three different schema of deep learning classifiers is shown in Table II.

In addition, some studies have applied other deep learning optimization techniques to existing deep learning base models. For example, incremental learning [30], explainable artificial intelligence [31], unknown application clustering [32], triple attention mechanism [33], multimodal learning [34].

TABLE II  
CURRENT DEEP LEARNING MODELS IN ENCRYPTED TRAFFIC CLASSIFICATION

<table><tr><td>Works</td><td>Year</td><td>Deep Learning Schema</td><td>Classifier</td></tr><tr><td>[15]</td><td>2017</td><td rowspan="5">Single base model</td><td>CNN</td></tr><tr><td>[16]</td><td>2019</td><td>MLP</td></tr><tr><td>[17]</td><td>2019</td><td>LSTM</td></tr><tr><td>[18]</td><td>2019</td><td>TextCNN</td></tr><tr><td>[19]</td><td>2019</td><td>CapsNet</td></tr><tr><td>[21]</td><td>2019</td><td rowspan="5">Model overlay</td><td>LSTM and 3d-CNN</td></tr><tr><td>[22]</td><td>2019</td><td>CNN and LSTM</td></tr><tr><td>[23]</td><td>2019</td><td>CNN and LSTM</td></tr><tr><td>[6]</td><td>2021</td><td>CNN and MLP</td></tr><tr><td>[24]</td><td>2021</td><td>ResNet and AutoEncoder</td></tr><tr><td>[25]</td><td>2021</td><td rowspan="6">Model fusion</td><td>CNN + LSTM + FCN</td></tr><tr><td>[26]</td><td>2021</td><td>Inception CNN + LSTM</td></tr><tr><td>[27]</td><td>2021</td><td>Self-attention + CNN</td></tr><tr><td>[28]</td><td>2021</td><td>Tree-organized RNNs</td></tr><tr><td>[29]</td><td>2023</td><td>LSTM Iteration Fingerprint</td></tr><tr><td>[20]</td><td>2023</td><td>Ensemble GNNs</td></tr></table>

## B. Encrypted Traffic Length Feature Engineering

Feature is an essential basis of classification. A good feature can effectively represent the gap between different categories to achieve classification effectively. However, the current research suggests that direct input of all raw bytes of the flow does not perform well in the cases of high encryption ratio [35]. It further evidences that the selected features are not necessarily the best and cannot be interpreted [6].

The main reason is the non-high-dimensional optimization of features (similar to natural language, traffic data will be segmented into different PDUs due to the network protocol stack, and the direct input of the original traffic data will lead to the loss of high-dimensional features) and local optimal with structural features ignorance [6] (encrypted traffic, unlike images, is structured data containing security protocols and network protocol stacks, and the original traffic directly input will erase such features). This phenomenon creates a serious concept drift [36].

Encrypted traffic is essentially a packet sequence in the network [37]. Therefore, the existing research on feature optimization mainly starts from its serialization characteristics, especially the Markov features between packets.

Korczy M. et al. [38] first proposed the FoSM to depict the change relation of message type in TLS headers. Further, TLS handshake certificates and the first application data length were proposed, named SoB [39]. Then, Chang Liu et al. first proposed LaFFT [40] based on fast Fourier transform, then proposed MaMPF [41] based on message type sequence and length block sequence, and finally proposed FS-Net [8] based on full packet length and representation learning. So far, the classification of encrypted traffic has mainly adopted the feature of the length sequence [42], [43], [44].

As a result of the layered design of network protocols, data needs to be segmented during actual transmission. As a result, the length of packets obtained at the network layer or transport layer differs greatly from that at the application layer. Subsequent studies pay more attention to the high dimensional length sequence features of encrypted traffic length sequences [45]. The high dimensional length sequence feature refers to the one obtained by further calculation or reconstruction of the packet length values. The most typical is to reconstruct the PDU of the packet sequence, using the PDU of the higher layer protocol as the input unit to eliminate the error caused by packet-level data segmentation.

TABLE III  
REPRESENTATIVE ENCRYPTED TRAFFIC LENGTH FEATURE ENGINEERING WORKS

<table><tr><td>Works</td><td>Year</td><td>Feature Unit</td><td>Specialties</td></tr><tr><td>[38]</td><td>2014</td><td>FoSM</td><td>Message Type</td></tr><tr><td>[39]</td><td>2017</td><td>SoB</td><td>Length Included</td></tr><tr><td>[40]</td><td>2018</td><td>LaFFT</td><td>Fourier Transform</td></tr><tr><td>[41]</td><td>2018</td><td>MaMPF</td><td>Power Distribution</td></tr><tr><td>[8], [42], [43], [44]</td><td>2019+</td><td>Packet length</td><td>Data Segmentation</td></tr><tr><td>[47]</td><td>2020</td><td>TLS Bidirectional flow</td><td>TLS Interaction</td></tr><tr><td>[46]</td><td>2021</td><td>TLS Segment Length</td><td>TLS Payload</td></tr><tr><td>[10]</td><td>2021</td><td>TLS Bidirectional Application Data</td><td>TLS Data</td></tr><tr><td>[9], [45]</td><td>2021</td><td>Multi-PDU</td><td>Diversified PDU</td></tr><tr><td>[48]</td><td>2021</td><td>Graphic Packet Length</td><td>Graphic Features</td></tr><tr><td>[3]</td><td>2022</td><td>Path Signature</td><td>Cumulative Length</td></tr><tr><td>[49]</td><td>2023</td><td>Multi-flow Lengths</td><td>Inter-flow Features</td></tr></table>

In this kind of research, the representative features include TLS segment length sequence [46], TLS bidirectional Application Data (a special message type, different from ADU in this paper) length sequence [10], TLS bidirectional flow length sequence [47] and multi-PDU length sequence [45] with its N-gram length hyper-sequence [9] in our previous studies.

In addition to high protocol level length features, there are also studies on cumulative length features [3], graphic length features [48], and multi-flow features [49].

A summary of different length feature engineering works is shown in Table III. The feature determines the upper limit of the classification effect, and the model only approximates it. However, the premise for practical feature engineering and model building is that there should be no errors or interferences in the input. Otherwise, the significance of selected features will be suppressed. This is also the problem that this paper needs to overcome.

## III. APPLICATION DATA UNIT LENGTH SEQUENCE

In this section, we first introduced and defined the concept of ADU in encrypted HTTPS traffic classification. Then, we prove that the ADU length sequence is more efficient than TLS segment and TCP packet length sequences. Afterwards, the ADU length interference is analyzed, and the problems to be solved in this paper are also formally defined.

## A. Application Data Unit

It is worth noting that ADU is not a completely new concept in the field of networks. It has already been introduced in the QoE estimations and classifications domain (although not named strictly as ADU, the meaning is highly relevant), and it mainly focuses on the fragments after the video is segmented [12]. However, during this process, these concepts are mainly used to calculate the statistical features of streaming media transmission such as BBP, rather than focusing on the relationship between the variable headers and core body of the encrypted application layer. For the classification scenarios of encrypted traffic, especially the HTTPS, in our previous work, we proposed the theory of ALFE [11]. In ALFE, ADU is a general name for all PDU at the application layer. However, currently in the field of encrypted traffic classification, ADU has not been clearly defined. Therefore, considering different message queue patterns, taking the HTTPS protocol stack as an example, we define the ADU in HTTPS encrypted traffic classification as follows.

Definition 1 (ADU). ADU is all data transmitted by HTTP protocol in a single request or response process: From the definition, it is evident that the distinction between BBP and ADU lies in the following aspects. Regarding encrypted videos, BBP constitutes a part of the entire encrypted protocol and encompasses the application layer header. In the case of the downlink stream response, ADU represents the actual size of the video fragments without the header. When it comes to HTTPS, BBP can be likened to the aggregation of TLS Segments. Simultaneously, BBP depends on well-defined boundaries. It is more appropriate for streaming media videos that are transmitted in fragments. However, it is less suitable for application scenarios such as web pages.

In an actual network environment, if an ADU is needed, we only need to obtain the HTTP request body and response body, that is, the data transmitted in the HTTP communication process. However, TLS encrypts all HTTP contents (including headers and bodies).

## B. Superiority ofADU Length Sequence

The HTTPS protocol stack has three different PDUs without considering the IP layer. They are packet length sequence, TLS segment length sequence, and ADU length sequence. The reason for not considering the IP layer is that its fixed IP header length and the existence of DHCP make its features irrelevant to classification. Since the ADU length is consistent with the data block length transferred in each request-response pair, it strongly correlates with the data standing back from the application to be classified.

In our prior research [11], we theoretically established the superiority of the ADU features. According to the principle [7], within the context of the same dataset and classification objective, the greater the feature information gain, the more effectively it can differentiate samples and fulfill the classification task. To illustrate the superiority of the ADU length sequence in encrypted traffic classification based on datasets, we chose the CERNET-1.1 Dataset (to be detailed later) for a preliminary experiment. We directly compared the relative information gains of the ADU length sequence, the TLS Segment length sequence, and the packet length sequence. The results indicate that the relative information gain of ADU (0.9978) exceeds that of the TLS segment (0.9950) and is significantly higher than that of the TCP packet (0.8483). Hence, theoretically, the ADU length sequence exhibits the optimal classification performance in these PDUs.

In addition to information gain, we also need to consider the real network characteristics because network protocols impose new restrictions on different PDU lengths.

If Ethernet is used as the data link layer protocol, the length of captured IP packets cannot exceed the default MTU (1500 bytes). Therefore, the length of the TCP payload does not exceed 1460 bytes (the IP header is fixed at 20 bytes, and the TCP header is at least 20 bytes). Therefore, two new concepts, namely Projection Ratio (PJR) and Occupation Ratio (OPR), are proposed to describe this feature.

PJR is proposed to represent the proportion of the packet length value in the valid length range. OPR represents the coverage ratio of the number of length values in the current sample space. It is worth noting that since the TLS segment and ADU do not have a clear and fixed upper limit, the value interval between the maximum and minimum length values in the current sample is selected as the length interval to be projected.

Suppose that the sample set is X, the PDUs used in the current classification are $u ,$ all length values of the current PDU are $L ^ { ( u ) }$ (including duplicates, equal to all length data), its quantity is $n ^ { ( u ) }$ , and the number of length values that do not duplicate is $\boldsymbol { s } ^ { ( u ) }$ , then the formal expression of PJR and OPR is as follows:

$$
\begin{array}{l} P J R = s ^ {(u)} / \left[ m a x \left(L ^ {(u)}\right) - m i n \left(L ^ {(u)}\right) \right] \\ O P R = s ^ {(u)} / n ^ {(u)} \end{array}\tag{1}
$$

Given the differences in the size of flows and the splicing of PDUs among applications, we select 50% of the PDU quantity of the flow with the largest number of PDUs in a certain category of the current dataset as the selection threshold. According to the arrival order of PDUs (i.e., the position of PDUs in the flow, starting from 1), PDUs with positions less than this threshold in each flow will be included in the calculation.

Why do we choose the position of PDU as the selection metric and set the threshold at 50%? The reasons mainly come from four aspects.

Firstly, the PDU sequence input in the process of encrypted traffic classification is continuous, and there is a Markovian relationship between adjacent PDUs. The position of PDU directly represents the arrival stage of data, and starting from the first position can meet the complete characterization of the flow.

\- Secondly, the number of packets in network flows can be approximately fitted by a Zipf distribution [50], allowing us to select a moderate proportion and still obtain a large proportion of PDUs.

$$
P (k; s, N) = \frac {1 / k ^ {s}}{H _ {N , s}}, H _ {N, s} = \sum_ {i = 1} ^ {N} \frac {1}{i ^ {s}}\tag{2}
$$

During this process, the PDUs from a very small number of flows without similar volume references can be eliminated. When s = 1, the proportion of considered PDUs to all PDUs is approximately $1 - 0 . 5 / \ln ( N )$ . When N is 1000, the acquisition ratio can reach 92.76%. For actual networks, the N value is much larger, and the distribution of flows within the same type is more concentrated, so the actual proportion of obtained PDUs will be even higher.

TABLE IV  
PJR, OPR AND FEC OF THREE DIFFERENT PDUS

<table><tr><td></td><td colspan="2">TCP Packet</td><td colspan="2">TLS Segment</td><td colspan="2">HTTP ADU</td></tr><tr><td></td><td>PJR</td><td>OPR</td><td>PJR</td><td>OPR</td><td>PJR</td><td>OPR</td></tr><tr><td>Douban</td><td>0.0761</td><td>0.1275</td><td>0.0211</td><td>0.2524</td><td>0.0023</td><td>0.2863</td></tr><tr><td>Hupu</td><td>0.0035</td><td>0.0915</td><td>0.0078</td><td>0.3441</td><td>0.0037</td><td>0.2784</td></tr><tr><td>JD</td><td>0.0162</td><td>0.1387</td><td>0.0078</td><td>0.4444</td><td>0.0008</td><td>0.4242</td></tr><tr><td>Sohu</td><td>0.0146</td><td>0.2694</td><td>0.0051</td><td>0.6075</td><td>0.0023</td><td>0.4039</td></tr><tr><td>Netease</td><td>0.0631</td><td>0.0969</td><td>0.0300</td><td>0.3065</td><td>0.0026</td><td>0.2778</td></tr><tr><td>Sina</td><td>0.0256</td><td>0.2856</td><td>0.0087</td><td>0.6220</td><td>0.0148</td><td>0.4081</td></tr><tr><td>Youku</td><td>0.0063</td><td>0.3244</td><td>0.0014</td><td>0.4586</td><td>0.0042</td><td>0.3500</td></tr><tr><td>Zhihu</td><td>0.0035</td><td>0.0365</td><td>0.0010</td><td>0.0720</td><td>0.0001</td><td>0.9210</td></tr><tr><td>FEC</td><td colspan="2">1.7545</td><td colspan="2">2.3720</td><td colspan="2">2.8336</td></tr></table>

Thirdly, we verified this theoretical result through a preexperiment. Taking the CERNET-1.1 dataset as an example, we can calculate that at the 50% threshold, the proportion of ADU obtained is 98.80%, that of TLS Segment is 99.79%, and that of TCP packets is 98.58%. This selection ratio is completely in line with expectations.

Fourth, given that there may be differences in the distribution of long and short flows among different categories, we adopted the principle of median robustness, which means that for skewed flow features, the median is more resistant to the interference of outliers than the mean. Therefore, we selected 50% as the threshold.

Since PJR reflects the proportion in the value space, the lower PJR is, the looser distribution of features relative to the value space is, and the lower the probability of feature similarity is. OPR reflects the proportion in the sample space, so the higher OPR is, the lower the probability of feature similarity is. In order to effectively combine these two evaluation criteria, we further propose a new concept called Feature Efficiency Coefficient (FEC):

$$
F E C = \log \left(\frac {1}{P J R}\right) + O P R\tag{3}
$$

We take logarithm base 2 of reciprocal of PJR. The main reason is that the maximum value determines the value space of PJR in ADU or segment in the current sample (to avoid almost zero PJR when a potential PDU max size is too large). If the logarithmic constraint is not used, the utility of OPR will be significantly reduced.

Table IV shows the PJR and OPR of the eight representative applications of HTTP-1.1 under three different PDUs, as well as the FEC of each PDU. Noted that if there is only one possible length, the PJR at that position is 0.

We also conducted statistics on the HTTP-2.0 dataset (CERNET-Web-2.0). The FEC presented by the three different PDUs is consistent with Table IV, that is, the FEC contained in the ADU is higher than that of the other two PDUs. The results show that the ADU length sequence is the most expressive. Therefore, we select the ADU length sequence as the optimized feature to classify encrypted traffic.

![](images/0be84caa67d8a613819176c8cca87b4eebf7f9420f6cc686e9d03d1d942f60b8.jpg)  
Fig. 3. Illustration of systematic and random errors in HTTPS ADU length.

## C. ADU Length Interference and Restoration

However, TLS effectively encrypts the entire HTTP application layer. Therefore, the real features of ADU, especially the length features, cannot be obtained directly. The ADU length read from the PDU segments of TLS has systematic and random errors. The systematic errors are caused by the plaintext TLS header and the encrypted fixed part in the HTTP header. It is worth noting that the fixed HTTP header length is derived from the fixed-length field in the HTTP header. Random errors are more varied than systematic errors, including non-fixed fields and variable-length fields of HTTP headers. Systematic errors need to be compensated by analyzing their causes, while random errors can only be reduced by estimation. The two errors are illustrated in Fig. 3.

Systematic errors can also be reduced using models, but it is better to remove them directly. As TLS headers are all plaintext (in TLS-1.3, the encrypted handshake part is determined as data), the systematic errors caused by the TLS layer can be directly removed. However, systematic errors in the HTTP layer need to be further calculated. After statistical analysis of massive samples, typical systematic errors in HTTP layer (include both HTTP-1.1 and HTTP-2.0) are listed in Table V. It can be seen that the systematic error of HTTP-2.0 is much less than that of HTTP-1.1. It is because HTTP-2.0 uses standardized static and dynamic parameter tables and the HPACK dynamic compression mechanism to compress the original fixed-length content greatly.

After the systematic error is removed, the remaining random error needs to be reduced by the model, which is the core problem to be solved in this paper. The essence of ADU accurate restoration is to restore the TLS segment length sequence to the real ADU length sequence.

## D. Problem Definition

Before the real ADU length restoration, the problem of encrypted traffic classification based on length should be formally described. The problem of encrypted traffic classification based on length is to classify encrypted traffic to a specific service or application, using only the length sequence of the traffic as the original input. Assuming there are N samples to be classified and C different categories, then the k-th sample (assuming the sequence length is m) $x _ { k } = [ l _ { 1 } ^ { ( k ) } , l _ { 2 } ^ { ( k ) } , \ldots , l _ { m } ^ { ( \hat { k } ) } ]$ , where $l _ { u } ^ { ( k ) }$ refers to the length of the u-th unit (ADU, in this paper) in the sequence. If it is a service classification and the real category of $x _ { k }$ is $S _ { k } .$ , the goal of the encrypted traffic service classification is to build a model $\varphi ( x _ { k } )$ to get a predicted label $\widehat { S _ { k } }$ which is expected to be the real label $S _ { k }$

TABLE V  
TYPICAL SYSTEMATIC ERRORS OF ADU LENGTH IN HTTP LAYER OF HTTP-1.1 AND HTTP-2.0

<table><tr><td colspan="3">HTTP-1.1 Request</td><td colspan="3">HTTP-1.1 Response</td></tr><tr><td>Fixed Request Line</td><td>Request MethodBlank SpaceRequest VersionRequest Line End Flag (\r\n)</td><td>3 bytes2 bytes8 bytes2 bytes</td><td>Fixed Response Line</td><td>Response VersionBlank SpaceStatus CodeRequest Line End Flag</td><td>8 bytes2 bytes3 bytes2 bytes</td></tr><tr><td>Fixed Header Fields</td><td>Host Key *Connection Field *User_agent Key &amp; Part of Value *Accept key *Accept-encoding key *Accept-language key *Request Header End Flag</td><td>8 bytes24 bytes27 bytes10 bytes19 bytes19 bytes2 bytes</td><td>Fixed Header Fields</td><td>Content-Type Key *ColonBlank SpaceField End FlagRequest Header End Flag</td><td>13 bytes1 bytes1 bytes2 bytes2 bytes</td></tr><tr><td>Total Systematic Error</td><td colspan="2">15+109=124 bytes</td><td>Total Systematic Error</td><td colspan="2">15+18=33 bytes</td></tr><tr><td colspan="3">HTTP-2.0 Request</td><td colspan="3">HTTP-2.0 Response</td></tr><tr><td>Fixed Frame Header</td><td>Payload LengthFrame TypeFrame FlagStream Identifier Field(Reserved bit &amp; Stream identifier)</td><td>3 bytes1 bytes1 bytes4 bytes</td><td>Fixed Frame Header</td><td>Same as Request</td><td>9 bytes</td></tr><tr><td>Fixed Frame Payload</td><td>Composite Fixed Field(Exclusive tag &amp; Stream dependency)Multiplexing Weight</td><td>4 bytes1 bytes</td><td>Fixed Frame Payload</td><td>HTTP Status Code</td><td>1 bytes</td></tr><tr><td>Total Systematic Error</td><td colspan="2">9+5=14 bytes</td><td>Total Systematic Error</td><td colspan="2">9+1=10 bytes</td></tr></table>

\*A colon (1 byte) with a blank space (1 byte) after the key and the field end flag (2 bytes) are considered (4 bytes in total).

For ADU restoration, we aim to make $l _ { u } ^ { ( k ) }$ closer to the real length we need. Therefore, assume that the current sample for classification is x (the sequence length is m), the observation sequence length is $\widetilde { x } = [ \widetilde { l _ { 1 } } , \widetilde { l _ { 2 } } , \ldots , \widetilde { l _ { m } } ]$ , and the corresponding real ADU length sequence is $r ( x ) = [ l _ { 1 } , l _ { 2 } , \ldots , l _ { m } ]$ . The goal of restoring ADU length sequence is to create a model that makes the length value of each ADU $\widetilde { l _ { u } } ( 1 \le u \le m )$ in the sequence closer to its corresponding real length $l _ { u } .$ . It is assumed that the ADU length are independent and identically distributed, and since the minimum systematic error $E _ { \omega }$ is removed, the observed value must be greater than the real ADU length value. It means if the random error of ADU length is $E _ { \delta }$ , for $\forall 1 \leq u \leq m , E _ { \delta } ( u ) = \tilde { l _ { u } } - E _ { \omega } - l _ { u } \geq 0$ . Hence, this paper aims to build a model $\mu$ that is according to the minimum sum of the differences between all the observed lengths and true lengths in a sequence, namely argmin ${ \textstyle \sum _ { u } ^ { m } } [ \mu ( \widetilde { l _ { u } } - E _ { \omega } - l _ { u } ) ]$

## IV. LENGTH-CORRECTION MULTIPLE REGRESSION NEURAL NETWORK

In order to restore the ADU length, we propose a LC-MRNN model, which takes the spliced TLS segment length sequence as input and restores each value to the real ADU length in the sequence.

## A. LC-MRNN Overview

The essence of ADU length restoration is to convert one length sequence into another length sequence, and the two length sequences can be equal in size. The relationship between each ADU length value in the ADU length sequence represents the relationship underlying the original data to be transmitted.

Therefore, the Markov properties between ADUs are not only reflected in the values but also in the positions of the sequences.

In an actual network environment, the HTTP header length will continue to change as the transmission progresses. In HTTP-1.1, we call this inter-flow header length variability. It refers to the effect that HTTP headers vary in length across different flows, even when the same data is transmitted. In HTTP-2.0, the presence of HPACK makes this more variable, which we call intra-flow header length variability. Through an extensive sample collection, it is found that in the vast majority of traffic, the length of ADU is much larger than the length of the HTTP header. Therefore, we restore the ADU length sequence directly from the TLS segment length sequence. Since the browser’s caching mechanism only affects the resource, there is no need to consider the impact of browser caching in this process.

In recent years, Google has proposed Transformer [51], a deep neural network architecture for machine translation in NLP, which can make good use of self-attention of the sentence for translation. The ADU restoration process can be considered as translating the spliced TLS segment length sequence into the real ADU length sequence. The relationship between length values before and after the restoration is not strictly corresponding and the values are discrete, similar to the translation problem.

Therefore, we propose a Length-Correction Multiple Regression Neural Network (LC-MRNN) algorithm based on Transformer to achieve the ADU restoration. The algorithm is shown in Fig. 4. It is worth noting that although LC-MRNN has a similar architecture to the standard Transformer, we have introduced additional local dependency-enhanced padding screening layers and hierarchical normalization strategies to adapt to the scenario where the PDU number of encrypted flow is variable. To improve computational efficiency (the embedding size is much larger than natural language), we have also introduced dynamic attention scaling and gradient clipping. Additionally, we customize and construct pad-aware loss and direction-aware filtering. Therefore, while focusing on global dependencies, we also explicitly enhance the ability to extract local features.

![](images/22c43f600175fbeefaa0032f0de9b62c9ae976508c35f436021893d171b23ce7.jpg)

Fig. 4. Neural network overview of LC-MRNN algorithm.  
![](images/6ca54508a3b69d7f4eed9d1033d4a2c3dbe0a93f5e5cabb4e5f7ec1ef592802d.jpg)  
Fig. 5. Illustration of two different length sequence encoding ways.

We first encode the input length sequence by embedding, and then, in order to reflect the position relationship between the length values, we encode the position. Then, we use the multi-head self-attention mechanism to dig into the significance and relationship between the values in the length sequence and finally restore the ADU length sequence.

Since encoding of length sequences is involved, there are two ways to do this. The first way is to encode the length value of the spliced TLS segment directly, that is, treat the length value as a numerical value. The second way is similar to the encoding in NLP, which first converts a word to an index and then encodes it. The two encoding paths are shown in Fig. 5. The specific choice of which way we further in-depth in the follow-up experiment. In this paper, we finally choose the word-to-index scheme.

## B. Application Classification Based on Restored ADU Length

ADU length sequence restoration is to improve the effect of encrypted traffic classification, so we associate ADU restoration with encrypted traffic application classification.

ADU restoration uses one model, while application classification requires another. The output of the restoration model is related to the input of the classification model. Both models have their own training and prediction stages, so it is necessary to consider what data the two models use as input in the training and prediction stages, respectively.

For LC-MRNN, its training stage requires the TLS segment length sequence and the corresponding real ADU length sequence as inputs. The real ADU length sequence is masked by encryption, so it can only be obtained by decryption. Based on the A3C system [13] in our previous research, we can effectively obtain application-level encrypted traffic with labels and only need to decrypt it to obtain the real ADU length sequence. However, since the decryption of encrypted traffic must be carried out using the key of the controllable end during visiting and requires the authorization of the visitor (involving personal privacy), it is difficult to deploy on a large scale. We call such nodes A3C core collection points.

However, for the classifier, because it only cares about classifying the input into a specific application category, it also needs a large number of labeled samples for training to cover the diversified functions and behaviors within the application. Therefore, it must be supported by a labeled dataset that can be obtained on a large scale. The A3C system without decryption does not involve any privacy issues, and its ability to deploy on a large scale without affecting normal use is also proven. Therefore, we can use many volunteered devices to obtain encrypted traffic samples corresponding to massive TLS segment length sequences and application category labels.

Due to the need to use the ADU length sequence as the input of the classifier to improve the classification effect, we choose to use the restored ADU length sequence after the LC-MRNN model as the input of the classifier (the training stage is the same as the prediction stage). It can effectively solve the problem that the two models have different emphases on input requirements.

Hence, we propose a new composite model called LC-MRNN-AC (LC-MRNN with Application Classification) for ADU restoration and encrypted traffic application classification. The model combines the LC-MRNN restorer and the classifier. As this paper does not explicitly study the classifiers, our previous work - the current state-of-the-art LS-LSTM model’s classification layer [9] is selected as a classifier (N-gram layer is deprecated). The structure and process of the LC-MRNN-AC model are shown in Fig. 6.

![](images/23239a7340f925c56dae0e876820cc2feb9b044ade0a372ab060ffe6643a390f.jpg)  
Fig. 6. The relationship between two submodels in LC-MRNN-AC and the overall deployment structure diagram.

It is worth noting that because some HTTP requests do not contain data body, the ADU length is restored to 0, which will cause certain information loss and may also affect the expression ability of the classifier. Therefore, we add a positive value to supplement to solve the problem that the input is 0 and the embedding input cannot be negative simultaneously.

## V. PERFORMANCE EVALUATION

In order to prove the methods in this paper, we carried out three stages of experiments. First, we conducted experiments to prove the significance of ADU length restoration. Then, we performed restoration experiments to prove the effectiveness of LC-MRNN. They were done in conjunction with the classification experiment, which included two different scenarios of the small world and the big world. Then, we made a deep comparison between LC-MRNN-AC and existing state-of-the-art methods in classification, including classification effect and performance cost, to prove the superiority of our method.

## A. Dataset & Experimental Settings

As this paper involves the restoration of ADU, current public datasets are difficult to support our experiment. Therefore, based on the improved A3C system [13], we collected traffic from nine mainstream web-based applications on the current Chinese Internet, covering video, e-commerce, social media, news, and other service types. Traffic samples were collected in the actual CERNET network environment from November 2021 to May 2023, and each sample has a complete encrypted flow with the corresponding ADU sequence decrypted as HTTP-1.1.

Meanwhile, to test the method’s validity under the HTTP-2.0 protocol, we collected another dataset and named it CERNET-Web-2.0. CERNET-Web-2.0 consists of 300 pages with 155194 samples (including article pages, blog pages, news pages, course pages, and resource pages) from CSDN blog website which is frequently visited in China. It is worth noting that due to the multiplexing characteristics of HTTP-2.0, the protocol is currently mainly used for website access. The two datasets will be available at https://data.iptas.edu.cn/web/tbps. The statistics of two datasets are shown in Table VI.

TABLE VI  
STATISTICS OF CERNET-1.1 DATASET AND CERNET-WEB-2.0 DATASET

<table><tr><td colspan="4">CERNET-1.1</td></tr><tr><td>Application</td><td>Number of flows</td><td>Application</td><td>Number of flows</td></tr><tr><td>Bilibili</td><td>3963</td><td>Douban</td><td>2061</td></tr><tr><td>Hupu</td><td>1565</td><td>JD</td><td>3761</td></tr><tr><td>Sohu</td><td>5150</td><td>Netease</td><td>2478</td></tr><tr><td>Sina</td><td>3195</td><td rowspan="2">Youku</td><td rowspan="2">935(3985 reformed)</td></tr><tr><td>Zhihu</td><td>4388</td></tr><tr><td colspan="4">CERNET-Web-2.0</td></tr><tr><td colspan="4">CSDN (https://www.csdn.net/)</td></tr><tr><td>Number of pages (#class)</td><td>300</td><td>Number of flows</td><td>155194</td></tr></table>

To make the experiment more practical, we conducted the experiments on a workstation cluster (the primary device is AMD 5950x + RTX 3090). Although the cluster contains devices with different computility, we ensured the computing units were consistent in each experiment.

For the experimental scenario, because the data scene classification faced is different from ADU restoration, it is inappropriate to apply the close-world and the open-world directly. Therefore, we deepen the concept of the open-world and propose smallworld scenarios and big-world scenarios.

Since this paper does not consider sample similarity measurement, we use time and cyberspace span as the distinction criteria of small-world and big-world scenarios. In terms of time, we use the year as a unit, much larger than the application version update cycle, representing the difference in application data version or function. In cyberspace, we distinguish the geographical location ofthe server cluster (obtained by querying the IP home), such as the cloud center in Beijing and Shanghai, which can effectively represent the difference in user habits.

Therefore, a small-world scenario refers to a scenario where the feature distribution of the application or data is similar. In addition, the real ADU length can be acquired by the A3C core point in a small-world scenario, as the sphere of influence is limited. On the contrary, the big-world scenario represents the data scene where the real length of the ADU cannot be effectively obtained. The data feature distribution, application type, and function are significantly different from the smallworld scenario.

![](images/26e4dfd503ea0ae0e4ce3302be80160c353c3bb02b1c2070c7368e35cd4810c7.jpg)  
Fig. 7. Convergence curves of three different PDU length sequences under three models.

TABLE VII  
COMPARISON OF THREE DIFFERENT LENGTH SEQUENCE INPUTS UNDER CERNET-1.1 HTTPS SAMPLES

<table><tr><td rowspan="2">Methods</td><td colspan="2">Packet</td><td colspan="2">Segment</td><td colspan="2">ADU</td></tr><tr><td>Pr</td><td>Rc</td><td>Pr</td><td>Rc</td><td>Pr</td><td>Rc</td></tr><tr><td>LS-LSTM</td><td>0.6912</td><td>0.6232</td><td>0.9372</td><td>0.9362</td><td>0.9761</td><td>0.9728</td></tr><tr><td>LS-CapsNet</td><td>0.6664</td><td>0.3323</td><td>0.8512</td><td>0.8505</td><td>0.8780</td><td>0.8771</td></tr><tr><td>FS-Net</td><td>0.6649</td><td>0.4938</td><td>0.8999</td><td>0.8964</td><td>0.9504</td><td>0.9477</td></tr></table>

Before the experiments, we divided the two datasets into 60% small-world dataset and 40% big-world dataset according to the time and server IP of sample data collection. The small-world dataset is used for LC-MRNN model training and testing, and the big-world dataset is not used for training. The big-world dataset is only used for the testing of models trained by small-world datasets.

## B. ADU Restoration Significance Experiment

As ADU serve for encrypted traffic classification in practical, we conducted a controlled experiment to prove the ADU length sequence’s optimization effect on encrypted traffic classification. Classifiers used for the experiment include LS-LSTM [9], LS-CapsNet [45], and FS-Net [8], which are currently the most representative encrypted traffic classification models based on length sequence.

When the input size is limited to 24, the full traffic classification results under CERNET-1.1 dataset are shown in Table VII (Pr represents precision and Rc is Recall).

Taking the amount of input packet counts as the independent variable (it is worth noting that since traffic is collected in the packet granularity and TLS Segment and ADU are spliced on packets, the packet is taken as the input unit), we further conducted experiments on the classification effects of three different PDUs under LS-LSTM in this scenario.

In addition, to prove the advantages of ADU length sequence in model training, we evaluated the convergence experiments under the three models based on a fixed number of input TCP packets of 800, as shown in Fig. 7.

![](images/885feaedb132db0391c1c52f5a1d0a3b93955e842595cc1ac18de1c53b134378.jpg)  
Fig. 8. Count distribution of adjacent ADU length interval.

This figure shows that the ADU length sequence features a faster convergence speed. In LS-CapsNet, the continuous oscillation is caused by the specialty of the model itself (CapsNet uses dynamic routing instead of gradient descent). The overall results demonstrate that the ADU length sequence has the best effect, which further verifies the effectiveness and necessity of ADU restoration.

## C. Small-World LC-MRNN Superiority Experiment With Numerical Encoding

After determining the necessity of restoration, we conducted experiments on the effect of the LC-MRNN algorithm on the small-world dataset. We selected six representative applications of HTTP-1.1 with relatively uniform length distribution and similar ADU length values (which are more challenging to restore accurately) for the LC-MRNN restoration experiment. In the meantime, we first experimented with numerical coding.

Since the theoretical maximum length of ADU is infinite, and sequences are embedded in the LC-MRNN algorithm, the vast ADU size will also cause a colossal memory occupation for the model. Therefore, we first made statistics on the size of adjacent intervals of all ADU length values in the CERNET-1.1 dataset, which are shown in Fig. 8. Since these statistics aim to find the factor of scaling, the distribution is represented as an exponential form with a base of 10.

![](images/869db95e996f5fc0e063c10dc498341485ec611ffaa4dbd80326379e8361e4ac.jpg)  
Fig. 9. Model memory size cost under different MATR after scaling.

The results show that the most ADU lengths are more than 100 bytes. Since the scaling will cause a loss of accuracy, we finally use 10 as the scaling factor to pre-compress the maximum length of ADU. When the ADU length is restored and the real ADU length is used as LC-MRNN model input, they will be scaled first and divided by 10.

Further, although we have scaled down the ADU length upper limit to one-tenth of the original size, the upper limit is still a variable. The input of the neural network requires that the upper limit of ADU length should be a certain value, and the selection of this value should balance the model’s size and effect.

Therefore, we conducted experiments to fix the maximum size of ADU, which is determined by the Maximum ADU Threshold Rate (MATR). MATR is the ratio of the chosen ADU length upper limit to the maximum value of all ADUs in the sample. The relationship between MATR (from 50% to 99%) and model size is shown in Fig. 9.

The results show that with the increase of MATR, the model’s size increases significantly, and the higher the MATR, the faster the rise. It is because an enormous ADU value is also a tiny percentage ofthe sample space, but it will greatly increase model size. Therefore, we need to limit the model size through MATR on the premise of ensuring accuracy. Otherwise, models over 1 GB are unacceptable on common traffic acquisition analysis points like gateways. Meanwhile, during the period from 50% to 80%, the accuracy rate increases significantly with the increase of MATR. The accuracy also improved from 80% to 99%, but the improvement was slight.

In order to determine the final MATR and obtain the fixed embedding size, we choose four representative MATRs from the above experimental results to carry out in-depth experiments, namely, 98%, 95%, 90%, and 80%. After we numeralize them, the four MATRs correspond to 83030, 55670, 43910, and 23450, respectively. The classification results of four MATR by LC-MRNN-AC are shown in Fig. 10.

The results show that 83030 has the fastest convergence speed with the best accuracy. Therefore, we choose 83030 as the ADU length upper limit (after scaling), and any value exceeding this length will be transformed into 83030.

On this basis, we further experiment with the restoration effect of the core LC-MRNN restoration model. The experimental results are shown in Table VIII. It is worth noting that the distance D used here is the Euclidean distance of the sequences.

TABLE VIII  
SMALL-WORLD: RESTORATION RESULT UNDER FIVE CRITERIONS

<table><tr><td></td><td> $\bar{D}$ </td><td>Max(D)</td><td> $\delta (D)$ </td><td> $r^{(0)}$ </td><td> $\beta$ </td></tr><tr><td>Douban</td><td>62.37</td><td>6266.88</td><td>469.29</td><td>0.8337</td><td>1.01</td></tr><tr><td>Hupu</td><td>654.02</td><td>14746.06</td><td>2734.17</td><td>0.9419</td><td>1.01</td></tr><tr><td>JD</td><td>12.26</td><td>9806.00</td><td>346.48</td><td>0.998</td><td>1.03</td></tr><tr><td>Sohu</td><td>161.49</td><td>19510.79</td><td>1399.10</td><td>0.9775</td><td>1.01</td></tr><tr><td>Netease</td><td>136.88</td><td>5173.19</td><td>629.99</td><td>0.94</td><td>1.05</td></tr><tr><td>Sina</td><td>47.17</td><td>9986.27</td><td>531.58</td><td>0.985</td><td>1.01</td></tr></table>

TABLE IX  
BIG-WORLD: RESTORATION RESULT UNDER FIVE CRITERIONS

<table><tr><td></td><td> $\bar{D}$ </td><td>Max(D)</td><td> $\delta (D)$ </td><td> $r^{(0)}$ </td><td> $\beta$ </td></tr><tr><td>Douban</td><td>4127.26</td><td>22531.73</td><td>4576.10</td><td>0.05916</td><td>2.61</td></tr><tr><td>Hupu</td><td>8304.84</td><td>19366.10</td><td>4638.27</td><td>0.0</td><td>3.35</td></tr><tr><td>JD</td><td>11239.79</td><td>28506.10</td><td>5736.73</td><td>0.0225</td><td>5.74</td></tr><tr><td>Sohu</td><td>10853.96</td><td>24121.22</td><td>4963.81</td><td>0.0333</td><td>3.19</td></tr><tr><td>Netease</td><td>5197.14</td><td>19900.19</td><td>3971.18</td><td>0.04416</td><td>2.49</td></tr><tr><td>Sina</td><td>9061.62</td><td>26003.59</td><td>5506.72</td><td>0.05416</td><td>2.96</td></tr></table>

Among them, $\bar { D } , M a x ( D )$ and $\delta ( D )$ refer to the average, maximum and standard variance of $D ,$ respectively. Zero rates $r ^ { ( 0 ) }$ refer to the ratio that the distance between two sequences is 0 (totally same). The higher the $r ^ { ( 0 ) }$ is, the more precise the restoration is. The restoration rate $\beta$ refers to the length ratio of the restored part to the part that should be restored. It is used to evaluate the overall restoration effect, and the restoration rate should be about 1. It can be seen from the results that the restoration effect of the small-world dataset is excellent. Although the restoration distance of a few sequences is large, almost identical restoration can be achieved on the whole.

Further, we carried out the classification experiment under the small-world dataset, and the experimental results are shown in Fig. 11.

The results show that the classification is outstanding under the small-world dataset. In other words, when there is a certain similarity between the sequence to be classified and the labeled sample sequence, it can achieve almost 100% accurate classification.

## D. Big-World LC-MRNN-AC Classification Experiment With Index Encoding

In an actual network open-world environment, a model trained in a controlled domain will likely be used nationally or globally. In the non-controllable domain, it is impossible to train LC-MRNN. Therefore, based on the LC-MRNN instance trained in small-world datasets, we use big-world datasets for restoration tests and classification experiments. The results are shown in Table IX.

There is a particular gap between this restoration result and the small-world dataset’s result. Although the average and maximum restoration distances are negligible compared with the total length, the zero rates are too low and the restoration rates are far higher than those in the small-world experiment. Therefore, if numerical coding is used, there may be problems of overreduction and insufficient accuracy in the big-world scenario, so we use index encoding instead. We name it isomorphic length-to-index. In other words, the lengths of PDU and ADU (which could contain the same value) are encoded to form two dictionaries, respectively.

![](images/78273fc131e2f4c211d7d5d60d9a9b8ec2f035b93775c9e2b66d4f4bdd328f56.jpg)  
(a)

![](images/a37aac17848324f3903b1abab4dd2597413baab449c428759812c2dfe65aa10a.jpg)  
(b)

Fig. 10. LC-MRNN-AC Classification Results with Increasing Epoch of Four MATR: (a) Accuracy, (b) Restoration Loss.  
![](images/ef9d3e3e21aec570902d7060e0f77b2ac234b846d50f0e875d179d5833626912.jpg)

![](images/dcd7272f2c6b0881b873d1b01b71b3aeaf8837a521a18214b5375f5da98e7f75.jpg)

Fig. 11. Small-world: Classification precision/recall curve and confusion matrix.  
![](images/cfd16513e567f24ca4a88f0bf36bb93c8292d78b60446b456c7a924c0e2c4f13.jpg)  
Fig. 12. Big-world: Index encoding accuracy and loss curve.

Since the brand new PDU and ADU length values will always exist in the big-world environment, we adopt the dynamic coding extension method to encode the new values continuously. For the problem that it is difficult to restore new values that have never appeared accurately, we rely on the robustness of the classifier to support it. The restoration accuracy curve of the LC-MRNN model encoded by an index is shown in Fig. 12.

It can be seen from the results that the overall restoration accuracy is not very high due to the existence of fresh values (corresponding to zero rate in numerical encoding), but it is far higher than the effect of numerical encoding. Since the purpose of restoration is ultimately classification, it is necessary to consider the effect of classification in the context of the big world.

In order to prove the universal superiority of the LC-MRNN-AC model, we compare the classification effect of the LC-MRNN-AC model with other state-of-the-art models using different feature engineering models on the big-world dataset. In order to ensure fairness, other models use their preset inputs and parameters. The models used for comparison are the most basic CNN [15] (modified to fit length sequences), SAE extracted from Deep Packet, FS-Net [8] for flow length features, LS-LSTM (without N-gram) [9] for the PDU length sequence features, GGNN [20] for the graphical packet length sequence, and miniflowpic [52] for both time and the sequence of lengths.

Firstly, we used the restored ADU length sequence for training the LS-LSTM classifier in the LC-MRNN-AC. Then, we conducted tests using the original TLS segment length sequence (LCMRNNAC-TLS-24) and the restored ADU length sequence (LCMRNNAC-RADU-24). The experimental results showed that LCMRNNAC-RADU-24 was superior to LCMRNNAC-TLS-24, which in turn was superior to LSLSTM-TLS. This proved the superiority of ADU restoration in classification. In addition, since we found that ADU restoration may lead to the existence of most 0 values in the request (HTTP request is likely to contain no data, only headers), which will cause the classifier’s poor effect to a certain extent, we proposed three feature enhancement schemes in big-world scenarios. The first is the direct addition of spliced PDU values and ADU values for calculation (Direct PDU and ADU Sum, DPAS), the second is the absolute value addition of spliced PDU values and ADU values (ABsolute PDU + ADU, ABPAS), and the third is the substitution of ADU sequences with non-zero values in the spliced PDU sequence (PDU-ADU Replacement, PAR). The results are shown in Table X.

The round-wise classification results are shown in Fig. 13.

The results show that LC-MRNN-AC has a classification effect far exceeding the existing state-of-the-art and is better than the complex and huge LS-LSTM model with the same amount of data input. The superiority of LC-MRNN-AC under HTTP-1.1 is proved.

## E. Applicability of Classification for Extremely Similar Samples Under HTTP-2.0

In addition to HTTP-1.1, HTTP-2.0 is now HTTPS’s mainstream application layer protocol. However, HTTP-2.0 is mostly used for web pages, which makes in-app confusion very serious. Therefore, we conducted experiments on the restoration performance of the LC-MRNN-AC model for HTTP-2.0 samples and its classification applicability in extremely similar sample environments under the CERNET-Web-2.0 dataset.

TABLE X  
BIG-WORLD HTTP-1.1: CLASSIFICATION RESULTS OF DIFFERENT SOTA METHODS WITH DIFFERENT PDUS AND INPUT SIZES

<table><tr><td>Classifier-PDU Layer -Input Size</td><td>Pr</td><td>Rc</td><td>F1</td><td>R-SCR</td></tr><tr><td>LeNet5-TCP-25 $^{1}$ </td><td>0.8516</td><td>0.8500</td><td>0.8450</td><td>-</td></tr><tr><td>LeNet5-TCP-36</td><td>0.8181</td><td>0.8273</td><td>0.8144</td><td>-</td></tr><tr><td>LeNet5-TCP-64</td><td>0.7834</td><td>0.7964</td><td>0.7825</td><td>-</td></tr><tr><td>LeNet5-TLS-25</td><td>0.6779</td><td>0.6853</td><td>0.6751</td><td> $1.0000^2$ </td></tr><tr><td>LeNet5-TLS-36</td><td>0.6525</td><td>0.6529</td><td>0.6506</td><td>0.8947</td></tr><tr><td>LeNet5-TLS-64</td><td>0.6981</td><td>0.7133</td><td>0.7038</td><td>0.6315</td></tr><tr><td>DPSAE-TCP-25</td><td>0.8207</td><td>0.8282</td><td>0.8204</td><td>-</td></tr><tr><td>DPSAE-TCP-50</td><td>0.7853</td><td>0.7945</td><td>0.7830</td><td>-</td></tr><tr><td>DPSAE-TCP-100</td><td>0.7761</td><td>0.7900</td><td>0.7824</td><td>-</td></tr><tr><td>DPSAE-TLS-25</td><td>0.7425</td><td>0.7416</td><td>0.7391</td><td>1.0000</td></tr><tr><td>DPSAE-TLS-50</td><td>0.7008</td><td>0.7086</td><td>0.7006</td><td>0.7368</td></tr><tr><td>DPSAE-TLS-100</td><td>0.7840</td><td>0.7950</td><td>0.7890</td><td>0.4211</td></tr><tr><td>FSNet-TCP-12 $^{3}$ </td><td>0.8322</td><td>0.8620</td><td>0.8284</td><td>-</td></tr><tr><td>FSNet-TCP-24</td><td>0.5363</td><td>0.7150</td><td>0.6129</td><td>-</td></tr><tr><td>FSNet-TCP-48</td><td>0.5597</td><td>0.6910</td><td>0.6034</td><td>-</td></tr><tr><td>FSNet-TLS-12</td><td>0.8018</td><td>0.8575</td><td>0.8284</td><td>1.0000</td></tr><tr><td>FSNet-TLS-24</td><td>0.8325</td><td>0.8856</td><td>0.8577</td><td>0.9000</td></tr><tr><td>FSNet-TLS-48</td><td>0.8395</td><td>0.8900</td><td>0.8634</td><td>0.7000</td></tr><tr><td>LSLSTM-TCP-12</td><td>0.9022</td><td>0.9027</td><td>0.9017</td><td>-</td></tr><tr><td>LSLSTM-TCP-24 $^{4}$ </td><td>0.9007</td><td>0.9009</td><td>0.8937</td><td>-</td></tr><tr><td>LSLSTM-TLS-16</td><td>0.8526</td><td>0.8530</td><td>0.8498</td><td>1.0000</td></tr><tr><td>LSLSTM-TLS-24 $^{5}$ </td><td>0.7825</td><td>0.8363</td><td>0.8084</td><td>0.9500</td></tr><tr><td>GGNN-TCP-24</td><td>0.3711</td><td>0.4155</td><td>0.3564</td><td>-</td></tr><tr><td>GGNN-TCP-48</td><td>0.5357</td><td>0.6282</td><td>0.5650</td><td>-</td></tr><tr><td>GGNN-TCP-72</td><td>0.5887</td><td>0.6564</td><td>0.5927</td><td>-</td></tr><tr><td>GGNN-TLS-24</td><td>0.4460</td><td>0.4247</td><td>0.3620</td><td>1.0000</td></tr><tr><td>GGNN-TLS-48</td><td>0.5448</td><td>0.4857</td><td>0.4139</td><td>0.7368</td></tr><tr><td>GGNN-TLS-72</td><td>0.5219</td><td>0.4873</td><td>0.4416</td><td>0.5789</td></tr><tr><td>miniflowpic-TCP $^{6}$ </td><td>0.1651</td><td>0.4064</td><td>0.2348</td><td>1.0000</td></tr><tr><td>miniflowpic-TLS $^{6}$ </td><td>0.7396</td><td>0.7232</td><td>0.7042</td><td>1.0000</td></tr><tr><td>miniflowpic-ADU $^{6}$ </td><td>0.0937</td><td>0.3062</td><td>0.1435</td><td>1.0000</td></tr><tr><td>LCMRNNAC-RADU-24</td><td>0.9317</td><td>0.9304</td><td>0.9306</td><td>1.0000</td></tr><tr><td>LCMRNNAC-TLS-24</td><td>0.9126</td><td>0.9120</td><td>0.9117</td><td>1.0000</td></tr><tr><td>LCMRNNAC-DPAS-24</td><td>0.9330</td><td>0.9320</td><td>0.9320</td><td>1.0000</td></tr><tr><td>LCMRNNAC-ABPAS-24</td><td>0.9358</td><td>0.9350</td><td>0.9352</td><td>1.0000</td></tr><tr><td>LCMRNNAC-PAR-24 $^{7}$ </td><td>0.8568</td><td>0.8570</td><td>0.8566</td><td>1.0000</td></tr></table>

1 To ensure that pooling is equivalent to the lengths of different positions, we choose the square matrix and kernel, so the input size must be a square number.  
2 The baseline of RSCR is the maximum number of samples of input size in the current PDU layer.  
3Both FS-Net and LS-LSTM classifiers can accommodate smaller input sizes, so the initial value is 12, slightly larger than the 10 cells of the standard TCP 3-way handshake and TLS 7-way handshake in TLS-1.2.  
4 LS-LSTM has the phenomenon of mode collapse when the input size is larger than 24, which may be due to the gradient explosion caused by the limited bearing capacity of the N-gram or too-large embedding size.  
5 Different from LCMRNNAC-TLS-24, although both cases use LS-LSTM as the classifier, LSLSTM-TLS-24 directly uses TLS segment length sequence for training and testing, while LCMRNNAC-TLS-24 uses the restored ADU length sequence for training and uses spliced TLS segment length sequence for testing  
6 In the training process of miniflowpic, the issue of class collapse emerges. Leveraging the augmentation mechanism inherent in the method, when the input PDU is TLS segment, this problem shows improvement after approximately 30 epochs. Nevertheless, for the other two types of PDUs, even with an elevated learning rate, this situation remains unmitigated.  
7 LCMRNNAC-PAR-24 has a high training and low test accuracy, with a difference of more than 10%.

This is an extremely difficult classification scenario because the data length changes every time we access it and the number of classes is large. Moreover, the pages on the same website are very similar, each sequence is very short, and the PDU sequence that does not meet the input requirements is aligned by filling in 0. In addition, using encrypted traffic application classification classifiers for web page classification can better reflect the generalization ability of the architecture. It is worth noting that due to the nature of HTTP-2.0, the distributed correlation between the training set and the test set generated by random partitioning will be weak.

![](images/2d1a79d1b63fbbc13e8e0f3570104994380643146fa2597ee4ddddebc45076e6.jpg)  
Fig. 13. Big-world HTTP-1.1: Comparison of state-of-the-art methods with different input features.

![](images/0e0958abfb0cb52baf929dafa0868f6bb386f81787a9f7da6dffe58d167f6208.jpg)  
Fig. 14. Big-world HTTP-2.0: Convergence Curves of Loss and Test Accuracy of LC-MRNN restorer.

First, we conducted a restoration effect experiment, and the experimental results are shown in Fig. 14. The training and test sets still follow the 60% vs. 40% rule of the big and small worlds.

The results show that even with the existence of multiplexing and HPACK head compression, which seriously interfere with the ADU length restoration, the LC-MRNN model can still realize the ADU restoration of HTTP-2.0 protocol encrypted traffic, and the restoration accuracy is even higher than that of HTTP-1.1.

On this basis, we also compared the LC-MRNN-AC model with the control group used in HTTP-1.1, and the experimental results are shown in Fig. 15.

Results show that the classification effect is not good, no matter what kind of classifier, which is as expected. There are three main reasons. First, the structural design of the above classifier is not for the unified website webpage classification but for the broad category of applications. Second, HTTP-2.0 header compression and multiplexing significantly impact the characteristics of different web pages visited within the website, and the distribution of training sets and test sets is inconsistent. Third, the number of classification categories is about fifty times that of the application, which may exceed the upper limit of the current classifier hyperparameters. However, it can be clearly seen from the results that the training accuracy of the LC-MRNN-AC model has been improving, indicating that the ADU length restoration still has obvious significance under HTTP-2.0. It can effectively extract stable ADU length sequence features from unstable TLS Segment length sequences (features used by other classifiers). The significance of ADU restoration and ALFE is further proved.

![](images/2b7366981ecd8f984f73f3a41ce2d842aa4202a666006613c915e290587b8bcb.jpg)  
Fig. 15. Big-world HTTP-2.0: Extreme classification convergence curves of five methods.

![](images/680c9da606bc7dd6db4b510f3004134b826b62e3157265e399c53576f8e5c488.jpg)  
Fig. 16. Memory usage of different models under HTTP-1.1 data.

## F. LC-MRNN-AC Performance Overhead Experiment

Since the LC-MRNN-AC model is very complex, especially the LC-MRNN itself, it is necessary to conduct experiments on its performance overhead to consider its applicability and suitable scenarios in the actual network environment.

First, we experimented on memory usage, and the experimental results are shown in Fig. 16.

It can be seen from the results that LC-MRNN-AC has no obvious advantage in memory occupancy due to the use of transformer architecture (restorer) and huge embedding (classifier), which even consumes more resources to some extent. This is mainly because the Transformer is a complex and large architecture, and LC-MRNN-AC consists of two models. However, the two models can be deployed separately in the engineering implementation to reduce the resource overhead.

![](images/d027a3ee554e7200ddfd91466ee1333e8d4c2d2616b2688404089d75fdd39b36.jpg)  
Fig. 17. Training time cost of different models under HTTP-1.1 data.

Then, we experimented on the training time of the overall encrypted traffic classification, and the experimental results are shown in Fig. 17.

As can be seen from the results, the training time of the classifier in LC-MRNN-AC has obvious advantages. With far better results than other classifiers, it has less training time (the model structure is simpler). This is due to the characteristic advantages brought by ADU restoration, which is consistent with the theoretical analysis in Section III.

However, it is worth noting that the training time of the LC-MRNN-AC restorer (LC-MRNN) model is relatively high, requiring 3714.1659 seconds to complete the training of 200 epochs in a single workstation and completing convergence in about 170 epochs. Because there is no free lunch in the classification task, however, the asynchronous separation deployment and the separation of big and small world datasets that LC-MRNN-AC relies on, in practical applications, the training cost of LC-MRNN reducers will not affect the classification (offline advance payment).

## G. Analysis & Discussion

1) Why is the ADU Length Sequence Restored From the Big-World Dataset Used as the Input of the Classification Model?: A labeled sample dataset with a decrypted HTTP plaintext data counterpart to the encrypted traffic is extremely challenging to obtain compared to an encrypted traffic dataset with only category labels. As a result, if a real ADU length sequence is used, the training and retraining process will be restricted by the amount of data, and the toughness to obtain enough samples will lead to a poor effect.

Although our LC-MRNN sequence is designed to restore the encrypted traffic length sequence into a real ADU length sequence as accurately as possible, the precise restoration requires similar features with a high degree found in the experiment. It is not realistic to acquire a large enough dataset of real ADU length sequences to cover all the scenarios of the applications. Coupled with the difference in the network environment and the rapid iteration of application, concept drift is more likely to occur.

By comparing small-world datasets with big-world datasets in experiments, we find that since the ultimate goal of restoration is classification, the problem of concept drift can be transferred from the restorer to the classifier. Compared with the restorer, the negative effect caused by concept drift can be suppressed by the classifier’s insensitivity to hits. Moreover, obtaining ADU length sequence labeled samples is more accessible after restoration. As an alternative, a restored ADU length sequence as the classifier’s input can significantly decrease the difficulty of classifier training by giving the classifier sufficient samples, which is also helpful in dealing with concept drift.

TABLE XI  
COMPARISON OF THREE ADU LENGTH SEQUENCES AS INPUT

<table><tr><td>Labeled PDU length sequence</td><td>Real ADU</td><td>Small-world restored ADU</td><td>Big-world restored ADU</td></tr><tr><td>Labeled sample acquire difficulty</td><td>Extremely challenging</td><td>Generally difficult</td><td>Relatively easy</td></tr><tr><td>Classification effect (average accuracy)</td><td>99%</td><td>99%</td><td>97%</td></tr><tr><td>Ability to cope with concept drift</td><td>Weak</td><td>Normal</td><td>Strong</td></tr><tr><td>Privacy or security risks exist</td><td>Yes</td><td>No</td><td>No</td></tr><tr><td>LC-MRNN algorithm required</td><td>No</td><td>Yes</td><td>Yes</td></tr></table>

In this paper, though, the big-world dataset is derived from the CERNET-1.1 dataset same as the small-world dataset, which has the corresponding decrypted HTTP data. However, in the LC-MRNN-AC model, its plaintext counterpart is not used. So this experiment is representative. The big-world dataset at the moment is a good representation of easily accessible labeled sample data using A3C normal nodes. The qualitative comparison was made among the three, as shown in Table XI.

2) Why is the ADU Restoration Accuracy Rate ofHTTP-2.0 Protocol With Many Interference Technologies Higher Than That of HTTP-1.1?: HTTP-2.0 should theoretically be more challenging to restore than HTTP-1.1 because it has a more complex protocol structure. However, in practice, because the header and data body of HTTP-2.0 are transmitted separately, even if they are out of order, they are separated, which brings the possibility of direct accurate restoration to some samples in non-multiplexing cases. On the other hand, CERNET-Web-2.0 datasets are all Web traffic, and the ADU of Web traffic is far less than the average value of conventional applications in terms of the overall distribution, especially compared with multimedia applications with extremely large data volumes. Therefore, the coding space of HTTP-2.0 is relatively small, and thus, better restoration accuracy is obtained.

3) Is It Worthwhile to Optimize the Input Using the LC-MRNNModel in Order to Improve the Precision and Recall Rate byAbout 4.2%?: It is worth it. The LS-LSTM model can achieve 89% F1-score under TLS segment length sequence. However, encrypted traffic classification is a massive data supervised learning problem (backbone Tbps level). In this situation, the number of flows to be classified can be in the billion range, and a four percent improvement might correspond to millions of correctly classified samples. The accurate classification of encrypted traffic is an essential basis for ISP network management and network security decision, which is of great economic value and security protection significance. All it costs is a little extra computing resource.

4) What are the Advantages and Disadvantages of Index Encoding?: The most significant advantage of index encoding is that it can achieve more accurate restoration in the big-world environment because after index encoding, the original length value no longer has a numerical adjacency relationship, and the restorer can pay more attention to the sequence context. In addition, index encoding does not need to take into account the effects of MATR because no matter how large, the value is converted to an equal-length alternative encoding. However, conversely, this is also the potential disadvantage of index encoding compared to numerical encoding. First, index encoding needs to consume more encoding space when the length value distribution is relatively dense, and the encoding codex itself needs to be stored, occupying additional memory. Second, index encoding does not solve the problem of values that have not occurred, which is also a dilemma often encountered in NLP translation. It is more common in encrypted traffic and can only be achieved by adding encodings, negatively impacting restoration. Third, the length sequence is different from the text sequence, and there is a similar relationship between the length values; the similar values are theoretically beneficial for classification. Index encoding ignores this feature, which results in a loss of information gain to some extent. Therefore, the coding method is also a key area worthy of further study.

5) Why Do the Effects of LCMRNNAC-DPAS-24 and LCMRNNAC-ABPAS-24 Turn Out to Be Better Than Those of LCMRNNAC-RADU-24?: The experimental results of Table X show that some augmentation methods have achieved a further improvement in classification performance compared to using only the restored ADU. This indicates that although TLS segment contains less information gain than ADU, there is a slight difference in the information coverage provided by the two. This suggests that in some cases, the network performance parameters contained in the TLS segment fragments and the HTTP header length hidden in the data may also have some effect on classification. This situation has also been indirectly demonstrated in the papers using time interval sequences for classification. This is also one of the reasons why miniflowpic can function under the TLS segment length sequence.

6) Why Choose the Transformer Architecture Instead of Other Models That are More Suitable for Local Dependencies?: The variation of TLS segment length is mainly determined by local dependencies, especially in multimedia transmission scenarios. However, in practical applications, many TLS segment lengths do not reach the maximum value. At the same time, the length variation of variable-length HTTP headers is globally dependent (the global correlation of HTTP parameters) and even has dependency relationships in multiple visits (application cookies), and this phenomenon is more obvious in HTTP-2.0 (with the HPACK compression mechanism). Therefore, considering these two situations, we chose the Transformer architecture to build our restorer. It is undeniable that Transformer, as a heavyweight architecture, has a large training cost for LC-MRNN. However, with the optimization of our model architecture, this cost is acceptable (it can run on consumer-grade graphics cards ranging from 3090 to 4090). At the same time, due to the architectural advantages of LC-MRNN-AC, it can be used for a long time after training and reduces the long-term cost.

7) Is ADU Suitable for QUIC? What are the Difficulties in Using ADU Under QUIC?: Since ADU is oriented towards the data being transmitted, it can be used for classifying QUIC encrypted traffic. However, QUIC encrypts more metadata and has two formats of long and short headers. Moreover, more variable-length fields and binary encoding modes make the systematic error less. Specifically, for the long header, there are 9 bytes in total, including the header form (1 byte), fixed bit (1 byte), packet number (at least 1 byte), long packet type (2 bytes), and version (4 bytes). For the short header, there are only 3 bytes, including the headerform,fixed bit, andpacket number. Nevertheless, it still has a relatively stable header structure that can support the restoration process.

In addition, the implications of QUIC streams and HTTP frames are different. Although QUIC does not, like HTTP-2.0, introduce an additional binary framing layer, streams and multiplexing on top of the TCP mechanism, it directly implements streams, and each QUIC connection can carry multiple independent streams, with each stream handling one request-response interaction. Nicely, its stream ID (connection ID) is in plaintext, and the number of streams currently existing in the connection can be directly known through statistics. This is also beneficial for the precise restoration of ADU.

## VI. SUMMARY AND FUTURE WORK

In this paper, we focus on the feature engineering of encryption traffic and propose a new input metric called ADU. We first propose three evaluation criteria to prove the theoretical advantages of ADU features in classifying encrypted traffic. Then, we propose the LC-MRNN algorithm to solve the problem of the real ADU length being interfered with and masked. In the next step, we deepen the open-world concept and propose big-world and small-world scenarios that more closely fit the actual Internet to prove the method’s adaptability in the real network environment. According to this setting, two datasets of application layer protocol HTTP-1.1 and HTTP-2.0 are collected respectively in the CERNET network environment. Based on the LC-MRNN algorithm, combined with the characteristics of HTTP-1.1 and HTTP-2.0 under the actual network environment, we propose the LC-MRNN-AC model. We experimented extensively with multiple angles and finally chose index encoding as the encoding method for the length sequence. The reduction experiments in big and small worlds show that LC-MRNN can restore ADU length sequences effectively. After the reduced features are used in classification experiments, the results show that the precision and recall of the proposed LC-MRNN-AC model are about 4.2% higher than that of the state-of-the-art method. Moreover, it has some advantages in memory, training time, and other performance indicators.

Future research needs to pay more attention to three points:

\- The encoding method of length sequence is very different from the conventional text sequence, which needs further study.

The webpage-oriented classifiers with more capabilities should be designed to make LC-MRNN adapt to webpage classification. The current application ofclassification classifiers does not perform well under the multi-page on the same site.

With the wide application of the QUIC (HTTP-3.0) protocol, encrypted QUIC traffic classification with ADU restoration will also become necessary research. Its challenges are inherently related to the life cycle. These challenges span multiple aspects, including the acquisition of labeled samples, the development of decryption tools, the rapid evolution of the QUIC protocol, the recombination of ADU during restoration (since QUIC functions at the packet level), and the alterations in data splitting techniques. All these areas hold significant research value.

## ACKNOWLEDGMENT

This paper is part on the topic of the encrypted traffic classification. Manuscript created March, 2023; This work was developed by the IEEE Publication Technology Department. This work is distributed under the Project Public License (LPPL) (http://www.latex-project.org/) version 1.3. A copy of the LPPL, version 1.3, is included in the base LaTeX documentation of all distributions of LaTeX released 2003/12/01 or later. The opinions expressed here are entirely that of the author. No warranty is expressed or implied. User assumes all risk.

Finally, I would like to express my deep remembrance to my beloved wife Yuying Shi, who passed away during the course of this research. Throughout my life and work, she provided me with unwavering support, understanding, and encouragement, which were a tremendous source of strength for me. Her influence is deeply embedded in this work. May she rest in peace.

## REFERENCES

[1] J. Muehlstein et al., “Analyzing HTTPs encrypted traffic to identify user’s operating system, browser and application,” in Proc. 14th IEEE Annu. Consum. Commun. Netw. Conf., 2017, pp. 1–6.

[2] Google, “HTTPS encryption on the web–Google Transparency Report,” 2023. [Online]. Available: https://transparencyreport.google.com/https/ overview

[3] S. Xu, G. Geng, X. Jin, D. Liu, and J. Weng, “Seeing traffic paths: Encrypted traffic classification with path signature features,” IEEE Trans. Inf. Forensics Secur., vol. 17, pp. 2166–2181, 2022.

[4] B. Yang and D. Liu, “Research on network traffic identification based on machine learning and deep packet inspection,” in Proc. IEEE 3rd Inf. Technol. Netw. Electron. Automat. Control Conf., 2019, pp. 1887–1891.

[5] P. Velan, M. Cermák, P. <sup>ˇ</sup> Celeda, and M. Drašar, “A survey of methods <sup>ˇ</sup> for encrypted traffic classification and analysis,” Networks, vol. 25, no. 5, pp. 355–374, Sep. 2015.

[6] G. Aceto, D. Ciuonzo, A. Montieri, A. Nascita, and A. Pescapé, “Encrypted multitask traffic classification via multimodal deep learning,” in Proc. IEEE Int. Conf. Commun., 2021, pp. 1–6.

[7] S. Li, H. Guo, and N. Hopper, “Measuring information leakage in website fingerprinting attacks and defenses,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Toronto, ON, Canada, 2018, pp. 1977–1992, doi: 10.1145/3243734.3243832.

[8] C. Liu, L. He, G. Xiong, Z. Cao, and Z. Li, “FS-net: A flow sequence network for encrypted traffic classification,” in Proc. IEEE Conf. Comput. Commun., 2019, pp. 1171–1179.

[9] Z. Chen, G. Cheng, Z. Xu, S. Guo, Y. Zhou, and Y. Zhao, “Length matters: Scalable fast encrypted internet traffic service classification based on multiple protocol data unit length sequence with composite deep learning,” Digit. Commun. Netw., vol. 8, no. 3, pp. 289–302, 2021.

[10] H. Wu, L. Wang, G. Cheng, and X. Hu, “Mobile application encryption traffic classification based on TLS flow sequence network,” in Proc. IEEE Int. Conf. Commun. Workshops, 2021, pp. 1–6.

[11] Z. Chen, G. Cheng, Z. Wei, Z. Xu, N. Fu, and Y. Zhou, “Higher layers, better results: Application layer feature engineering in encrypted traffic classification,” in Wireless Algorithms, Systems, and Applications. Cham, Switzerland: Springer, 2022, pp. 548–556.

[12] R. Dubin, A. Dvir, O. Pele, and O. Hadar, “I know what you saw last minute—encrypted HTTP adaptive video streaming title classification,” IEEE Trans. Inf. Forensics Secur., vol. 12, no. 12, pp. 3039–3049, Dec. 2017.

[13] Z. Chen, G. Cheng, Z. Xu, K. Xu, Y. Shan, and J. Zhang, “A3C system: One-stop automated encrypted traffic labeled sample collection, construction and correlation in multi-systems,” Appl. Sci., vol. 12, no. 22, 2022. [Online]. Available: https://www.mdpi.com/2076-3417/12/22/11731

[14] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and vpn traffic using time-related,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016, pp. 407–414.

[15] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted traffic classification with one-dimensional convolution neural networks,” in Proc. IEEE Int. Conf. Intell. Secur. Informat., 2017, pp. 43–48.

[16] F. Al-Obaidy, S. Momtahen, M. Hossain, and F. Mohammadi, “Encrypted traffic classification based ml for identifying different social media applications,” in Proc. IEEE Can. Conf. Elect. Comput. Eng., 2019, pp. 1–5.

[17] H. Yao, C. Liu, P. Zhang, S. Wu, C. Jiang, and S. Yu, “Identification of encrypted traffic through attention mechanism based long short term memory,” IEEE Trans. Big Data, vol. 8, no. 1, pp. 241–252, Feb. 2012.

[18] M. Song, J. Ran, and S. Li, “Encrypted traffic classification based on text convolution neural networks,” in Proc. IEEE 7th Int. Conf. Comput. Sci. Netw. Technol., 2019, pp. 432–436.

[19] S. Cui, B. Jiang, Z. Cai, Z. Lu, S. Liu, and J. Liu, “A session-packetsbased encrypted traffic classification using capsule neural networks,” in Proc. IEEE 21st Int. Conf. High Perform. Comput. Commun.; IEEE 17th Int. Conf. Smart City; IEEE 5th Int. Conf. Data Sci. Syst., 2019, pp. 429–436.

[20] Z. Chen, G. Cheng, D. Niu, X. Qiu, Y. Zhao, and Y. Zhou, “WFF-EGNN: Encrypted traffic classification based on weaved flow fragment via ensemble graph neural networks,” IEEE Trans. Mach. Learn. Commun. Netw., vol. 1, pp. 389–411, 2023.

[21] Y. Zhang, S. Zhao, J. Zhang, X. Ma, and F. Huang, “STNN: A novel TLS/SSL encrypted traffic classification system based on stereo transform neural network,” in Proc. IEEE 25th Int. Conf. Parallel Distrib. Syst., 2019, pp. 907–910.

[22] Y. Zeng, Z. Qi, W. Chen, and Y. Huang, “Test: An end-to-end network traffic classification system with spatio-temporal features extraction,” in Proc. IEEE Int. Conf. Smart Cloud, 2019, pp. 131–136.

[23] G. Aceto, D. Ciuonzo, A. Montieri, V. Persico, and A. Pescapé, “Know your Big Data trade-offs when classifying encrypted mobile traffic with deep learning,” in Proc. Netw. Traffic Meas. Anal. Conf., 2019, pp. 121–128.

[24] W. Maonan, Z. Kangfeng, X. Ning, Y. Yanqing, and W. Xiujuan, “Centime: A direct comprehensive traffic features extraction for encrypted traffic classification,” in Proc. IEEE 6th Int. Conf. Comput. Commun. Syst., 2021, pp. 490–498.

[25] X. Hu, C. Gu, F. Wei, and C.-H. Chen, “CLD-Net: A network combining CNN and LSTM for internet encrypted traffic classification,” Sec. Commun. Netw., vol. 2021, Jan. 2021, Art. no. 9835476, doi: 10.1155/2021/5518460.

[26] B. Lu, N. Luktarhan, C. Ding, and W. Zhang, “ICLSTM: Encrypted traffic service identification based on inception-LStM neural network,” Symmetry, vol. 13, no. 6, 2021, Art. no. 1080. [Online]. Available: https: //www.mdpi.com/2073-8994/13/6/1080

[27] G. Xie, Q. Li, and Y. Jiang, “Self-attentive deep learning method for online traffic classification and its interpretability,” Comput. Netw., vol. 196, 2021, Art. no. 108267. [Online]. Available: https://www.sciencedirect. com/science/article/pii/S1389128621002930

[28] X. Ren, H. Gu, and W. Wei, “Tree-RNN: Tree structural recurrent neural network for network traffic classification,” Expert Syst. Appl., vol. 167, 2021, Art. no. 114363. [Online]. Available: https://www.sciencedirect. com/science/article/pii/S0957417420310435

[29] Z. Song et al., “I <sup>2</sup> RNN: An incremental and interpretable recurrent neural network for encrypted traffic classification,” IEEE Trans. Dependable Secure Comput., early access, doi: 10.1109/TDSC.2023.3245411.

[30] Y. Chen, T. Zang, Y. Zhang, Y. Zhou, L. Ouyang, and P. Yang, “Incremental learning for mobile encrypted traffic classification,” in Proc. IEEE Int. Conf. Commun., 2021, pp. 1–6.

[31] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescapé, “XAI meets mobile traffic classification: Understanding and improving multimodal deep learning architectures,” IEEE Trans. Netw. Service Manag., vol. 18, no. 4, pp. 4225–4246, Dec. 2021.

[32] Y. Li, Y. Lu, and S. Li, “Ezac: Encrypted zero-day applications classification using CNN and k-means,” in Proc. IEEE 24th Int. Conf. Comput. Supported Cooperative Work Des., 2021, pp. 378–383.

[33] J. Zhang, J. Zhou, and N. Zhou, “Network traffic classification method based on subspace triple attention mechanism,” in Proc. 3rd Int. Conf. Inf. Sci. Parallel Distrib. Syst., 2022, pp. 312–316.

[34] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescapé, “Improving performance, reliability, and feasibility in multimodal multitask traffic classification with XAI,” IEEE Trans. Netw. Service Manag., vol. 20, no. 2, pp. 1267–1289, Jun. 2023.

[35] G. Bovenzi, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescapé, “A Big Data-enabled hierarchical framework for traffic classification,” IEEE Trans. Netw. Sci. Eng., vol. 7, no. 4, pp. 2608–2619, 4th Quarter 2020.

[36] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, “Learning under concept drift: A review,” IEEE Trans. Knowl. Data Eng., vol. 31, no. 12, pp. 2346–2363, Dec. 2019.

[37] V. F. Taylor, R. Spolaor, M. Conti, and I. Martinovic, “Robust smartphone app identification via encrypted network traffic analysis,” IEEE Trans. Inf. Forensics Secur., vol. 13, no. 1, pp. 63–78, Jan. 2018.

[38] M. Korczy´nski and A. Duda, “Markov chain fingerprinting to classify encrypted traffic,” in Proc. IEEE Conf. Comput. Commun., 2014, pp. 781–789.

[39] M. Shen, M. Wei, L. Zhu, and M. Wang, “Classification of encrypted traffic with second-order markov chains and application attribute bigrams,” IEEE Trans. Inf. Forensics Secur., vol. 12, no. 8, pp. 1830–1843, Aug. 2017.

[40] C. Liu, Z. Cao, Z. Li, and G. Xiong, “LaFFT: Length-aware FFT based fingerprinting for encrypted network traffic classification,” in Proc. 2018 IEEE Symp. Comput. Commun., 2018, pp. 1–6.

[41] C. Liu, Z. Cao, G. Xiong, G. Gou, S.-M. Yiu, and L. He, “MaMPF: Encrypted traffic classification based on multi-attribute markov probability fingerprints,” in Proc. IEEE/ACM 26th Int. Symp. Qual. Service, 2018, pp. 1–10.

[42] C. Dong, C. Zhang, Z. Lu, B. Liu, and B. Jiang, “Cetanalytics: Comprehensive effective traffic information analytics for encrypted traffic classification,” Comput. Netw., vol. 176, 2020, Art. no. 107258. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1389128619309466

[43] X. Yun, Y. Wang, Y. Zhang, C. Zhao, and Z. Zhao, “Encrypted TLS traffic classification on cloud platforms,” IEEE/ACM Trans. Netw., vol. 31, no. 1, pp. 164–177, 2023.

[44] G. Aceto, G. Bovenzi, D. Ciuonzo, A. Montieri, V. Persico, and A. Pescapé, “Characterization and prediction of mobile-app traffic using markov modeling,” IEEE Trans. Netw. Service Manag., vol. 18, no. 1, pp. 907–925, Mar. 2021.

[45] Z. Chen, G. Cheng, B. Jiang, S. Tang, S. Guo, and Y. Zhou, “Length matters: Fast internet encrypted traffic service classification based on multi-PDU lengths,” in Proc. 16th Int. Conf. Mobility Sens. Netw., 2020, pp. 531–538.

[46] W. Chen, F. Lyu, F. Wu, P. Yang, G. Xue, and M. Li, “Sequential message characterization for early classification of encrypted internet traffic,” IEEE Trans. Veh. Technol., vol. 70, no. 4, pp. 3746–3760, Apr. 2021.

[47] X. Wang, S. Chen, and J. Su, “App-net: A hybrid neural network for encrypted mobile traffic classification,” in Proc. IEEE Conf. Comput. Commun. Workshops, 2020, pp. 424–429.

[48] M. Shen, J. Zhang, L. Zhu, K. Xu, and X. Du, “Accurate decentralized application identification via encrypted traffic analysis using graph neural networks,” IEEE Trans. Inf. Forensics Secur., vol. 16, pp. 2367–2380, 2021.

[49] Z. Chen, G. Cheng, Z. Wei, D. Niu, and N. Fu, “Classify traffic rather than flow: Versatile multi-flow encrypted traffic classification with flow clustering,” IEEE Trans. Netw. Service Manag., vol. 21, no. 2, pp. 1446–1466, Apr. 2024.

[50] Y. Cao, Y. Feng, H. Wang, X. Xie, and S. K. Zhou, “Learning to sketch: A neural approach to item frequency estimation in streaming data,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 46, no. 11, pp. 7136–7153, Nov. 2024.

[51] A. Vaswani et al., “Attention is all you need,” in Proc. 31st Int. Conf. Neural Inf. Process. Syst., Red Hook, NY, USA: Curran Associates Inc., 2017, pp. 6000–6010.

[52] E. Horowicz, T. Shapira, and Y. Shavitt, “A few shots traffic classification with mini-flowpic augmentations,” in Proc. 22nd ACM Internet Meas. Conf., Nice, France, 2022, pp. 647–654, doi: 10.1145/3517745.3561436.

![](images/c8792679ed43aae64adc6fc908a7683a4d517afc64842c0dca724afb799fe1f1.jpg)

Yuyu Zhao (Member, IEEE) received the BS degree in software engineering from the Nanjing University of Science and Technology in 2016, and the MS and PhD degrees in cyber security from Southeast University, Nanjing, China, in 2019 and 2023, respectively. He is a currently a lecturer with the School of Cyber Science and Engineering, Southeast University. His research interests include in-band telemetry, blockchain, and network processors.

![](images/e34fac2cabebc447553fec34d92a9bf2fb4c0a505db76249642772c36703473d.jpg)

Zihan Chen (Member, IEEE) received the BS degree in software engineering from Central South University in 2017, and the PhD degree in cyber security from Southeast University in 2023. He is currently working as a postdoc with the School of Cyber Science and Engineering at Southeast University. His major research interests include cyber security, encrypted traffic classification, encrypted traffic feature engineering, and deep learning. He is a Member of CCF and works as a reviewer for multiple Journals such as IEEETransactions on Dependable andSecure

Computing, IEEE Internet of Things Journal, ESWA and the duty editor of the Journal ofCyberspace.

![](images/644e77ffcd527ef7041e731ea39ca2dc2c7ce8c80a7fe532da44a5b416600eb8.jpg)

![](images/2c893b19d3dc271313baac19a57f100049dbfb739e2fff5786a0cdee0feead58.jpg)

Guang Cheng (Member, IEEE) received the BS degree in traffic engineering from Southeast University in 1994, the MS degree in computer application from the Hefei University of Technology in 2000, and the PhD degree in computer network from Southeast University in 2003. He is a full professor with the School of Cyber Science and Engineering, Southeast University, Nanjing, China. He has authored or coauthored seven monographs and more than 100 technical papers, including top journals and top conferences. His research interests include network security, network

Yuyang Zhou (Member, IEEE) received the BS degree in electronic information engineering from the Nanjing University of Science and Technology in 2016 and the PhD degree in cyberspace security from Southeast University in 2021. He is currently working as a postdoc with the School of Cyber Science and Engineering, Southeast University. His major research interests include moving target defense, DDoS mitigation, security modeling, intrusion detection, and Android malware detection. He has published in some of the topmost journals and conferences like

IEEE Transactions on Information Forensics and Security, IEEE Transactions on Industrial Informatics, and ACM Computing Classification System, and is involved as reviewer and in technical program committees of several journals and conferences in the field.

measurement, and traffic behavior analysis. He is a senior member of CCF.

![](images/25a36c14cda718205467c26eedd021b107ee1b9eb8f778a341c0a32d59248b6d.jpg)

Dandan Niu (Student Member, IEEE) received the BS degree in Internet of Things from Jiangnan University in 2021. She is currently working toward the MS degree in cyberspace security with the School of Cyber Science and Engineering, Southeast University. Her major research interests include cyber security, encrypted traffic analysis.

![](images/431ec565c0b90338b635d0dba105d2b30710eeb57a4ff07006a7be93a820f91d.jpg)

Shanqing Jiang (Member, IEEE) received the BS degree in Internet of Things engineering from North China Electric Power University in 2017 and the PhD degree in cyber security from Southeast University in 2023. He is currently a research associate with Purple Mountain Laboratories, Nanjing, China. His research interests include SDN, future network architecture, and network resilience.
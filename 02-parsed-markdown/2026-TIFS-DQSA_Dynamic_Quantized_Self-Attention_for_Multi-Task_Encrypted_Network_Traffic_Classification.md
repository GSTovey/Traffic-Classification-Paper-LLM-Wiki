# DQSA: Dynamic Quantized Self-Attention for Multi-Task Encrypted Network Trafic Classification

Yongming Chen , Graduate Student Member, IEEE, Hongsheng Lan, Bah Hwee Gwee , Senior Member, IEEE, Qi Cao , Sirajudeen Gulam Razul , and Zhiping Lin , Life Senior Member, IEEE

Abstract—Network trafic classification is crucial for both network security and management. Despite advances in deep learning-based multi-task trafic classification, existing models often struggle to jointly handle multiple tasks while providing interpretable insights. In multi-task scenarios, diferent tasks rely on distinct regions of the trafic sequence, motivating the use of dynamic and interpretable attention mechanisms. To this end, we propose Dynamic Quantized Self-Attention (DQSA), a unified framework specifically designed for multi-task network trafic classification. At its core, the Task Gated Attention Router (TGAR) dynamically associates attention heads with diferent tasks, enabling adaptive focus on task-specific patterns. This mechanism provides interpretable attention scores, which help analyze misclassifications and guide further model refinement. To improve eficiency and handle diverse network trafic features, we introduce the Soft Quantized Self-Attention Head (SQ-SAH) to reduce computational complexity and extend the Rotary Position Embedding (RoPE) to accommodate these features. Extensive experiments on ISCX VPN-nonVPN and DCI-LTE datasets demonstrate that DQSA consistently outperforms state-of-the-art baselines, achieving 92.85% accuracy on the encapsulationlevel task of ISCX VPN-nonVPN and 93.17% accuracy on the application-level task of DCI-LTE, surpassing the strongest existing methods by up to 2.65%, while providing interpretable task-specific attention for eficient multi-task network trafic classification.

Index Terms—Trafic classification, self-attention mechanism, multi-task learning, interpretability.

## I. INTRODUCTION

agement [1]. In recent years, deep learning has significantly advanced the trafic classification field. By conducting a deep analysis of network trafic, such as Transmission Control Protocol (TCP) packet flows, various aspects of network trafic can be accurately recognized and classified. This includes the identification of malware [2], Virtual Private Network (VPN) trafic [3], and various network services and applications [4]. Naturally, this scenario lends itself to multi-task learning (MTL), where a single model can handle multiple related classification tasks simultaneously. Existing approaches, including end-to-end MTL [5] and pre-trained MTL models [6], [7], achieve promising performance. However, they often face limitations: diferent tasks may interfere with each other, and model decisions remain largely opaque, reducing interpretability in practical applications. These challenges motivate the design of a model that can dynamically capture task-specific features while providing inherently interpretable insights.

The efectiveness of deep learning in trafic classification largely stems from its ability to automatically extract complex features from raw data. However, as models grow in depth and complexity, their decision-making processes become increasingly opaque, making it dificult to identify class-discriminative patterns and undermining transparency and trustworthiness. The lack of interpretability limits their real-world applications. Moreover, understanding the decisionmaking process of a model helps identify weaknesses or biases, enabling targeted improvements. To mitigate this, various post-hoc interpretability methods have been developed and applied in the field of network trafic classification [8], [9], [10]. However, these methods may lead to increased computational overhead and potentially inaccurate explanations. This highlights the need for models that integrate interpretability into the classification process itself, eliminating dependence on post-hoc analysis and reducing the associated risks [11].

While inherent interpretability often involves a trade-of between classification performance and model transparency [12], traditional models such as decision trees or linear models provide transparent decision processes, but they often sacrifice accuracy due to their simplicity. In contrast, deep neural networks capture complex trafic patterns but remain largely opaque. Recently, the Multi-Head Self-Attention (MHSA) mechanism has gained attention for trafic classification [13], [14], since its attention weights naturally ofer interpretable insights into which parts of the sequence contribute most to predictions [15]. However, directly applying MHSA to multi-task trafic classification presents several challenges. First, incorporating fine-grained trafic features into attention analysis improves fidelity but increases the risk of overfitting due to irrelevant details [16]. Second, the quadratic complexity of MHSA with respect to sequence length raises computational and deployment costs [13]. Finally, and most importantly, existing MHSA-based approaches do not explicitly account for task-specific diferences, even though diferent tasks may depend on distinct regions of the trafic sequence. This motivates the need for a dynamic mechanism that can flexibly associate tasks with attention heads.

To address these challenges, we propose Dynamic Quantized Self-Attention (DQSA), a unified framework for multitask trafic classification. The central component is the Task Gated Attention Router (TGAR), which dynamically associates attention heads with diferent tasks. This mechanism explicitly captures both shared and task-specific patterns, improves interpretability, and enables targeted analysis of misclassifications. To enhance eficiency, inspired by [17], we design the Soft Quantization Self-Attention Head (SQ-SAH), which employs a codebook and soft quantization mechanism to constrain the hypothesis space, thereby achieving faster operation, reduced memory usage, and a lower risk of overfitting [18]. Finally, to better handle diverse network metrics, we treat all inputs as time series and enhance the Rotary Position Embedding (RoPE) [19] with a monotonic and multi-velocity variant (M2RoPE), which improves relative position modeling and adapts to trafic characteristics across diferent protocol layers. Together, these modules make DQSA both eficient and interpretable, while remaining well-suited for real-world multi-task trafic classification.

Our main contributions can be summarized as follows:

• We propose DQSA, a novel framework for multi-task traffic classification that achieves strong performance while ofering inherent interpretability.

We develop the Task Gated Attention Router (TGAR), which dynamically allocates attention heads to tasks, explicitly capturing both task-specific and shared patterns while enhancing interpretability through attention scores.

We design the Soft Quantized Self-Attention Head (SQ-SAH), which leverages a codebook and soft quantization to constrain the hypothesis space, thereby reducing the quadratic complexity of MHSA, lowering computational and memory costs, and mitigating overfitting risks.

• We extend the Rotary Position Embedding (RoPE) into a monotonic and multi-velocity variant (M2RoPE), improving relative positional modeling and better handling diverse trafic features.

• We evaluate DQSA on the ISCX VPN-nonVPN dataset [20] and a self-collected dataset of Transport Block Size (TBS) in Downlink Control Information (DCI) from cellular networks. Comparisons with state-of-theart baselines and the post-hoc method DEEPSHAP [21] demonstrate DQSA’s superior accuracy, interpretability, and generalizability across diverse network data, with ablation studies confirming the efectiveness of each module.

The remainder of the paper is organized as follows: Section II reviews related work on trafic classification and multiple instance learning. Section III introduces our DQSA method. Section IV details the experiments and results. Finally, Section V provides the conclusion.

## II. RELATED WORK

In the early years, trafic classification was typically accomplished using port-based methods or Deep Packet Inspection (DPI) [1], [22]. However, as networks evolved, these techniques have gradually lost their efectiveness. Recently, deep learning-based approaches have rapidly advanced, providing strong performance and ease of implementation. In [23], the feasibility of protocol classification was investigated by analyzing transport-layer payloads using artificial neural networks (ANN) and Stacked Auto-Encoders (SAE). The first 784 bytes of the payload were utilized and converted into a $2 8 \times 2 8$ image. Then CNN was employed to recognize malware trafic [24] and encrypted trafic [3], respectively. In addition to analyzing payloads, Lopez-Martin et al. extracted both spatial and temporal features from network trafic using CNN and Long Short-Term Memory (LSTM) networks. They focused on the first 20 packets in the network trafic, extracting six key features: source port, destination port, the number of bytes in the packet payload, TCP window size, inter-arrival time, and packet direction [25].

Recently, some studies have leveraged both perspectives of the network trafic mentioned above to enhance model performance. In [26], both payload information and packetlevel information were simultaneously utilized. In contrast to the packet information used in [25], the port information was excluded, arguing that the inclusion of port information could lead to performance inflation [27]. Another study [14] explored an alternative approach for extracting temporal information from network trafic. By utilizing both the payload of individual packets and the payload of the entire flow, this method achieves notable performance. In [13], MHSA and LSTM are utilized to extract features from the payload bytes and packet flow, demonstrating strong performance in classifying Transport Layer Security (TLS) protocol trafic.

Building on these advances, another line of work focuses on leveraging large-scale pre-training to further improve trafic classification. Instead of training models from scratch on taskspecific datasets, these approaches first pre-train a model on massive packet or flow level trafic datasets and then fine-tune it for specific tasks. For example, in [28], the authors propose a pre-trained datagram-level trafic model for encrypted trafic. Masked autoencoders (MAE) have also been employed to pretrain on large-scale packet and flow level datasets [29], or on masked patch embeddings of trafic bursts [30], achieving accurate trafic classification while significantly reducing the need for labeled data.

Due to the diverse and varied requirements of classifi cation tasks, such as malware detection, service recognition, and trafic classification [22], multi-task learning has attracted attention in the field of network trafic classification. Huang et al. utilized payload information along with a 2D-CNN approach to address multiple tasks simultaneously, including malware detection, VPN encapsulation recognition, and Trojan classification [31]. Zhao et al. introduced another multi-task deep learning architecture within the framework of federated learning, driven primarily by privacy considerations. In this distributed learning scenario, the tasks addressed include anomaly detection, VPN recognition, and service classification [32]. Another study explored multi-task learning by addressing service classification along with predicting the bandwidth requirements and flow duration [33].

![](images/e07bfb92aa2d5612ba522bbd37670ec63f050672a37c8a74f82df5956030d91d.jpg)  
Fig. 1. The framework of DQSA for multi-task trafic classification. (I) The feature extractor captures instance-level feature embeddings. (II) DQSA aggregates instance features into sample-level embedding. Each DQSA block includes a) N SQ-SAH for attention measurement, b) M2RoPE for positional embedding, and c) TGAR for dynamically routing task-specific attention heads. (III) The task-specific classifier maps the sample-level embedding to the corresponding label.

In addition to the aforementioned works, there are also studies that address multi-task learning by integrating payload data with informative protocol fields from network packets. In [34], a two-stage learning framework called Distiller was presented to fuse network trafic information and simultaneously tackle VPN detection, service classification, and application classification. Similarly, Dai et al. [5] designed a Global-Local Attention Data Selection model (GLADS), which combined trafic data by preprocessing it into a specially designed data structure. This structure, processed through a CNN and an attention-based model, achieved the same three classification tasks as Distiller.

It is important to note that these models lack interpretability, which is crucial not only for ensuring the trustworthiness of the model but also for enabling improvements after deployment. Even though the post-hoc method can be conducted in trafic classification model [8], which includes methods based on Shapley values [21], gradient-based approaches [35], and Local Interpretable Model-agnostic Explanations (LIME) [36], the insensitivity to the model or the data reduces some gradient-based methods’ reliability for attributing data features [37], [38]. Additionally, some post-hoc interpretation methods, like DeepSHAP, involve huge computation consumption [39]. Moreover, the results of diferent post-hoc interpretability methods demonstrate the inconsistency [40]. To address this issue, in this paper we proposed DQSA as a solution since DQSA ofers inherent interpretability.

Another drawback of existing methods is that some model architectures are specifically tailored to certain input data structures, such as GLADS, which limits their broader applicability. This limitation restricts the model’s applicability, as transport layer packets cannot be acquired from all types of networks due to encryption mechanisms. However, alternative network metrics, such as TBS in DCI within cellular networks, can be utilized for trafic classification [41]. To address this issue, we treat all types of input as time series and enhance Rotary Position Embedding (RoPE), making our model more versatile. The rationale behind this approach is that both the informative protocol fields from network packets and the TBS in DCI inherently exhibit a time series structure. Furthermore, the payload is frequently processed using 1D-CNN in numerous studies [5], [24], [34]. For cases where multiple types of network trafic features are input simultaneously, such as payload from the transport layer and packet header information, we will continue referring to this as multimodal to maintain consistency with the terminology used in Distiller [34] and GLADS [5].

## III. METHODOLOGY

In this section, we present the modules of the DQSA framework and their implementation for multi-task trafic classification. The overall architecture of DQSA is illustrated in Fig. 1. Following the feature extraction from network trafic data, each timestamp is treated as an instance and represented as a feature embedding. The DQSA framework comprises two blocks, each incorporating M2RoPE for positional embedding, TGAR for weighting task-specific attention heads, and multiple SQ-SAH. Each block also includes a feed-forward network (FFN), omitted from the figure for simplicity. Finally, the class token of the sample is utilized for addressing specific trafic classification tasks.

## A. Problem Definition

Multi-task trafic classification aims to jointly predict multiple task-specific labels for the same network trafic instance. Formally, given an input trafic sample $X ~ \in ~ { \mathcal { X } } .$ , the goal is to predict the corresponding task-specific labels ${ \cal Y } \_ { } =$ $[ y _ { 1 } , y _ { 2 } , \ldots , y _ { \tau } ] \in \mathcal { V }$ , where τ denotes the number of classification tasks (e.g., application type, encryption status, or trafic service).

1) Trafic Representation: A trafic instance X may consist of multiple modalities:

$$
\boldsymbol {X} = \{\mathcal {M} _ {1}, \mathcal {M} _ {2}, \dots , \mathcal {M} _ {J} \},\tag{1}
$$

where each modality $\mathcal { M } _ { j }$ corresponds to a distinct feature of the trafic, $\mathrm { e . g . }$ , transport-layer payload or header information. Each modality is a sequence of length $t _ { j } { \mathrm { : } }$

$$
\mathcal {M} _ {j} = [ \boldsymbol {x} _ {1} ^ {j}, \boldsymbol {x} _ {2} ^ {j}, \dots , \boldsymbol {x} _ {t _ {j}} ^ {j} ].\tag{2}
$$

Thus, the entire trafic sample is represented as a multimodal sequence.

2) Transport-Layer Trafic: A flow $\mathcal { F }$ is defined as a sequence of n packets that share the same 5-tuple: transportlayer protocol, source address, destination address, source port, and destination port:

$$
\mathcal {F} = \{P _ {1}, P _ {2}, \dots , P _ {n} \},\tag{3}
$$

where each packet $P _ { i }$ contains: (i) packet-level information $P I _ { i }$ (e.g., length, direction), and (ii) raw payload bytes $\pmb { B } _ { i }$ with $q$ bytes in the i-th packet:

$$
P _ {i} = \{\boldsymbol {P I} _ {i}, \boldsymbol {B} _ {i} \}.\tag{4}
$$

For example, a TCP flow may contain 10 packets. The packet-level information such as length and direction [5], [25], [34] can be represented as PI, and the sequence

$$
\mathcal {M} _ {1} = \left[ \boldsymbol {P I} _ {1}, \boldsymbol {P I} _ {2}, \dots , \boldsymbol {P I} _ {1 0} \right]\tag{5}
$$

can be considered as one modality of the trafic, preserving its time series property. The payload of each packet $P _ { i }$ can be represented as

$$
\boldsymbol {B} _ {i} = \left[ \text { byte } _ {i} ^ {1}, \dots , \text { byte } _ {i} ^ {q} \right], \quad \text { where   byte } _ {i} ^ {q} \in [ 0, 2 5 5 ].\tag{6}
$$

Here, i denotes the i-th packet and $q$ is the number of bytes in the packet. The payload sequence of the entire flow can then be represented as

$$
\mathcal {M} _ {2} = [ \mathrm{byte} _ {1} ^ {1}, \mathrm{byte} _ {1} ^ {2}, \dots , \mathrm{byte} _ {1 0} ^ {q} ].\tag{7}
$$

Thus, the entire trafic flow can be represented as a multimodal sequence, $X = \{ \mathcal { M } _ { 1 } , \mathcal { M } _ { 2 } \}$

3) Physical-Layer Trafic: For trafic metrics collected from the physical layer, such as the TBS in DCI within cellular networks [41], the network trafic can be represented as a TBS flow. In this case, each feature x corresponds to a TBS value. The entire sample $X = \lbrace \mathcal { M } _ { 1 } \rbrace$

$$
\mathcal {M} _ {1} = \left[ \mathrm{TBS} _ {1}, \mathrm{TBS} _ {2}, \dots , \mathrm{TBS} _ {t} \right].\tag{8}
$$

Each TBS flow represents a sequence of transmitted block sizes in cellular downlink control information (DCI), which can be used as features for trafic classification.

## B. Soft Quantization Self Attention Head (SQ-SAH)

After the feature extraction process, each $\boldsymbol { x } _ { i } ^ { j }$ in X is transformed into a feature embedding. For simplicity, without introducing additional variables, we continue to use X to denote the network trafic sample, and $\boldsymbol { x } _ { i } ^ { j } \in \mathbb { R } ^ { d }$ represents a $d -$ dimensional instance feature embedding. We utilize the class token to consolidate information across instances [42]. Additionally, we employ the task token to introduce task-specific biases, facilitating tailored adjustments for each task [43]. In this way, we obtain $X _ { t a s k }$ for the subsequent processing specific to the task, which can be presented as:

$$
X _ {t a s k} = [ c l s, x _ {1}, x _ {2}, \dots , x _ {L} ] + [ t a s k ]\tag{9}
$$

where [cls] and [task] represent class token and task token respectively and L denotes the length of the sequence X.

The MHSA mechanism can be presented in Eq. (10) as follows [44]:

$$
\operatorname{MultiHead} (\boldsymbol {Q}, \boldsymbol {K}, \boldsymbol {V}) = \operatorname{Concat} \left(\operatorname{head} _ {1}, \dots , \operatorname{head} _ {h}\right) \boldsymbol {W} ^ {O}\tag{10}
$$

where each attention head is computed as shown in Eq. (11):

$$
\text { head } _ {i} = \text { Attention } \left(X _ {\text { task }} W _ {i} ^ {Q}, X _ {\text { task }} W _ {i} ^ {K}, X _ {\text { task }} W _ {i} ^ {V}\right)\tag{11}
$$

The scaled dot-product attention is defined as:

$$
\operatorname{Attention} (\boldsymbol {Q}, \boldsymbol {K}, V) = \operatorname{Softmax} \left(\frac {\boldsymbol {Q} \boldsymbol {K} ^ {T}}{\sqrt {d _ {k e y}}}\right) \boldsymbol {V}\tag{12}
$$

where Q, K, and V are the query, key, and value matrices, respectively; $W _ { i } ^ { Q } , ~ W _ { i } ^ { K }$ , and $\bar { \boldsymbol { W } } _ { i } ^ { V }$ are the learned projection matrices for the i-th head; $W ^ { O }$ is the output projection matrix; and $d _ { k e y }$ is the dimensionality of the keys.

However, the Multi-Head Self-Attention (MHSA) mechanism has a complexity of $\mathcal { O } ( L ^ { 2 } )$ due to the computation of the attention matrix $\boldsymbol { Q } \boldsymbol { K } ^ { \intercal }$ , which grows quadratically with the sequence length $( L + 1$ in this paper). Therefore, a vectorquantized attention matrix calculation method is introduced in [17]. By leveraging a codebook $\textbf { \textit { C } } = \ [ c _ { 1 } , \ldots , c _ { S } ]$ and the vector-quantization method, the complexity is reduced to O(LS ), which can be represented as:

$$
\Phi \left(\frac {\boldsymbol {Q} \hat {\boldsymbol {K}} ^ {\top}}{\sqrt {d _ {k e y}}}\right) = \Phi \left(\frac {\boldsymbol {Q} \boldsymbol {C} ^ {\top} \boldsymbol {\Delta}}{\sqrt {d _ {k e y}}}\right) = \Phi \left(\frac {\boldsymbol {Q} \boldsymbol {C} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \boldsymbol {\Delta}\tag{13}
$$

where Φ ( ) denotes Softmax ( ) operation, $\pmb { \Delta } \in \mathcal { R } ^ { S \times ( L + 1 ) }$ and $\Delta _ { \mathbf { s } , \mathbf { l } } = \delta _ { s , z _ { l } }$ . Here $\delta _ { s , z _ { l } }$ denotes the Kronecker delta function:

$$
\delta_ {i j} = \left\{ \begin{array}{l l} 1 & i = j \\ 0 & i \neq j \end{array} \right.\tag{14}
$$

and,

$$
z _ {l} = \arg \min _ {z} \| \boldsymbol {k} _ {l} - \boldsymbol {c} _ {z} \| ^ {2}\tag{15}
$$

In other words, this method utilizes a fixed-size codebook to control the computational complexity. For each $k _ { l }$ in K, the closest codeword $\boldsymbol { c } _ { z _ { l } }$ is selected to approximate $k _ { l } .$ Nevertheless, due to the involvement of the arg min function, the gradient must be adjusted, for instance, through methods like the Straight-Through Estimator (STE) [45]. To circumvent this complex process, we introduce the SQ-SAH, which can be formulated as:

$$
\operatorname{SQ-SAH} (\boldsymbol {Q}, \boldsymbol {K}, V) = \Phi \left(\frac {\boldsymbol {Q} \boldsymbol {C} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \Phi \left(\frac {\boldsymbol {C} \boldsymbol {K} ^ {\top}}{\sqrt {d _ {k e y}}}\right) V\tag{16}
$$

where Φ ( ) denotes Softmax ( ) operation. The advantages of SQ-SAH are evident from two perspectives. Firstly, by avoiding the direct calculation of $\boldsymbol { Q } \boldsymbol { K } ^ { \intercal }$ , the complexity is reduced to $\mathcal { O } ( L S )$ . In practice, this leads to a significant reduction in computational complexity, as the calculation of the $( L + 1 ) \times ( L + 1 )$ matrix is avoided. Specifically, the following expression demonstrates the reduction in complexity:

$$
\begin{array}{l} \left(\Phi \left(\frac {\boldsymbol {Q C} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \Phi \left(\frac {\boldsymbol {C K} ^ {\top}}{\sqrt {d _ {k e y}}}\right)\right) \boldsymbol {V} \\ = \Phi \left(\frac {\boldsymbol {Q C} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \left(\Phi \left(\frac {\boldsymbol {C K} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \boldsymbol {V}\right) \end{array}\tag{17}
$$

Another advantage of the SQ-SAH is that it can be interpreted as the Query measuring attention to the codebook, while the similarity between each codeword and the Key is evaluated by the second Φ ( ) function. This approach efectively constrains the hypothesis space of the attention mechanism, thereby reducing the risk of overfitting [18]. Our experiment results in Section IV demonstrate the efectiveness of the SQ-SAH.

## C. Positional Embedding

Since the self-attention module does not inherently capture temporal information, positional embeddings are crucial for self-attention-based models. Although sinusoidal positional embeddings are commonly used [44], they tend to lose relative temporal information, which is important in network trafic classification, during the feedforward process [46]. Recently, RoPE has been a method for encoding positional information in self-attention-based models that enhances the capture of relative positional relationships by rotating embeddings in a continuous space [19]. This approach allows for more efective modeling of sequential data by maintaining the relative distances between positions. Let $\pmb { x } _ { m } \in \mathbb { R } ^ { d }$ denote the feature vector at the m-th position. The general form of RoPE for $x _ { m }$ can be presented in Eq. (18).

$$
R o P E _ {\{q, k \}} (\pmb {x} _ {m}, m) = \pmb {R} _ {\Theta , m} ^ {d} \pmb {W} _ {\{q, k \}} \pmb {x} _ {m}\tag{18}
$$

where

$$
R _ {\Theta , m} ^ {d} = \left[ \begin{array}{c c c c} M _ {1} & & & \\ & M _ {2} & & \\ & & \ddots & \\ & & & M _ {d / 2} \end{array} \right]\tag{19}
$$

$$
M _ {i} = \left[ \begin{array}{c c} \cos m \theta_ {i} & - \sin m \theta_ {i} \\ \sin m \theta_ {i} & \cos m \theta_ {i} \end{array} \right]\tag{20}
$$

is the rotary matrix with pre-defined parameters $\Theta = \{ \theta _ { i } =$ $\theta _ { b a s e } ^ { - 2 ( i - 1 ) / d } , i \in [ 1 , 2 , \cdots , d / 2 ] \}$

An illustration of RoPE is shown in Fig. 2, where the input $\pmb { x } _ { m } \in \mathbb { R } ^ { d }$ is divided into two-dimensional vectors. Each twodimensional vector undergoes a rotation based on $\theta _ { i } ,$ , which is determined by $\theta _ { \mathrm { b a s e } } ,$ the positional information m, and the dimensional index of the corresponding two-dimensional vector.

![](images/554a81539c44cd0c489ad4f82c921e54fcd76626e5c87dd6c04b8fb73b0eaa1f.jpg)  
Fig. 2. An illustration of RoPE.

To enhance the efectiveness of RoPE for our task, we made two adjustments to RoPE. First, we scale the position m to mσ. We observe that interpolating the position improves the monotonicity of the inner product as the relative position increases. To ensure a consistent decay in the magnitude of the inner product with increasing relative position, $\theta _ { b a s e } ,$ which is set as 10000 by default [19], should be reduced to accelerate the rotational transformation. This adjustment ensures that the dot product exhibits the desired monotonic decay as the relative position between vectors grows.

To accommodate the input of network trafic features across multiple modalities, we partition the rotational matrix $R _ { \Theta , m } ^ { d }$ into two components with diferent $\theta _ { b a s e } \mathrm { : }$ one that captures the relative positional information within each modality and another that represents the information between diferent modalities. We hold the assumption that the relative distance within a modality is smaller than the distance between modalities, which is expressed in Eq. (21).

$$
d \left(\boldsymbol {x} _ {t _ {i 1}} ^ {i}, \boldsymbol {x} _ {t _ {i 2}} ^ {i}\right) <   d \left(\boldsymbol {x} _ {t _ {i 1}} ^ {i}, \boldsymbol {x} _ {t _ {j 1}} ^ {j}\right)\tag{21}
$$

where $d ( . )$ means the relative distance measure and $x _ { t _ { i 1 } } ^ { i }$ means one timepoint in the $i _ { t h }$ modality. The distance between two time points within the same modality, $x _ { t _ { i 1 } } ^ { i }$ and $x _ { t _ { i 2 } } ^ { i } ,$ , is smaller than that between time points from diferent modalities, $x _ { t _ { i 1 } } ^ { i }$ and $x _ { t _ { j 1 } } ^ { j }$ . Because the $\theta _ { b a s e }$ can be considered as a unit velocity of the rotation, we introduce this diference in the $\theta _ { b a s e }$ as multi-velocity. Finally, the rotation matrix of the monotonic and multi-velocity variant of RoPE, called M2RoPE, can be expressed as:

$$
R = \left[ \begin{array}{c c} R _ {\Theta_ {1}, m _ {1} \sigma_ {1}} ^ {d _ {1}} & \\ & R _ {\Theta_ {2}, m _ {2} \sigma_ {2}} ^ {d _ {2}} \end{array} \right]\tag{22}
$$

where $d _ { 1 }$ and $d _ { 2 }$ are even integers and hold $d _ { 1 } + d _ { 2 } = d .$ In DQSA, we employ M2RoPE in the same manner as RoPE is used in [19].

## D. Task Gated Attention Routing (TGAR)

Another module of DQSA is Task-Gated Attention Routing, which enables each attention head to either share functionality across tasks or be for specific tasks. This flexibility allows the model to leverage commonalities while also focusing on task-specific details, thereby enhancing performance across multiple tasks. To achieve this, the routing network can be represented as:

$$
G (\boldsymbol {x}) _ {\text { task } _ {\tau}} = \text { TopK } \left(\text { Softmax } (\boldsymbol {x} \boldsymbol {W} _ {\boldsymbol {g}}), K\right)\tag{23}
$$

where x is from $X _ { t a s k } ; ~ W _ { g } ~ \in ~ \mathbb { R } ^ { d \times h }$ denotes the router parameters; and TopK ( K) sets all elements in the vector to zero except for the K largest values. This process allows us to identify the relevant attention heads for the instance x in task task . The final attention can be presented as:

$$
\mathrm{DQSA} _ {\text { task } _ {\tau}} = \operatorname{Concat} \left(G (\boldsymbol {x}) _ {\text { task } _ {\tau}} [ \text { head } _ {1}, \dots , \text { head } _ {h} ]\right)\tag{24}
$$

However, two issues arise when using the task-gated router directly. First, most instances will utilize only a subset of attention heads or codewords, leading to the other heads or codewords being unused. Second, the task-gated router does not capture the relationships or connections between diferent tasks. To address these issues, two loss functions are designed in TGAR: Attention Balance Loss and Task Related Loss.

1) Attention Balance Loss: For the model as a whole, our goal is to ensure that each codeword in every attention head is fully utilized to achieve the maximum performance potential of the model. To quantify this, we define the average attention assigned to codeword $c _ { s }$ in attention head h across all tasks and samples as $P ( c _ { s } ^ { h } )$ . The entropy of the attention distribution over all codewords is given by:

$$
H (C) = - \sum_ {h = 1} ^ {H} \sum_ {s = 1} ^ {S} P (c _ {s} ^ {h}) \log P (c _ {s} ^ {h})\tag{25}
$$

Then, the Attention Balance Loss can be defined as:

$$
\operatorname{Loss} _ {A B} = \log (H \times S) - H (C)\tag{26}
$$

This loss measures the distance between H(C) and its upper bound.

2) Task Related Loss: To illustrate the cooperation and specialization among tasks, we follow the approach outlined in [43]. Specifically, we model $P ( H _ { h } | T _ { \tau } )$ as the probability that attention head $H _ { h }$ is used for task $T _ { \tau }$ . We then define $P ( H _ { h } , T _ { \tau } ) = P ( H _ { h } | T _ { \tau } ) P ( T _ { \tau } )$ and $\begin{array} { r } { P ( H _ { h } ) \ = \ \sum _ { T } P ( H _ { h } , T _ { \tau } ) } \end{array}$ . To capture the dependence of attention head usage on tasks, we introduce a mutual information measure to quantify this relationship:

$$
I (H; T) = \sum_ {h = 1} ^ {H} \sum_ {\tau = 1} ^ {T} P \left(H _ {h}, T _ {\tau}\right) \log \frac {P \left(H _ {h} , T _ {\tau}\right)}{P \left(H _ {h}\right) P \left(T _ {\tau}\right)}\tag{27}
$$

Due to the absence of an upper bound for maximizing the Kullback-Leibler (KL) divergence, we choose to use Jensen-Shannon (JS) divergence. We minimize the distance between the JS divergence and its theoretical upper bound to ensure stable training. The JS divergence can be presented as:

$$
D _ {\mathrm{JS}} (P \| Q) = \frac {1}{2} D _ {\mathrm{KL}} (P \| M) + \frac {1}{2} D _ {\mathrm{KL}} (Q \| M)\tag{28}
$$

where

$$
M = \frac {1}{2} (P + Q)\tag{29}
$$

Then the Task Related Loss can be defined as:

$$
\operatorname{Loss} _ {T R} = \log 2 - D _ {\mathrm{JS}} (P \| Q)\tag{30}
$$

After processing, for a specific task $T _ { \tau } ,$ we utilize the taskspecific MLP head along with the class token to compute the task loss shown in Eq. (31).

$$
L _ {\tau} = \text { CrossEntropy } (\text { MLP } _ {\tau} ([ \text { cls } _ {\tau} ]), Y _ {\tau})\tag{31}
$$

So the total loss of the multi-task trafic classification is shown in Eq. (32).

$$
\text { Loss } = \sum_ {\tau} w _ {\tau} L _ {\tau} + \sum_ {\text { layers }} (w _ {A B} \text { Loss } _ {A B} + w _ {T R} \text { Loss } _ {T R})\tag{32}
$$

## E. Interpretability

The proposed DQSA is naturally interpretable due to its capacity to localize instances of interest within network trafic. This interpretability is achieved by examining the attention maps of the self-attention layers. Specifically, the attention information can be obtained using the class token, for the $i _ { t h }$ SQ-SAH:

$$
\boldsymbol {A} _ {i} = \Phi \left(\frac {[ c l s ] \boldsymbol {C} ^ {\top}}{\sqrt {d _ {k e y}}}\right) \Phi \left(\frac {\boldsymbol {C} \boldsymbol {K} ^ {\top}}{\sqrt {d _ {k e y}}}\right)\tag{33}
$$

$$
I n t e r p r e t a b i l i t y = G (X) \mathcal {A}\tag{34}
$$

where $\mathcal { A } = [ A _ { i } , \cdots , A _ { h } ]$ and $A _ { i } \in \mathcal { R } ^ { L }$ gives the importance weights of all instances in the network trafic.

## F. Complexity Analysis

For a sequence of length L and key dimension $d _ { k e y } ,$ the conventional self-attention mechanism requires computing the full attention matrix $Q K ^ { \top } ~ \in ~ \mathbb { R } ^ { L \times L }$ , which incurs $\mathcal { O } ( L ^ { 2 } d _ { k e y } )$ time complexity and $\mathcal { O } ( L ^ { 2 } )$ memory consumption. Such quadratic scaling limits the applicability of self-attention to long sequences.

In contrast, the proposed SQ-SAH leverages a fixed-size codebook $C \in \mathbb { R } ^ { S \times d _ { k e y } }$ to replace pairwise token interactions with token–codeword interactions. As a result, the computation reduces to $\mathcal { O } ( L S d _ { k e y } )$ , where S is the codebook size, typically much smaller than L and fixed. This yields linear complexity with respect to sequence length. Moreover, since the $\mathcal { O } ( L ^ { 2 } )$ attention matrix is avoided, the memory consumption is reduced to O(LS ).

Therefore, SQ-SAH not only improves computational eficiency but also reduces memory usage, which is particularly beneficial for processing long transport-layer packet sequences. This eficiency improvement is further validated by runtime and GPU memory usage comparisons in Section IV (see Fig. 4).

## IV. EXPERIMENTS AND RESULTS

This section begins by introducing the dataset and preprocessing steps. Next, the experimental setup and the baseline models considered are presented. A comprehensive comparison of DQSA against state-of-the-art network trafic classification models across multiple tasks and datasets is subsequently presented, followed by an ablation study to analyze the performance of DQSA. Finally, we demonstrate the performance of DQSA in model pruning and interpretability.

![](images/fb48323b0e6888dab26636e74d54968ba31291ae8dec08fd7a5106ba74de7579.jpg)  
(a) Confusion matrix for Distiller

![](images/cbd9f9a7a961c87b16b715f77cee9dfd9f25310311656eb47e14ca43c90aed1b.jpg)  
(b) Confusion matrix for DQSA

![](images/3dc8f18064e4340cb6b44f641037589c6be82de968f747405db2d55a5a392014.jpg)  
(c) Label Distribution in the test set

Fig. 3. Confusion matrix for Distiller and DQSA in the Application Classification task on the ISCX VPN-NonVPN dataset, alongside the label distribution in the test set for this task.  
![](images/f7e68cde8e8c1ff39b28bd7b74fd128dfb09a49783e0de24d3006090ae1661a9.jpg)  
(a) Operation Speed

![](images/6921a194a8246b6b969d93b29fc8f62cced2db4d0b47ec9bb9eec2541cf8584d.jpg)  
(b) GPU Memory Usage  
Fig. 4. Comparison of the speed and GPU memory usage between Self-Attention Head (SAH) and SQ-SAH.

## A. Dataset and Preprocessing

To evaluate the performance of our model, we conduct experiments using two datasets shown in TABLE I.

1) ISCX VPN-NonVPN: The ISCX VPN-NonVPN dataset [20] is a well-known public resource for multi-task trafic classification, which provides network trafic data with both standard and VPN-encrypted versions. Each network trafic is labeled with three attributes: encapsulation type, trafic type, and application. For each classification task, there are 2 classes for encapsulation classification, 6 classes for trafic type classification, and 15 classes for application classification.

We implement data cleaning to ensure the quality and relevance of the data. Specifically, we remove biflows that are invalid or do not match the expected labels. This process involves retaining biflows according to the criteria outlined in [47] and excluding those with IP addresses of 0.0.0.0 or 255.255.255.255 [34]. These measures are essential to maintain the integrity of the dataset and ensure that only meaningful and accurate trafic data is used for analysis.

For the input, we use the same two types of input data as in [34]. The first type consists of the first 784 bytes of the transport-layer payload (PAY), which is normalized to a range of [0, 1] [24]. The second type includes header information fields (HDI) from the first 32 packets, incorporating four metrics:

TABLE I  
ISCX VPN-NONVPN AND DCI-LTE DATASET TASKS AND CLASSES. CATEGORICAL LABELS ARE REPORTED IN ROUND BRACKETS

<table><tr><td>Dataset</td><td>Task</td><td>Classes</td></tr><tr><td rowspan="3">ISCX</td><td> $T_1$  - Encapsulation</td><td>nonVPN (1), VPN (2)</td></tr><tr><td> $T_2$  - Traffic Type</td><td>VoIP (1), FileTransfer (2), P2P (3), Streaming (4), Chat (5), Email (6)</td></tr><tr><td> $T_3$  - Application</td><td>Skype (1), BitTorrent (2), Hangouts (3), VoipBuster (4), Facebook (5), FTPS (6), SCP (7), Mail (8), YouTube (9), Vimeo (10), Spotify (11), Netflix (12), SFTP (13), Aim (14), ICQ (15)</td></tr><tr><td rowspan="2">DCI-LTE</td><td> $T_1$  - Traffic Type</td><td>StreamingVideo (1), TextChat (2), StreamingMusic (3), VideoChat (4), Game (5), SocialNetworking (6), Shopping (7)</td></tr><tr><td> $T_2$  - Application</td><td>YouTube (1), Netflix (2), Instagram (3), X (4), AppleMusic(5), Facebook (6), YouTubeMusic (7), TelegramVideo (8), TelegramText (9), WeChatText (10), WhatsAppText (11), WeChatVideo (12), WhatsAppVideo (13), Carousell (14), Legends (15), PUBG (16), Genshin (17), AmazonPrimeVideo (18), Spotify (19), Lazada (20), Shopee(21)</td></tr></table>

1) Number of bytes in the transport-layer payload

2) TCP window size (or zero for UDP packets)

3) Inter-arrival time

4) Packet direction (0 or 1)

These data types provide a comprehensive feature set for efective classification.

TABLE II  
EXPERIMENTAL CONFIGURATION

<table><tr><td>Hyperparameter</td><td>Value</td></tr><tr><td>Number of Attention Heads</td><td>8</td></tr><tr><td>Number of Codewords</td><td>16</td></tr><tr><td>Top-K</td><td>4</td></tr><tr><td>Instance Feature Dimension</td><td>128</td></tr><tr><td>Dropout Rate</td><td>0.2</td></tr><tr><td> $w_{AB}$ </td><td>0.02</td></tr><tr><td> $w_{TR}$ </td><td>0.02</td></tr><tr><td> $w_{\tau}$ </td><td> $1/num_{tasks}$ </td></tr><tr><td>Learning Rate</td><td>0.0008</td></tr><tr><td>Batch Size</td><td>200</td></tr><tr><td>Epochs</td><td>200</td></tr></table>

2) DCI-LTE: Another dataset we utilize is called the DCI-LTE dataset, which is self-collected. This experiment addresses the challenge that, in some network frameworks, such as cellular networks, obtaining packet information from the transport layer can be dificult. Our goal is to ensure that our method is applicable to network trafic metrics collected from diferent network layers. DCI is transmitted unencrypted in the physical layer, including the TBS, reflecting the volume of resources allocated to users in both uplink and downlink. It is hypothesized that variations in trafic utilization across diferent applications are distinct and that TBS can be employed as a discriminatory feature for trafic classification [41], [48], [49]. The data collection procedure follows the data acquisition system mentioned in [49]. Seven types of network trafic services are collected, with each service represented by trafic from three mobile applications. For each mobile application, 200 TBS flows are collected, with each flow lasting 25 seconds. In total, there are 4200 TBS flows in this dataset.

For preprocessing, we apply a non-overlapping sliding window of 0.1 seconds and compute six features for each window:

1) Maximum TBS for uplink/downlink

2) Total TBS for uplink/downlink

3) Number of DCI instances for uplink/downlink

The class names for each task in each dataset are presented in TABLE I.

## B. Setup and Baseline

Here, we introduce the setup of our experiment. The experiments on the two datasets were conducted separately. The dataset was split into three parts: training set, validation set, and test set, with a ratio of 0.7, 0.1, and 0.2, respectively. The model with the highest average accuracy on the multitask validation set was saved, and its performance was then evaluated on the test dataset. We use InceptionTime [50] as the feature extractor.

The hyperparameters are summarized in Table II. We adopt the Adam optimizer and apply a learning rate scheduler, where the learning rate is reduced by a factor of 0.5 every 45 epochs.

We consider a wide range of existing models for performance comparison.

1) ISCX VPN-NonVPN: The multi-task scenario has been explored in this dataset. To this end, we consider several categories of existing models listed below.

• Multi-task-Multimodalities Here, we compare two state-of-art models. Distiller [34] leverages intra- and inter-modality dependencies to utilize the heterogeneity of trafic data and overcome the performance limitations of existing single-modal deep learningbased trafic classification methods. GLADS [5] utilizes an “indicator” mechanism to reconstruct multimodal data, combined with an attention-based framework that captures input features and delivers classification results.

Singletask-Multimodalities We consider the ATVITSC model [14], where payload packet-level images are aggregated into session images. A ViT-like model captures global features, while attention-based convolution extracts temporal features, and a bidirectional LSTM captures spatial features between packets. The fused global and spatiotemporal features are then used to classify encrypted trafic.

• Multi-task-Singlemodalities We consider the 2D-CNN model [31], which is a single-modal, multi-task model originally designed for two binary and one multi-class learning task. We have adapted it to fit our requirements, transforming it into one binary learning task (Encaps.) and two multi-class learning tasks (Trafic and App.).

• Singletask-Singlemodalities We consider four models in this part, two deep learning models 1D-CNN (PAY) [3], 2D-CNN + LSTM (HDI) [25], and two pretrained models ET-BERT [28] and YaTC [29] as strong baselines. We add task-specific MLP layers to adapt these for a multi-task setting.

It is noted that all models used the same PAY and/or HDI data for a fair performance comparison, except for GLADS and ATVITSC, where special input data constructions are employed. For these cases, we construct the input data as described in their respective papers.

2) DCI-LTE: : Since there are no existing methods specifically designed for multi-task situations in network trafic classification using the TBS in DCI, we consider the following baseline models:

• Native DL architectures We consider five deep learning architectures, LSTM, 1D-CNN, 2D-CNN, MLP, and Transformer Encoder, where the first four have been utilized in TBS-based trafic classification [41].

• Time series classification DL architectures Because the TBS flow has the characteristics of the time series. We consider three Time series classification DL architectures, i.e., Inceptiontime [50], FCN and Resnet [51]

We implement a classic Transformer baseline (Tr-CLS) for multi-task trafic classification on both ISCX VPN-NonVPN and DCI-LTE datasets. The model uses the same feature embeddings as DQSA, aggregates information via a [cls] token, and employs three separate MLP heads for multitask prediction. This baseline does not include SQ-SAH, TGAR, M2RoPE, or task tokens, providing a fair reference to evaluate the benefits of our dynamic attention and task-gated design.

TABLE III  
COMPARISON OF DQSA ACCURACY AND F-MEASURE WITH STATE-OF-THE-ART BASELINES ON THE ISCX VPN-NONVPN DATASET.RESULTS ARE PRESENTED AS MEAN ± STD OVER THREE RANDOM REPETITIONS OF EXPERIMENTS. WE HIGHLIGHT THE TOPRESULT WITH BOLD FORMATTING AND THE SECOND-BEST RESULT WITH UNDERLINED FORMATTING

<table><tr><td>Model</td><td>Acc. (Encaps.)</td><td>Acc. (Traffic)</td><td>Acc. (App.)</td><td>F1 (Encaps.)</td><td>F1 (Traffic)</td><td>F1 (App.)</td></tr><tr><td>DQSA(ours)</td><td>92.85 ± 0.66</td><td>82.49 ± 0.88</td><td>80.35 ± 0.26</td><td>92.14 ± 0.67</td><td>82.05 ± 1.29</td><td>67.85 ± 0.29</td></tr><tr><td>Distiller [34]</td><td>89.55 ± 0.55</td><td>81.07 ± 0.81</td><td>79.13 ± 0.25</td><td>88.01 ± 0.53</td><td>80.00 ± 0.88</td><td>63.49 ± 1.26</td></tr><tr><td>GLADS [5]</td><td>90.19 ± 1.08</td><td>77.09 ± 1.09</td><td>76.02 ± 0.92</td><td>87.85 ± 1.12</td><td>75.71 ± 0.40</td><td>59.18 ± 2.87</td></tr><tr><td>ATVITSC [14]</td><td>86.61 ± 0.97</td><td>75.70 ± 0.80</td><td>75.91 ± 1.13</td><td>85.41 ± 1.17</td><td>73.67 ± 0.70</td><td>60.61 ± 1.59</td></tr><tr><td>YaTC [29]</td><td>91.16 ± 0.79</td><td>79.84 ± 2.56</td><td>78.64 ± 0.95</td><td>90.27± 0.76</td><td>80.16 ± 1.99</td><td>65.28 ± 1.96</td></tr><tr><td>ET-BERT [28]</td><td>87.20 ± 0.66</td><td>80.15 ± 0.44</td><td>79.10 ± 0.84</td><td>85.84 ± 0.53</td><td>81.05 ± 0.20</td><td>65.32 ± 0.32</td></tr><tr><td>Tr-CLS</td><td>87.52 ± 1.46</td><td>78.49 ± 0.34</td><td>77.02 ± 1.01</td><td>86.54 ± 1.69</td><td>78.20 ± 1.33</td><td>63.75 ± 1.34</td></tr><tr><td>2D-CNN_HUANG(PAY) [31]</td><td>80.54 ± 1.74</td><td>72.35 ± 0.98</td><td>75.46 ± 0.82</td><td>77.20 ± 1.82</td><td>70.41 ± 1.50</td><td>61.57 ± 1.23</td></tr><tr><td>1D-CNN_WANG(PAY) [3]</td><td>81.58 ± 1.26</td><td>73.89 ± 0.47</td><td>75.58 ± 1.32</td><td>80.76 ± 1.87</td><td>73.21 ± 1.32</td><td>61.34 ± 0.34</td></tr><tr><td>2D-CNN+LSTM(HDR) [25]</td><td>87.56 ± 1.37</td><td>75.81 ± 1.19</td><td>73.67 ± 0.85</td><td>84.67 ± 1.85</td><td>72.74 ± 1.45</td><td>58.57 ± 0.70</td></tr></table>

TABLE IV

COMPARISON OF DQSA ACCURACY AND F-MEASURE WITH STATE-OF-THE-ART BASELINES ON THE DCI-LTE DATASET.RESULTS ARE PRESENTED AS MEAN ± STD OVER THREE RANDOM REPETITIONS OF EXPERIMENTS. WE HIGHLIGHT THE TOPRESULT WITH BOLD FORMATTING AND THE SECOND-BEST RESULT WITH UNDERLINED FORMATTING

<table><tr><td>Model</td><td>Acc. (Traffic)</td><td>Acc. (App.)</td><td>F1 (Traffic)</td><td>F1 (App.)</td></tr><tr><td>DQSA(ours)</td><td>96.19 ± 0.42</td><td>93.17 ± 0.55</td><td>96.19 ± 0.41</td><td>93.19 ± 0.56</td></tr><tr><td>Tr-CLS</td><td>95.31 ± 0.27</td><td>90.52 ± 1.12</td><td>95.32 ± 0.28</td><td>90.51 ± 1.19</td></tr><tr><td>LSTM</td><td>93.29 ± 0.75</td><td>82.50 ± 1.41</td><td>93.30 ± 0.75</td><td>82.59 ± 1.43</td></tr><tr><td>1D-CNN</td><td>90.28 ± 0.74</td><td>81.58 ± 1.27</td><td>90.28 ± 0.74</td><td>81.66 ± 1.24</td></tr><tr><td>2D-CNN</td><td>86.03 ± 1.20</td><td>68.45 ± 1.51</td><td>86.03 ± 1.24</td><td>68.49 ± 1.38</td></tr><tr><td>MLP</td><td>76.07 ± 1.66</td><td>51.74 ± 2.06</td><td>75.65 ± 1.86</td><td>50.23 ± 2.56</td></tr><tr><td>INCEPTION [50]</td><td>88.65 ± 1.03</td><td>73.01 ± 0.43</td><td>88.60 ± 1.06</td><td>72.78 ± 0.28</td></tr><tr><td>FCN [51]</td><td>89.88 ± 0.95</td><td>72.34 ± 2.11</td><td>89.83 ± 0.96</td><td>72.08 ± 2.15</td></tr><tr><td>RESNET [51]</td><td>87.34 ± 0.31</td><td>68.37 ± 1.61</td><td>87.27 ± 0.34</td><td>67.88 ± 1.10</td></tr></table>

## C. Overall Comparison

To evaluate the performance of the DQSA, we use accuracy, which represents the proportion of correctly classified samples, and macro F1-score, which is calculated as the average of the F1-scores across all classes for each task. The results are shown in TABLE III and TABLE IV.

accuracy and F-measure across diverse network trafic data, which shows its efectiveness in trafic classification tasks.

In our comparative analysis of the DQSA model against state-of-the-art baselines using the ISCX VPN-NonVPN and DCI-LTE datasets, DQSA consistently demonstrates superior performance. On the ISCX VPN-NonVPN dataset shown in TABLE III, DQSA achieves the highest accuracy in all categories, with 92.85% for Encapsulation, 82.49% for Trafic, and 80.35% for Application. DQSA also attains the best F-measure scores: 92.14 for Encapsulation, 82.05 for Trafic, and 67.85 for Application. The next best models, such as Distiller and YaTC, exhibit notably lower performance metrics. Relative to the classical Transformer baseline (Tr-CLS), DQSA achieves accuracy gains of 5.33%, 4.00%, and 3.33% on the three tasks, respectively. Furthermore, when compared with all baseline models, DQSA consistently delivers absolute improvements ranging from 1.69% to 12.31% in encapsulation classification, 1.42% to 6.79% in trafic service classification, and 1.22% to 6.68% in application classification.

Another advantage of DQSA is evident in its F1 score for the Application Classification task on the ISCX VPN-NonVPN dataset. This dataset is imbalanced, and to ensure a fair comparison, we did not apply any techniques for handling class imbalance, such as oversampling or specialized loss functions, but instead used the same operation as models in [5] and [34]. Under these conditions, DQSA achieves an F1 score of 67.85, surpassing all other models. Compared with the classical Transformer baseline (Tr-CLS), DQSA improves the F1 score by 5.6, 3.85, and 4.1 points across the three tasks. Against all other baselines, DQSA demonstrates consistent absolute F1 score gains, ranging from 1.87 to 14.94 in encapsulation classification, 1.00 to 11.64 in trafic service classification, and 2.53 to 9.28 in application classification. In Figure 3, we visualize the confusion matrix for DQSA and Distiller for this task, as well as the label distribution of the data. It is observed that while Distiller struggles to efectively diferentiate categories with few samples, DQSA excels in this aspect.

Similarly, on the DCI-LTE dataset shown in TABLE IV, DQSA excels with accuracy scores of 96.19% for Trafic and 93.17% for Application. It also exhibits F-measure scores of 96.19 for Trafic and 93.19 for Application. Other models, such as Tr-CLS and INCEPTION, lag behind in these metrics. DQSA achieves accuracy improvements of 0.88% and 2.56% compared with Tr-CLS on the two tasks respectively. Overall, consistent top performance of DQSA is observed in both

These consistent improvements, ranging from the classical Transformer baseline to the best-performing state-of-the-art models, demonstrate that DQSA provides not only robustness across tasks and datasets but also tangible advantages in challenging settings such as imbalanced application classification.

## D. Ablation Study

In this subsection, we conduct ablation studies on each component of the DQSA model to demonstrate the role and significance of each part in the overall performance of the model. To ensure clarity, we present the average accuracy and F1 score across all tasks for a given dataset.

![](images/0840134baf0c639831f7cf398774a50ad6b31ed75d7d5b985deba45aa26efb7e.jpg)  
(a) Encaps.

![](images/bb33bf3ba4173ab94bd3e0a519e048b4f5f7e1fc05ab0add7a4a3f88dd9558c4.jpg)  
(b) Traffic

![](images/38842728029d20d437df7c78e63bf366876e06d788d89f48bf83da6f80482553.jpg)  
(c) App.  
Fig. 5. Parameter-priority pruning method. We prune fixed attention heads, aiming to retain as much model performance as possible.

TABLE V  
PERFORMANCE COMPARISON BETWEEN SAH AND SQ-SAH

<table><tr><td rowspan="2">Model</td><td colspan="2">ISCX</td><td colspan="2">DCI</td></tr><tr><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td></tr><tr><td>SQ-SAH(ours)</td><td>83.29</td><td>78.27</td><td>93.23</td><td>93.25</td></tr><tr><td>SAH</td><td>79.51</td><td>73.88</td><td>92.61</td><td>92.64</td></tr></table>

TABLE VI

PERFORMANCE COMPARISON BETWEEN DIFFERENT POSITIONAL EMBEDDING METHODS

<table><tr><td rowspan="2">Model</td><td colspan="2">ISCX</td><td colspan="2">DCI</td></tr><tr><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td></tr><tr><td>DQSA(ours)</td><td>85.23</td><td>80.67</td><td>94.68</td><td>94.69</td></tr><tr><td>None</td><td>84.60</td><td>79.93</td><td>94.60</td><td>94.61</td></tr><tr><td>Sinusoidal</td><td>84.47</td><td>80.09</td><td>94.63</td><td>94.62</td></tr><tr><td>1DROPE</td><td>84.69</td><td>79.93</td><td>93.39</td><td>93.40</td></tr></table>

1) SQ-SAH: We replace SQ-SAH with diferent variants of SAH to compare changes in runtime and GPU consumption by fixing the batch size at 50. The results are shown in Fig. 4, where it is evident that as the sequence length increases, both the runtime and GPU consumption for SAH rise dramatically. In contrast, SQ-SAH does not exhibit a significant increase in these metrics. We demonstrate that SQ-SAH can eficiently handle longer sequences, such as extended packets of data retrieved from the transport layer. From the model results shown in Table V, SQ-SAH exhibits enhanced performance, especially on the ISCX dataset. This improvement is attributed to its use of codebooks, which helps mitigate overfitting. As a result, SQ-SAH is able to deliver better outcomes, particularly on imbalanced datasets like ISCX. It is notable that to conduct a fair comparison, we removed the TGAR module but kept [task] token in this experiment.

PERFORMANCE COMPARISON BETWEEN WITH OR W/O TGAR

<table><tr><td rowspan="2">Model</td><td colspan="2">ISCX</td><td colspan="2">DCI</td></tr><tr><td>Acc.</td><td>F1</td><td>Acc.</td><td>F1</td></tr><tr><td>DQSA(ours)</td><td>85.23</td><td>80.67</td><td>94.68</td><td>94.69</td></tr><tr><td>w/o  $Loss_{TR}$ </td><td>84.46</td><td>79.38</td><td>93.98</td><td>93.99</td></tr><tr><td>w/o  $Loss_{AB}$ </td><td>84.63</td><td>80.13</td><td>94.40</td><td>94.41</td></tr><tr><td>w/o  $Loss_{TR}$ &amp; $Loss_{AB}$ </td><td>84.62</td><td>80.30</td><td>93.57</td><td>93.58</td></tr><tr><td>w/o TGAR</td><td>83.29</td><td>78.27</td><td>93.23</td><td>93.25</td></tr></table>

TABLE VII

2) Positional Embedding Method: We present the performance of the model using diferent positional embedding methods. Specifically, we compare sinusoidal embeddings, the original RoPE encoding, and a version without positional embeddings. The results in Table VI demonstrate that our positional encoding yields the best performance on both datasets. Given the strong temporal characteristics of the data, inefective encoding methods can even slightly degrade the model’s performance. A comparison with the original RoPE results also shows that slight adjustments to RoPE’s $\theta _ { b a s e } ,$ along with the introduction of modality-specific encodings, can enhance the efectiveness of the positional embedding.

3) TGAR: We ablate TGAR and its associated loss functions separately to observe the impact on model performance, with results presented in Table VII. From the results, we can see that incorporating the router significantly enhances the model’s performance. Additionally, including the balance loss for codewords and the task-attention relationship loss further improves the model’s efectiveness. Our experiments also reveal that these loss functions not only boost performance but also encourage more sparse and focused usage of attention heads, which provides possibilities for model pruning. We will present the results of this pruning experiment in the following section.

## E. Model Pruning

In this section, we demonstrate the pruning capability of DQSA. As mentioned earlier, with the inclusion of the TGAR loss function, DQSA exhibits a more sparse codeword usage distribution across diferent tasks, reflecting both task cooperation and specialization. In this section, all experiments are conducted on ISCX dataset because it is more complex. We here first illustrate the definition we used to measure the variation in the model performance. We define the retained performance after pruning is $A c c _ { p r u n e d } / A c c _ { o r i g i n a l } .$ Fig. 7 illustrates the codeword usage distribution in the first layer of DQSA. We normalized the usage probabilities so that the sum across the eight attention heads and four codewords equals one. The results show that, with the TGAR loss, DQSA efectively captures task cooperation, as evidenced by the sharp utilization of the fifth and second attention heads across multiple tasks. Additionally, task specialization is observed, such as the exclusive use of the third head for Encapsulation classification. To this end, we introduce two prune strategies.

![](images/60b7adc8a211a8dbba58ecf4d22d864f356b5bcdff591bca0e8639eea53183ea.jpg)  
(a) Encaps.

![](images/7ad4e0296b4853ab804b6cbac48c576ddd0e03ffe8f4299b84b841c453f56273.jpg)  
(b) Traffic

![](images/ff29a5bb2a2534368a582e016ab52f779958a73a3f1c89afed5963dbc2e85b83.jpg)  
(c) App.  
Fig. 6. Performance-priority pruning method. We retain fixed performance, aiming to prune as many attention heads as possible.

1) Parameter-priority pruning method: In this approach, the priority is given to pruning a fixed proportion of attention heads. Specifically, we remove a predetermined percentage of attention heads in the model, with retained model performance serving as the primary metric, where higher values indicate better outcomes. In our experiment, we progressively prune attention heads based on their importance in the variation in the performance, starting from the lowest. The model includes 16 SQ-SAH heads, and we experiment by pruning 4, 6, 8, and 11 heads. The impact of this pruning on model performance is shown in Fig 5.

2) Performance-priority pruning method: In this approach, the primary focus is on preserving model performance. Specifically, we define a target proportion of the original performance to retain and use the proportion of attention heads that can be pruned as the metric, where a higher pruned proportion indicates better eficiency. In our experiment, we aim to retain 99%, 97.5%, 95%, 92.5%, and 90% of the model’s performance and analyze how many attention heads can be pruned while maintaining these levels. The results are presented in Fig. 6.

For the results of the parameter-priority pruning method, across three tasks, applying a fixed proportion of pruning generally shows that incorporating TGAR preserves higher model performance. Besides, the usage of the Loss and $L o s s _ { A B }$ further enhances the model performance when the fixed amount of the parameters are pruned. For instance, in the Encapsulation task, using TGAR loss allows the model to retain nearly 98% of its performance even after pruning 50% of the attention heads. This is advantageous for practical model deployment, as it suggests that after training a multitask classification model, modular properties exist between tasks. As a result, fewer parameters can be used to deploy a single-task model. Moreover, this characteristic is inherent to the model and does not require complex operations, such as knowledge distillation.

![](images/78f2dadd8b868889d73d1cea0e2a6f3e553b9fc194f8a6451bf667eded6f1176.jpg)

![](images/062d68ccb7fb759e322c7b9bc8bda33806ed956ded7331ec2864d4fe33df1c8b.jpg)

![](images/2c5c9433421a7c57351c353fcd3ccd7a5a02adffdb29cf31c95e3b40c9379b40.jpg)  
(a) Codewords usage distribution with TGAR loss function

![](images/4f800ebb3cb44ad9d49295811983eda04331a255a5bb15ddb8b1667a661263e7.jpg)  
(b) Codewords usage distribution w/o TGAR loss function  
Fig. 7. Codewords usage distribution over the three tasks in ISCX VPN-NonVPN with and w/o TGAR loss function.

It is noteworthy that for the application task, when pruning and retaining only around 30% of the attention heads, we observe a significant performance drop when TGAR loss is applied, even falling below the performance without the loss. This occurs because, with the addition of TGAR loss, the model allocates more efective attention heads to complex tasks to enhance their performance, as evidenced by the ablation experiments in the previous section. Therefore, we argue that for complex tasks, retaining a larger number of parameters during pruning is essential to maintain performance, as excessive pruning can lead to substantial performance degradation.

A similar conclusion can be drawn from the results of the performance-priority pruning method. For simpler tasks, such as Encapsulation, even when requiring the model to retain 90% of its original performance, we are still able to prune nearly 70% of the attention heads. However, for more complex tasks, excessive pruning should be avoided to prevent performance degradation.

![](images/1f0a8091b6a28a73b9495cda7f31966d9a33564ba112ca5bfb3e0a3a993c5eb6.jpg)  
(a) Encaps.

![](images/39f0d790d1d5abe3008b95ac632ce47c2ac16e6689d4d771f5624178f1b305dc.jpg)  
(b) Traffic.

![](images/e8978aaf6bc033ff82b392445dc43a96459299fd1c14d1f261de75cc41216553.jpg)  
(c) App.  
Fig. 8. AOPC-R in ISCX VPN-NonVPN dataset.

## F. Interpretability Performance

DQSA is inherently an interpretable model by leveraging the self-attention mechanism. In this section, we first demonstrate the efectiveness of DQSA’s interpretability by comparing it with the interpretability ofered by a well-known post-hoc interpretability analysis method, DEEPSHAP [21]. In this paper, we employ a quantitative comparison of interpretability rather than relying on qualitative visualizations [5], [15]. We believe the quantitative approach provides a clearer understanding of whether the interpretability is indeed efective. In this paper, we use the area over the perturbation curve (AOPC) [52] as the metric to measure the interpretability efectiveness of the DQSA and DEEPSHAP. This idea posits that the efectiveness of interpretability for a sample lies in its ability to highlight what distinguishes one category from another. Therefore, when we progressively remove information from the sample in the order of importance, it should impact the classification outcome accordingly. The most relevant firstly (MoRF) removed procedure can be expressed as:

$$
\begin{array}{c} \mathcal {X} _ {M o R F} ^ {(0)} = \mathcal {X} \\ \forall 1 \leq k \leq L: \mathcal {X} _ {M o R F} ^ {(k)} = g \left(\mathcal {X} _ {M o R F} ^ {(k - 1)}, r _ {k}\right) \end{array}\tag{35}
$$

where $g \left( \cdot \right)$ denotes the removing operation of the data point that is ranked at position $r _ { k } .$ . In this paper, we use the accuracy decay over the test set to measure the impact of the perturbation. So the AOPC is expressed in Eq. (36).

$$
A O P C = \sum_ {i = 0} ^ {L} A C C \left(\mathcal {X} _ {M o R F} ^ {(0)}\right) - A C C \left(\mathcal {X} _ {M o R F} ^ {(i)}\right)\tag{36}
$$

where L represents the number of perturbation steps and ACC(·) denotes the accuracy of the corresponding perturbed input text set. Then the definition of the AOPC relative randomly perturbed (AOPC-R) is shown in Eq. (37).

$$
A O P C - R = A O P C _ {I n t e r p r e t a b i l i t y} - A O P C _ {R a n d o m}\tag{37}
$$

where $A O P C _ { R a n d o m }$ means the AOPC with random perturbation.

![](images/3960513c754dd162c8c066c662e95679c180ff8cd19b6c65e343ebf3c7d95091.jpg)  
(a) Traffic.

![](images/d2d1619bf914b8d11b07ba2f0b1b970e76c70692b05608fa60fc87fcf701ca7c.jpg)  
(b) App.  
Fig. 9. AOPC-R in DCI-LTE dataset.

In this experiment, we perturb data points ranging from 5% to 50% based on interpretability annotations provided by DQSA and DEEPSHAP. The AOPC-R results are presented in Fig. 8 and Fig. 9.

From the results, we observe that random erasure, serving as the baseline in our experiments, is at zero. In each task, DQSA consistently outperforms DEEPSHAP. This indicates that removing data points based on the interpretability scores provided by DQSA, ordered from highest to lowest, has a significantly greater impact on performance compared to random erasure and also exceeds the impact of DEEPSHAP, a post-hoc analysis method. This demonstrates that DQSA possesses efective intrinsic interpretability, capable of identifying instances that significantly afect model performance. This insight is valuable for understanding the model and for subsequent model enhancement.

We further illustrate the task-specific interpretability of DQSA by visualizing the weighted attention scores derived from Eq. (33) and Eq. (34) for four representative LTE-DCI trafic samples in Fig. 10. Samples #1 and #2 (Game, PUBG) are correctly classified, showing distinct attention patterns across trafic service classification and application classification. Sample #3 (also PUBG) is misclassified as Shopee and its attention map resembles that of sample #4 (Shopee) rather than #1/#2, highlighting how attention visualization can explain misclassification and aid debugging. Specifically, in the “Total UL” channel, unlike the continuous signals in typical gaming samples that reflect the constant stream of user inputs and synchronization packets required by realtime gaming, Sample #3 exhibits intermittent spikes similar to #4, which misleads the attention mechanism. This analysis can also guide data inspection and model refinement, e.g., identifying potential label noise or designing targeted data augmentation to improve robustness.

![](images/16fbb5468b59839edf0fc5b4d81f5a6ebe5dcc1e68135065551afbf5b7c77c12.jpg)  
(a) #1 Service (Game)

![](images/9e69086913efb3d6be5add3b253bc3a7c1b1f5f9b4502307f4e97c9cdc888f50.jpg)  
(b) #1 App (PUBG)

![](images/a9d5ef26f0593751f769214eaf9a38a80794c62468503e9747399000acadbf75.jpg)  
(c) #2 Service (Game)

![](images/2257a3537966536a22987198fa74d2b586b354a491a0f8aa7089cd02a727440c.jpg)

![](images/e27d892fe9392f81af3e142d2b9344b7e33d8853e002c27194f55da6148b4833.jpg)  
(e) #3 App (PUBG)

(d) #2 App (PUBG)  
![](images/c4e78058b67193050488a8c67852fc1e26b1d93e0824a1eaaa25173e47cf3639.jpg)  
(f) #4 App (Shopee)  
Fig. 10. Attention visualization of four samples(#num Task (true label)). #1 and #2 show distinct attention patterns across service and application tasks. # is misclassified into the same class as #4 (Shopee), and its attention resembles #4 rather than #1/#2, supporting interpretability and error analysis.

TABLE VIII  
PERFORMANCE OF DQSA AND BASELINE MODELS UNDER DISTRIBUTION SHIFTS

<table><tr><td>Model</td><td>Original</td><td>DiffBS</td><td>LowSig</td></tr><tr><td>DQSA</td><td>96.19</td><td>93.21</td><td>87.50</td></tr><tr><td>Tr-CLS</td><td>95.31</td><td>90.00</td><td>80.71</td></tr><tr><td>LSTM</td><td>93.29</td><td>87.14</td><td>66.79</td></tr></table>

## G. Robustness to New Scenarios

Robustness is a practical concern when deploying trafic classification models in real-world networks. To evaluate this, we collected TBS flows from two diferent network environments in cellular networks: one from a diferent base station and another under low signal quality conditions. We tested trafic service classification using three models trained on the original dataset. Table VIII reports the performance of DQSA and two baseline models under these scenarios. Here, “Original” refers to the training dataset, while “DifBS” and “LowSig” represent distribution shifts relative to the training data.

As shown, DQSA consistently outperforms the baselines across all scenarios. While all models experience some performance drop under new conditions, DQSA demonstrates smaller degradation (e.g., 96.19% → 87.50% in LowSig), indicating stronger generalization and robustness to unseen trafic patterns. These results suggest that DQSA can maintain reliable classification under moderately shifted scenarios. We note, however, that handling severe distribution shifts or entirely new trafic classes remains a challenging and important direction for future research.

## V. CONCLUSION

We propose a multi-task network trafic classification model, Dynamic Quantized Self-Attention (DQSA), with inherent interpretability. DQSA incorporates SQ-SAH to reduce complexity and mitigate overfitting, enhanced RoPE encoding for diverse input data, and TGAR for dynamic task-specific attention allocation. We introduce two loss functions for balancing attention load and aligning task-specific focus. Extensive experiments using the ISCX VPN-NonVPN and self-collected DCI-LTE datasets show that DQSA outperforms state-of-the-art models, achieving superior accuracy and F1- scores, especially for classes with fewer samples. Additionally, our model supports task-specific pruning, maintaining 97.5% performance in the Encapsulation classification even after significant pruning. DQSA also demonstrates superior interpretability compared to post-hoc methods, ofering valuable insights for future model improvements.

However, our work has limitations. We consider each timestamp as the smallest unit impacting the prediction results. However, in diferent trafic classification problems, various channels may contribute diferently. Future works will address this issue by exploring more sophisticated trafic data representations.

## REFERENCES

[1] A. Azab, M. Khasawneh, S. Alrabaee, K.-K.-R. Choo, and M. Sarsour, “Network trafic classification: Techniques, datasets, and challenges,” Digit. Commun. Netw., vol. 10, no. 3, pp. 676–692, Jun. 2024.

[2] X. Zhang et al., “Enhanced few-shot malware trafic classification via integrating knowledge transfer with neural architecture search,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 5245–5256, 2024.

[3] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted trafic classification with one-dimensional convolution neural networks,” in Proc. IEEE Int. Conf. Intell. Secur. Informat. (ISI), Jul. 2017, pp. 43–48.

[4] Y. Yang et al., “A network trafic classification method based on dualmode feature extraction and hybrid neural networks,” IEEE Trans. Netw. Service Manage., vol. 20, no. 4, pp. 4073–4084, Dec. 2023.

[5] J. Dai, X. Xu, and F. Xiao, “GLADS: A global-local attention data selection model for multimodal multitask encrypted trafic classification of IoT,” Comput. Netw., vol. 225, Apr. 2023, Art. no. 109652.

[6] G. Wang and Y. Gu, “Multi-task scenario encrypted trafic classification and parameter analysis,” Sensors, vol. 24, no. 10, p. 3078, May 2024.

[7] J.-T. Park, C.-Y. Shin, U.-J. Baek, and M.-S. Kim, “Fast and accurate multi-task learning for encrypted network trafic classification,” Appl. Sci., vol. 14, no. 7, p. 3073, Apr. 2024.

[8] A. Nascita, A. Montieri, G. Aceto, D. Ciuonzo, V. Persico, and A. Pescape, “Improving performance, reliability, and feasibility in mul-´ timodal multitask trafic classification with XAI,” IEEE Trans. Netw. Service Manage., vol. 20, no. 2, pp. 1267–1289, Jun. 2023.

[9] F. Cerasuolo, I. Guarino, V. Spadari, G. Aceto, and A. Pescape, “XAI for ´ interpretable multimodal architectures with contextual input in mobile network trafic classification,” in Proc. IFIP Netw. Conf. (IFIP Networking), Jun. 2024, pp. 757–762.

[10] L. Garcia, G. Bartlett, S. Ravi, H. Ibrahim, W. Hardaker, and E. Kline, “Explaining deep learning models for per-packet encrypted network trafic classification,” in Proc. IEEE Int. Symp. Meas. Netw. (M&N), Jul. 2022, pp. 1–6.

[11] C. Molnar et al., “General pitfalls of model-agnostic interpretation methods for machine learning models,” in Proc. Int. Workshop Extending Explainable AI Beyond Deep Models Classifiers. Cham, Switzerland: Springer, 2020, pp. 39–68.

[12] M. He, L. Jin, and M. Song, “Interpretability framework of network security trafic classification based on machine learning,” in Proc. Int. Conf. Artif. Intell. Secur. Cham, Switzerland: Springer, 2021, pp. 305–320.

[13] P. Lin, K. Ye, Y. Hu, Y. Lin, and C.-Z. Xu, “A novel multimodal deep learning framework for encrypted trafic classification,” IEEE/ACM Trans. Netw., vol. 31, no. 3, pp. 1369–1384, Jun. 2023.

[14] Y. Liu, X. Wang, B. Qu, and F. Zhao, “ATVITSC: A novel encrypted trafic classification method based on deep learning,” IEEE Trans. Inf. Forensics Security, vol. 19, pp. 9374–9389, 2024.

[15] G. Xie, Q. Li, and Y. Jiang, “Self-attentive deep learning method for online trafic classification and its interpretability,” Comput. Netw., vol. 196, Sep. 2021, Art. no. 108267.

[16] C. Zhang, S. Bengio, M. Hardt, B. Recht, and O. Vinyals, “Understanding deep learning (still) requires rethinking generalization,” Commun. ACM, vol. 64, no. 3, pp. 107–115, Mar. 2021.

[17] L. D. Lingle, “Transformer-VQ: Linear-time transformers via vector quantization,” in Proc. 12th Int. Conf. Learn. Represent., 2023, pp. 1–30. [Online]. Available: https://openreview.net/forum?id=oDdzXQzP2F

[18] D. Bashir, G. D. Montanez, S. Sehra, P. S. Segura, and J. Lauw, “An˜ information-theoretic perspective on overfitting and underfitting,” in Proc. 33rd Australas. Joint Conf. AI: Adv. Artif. Intell. (AI), Canberra, ACT, Australia. Cham, Switzerland: Springer, 2020, pp. 347–358.

[19] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu, “RoFormer: Enhanced transformer with rotary position embedding,” Neurocomputing, vol. 568, Feb. 2024, Art. no. 127063.

[20] G. Draper-Gil, A. H. Lashkari, M. S. I. Mamun, and A. A. Ghorbani, “Characterization of encrypted and VPN trafic using time-related features,” in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016, pp. 407–414.

[21] S. M. Lundberg and S.-I. Lee, “A unified approach to interpreting model predictions,” in Proc. Adv. Neural Inf. Process. Syst., I. Guyon et al.., Eds., Red Hook, NY, USA: Curran Associates, 2017, pp. 4765–4774. [Online]. Available: http://papers.nips.cc/paper/7062-a-unified-approachto-interpreting-model-predictions.pdf

[22] P. Wang, X. Chen, F. Ye, and Z. Sun, “A survey of techniques for mobile service encrypted trafic classification using deep learning,” IEEE Access, vol. 7, pp. 54024–54033, 2019.

[23] Z. Wang, “The applications of deep learning on trafic identification,” BlackHat USA, vol. 24, no. 11, pp. 1–10, 2015.

[24] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in Proc. Int. Conf. Inf. Netw. (ICOIN), Da Nang, Vietnam, Jan. 2017, pp. 712–717.

[25] M. Lopez-Martin, B. Carro, A. Sanchez-Esguevillas, and J. Lloret, “Network trafic classifier with convolutional and recurrent neural networks for Internet of Things,” IEEE Access, vol. 5, pp. 18042–18050, 2017.

[26] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “MIMETIC: Mobile\` encrypted trafic classification using multimodal deep learning,” Comput. Netw., vol. 165, Dec. 2019, Art. no. 106944.

[27] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “Mobile encrypted trafic classification using deep learning: Experimental evaluation, lessons learned, and challenges,” IEEE Trans. Netw. Service Manage., vol. 16, no. 2, pp. 445–458, Jun. 2019.

[28] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” in Proc. ACM Web Conf., New York, NY, USA, Apr. 2022, pp. 633–642, doi: 10.1145/3485447.3512217.

[29] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., Jun. 2023, vol. 37, no. 4, pp. 5420–5427. [Online]. Available: https://ojs.aaai.org/index.php/AAAI/article/view/ 25674

[30] Z. Hang, Y. Lu, Y. Wang, and Y. Xie, “Flow-MAE: Leveraging masked AutoEncoder for accurate, eficient and robust malicious traffic classification,” in Proc. 26th Int. Symp. Res. Attacks, Intrusions Defenses, Oct. 2023, pp. 297–314.

[31] H. Huang, H. Deng, J. Chen, L. Han, and W. Wang, “Automatic multi-task learning system for abnormal network trafic detection,” Int J. Emerg. Technol. Learn. (iJET), vol. 13, no. 4, p. 4, Mar. 2018.

[32] Y. Zhao, J. Chen, D. Wu, J. Teng, and S. Yu, “Multi-task network anomaly detection using federated learning,” in Proc. 10th Int. Symp. Inf. Commun. Technol., 2019, pp. 273–279.

[33] S. Rezaei and X. Liu, “Multitask learning for network trafic classification,” in Proc. 29th Int. Conf. Comput. Commun. Netw. (ICCCN), Aug. 2020, pp. 1–9.

[34] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “DISTILLER:´ Encrypted trafic classification via multimodal multitask deep learning,” J. Netw. Comput. Appl., vols. 183–184, Jun. 2021, Art. no. 102985.

[35] M. Sundararajan, A. Taly, and Q. Yan, “Axiomatic attribution for deep networks,” in Proc. Int. Conf. Mach. Learn., vol. 70, 2017, pp. 3319–3328.

[36] M. T. Ribeiro, S. Singh, and C. Guestrin, “‘Why should I trust you?’: Explaining the predictions of any classifier,” in Proc. 22nd ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, Aug. 2016, pp. 1135–1144.

[37] J. Adebayo, J. Gilmer, M. Muelly, I. Goodfellow, M. Hardt, and B. Kim, “Sanity checks for saliency maps,” in Proc. Adv. Neural Inf. Process. Syst., vol. 31, 2018, pp. 9505–9515.

[38] P.-J. Kindermans et al., “The (Un)reliability of saliency methods,” in Explainable AI: Interpreting, Explaining and Visualizing Deep Learning. Cham, Switzerland: Springer, 2019, pp. 267–280. [Online]. Available: https://doi-org.remotexs.ntu.edu.sg/10.1007/978-3-030-28954-6 14

[39] J. Early, G. K. C. Cheung, K. Cutajar, H. Xie, J. Kandola, and N. Twomey, “Inherently interpretable time series classification via multiple instance learning,” 2023, arXiv:2311.10049.

[40] H. Turbe, M. Bjelogrlic, C. Lovis, and G. Mengaldo,´ “Evaluation of post-hoc interpretability methods in time-series classification,” Nature Mach. Intell., vol. 5, no. 3, pp. 250–260, Mar. 2023.

[41] H. D. Trinh, A. Fern<sup>´</sup> andez Gamb´ ´ın, L. Giupponi, M. Rossi, and P. Dini, “Mobile trafic classification through physical control channel fingerprinting: A deep learning approach,” IEEE Trans. Netw. Service Manage., vol. 18, no. 2, pp. 1946–1961, Jun. 2021.

[42] X. Chen et al., “TimeMIL: Advancing multivariate time series classification via a time-aware multiple instance learning,” 2024, arXiv:2405.03140.

[43] Z. Chen et al., “Mod-squad: Designing mixtures of experts as modular multi-task learners,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2023, pp. 11828–11837.

[44] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2025, pp. 5998–6008.

[45] Y. Bengio, N. Leonard, and A. Courville, “Estimating or propagating´ gradients through stochastic neurons for conditional computation,” 2013, arXiv:1308.3432.

[46] P. Dufter, M. Schmitt, and H. Schutze, “Position information in¨ transformers: An overview,” Comput. Linguistics, vol. 48, no. 3, pp. 733–763, Sep. 2022.

[47] U.-J. Baek, M.-S. Lee, J.-T. Park, J.-W. Choi, C.-Y. Shin, and M.-S. Kim, “Preprocessing and analysis of an open dataset in application trafic classification,” in Proc. 24th Asia–Pacific Netw. Oper. Manage. Symp. (APNOMS), Sep. 2023, pp. 227–230.

[48] J.-W. Son, S. Lee, and M.-H. Han, “Supervised service classification using downlink control indicator in LTE physical downlink control channel,” in Proc. Int. Conf. Inf. Commun. Technol. Converg. (ICTC), Oct. 2021, pp. 1533–1536.

[49] Y. Chen, Y. Tong, G. B. Hwee, Q. Cao, S. G. Razul, and Z. Lin, “Real-time trafic classification in encrypted wireless communication network,” in Proc. IEEE Int. Symp. Circuits Syst. (ISCAS), May 2023, pp. 1–5.

[50] H. Ismail Fawaz et al., “InceptionTime: Finding AlexNet for time series classification,” Data Mining Knowl. Discovery, vol. 34, no. 6, pp. 1936–1962, Nov. 2020.

[51] Z. Wang, W. Yan, and T. Oates, “Time series classification from scratch with deep neural networks: A strong baseline,” in Proc. Int. Joint Conf. Neural Netw. (IJCNN), May 2017, pp. 1578–1585.

[52] W. Samek, A. Binder, G. Montavon, S. Lapuschkin, and K.-R. Muller, “Evaluating the visualization of what a deep neural network has learned,” IEEE Trans. Neural Netw. Learn. Syst., vol. 28, no. 11, pp. 2660–2673, Nov. 2017.

![](images/64846d82053702629ad030a2c3beb025c9ff5719e2fe335060e1702281a31a3e.jpg)

Yongming Chen (Graduate Student Member, IEEE) received the B.E. degree in communication engineering from Harbin Institute of Technology, Weihai, China, in 2020, and the M.S. degree in signal processing from Nanyang Technological University, Singapore, in 2022, where he is currently pursuing the Ph.D. degree with the School of Electrical and Electronic Engineering.

His research interests include machine learning, time-series analysis, and signal processing.

Hongsheng Lan received the B.S. degree in information engineering from Beijing University of Posts and Telecommunications, Beijing, China, in 2023, and the M.S. degree in signal processing from Nanyang Technological University, Singapore, in 2025.

His current research interests include trafic classification and trafic anomaly detection.

![](images/bce1d4783793ba7afc2d3abb50b834b82426febdf18394f21b55f2bbf724239d.jpg)

![](images/192b4f5de11e7bc067c460ac3a6684407e0a320f36d4107d6a5d72cc722a3de1.jpg)

University of Singapore, as an Associate Professor (Practice), in January 2026. His research interests include computational intelligence, data analytics, software engineering education, and technology enhanced learning with virtual reality (VR) and augmented reality (AR).

Qi Cao received the B.Eng. degree from the Huazhong University of Science and Technology (HUST), Wuhan, China, in 2000, and the Ph.D. degree from Nanyang Technological University, Singapore, in 2007.

![](images/b30db57017105550d9f51b233ff8d7cdfcd49c4e258a7280d5b43e02950c1ee8.jpg)

Since 2024, he has been an Associate Professor with the School of Computing Science, University of Glasgow, U.K. From 2019 to 2024, he was an Assistant Professor with the School of Computing Science, University of Glasgow. He will join the Department of Statistics and Data Science, National

Bah Hwee Gwee (Senior Member, IEEE) received the B.Eng. degree from the University of Aberdeen in 1990 and the M.Eng. and Ph.D. degrees from Nanyang Technological University in 1992 and 1998, respectively.

He is currently an Associate Professor and an Associate Chair (Students) with the School of EEE, NTU, and the Director of the National Integrated Centre for Evaluation (NiCE). He has led research projects totaling over USD 15 million, including major grants from MOE Tier-2, ASEAN-EU, DSO,

![](images/b7969bfec2fcead86f89e5fe2ccf95e4982c564f64b80e7b4cc01c037d770cef.jpg)

From 2004 to 2009, he was a Faculty Member with the School of EEE, Nanyang Technological University. He joined Temasek Laboratories@NTU

Sirajudeen Gulam Razul received the B.Eng. and M.Eng. degrees in electrical and electronics engineering from Nanyang Technological University, Singapore, in 1997 and 2000, respectively, and the Ph.D. degree from the University of Cambridge, U.K., in 2003. His Ph.D. work was on Bayesian estimation using Markov Chain Monte Carlo techniques.

in 2009. He is currently the Program Director of the Centre for Communications and Signal Processing, TL@NTU. His research interests include Bayesian signal processing, statistical signal processing, and array processing.

![](images/e27d5c618864bb264d139c937f41dfbd757b835456848a7e1de8563baa4bd95a.jpg)

NTU-Panasonic, US DARPA, A\*STAR, CSA, and NRF. He has published more than 200 articles, five U.S. patents granted, and founded two startups. His research interests include machine learning, hardware security, image processing, and asynchronous circuits.

Zhiping Lin (Life Senior Member, IEEE) received the Ph.D. degree in information engineering from the University of Cambridge, U.K., in 1987.

Since 1999, he has been an Associate Professor with the School of EEE, Nanyang Technological University (NTU), Singapore. He is currently the Program Director of the Master of Science, School of EEE, NTU. Prior to that, he was with DSO National Laboratories, Singapore, and Shantou University, China. He has published more than 400 journal articles and conference papers. His research

interests include signal processing and machine learning. He was the Editorin-Chief of Multidimensional Systems and Signal Processing from 2011 to 2015 and served as an associate editor for several other international journals. He was an IEEE CASS Distinguished Lecturer and served as IEEE CASS and SPS Singapore Chapter Chairs.
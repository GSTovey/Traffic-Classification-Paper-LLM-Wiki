# ARI-LLM: Autoregressive Imputation for Network Traffic Matrix via Large Language Models

Fenglin Yan<sup>†‡</sup>, Kaiwen Jiang<sup>†‡</sup>, Yan Qiao,<sup>∗‡§∗∗</sup> Meng Li<sup>∗‡§∗∗</sup>, Yuxuan Li<sup>¶</sup>, Peng Yu<sup>§</sup>, Cuiying Feng<sup>∥∗∗</sup>

<sup>‡</sup>School of Computer Science and Information Engineering, Hefei University of Technology; <sup>§</sup>State key Laboratory of Networking and Switching Technology, Beijing University of Posts and Telecommunications; <sup>∗∗</sup>Key Laboratory of Knowledge Engineering with Big Data (Hefei University of Technology), Ministry of Education

<sup>¶</sup>Faculty of Computer and Mathematical Science, The Hong Kong Polytechnic University

<sup>∥</sup>School of Information and Software Engineering, University of Electronic Science and Technology of China

Abstract—The Traffic Matrix (TM) plays a vital role in a wide range of network management tasks, yet monitoring complete TMs is prohibitively expensive. Recent efforts focus on recovering incomplete TMs via learning-based models by learning from historical TM snapshots. However, existing approaches often suffer from poor generalization and require frequent retraining when the network environment evolves—let alone unseen networks. In this paper, we propose a novel TM imputation framework, named ARI-LLM, based on Large Language Models (LLMs). Inspired by human-like cognitive process of coarse-tofine reasoning, our method incrementally refines the incomplete TM through a step-wise autoregressive mechanism, which is compatible with the pretraining paradigm of LLMs, endowing our model with powerful generalization and zero-shot capabilities. To ensure plug-and-play deployment across TM imputation tasks in dynamic environments, we craft a flow-aware tokenization scheme that supports scalable and topology-adaptive embeddings. Extensive experiments demonstrate that ARI-LLM significantly outperforms state-of-the-art methods on large-scale sparse TMs (over 90% missingness), reducing imputation error by up to 34.7%. It maintains strong performance whether given only limited TM knowledge (e.g., 20% observed flows, 5% training snapshots) or no prior knowledge at all on unseen networks.

Index Terms—Network measurement, traffic matrix imputation, large language models, autoregressive learning.

## I. INTRODUCTION

A Traffic Matrix (TM) represents the set of traffic volumes exchanged between nodes in a network over a given time interval. Accurately monitoring the TM is crucial for a wide range of downstream network tasks, such as capacity planning [1], anomaly detection [2], and traffic engineering [3] [4].

TMs can be collected using diverse techniques, including SNMP [5] [6], NetFlow [7], OpenTM [8], or methods based on routing information [9] [10]. However, as network scales continue to expand, directly measuring all OD flows by capturing each packet trace incurs prohibitively high administrative and computational costs [11] [12]. Even worse, missing values in TMs are often inevitable in most real-world networks, with missing rates of over 90% being fairly common. Beyond costsaving considerations, several practical constraints account for this phenomenon [13]. Firstly, many networks are undergoing a transition between legacy and modern devices, and not all devices are equipped with the capability to monitor and store

![](images/b6b780f2bb5dbf20418e503bd403fb66ef3da01934f95ee17705f4b9b8597126.jpg)  
(a) One-step imputation vs. autoregressive imputation

![](images/0a23206058acd9c5b9f19e1952fb768e149aa18d6eb1750b7c973e9316950381.jpg)  
(b) Low generalization vs. high generalization

Fig. 1. Illustration of previous models vs. our proposed model. (a) Previous models apply one-step imputation to recover the entire TM in a single pass, whereas our autoregressive model iteratively predict a finer TM based on a coarser one. (b) Previous models require retraining once new flows are involved, whereas our model adapts to new flows without retraining.

the enormous flow-level traffic data. Secondly, for privacypreserving reasons, monitoring end-to-end traffic is often prohibited in certain sensitive regions of the network. Lastly, even if all devices support flow-level monitoring and no privacy restrictions are imposed, the collected TM is often incomplete due to practical issues such as device failures or network congestion. Therefore, due to the high cost of comprehensive monitoring or unavoidable practical limitations, accurately recovering missing TM entries is critically important for effective downstream network optimization tasks.

With the rapid advancements in neural network technologies, learning-based TM imputation methods [14] have surpassed traditional low-rank matrix factorization approaches [15] [16], becoming the new state-of-the-art. These methods first learn TM patterns from historical snapshots, and then recover the missing flows by inferring the most likely values that align with the learned pattern based on the observed flows [17]. However, these methods face several critical challenges in practical deployments: (1) High uncertainty in one-step imputation. Almost all existing methods adopt a one-step imputation strategy (as illustrated in the top part of Fig. 1(a)). Such learning paradigm tends to be unstable, particularly under high missing rates (e.g., over 90% missingness). With only one-step supervision, the model often fails to converge effectively, resulting in highly fluctuating outputs. (2) Limited model generalizability. Almost all imputation models are tailored to specific network configurations present in the training dataset. When the network topology changes—such as the addition or removal of nodes—it becomes necessary to recollect training data, redesign the neural architecture, and retrain the model from scratch, incurring significant human and computational overhead. (3) Dependence on rich historical TM data. Many methods assume the availability of a long-term TM training data to learn the traffic pattern comprehensively. However, in practice, especially in dynamic or constrained networks, obtaining a long period of TM data is extremely difficult, making it challenging to train the model adequately.

Since the TM data in practical networks is often limited (either incomplete or with short term) and network structures often frequently evolve, a fundamental question raises: Can we develop a TM imputation method that, once trained—even with limited TM measurements—can be plug-and-play across diverse network environments? Ideally, such a method should accurately recover highly sparse TMs, generalize well to network changes without retraining, and even perform zero-shot imputation on entirely unseen networks with unknown topologies and TM prior knowledge.

The emerging large language models (LLMs), with their powerful pretrained knowledge and zero-shot reasoning capabilities, offer new opportunity for addressing the above challenges. Recently, the rapid advancement of LLMs has led to transformative breakthroughs across a wide range of domains [18] [19] [20]. Although a few recent LLM-based models have been developed for networking-related tasks [21] [22], most of them treat LLMs merely as typical neural networks, applying end-to-end training or fine-tuning strategies. In fact, the powerful comprehension ability of LLMs is largely attributed to their autoregressive training paradigm that mimics human learning processes [23].

In this paper, we take the first step toward designing an LLM-based model tailored for TM imputation tasks. Inspired by the autoregressive training paradigm of LLMs, our model adopts a coarse-to-fine autoregressive imputation strategy (as illustrated in the bottom of Fig. 1(a)), which closely aligns with human cognitive processes. Compared to one-step imputation, the autoregressive paradigm not only enables LLMs to quickly grasp the underlying essence of the TM imputation task but also enhances reasoning stability.

Furthermore, to ensure high generalization capability to dynamic network changes or even unseen networks, we craft a tokenization scheme for the TM imputation. Specifically, different from conventional tokenization strategies that treat time steps as basic units, we instead perform tokenization at the level of individual flows. Additionally, we demonstrate both theoretically and empirically that including all flows in each training epoch does not always lead to expected performance;

instead, there exists an optimal number of flows that maximizes the model’s effectiveness. This design offers two key advantages: First, flow-level tokenization allows the model to flexibly adapt to TM dimensional changes by simply adjusting the number of input tokens—just like LLMs handle sentences of varying lengths—without requiring any modifications to the model’s input layer (as illustrated in Fig. 1(b)). Second, flowlevel tokenization allows the model to better exploit spatial correlations among flows. Compared to traditional time-series dependencies, capturing inter-flow correlations in networks is more critical for accurate TM imputation.

In summary, this paper makes the following key contributions to the field of TM measurement:

• We propose an LLM-based method for TM imputation, which adopts a coarse-to-fine imputation strategy to mimic human-like reasoning and fully exploit the capabilities of LLMs. Specifically, we decompose the input TM data into a sequence of multi-resolution representations, and employ an autoregressive framework that enables the model to progressively predict a finer-resolution TM conditioned on the coarser one.

• We design a flow-aware tokenization scheme, taskspecific prompt template, and lightweight fine-tuning strategy for TM imputation, enabling the LLMs to effectively align with the TM imputation tasks. These designs allow the model to handle dynamic network environments without requiring any structural modifications or retraining. They also endow the model with strong few-shot and zero-shot learning capabilities, making it possible to seamlessly transfer to unseen network environments.

• We conduct extensive experiments on three real-world TM datasets to compare ARI-LLM with the state-ofthe-arts. The results demonstrate that ARI-LLM achieves high accuracy under extreme sparsity (90%+ missing), improving the accuracy of the best baseline by up to 34.7%; generalizes well to network evolutions (only 7.1% drop on accuracy with 80% newly-added flows) and unseen networks (only 8.2% drop on average); converges rapidly (within 2∼3 training epochs).

## II. RELATED WORK

In this section, we first review the mainstream TM imputation methods, including traditional approaches, and learning-based approaches. Then we review recent advances in networking-related tasks using LLMs and highlight key differences between our method and existing approaches.

## A. Traditional TM Imputation

Traditional TM imputation methods include Network Tomography (NT)-based approaches and Matrix/Tensor Decomposition (M/TD)-based techniques.

NT-based methods estimate fine-grained OD flows using linear equations from link loads and the routing matrix. Since these equations are often rank-deficient, NT-based methods address the ill-posed problem by introducing assumptions about the TM distribution [24] [12] [25]. For instance, Vardi [24] and Tebaldi et al. [12] assumed a Poisson distribution for network traffic. Cao et al. [26] assume a Gaussian traffic model, while

Zhang et al. [27] applied a gravity model. M/TD-based methods first extract the principal components of the TM through matrix or tensor decomposition, and then reconstruct the full TM entries based on these components [15] [16]. Matthew et al. [16] utilized K-Nearest Neighbors (KNN) to model the similarity patterns among different OD pairs and introduced a spatial constraint matrix to improve imputation accuracy. Paul et al. [15] leveraged the principle of maximum entropy to reconstruct missing entries in TMs. Xie et al. [28] exploited the local structures of TMs to form lower-rank tensors from local correlations which significantly enhanced the imputation accuracy. Tian et al. [29] proposed a tensor-based imputation method that encodes continuous distance information into each tensor and integrates a sample selection mechanism to reduce the sampling rate. However, these methods perform well only under simple or idealized traffic distributions. They suffer from high computational costs and limited imputation performance when recovering intricate traffic flows.

## B. Learning-Based TM Imputation

To better capture the complex correlations within TM, recent studies have adopted neural networks for TM imputation. Xie et al. [14] proposed NTC, which captures third-order interactions among traffic features via outer products. DATC proposed in [17] leverages a generative adversarial network (GAN) to recover the missing values in tensor-structured TMs. Autotomo proposed in [30] addressed the challenge of TM estimation under incomplete and biased training data. Ouyang et al. [31] proposed LTP, which boosts recovery accuracy by combining time embeddings with attention-enhanced LSTM. Liu et al. [32] introduces a distributed tensor completion method based on convolutional neural networks (CNNs), enhancing both scalability and accuracy. Wang et al. [13] proposed PetTC, a pairwise joint embedding-based tensor completion method that improves TM imputation by leveraging crossdomain embeddings and contrastive learning. Despite their superior performance in capturing complex TM correlations, these methods still face notable limitations mentioned above.

## C. LLM-based Networking Approaches

LLMs have recently emerged as promising tools for generalpurpose networking applications. For example, Wu et al. [22] proposed NetLLM for diverse networking tasks, including viewport prediction, adaptive bitrate streaming, and cluster job scheduling. Cui et al. [21] introduced TrafficLLM, a dual-stage fine-tuning framework to learn generalizable traffic representations from heterogeneous data, enabling both traffic classification and packet generation. Zhou et al. [33] proposed a GPT-4- based software agent framework that simulates knowledgeable researchers to assist in Internet incident investigations. Despite the remarkable breakthroughs achieved by these methods, they remain inadequate for solving the TM imputation problem.

In contrast to the aforementioned methods, we propose an LLM-based model for TM imputation. To the best of our knowledge, this is the first TM imputation approach with strong generalization capabilities: it adapts to network changes and generalizes to entirely unseen network environments without model modification or retraining.

## III. METHODOLOGY

In this section, we present our proposed model, named ARI-LLM, which employs LLMs for flexible and generalizable imputation for severely missing TMs.

## A. Problem Formulation

We model the network as a graph $G ~ = ~ ( V , E )$ , where V denotes the set of nodes and E represents the set of links connecting them. Let $X _ { t } ~ = ~ \{ x _ { t 1 } , x _ { t 2 } , . . . , x _ { t N } \}$ , and $N = | V | \times | V |$ |, denotes the collection of traffic flows between all network nodes, at the t-th time point. The TM is typically formulated as a $T \times N$ matrix, $\mathbf { \bar { X } } \ = \ \{ X _ { 1 } , X _ { 2 } , . . . , { \bar { X } } _ { T } \} ^ { \top }$ represents the traffic flows measured during T time points. We use a sampling indication matrix M $\in \mathbb { R } ^ { \breve { T } \times N }$ to indicate the observed and missing values in X. $\operatorname { I f } x _ { t i }$ is observed, $m _ { t i } = 1 ;$ otherwise, $m _ { t i } = 0 .$ Let $\widetilde { \mathbf { X } } = \mathbf { M } \odot \mathbf { X }$ denote the TM with only the observed values, where ⊙ represents the element-wise product. In this paper, our goal is to recover all missing values in X given the observed values $\widetilde { \mathbf { X } }$

## B. Model Overview

The overall framework of our proposed ARI-LLM is illustrated in Fig. 2. ARI-LLM performs progressive TM imputation in an autoregressive manner. For a training sample of TM X, we first decompose it into sequences of different resolutions $\mathcal { X } = \{ \mathbf { X } ^ { ( 1 ) } , \mathbf { X } ^ { \mathsf { ( 2 ) } } , \ldots , \mathbf { X } ^ { ( h ) } \}$ }. At the s-th autoregressive step, the model predicts the next resolution $\mathbf { X } ^ { ( s + 1 ) }$ based on the current resolution $\mathbf { X } ^ { ( s ) }$ , until the high-fidelity TM Xb is generated. In each autoregressive step, the input TM $\mathbf { X } ^ { ( s ) }$ is firstly processed by a crafted Flow2Vec Embedder, which maps each flow onto the token space of the LLM. Simultaneously, a Prompt Embedder encodes the designed prompt into tokens. The two embeddings are then concatenated and fed into the LLM body, whose output is subsequently passed through a MLP to map it onto a finer-grained TM.

We next provide a detailed explanation of the key components of our framework, including the autoregressive imputation mechanism, the Flow2Vec Embedder, the design of the Prompt Template, the LLM body, and the lightweight finetuning strategy.

## C. Autoregressive Imputation Mechanism

Unlike existing methods that rely on one-step imputation, ARI-LLM adopts a novel autoregressive imputation mechanism that progressively predict the complete TM from coarse to fine granularity. On the one hand, under high missing rates, this multi-step imputation strategy significantly enhances the stability of the imputation process. On the other hand, this human-aligned, stepwise reasoning paradigm allows the LLMs to better capture the underlying traffic patterns, and grasp the essence of the TM imputation task.

To enforce LLMs to perform autoregressive imputation, two key problems must be addressed: First, how to determine the appropriate resolution for each imputation step; Second, how to effectively guide the model to generate the next, finergrained TM based on the current resolution.

To address the first problem, we develop a coarse-to-fine strategy that doubles the resolution of the observations at each autoregressive step, inspired by human-like imputation process. Consider a TM with a total length of w time steps: $\mathbf { \bar { X } } \ = \ \{ X _ { 1 } , X _ { 2 } , . . . , X _ { w } \} ^ { \top }$ , we aim to construct a set of observation index collections $\mathcal { T } = \{ \mathcal { T } ^ { 0 } , \mathcal { T } ^ { 1 } , \ldots , \mathcal { T } ^ { h } \}$ , where $\mathcal { Z } ^ { s }$ $( s = \{ 0 , 1 , \ldots , h \} )$ ) denotes the set of observed time indices at the s-th autoregressive step. The corresponding observations are represented as $\widetilde { \mathbf { X } } ^ { \left( s \right) } = \left\{ X _ { i } \in \mathbf { X } \vert i \in \mathcal { I } ^ { s } \right\}$

![](images/ba57cf9f4ab982bee39edb8c8035cd19f2c70d08de9630cc04d411c404cfe956.jpg)  
Fig. 2. The framework of ARI-LLM: the Multi-Head Attention layers of the pre-trained LLM are frozen to preserve general language modeling capabilities. The LLM Embedder is also frozen, while the Flow2Vec Embedder is fine-tuned to adapt to the traffic data. Additionally, the Normalization layers, Feed Forward layers, and MLP layer are trainable.

$\boldsymbol { \mathcal { T } ^ { ( 0 ) } }$ is initialized to include the starting and ending points. We then determine a minimum observation ratio $q \in \mathsf { \Gamma } ( 0 , 1 ]$ which controls the starting observation density. Let $K = \lfloor q w \rfloor$ denote the number of observed time points at the first step. Starting from $s = 1$ , we uniformly sample K indices across the entire time range to form the observation set $\boldsymbol { \mathcal { T } ^ { ( 1 ) } }$ . Then, at each autoregressive step $s \ ( s > 1 )$ , the model predicts new values at the midpoints between consecutive observed time steps. Therefore, $\dot { \mathcal { T } } ^ { ( s ) }$ can be uniformly formulated by:

$$
\mathcal {I} ^ {(s)} = \left\{ \begin{array}{l l} \{1, w \}, & s = 0, \\ \mathcal {I} ^ {(0)} \cup \left\{\left\lfloor \frac {i w}{K} \right\rfloor   \bigg |   i = 1, \ldots , K \right\}, & s = 1, \\ \mathcal {I} ^ {(s - 1)} \cup \left\{\left\lfloor \frac {t _ {i} + t _ {i + 1}}{2} \right\rfloor   \bigg |   t _ {i}, t _ {i + 1} \in \mathcal {I} ^ {(s - 1)} \right\}, s > 1. \end{array} \right.\tag{1}
$$

This progressive scheme doubles the observed points at each step, where the unobserved values are simply filled by linear interpolation between the two nearest observed neighbors. In doing this, we can construct a coarse-to-fine sequence of TMs: $\{ \mathbf { X } ^ { ( \tilde { 1 } ) } , \mathbf { X } ^ { ( 2 ) } , \ldots , \mathbf { X } ^ { ( h ) } \}$ , where ${ \bf X } ^ { ( s ) } = L i n e a \dot { r } I n t e r p ( \widetilde { \bf X } ^ { ( s ) } )$ , $s = \{ 1 , 2 , \ldots , h \}$

Moreover, ARI-LLM reduces drift in TM imputation by iteratively refining predictions through a correction-based autoregressive strategy, instead of relying on single-pass end-toend prediction. At each step $s ,$ the model generates a finergrained TM $\mathbf { X } ^ { ( s + 1 ) }$ based on the previously imputed result $\bar { \mathbf { X } } ^ { ( s ) }$ . This process is guided by two mechanisms: a loss term that penalizes the discrepancy between the predicted $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ and the ground-truth $\mathbf { X } ^ { ( s + 1 ) }$ , and task-specific prompts that instruct the LLM to perform finer-grained reasoning.

Considering the significant variability in traffic magnitudes in TM, we adopt the Symmetric Mean Absolute Percentage Error (SMAPE) [34] as the loss function to balance differences across TMs of varying resolutions. Specifically, for the predicted matrix $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ at step s, and the corresponding groundtruth matrix $\mathbf { X } ^ { ( s + 1 ) }$ , the SMAPE loss is defined as:

$$
\mathcal {L} _ {\mathrm{SMAPE}} ^ {(s + 1)} = \frac {1}{w} \sum_ {i = 1} ^ {w} \frac {| | \widehat {\mathbf {X}} _ {i} ^ {(s + 1)} - \mathbf {X} _ {i} ^ {(s + 1)} | | _ {1}}{(| | \widehat {\mathbf {X}} _ {i} ^ {(s + 1)} | | _ {1} + | | \mathbf {X} _ {i} ^ {(s + 1)} | | _ {1}) / 2 + \epsilon},\tag{2}
$$

where $| | \cdot | | _ { 1 }$ denotes the L1-Norm, and ϵ is a small constant added for numerical stability to avoid division by zero.

To enable the LLMs to comprehend the reasoning process from coarse to fine, we design the prompt template as illustrated in the Instruction and Stage part in Fig. 4. Specifically, Instruction guides the model to impute the TM progressively over h stages. The Stage specifies the observation ratio at each stage and indicates the target resolution of the next stage.

## D. Flow2Vec Embedder

Existing LLM-based models for time series tasks typically treat the full set of observations at each time step as a single unit [18] [35] [36], which is then embedded into the token space of the LLMs. While these approach facilitate learning temporal dependencies across different time series, it inherently requires the input layer to be explicitly tailored to a fixed input dimension. Consequently, when the number of features varies, the input layer must be modified accordingly and the model must be retrained.

To address this limitation and accommodate the dynamic nature of network environment, we propose a novel embedding module, Flow2Vec, which treats each individual traffic flow as an unit. For each flow, we fix a temporal window of length $w ,$ treating it as the input dimension. Each flow is represented as a $w \times 1$ vector, which is then embedded into a $d \times 1$ token with the same dimensionality as the word embeddings used in LLMs. Thus, each flow corresponds to a single token, enabling the model to predict the next set of tokens by capturing correlations among the current tokens via self-attention. This design ensures that the model remains structurally consistent regardless of changes in the number of flows within the TM, just as LLMs can handle sentences of varying lengths. To ensure that the model can still learn the temporal dependencies within each flow, the Flow2Vec embedder incorporates an LSTM encoder to extract temporal features from each flow over the fixed-length window.

The embedding process of Flow2Vec is illustrated in Fig. 3, at the s-th step of the autoregressive process, the current TM $\mathbf { X } ^ { ( s ) } \in \mathbb { R } ^ { w \times n }$ is first transposed and then fed into an LSTM encoder to extract temporal dependencies. It is subsequently embedded into flow-level token embeddings $\mathbf { E } _ { \mathrm { T M } } ^ { ( s ) } \in \overline { { \mathbb { R } ^ { n \times d } } }$ which are finally input to the LLM for self-attention learning to capture spatial correlations among flows.

![](images/eb8e9c1f6aef52e70c2536f380eb86fcf6611761811c931301ec237a4284e40f.jpg)  
Fig. 3. TM embedding process through Flow2Vec.

Although incorporating more flows in each input allows the LLMs to extract richer inter-flow information, we provide the following theorem to show that increasing the number of flows beyond a certain threshold yields diminishing returns.

Theorem 1 (Optimal Number of Input Flows for LLMs). Assume a TM $\textbf { X } \in \mathbb { R } ^ { w \times n }$ has rank r, where n is the total number of flows and w is the time length. Consider a Transformer-based LLM architecture, where each flow is embedded as a token vector and fed into the model. Then, the optimal number of input flows $n ^ { * }$ to the LLM that maximizes the imputation performance is $n ^ { * } = r .$

Proof. We prove the theorem by analyzing the trade-off between information completeness and model complexity in the context of TM imputation.

Since the TM X is rank-r, all the intrinsic spatial-temporal information of the matrix lies in an r-dimensional subspace. Thus, observing fewer than r flows $( n < r )$ implies incomplete coverage of this subspace, resulting in a biased and underdetermined model that cannot fully reconstruct the TM. Consequently, increasing the number of input flows n for $n \leq r$ leads to a strict decrease in reconstruction error:

$$
\frac {d \mathcal {E} _ {r e c} (n)}{d n} <   0, \quad \text { for } n \leq r,
$$

where $\mathcal { E } _ { r e c } ( n )$ denotes the prediction error as a function of input flow count.

When $n > r .$ , additional flows provide redundant or nearly linearly dependent information. While the intrinsic information content saturates at r flows, increasing n further introduces several negative effects: (1) Computational overhead: transformer self-attention complexity scales quadratically with input sequence length, increasing training and inference costs; (2) Model overfitting and noise sensitivity: excessive input tokens increase model capacity requirements and raise variance, which harms generalization under limited training data.

Hence, for $n > r ,$ prediction error tends to increase with n:

$$
\frac {d \mathcal {E} _ {r e c} (n)}{d n} > 0, \quad \text { for } n > r.
$$

Combining the above two results, $\mathcal { E } _ { r e c } ( n )$ is a unimodal function with a minimum at $n = r .$ □

According to Theorem 1, the optimal number of flows can be determined by the degree of spatiotemporal correlation of the underlying network’s TMs. The stronger the spatiotemporal correlation the smaller of the rank $r ,$ and consequently, fewer flows need to be fed into the LLMs in each batch; otherwise, more flows are required. In Section IV.B, we empirically verified the optimal number of flows for each dataset.

Remark 1. Ideally, each batch of inputs to the LLM should consist of r independent flows. However, in real-world networks, the true value of r is often unknown and can only be empirically estimated. Moreover, due to missing data, it is difficult to identify truly independent flows. In our experiments, we randomly divide theflows into $\lceil T / r \rceil$ groups for batch-wise input, which has already achieved satisfactory performance.

## E. Prompt Template

To leverage the pretrained knowledge of LLMs for the TM imputation task, we design a prompt template as illustrated in Fig. 4. The starting observation ratio q is set to 2%.

```txt
[Database]: The Abilene dataset contains 12 routers from the U.S. Internet2 Network, 30 directed inner links, and 24 outside links. The dataset collected the volumes of all OD flows in the network every 5 minutes from March to September 2004. Below is the information about the input time series:

[Domain]: The dataset consists of 12 routers (v1-v12) with 144 OD flows (x1-x144). Each flow xij represents traffic from vi to vj, indexed as (i-1)*12+j (i,j∈1..12). Temporal sequence length: [seq len] time points. The current traffic matrix has [known_rate] known rate with 1 - [known_rate] missing data. Missing values are initially imputed using two observed neighbors linear interpolation along columns. During the training process, we select fixed-interval rows as sampled data.

[Instruction]: Learn spatiotemporal patterns in traffic flows, perform progressive matrix imputation through six refinement stages:

[Stage]: 2% → 4%, 4% → 8%, 8% → 16%, 16% → 32%, 32% → 64%, 64% → 100% (current observed data → target filling). Current stage is [known rate]→[target rate].

[Input statistics]: Min value is [min value]. Max value is [max value]. Median value [median value].
```  
Fig. 4. Example of a prompt template for TMs imputation in the Abilene dataset with starting ratio of 2%: [] represents task-specific configurations and data statistics. [] indicates the start of a specific type of prompt.

The prompt structure contains a Head section describing dataset fundamentals (including name, network topology, and sampling methodology) and a Load section with four key components: (a) Domain specifies the TM dimensions and data properties; (b) Instruction details our autoregressive imputation strategy and task requirements; (c) Stage indicates the current phase $( \mathrm { e . g . } ,$ 2% observed data) and target phase (e.g., 4% observed data) of the refinement process; (d) Statistics provide key metrics (minimum, maximum, and median values) of the TM. This crafted prompt template allows the LLMs to properly understand both our coarse-to-fine imputation mechanism and the inherent traffic patterns within TMs.

For a given TM X, we first generate a prompt based on the prompt template. This prompt is then embedded into the token embeddings using the LLM’s native tokenization module, resulting in a prompt embedding $\mathbf { E _ { \mathrm { p r o m p t } } }$ that shares the same dimensionality as the TM embedding processed by Flow2Vec. The two embeddings are then concatenated and fed into the LLM body for further processing.

## F. LLM Body

The input to the LLM body is constructed by concatenating the TM embedding and the prompt embedding:

$$
\mathbf {E} = [ \mathbf {E} _ {\mathrm{TM}}, \mathbf {E} _ {\mathrm{prompt}} ] \in \mathbb {R} ^ {(n + m) \times d},\tag{3}
$$

where $\mathbf { E } _ { \mathrm { T M } } \in \mathbb { R } ^ { n \times d }$ is the embedding of n traffic flows and $\mathbf { E } _ { \mathrm { p r o m p t } } \in \mathbb { R } ^ { m \times d }$ is the prompt embedding, where m denotes the number of prompt tokens, and both embeddings share the same token dimension d.

This concatenated input E is then sequentially passed through L layers of the Transformer-based LLM. Each layer consists of a Multi-Head Attention module (denoted by $\mathrm { A t t } ( ) )$ a residual connection followed by a layer Normalization (denoted by Norm()), and a Feed Forward network (denoted by FF()). Specifically, for each Transformer layer l, the transformation is given by:

$$
\mathbf {H} ^ {(l)} = \operatorname{FF} \left(\operatorname{Norm} \left(\mathbf {H} ^ {(l - 1)} + \operatorname{Att} \left(\mathbf {H} ^ {(l - 1)}\right)\right)\right),\tag{4}
$$

where ${ \bf H } ^ { ( 0 ) } = { \bf E }$ , and $\mathbf { H } ^ { ( l ) } \in \mathbb { R } ^ { ( n + m ) \times d }$ denotes the output of the l-th layer. After passing through all L layers, we obtain the final hidden representation: $\mathbf { X } _ { \mathrm { o u t } } = \mathbf { H } ^ { ( L ) }$

To isolate the model’s prediction for the traffic flows, we discard the first m rows of $\mathbf { X _ { \mathrm { o u t } } }$ corresponding to the prompt tokens. The remaining n rows form the TM-related output: ${ \bf X } _ { \mathrm { T M } } ^ { \mathrm { o u t } } = { \bf X } _ { \mathrm { o u t } } [ m + 1 \ : ]$ , which is then fed into a multilayer perceptron (MLP()) to produce the final prediction of TM:

$$
\widehat {\mathbf {X}} = \operatorname{MLP} \left(\mathbf {X} _ {\mathrm{TM}} ^ {\text { out }}\right).\tag{5}
$$

## G. Lightweight Fine-Tuning

To maintain the model’s pre-trained knowledge while adapting it to the imputation task, we employ a lightweight finetuning approach. Specifically, while keeping the Multi-Head Attention layers frozen to preserve their learned representations, we selectively update only four critical components: the Flow2Vec weights $\left( \Theta _ { \mathrm { f } 2 \mathrm { v } } \right)$ to tokenize the TM data, the Normalization weights $\left( \Theta _ { \mathrm { n o r m } } \right)$ to maintain stable feature scale, the Feed Forward weights $( \Theta _ { \mathrm { f f } } )$ to facilitate non-linear feature transformations, and the MLP weights $\left( \Theta _ { \mathrm { m l p } } \right)$ to map the outputs onto the TM space.

The detailed fine-tuning algorithm is presented in Alg. 1. It inputs a set of training TMs X, an initial observation ratio q, and a learning rate η. It outputs the trained parameters $\Theta _ { \mathrm { l l m } } .$ that comprises $\Theta _ { \mathrm { f } 2 \mathrm { v } } , \Theta _ { \mathrm { n o r m } } , \Theta _ { \mathrm { f f } } ,$ and $\Theta _ { \mathrm { m l p } }$

The algorithm first initializes the model parameters and the observation index (line 1). Then it calculates the initial number of observations K and the total number of resolutions h (line 2∼3), and performs the autoregressive imputation through h loops (line 4∼15). In each loop, it first determines the observed indices $\boldsymbol { \mathcal { T } ^ { ( s ) } }$ and $\mathcal { T } ^ { ( s + 1 ) }$ based on Eqn. (1) (line 5). Linear interpolation is then applied to the observed traffic flows to generate the TM in current and next resolutions $\mathbf { X } ^ { ( s ) }$ and $\bar { \mathbf { X } } ^ { ( s + 1 ) }$ , respectively (line 6). It transposes $\mathbf { X } ^ { ( s ) }$ and feeds it into the Flow2Vec to generate the flow-level embedding $\mathbf { E } _ { \mathrm { T M } } ^ { ( s ) }$ (line 7). Then, the prompt corresponding to $\mathbf { X } ^ { ( s ) }$ is processed by the LLM Embedder to generate the prompt embedding $\dot { \mathbf { E } _ { \mathrm { p r o m p t } } ^ { ( s ) } }$ (line 8). The two embeddings are then concatenated to form the embedding $\mathbf { E } ^ { ( s ) }$ as the input to the LLM (line 9). After passing $\mathbf { E } ^ { ( s ) }$ through the LLM, it obtains the output of the last hidden layer, denoted as $\mathbf { X } _ { \mathrm { o u t } } ^ { ( s ) }$ (line 10). The first m prompt tokens is cut off to obtain an output for the TM (line 11), which is then passed through an $\bf M L P$ to produce the final prediction $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ (line 12). The loss between the imputed matrix $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ and the ground truth $\mathbf { X } ^ { ( s + 1 ) }$ is computed in terms of SMAPE (line 13) and added to the total loss L (line 14). When the iterations terminate, it backpropagates the total loss L (line 16), and applies gradient descent to update all trainable parameters (line 17). Note that in the final iteration, the generated X<sup>ˆ</sup> <sup>(h+1)</sup> corresponds to the fully recovered TM Xb , while $\mathbf { X } ^ { ( h + 1 ) }$ is the ground-truth TM X. The associated index set $I ^ { ( h + 1 ) } = \{ 1 , 2 , \cdot \cdot \cdot , w \}$ includes all time points.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Fine-Tuning Algorithm of ARI-LLM
Input:  $X = \{X_{1}, X_{2}, \ldots, X_{w}\}^{\top}$ , q,  $\eta$ 
Output: Trained parameters  $\Theta_{llm} = \{\Theta_{f2v}, \Theta_{norm}, \Theta_{ff}, \Theta_{mlp}\}$ 

1: Initialize:  $\Theta_{llm}$ ,  $\mathcal{I}^{(0)} \leftarrow \{1, w\}$ ;
2:  $K = \lfloor qw \rfloor$ ;
3:  $h = \lceil \log_{2} w / K \rceil$ ;
4: for s = 1 to h do
5: Compute  $\mathcal{I}^{(s)}$  and  $\mathcal{I}^{(s+1)}$  by Eqn. (1);
6:  $\mathbf{X}^{(s)} \leftarrow LinearInterp(\{X_i \in \mathbf{X} \mid i \in \mathcal{I}^s\})$ ,
 $\mathbf{X}^{(s+1)} \leftarrow LinearInterp(\{X_i \in \mathbf{X} \mid i \in \mathcal{I}^{s+1}\})$ ;
7:  $\mathbf{E}_{\mathrm{TM}}^{(s)} \leftarrow Flow2Vec((\mathbf{X}^{(s)})^\top, \Theta_{f2v})$ ;
8:  $\mathbf{E}_{prompt}^{(s)} \leftarrow LLMEmbedder(Prompt(\mathbf{X}^{(s)}))$ ;
9:  $\mathbf{E}^{(s)} \leftarrow [\mathbf{E}_{\mathrm{TM}}^{(s)}; \mathbf{E}_{prompt}^{(s)}]$ ;
10:  $\mathbf{X}_{out}^{(s)} \leftarrow LLM(\mathbf{E}^{(s)}; \Theta_{norm}, \Theta_{ff})$ ;
11:  $\mathbf{X}_{\mathrm{TM}}^{\mathrm{out}(s)} \leftarrow \mathbf{X}_{\mathrm{out}}^{(s)}[m + 1:]$ ;
12:  $\widehat{\mathbf{X}}^{(s+1)} \leftarrow MLP(\mathbf{X}_{\mathrm{TM}}^{\mathrm{out}(s)}; \Theta_{\mathrm{mlp}})$ ;
13:  $L_s \leftarrow SMAPE(\widehat{\mathbf{X}}^{(s+1)}, \mathbf{X}^{(s+1)})$ ;
14:  $L \leftarrow L + L_s$ ;
15: end for
16:  $\nabla_{\Theta_{llm}}L \leftarrow Backpropagation(L)$ ;
17:  $\Theta_{llm} \leftarrow \Theta_{llm} - \eta\nabla_{\Theta_{llm}}L$ 
18: return  $\Theta_{llm}$
</div>

## IV. EXPERIMENTS

In this section, we conduct comprehensive experiments to evaluate ARI-LLM. We compare our method with seven stateof-the-art baselines on three benchmark datasets.

## A. Experimental Setup

1) Datasets: We use three real-world datasets from different network environments. The Abilene dataset [9], contains OD flows’ measurements between 12 network nodes, recorded every 5 minutes over a period of 168 days. The GEANT<sup>´</sup> dataset [37], contains the flows between 23 nodes, taken every 15 minutes for 112 consecutive days. The WS-DREAM dataset [38] focuses on throughput measurements between 4,500 web services and 142 users, collected at 15-minute intervals during 64 continuous time slots. We split each dataset into training, validation, and testing sets in an 8:1:1 ratio.

2) Evaluation Metrics: Following most imputation methods, we employ three metrics: Normalized Mean Absolute Error (NMAE), Normalized Root Mean Square Error (NRMSE) and Kullback-Leibler Divergence (KL) to evaluate the performance of imputation methods. NMAE and NRMSE evaluate the errors of the predicted values compared to the ground truth. KL divergence measures the similarity between the distributions of the predicted and real TM data, where a smaller KL value implies a closer match.

Table I presents the formulas for each metric. Here, $x _ { i j }$ and $\hat { x } _ { i j }$ denote the real and predicted values of the $j \mathrm { - t h }$ OD flow at time point i in X and ${ \widehat { \mathbf { X } } } ,$ , respectively. $\begin{array} { r l } { p _ { i j } } & { { } = } \end{array}$ $\begin{array} { r l r } { \frac { x _ { i j } } { \sum _ { ( i , j ) \in \bar { \Phi } } x _ { i j } } , } & { { } \hat { p } _ { i j } } & { = \frac { \hat { x } _ { i j } } { \sum _ { ( i , j ) \in \bar { \Phi } } \hat { x } _ { i j } } } \end{array}$ represent the probability density function of the real and predicted flows, respectively. Φ and $\overline { { \Phi } }$ denote index sets of observed and unobserved data. These metrics are computed solely on unobserved data.

TABLE I PERFORMANCE METRICS

<table><tr><td>Method</td><td>Formula</td></tr><tr><td>NMAE</td><td>$ \frac{\sum_{(i,j)\in\bar{\Phi}}|x_{ij}-\hat{x}_{ij}|}{\sum_{(i,j)\in\bar{\Phi}}|x_{ij}|} $</td></tr><tr><td>NRMSE</td><td>$ \frac{\sqrt{\sum_{(i,j)\in\bar{\Phi}}(x_{ij}-\hat{x}_{ij})^2}}{\sqrt{\sum_{(i,j)\in\bar{\Phi}}x_{ij}^2}} $</td></tr><tr><td>KL</td><td>$ \sum_{(i,j)\in\bar{\Phi}}p_{ij}\log\left(\frac{p_{ij}}{\hat{p}_{ij}}\right) $</td></tr></table>

3) Baselines: We compare TM-LLM with 7 representative imputation methods, which can be categorized into three groups: (1) deep network embedding methods including CoSTCo [39], NTC [14], NTM [40], and PetTC [13], (2) temporal network embedding methods, including NTF [41] and LTP [31], and (3) GAN-based method DATC [17]. Among them, NTC, DATC, LTP and PetTC are specifically designed for network TM imputation, while NTM, NTF, CoSTCo are widely applied in recommendation systems.

4) Experimental settings: All experiments were conducted on a single NVIDIA Tesla A800 80G GPU. We employed GPT-2 (124M) as our base pre-trained model. The initial observation rate $q = 0 . 0 2$ . We set the window size $w = 5 0$ for each input TM. The results presented below represent the average of five runs, adhering to the experimental settings outlined in [13]. Further detailed settings of our experiments are available at https://github.com/JKevin17/ARI-LLM.

## B. Optimal Flow Number for Each Dataset

As mentioned in Section III.D, there exists an optimal number of flows for best performance. We validate this empirically in this subsection under the observation rate of 10%.

Fig. 5 illustrates imputation errors in terms of NMAE and training time under different numbers of input flows. According to Fig. 5, as the number of input flows increases, the imputation error initially declines, and then either stabilizes or increases slightly. For the Abilene dataset, the number of input flows required to achieve the lowest imputation error is nearly equal to the total number of flows in the network. This indicates the spatiotemporal correlations among flows are not particularly strong. In contrast, for the GEANT dataset,<sup>´</sup> the imputation error stabilizes when the number of input flows reaches approximately 300, indicating relatively stronger spatiotemporal correlations among flows in the GEANT net-<sup>´</sup> work. For WS-DREAM, the lowest error occurs at 550 input flows. Moreover, as the number of input flows increases, the model becomes harder to train, resulting in significantly longer training times. Based on this analysis, we set the number of input flows to 144 for Abilene, 300 for GEANT, and 550 for<sup>´</sup> WS-DREAM in the subsequent experiments.

![](images/5617acbe404f482205d454e22cc0b4be39eb43934152236e609dfcc9da1d9ec1.jpg)  
(a) Abilene

![](images/3a9d268d1aafafbaf4c10df5c5f9be5773170bef025a46cea6df7e7e2f310ac5.jpg)  
(b) GEANT<sup>´</sup>

![](images/8340964ec3a36c5d5d8b1709c33999bb1a417ff3bd647daaa52e29b6ba487ba0.jpg)  
Fig. 5. The optimal number of input flows for the three datasets.

## C. Imputation Performance under Various Sampling Rates

Table II summarizes the performance of the eight TM imputation methods on three datasets under extremely low observation rates (OR) from 2% to 10%. From the table, ARI-LLM achieves the best performance on nearly all metrics, consistently outperforming the other seven baselines.

Specifically, compared to the best-performing baseline PetTC, ARI-LLM improves the NMAE by $1 1 . 8 \% \sim 1 8 . 1 \%$ on Abilene, 0.8% ∼ 8.6% on GEANT, and<sup>´</sup> $2 7 . 9 \% \sim 3 4 . 7 \%$ on WS-DREAM. For the NRMSE metric, the gains are 3.7% ∼ 11.8% on Abilene, $2 . 3 \% \sim \ 1 3 . 9 \%$ on GEANT,<sup>´</sup> and $1 4 . 3 \% \sim \ 2 2 . 8 \%$ on WS-DREAM, respectively. The accuracy gains are especially pronounced on WS-DREAM, which involves high-dimensional traffic data, indicating the model’s strong robustness in large-scale networks.

From different observation ratios, ARI-LLM averagely reduces the best-performing baseline’s errors by 13.2%, 14.6%, 16.2%, 16.5%, and 19.6% under the observation rates from 10% to 2%, respectively. The performance gap widens as the observation rate decreases, demonstrating our model’s robustness under sparse imputation scenarios.

Regarding KL divergence, ARI-LLM achieves average improvements of 25.6% on Abilene, 37.3% on GEANT, and<sup>´</sup> 30.8% on WS-DREAM. This demonstrates ARI-LLM can generate TMs that are significantly closer to the true distribution. The above results highlight the powerful TM imputation and pattern learning capability from the synergy between autoregressive imputation and the pretrained LLM.

## D. Ablation Study

To verify the effectiveness of the key designs in ARI-LLM, we conduct an ablation study by implementing two variants of the model: ARI-LLM w/o Prompt and ARI-LLM w/o AR. ARI-LLM w/o Prompt discards the prompt input, relying solely on TM input without textual guidance. ARI-LLM w/o AR removes the autoregressive learning/imputation mechanism, and applies a single-step imputation strategy.

TABLE II  
IMPUTATION PERFORMANCE ON ABILENE, GEANT<sup>´</sup> AND WS-DREAM. BOLD: BEST, UNDERLINED: SECOND BEST.

<table><tr><td colspan="2">Dataset</td><td colspan="5">Abilene</td><td colspan="5">GÉANT</td><td colspan="5">WS-DREAM</td></tr><tr><td>Metric</td><td>Model</td><td>OR2%</td><td>OR4%</td><td>OR6%</td><td>OR8%</td><td>OR10%</td><td>OR2%</td><td>OR4%</td><td>OR6%</td><td>OR8%</td><td>OR10%</td><td>OR2%</td><td>OR4%</td><td>OR6%</td><td>OR8%</td><td>OR10%</td></tr><tr><td rowspan="8">NMAE</td><td>ARI-LLM</td><td>0.1839</td><td>0.1638</td><td>0.1568</td><td>0.1543</td><td>0.1492</td><td>0.2666</td><td>0.2349</td><td>0.2242</td><td>0.2189</td><td>0.2076</td><td>0.2376</td><td>0.1940</td><td>0.1852</td><td>0.1833</td><td>0.1812</td></tr><tr><td>PetTC</td><td>0.2247</td><td>0.1925</td><td>0.1843</td><td>0.1764</td><td>0.1692</td><td>0.2917</td><td>0.2345</td><td>0.2264</td><td>0.2208</td><td>0.2014</td><td>0.3513</td><td>0.2974</td><td>0.2762</td><td>0.2647</td><td>0.2515</td></tr><tr><td>LTP</td><td>0.2585</td><td>0.2293</td><td>0.2257</td><td>0.2144</td><td>0.2031</td><td>0.3694</td><td>0.3286</td><td>0.3008</td><td>0.2858</td><td>0.2788</td><td>0.4087</td><td>0.3855</td><td>0.3525</td><td>0.3413</td><td>0.3405</td></tr><tr><td>DATC</td><td>0.2954</td><td>0.2748</td><td>0.2631</td><td>0.2596</td><td>0.2541</td><td>0.4939</td><td>0.4332</td><td>0.3651</td><td>0.3215</td><td>0.3037</td><td>0.9210</td><td>0.8431</td><td>0.8536</td><td>0.7734</td><td>0.8125</td></tr><tr><td>NTC</td><td>0.3702</td><td>0.3362</td><td>0.3243</td><td>0.3115</td><td>0.3073</td><td>0.7042</td><td>0.6796</td><td>0.6239</td><td>0.5781</td><td>0.4751</td><td>0.4931</td><td>0.4983</td><td>0.4818</td><td>0.4619</td><td>0.4355</td></tr><tr><td>NTM</td><td>1.2214</td><td>0.8818</td><td>0.7633</td><td>0.6686</td><td>0.6178</td><td>1.4547</td><td>1.3646</td><td>1.3266</td><td>1.2003</td><td>1.1978</td><td>0.6337</td><td>0.7210</td><td>0.6502</td><td>0.6390</td><td>0.6320</td></tr><tr><td>NTF</td><td>0.7529</td><td>0.4147</td><td>0.3637</td><td>0.3486</td><td>0.3353</td><td>0.9061</td><td>0.7783</td><td>0.7189</td><td>0.5958</td><td>0.5125</td><td>0.6788</td><td>0.5335</td><td>0.4976</td><td>0.4620</td><td>0.4114</td></tr><tr><td>CoSTCo</td><td>0.3857</td><td>0.3739</td><td>0.3381</td><td>0.3224</td><td>0.3145</td><td>0.8588</td><td>0.7826</td><td>0.7291</td><td>0.7241</td><td>0.7042</td><td>0.5412</td><td>0.5321</td><td>0.4655</td><td>0.4501</td><td>0.4430</td></tr><tr><td rowspan="8">NRMSE</td><td>ARI-LLM</td><td>0.2316</td><td>0.2123</td><td>0.1966</td><td>0.1905</td><td>0.1818</td><td>0.2767</td><td>0.2360</td><td>0.2221</td><td>0.2206</td><td>0.2077</td><td>0.3525</td><td>0.2923</td><td>0.2830</td><td>0.2790</td><td>0.2729</td></tr><tr><td>PetTC</td><td>0.2413</td><td>0.2205</td><td>0.2113</td><td>0.2087</td><td>0.2062</td><td>0.3214</td><td>0.2321</td><td>0.2298</td><td>0.2285</td><td>0.2128</td><td>0.4116</td><td>0.3789</td><td>0.3632</td><td>0.3576</td><td>0.3425</td></tr><tr><td>LTP</td><td>0.3173</td><td>0.2937</td><td>0.2921</td><td>0.2908</td><td>0.2642</td><td>0.2954</td><td>0.2614</td><td>0.2446</td><td>0.2381</td><td>0.2329</td><td>0.4720</td><td>0.4375</td><td>0.4112</td><td>0.4042</td><td>0.3947</td></tr><tr><td>DATC</td><td>0.3453</td><td>0.3312</td><td>0.3226</td><td>0.3202</td><td>0.3178</td><td>0.3818</td><td>0.3415</td><td>0.2979</td><td>0.2547</td><td>0.2368</td><td>0.9276</td><td>0.8721</td><td>0.7992</td><td>0.7786</td><td>0.7473</td></tr><tr><td>NTC</td><td>0.4388</td><td>0.4072</td><td>0.3951</td><td>0.3858</td><td>0.3766</td><td>0.6412</td><td>0.6266</td><td>0.5888</td><td>0.5450</td><td>0.4310</td><td>0.5308</td><td>0.4737</td><td>0.4490</td><td>0.4259</td><td>0.4140</td></tr><tr><td>NTM</td><td>0.9720</td><td>0.7573</td><td>0.7234</td><td>0.6613</td><td>0.6197</td><td>0.9230</td><td>0.9057</td><td>0.8877</td><td>0.7854</td><td>0.7629</td><td>0.6229</td><td>0.5613</td><td>0.5788</td><td>0.5389</td><td>0.5128</td></tr><tr><td>NTF</td><td>0.6856</td><td>0.4201</td><td>0.3882</td><td>0.3848</td><td>0.3723</td><td>0.7110</td><td>0.6621</td><td>0.5838</td><td>0.4959</td><td>0.4128</td><td>0.6206</td><td>0.5105</td><td>0.4782</td><td>0.4757</td><td>0.4379</td></tr><tr><td>CoSTCo</td><td>0.4081</td><td>0.3929</td><td>0.3736</td><td>0.3666</td><td>0.3600</td><td>0.7215</td><td>0.6579</td><td>0.6252</td><td>0.6037</td><td>0.5927</td><td>0.5286</td><td>0.4643</td><td>0.4595</td><td>0.4234</td><td>0.4120</td></tr><tr><td rowspan="8">KL</td><td>ARI-LLM</td><td>0.0493</td><td>0.0393</td><td>0.0355</td><td>0.0336</td><td>0.0302</td><td>0.1397</td><td>0.1011</td><td>0.0886</td><td>0.0843</td><td>0.0772</td><td>0.1463</td><td>0.0820</td><td>0.0652</td><td>0.0592</td><td>0.0587</td></tr><tr><td>PetTC</td><td>0.0532</td><td>0.0513</td><td>0.0501</td><td>0.0498</td><td>0.0471</td><td>0.2593</td><td>0.1408</td><td>0.1308</td><td>0.1419</td><td>0.1280</td><td>0.1237</td><td>0.1145</td><td>0.1076</td><td>0.1053</td><td>0.1029</td></tr><tr><td>LTP</td><td>0.5021</td><td>0.1832</td><td>0.1524</td><td>0.1336</td><td>0.1004</td><td>0.7012</td><td>0.4531</td><td>0.4254</td><td>0.3755</td><td>0.3491</td><td>0.4641</td><td>0.3573</td><td>0.3214</td><td>0.2561</td><td>0.2139</td></tr><tr><td>DATC</td><td>0.0994</td><td>0.0881</td><td>0.0794</td><td>0.0767</td><td>0.0736</td><td>0.4495</td><td>0.3338</td><td>0.2522</td><td>0.2327</td><td>0.2103</td><td>1.5789</td><td>1.2631</td><td>1.0789</td><td>0.7368</td><td>0.7894</td></tr><tr><td>NTC</td><td>0.1578</td><td>0.1326</td><td>0.1202</td><td>0.1157</td><td>0.1095</td><td>1.2776</td><td>1.0643</td><td>0.8378</td><td>0.8306</td><td>0.4765</td><td>0.4814</td><td>0.3476</td><td>0.3015</td><td>0.3289</td><td>0.1952</td></tr><tr><td>NTM</td><td>2.5215</td><td>0.9318</td><td>0.8276</td><td>0.7838</td><td>0.6946</td><td>2.0707</td><td>1.9729</td><td>1.8230</td><td>1.7226</td><td>1.5882</td><td>2.3166</td><td>0.2011</td><td>0.1974</td><td>0.1553</td><td>0.1102</td></tr><tr><td>NTF</td><td>0.4744</td><td>0.2114</td><td>0.1635</td><td>0.1591</td><td>0.1228</td><td>1.1552</td><td>0.7186</td><td>0.6736</td><td>0.6624</td><td>0.5734</td><td>0.2431</td><td>0.1572</td><td>0.1084</td><td>0.1057</td><td>0.1041</td></tr><tr><td>CoSTCo</td><td>0.3566</td><td>0.4370</td><td>0.3305</td><td>0.2851</td><td>0.2461</td><td>5.2273</td><td>3.7190</td><td>3.4680</td><td>3.3872</td><td>3.0307</td><td>0.2995</td><td>0.2439</td><td>0.1911</td><td>0.1768</td><td>0.1244</td></tr></table>

Fig. 6 presents the results of the ablation study at 10% observation rate. As shown in the figure, the original model significantly outperforms the two ablated variants, validating the effectiveness of both key components. Between them, ARI-LLM w/o AR shows a larger performance drop than ARI-LLM w/o prompt, indicating the critical role of the autoregressive mechanism for LLM-based imputation.

![](images/d614c30913ac2c5dbe4ca901e531d60c47eee813d62235cd4891a2725bbb272c.jpg)  
Fig. 6. Results on ablation study with 10% observation rate.

## E. Performance in Dynamic Network Environments

To simulate the dynamic network environments, we randomly select p% of all flows in each dataset for training and then introduce the remaining flows during testing. This setup is designed to assess the model’s ability to adapt to newly emerging traffic patterns when the underlying network structure undergoes varying degrees of changes.

Fig. 7 presents the imputation errors of ARI-LLM and the best-performing baseline, PetTC<sup>1</sup>, under varying proportions of flows used for training. As shown in the figure, although both methods exhibit increased errors as the proportion of training flows decreases, the error of PetTC rises significantly faster than that of ARI-LLM. Specifically, when only 20% of flows are used for training, the average error of ARI-LLM across the three datasets increases by just 7.1%, while the error for PetTC rises by 22.3%. This demonstrates the strong generalization ability of ARI-LLM.

![](images/fdd203eb1a6388a059ed447d720925c2e5b91e795eadff0c2e8aff1ec613697a.jpg)  
(a) Abilene

![](images/4c4d045e2264493e1b6e626a672c42a83736885189acbac75558645920def018.jpg)  
(b) GEANT<sup>´</sup>

![](images/d023a529f6d09e7f274aef950d77f1913f29f5c538df240239eabf58208ec264.jpg)  
(c) WS-DREAM  
Fig. 7. Imputation errors in dynamic network environments with 10% observation rate.

## F. Performance in Unseen Networks

Experiments in this subsection evaluates the applicability of the two methods in a more challenging scenario: unseen network without any prior knowledge. In such scenario, the model is trained on the TM data from one network and then used to predict the missing flows in a different network.

In Fig. 8(a), A→A denotes both the training and testing flows are from the Abilene network; G→A indicates the model is trained on flows from the GEANT network and<sup>´</sup> tested on Abilene; W→A means training is done on WS-DREAM and testing on Abilene. In Fig. 8(b) and (c), the corresponding symbols follow the same convention. As shown in the figure, although ARI-LLM has never seen the traffic from the target network, it still achieves relatively stable and reliable imputation performance. In contrast, PetTC exhibits a significant performance drop when applied to unseen networks. Specifically, ARI-LLM experiences an accuracy degradation of 7.6% in Abilene, 8.7% in GEANT, and 8.3%<sup>´</sup> in WS-DREAM on average, while PetTC suffers from a severe degradation of 23.2% in Abilene, 32.5% in GEANT,<sup>´</sup> and 23.3% in WS-DREAM. This demonstrates the pre-trained knowledge embedded in the LLM within ARI-LLM endows it with strong zero-shot and knowledge transfer capabilities, significantly enhancing its adaptability to unseen networks.

![](images/ab3e3e8b40f030b781d5d48b50d68d42128edf20a9ea5ba8fd102efd78ba28ce.jpg)  
(a) Test on Abilene

![](images/63a79b5c910b820affdff7fed29f8cb438c7e811fcd15cc7270520a0ab562848.jpg)  
(b) Test on GEANT<sup>´</sup>

![](images/e2f2a13d8bef2a3b93fcda94852b978d9ce8dc474eeab0759a31e574a5de620b.jpg)  
(c) Test on WS-DREAM  
Fig. 8. Imputation errors on unseen networks with 10% observation rate: A: Abilene, G: GEANT, W: WS-DREAM.<sup>´</sup>

## G. Performance with Limited TM snapshots

Considering the high cost of TM data collection, we evaluate the performance of the two methods under limited TM snapshots. Specifically, we train the model using only the first 5% or 10% of the full snapshots, and then apply it to predict the missing TMs in the test set.

Fig.9 presents the imputation errors of the two methods under three training settings: using the full training set, using 10% and 5% of the training data. As shown, even with significantly reduced training data, ARI-LLM maintains relatively stable performance, while PetTC exhibits a sharp drop in accuracy. Specifically, averaging across the three datasets, ARI-LLM’s imputation accuracy drops only 0.6% ∼ 1.5% with 10% training data and 0.9% ∼ 4.7% with 5%. In contrast, PetTC suffers a much steeper decline, with accuracy dropping by $9 . 5 \% \sim 1 4 . 5 \%$ and $1 2 . 4 \% \sim 1 8 . 2 \%$ , respectively. These results demonstrate the strong few-shot learning capability of ARI-LLM, enabling significant reductions in training costs.

![](images/037bc7c6f3b11bbccad5308559cc978504b48db227df1e3902986adc2c3fe8ea.jpg)  
(a) Abilene

![](images/d993dd7bb5294bbf0deeceec658fdca3bb0e92a1d1463f6a4053067d407654a3.jpg)  
(b) GEANT <sup>´</sup>

![](images/895ca8ce40d1b34a4f6ecef6b7cb0cd5575a85971c5d2743561dd687a312d662.jpg)  
(c) WS-DREAM  
Fig. 9. Imputation errors on limited TM snapshots with 10% observation rate.

## H. Running Speed

Table III compares the training and inferring time of each impuation method. The training time refers to the duration from feeding the training data into the model to its convergence, while the inference time is measured as the total time taken to recover all testing data under a 10% sampling rate.

As shown in Table III, the training and testing times for all models are shortest on the Abilene dataset and longest on the WS-DREAM dataset. This is because Abilene has the smallest network size and the lowest TM dimension, while WS-DREAM has the largest. Surprisingly, despite ARI-LLM adopting a step-wise autoregressive strategy for training and imputation, its training and inferring times do not increase significantly. On the contrary, ARI-LLM demonstrates superior speed on large-scale networks compared to other baselines.

The key reasons are as follows: (1) The autoregressive scheme in ARI-LLM generates TM blocks of varying resolutions at each step, rather than individual flows, enabling batch processing that improves efficiency. (2) Unlike other models with many trainable parameters, ARI-LLM involves only lightweight LLM fine-tuning. (3) With the coarse-to-fine autoregressive training and prompt-based guidance, the model converges rapidly, typically within just 2∼3 training epochs.

TABLE III  
TRAINING AND INFERRING TIME IN SECONDS [S]. BOLD: BEST, UNDERLINED: SECOND BEST.

<table><tr><td rowspan="2">Model / Datasets</td><td colspan="2">Abilene</td><td colspan="2">GÉANT</td><td colspan="2">WS-DREAM</td></tr><tr><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td></tr><tr><td>NTM</td><td>128.0</td><td> $\underline{2.8}$ </td><td>1460.5</td><td>9.2</td><td>5202.0</td><td>266.4</td></tr><tr><td>NTC</td><td>618.1</td><td>4.2</td><td>3506.3</td><td>13.7</td><td>2177.1</td><td>228.6</td></tr><tr><td>CoSTCo</td><td>596.2</td><td>3.2</td><td> $\underline{526.2}$ </td><td>65.1</td><td> $\underline{1487.8}$ </td><td>20.6</td></tr><tr><td>NTF</td><td> $\underline{84.8}$ </td><td>2.9</td><td>678.3</td><td>10.3</td><td>3019.4</td><td>207.9</td></tr><tr><td>LTP</td><td>239.6</td><td>2.9</td><td>1373.0</td><td>10.3</td><td>3829.0</td><td>209.0</td></tr><tr><td>DATC</td><td>1728.5</td><td>4.5</td><td>1876.2</td><td> $\underline{6.1}$ </td><td>7548.6</td><td>23.2</td></tr><tr><td>PetTC</td><td>160.3</td><td>4.0</td><td>1723.1</td><td>13.0</td><td>2127.8</td><td>253.3</td></tr><tr><td>ARI-LLM</td><td> $\underline{93.2}$ </td><td> $\underline{1.3}$ </td><td>360.7</td><td> $\underline{8.4}$ </td><td>1024.8</td><td>16.4</td></tr></table>

## V. CONCLUSION

In this work, we introduced ARI-LLM, a novel framework for TM imputation. Inspired by human-like reasoning, our ARI-LLM models the imputation process as a progressive refinement task, gradually enhancing TM quality from coarse to fine. To enable a plug-and-play imputation framework, we developed a specialized embedding scheme and prompt template that enable LLMs to leverage their powerful few-shot and zero-shot capabilities, thereby enhancing generalization to evolving and unseen networks. Extensive experiments on real-world datasets demonstrate ARI-LLM greatly outperforms existing state-of-the-art methods and exhibits outstanding performance when faced with dynamic or unseen networks. We have provided public access to our code and data at https://github.com/JKevin17/ARI-LLM.

## ACKNOWLEDGEMENTS

This research is supported by National Natural Science Foundation of China (NSFC) (No. 62572168, No. 62372149, No. 62302081, No. 62571058, and No. U23A20303), Anhui Provincial Natural Science Fund (2508085MF151), Sichuan Science and Technology Program (2024NSFSC1458), the Key Laboratory of Knowledge Engineering with Big Data (the Ministry of Education of China) (BigKEOpen2025-04), and Open Foundation of State key Laboratory of Networking and Switching Technology (Beijing University of Posts and Telecommunications) (SKLNST-2025-1-12).

[1] Y.-F. Liu, K. C.-J. Lin, and C.-C. Tseng, “Dynamic cluster-based flow management for software defined networks,” IEEE Transactions on Services Computing, vol. 15, no. 1, pp. 361–371, 2019.

[2] S. H. Rafique, A. Abdallah, N. S. Musa, and T. Murugan, “Machine learning and deep learning techniques for internet of things network anomaly detection—current research trends,” Sensors, vol. 24, no. 6, p. 1968, 2024.

[3] Y. Xie, F. Yi, and K. Jamieson, “Pbe-cc: Congestion control via endpoint-centric, physical-layer bandwidth measurements,” in Proceedings of the Annual conference of the ACM Special Interest Group on Data Communication on the applications, technologies, architectures, and protocols for computer communication, 2020, pp. 451–464.

[4] <sup>´</sup>I. Cunha, R. Teixeira, D. Veitch, and C. Diot, “Predicting and tracking internet path changes,” in Proceedings of the ACM SIGCOMM 2011 Conference, 2011, pp. 122–133.

[5] Q. Zhao, Z. Ge, J. Wang, and J. Xu, “Robust traffic matrix estimation with imperfect information: Making use of multiple data sources,” in Proceedings of the joint international conference on Measurement and modeling of computer systems, 2006, pp. 133–144.

[6] Y. Qiao, X. Yuan, and K. Wu, “Routing-oblivious network tomography with flow-based generative model,” in IEEE INFOCOM 2024-IEEE Conference on Computer Communications. IEEE, 2024, pp. 2139– 2148.

[7] Z. Hu and J. Luo, “Cracking network monitoring in dcns with sdn,” in 2015 IEEE Conference on Computer Communications (INFOCOM). IEEE, 2015, pp. 199–207.

[8] A. Tootoonchian, M. Ghobadi, and Y. Ganjali, “Opentm: traffic matrix estimator for openflow networks,” in International Conference on Passive and Active Network Measurement. Springer, 2010, pp. 201–210.

[9] Y. Zhang, M. Roughan, N. Duffield, and A. Greenberg, “Fast accurate computation of large-scale ip traffic matrices from link loads,” ACM SIGMETRICS Performance Evaluation Review, vol. 31, no. 1, pp. 206– 217, 2003.

[10] E. D. Biyar, B. Karanlik, and B. Canberk, “Flow-based network tomography agent for software defined data center,” in 2019 3rd International Conference on Recent Advances in Signal Processing, Telecommunications & Computing (SigTelCom). IEEE, 2019, pp. 170–175.

[11] A. Medina, N. Taft, K. Salamatian, S. Bhattacharyya, and C. Diot, “Traffic matrix estimation: Existing techniques and new directions,” ACM SIGCOMM Computer Communication Review, vol. 32, no. 4, pp. 161–174, 2002.

[12] C. Tebaldi and M. West, “Bayesian inference on network traffic using link count data,” Journal ofthe American Statistical Association, vol. 93, no. 442, pp. 557–573, 1998.

[13] H. Wang, K. Xie, J. Wen, G. Zhang, W. Liang, G. Xie, and K. Li, “Pettc: Pairwise joint embedding based contrastive tensor completion for network traffic monitoring services,” IEEE Trans. Serv. Comput., vol. 18, no. 1, pp. 357–371, 2025.

[14] K. Xie, H. Lu, X. Wang, G. Xie, Y. Ding, D. Xie, J. Wen, and D. Zhang, “Neural tensor completion for accurate network monitoring,” in IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 2020, pp. 1688–1697.

[15] P. Tune and M. Roughan, “Spatiotemporal traffic matrix synthesis,” in Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication, 2015, pp. 579–592.

[16] M. Roughan, Y. Zhang, W. Willinger, and L. Qiu, “Spatio-temporal compressive sensing and internet traffic matrices (extended version),” IEEE/ACM Transactions on Networking, vol. 20, no. 3, pp. 662–676, 2011.

[17] K. Xie, Y. Ouyang, X. Wang, G. Xie, K. Li, W. Liang, J. Cao, and J. Wen, “Deep adversarial tensor completion for accurate network traffic measurement,” IEEE/ACM Transactions on Networking, vol. 31, no. 5, pp. 2101–2116, 2023.

[18] M. Jin, S. Wang, L. Ma, Z. Chu, J. Y. Zhang, X. Shi, P.-Y. Chen, Y. Liang, Y.-F. Li, S. Pan, and Q. Wen, “Time-LLM: Time series forecasting by reprogramming large language models,” in The Twelfth International Conference on Learning Representations (ICLR), 2024.

[19] H. Wang, J. Qin, A. Bastola, X. Chen, J. Suchanek, Z. Gong, and A. Razi, “Visiongpt: Llm-assisted real-time anomaly detection for safe visual navigation,” arXiv preprint arXiv:2403.12415, 2024.

[20] H. Abburi, M. Suesserman, N. Pudota, B. Veeramani, E. Bowen, and S. Bhattacharya, “Generative ai text classification using ensemble llm approaches,” arXiv preprint arXiv:2309.07755, 2023.

[21] T. Cui, X. Lin, S. Li, M. Chen, Q. Yin, Q. Li, and K. Xu, “Trafficllm: Enhancing large language models for network traffic analysis with generic traffic representation,” arXiv preprint arXiv:2504.04222, 2025.

[22] D. Wu, X. Wang, Y. Qiao, Z. Wang, J. Jiang, S. Cui, and F. Wang, “Netllm: Adapting large language models for networking,” in Proceedings of the ACM SIGCOMM 2024 Conference, 2024, pp. 661–678.

[23] K. Tian, Y. Jiang, Z. Yuan, B. Peng, and L. Wang, “Visual autoregressive modeling: Scalable image generation via next-scale prediction,” Advances in neural information processing systems (NeurlPS), vol. 37, pp. 84 839–84 865, 2024.

[24] Y. Vardi, “Network tomography: Estimating source-destination traffic intensities from link data,” Journal of the American statistical association, vol. 91, no. 433, pp. 365–377, 1996.

[25] Y. Qiao, Z. Hu, and J. Luo, “Efficient traffic matrix estimation for data center networks,” in 2013 IFIP Networking Conference. IEEE, 2013, pp. 1–9.

[26] J. Cao, D. Davis, S. Vander Wiel, and B. Yu, “Time-varying network tomography: Router link data,” Journal of the American statistical association, vol. 95, no. 452, pp. 1063–1075, 2000.

[27] Y. Zhang, M. Roughan, N. Duffield, and A. Greenberg, “Fast accurate computation of large-scale ip traffic matrices from link loads,” ACM SIGMETRICS Performance Evaluation Review, vol. 31, no. 1, pp. 206– 217, 2003.

[28] K. Xie, X. Wang, X. Wang, Y. Chen, G. Xie, Y. Ouyang, J. Wen, J. Cao, and D. Zhang, “Accurate recovery of missing network measurement data with localized tensor completion,” IEEE/ACM Transactions on Networking, vol. 27, no. 6, pp. 2222–2235, 2019.

[29] J. Tian, K. Xie, X. Wang, J. Wen, G. Xie, J. Cao, W. Liang, and K. Li, “Reducing network distance measurement overhead: A tensor completion solution with a new minimum sampling bound,” IEEE Transactions on Networking, vol. 33, no. 1, pp. 255–270, 2025.

[30] Y. Qiao, K. Wu, and X. Yuan, “Autotomo: Learning-based traffic estimator incorporating network tomography,” IEEE/ACM Transactions on Networking, vol. 32, no. 6, pp. 4644–4659, 2024.

[31] Y. Ouyang, K. Xie, X. Wang, J. Wen, and G. Zhang, “Lightweight trilinear pooling based tensor completion for network traffic monitoring,” in IEEE INFOCOM 2022-IEEE Conference on Computer Communications. IEEE, 2022, pp. 2128–2137.

[32] C. Liu, K. Xie, T. Wu, C. Ma, and T. Ma, “Distributed neural tensor completion for network monitoring data recovery,” Information Sciences, vol. 662, p. 120259, 2024.

[33] Y. Zhou, N. Yu, and Z. Liu, “Towards interactive research agents for internet incident investigation,” in Proceedings of the 22nd ACM Workshop on Hot Topics in Networks, 2023, pp. 33–40.

[34] V. Kreinovich, H. T. Nguyen, and R. Ouncharoen, “How to estimate forecasting quality: A system-motivated derivation of symmetric mean absolute percentage error (smape) and other similar characteristics,” Department of Computer Science, University of Texas at El Paso, Technical Report 865, 2014.

[35] T. Zhou, P. Niu, L. Sun, R. Jin et al., “One fits all: Power general time series analysis by pretrained lm,” Advances in neural information processing systems (NeurlPS), vol. 36, pp. 43 322–43 355, 2023.

[36] H. Wu, J. Xu, J. Wang, and M. Long, “Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting,” Advances in neural information processing systems (NeurlPS), vol. 34, pp. 22 419–22 430, 2021.

[37] S. Uhlig, B. Quoitin, J. Lepropre, and S. Balon, “Providing public intradomain traffic matrices to the research community,” ACM SIGCOMM Computer Communication Review, vol. 36, no. 1, pp. 83–86, 2006.

[38] Z. Zheng and M. R. Lyu, “Ws-dream: A distributed reliability assessment mechanism for web services,” in 2008 IEEE International Conference on Dependable Systems and Networks With FTCS and DCC (DSN). IEEE, 2008, pp. 392–397.

[39] H. Liu, Y. Li, M. Tsang, and Y. Liu, “Costco: A neural tensor completion model for sparse tensors,” in Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2019, pp. 324–334.

[40] H. Chen and J. Li, “Neural tensor model for learning multi-aspect factors in recommender systems,” in Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence, IJCAI 2020, 2020, pp. 2449–2455.

[41] X. Wu, B. Shi, Y. Dong, C. Huang, and N. V. Chawla, “Neural tensor factorization for temporal interaction learning,” in Proceedings of the Twelfth ACM international conference on web search and data mining, 2019, pp. 537–545.
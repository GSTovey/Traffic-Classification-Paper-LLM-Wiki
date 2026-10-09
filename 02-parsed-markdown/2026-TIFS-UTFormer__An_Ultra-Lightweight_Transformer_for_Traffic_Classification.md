# UTFormer: An Ultra-Lightweight Transformer for Trafic Classification

Dong Wen , Tianyun Li, Zhuochen Fan , Member, IEEE, Qing Li , Senior Member, IEEE, Jie Li, Fa Zhu , Member, IEEE, Chenglong Li , Athanasios V. Vasilakos , Senior Member, IEEE, and Tao Li

Abstract—Transformer-based models have shown promise in network trafic classification, but face challenges of architectural and computational redundancy. This paper presents UTFormer, an ultra-lightweight Transformer that addresses dual redundancies in input features and model architecture. We introduce two key innovations: 1) Dynamic payload distillation that automatically identifies critical bytes through attention-driven selection, reducing input features by up to 95% while maintaining high accuracy; 2) Diferentiable architecture search formulates Transformer configurations as continuous parameters that can be optimized via stochastic gradient descent, enabling automated search of compact architectures with layer depth ≤ 4 and hidden dimensions ≤ 256. Our evaluation on six datasets shows that UTFormer achieves 87.79%-99.99% accuracy while significantly decreasing computational costs by 9<sub>.</sub>0×-36398<sub>.</sub>5× and reducing the model size by 44 9×-5433 9× compared to Transformersbased baselines. UTFormer demonstrates excellent architectural eficiency with a minimum 106 KB model size, enabling trafic classification at the speed of 7.55 million packet-per-second in ofline evaluations and reaching the throughput of 10 Gbps linerate under a real deployment environment. It is demonstrated that our work is capable of performing trafic classification with a lightweight model architecture while maintaining high accuracy. The source code is available at: https://github.com/ utformer/UTFormer

Index Terms—Trafic classification, transformer, self-attention, stochastic gradient descent.

## I. INTRODUCTION

block for network systems, enabling critical applications

Received 2 May 2025; revised 28 November 2025 and 31 May 2026; accepted 22 June 2026. Date of publication 9 July 2026; date of current version 6 August 2026. This work was supported in part by the New Generation Artificial Intelligence-National Science and Technology Major Project under Grant 2025ZD0122201 and in part by the Natural Science Foundation of China under Grant NSFC U24B20151. The associate editor coordinating the review of this article and approving it for publication was Prof. Abderrahim Benslimane. (Corresponding authors: Tao Li; Zhuochen Fan.)

Dong Wen, Tianyun Li, Jie Li, and Tao Li are with the College of Computer Science and Technology, National University of Defense Technology, Changsha 410000, China (e-mail: wendong19@nudt.edu.cn; lty 23@nudt.edu.cn; lijie @nudt.edu.cn; taoli@nudt.edu.cn).

Zhuochen Fan and Qing Li are with the Department of Strategic and Advanced Interdisciplinary Research, Peng Cheng Laboratory, Shenzhen 518055, China (e-mail: fanzc@pku.edu.cn; liq@pcl.ac.cn).

Fa Zhu is with the College of Information Science and Technology and the College of Artificial Intelligence, Nanjing Forestry University, Nanjing 210000, China (e-mail: zhufag@gmail.com).

Chenglong Li is with the Defense Innovation Institute, Academy of Military Sciences, Beijing 100000, China (e-mail: chenglongli17@163.com).

Athanasios V. Vasilakos is with the Department of Networks and Communications, College of Computer Science and Information Technology, IAU, Dammam 31441, Saudi Arabia, and also with the Center for AI Research (CAIR), University of Agder (UiA), 4604 Grimstad, Norway (e-mail: th.vasilakos@gmail.com).

Digital Object Identifier 10.1109/TIFS.2026.3711855 ranging from fine-grained trafic classification to intrusion trafic detection. To address the inherent complexity of modern network trafic, the research community has increasingly adopted machine learning (ML) and deep learning (DL) techniques. Typical approaches leverage decision trees [1], [2], [3], recurrent neural networks (RNNs) [4], [5], [6], and convolutional neural networks (CNNs) [7], [8], [9] to capture spatial and temporal dependencies in trafic data [10], [11], [12]. Considering the success of Transformer models in natural language processing (NLP) [13], [14], recent work has explored Transformer-based architectures as a paradigm for trafic classification. Leveraging the ability of Transformers to model long-range dependencies in network trafic, it has demonstrated state-of-the-art (SOTA) performance in key tasks including encrypted trafic classification and malware behavior detection [15], [16], [17].

TABLE I  
THE REDUNDANCY IN EXISTING TRANSFORMER MODELS

<table><tr><td></td><td>Model-A</td><td>Model-B</td><td>Model-C</td></tr><tr><td># layers</td><td>12</td><td>5</td><td>12</td></tr><tr><td>Input</td><td>1500 B</td><td>1500 B</td><td>512 B</td></tr><tr><td>Accuracy</td><td>99.97%</td><td>99.99%</td><td>99.99%</td></tr><tr><td>Normalized computation</td><td>1.0</td><td>0.42</td><td>0.13</td></tr></table>

## A. Motivation

Specifically, the emerging Transformer-based trafic classification considers network communication as a contextual language exchange between devices on the network [18]. This novel perspective enables the direct processing of raw packet bytes through tokenization mechanisms without traditional feature engineering pipelines. Then, the selfattention mechanism within the Transformer architecture demonstrates exceptional capability in modeling byte-level inter-dependencies, achieving superior classification performance. However, components such as multi-head self-attention (MHSA) modules and deep Transformer block layers (e.g., the 12-layer architectures in [18] and [19]) in existing work raise practical deployment concerns due to their high computational cost. This architecture fundamentally conflicts with the low-latency and high-throughput requirements for trafic classification [20], [21]. Therefore, there is an urgent need to design lightweight Transformer models to address such conflicts.

Meanwhile, our ablation experiments on the malware detection task of USTC-TFC dataset [22] reveal that existing Transformer-based trafic classification models have critical redundancy in the model architecture and input feature, as listed in Table I. We select the architecture of ET-Bert [19] as the baseline model (Model-A in Table I), which employs a 12-layer Transformer architecture with 1500-byte of input. For fair comparison, Model-B and Model-C, respectively, have reduced architecture or input features: Model-B has the same input as Model-A but adopts a reduced 5-layer architecture, while Model-C has a shorter input of 512 bytes with the exact architecture of Model-A. To benchmark the computational overhead, we normalize the computation workload of three models against Model-A. (i) Architectural redundancy. Although Model-B only requires 42.67% computation compared to Model-A, it maintains comparable classification accuracy, suggesting the architectural redundancy in existing models. (ii) Input redundancy. While prior work [23], [24], [25] universally adopts a fixed-length input (256-1500 bytes), Model-C processes only 512 bytes per packet (34.13% of Model-A) while maintaining equivalent accuracy on the same task. The reduction in input features directly reduces the computational overhead by 7 69×, confirming the redundancy of the input feature.

## B. Challenges and Contributions

Despite these empirical observations, designing lightweight Transformer models for trafic classification faces two fundamental challenges: (i) How to determine an efective transformer architecture. The computational complexity of Transformer models depends on multiple interdependent parameters, including layer depth, self-attention head count, and hidden dimension sizes. These architectural parameters form a high-dimensional combinatorial search space where finding optimal configurations becomes NP-hard [26], [27]. (ii) How to select the most informative bytes in the trafic. It is dificult to identify the most informative payload bytes without prior knowledge of their spatial distribution, particularly for encrypted trafic classification. There emerges a critical question: How do we reliably locate informative bytes within variable-length network payloads across various protocols and encapsulation formats?

To overcome these challenges, we present UTFormer, an ultra-lightweight Transformer model for trafic classification. Our design introduces two fundamental innovations.

• Dynamic payload distillation: Leveraging the inherent self-attention mechanism of Transformers, we develop an adaptive byte selection technique that automatically identifies and retains semantically significant trafic segments. This distillation process is controlled by the diferential byte-keeping rate, eliminating tedious manual threshold tuning through gradient-based optimization.

• Diferential architecture search: To further determine the eficient architecture of Transformer models, we formulate architectural parameters (layer depth, head dimension, etc.) as continuous optimization variables within a composed search space. A unified loss function guides the simultaneous optimization of model accuracy and computational cost via stochastic gradient descent (SGD). The byte-keeping rate in dynamic payload distillation is also automatically optimized during the search.

![](images/e634360feb418939983e1ac004688a59efb7ec32c7f97297a3ac419d12ac1048.jpg)  
Fig. 1. Accuracy vs computational cost. The x-axis (normalized computational cost) decreases left-to-right; the y-axis (accuracy) increases bottom-to-top. Our UTFormer, positioned at the right-top area, exhibits the lowest computational cost and SOTA-comparable accuracy among six baselines.

Experimental evaluations on six datasets verify the model eficiency and classification performance of UTFormer, as depicted in Figure 1. Compared with the baselines, UTFormer introduces the lowest computational cost with competitive accuracy compared with SOTA models. Moreover, our dynamic payload distillation reduces up to 90% useless trafic bytes, with a diferential architecture search technique resulting in 100 KB-level ultra-lightweight Transformer models. In-depth experiments further demonstrate the capacity and potential of dynamic payload distillation to be a drop-in light-weighting method for Transformer-based trafic analysis models.

Our contributions are as follows.

(i) We propose UTFormer, a novel light-weight Transformer model for trafic analysis. With a compact model size of 106KB-12.8MB and 3 61×-36538 46× reduced computational overhead, UTFormer maintains 87 79% − 99 99% classification accuracy on six datasets. Its lightweight design and classification performance make it a practical solution for low-latency and high-throughput trafic classification deployment.

(ii) We present key innovations, including dynamic payload distillation and diferential architecture search. These methods co-optimize input features and model architecture, automatically eliminating up to 95% of redundant trafic bytes while constructing ultra-lightweight models. Experiments also prove the compatibility of dynamic payload distillation on other Transformer-based trafic analysis models.

(iii) We conduct rigorous evaluations on UTFormer under real-world deployment environments, and the experimental results demonstrate that UTFormer yields 10 Gbps line-rate throughput with a real-time latency of less than 0.2 milliseconds, proving the practical deployability of UTFormer.

## II. BACKGROUND

## A. Transformer Models

The Transformer architecture introduces a fundamental structural divergence from traditional deep neural networks (DNNs) through its tokenization paradigm, where Transformer models directly transform raw trafic bytes into a series of tokens. This method originates in NLP, where word tokens enable context-aware processing [13], [14]. In some variants of Transformer models, an extra class token [28], [29], [30] is introduced to dynamically aggregate global features through self-attention mechanisms. Classification tasks related to network trafic or computer vision domains can benefit from the use of class token [28], [30].

![](images/a23698bd3649898e9b4441dad277eb14d9da1574c01c86b704b4aabac6f51b97.jpg)  
Fig. 2. The architecture of transformer models.

Transformer architecture comprises multiple stacked Transformer block layers, as illustrated in Figure 2. Each block layer contains two primary components: a Multi-Head Self-Attention (MHSA) module and a Feed-Forward Neural Network (FFN), with each module incorporating a Layer Normalization (LayerNorm) operation. The basic building block of the MHSA module is the self-attention mechanism, which projects the input tokens into respective vectors: query (Q), key (K), and value (V) through matrix multiplication (MatMul) with three learnable parameter matrices respectively. The attention computation follows the formulation in Equation 1, where l denotes the dimension of token embeddings. The Softmax operation generates an attention matrix that captures pairwise token dependencies, which subsequently performs weighted aggregation of value vectors through the matrix multiplication with V. A single instantiation of this computation constitutes an attention head, while multiple parallel heads with independent parameters collectively form the complete MHSA module.

The MHSA module is succeeded by an FFN that enhances non-linear representation capacity. As shown in Figure 2, the FFN first expands input token embeddings via a hidden dimension parameter, then projects them back to the original dimensionality. This expansion-contraction design introduces parameterized feature interactions. Obviously, the hidden dimension size of FFN also influences the computational overhead.

$$
X = \operatorname{Attn} (Q, K, V) = \operatorname{Softmax} \left(\frac {Q K ^ {T}}{\sqrt {l}}\right) \cdot V\tag{1}
$$

THE NOTATION TABLE OF UTFORMER  
TABLE II

<table><tr><td>Variants</td><td>Definition</td></tr><tr><td> $N_h$ </td><td>The number of attention heads</td></tr><tr><td> $N_l$ </td><td>The depth of block layers</td></tr><tr><td>d</td><td>The hidden dimension of FFN</td></tr><tr><td>γ</td><td>The byte-keeping rate</td></tr><tr><td>P</td><td>The configuration of variants,  $P = \{N_h, d, N_l, \gamma\}$ </td></tr><tr><td> $N_{token}$ </td><td>The number of tokens</td></tr><tr><td> $\mathcal{L}$ </td><td>The loss function</td></tr><tr><td> $\mathcal{L}_v$ </td><td>The loss value of neural networks</td></tr><tr><td> $\mathcal{C}_{\mathcal{A}}$ </td><td>The computational cost of self-attention</td></tr><tr><td> $\mathcal{C}_{\mathcal{F}}$ </td><td>The computational cost of FFN</td></tr></table>

## B. Transformer-Based Trafic Classification Models

Unlike conventional DL-based trafic classification approaches that rely on hand-crafted statistical features (e.g., flow duration, packet size distributions) [1], [6], [31], [32], Transformer architectures directly process raw packet bytes through end-to-end learning. Such a paradigm has two advantages: (i) The self-attention mechanism automatically discovers contextual patterns in the content of the application layer that conventional aggregated flow characteristics fail to capture, yielding superior classification accuracy across diverse trafic types. (ii) The elimination of manual feature engineering pipelines removes both human biases in feature selection and computational overhead from pre-processing stages, as models operate directly on raw byte sequences without requiring pre-defined statistical abstractions.

Recent advances in trafic classification have seen increasing adoption of Transformer architectures with varying designs of models. MTT framework [25] employs five Transformer block layers with five self-attention heads per layer, processing a 1500-byte packet by aggregating 50 bytes into one token. Subsequent work, such as MTC [33], hybridizes CNN with transformers for enhanced local feature extraction. In contrast, ET-Bert [19] adapts the BERT architecture from the field of NLP, which implements a twelve-layer deep network with twelve attention heads per layer, becoming the most complex trafic classification transformer currently. While these approaches demonstrate 87%-99% classification accuracy across various datasets, they usually prioritize model performance over lightweight eficiency, overlooking critical system constraints like computational complexity, memory footprint, and practical deployment considerations for resource-constrained network environments.

## III. METHOD

## A. Overview

UTFormer achieves a lightweight Transformer architecture for trafic classification through two key techniques: Dynamic Payload Distillation and Diferential Architecture Search. As illustrated in Figure 3, the framework first applies dynamic payload distillation in the first block layer to adaptively keep important bytes in raw packets, efectively removing redundant computation on less informative bytes. Consequently, the state information of the Transformer (such as accuracy, bytekeeping rate of distillation, and architectural configurations)

![](images/cb1b2b76e2c2711cc03f447a56438b874aca35c2b49498545fc7cd2695befdc8.jpg)  
Fig. 3. The workflow of UTFormer, comprising dynamic payload distillation and diferential architecture search.

is sent to the diferential architecture search to evaluate the computational cost and loss value of the neural network. Through normalization and co-eficient tuning, these terms are then unified in the loss function, which finally guides the diferential architecture search. The latest search result is updated to generate the configurations that determine the architecture of UTFormer. The optimization process terminates automatically when the gradient-based search reaches convergence or the iteration count reaches the predefined budget, delivering a lightweight architecture with low cost and high accuracy. The variants utilized in UTFormer are noted and explained in Table II.

## B. Dynamic Payload Distillation

Modern Transformer-based trafic classification models, such as MTT [25] and ET-BERT [19], employ byte-level tokenization where raw trafic is segmented into fixed-length token sequences. Such a method motivates rephrasing the feature selection challenge: identifying the most useful bytes now reduces to detecting the informative tokens within the self-attention mechanism. Our proposed dynamic payload distillation introduces a novel methodology leveraging the inherent self-attention mechanisms to achieve adaptive byte selection. As mathematically formalized in Equation 2, the computation of the class token $( x _ { c l a s s } )$ inherently encapsulates this distillation process through the attention-scored aggregation across global tokens, where informative tokens emerge naturally from the attention matrix.

In the computation of self-attention, let $q _ { c l a s s }$ denote the query vector and $x _ { c l a s s }$ denote the representation of the class token. The value projection $V = [ \nu _ { 1 } , \nu _ { 2 } , \ldots , \nu _ { n } ] ^ { T }$ constitutes a learnable combination of all n token embeddings, where $\nu _ { i }$ represents the contextual encoding of i-th token. We denote the vector $\mathbf { s } = [ s _ { 1 } , s _ { 2 } , \ldots , s _ { n } ]$ generated by Softmax function in Equation 2. This vector inherently quantifies the crosstoken informative confidence due to the global computation of Softmax. When positioned as the initial token, the attention vector s of the class token corresponds to the first row of the attention matrix. This perspective allows Equation 2 to admit the following reformulation in Equation 3.

$$
x _ {c l a s s} = \text { Softmax } \left(\frac {q _ {c l a s s} \cdot K ^ {T}}{\sqrt {l}}\right) \cdot [ V _ {1}, V _ {2}, \dots , V _ {n} ] ^ {T}
$$

$$
x _ {c l a s s} = [ s _ {1}, s _ {2}, \ldots , s _ {n} ] \cdot [ V _ {1}, V _ {2}, \ldots , V _ {n} ] ^ {T}\tag{2}
$$

(3)

Formally, the attention vector of the class token s defines a set of attention confidence governing the inter-token composition, where $s _ { j }$ quantifies the global contribution of the j-th token to the representation of the class token. As established in Section II-A, the class token represents a global feature integration across the input sample. Consequently, s encodes the confidence relationships between trafic semantics and byte/token-level features within payloads. Higher $s _ { i }$ values indicate a stronger influence between the i-th token and the final classification decision. This attention-driven confidence distribution efectively operates as a dynamic metric, enabling the identification of trafic segments that are most influential to the classification.

Building on our analysis, we propose dynamic payload distillation, as shown in Figure 4. The raw trafic is segmented into discrete tokens, with the class token positioned at the first. After computing the attention matrix through the Softmax function, we extract its first row s, where $s _ { i }$ represents the attention-based confidence score of the i-th token. Tokens are ranked in descending order by $s _ { i } ;$ the Top-K important tokens correspond to the most informative bytes. A tunable bytekeeping rate $\gamma$ controls the distillation process, which retains the Top-[γn] important tokens while removing low-confidence tokens, n is the number of overall tokens in the Transformer. As discussed in further detail in Section III-C, variant γ is diferential, and thereby it can be automatically determined by the diferential architecture search.

![](images/ea3efe3b5cd004c0d6704bab32c9811157f9446b15c053ae83ea2cd8ecff2c41.jpg)  
Fig. 4. Dynamic payload distillation.

The entire dynamic payload distillation occurs between the MHSA and FFN modules, reducing the size of input data for the FFN and subsequent layers. By constraining the distillation to the first block layer of UTFormer, we maximize computational eficiency across all downstream operations while preserving critical information. Moreover, the dynamic payload distillation is established on the attention matrix, which is inherently derived from the computing process of the self-attention module. Only a simple Top-K sorting operation is added to the distillation process, introducing no significant overhead to the UTFormer.

## C. Diferential Architecture Search

Dynamic payload distillation efectively improves the input redundancy of the input data. To further remove the architectural redundancy of Transformer models, we propose the diferential architecture search.

The architectural configuration of UTFormer is governed by four key parameters: the number of attention heads in MHSA modules $( N _ { h } )$ , the depth of block layers (N<sub>l</sub>), the hidden dimension of FFN (d), and the byte-keeping rate (γ) from the dynamic payload distillation. We formalize these as a multidimensional parameter space $P = \{ N _ { h } , d , N _ { l } , \gamma \}$ to jointly optimize the computational overhead and prediction accuracy of the Transformer models. However, these parameters formulate a complex problem space, where manual parameter tuning could be prohibitively expensive due to exponential state-space growth. To address this problem, we implement an automated parameter optimization via stochastic gradient descent (SGD)-based search. This approach automatically navigates the configuration space to identify near-optimal architectures of UTFormer that balance computational eficiency and task accuracy.

1) Problem Space: Stochastic gradient descent operates as an iterative optimization protocol that approximates gradient descent by stochastically sampling gradient directions to minimize a diferentiable loss function. This stochastic approximation enables an eficient search of the highdimensional parameter spaces. However, employing SGD to optimize the architecture of UTFormer faces two critical challenges. (i) Multiscale parameter coordination: The architectural parameter space $P = \{ N _ { h } , d , N _ { l } , \gamma \}$ contains variables with significantly mismatched numerical characteristics. The byte-keeping rate γ operates in a continuous space (0 1], while structural parameters $N _ { l }$ and $N _ { h }$ usually occupy small integer domains {1 2 3 12}. In contrast, the hidden dimension d spans large integer values over 1024. This discrepancy, from 0.01-scale for γ to 1000-scale variations for $d ,$ creates unstable gradient interactions during joint optimization. (ii) Discrete parameters search. Key architectural parameters $( N _ { h } , d , N _ { l } )$ inherently reside in discrete integer spaces, fundamentally conflicting with the requirement of SGD for continuous differentiable variables. Direct gradient computation becomes infeasible for these integer parameters. This mismatch between discrete search space and continuous optimization mechanics frequently leads to suboptimal architectural convergence.

2) Methods: To address such problems, we propose the architectural normalization via L1-regularization on P. Each parameter $p ^ { t } \in P$ in the t-th iteration is first projected into a unified numerical space through range normalization as in Equation 4. The Max(p) is the architecture-specific upper bound, e.g., Max(N<sub>l</sub>) = 12 aligned with the configurations of ET-Bert, currently the largest Transformer-based trafic classification model. This transformation eliminates magnitude disparities by constraining all parameters to $p _ { R } ^ { t } ~ \in ~ ( 0 , 1 ]$ while preserving relative scaling relationships. Moreover, the architectural normalization via L1-regularization induces an approximate continuous space for originally discrete integer parameters, making theoretical gradients exist across all architectural variables. Consequently, in Equation 5, SGD searches in this approximate continuous space, and parameters are updated along the regularized gradient directions while maintaining architectural validity. After each optimization step, $N _ { l } , N _ { h }$ , and d are mapped back to their native integer domains via rounding operations in Equation 6, completing the current optimization step of UTFormer architecture search.

$$
p _ {R} ^ {t} = \| p ^ {t} \| = \frac {p ^ {t}}{\mathrm{Max} (p)}\tag{4}
$$

$$
p _ {R} ^ {t + 1} = p _ {N} ^ {t} - l r \cdot \frac {\partial l o s s}{\partial p _ {R} ^ {t}}
$$

$$
p ^ {t + 1} = \operatorname{round} (p _ {R} ^ {t + 1}, \operatorname{Max} (p))\tag{5}
$$

(6)

3) Algorithm: The entire SGD-based searching method is illustrated in algorithm 1. The SGD-based search procedure (Algorithm 1) begins by initializing the parameter P and the SGD learning rate lr. A Transformer instance Model(P) is constructed through parametric configuration and trained for multiple epochs, followed by the evaluation of its accuracy via validation loss loss (line 2-3). This metric feeds into our proposed loss function, where subtracting the historical loss baseline $\Omega _ { L o s s }$ yields the loss variance 4loss for gradient computation (line 4-5). Based on these gradients, we update to regularized parameters $P _ { R }$ (line 6), which are subsequently discretized to their integer form P (line 7-8). The process iteratively refines P until parameter stability or maximum iteration count is reached, ultimately producing near-optimal configurations for UTFormer (line 9).

```txt
Algorithm 1 SGD-Based Searching
Input: A set of initial parameters P, learning rate lr
Output: the final parameters of P
1: while P is unstable or # iter ≤ max iter count do
2: train the Model(P)
3: loss_v ← Validate(Model(P))
4: Loss ← Loss function(loss_v, P)
5: get Δloss && ΩLoss ← Loss
6: ∂PR ← get_grad(ΔLoss, ΩLoss, lr, PR)
7: update PR with ∂PR
8: P ← PR
9: end while
```

## D. Unified Loss Function

Our loss function in Equation 7 mediates the important accuracy-eficiency trade-of in Transformer architecture search. $\mathcal { L } _ { \nu } ( P )$ directly quantifies the model accuracy under architecture configuration P through the model forwarding, making SGD iterations acquire the accuracy performance. The computational cost term C(P) uses floating-point operations (FLOPs) as an architecture complexity metric. For Transformer-based trafic classification models, we derive C(P) by layer-wise FLOP estimation in Equation 8.

$$
\mathcal {L} = \alpha \| \mathcal {L} _ {v} (P) \| + \beta \| \mathcal {C} (P) \|\tag{7}
$$

$$
\mathcal {C} (P) = \mathcal {C} _ {\mathcal {A}} (P) + \gamma [ (N _ {l} - 1) \mathcal {C} _ {\mathcal {A}} \gamma (P) + N _ {l} \mathcal {C} _ {\mathcal {F}} (P) ]
$$

$$
\mathcal {C} _ {\mathcal {A}} (P) = 6 \cdot N _ {h} \cdot N _ {t o k e n} \cdot l ^ {2} + 2 \cdot N _ {h} \cdot N _ {t o k e n} ^ {2} \cdot l\tag{8}
$$

(9)

$$
\mathcal {C} _ {\mathcal {A}} \gamma (P) = 6 \cdot N _ {h} \cdot \gamma N _ {t o k e n} \cdot l ^ {2} + 2 \cdot N _ {h} \cdot \gamma^ {2} N _ {t o k e n} ^ {2} \cdot l\tag{10}
$$

$$
\mathcal {C} _ {\mathcal {F}} (P) = 4 \cdot l \cdot d \cdot \gamma N _ {t o k e n}\tag{11}
$$

1) Computational Cost: The computational cost of Transformer models emerges mainly from MHSA and FFN modules. The dynamic payload distillation is positioned after the first MHSA module, and thus, the subsequent modules only need to process the kept tokens. Therefore, it is necessary to calculate the computation of the first MHSA $( { \mathcal { C } } _ { A } )$ and other MSHA modules $( \mathcal { C } _ { A } \gamma )$ , respectively. The computational cost of the first MHSA module approximately contains two parts: the matrix multiplication of calculating Q K V, and the following operations, such as Softmax. The calculation of two parts is separately demonstrated in Equation 9, where $N _ { t o k e n }$ denotes the number of tokens (bytes). Similarly, the computation of other MHSA modules can be calculated by Equation 10, with γ controlling the distillation process. This equation reveals that the number of tokens greatly influences the computational complexity of the Transformer model with a quadratic proportionality, reflecting the critical importance of dynamic payload distillation for reducing redundant tokens. After each MHSA, FFN mainly utilizes two linear layers for token computing, with d determining its computational complexity. We calculate its computational cost by the equation 11.

2) Trade-of Through Co-Eficient Tuning: The unified loss formulation faces a similar numerical stability challenge where the loss value of Transformer models $\mathcal { L } _ { \nu }$ typically resides in the (0 2] range, while the computational cost C spans nine orders of magnitude (GFLOPs). We address this problem by the normalization method introduced in Section III-C.2 as well. Additionally, we employ two coeficients α and $\beta$ to explicitly control the accuracy-cost trade-of, where α modulates prediction accuracy and $\beta$ governs computational overhead. Section V-B quantifies their sensitivity through ablation studies.

## IV. DATASET PREPARATION: PRE-PROCESSING &SPLITTING

UTFormer is evaluated on six diferent trafic datasets and classification tasks, as demonstrated in Table III.

• ISCX-VPN-2016 (ISCX) datasets [34]: This dataset collects six classes (E-mail and FTP, etc.) of trafic encrypted by VPN. The encrypted trafic classification task is conducted on this dataset to evaluate the UTFormer.

• USTC-TFC (app) datasets [22]: The USTC-TFC (app) dataset includes application-level (app-level) trafic from ten popular applications. Therefore, we perform application-level trafic classification tasks to validate UTFormer using this dataset.

• USTC-TFC (malware) datasets [22]: The USTC-TFC (malware) dataset contains both normal and malware trafic for intrusion detection tasks. Six diferent types of attack trafic are collected in the dataset.

• Cross-platform-android [35]: The dataset collects encrypted trafic data of the 121 most popular applications on Android. The collected data ofers the base of encrypted app-level trafic classification.

• Cross-platform-iOS [35]: The dataset collects encrypted app-level trafic from the 167 most popular applications on iOS. The task in this dataset is encrypted app-level trafic classification as well.

• CampusVideo: This dataset (CapVideo) targets five popular video applications in China (e.g., TikTok and Tencent Meeting) and was collected from the campus network in 2024. To better support application-level trafic classification, CapVideo also includes background trafic from the campus network, reflecting real-world trafic patterns. All trafic in the dataset has been anonymized to preserve privacy.

Following standard practice in trafic classification [17], [25], we adopt a uniform per-packet pre-processing pipeline, including: (1) remove Ethernet headers, (2) mask IP address in network-layer headers, and (3) mask transport-layer port numbers to prevent potential bias from layer-2/3/4 identifiers. Besides, SYN/ACK/FIN packets, and packets of ICMP/ARP protocols are removed. (4) The remaining header fields and payload are concatenated and zero-padded to a fixed 1500-byte length, enabling dynamic payload distillation to have full-sequence attention on any possible valuable bytes. (5) Each byte undergoes a float-32 projection via $x ^ { \prime } = x / 2 5 6$ where 8-bit unsigned range [0 255] is mapped to the float range [0 1]. For each dataset, we partition the data by flow into training, validation, and test sets: 70% of the flows and their constituent packets are assigned to the training set, 10% to the validation set, and 20% to the test set. The code for dataset pre-processing and splitting is open-sourced at our homepage for reproduction.

TABLE III  
THE DETAIL OF SIX EVALUATED DATASETS, THREE OF THEM COLLECT ENCRYPTED TRAFFIC FROM REAL-WORLD APPLICATIONS

<table><tr><td>Datasets</td><td>ISCX-VPN-2016</td><td>USTC-TFC (app)</td><td>USTC-TFC (malware)</td><td>Cross-platform-android</td><td>Cross-platform-iOS</td><td>CapVideo</td></tr><tr><td>Category</td><td>Encrypted</td><td>App-level</td><td>Malware</td><td>Encrypted &amp; App-level</td><td>Encrypted &amp; App-level</td><td>App-level</td></tr><tr><td># Classes</td><td>6</td><td>10</td><td>6</td><td>121</td><td>167</td><td>6</td></tr><tr><td># Train-pkts</td><td>3.1M</td><td>1.5M</td><td>3.5M</td><td>299.8K</td><td>2.5M</td><td>3.1M</td></tr><tr><td># Test-pkts</td><td>880.5K</td><td>581.7K</td><td>1.2M</td><td>85.7K</td><td>733.3K</td><td>1.3M</td></tr><tr><td>Volume</td><td>20 GB+</td><td>3.1 GB</td><td>3.9 GB</td><td>0.75 GB</td><td>2.41 GB</td><td>3.31 GB</td></tr></table>

TABLE IV  
THE OFFLINE AND ONLINE EXPERIMENTS

<table><tr><td>Paradigm</td><td>Tasks</td><td>Evaluation metrics</td></tr><tr><td>Offline</td><td>Train &amp; search UTFormer, Reproducing baselines, Test architectural efficiency.</td><td>Accuracy: AC, PR, RC, F1, Efficiency: inference/sec and memory footprint.</td></tr><tr><td>Online</td><td>Test end-to-end throughput and real-time latency.</td><td>Throughput: bits/sec (bps), Latency: millisecond (ms).</td></tr></table>

Fig. 5. Online end-to-end test bed.

## V. EXPERIMENTAL SETUP AND IMPLEMENTATION

## A. Experimental Environment and Evaluation Metrics

The evaluations of UTFormer and baselines involve two paradigms: the ofline experiments and the online end-to-end experiments, as summarized in Table IV.

1) Ofline Evaluation: The ofline evaluation encompasses the diferential architecture search and training for UTFormer, as well as the reproduction of all baseline models. Each model is validated by two orthogonal dimensions: (1) Trafic analysis capability, measured by classification accuracy (AC), precision (PR), recall (RC), and F1 score (F1); (2) Architectural eficiency, quantified by inference-per-second (IPS) and GPU memory footprint on a server platform.

2) Online Evaluation: The online evaluation accesses the performance of distinct models in real-world deployment environments using the end-to-end test bed shown in Figure 5. The test bed incorporates a trafic tester that replays trafic collected by diferent datasets to a GPU server through a 10 Gbps NIC. We implement a C-based DPDK program to receive test trafic into a 4GB shared memory bufer, which is accessed by four Python-based threads transforming raw trafic into PyTorch tensors. These trafic tensors are batched every 4096 packets and then moved to the GPU to trigger model inference. We define a model’s end-to-end throughput as the maximum input trafic rate it can sustain without causing bufer overflow, and its latency as the end-to-end delay to inference one data batch under deployment conditions.

3) Hardware and Software Configurations: Both ofline and online experiments are conducted on a system equipped with an NVIDIA RTX 4090 GPU (48 GB GPU memory), an Intel Core i9-14900K CPU, and 80 GB of DRAM, running Ubuntu 20.04 with Numpy 1.24, PyTorch 1.13.1, CUDA 11.6, and cuDNN 8. In the online evaluation, the test bed employs an Intel 82599ES 10 GbE NIC and a TOYO Corporation SYNE-SIS trafic tester to replay trafic from pcap files and receive trafic at line rate (10 Gbps). The DPDK version is 22.11.

## B. Implementation

The implementation of UTFormer includes the diferential architecture search phase and the final model training, with distinct configurations aligned to each stage.

1) Configurations of the Diferential Architecture Search: We constrain architectural parameters $P = ( N _ { h } , N _ { l } , d , \gamma )$ with maximum thresholds $N _ { h } ^ { m a x } \ = \ 1 2 , N _ { l } ^ { m a x } \ = \ 1 2 , d ^ { m a x } \ = \ 1 0 2 4$ Such configuration is inherited from ET-Bert [19] (12 selfattention heads and 12 block layers). We enforce $\gamma > = 0 . 0 5$ to prevent catastrophic information loss while preserving at least five tokens (one class token plus four content tokens). With the learning rate= 0.005, each SGD iteration includes four model training epochs for stable loss estimation.

2) The Configurations of the Unified Loss Function: The unified loss function balances accuracy and computational cost by setting $( \alpha = 0 . 5 , \beta = 1 . 5 )$ . The computational cost regularization uses the cost of ET-Bert, the largest Transformer-based trafic classification model, as the regularization upper bound for architecture search. The SGD searching terminates with 15 iterations or early-stopping when the loss function becomes stable.

3) The Configurations ofthe Model Training: We set batchsize as 256 across all datasets, with the use of the Adam optimizer and a learning rate = 0.001. Once the architecture of UTFormer is determined, we further train the model with another 40 epochs using the cross-entropy loss function.

## C. Baseline Models and Reproduction

We evaluate UTFormer against multiple representative DL-based models. The baseline models span (1) Light-weight CNN architectures with model size smaller than 20 MB, (2) Transformer models with model size ranging from 40 MB to 576MB, and (3) The latest large-language-model-based approach requiring over 1 GB parameters. (4) The latest Mamba-based model, which is established on state space model (SSM). The architectural detail of all baseline models is listed in Table V.

TABLE V  
THE ARCHITECTURAL COMPARISON BETWEEN UTFORMER AND BASELINES

<table><tr><td>Model</td><td>Model type</td><td># Layer</td><td># Head</td><td>Hidden dimension</td><td>Byte-keeping rate</td><td>Model size</td><td>Computation cost</td></tr><tr><td>MTC-CNN[33]</td><td>Light-weight CNN</td><td>15</td><td>-</td><td>-</td><td>-</td><td>19.5 MB</td><td>521.3 MFLOPs</td></tr><tr><td>DeepFP[36]</td><td>Light-weight CNN</td><td>12</td><td>-</td><td>-</td><td>-</td><td>15.7 MB</td><td>444.2 MFLOPs</td></tr><tr><td>MTT[25]</td><td>Transformer</td><td>5</td><td>5</td><td>1024</td><td>-</td><td>40.6 MB</td><td>1.1 GFLOPs</td></tr><tr><td>ET-Bert[19]</td><td>Transformer</td><td>12</td><td>12</td><td>768</td><td>-</td><td>576 MB</td><td>5.7 GFLOPs</td></tr><tr><td>TrafficFormer[17]</td><td>Transformer</td><td>12</td><td>12</td><td>768</td><td>-</td><td>576 MB</td><td>5.7 GFLOPs</td></tr><tr><td>PcapEncoder[37]</td><td>LLM-based</td><td>24</td><td>24</td><td>768</td><td>-</td><td>1210 MB</td><td>11.8 GFLOPs</td></tr><tr><td>NetMamba+[38]</td><td>Mamba</td><td>6</td><td>-</td><td>-</td><td>-</td><td>27 MB</td><td>694 MFLOPs</td></tr><tr><td>UTF-ISCX</td><td>Light-weight Transformer</td><td>1</td><td>4</td><td>268</td><td>5%</td><td>156 KB</td><td>241.8 kFLOPs</td></tr><tr><td>UTF-USTC-app</td><td>Light-weight Transformer</td><td>1</td><td>1</td><td>64</td><td>5%</td><td>106 KB</td><td>156.6 kFLOPs</td></tr><tr><td>UTF-USTC-mal</td><td>Light-weight Transformer</td><td>1</td><td>1</td><td>72</td><td>5%</td><td>107 KB</td><td>160.0 kFLOPs</td></tr><tr><td>UTF-android</td><td>Light-weight Transformer</td><td>4</td><td>4</td><td>224</td><td>25%</td><td>8.8 MB</td><td>122.8 MFLOPs</td></tr><tr><td>UTF-iOS</td><td>Light-weight Transformer</td><td>4</td><td>4</td><td>256</td><td>15%</td><td>12.8 MB</td><td>87.3 MFLOPs</td></tr><tr><td>UTF-CapVideo</td><td>Light-weight Transformer</td><td>1</td><td>1</td><td>64</td><td>10%</td><td>106 KB</td><td>180.4 kFLOPs</td></tr></table>

• MTC-CNN [33] is a light-weight CNN model implementing three 1D convolutional layers for raw packet processing. This model is selected to directly compare the computational eficiency with UTFormer.

• DeepFP [36] is a light-weight CNN model that utilizes trafic features such as the size and direction information of the trafic. These features are organized into a 2D feature map for CNN inference. Choosing this model demonstrates the comparison between the featureengineering-based model and end-to-end learning.

• MTT [25] is a vanilla transformer with five layers and five self-attention heads per layer.

• ET-Bert basically follows the architecture of Bert [13] (comprises 12 block layers), and each layer includes 12 self-attention heads with a hidden dimension of 768.

• TraficFormer [17] is a derivative of ET-Bert and achieves state-of-the-art (SOTA) accuracy by improving training methods.

• PcapEncoder [37] is a pretrained model based on T5 [39], an open-source large language model (LLM). The LLM-based PcapEncoder is the largest model in the field of trafic classification, demonstrating generalization to diferent trafic datasets.

• NetMamba+ [38] is built on SSM-based Mamba model, which combines the high accuracy of Transformer models and the low-overhead of RNNs.

MTC-CNN, MTT, ET-Bert, PcapEncoder, and NetMamba+ provide open-sourced pretrained parameters for their backbone neural network (NN). As PcapEncoder suggested, we reuse these backbone parameters and keep them frozen, only adding and training a dataset-adaptive classifier layer following the backbone. Meanwhile, DeepFP and TraficFormer do not release pretrained parameters; therefore, we train both models entirely from scratch. In ofline experiments, we use a batch size of 256 and a learning rate of 0.0001 to train UTFormer and reproduce all baselines for 30 epochs during the ofline experiments, as detailed in Section V-A.

## VI. EVALUATION

## A. Evaluation Guideline

In Section VI-B, we introduce the architectural configurations of UTFormer with a comparison of baseline models.

Consequently, we conduct comprehensive end-to-end comparative experiments on accuracy performance (in Section VI-C), practical throughput (in Section VI-D). In the Ablation Study Section, we thoroughly explore the mechanism of the proposed diferential architecture search (Section VII-A) and dynamic payload distillation (Section VII-B). Several experiments are designed to validate the convergence performance of the diferential architecture search. Simultaneously, the deep dive reveals the position of the most informative bytes within the payload, and dynamic payload distillation can potentially be an of-the-shelf lightweight technique for Transformer-based trafic classification models.

## B. The Architecture of UTFormer

In Table V, we present the architectural configurations determined by the diferential architecture search. The resultant models are denoted by the namesake of respective datasets, as listed in Table V (UTF-ISCX, UTF-USTC-app, UTF-USTCmal, UTF-android, UTF-iOS, and UTF-CapVideo).

1) Architectural Eficiency: UTFormer exhibits outstanding light-weight capacity across diferent datasets. On ISCX-VPN, USTC-TFC (app), USTC-TFC (mal), and CapVideo datasets, the search converges to a single-layer architecture, maintaining 100KB-level model size. Dynamic payload distillation further eliminates 90%-95% of input bytes, yielding computation below 200 kFLOPs. On Cross-platform-android and Cross-platform-iOS datasets, UTFormer adapts to multi-class challenges with a configuration of 4 block layers ×4 heads, expanding model size to MB-level. Despite the parameter growth, the distillation removes 75%-85% of input, saving over 9 0× computational cost.

2) Architectural Comparison: UTFormer exhibits significant architectural eficiency improvements over CNN baselines. UTFormer achieves 1.2-1844 3× reduction in model size compared to MTC-CNN and DeepFP, reducing computational cost by 3.6-3328 9×. In contrast to Transformer baselines, UTFormer removes redundancy in both model architecture and input. Existing Transformers like ET-Bert [17], [19] directly adopt Bert-based architectures [13] with fixed-length payload inputs (e.g, 1500B in MTT [25]), leading to excessive model size up to 576 MB and computation overhead over 1 GFLOPs. Our evaluation shows that UTFormer reduces the model size by 44.9-5433 9× while eliminating redundant computation by 9.0-36398 5×. When compared to PcapEncoder, a LLM-based trafic analysis model, the model size of UTFormer is up to five orders of magnitude smaller, and the computational cost is reduced by up to four orders of magnitude. Moreover, UTFormer still delivers 2.11-254 7× smaller model size than NetMamba+, and further reduces 5.65-4448 7× computation.

TABLE VI  
THE ACCURACY RESULTS ACROSS DISTINCT DATASETS. THE HIGHEST VALUE OF ACCURACY IS HIGHLIGHTED IN RED, AND THE SECOND-HIGHEST VALUE IS IN YELLOW. THE DIFFERENCE IN PARENTHESES REPRESENTS THE GAP BETWEEN UTFORMER AND THE BEST ACCURACY

<table><tr><td>Datasets</td><td colspan="4">USTC-TFC (app)</td><td colspan="4">USTC-TFC (mal)</td><td colspan="4">ISCX-VPN-2016</td></tr><tr><td>Metrics (%)</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td></tr><tr><td>MTC-CNN[33]</td><td>99.41</td><td>99.74</td><td>99.53</td><td>99.40</td><td>98.52</td><td>98.65</td><td>98.62</td><td>98.60</td><td>95.75</td><td>91.94</td><td>92.92</td><td>93.31</td></tr><tr><td>DeepFP[36]</td><td>78.83</td><td>78.19</td><td>78.59</td><td>78.77</td><td>85.09</td><td>86.33</td><td>85.74</td><td>85.88</td><td>68.45</td><td>66.78</td><td>67.81</td><td>67.23</td></tr><tr><td>MTT[25]</td><td>99.97</td><td>99.68</td><td>99.88</td><td>99.68</td><td>99.98</td><td>99.88</td><td>99.95</td><td>99.97</td><td>95.75</td><td>91.94</td><td>92.92</td><td>93.31</td></tr><tr><td>ET-Bert[19]</td><td>99.15</td><td>99.16</td><td>99.15</td><td>99.16</td><td>99.99</td><td>99.99</td><td>99.99</td><td>99.99</td><td>94.39</td><td>97.31</td><td>95.33</td><td>95.29</td></tr><tr><td>TrafficFormer[17]</td><td>99.80</td><td>99.21</td><td>99.50</td><td>99.71</td><td>99.99</td><td>99.99</td><td>99.99</td><td>99.99</td><td>96.21</td><td>94.50</td><td>95.80</td><td>95.89</td></tr><tr><td>PcapEncoder[37]</td><td>97.28</td><td>97.05</td><td>97.10</td><td>99.71</td><td>100</td><td>100</td><td>100</td><td>100</td><td>91.03</td><td>88.24</td><td>89.85</td><td>92.12</td></tr><tr><td>NetMamba+[38]</td><td>97.68</td><td>97.50</td><td>97.65</td><td>97.65</td><td>99.92</td><td>99.99</td><td>99.95</td><td>99.95</td><td>94.50</td><td>92.55</td><td>94.20</td><td>94.60</td></tr><tr><td>UTFormer</td><td>99.78</td><td>99.66</td><td>99.74</td><td>99.69 (-0.02)</td><td>99.99</td><td>99.99</td><td>99.99</td><td>99.99 (-0.01)</td><td>94.02</td><td>91.01</td><td>93.24</td><td>94.35 (-1.54)</td></tr></table>

<table><tr><td>Datasets</td><td colspan="4">Cross-platform-android</td><td colspan="4">Cross-platform-iOS</td><td colspan="4">CapVideo</td></tr><tr><td>Metrics (%)</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td><td>RC</td><td>PR</td><td>F1</td><td>AC</td></tr><tr><td>MTC-CNN[33]</td><td>79.63</td><td>78.72</td><td>80.34</td><td>82.04</td><td>70.04</td><td>75.67</td><td>71.38</td><td>78.05</td><td>95.45</td><td>96.03</td><td>95.50</td><td>95.24</td></tr><tr><td>DeepFP[36]</td><td>22.32</td><td>21.79</td><td>21.40</td><td>31.06</td><td>25.95</td><td>26.20</td><td>25.27</td><td>38.62</td><td>93.97</td><td>94.60</td><td>94.27</td><td>94.50</td></tr><tr><td>MTT[25]</td><td>76.28</td><td>75.91</td><td>75.50</td><td>87.72</td><td>86.21</td><td>86.11</td><td>85.84</td><td>87.89</td><td>96.35</td><td>98.58</td><td>97.61</td><td>96.44</td></tr><tr><td>ET-Bert[19]</td><td>86.39</td><td>83.19</td><td>84.06</td><td>89.28</td><td>87.57</td><td>87.72</td><td>87.54</td><td>89.10</td><td>99.55</td><td>96.41</td><td>98.88</td><td>98.50</td></tr><tr><td>TrafficFormer[17]</td><td>74.35</td><td>72.04</td><td>71.67</td><td>86.64</td><td>89.66</td><td>86.97</td><td>88.89</td><td>89.97</td><td>96.18</td><td>97.33</td><td>97.23</td><td>97.83</td></tr><tr><td>PcapEncoder[37]</td><td>78.06</td><td>76.51</td><td>77.30</td><td>87.36</td><td>80.54</td><td>89.99</td><td>80.63</td><td>87.10</td><td>98.99</td><td>96.55</td><td>98.86</td><td>98.89</td></tr><tr><td>NetMamba+[38]</td><td>86.14</td><td>86.48</td><td>87.23</td><td>87.03</td><td>88.11</td><td>88.21</td><td>89.92</td><td>89.96</td><td>97.65</td><td>98.08</td><td>97.70</td><td>97.71</td></tr><tr><td>UTFormer</td><td>86.70</td><td>85.33</td><td>86.29</td><td>87.79 (-1.49)</td><td>87.96</td><td>87.01</td><td>87.63</td><td>89.87 (-0.10)</td><td>97.23</td><td>95.71</td><td>96.21</td><td>96.88 (-2.01)</td></tr></table>

## C. Accuracy Performance

Table VI presents the comparison of classification accuracy across six datasets. UTFormer is compared against diverse baselines.

1) UTFormer Versus Light-Weight CNN and Mamba Baselines: As shown in Table VI, our transformer architecture achieves 0.29%-11.82% higher accuracy than MTC-CNN and 14.11%-56.73% absolute accuracy gains over DeepFP across all evaluation scenarios. DeepFP exhibits an unsatisfactory accuracy (38.2%-52.1%), corroborating prior findings [19], [25] about the limitations of feature-based models in handling complex trafic patterns. Moreover, the overall comparison results demonstrate that CNN models fail on accuracycomputational cost eficiency, with a non-negligible gap where UTFormer outperforms CNNs with higher accuracy and lower cost. This eficiency gap stems from structural ineficiencies in CNNs architectures: these CNNs models employ multi-layer convolutional stacks and process full-length sequence inputs, leading to parameter redundancy and unsatisfied computational cost. Our findings align with prior studies [18], [19] that have identified CNNs as suboptimal for trafic classification tasks, which means CNNs require a larger model to achieve comparable accuracy to UTFormer. Based on the architectures of Mamaba models, NetMamba+ achieves accuracy comparable to UTFormer. However, linear feature processing methods make NetMamba+ to occupy 2 11× more parameters for high accuracy, indicating a lower parameter eficiency.

2) UTFormer Versus Transformer and LLM-Based Baselines: Across distinct datasets, PcapEncoder exhibits the best accuracy in most cases, demonstrating the performance and generalization of the LLM-based approach. Meanwhile, with UTFormer achieving second-place rankings in three datasets, our experimental evaluation reveals that UTFormer consistently achieves top-tier accuracy across multiple datasets and trafic analysis tasks, often matching the performance of much heavier models such as PcapEncoder. Although minor gaps exist in some cases (e.g., 1.54% lower than TraficFormer on the ISCX-VPN dataset), these are worth it relative to the gains in architectural eficiency. Moreover, all Transformer architectures (including UTFormer) consistently achieve high accuracy across six diverse datasets, confirming their architectural superiority for trafic classification. Transformer models average exceed CNNs by 1.04%-51.17% on accuracy.

## D. Inference Performance

As illustrated in Figure 6, further evaluations are conducted in both ofline and online environments to compare UTFormer to other baselines.

1) Ofline Evaluations: To validate inference performance under ofline settings, we use a batch size of 512 for all models to report metrics of inference-per-second (IPS) and memory footprint. The results are depicted in Figure 6a. Due to its large model size and high computational cost, the LLM-based PcapEncoder occupies over 3GB of GPU memory and achieves only 0.07 million IPS (MIPS) in the experiments. Compared to light-weight CNN approaches, Transformer baselines generally demand more memory and deliver lower IPS performance. However, CNN models fall short on accuracy metrics. NetMamba+ delivers higher IPS performance and lower memory footprint than other CNNs and Transformer models due to lightweight SSM architecture. Meanwhile, our experiments demonstrate that

![](images/58031cdd46931eb68ca1655c052f51588b820c7c699c0d4ad5ec64baf6b169b6.jpg)

(a) Evaluating inference performance and memory footprint in Offline experiments.  
![](images/41d14fc9c7fa50ab29352f3b887901863d72aadc4431dac0a15da95fa6896a01.jpg)  
(b) Evaluating real-time throughput and inference latency in Online experiments.

Fig. 6. Inference performance.  
![](images/d3a4bf42d970457f6e21282653b40f77d978c5fccf2d1384188a78ddddb05757.jpg)

![](images/b296fb273d927724561a4e849046f08425e856f4cb251ccc13b8aa80564fe7e7.jpg)  
(a) The convergence process of (b) The convergence process of loss value. variants in $P .$  
Fig. 7. The convergence process of diferential architecture search. The convergence is completed within 12 iterations.

UTFormer achieves competitive accuracy as well as strong inference performance. Due to its lightweight architecture, UTFormer performs 3 28−7 55 MIPS performance across different datasets, achieving 107 85× speedup over LLM-based PcapEncoder, 50 33× higher throughput than other Transformers, and 14 25× speedup over CNN baselines. Moreover, the memory eficiency of UTFormer is substantial, only requiring 40-96 MB of GPU memory space, which is 2.48-14 13× smaller than CNNs, and 41 56× smaller than Transformer and LLM-based baselines on average.

2) Online Evaluations: The online evaluations are conducted on our real-world test bed, as described in Section V-A. The trafic tester generates replay trafic to the GPU server to validate the deployability of diferent trafic analysis models. We use two key metrics: (1) end-to-end throughput, defined as the maximum input trafic rate a model can sustain without causing bufer overflow, and (2) inference latency, defined as the end-to-end delay to process one data batch. As depicted in Figure 8b, LLM-based and other Transformer baselines deliver throughput lower than 100 Mbps and end-to-end inference latency exceeding 1 second, making them impractical to deploy in a real-world trafic analysis environment due to the performance bottlenecks. Two CNN baselines attain throughput of 1.2-1.8 Gbps with 96-954 milliseconds (ms) inference latency. However, their deployment is still limited by inferior accuracy. Simultaneously, NetMamba+ achieves 4.8 Gbps throughput and 0.08 ms inference latency in online evaluation, demonstrating the lightweight advantage of SSM architecture. In contrast, UTFormer demonstrates superior performance and practical deployability. It reaches 10 Gbps line-rate throughput across four datasets, with a minimum inference latency of 0.11 ms. UTFormer outperforms Transformer and LLM-based baselines by 125.0-333 3× on throughput and up to 28481 8× on inference latency. The experiments conclusively demonstrate the capacity and potential performance of UTFormer for real-world deployment in high-speed trafic analysis tasks.

![](images/514dd999e6c112dbb87bb4889e5405d6cddbb422bc1f2bd8dc99cb63c7aece78.jpg)  
(a) Evaluation on ISCX dataset.

![](images/fd4babe85dce499be955ac954b5482508b67c7b0d8209664b6b87ca8fe7602f3.jpg)  
(b) Evaluation on USTC dataset

![](images/592c338ade4318a69c46e12328e744f1cdef192dea2d9b6058b7d05558e8520c.jpg)  
(c) Evaluation on iOS dataset.

![](images/012ebb5aa7255510928324c7b70f8640d57c495fac9a6d882b8acf0537d9a9cd.jpg)  
(d) Evaluation on Android dataset.  
Fig. 8. Ablation experiments on Rand-k and SVD-k.

## VII. ABLATION STUDY AND DEEP DIVE

## A. Evaluation on Diferential Architecture Search

1) Setup: As discussed in Section V-B, our diferential architecture search constrains parameters $P = ( N _ { h } , N _ { l } , d , \gamma )$ with maximum thresholds $N _ { h } ^ { m a x } = 1 2 , N _ { l } ^ { m a x } = 1 2 , d ^ { m a x } = 1 0 2 4$ The byte-keeping rate $\gamma ~ \in ~ [ 0 . 0 5 , 1 ]$ preserves at least five tokens to prevent catastrophic information loss. Each search iteration performs four training epochs for stable loss estimation, guided by a unified loss function balancing accuracy and eficiency $( \alpha = 0 . 5 , \beta = 1 . 5 )$ . The search terminates at 15 iterations or when parameters stabilize through early stopping.

TABLE VII  
MODEL SEARCHED BY DIFFERENT COEFFICIENT CHOICES. FROM RIGHT TO THE LEFT, LOSS FUNCTION WEIGHTS MORE ON REDUCING COMPUTATIONAL COST

<table><tr><td>(α : β)</td><td>3: 1</td><td>2: 1</td><td>1: 1</td><td>0.5: 1</td></tr><tr><td>Model size</td><td>4.6MB</td><td>2.2 MB</td><td>744 KB</td><td>156 KB</td></tr><tr><td>byte-keeping rate</td><td>42%</td><td>24%</td><td>10%</td><td>5%</td></tr><tr><td>Computation (FLOPs)</td><td>63.9M</td><td>30.7M</td><td>2.6M</td><td>241.8K</td></tr><tr><td>Accuracy</td><td>95.01%</td><td>94.81%</td><td>94.69%</td><td>94.35%</td></tr></table>

2) Convergence Performance: Figure 7 captures this optimization trajectory on the ISCX-VPN dataset, showing how the loss function progressively leads to an ultra-lightweight architecture. Figure 7a reveals that the diferential architecture search completes convergence within 12 iterations despite a conservative 15-iteration search maximum. To analyze the convergence process in detail, we depict the trajectory of all variants of $P$ in Figure 7b. Two architectural parameters $N _ { l }$ (the number of layers) and $N _ { h }$ (The number of self-attention heads) reach convergence at the 5th iteration. Their relatively small search space $( N _ { h } , N _ { l } \in \{ 1 , 2 , 3 , \dots , 1 2 \} )$ ensures a rapid convergence speed. On the other hand, γ (byte-keeping rate) and d (the hidden dimension) convergence around 10-12th iterations due to larger search space $( \mathbf { e . g . , } d \in \{ 1 , 2 , \dotsc , 1 0 2 4 \} )$ . All relevant variants in P are stabilized within 12 iterations, enabling fast convergence.

3) Discussion on Co-Eficient Choices of Loss Function: To validate the impact of diferent coeficient choices in the unified loss function, we design four groups of experiments with $( \alpha = 3 , \beta = 1 ) , ( \alpha = 2 , \beta = 1 ) , ( \alpha = 1 , \beta = 1 )$ , and the configuration $( \alpha = 0 . 5 , \beta = 1 )$ adopted in UTFormer. Loss function with larger α weighs more on the accuracy term and less on the cost term, guiding the complicated trade-of of the architecture design. The evaluation experiments are conducted on the ISCX-VPN dataset. For simplicity, we list the ratio between α and $\beta$ in Table VII. Our empirical experiments reveal that the choice of coeficient value has a significant influence on the accuracy and computational overhead. With $\alpha : \beta$ ranging from 3:1 to 0.5:1, the overall computational cost is reduced from 63.9 MFLOPs to 241.8 kFLOPs, while the accuracy is decreased by 0.74%. Although a smaller α brings a certain influence to the accuracy, its overall reduction in cost is still worth it. As listed in Table VII, the resultant architecture searched with $( \alpha = 0 . 5 , \beta = 1 )$ reduces 97.2% model size and 99.6% redundant computation with an acceptable accuracy loss; therefore, we utilize such configurations in determining the architecture of UTFormer. It is also observed that the bytekeeping rate $\gamma$ decreases from 42% to 5%, demonstrating that the diferential architecture search efectively integrates the dynamic payload distillation method, enabling the automated parameter adjustment. The above experiments reveal the parametric sensitivity of the proposed loss function, users can strategically tune $( \alpha , \beta )$ to adjust the accuracy-cost tradeof based on deployment requirements.

## B. Deep Dive on Dynamic Payload Distillation

1) Ablation Experiments on Rand-k and SVD-k: To rigorously assess the eficiency of dynamic payload distillation based on Top-k strategy, we perform comprehensive comparisons to (1) random distillation that follows a naive random-k strategy (Rand-k), and (2) singular value decomposition based distillation (SVD-k), which performs SVD operations on the feature matrix X and selects informative tokens based on the sorting results of Σ matrix, as shown in Equation 12. Based on the diagonal matrix Σ, the SVD-k strategy selects k tokens with the largest singular value. We evaluate all methods on four trafic classification datasets—ISCX, USTC-TFC-app (USTC), CP-iOS (iOS), and CP-Android (Android)—progressively reducing the byte-keeping rate from 90% to 10%.

![](images/7d37d0e10c65662ef484586326dc8a0977e9bc917553d44683adb3a7df50afe8.jpg)  
(a) MTT integrated with dynamic payload distillation.

![](images/ec811e633886f83ae6a576fdb82c9993b811c42166fc702dd0f84317169c0246.jpg)  
(b) PcapEncoder integrated with dynamic payload distillation.  
Fig. 9. Integrating dynamic payload distillation into other transformer-based and LLM-based trafic analysis models.

$$
X = U \Sigma V ^ {T}\tag{12}
$$

The results in Figure 8 demonstrate that the Rand-k achieves inference performance comparable to the proposed Top-k method at higher keeping rates. However, as the keeping rate decreases, Rand-k sufers severe accuracy degradation due to uninformed and random token selection. In contrast, SVD-k attains high accuracy on par with dynamic payload distillation based on Top-k, confirming that selecting tokens associated with dominant singular values efectively preserves discriminative information. Nevertheless, SVD-k incurs substantial computational overhead from performing SVD on the feature matrix, consuming significant compute resources and ofsetting the benefits of token reduction. By contrast, our dynamic payload distillation utilizes the attention matrix, which is already computed as part of the self-attention mechanism in Transformers. The method only adds to Transformers with a Top-k sorting. The method introduces only a lightweight Top-k sorting operation. Given that typical trafic classification inputs contain fewer than 500 tokens [19], [25], this additional overhead is negligible during inference. To conclude, the Top-kbased dynamic payload distillation efectively preserves accuracy while improving the inference performance, achieving a favorable trade-of between accuracy and computational cost.

2) Dynamic Payload Distillation as a Drop-in Technology for Transformer-Based Trafic Analysis: To validate the potential of dynamic payload distillation as a drop-in lightweighting method for Transformer trafic analysis models, we integrate it as a plug-in module into the first layer of both MTT and the LLM-based PcapEncoder. Resulting models are trained on the CP-iOS dataset, and validated on our online test bed. Figure 9a demonstrates the compatibility of dynamic payload distillation with Transformer-based MTT models. At a 20% byte-keeping rate, it improves end-to-end throughput from 80 Mbps to 224 Mbps by 2 8× at the cost of 1.05% accuracy loss. When integrated into the LLM-based PcapEncoder, the presented approach yields a 4 42× end-toend throughput improvement, with an accuracy degradation of less than 1.5% in Figure 9b. By selectively retaining only the most informative tokens, dynamic payload distillation preserves model accuracy while delivering significant acceleration across diverse Transformer-based trafic analysis models.

![](images/57d4ae27a14580cd1b0db81bc3ef5e0b060898666b2b0f1c8b669ee520ba194a.jpg)  
(a) Comparing dynamic payload distillation to structured pruning on MTT model.

![](images/01d6e9afa30d9282c6e35d8656ab0afc800d621fd5409e80a87b66f0b36155dc.jpg)  
(b) Comparing dynamic payload distillation to structured pruning on ET-Bert model.  
Fig. 10. Comparing dynamic payload distillation to structured pruning on transformer-based baselines.

3) Comparison to Structured Pruning: Although dynamic payload distillation can be seen as an orthometric optimization method relative to general NN light-weighting methods, we still compare the performance of the proposed method against structured pruning [40], [41], [42]. Structured pruning is a GPU-friendly method utilized to reduce model size and computational cost by pruning redundant self-attention heads, FFN channels, or other Transformer components without introducing sparse computation. We reproduce the structured pruning method from [42], progressively removing unimportant self-attention heads within ET-Bert and MTT, followed by fine-tuning both models on the CP-iOS dataset. For example, MTT contains five self-attention heads; we remove these structures and their corresponding parameter channels one at a time, thereby gradually reducing model size and computational cost. Simultaneously, we progressively adjust the byte-keeping rate of dynamic payload distillation to enable a fair comparison with structured pruning. The comparison results in Figure 10 demonstrate that when only a few Transformer attention heads are pruned, both methods achieve comparable accuracy and inference performance. However, as more parameters are reduced, structured pruning endures a significant accuracy drop due to the loss of information carried by the pruned attention heads. In contrast, dynamic payload distillation maintains better accuracy and inference performance, proving its efectiveness as a light-weighting method for Transformerbased trafic analysis.

4) Revealing the Most Important Bytes: Via the dynamic payload distillation method, we try to identify where the most important bytes are in a packet. As detailed in Section V-B, we split the raw bytes into 90 tokens with 16 bytes in each. The dynamic payload distillation method utilizes the attention matrix to choose the most informative tokens (bytes). Therefore, we visualize the confidence value as heat maps from the first row of the attention matrix in Figure 11. The visualization reveals two distinct regions of significance: a primary critical segment spanning tokens 1-6 (bytes 1-96) and a secondary hot spot at tailed tokens, for example, around bytes 800 and bytes 960 in the ISCX-VPN dataset in Figure 11a. The importance of bytes 1-96 aligns with fundamental protocol structures where header fields typically contain transport-layer specifications and application-layer identifiers that are crucial for trafic classification. The secondary hot spot emerges from empirical observations: 12.7% of packets in ISCX-VPN datasets end with 800-960 bytes. With some application-layer protocols (e.g., HTTP and SMTP) appending session identifiers in final payload segments, such a tail segment is significant for trafic classification. Similar phenomena exist in CP-android and CP-iOS datasets as well, as shown in Figure 11b and Figure 11c. Conversely, dynamic payload distillation consistently neglects mid-packet tokens, which typically contain user payloads or generic application data. By focusing computational resources on the identified critical regions, our distillation method achieves substantial computational reduction while maintaining classification accuracy.

![](images/32c93539e0737face970d5e8192ff690253985e2e21aec0ec6ae73af0fa28083.jpg)  
(c) The heatmap of Cross-platform-iOS dataset.  
Fig. 11. The heatmap of raw trafic in datasets. Underlying numbers indicate the location of 0-1500 bytes in a packet.

## VIII. DISCUSSION

## A. UTFormer Lightweight Architecture

The performance of UTFormer makes us wonder why UTFormer can be lightweight and high-accuracy. We conclude three reasons as follows:

(i) Dynamic payload distillation removes noise bytes. As illustrated in Section VII-B, the distillation keeps the content near the packet header and packet tail, removing left input tokens. Most removed bytes are user data, which contribute little to the final classification and can be seen as noise. Dynamic payload distillation removes these noises and only keeps the most informative bytes, resulting in reduced computational cost and high accuracy.

(ii) We set no important constraint on the diferential architecture search process, yielding the ultra-lightweight UTFormer configuration. Although contemporary Transformer adaptations for trafic classification (MTT [25], ET-Bert [19]) simply inherit the multi-layer paradigms from NLP/CV domains, we fundamentally re-examined architectural prerequisites by mandating only a single attention head and layer as minimal building blocks, exploring the conventional assumptions about depth requirements.

(iii) The problem space of trafic classification is smaller than that in CV and NLP, thus an ultra-lightweight Transformer model can achieve high accuracy. The input of packet-based trafic classification tasks is usually 1500 raw bytes. However, the input data of Transformers can be a 4K high-resolution image, up to dozens of millions of bytes in CV tasks. On the other hand, the output of trafic classification is to classify hundreds of trafic categories, while in large language models, the output space of Transformer models is to generate context content for humans. The problem space of trafic classification suggests that a lightweight Transformer architecture may be suficient for high performance.

## B. Adapting to Open-World Scenarios

Trafic classification tasks in open-world scenarios could be complex, particularly when trafic and its source application are unseen during training. Currently, numerous works have investigated how to address open-world trafic classification, e.g., leveraging contrastive learning [10], unsupervised learning [15], or open-set method [7] to automatically recognize and label unknown trafic. We want to emphasize that the lightweight technology of UTFormer is orthogonal to the above methods. Therefore, UTFormer can be seamlessly integrated with these technologies to adapt to open-world trafic classification scenarios.

## IX. RELATED WORK

## A. DL-Based Trafic Classification Models

DL-based trafic classification models can be categorized into feature-based and raw-byte-based depending on the input:

Feature-based DL models. Feature-based NN models [43], [44] rely on statistical trafic features as input. Features such as packet arrival intervals, etc., reflect the high-level state of the trafic. However, as revealed by previous research and comparison in our evaluation, feature-based DL models are inferior to raw-byte-based models in accuracy performance.

Raw-byte-based DL models. Raw-byte-based methods [45], [46] feed the models with the raw packet, utilizing important information about the protocol and data distribution carried in the packet, leading to the SOTA accuracy [17], [45], [46]. The trafic classification community has seen the development from lightweight MLP [47] to more complex RNN [5], [48] and CNN models [21], [49]. Recently, Transformer [17], [18], [19] and Mamba [38], [46] models have been introduced in trafic classification. In this paper, we mainly select CNNs and Transformers as the baseline models for their complexity and high accuracy performance.

## B. Lightweight Method of Neural Network

There exist several lightweight technologies for deep neural networks (DNNs), like quantization [50], [51] and NN pruning [52], [53]. Neural network (NN) quantization reduces the numerical precision of weights and activations to compress models and accelerate inference, while NN pruning removes redundant parameters to compress models while preserving accuracy via iterative retraining. We claim that quantization and pruning are orthogonal to the diferential architecture search and dynamic payload distillation in UTFormer.

## X. CONCLUSION

UTFormer is an ultra-lightweight trafic classification model that integrates dynamic payload distillation and diferential architecture search, achieving 87.79-99.99% accuracy while reducing computational costs by 9.0-36398 5× and model sizes by 44.9-5433 9× compared to state-of-the-art Transformers. UTFormer eliminates up to 95% of input redundancy with a minimum 106 KB model. Under real-world deployment environments, UTFormer yields 10 Gbps line-rate throughput with a real-time latency of less than 0.2 milliseconds. This work proves that ultra-lightweight UTFormer can rival deep architectures in accuracy while enabling practical improvement in inference throughput performance, paving the way for eficient trafic classification on resource-constrained environments.

## REFERENCES

[1] C. Zheng et al., “IIsy: Hybrid in-network classification using programmable switches,” IEEE/ACM Trans. Netw., vol. 32, no. 3, pp. 2555–2570, Jun. 2024.

[2] C. Busse-Grawitz, R. Meier, A. Dietmuller, T. B ¨ uhler, and L. Van-¨ bever, “PForest: In-network inference with random forests,” 2019, arXiv:1909.05680.

[3] G. Xie et al., “Empowering in-network classification in programmable switches by binary decision tree and knowledge distillation,” IEEE/ACM Trans. Netw., vol. 32, no. 1, pp. 382–395, Feb. 2024.

[4] L. Yang, S. Fu, Y. Wang, L. Liu, and Y. Luo, “The analysis of encrypted video stream based on low-dimensional embedding method,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 8280–8295, 2025, doi: 10.1109/TIFS.2024.3515816.

[5] K. Kim, J.-H. Lee, H.-K. Lim, S. Oh, and Y.-H. Han, “Deep RNNbased network trafic classification scheme in edge computing system,” Comput. Sci. Inf. Syst., vol. 19, no. 1, pp. 165–184, 2022.

[6] J. Yan et al., “Brain-on-switch: Towards advanced intelligent network data plane via nn-driven trafic analysis at line-speed,” in Proc. 21st USENIX Symp. Networked Syst. Design Implement. (NSDI), 2024, pp. 419–440.

[7] X. Wang, Y. Wang, Y. Lai, Z. Hao, and A. X. Liu, “Reliable openset network trafic classification,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 2313–2328, 2025.

[8] G. Aceto, D. Ciuonzo, A. Montieri, and A. Pescape, “Mobile encrypted trafic classification using deep learning: Experimental evaluation, lessons learned, and challenges,” IEEE Trans. Netw. Service Manage., vol. 16, no. 2, pp. 445–458, Jun. 2019.

[9] S. Zhao, S. Chen, Y. Sun, Z. Cai, and J. Su, “Identifying known and unknown mobile application trafic using a multilevel classifier,” Secur. Commun. Netw., vol. 2019, pp. 1–11, Jan. 2019.

[10] C. Wu, J. Sun, J. Chen, M. Alazab, Y. Liu, and Y. Xiang, “TCG-IDS: Robust network intrusion detection via temporal contrastive graph learning,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 1475–1486, 2025.

[11] J. Ghadermazi, S. Hore, A. Shah, and N. D. Bastian, “GTAE-IDS: Graph transformer-based autoencoder framework for real-time network intrusion detection,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 4026–4041, 2025, doi: 10.1109/TIFS.2025.3557741.

[12] T. Shapira and Y. Shavitt, “FlowPic: A generic representation for encrypted trafic classification and applications identification,” IEEE Trans. Netw. Service Manage., vol. 18, no. 2, pp. 1218–1232, Jun. 2021.

[13] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pretraining of deep bidirectional transformers for language understanding,” in Proc. Conf. North Amer. Chapter Assoc. Comput. Linguistics, 2019, pp. 4171–4186.

[14] A. Vaswani et al., “Attention is all you need,” in Proc. Adv. Neural Inf. Process. Syst., vol. 30, 2017, pp. 5998–6008.

[15] L. Yang et al., “UnFlowS: An unsupervised construction scheme of flow spectrum for network trafic detection,” IEEE Trans. Inf. Forensics Security, vol. 20, pp. 3330–3345, 2025.

[16] R. Zhao, X. Deng, Z. Yan, J. Ma, Z. Xue, and Y. Wang, “MT-FlowFormer: A semi-supervised flow transformer for encrypted trafic classification,” in Proc. 28th ACM SIGKDD Conf. Knowl. Discov. Data Min., 2022, pp. 2576–2584.

[17] G. Zhou, X. Guo, Z. Liu, T. Li, Q. Li, and K. Xu, “TraficFormer: An eficient pre-trained model for trafic data,” in Proc. IEEE Symp. Secur. Privacy (SP), May 2025, pp. 1844–1860.

[18] H. Y. He, Z. Guo Yang, and X. N. Chen, “PERT: Payload encoding representation from transformer for encrypted trafic classification,” in Proc. ITU Kaleidoscope: Industry-Driven Digit. Transformation (ITU K), Dec. 2020, pp. 1–8.

[19] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification,” Proc. ACM Web Conf., pp. 633–642, 2022.

[20] D. Wen, T. Li, C. Li, P. Xia, H. Yang, and Z. Sun, “Octopus: A heterogeneous in-network computing accelerator enabling deep learning for network,” 2023, arXiv:2308.11312.

[21] M. Gallo, A. Finamore, G. Simon, and D. Rossi, “FENXI: Deep-learning trafic analytics at the edge,” in Proc. IEEE/ACM Symp. Edge Comput. (SEC), Dec. 2021, pp. 202–213.

[22] W. Wang and L. David. USTC-TFC Dataset. Accessed: May 6, 2019. [Online]. Available: https://github.com/yungshenglu/USTC-TFC2016

[23] H. Lim, J. Kim, J. Heo, K. Kim, Y. Hong, and Y. Han, “Packetbased network trafic classification using deep learning,” in Proc. Int. Conf. Artif. Intell. Inf. Commun. (ICAIIC), Okinawa, Japan, Feb. 2019, pp. 46–51.

[24] W. Wang, M. Zhu, J. Wang, X. Zeng, and Z. Yang, “End-to-end encrypted trafic classification with one-dimensional convolution neural networks,” in Proc. IEEE Int. Conf. Intell. Secur. Informat. (ISI), Jul. 2017, pp. 43–48.

[25] W. Zheng, J. Zhong, Q. Zhang, and G. Zhao, “MTT: An eficient model for encrypted network trafic classification using multi-task transformer,” Appl. Intell., vol. 52, no. 9, pp. 10741–10756, Jul. 2022.

[26] X. He, K. Zhao, and X. Chu, “AutoML: A survey of the state-of-the-art,” Knowl.-Based Syst., vol. 212, pp. 106622–106643, Jan. 2021.

[27] B. Zoph and Q. V. Le, “Neural architecture search with reinforcement learning,” 2016, arXiv:1611.01578.

[28] A. Dosovitskiy et al., “An image is worth 16 × 16 words: Transformers for image recognition at scale,” 2020, arXiv:2010.11929.

[29] Z. Liu et al., “Swin transformer: Hierarchical vision transformer using shifted windows,” in Proc. IEEE/CVF Int. Conf. Comput. Vis. (ICCV), Oct. 2021, pp. 10012–10022.

[30] H. Touvron, M. Cord, M. Douze, F. Massa, A. Sablayrolles, and H. Jegou, “Training data-e´ ficient image transformers & distillation through attention,” in Proc. Int. Conf. Mach. Learn., 2021, pp. 10347–10357.

[31] S. U. Jafri, S. Rao, V. Shrivastav, and M. Tawarmalani, “Leo: Online ML-based trafic classification at multi-terabit line rate,” in Proc. 21st USENIX Symp. Networked Syst. Design Implement. (NSDI), 2024, pp. 1573–1591.

[32] Z. Xiong and N. Zilberman, “Do switches dream of machine learning? Toward in-network classification,” in Proc. 18th ACM Workshop Hot Topics Netw., Nov. 2019, pp. 25–33.

[33] K. Wang, J. Gao, and X. Lei, “MTC: A multi-task model for encrypted network trafic classification based on transformer and 1D-CNN,” Intell. Autom. Soft Comput., vol. 37, no. 1, pp. 619–631, 2023.

[34] ISCX-VPN Dataset. Accessed: Apr. 28, 2016. [Online]. Available: https://www.unb.ca/cic/datasets/vpn.html

[35] T. van Ede et al., “FlowPrint: Semi-supervised mobile-app fingerprinting on encrypted network trafic,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2020, pp. 1–18.

[36] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur. (CCS), Toronto, ON, Canada, Oct. 2018, pp. 1928–1943.

[37] Y. Zhao, G. Dettori, M. Bofa, L. Vassio, and M. Mellia, “The sweet danger of sugar: Debunking representation learning for encrypted trafic classification,” in Proc. ACM SIGCOMM Conf., Sep. 2025, pp. 296–310.

[38] T. Wang et al., “NetMamba+: A framework of pre-trained models for eficient and accurate network trafic classification,” 2026, arXiv:2601.21792.

[39] C. Rafel, N. Shazeer, A. Roberts, K. Lee, S. Narang, and M. Matena, “Exploring the limits of transfer learning with a unified text-to-text transformer,” J. Mach. Learn. Res., vol. 21, no. 140, pp. 1–67, 2020.

[40] J. Mao, H. Yang, A. Li, H. Li, and Y. Chen, “TPrune: Eficient transformer pruning for mobile devices,” ACM Trans. Cyber-Physical Syst., vol. 5, no. 3, pp. 1–22, Jul. 2021.

[41] A. Zayed, G. Mordido, S. Shabanian, I. Baldini, and S. Chandar, “Fairness-aware structured pruning in transformers,” in Proc. AAAI Conf. Artif. Intell., vol. 38, no. 20, 2024, pp. 22484–22492.

[42] G. Fang, X. Ma, and M. Song, “Depgraph: Towards any structural pruning,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit., Jun. 2023, pp. 16091–16101.

[43] M. Dener, S. Al, and G. Ok, “RFSE-GRU: Data balanced classification model for mobile encrypted trafic in big data environment,” IEEE Access, vol. 11, pp. 21831–21847, 2023.

[44] P. P. Kundu, T. Truong-Huu, L. Chen, L. Zhou, and S. G. Teo, “Detection and classification of botnet trafic using deep learning with model explanation,” IEEE Trans. Depend. Secure Comput., early access, Jun. 15, 2022, doi: 10.1109/TDSC.2022.3183361.

[45] R. Zhao et al., “Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation,” in Proc. AAAI Conf. Artif. Intell., vol. 37, no. 4, 2023, pp. 5420–5427.

[46] T. Wang, X. Xie, W. Wang, C. Wang, Y. Zhao, and Y. Cui, “Netmamba: Eficient network trafic classification via pre-training unidirectional mamba,” in Proc. IEEE 32nd Int. Conf. Netw. Protocols (ICNP), Oct. 2024, pp. 1–11.

[47] T. A. Tang, L. Mhamdi, D. McLernon, S. A. R. Zaidi, and M. Ghogho, “Deep learning approach for network intrusion detection in software defined networking,” in Proc. Int. Conf. Wireless Netw. Mobile Commun. (WINCOM), Oct. 2016, pp. 258–263.

[48] M. Lopez-Martin, B. Carro, A. Sanchez-Esguevillas, and J. Lloret, “Network trafic classifier with convolutional and recurrent neural networks for Internet of Things,” IEEE Access, vol. 5, pp. 18042–18050, 2017.

[49] Q. Liao, T. Li, and W. Zhang, “An online network trafic classification method based on deep learning,” in Proc. IEEE 2nd Int. Conf. Electron. Inf. Commun. Technol. (ICEICT), Jan. 2019, pp. 34–39.

[50] S. I. Young, W. Zhe, D. Taubman, and B. Girod, “Transform quantization for CNN compression,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 44, no. 9, pp. 5700–5714, Sep. 2022.

[51] J. Lin, J. Tang, H. Tang, S. Yang, G. Xiao, and S. Han, “AWQ: Activation-aware weight quantization for on-device LLM compression and acceleration,” GetMobile, Mobile Comput. Commun., vol. 28, no. 4, pp. 12–17, Jan. 2025.

[52] M. Lin et al., “1×N pattern for pruning convolutional neural networks,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 45, no. 4, pp. 3999–4008, Apr. 2023.

[53] Z. Wang, C. Li, and X. Wang, “Convolutional neural network pruning with structural redundancy reduction,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2021, pp. 14913–14922.

![](images/4f03f9ef4e9a85c59834ae5764da6d2f08989e6d746625e3635903c959f49eb5.jpg)  
Dong Wen received the bachelor’s degree in computer science from Northeastern University in 2019 and the master’s degree in computer science from the National University of Defense Technology in 2022, where he is currently pursuing the Ph.D. degree under the supervision of Prof. Tao Li and Prof. Zhigang Sun. His research interests include AI-for-networking, computer architecture, and edge computing.

![](images/d8d2cbe6ae674586a0fbeddcd09be72e8c67498e08535e82b5293fddfdeef5a3.jpg)

Tianyun Li received the Bachelor of Science degree from the College of Software Engineering, Dalian University of Technology, Dalian, Liaoning. She is currently pursuing the master’s degree with the College of Computer Science, National University of Defense Technology, Changsha, Hunan. Her main research interests include high performance networks, data center networks, RDMA congestion control, and artificial intelligence.

![](images/7634aa440f3eec93160036f75827bad2bcde2b4cc94203b66fe3a391813bc589.jpg)

Zhuochen Fan (Member, IEEE) received the Ph.D. degree in computer science from Peking University in 2023, advised by Prof. Tong Yang. He is currently an Associate Researcher with the Peng Cheng Laboratory. He has published papers in IEEE/ACM TRANSACTIONS ON NETWORK-ING, IEEE TRANSACTIONS ON KNOWLEDGE AND DATA ENGINEERING, The VLDB Journal, ICDE, RTSS, ICPP, and ICNP. His research interests include approximation algorithms in security, computer networks, and databases.

![](images/2bb4569ceaa02382fbeede1e8348b5ffd723d18a2b434b043f690cb9c8b84dbc.jpg)

Qing Li (Senior Member, IEEE) received the B.S. degree in computer science and technology from Dalian University of Technology, Dalian, China, in 2008, and the Ph.D. degree in computer science and technology from Tsinghua University, Beijing, China, in 2013. He is currently a Full Professor with the Peng Cheng Laboratory, Shenzhen, China. His research interests include reliable and scalable routing of the internet, software defined networking, network function virtualization, in-network caching/computing, and edge computing.

Jie Li was born in 1992. He is currently pursuing the degree with the National University of Defense Technology. His main research interests include traffic classification and deep learning.

![](images/77e44a607d476605dab33cf3d602602a564ec951abdb92f94dac79201a655b6d.jpg)

Fa Zhu (Member, IEEE) received the Ph.D. degree in control science and engineering from the School of Computer Science and Engineering, Nanjing University of Science and Technology, Nanjing, China, in 2019. From 2016 to 2018, he was a Visiting Student with the Center for Artificial Intelligence (CAI) and the Faculty of Engineering and Information Technology, University of Technology Sydney, Australia. He is currently an Associate Professor with the College of Information Science and Technology and the College of Artificial Intelligence, Nanjing

![](images/ccf8d7f45ae0638f0b72a13e0ad71453c00fb9b0ba69a3a21dd4206c5293c56c.jpg)

![](images/75094846dd7a026fb716456bb7f0a3cddc029f6bef0e4fe2000676cf6591d680.jpg)

Forestry University, Nanjing. His current research interests include artificial intelligence, pattern recognition, machine learning, and the Internet of Things. Most of his researches have published on high prestigious journals, such as IEEE TRANSACTIONS ON NEURAL NETWORKS AND LEARNING SYSTEMS, IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, IEEE TRANSACTIONS ON SERVICES COMPUTING, IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, IEEE TRANSACTIONS ON VEHICULAR TECHNOLOGY, IEEE IV Magazine, IEEE TRANSACTIONS ON CONSUMER ELECTRONICS, IEEE INTERNET OF THINGS JOURNAL, and IEEE JOURNAL OF BIOMEDICAL AND HEALTH INFORMATICS. He serves/served as an associated editor or a guest editor for several journals.

![](images/f23a9d4b1915589d120d0963d92ad7882fb4eb0ca5f5d00ffec4b00c787dc334.jpg)

Chenglong Li was born in 1995. He received the Ph.D. degree. He is currently a Research Associate with the Defense Innovation Institute, Academy of Military Sciences, Beijing. His main research interests include time-sensitive networking, in-network computing, and RISC-V.

Athanasios V. Vasilakos (Senior Member, IEEE) is currently with the College of Mathematics and Computer Science, Fuzhou University, Fuzhou, China; and the Center for AI Research, University of Agder, Grimstad, Norway. His main research interests include green networks, sensor nets, the IoTs/mobile nets, smart cities, cloud computing, artificial intelligence/machine learning, block chain technologies, cybersecurity, and big data analytics. He is a member of the technical program committee of several conferences. He received the Best Paper Award

at the IEEE ICCCN 2014 International Workshop on Hot Topics in Big Data and Networking (HotData I), ACM Mobiquitous 2013, and the Fifth International Conference on Bio-Inspired Models of Network, Information and Computing Systems (ACM BIONETICS 2010). He is chairing (as the General Chair) and organizing several international conferences, including the IEEE ICDCS 2012 First Workshop on Forensics, Security and Privacy; ACM BodyNets 2010; the 2011 IEEE INFOCOM 2011 First Workshop on Cloud Computing; and the IEEE SECON 2016 First Workshop on CoWPER (Toward a City-Wide Pervasive Environment). He served or is serving as an Editor for many technical journals, such as IEEE TRANSACTIONS ON NETWORK AND SERVICE MANAGEMENT, IEEE TRANSACTIONS ON CLOUD COMPUTING, IEEE TRANSACTIONS ON INFORMATION FORENSICS AND SECURITY, IEEE TRANSACTIONS ON CYBERNETICS, IEEE TRANS-ACTIONS ON NANOBIOSCIENCE, IEEE TRANSACTIONS ON INFORMATION TECHNOLOGY IN BIOMEDICINE, ACM Transactions on Autonomous and Adaptive Systems, and IEEE JOURNAL ON SELECTED AREAS IN COMMU-NICATIONS.

![](images/4629f9904d261c574a08426c9f2d0a8eacb003289e5ec0256fef3f38d6a4da23.jpg)

Tao Li is currently an Associate Professor with the College of Computer, National University of Defense Technology. He has been in charge of the development of five specialized network chips. His research interests include high-performance network chips and systems. His research achievements have been awarded with one Second Prize of the National Science and Technology Progress, three First Prizes at the provincial and ministerial level for Science and Technology Progress, and one Third Prize for Science and Technology Progress.
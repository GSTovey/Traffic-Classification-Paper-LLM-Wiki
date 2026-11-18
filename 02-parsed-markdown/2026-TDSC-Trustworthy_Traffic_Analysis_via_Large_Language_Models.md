# Trustworthy Traffic Analysis via Large Language Models

Yan Qiao, Member, IEEE, Junjie Wang, Shuangshuang Ding, Fenglin Yan, Kaiwen Jiang, Zhenchun Wei<sup>∗</sup>, Member, IEEE, Kun Xie<sup>∗</sup>, Member, IEEE

Abstract—The Traffic Matrix (TM) is vital for network management; however, its decentralized circulation faces strict regulatory and data sovereignty constraints, restricting raw data sharing and causing massive data missingness. Existing learningbased TM recovery methods lack trustworthiness: they either adopt a single-stage generation paradigm that lacks generalization ability, or suffer from cross-scale parameter interference and ignore multi-scale features. To build a secure and compliant data circulation infrastructure, we propose MPA-LLM, a trustworthy traffic analysis and reconstruction framework based on a Multi-Parameterized Autoregressive Large Language Model. Inspired by the coarse-to-fine human cognitive process, MPA-LLM deploys LLMs to incrementally refine the TM through a step-wise autoregressive mechanism. It also employs a decoupled resolution reconstruction framework to eliminate parameter interference, rendering TM recovery highly transparent, auditable, and reliable for multi-party collaboration. Furthermore, a dynamic ondemand mechanism maintains a unified multi-task framework and simultaneously supports high-precision TM imputation, forecasting, and anomaly detection tasks. Extensive experiments show that MPA-LLM significantly outperforms state-of-the-art methods on multiple TM analysis tasks. Furthermore, it maintains strong performance whether given only limited TM knowledge (e.g., 5%–10% TM snapshots) or no prior knowledge at all on unseen networks. The reproducible experimental code is available at https://github.com/Labman-Wangjunjie/MPA-LLM.

Index Terms—Trustworthy data circulation, traffic analysis, traffic matrix imputation, large language models, autoregressive learning.

## I. INTRODUCTION

RAFFIC Matrix (TM) captures traffic volume between source-destination pairs over a given time interval. It is indispensable for many networking tasks such as anomaly detection [1], traffic engineering [2], and capacity planning [3]. To obtain the TMs, operators employ measurement tools such as NetFlow [4] or sFlow [5] on network devices to record the traffic volumes traversing them. However, in largescale cross-institutional environments, data sharing faces a profound privacy and trust crisis: driven by regulatory compliance and data sovereignty, distributed nodes are reluctant to share complete raw traffic data. Consequently, collected data suffer from extensive omissions or corruption, often exceeding a 90% missing rate. Thus, the TM missing problem is an inevitable outcome of privacy-preserving data sharing in untrustworthy environments. Enabling privacy-preserving computation among untrustworthy entities for secure data governance, while accurately recovering the missing TM data, has therefore become a paramount challenge for downstream network optimization.

To address these challenges, existing research over the past few decades has extensively explored network TM analysis methods. Specifically, conventional approaches often formulate this as a matrix or tensor completion problem [6] to infer missing traffic volumes by exploiting spatial-temporal low-rank properties. Alternatively, network tomography-based methods [7] [8] estimate the complete TM from link loads collected via SNMP. However, the aforementioned methods face several critical limitations in practical deployments: (1) High uncertainty in one-step paradigms. Most existing models adopt a one-step inference or reconstruction paradigm. Under extreme data missing scenarios (e.g., over 90% missingness), the lack of progressive supervision causes the models to struggle with effective convergence, resulting in highly uncertain and fluctuating outputs. (2) Limited model generalizability. Existing models are strongly coupled with specific network topologies. Any evolution in the network topology necessitates high-cost data recollection, architecture redesign, and model retraining from scratch. (3) Restricted to a single task. Existing models are designed solely for imputation and cannot meet the diverse requirements of various network management tasks across different scenarios. This forces network operators to maintain multiple independent, highly specialized models for different objectives, leading to severe system fragmentation.

Our previous work ARI-LLM [9] took an initial step toward addressing above issues. To overcome the high uncertainty of one-step paradigms under extreme sparsity, it conceptualized TM analysis as a coarse-to-fine autoregressive generation process. This multi-step strategy mimics human cognitive reasoning, progressively refining predictions, significantly enhancing the stability of the imputation process, and helping LLMs better comprehend TM analysis tasks. Furthermore, to tackle issues of rigid topology dependency, ARI-LLM introduced a flow-aware tokenization scheme that supports scalable and topology-adaptive embeddings. Through the above design, the model demonstrated strong few-shot and zero-shot learning capabilities, enabling seamless transfer to unseen or dynamically evolving network environments without retraining. However, ARI-LLM still suffers from two major limitations: First, it relies on a single shared LLM architecture across all recovery stages. This reliance causes severe parameter interference among different resolution scales, which renders the recovery process opaque and non-auditable. Second, by being restricted to a single imputation task, it forces operators to maintain fragmented, single-purpose models, breaking the continuity of end-to-end secure data governance and hindering privacypreserving data circulation across multi-party domains [10].

This paper extends previous work to overcome these bottlenecks by proposing a new framework named MPA-LLM (Multi-Parameterized Autoregressive Large Language Model). The core optimizations of this extended work lie in two dimensions: expanding to a unified multi-task paradigm, and upgrading from a single-LLM design to a multi-parameterized decoupled architecture. Specifically, MPA-LLM pioneers a stage-decoupled architecture that deploys multiple independent LLM modules. Each module acts as a dedicated stage expert, exclusively responsible for capturing and isolating the specific reconstruction parameters of a designated resolution interval. This multi-parameterized mechanism offers the following advantages. First, it completely eliminates cross-scale parameter interference, transforming data recovery into a ”white-box” process. This ensures that every step of data processing is traceable and auditable, providing the essential robustness required for secure decentralized data circulation. Second, by extracting stage-specific traffic representations, MPA-LLM transcends traditional single-task boundaries. Driven by a dynamic on-demand invocation mechanism, it establishes a unified framework to support multiple TM tasks: imputation, forecasting, and anomaly detection. Experimental results demonstrate that MPA-LLM achieves state-of-the-art performance across multiple network management tasks without incurring a significant computational burden.

In summary, this work makes the following contributions to the field of trustworthy network traffic analysis:

(1) Building upon our previous work ARI-LLM, which introduced a coarse-to-fine autoregressive generation paradigm, we propose MPA-LLM, a trustworthy TM analysis infrastructure that further extends autoregressive learning to multi-task traffic analysis. Specifically, MPA-LLM introduces a stage-decoupled architecture that deploys independent LLMs for different resolution stages, thereby eliminating the parameter entanglement across resolution levels in ARI-LLM. This multi-parameterized design improves the trustworthiness, traceability, and auditability of TM analysis in decentralized data circulation scenarios.

(2) We achieve a unified multi-task representation with a dynamic on-demand invocation mechanism. While maintaining low computational and memory overhead, MPA-LLM utilizes a flow-aware tokenization scheme to extract pure stage-specific features. This seamlessly supports TM imputation, traffic forecasting, and anomaly detection, while exhibiting strong zero-shot generalization capabilities on unseen networks.

(3) We conduct comprehensive empirical evaluations using three real-world TM datasets. The experimental results demonstrate that MPA-LLM maintains outstanding performance. Even under extreme missing rates of over 90%, it substantially outperforms state-of-the-art methods across all three evaluation metrics: imputation error, forecasting accuracy, and anomaly detection F1 score.

The remainder of this paper is organized as follows. Section II reviews related work on TM analysis. Section III formulates the TM analysis problem and presents the proposed MPA-LLM framework. Section IV reports extensive experimental results on three real-world datasets to evaluate the effectiveness of MPA-LLM. Section V discusses the limitations of the proposed approach. Finally, Section VI concludes this paper.

## II. RELATED WORK

In this section, we review existing works on TM analysis from three perspectives: traditional approaches, deep learningbased methods, and the emerging LLM-based methods.

## A. Traditional TM Analysis Methods

Traditional TM analysis methods can be broadly categorized into three paradigms. Network Tomography (NT)-based methods estimate fine-grained origin–destination (OD) flows from aggregated link loads by introducing statistical assumptions such as Poisson models [7], Bayesian inference [11], or gravity models [12] to address the underdetermined inverse problem. These methods are primarily applied to OD flow estimation [13] and anomaly detection [14]. Matrix/tensor decomposition-based methods exploit the low-rank property of TMs to recover missing entries via compressive sensing [15], maximum entropy [16], or neural tensor completion [17]. They are widely used for imputation [18], prediction [19], and anomaly detection [20]. Statistical models, such as ARIMA/SARIMA [21], capture temporal dependencies in each OD flow for short-term forecasting [22] and outlier detection [23]. Despite their interpretability, these traditional methods struggle to handle non-linear traffic patterns [24], high-dimensional OD flows [25], and cross-flow correlations [26], motivating the deep learning-based approaches.

## B. Deep Learning-Based TM Analysis

To better capture complex spatiotemporal correlations, recent studies have adopted deep-learning models for TM analysis, which can be categorized into four categories based on their core architectures. Generative Adversarial Networks (GANs) are widely used for imputation: DATC [27] recovers missing tensor-structured TMs via adversarial training. Diffusion models offer superior distribution fidelity: Diffusion-TM [28] leverages progressive denoising for robust recovery under high missing rates. Graph Neural Networks (GNNs) dominate forecasting tasks: DG-STMTL [29] uses dynamic grouping GCNs for multi-scale prediction. RNNs and Transformers focus on temporal dynamics: ConvLSTMTransNet [30] integrates CNNs, LSTMs, and Transformers for forecasting, while Transformer-based autoencoders [31] are applied to anomaly detection. Other representative works include NTC [17], PetTC [32], and flow-based generative tomography [2] for TM imputation and estimation, as well as CATCH [33] and GCAD [34] for anomaly detection. Despite these advances, deep learning methods still face critical limitations in generalizing to dynamic network topologies and handling multiple tasks without parameter interference.

## C. LLM-Based Analysis Approaches

Inspired by the remarkable success of LLMs, recent research has begun exploring LLMs for networking-related tasks. NetLLM [35] provides a coherent framework for adapting LLMs to diverse networking problems, including viewport prediction, adaptive bitrate streaming, and cluster job scheduling. TrafficLLM [36] introduces a dual-stage finetuning framework that learns generic traffic representations from heterogeneous raw data, enabling both traffic classification and packet generation. ALM [37] provides a twostage traffic anomaly detection and attack classification system that leverages LLMs’ few-shot learning ability, achieving over 90% F1 score on four public datasets. MET-LLM [38] targets malicious encrypted traffic detection by integrating domainspecific tokenization with a dynamic adaptive tuning adaptor. Most recently, ARI-LLM [9] established the first LLM-based TM imputation model, adopting a coarse-to-fine autoregressive strategy that achieves strong zero-shot and few-shot generalization across diverse network environments. However, ARI-LLM relies on a single set of model weights tailored to a single task. When extended to multi-task scenarios, this monolithic design introduces parameter interference that renders inference opaque and non-auditable, thereby undermining trustworthy recovery and hindering secure data circulation across domains.

In contrast, the proposed MPA-LLM introduces a decoupled multi-parameterized architecture with independent LLM modules for different resolution stages, thereby enabling trustworthy TM analysis across multi-task scenarios.

## III. METHODOLOGY

In this section, we present our multi-parameterized autoregressive model, termed MPA-LLM, which leverages LLMs to perform generalizable imputation, prediction, and anomaly detection tasks with severely missing TMs. All symbols used in the main text are summarized in Table I.

## A. Problem Formulation

We consider a backbone network $G ( V , E )$ with |V| end nodes and |E| directed links. Let $X _ { t } = \{ x _ { t , 1 } , x _ { t , 2 } , . . . , x _ { t , N } \}$ denote the traffic volumes between all source-destination node pairs at the t-th time point, where $N = | V | \times | V |$ . For ease of computation, we construct the TM as a $T \times N$ matrix $\textbf { X } = \ \{ X _ { 1 } , X _ { 2 } , \ldots , X _ { T } \} ^ { \top }$ , representing all traffic volumes measured over $T$ time points. We introduce a binary indicator matrix $\mathbf { M } \in \{ 0 , 1 \} ^ { T \times \bar { N } }$ to distinguish observed and missing values in X, where if $x _ { t , i }$ is observed, the corresponding entry $m _ { t , i } = 1$ , and otherwise $m _ { t , i } = 0$ . Meanwhile, we define the partially observed TM as $\tilde { \mathbf { X } } = \mathbf { M } \odot \mathbf { X }$ , where $\odot$ denotes the Hadamard product.

This paper aims to address three fundamental network traffic analysis tasks: TM imputation, traffic forecasting and anomaly detection. For TM imputation, the objective is to reconstruct the complete matrix X by estimating unobserved entries where $m _ { t , i } = 0$ . For traffic forecasting, we aim to predict future traffic volumes $\mathbf { X } _ { T _ { u } + 1 : T _ { u } + U }$ based on a few historical observations $\mathbf { X } _ { 1 : T _ { u } }$ , where $T _ { u }$ is the length of the current observation window, and $U$ denotes the number of future time steps to be predicted. Finally, for network anomaly detection, we identify abnormalities using the absolute deviation anomaly score matrix defined as $\textbf { A } = ~ | \widehat { \textbf { X } } - \textbf { X } |$ , where $\widehat { \mathbf X }$ is the imputed TM. Entries in A exceeding a dynamically calibrated threshold τ are subsequently flagged as anomalous, where τ is determined according to the target anomaly ratio on the anomaly score distribution.

LIST OF SYMBOLS USED IN THIS PAPER  
TABLE I

<table><tr><td>Symbol</td><td>Description</td></tr><tr><td> $G(V,E)$ </td><td>Backbone network</td></tr><tr><td> $V$ </td><td>Set of end nodes</td></tr><tr><td> $E$ </td><td>Set of directed links</td></tr><tr><td> $N$ </td><td>Total number of node pairs</td></tr><tr><td> $T$ </td><td>Total number of all time steps</td></tr><tr><td> $w$ </td><td>Number of time steps in a TM sample</td></tr><tr><td> $X_{t}$ </td><td>TM at time point  $t$ </td></tr><tr><td> $\mathbf{X}$ </td><td>Ground-truth TM over all time points</td></tr><tr><td> $\mathbf{M},m_{t,i}$ </td><td>Observation indicator matrix/entry</td></tr><tr><td> $\widetilde{\mathbf{X}}$ </td><td>Partially observed TM</td></tr><tr><td> $\widehat{\mathbf{X}}$ </td><td>Imputed TM estimate</td></tr><tr><td> $\mathbf{A}$ </td><td>Anomaly score matrix</td></tr><tr><td> $h$ </td><td>Total number of observation stages</td></tr><tr><td> $\mathbf{X}^{(s)}$ </td><td>TM state at stage  $s$ </td></tr><tr><td> $\widehat{\mathbf{X}}^{(s)}$ </td><td>Predicted TM for stage  $s$ </td></tr><tr><td> $\mathcal{I}^{(s)}$ </td><td>Observed indices at stage  $s$ </td></tr><tr><td> $q$ </td><td>Initial sampling density</td></tr><tr><td> $K$ </td><td>Base observation count</td></tr><tr><td> $T_{u}$ </td><td>Historical window length</td></tr><tr><td> $U$ </td><td>Prediction horizon</td></tr><tr><td> $r,r_{\text{est}}$ </td><td>True/estimated TM rank</td></tr><tr><td> $n$ </td><td>Number of sampled flows</td></tr><tr><td> $n^{*}$ </td><td>Optimal input flow count</td></tr><tr><td> $d$ </td><td>LLM hidden dimension</td></tr><tr><td> $P$ </td><td>Prompt sequence length</td></tr><tr><td> $\mathbf{E}_{\text{TM}}^{(s)}$ </td><td>TM embedding in stage  $s$ </td></tr><tr><td> $\mathbf{E}_{\text{prompt}}^{(s)}$ </td><td>Prompt embedding in stage  $s$ </td></tr><tr><td> $\mathbf{E}_{\text{in}}^{(s)}$ </td><td>Combined embedding in stage  $s$ </td></tr><tr><td> $L,l$ </td><td>Total/current Transformer layer</td></tr><tr><td> $\mathbf{H}^{(l,s)}$ </td><td>Hidden state at layer  $l$ , stage  $s$ </td></tr><tr><td> $\mathbf{X}_{\text{out}}^{(s)}$ </td><td>Traffic-related latent state</td></tr><tr><td> $\boldsymbol{\Theta}$ </td><td>Learnable parameters in MPA-LLM</td></tr><tr><td> $\boldsymbol{\Theta}^{(s)}$ </td><td>Learnable parameters for model  $F^{(s)}$ </td></tr><tr><td> $\mathcal{L}_{\text{SMAPE}}^{(s)}$ </td><td>SMAPE loss for stage  $s$ </td></tr><tr><td> $\eta$ </td><td>Learning rate</td></tr><tr><td> $\epsilon$ </td><td>Small constant for stability</td></tr></table>

## B. Model Architecture

The overall framework of our proposed MPA-LLM is illustrated in Fig. 1. To effectively learn the traffic pattern of TMs, MPA-LLM performs progressive feature extraction and state reconstruction. For a given TM X, we decompose its state into a sequence of intermediate representations at varying resolutions, denoted as $\mathcal { X } = \{ \mathbf { X } ^ { ( 1 ) } , \mathbf { \bar { X } } ^ { ( 2 ) } , \dots , \mathbf { X } ^ { ( s ) } , \dots , \mathbf { \bar { X } } ^ { ( h ) } \}$ where h represents the number of distinct observation stages with increasing sampling rates. At the s-th evolutionary stage, the framework processes the current resolution $\mathbf { X } ^ { ( s ) }$ to infer the refined state $\mathbf { X } ^ { ( s + 1 ) }$ , systematically reducing uncertainty until the final high-fidelity matrix $\widetilde { \mathbf { X } }$ is generated. As illustrated in Fig. 1, this coarse-to-fine process progressively increases the observation resolution $( \mathrm { e . g . , 2 \% \to 4 \% \to 8 \% \to }$ $\cdot \cdot \cdot  1 0 0 \% )$ , with each resolution transition handled by an independent stage-specific LLM.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/87b177025ec2c7ce7e0f8aebfb850397f9fbf30dcfc1b8aebdd5cc7dc0896223.jpg)  
Fig. 1. The MPA-LLM framework. Traffic data are processed through a sequence of varying resolutions in a coarse-to-fine manner. The Multi-Head Attention layers and Text Embedder of the pre-trained LLM are kept frozen to preserve general language modeling capabilities, while the Flow2Vec Embedder, normalization layers, feed-forward layers, and the shared MLP projection head are fine-tuned to align latent representations with diverse downstream tasks.

In each step, the input $\mathbf { X } ^ { ( s ) }$ is processed by our Flow2Vec Embedder, which uses an internal LSTM to map the raw flows into a high-dimensional token space. Simultaneously, a Text Embedder translates task instructions and statistical meta-data into contextual tokens. These two embeddings are concatenated and fed into the core LLM. To bridge the modality gap and reduce computational cost, we keep the Multi-Head Attention layers and the Text Embedder strictly frozen. Only the Flow2Vec Embedder, Normalization layers, and Feed Forward networks are fine-tuned. Finally, the contextually enriched hidden states pass through a shared Multi-Layer Perceptron (MLP) projection head, yielding the output TM.

In the following, we elaborate on the key components of the framework, including the autoregressive learning mechanism, the Flow2Vec Embedder, including the Autoregressive Learning Mechanism, the Flow2Vec Embedder, the Prompt Template, the LLM Body, the Multi-Task Adaptation Mechanism, and the Lightweight Fine-Tuning strategy.

## C. Autoregressive Learning Mechanism

A fundamental limitation of existing sequence-to-sequence imputation models is the capacity bottleneck encountered when attempting to map highly sparse inputs directly to dense outputs within a single, unified parameter space. The mathematical distribution of data manifolds varies drastically across different sparsity levels, making it exceedingly difficult for a single set of weights to generalize across the entire reconstruction trajectory. To overcome this limitation, MPA-LLM introduces a novel multi-parameterized stage-decoupled mechanism. Instead of relying on a single recurrent architecture, we deploy an ensemble of h distinct, sequentially ordered LLM bodies, where $h = 6$ is an empirical design choice. It corresponds to the minimum number of geometric doubling steps required to expand the observation ratio from 2% to 100% $( 2 \%  4 \%  8 \%  1 6 \%  3 2 \%  6 4 \%$ → 100%), which provides a practical balance between stage granularity and computational overhead (see sec. IV-I). Each model specializes in a specific density transition, mapping the observation at stage s to a denser representation at stage s+1.

To formalize this coarse-to-fine trajectory, we systematically construct a sequence of observation index sets, denoted as $\mathcal { T } = \{ \mathcal { Z } ^ { ( 0 ) } , \mathcal { T } ^ { ( \bar { 1 } ) } , \ldots , \mathcal { T } ^ { ( h ) } \}$ , where $\mathcal { T } ^ { ( s ) } ~ ( s = \{ 0 , 1 , \ldots , h \} )$ defines the precise time indices observed at the s-th evolutionary step. Consider a TM with a total length of w time steps: $\mathbf { X } = \{ X _ { 1 } , X _ { 2 } , \ldots , X _ { w } \} ^ { \top }$ , we define an initial sampling density parameter $q \in ( 0 , 1 ]$ and let $K = \lfloor q w \rfloor$ be the base number of observed time points. The progressive doubling of the observation resolution at each stage is mathematically

formulated as:

$$
\mathcal {I} ^ {(s)} = \left\{ \begin{array}{l l} \{1, w \}, & s = 0, \\ \mathcal {I} ^ {(0)} \cup \left\{\left\lfloor \frac {i w}{K} \right\rfloor   \bigg |   i = 1, \ldots , K \right\}, & s = 1, \\ \mathcal {I} ^ {(s - 1)} \cup \left\{\left\lfloor \frac {t _ {i} + t _ {i + 1}}{2} \right\rfloor   \bigg |   t _ {i}, t _ {i + 1} \in \mathcal {I} ^ {(s - 1)} \right\}, & s > 1. \end{array} \right.\tag{1}
$$

This deterministic sampling scheme exponentially expands the observation set, naturally forming a target density progression from extensive sparsity to complete observability. The corresponding matrix at stage s, denoted as $\mathbf { X } ^ { ( s ) }$ , is constructed by masking the full matrix according to $\boldsymbol { \mathcal { T } ^ { ( s ) } }$ , where the unobserved values are simply filled by linear interpolation between the two nearest observed neighbors.

At each decoupled step $s \in \{ 0 , 1 , \ldots , h - 1 \}$ , a stagespecific model $\bar { F } ^ { ( s ) }$ with independent parameters $\Theta ^ { ( s ) }$ is invoked. The model processes the current state $\mathbf { X } ^ { ( s ) }$ combined with stage-specific contextual prompts, outputting the refined prediction $\hat { \mathbf { X } } ^ { ( s + 1 ) }$ targeted for the next predefined density level:

$$
\widehat {\mathbf {X}} ^ {(s + 1)} = F ^ {(s)} (\mathbf {X} ^ {(s)}; \Theta^ {(s)})\tag{2}
$$

By decoupling the parameters $\Theta ^ { ( s ) }$ across stages, each model acts as an isolated expert optimized for a specific missing-rate distribution.

During the optimization phase, we enforce rigorous stepwise supervision. Considering the significant magnitude variations inherent in network traffic, we adopt the Symmetric Mean Absolute Percentage Error (SMAPE) to rigorously penalize the discrepancy between the stage-wise prediction and the ground-truth target. The loss function for the $( s + 1 )$ -th stage is defined as:

$$
\mathcal {L} _ {\mathrm{SMAPE}} ^ {(s + 1)} = \frac {1}{w} \sum_ {i = 1} ^ {w} \frac {| | \widehat {X} _ {i} ^ {(s + 1)} - X _ {i} ^ {(s + 1)} | | _ {1}}{(| | \widehat {X} _ {i} ^ {(s + 1)} | | _ {1} + | | X _ {i} ^ {(s + 1)} | | _ {1}) / 2 + \epsilon}\tag{3}
$$

where $| | \cdot | | _ { 1 }$ denotes the L1-Norm computed over the feature dimension, and ϵ is a remarkably small constant introduced to prevent numerical instability. The loss $\mathcal { L } _ { \mathrm { S M A P E } } ^ { ( s + 1 ) }$ is independently back-propagated to fine-tune the parameters $\Theta ^ { ( s ) }$ of the model $F ^ { ( s ) }$

## D. Flow2Vec Embedder

Existing model adaptations for TM analysis typically treat the full set of observational features at each discrete time step as a single, indivisible unit. This flattened representation imposes strict architectural rigidity. It inherently ties the input layer to a fixed feature dimension. Whenever network topologies fluctuate dynamically, structural modifications and retraining become necessary. To accommodate such dynamic environments, we design the Flow2Vec embedding module. Instead of temporal slicing, Flow2Vec treats each individual traffic flow as an independent tokenizable unit. For any flow defined over a temporal window of length w, the initial $w \times 1$ numerical vector is mapped by a temporal feature extractor into a d-dimensional latent token, perfectly aligning with the intrinsic word embedding dimensionality of the pre-trained language model.

By mapping each flow to a high-dimensional token, the model processes the TM analogously to a natural language sentence composed of a variable number of words. Interflow spatial correlations are efficiently captured through inherent self-attention mechanisms, ensuring absolute structural consistency regardless of the total input flow count. Operationally, at the s-th progressive stage, the current-resolution TM $\mathbf { X } ^ { ( s ) } \in \mathbb { R } ^ { w \times n }$ (comprising n sampled flows) is transposed to prioritize the flow dimension. An LSTM-based temporal encoder subsequently distills intra-flow temporal dependencies, projecting the data into the flow-level token embedding space $\mathbf { E } _ { \mathrm { T M } } ^ { ( s ) } \in \mathbb { R } ^ { n \times d }$ . Here, the LSTM is an internal component of the Flow2Vec Embedder and is used to capture temporal dependencies within each individual traffic flow. These dense embeddings are finally ingested by the frozen LLM body to orchestrate spatial correlation learning via multi-head selfattention.

While expanding the number of input flows enables the attention mechanism to construct a richer spatial correlation graph, indiscriminately increasing the sequence length induces severe computational bottlenecks and potential performance degradation. We formalize this trade-off by establishing a theoretical optimum for the input flow count.

Theorem 1 (Optimal Number of Input Flows for LLMs). Assume a TM $\textbf { X } \in \mathbb { R } ^ { w \times n }$ has rank r, where n is the total number of flows and w is the time length. Consider a Transformer-based LLM architecture, where each flow is embedded as a token vector and fed into the model. Then, the optimal number of input flows $n ^ { * }$ to the LLM that maximizes the downstream analytical performance is $n ^ { * } = r .$

Proof. This theoretical bound emerges from analyzing the fundamental balance between informational completeness and model complexity capacity.

Given that the spatiotemporal manifold of X is spanned by an r-dimensional subspace, sampling fewer than r flows $( n <$ r) yields an incomplete basis representation. This inevitably results in a mathematically underdetermined system and biased latent representations. Consequently, as the input flow count n increases up to $r ,$ the theoretical inference error $\mathcal { E } _ { r e c } ( n )$ decreases strictly monotonically:

$$
\frac {d \mathcal {E} _ {r e c} (n)}{d n} <   0, \quad \text { for } n \leq r.\tag{4}
$$

Conversely, when $n \ > \ r .$ , additional flows introduce redundant, linearly dependent vectors that fail to expand the informational subspace. Although intrinsic information content reaches saturation at r flows, increasing n further precipitates severe computational overhead, as the time and space complexity of the self-attention mechanism scales quadratically with the token sequence length $\mathcal { O } ( n ^ { 2 } d )$ . Furthermore, an excessive influx of redundant tokens aggressively expands the functional hypothesis space, raising the model’s variance and rendering attention maps highly susceptible to localized noise under limited training data regimes. Therefore, the accumulation of noise and redundancy causes the expected prediction error to ascend:

$$
\frac {d \mathcal {E} _ {r e c} (n)}{d n} > 0, \quad \text { for } n > r.\tag{5}
$$

Synthesizing these continuous dynamics reveals that $\mathcal { E } _ { r e c } ( n )$ strictly forms a unimodal convex function with respect to $n ,$ achieving its global minimum at exactly n = r.

The optimal number of tokens is thus inextricably linked to the degree of spatiotemporal correlation inherent in the network, where a highly correlated network traffic yields a lower rank r and requires fewer tokenized flows per forward pass.

Remark 1. Under idealized theoretical conditions, each input batch dispatched to the model should perfectly encapsulate r orthogonal flows. In real-world deployments, however, the precise rank r remains latent and obscured by extreme data sparsity, making perfectly independent flow identification computationally intractable. To operationalize this theoretical optimum, our framework groups the total N flows into $\lceil N / r _ { e s t } \rceil$ sequential batches based on an empirically estimated rank $r _ { e s t } ,$ extensively mitigating computational overhead while preserving robust multi-task reconstruction capabilities.

## E. Prompt Template

LLMs are fundamentally pre-trained on vast corpora of natural language, developing profound capabilities in sequential reasoning, pattern recognition, and zero-shot generalization. However, raw numerical TMs lack the explicit semantic context inherently expected by these auto-regressive architectures. To bridge this cross-modal gap and fully unleash the pre-trained cognitive prowess of LLMs for specialized network analytical tasks, MPA-LLM incorporates a rigorously structured Prompt Template. This text-based prefix acts as a semantic anchor, guiding the LLM to properly contextualize the numerical flow variations processed by the Flow2Vec module.

As illustrated in Fig. 2, the Prompt Template consists of a macro-level Head section and a micro-level Load section. The Head section formulates the Database background, specifying global dataset fundamentals such as network topology, spatial scale, and the historic sampling methodology. The Load section drives the progressive inference engine through four dynamic components: (i) Domain outlines the spatialtemporal tensor boundaries and sequence length configuration; (ii) Instruction details the unified multi-task analytical objectives, directing the model toward imputation, forecasting, and anomaly detection; (iii) Stage acts as a conditional indicator that specifies the current data density (e.g., 2% observed data) and dictates the targeted refinement resolution (e.g., moving toward 4%) for the multi-parameterized mechanism; and (iv) Statistics injects real-time empirical meta-data—including minimum, maximum, and median values—computed directly from the input batch to effectively ground the numerical scale.

Mathematically, for a given TM observation at stage s, the dynamically constructed prompt text is mapped via the

LLM’s native integrated Text Embedder into a dense semantic space. This operation yields a prompt embedding denoted as $\dot { \mathbf { E } } _ { \mathrm { p r o m p t } } ^ { ( s ) } \in \mathbb { R } ^ { \hat { P } \times d }$ , where $P$ represents the sequence length of the prompt tokens and d signifies the hidden dimensionality of the language model backbone.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/0a4695b5758b269a14520c821d0379d655f67636b2dad181114f2e16e3e06ef2.jpg)  
Fig. 2. An illustrative example of the prompt template utilized in MPA-LLM. The tags in brackets (e.g., [Database], [Instruction]) indicate the start of a specific contextual block, while dynamic data statistics and stagespecific configurations are injected iteratively at each step of the decoupled mechanism.

## F. LLM Body

In MPA-LLM, each discrete evolutionary stage s is governed by an independent LLM instance. To form a cohesive representation capable of joint spatiotemporal and semantic reasoning, the text-based prompt embedding $\mathbf { E } _ { \mathrm { p r o m p t } } ^ { ( s ) } \in \mathbb { R } ^ { P \times d }$ (generated by the Text Embedder) and the flow-level traffic embedding $\mathbf { E } _ { \mathrm { T M } } ^ { ( s ) } \in \mathbb { R } ^ { n \times d }$ (comprising n input flows within the current batch generated by the Flow2Vec Embedder) should be projected into a unified coordinate space.

Specifically, we concatenate the two embeddings along the token hidden dimension of the pre-trained language model. The combined input representation $\mathbf { E } _ { \mathrm { i n } } ^ { ( s ) }$ fed into the core of the s-th LLM is formalized as:

$$
\mathbf {E} _ {\mathrm{in}} ^ {(s)} = \left[ \mathbf {E} _ {\mathrm{prompt}} ^ {(s)}; \mathbf {E} _ {\mathrm{TM}} ^ {(s)} \right] \in \mathbb {R} ^ {(P + n) \times d}\tag{6}
$$

where both embeddings share an identical token hidden dimension d. This integrated input matrix is sequentially propagated through L cascaded Transformer layers inherent to the LLM architecture. Each Transformer layer executes deep self-attention to capture the intricate spatial correlations among distinct network flows. For any given Transformer layer $l \in \{ 1 , 2 , \ldots , L \}$ at stage $s ,$ the dual-residual non-linear transformations are mathematically defined as:

$$
\widetilde {\mathbf {H}} ^ {(l, s)} = \operatorname{Norm} \left(\mathbf {H} ^ {(l - 1, s)} + \operatorname{Att} \left(\mathbf {H} ^ {(l - 1, s)}\right)\right),\tag{7}
$$

$$
\mathbf {H} ^ {(l, s)} = \operatorname{Norm} \left(\widetilde {\mathbf {H}} ^ {(l, s)} + \operatorname{FF} \left(\widetilde {\mathbf {H}} ^ {(l, s)}\right)\right)\tag{8}
$$

where $\mathrm { A t t } ( \cdot )$ , Norm(·), and $\mathrm { F F } ( \cdot )$ symbolize the standard Multi-Head Attention module, Layer Normalization, and the Position-Wise Feed-Forward network, respectively. The initial hidden state is mapped as ${ \bf H } ^ { ( 0 , s ) } ~ = ~ { \bf \dot { E } } _ { \mathrm { i n } } ^ { ( s ) }$ , and $\mathbf { H } ^ { ( l , s ) } ~ \in$ $\mathbb { R } ^ { ( P + n ) \times d }$ denotes the output of the l-th layer.

After traversing all L hidden layers, the model extracts the final deep representation $\mathbf { H } ^ { ( L , \bar { s } ) }$ . To completely isolate the model’s predictions for the physical TM and discard the text-based auxiliary context, we actively truncate the prefix segment corresponding to the first $P$ prompt tokens. The remaining n rows form the pure traffic-related output latent state:

$$
\mathbf {X} _ {\mathrm{out}} ^ {(s)} = \mathbf {H} ^ {(L, s)} [ P + 1: P + n ] \in \mathbb {R} ^ {n \times d}\tag{9}
$$

Finally, this deeply contextualized traffic representation $\mathbf { X } _ { \mathrm { o u t } } ^ { ( s ) }$ is fed into the shared projection head. Modeled as an MLP, this head decodes the latent tokens back into the numerical TM space targeted for the next step:

$$
\widehat {\mathbf {X}} ^ {(s + 1)} = \operatorname{MLP} \left(\mathbf {X} _ {\text { out }} ^ {(s)}\right)\tag{10}
$$

## G. Multi-Task Adaptation Mechanism

To support multiple traffic analysis tasks within a unified framework, MPA-LLM employs a multi-task adaptation layer implemented by the MLP projection head introduced in Section III.F. This task-agnostic projection head maps the traffic-related latent representation produced by each stagespecific LLM back to the numerical TM space, without introducing separate task-specific decoder architectures. Task differentiation is instead achieved through the corresponding task instructions, input construction, training targets, and taskspecific inference procedures.

For TM imputation, the full sequence of the decoupled mechanism is executed to estimate the unobserved TM entries $\widehat { \mathbf { X } } _ { \mathrm { i m } }$ from the randomly observed traffic Xe . For traffic forecasting, the future prediction window $\mathbf { X } _ { T _ { u } + 1 : T _ { u } + U }$ is conceptualized as an artificially masked region, allowing the model to iteratively extrapolate future traffic volumes $\widetilde { \mathbf { X } } _ { \mathrm { f } }$ based on the causal temporal dependencies captured from the historical unmasked context. For anomaly detection, the framework computes an absolute residual matrix $\mathbf { A } = | \widehat { \mathbf { X } } - \mathbf { X } |$ between the reconstructed TM Xb and the actual observed values $\mathbf { X } .$ Data entries in A exceeding a dynamically calibrated threshold are subsequently flagged as anomalies.

It is important to clarify that the unified architecture does not imply joint end-to-end training of the three tasks. Imputation and forecasting are trained separately because they involve different input constructions and supervision targets: imputation learns to recover missing entries, whereas forecasting learns to estimate future traffic windows from historical observations. Anomaly detection does not require an additional training stage; instead, it directly reuses the reconstruction model and identifies anomalies through residual-based post-processing with the dynamically calibrated threshold. Thus, MPA-LLM shares a common adaptation architecture across tasks while preserving task-specific training and inference procedures.

## H. Lightweight Fine-Tuning

We utilize a lightweight fine-tuning strategy to adapt the multi-parameterized framework for the imputation task without discarding the pre-trained knowledge of the LLM backbones. In particular, the Multi-Head Attention layers across all stage-specific models are kept frozen to protect their acquired representations. We deliberately update just four essential modules per stage: the Flow2Vec parameters $( \Theta _ { \mathrm { f 2 v } } ^ { ( s ) } )$ for tokenizing the TM data, the Normalization parameters $( \Theta _ { \mathrm { n o r m } } ^ { ( s ) } )$ for ensuring stable feature scaling, the Feed Forward parameters $( \Theta _ { \mathrm { f f } } ^ { ( s ) } )$ for enabling non-linear transformations, and the MLP parameters $( \Theta _ { \mathrm { m l p } } ^ { ( s ) } )$ responsible for projecting the latent states back into the TM space. Crucially, these trainable parameters are strictly isolated across different resolution stages, completely eradicating cross-scale parameter interference.

The comprehensive fine-tuning procedure is outlined in Alg. 1. The algorithm takes the training TMs X, a starting observation ratio q, and a learning rate η as inputs. Ultimately, it yields an ensemble of optimized parameter sets $\boldsymbol { \Theta } \ : = \ :$ $\{ \Theta _ { \mathrm { l l m } } ^ { \overline { { ( s ) } } } \} _ { s = 0 } ^ { h - 1 }$ , where each independent stage expert parameter set is explicitly defined as $\Theta _ { \mathrm { l l m } } ^ { ( \bar { s } ) } = \{ \Theta _ { \mathrm { f 2 v } } ^ { ( s ) } , \mathbf { \bar { \Theta } } _ { \mathrm { { n o r m } } } ^ { ( s ) } , \Theta _ { \mathrm { f f } } ^ { ( \bar { s } ) } , \Theta _ { \mathrm { m l p } } ^ { ( s ) } \}$

The process begins by initializing the observation indices alongside the ensemble model parameters (line 1). Subsequently, it determines the baseline observation count K and the overall resolution levels h (lines 2∼3), initiating the multi-parameterized autoregressive learning procedure over h sequential transitions (lines 4∼14). During the s-th transition step, the algorithm establishes the observed indices $\boldsymbol { \mathcal { T } ^ { ( s ) } }$ and $\mathcal { T } ^ { ( s + 1 ) }$ utilizing Eqn. (1) (line 5). Following this, linear interpolation is performed on the available traffic flow data to construct the TMs for both the current $( \mathbf { X } ^ { ( s ) } \in \mathbb { R } ^ { w \times n } )$ and subsequent $( \mathbf { X } ^ { ( s + 1 ) } )$ resolutions (line 6). The current matrix $\mathbf { X } ^ { ( \bar { s } ) }$ is then transposed and processed through the stage-specific Flow2Vec to produce the flow-level embedding $\mathbf { E } _ { \mathrm { T M } } ^ { ( s ) }$ (line 7). Simultaneously, the Text Embedder encodes the prompt associated with $\mathbf { X } ^ { ( s ) }$ , yielding the prompt embedding $\mathbf { E } _ { \mathrm { p r o m p t } } ^ { ( s ) }$ (line 8). These two representations are concatenated into a unified embedding $\mathbf { E } ^ { ( s ) }$ , serving as the input for the s-th LLM (line 9). Once processed, the output from the final hidden layer, represented as $\mathbf { X } _ { \mathrm { o u t } } ^ { ( s ) }$ , is extracted (line 10). To isolate the TM-specific output, the initial $P$ prompt tokens are truncated (line 11). This isolated output is subsequently fed into the stage-specific MLP to generate the final prediction $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ (line 12). The discrepancy between this imputed matrix $\widehat { \mathbf { X } } ^ { ( s + 1 ) }$ and the actual ground truth $\mathbf { X } ^ { ( s + 1 ) }$ is calculated using the SMAPE metric (line 13). Upon completion of all stage transitions, the algorithm backpropagates the loss $\mathcal { L } ^ { ( s + 1 ) }$ (line 15) and updates all isolated parameters via gradient descent (line 16). Importantly, during the last iteration, the resulting $\widehat { \mathbf { X } } ^ { ( h ) }$ represents the entirely reconstructed TM Xb , whereas $\mathbf { X } ^ { ( h ) }$ equates to the original ground-truth TM X. At this stage, the corresponding index set $\mathcal { T } ^ { ( h ) } = \{ 1 , 2 , . . . , w \}$ encompasses the complete sequence of time points.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Fine-Tuning Algorithm of MPA-LLM
Require:  $X = \{X_{1}, X_{2}, \ldots, X_{w}\}^{\top}$ , q,  $\eta$ 
Ensure: Ensemble of trained parameters  $\Theta = \{\Theta_{\mathrm{llm}}^{(s)}\}_{s=0}^{h-1}$ 
with  $\Theta_{\mathrm{llm}}^{(s)} = \{\Theta_{\mathrm{f2v}}^{(s)}, \Theta_{\mathrm{norm}}^{(s)}, \Theta_{\mathrm{ff}}^{(s)}, \Theta_{\mathrm{mlp}}^{(s)}\}$ 

1: Initialize:  $\Theta$ ,  $\mathcal{I}^{(0)} \leftarrow \{1, w\}$ ;

2:  $K = \lfloor qw \rfloor$ ;

3:  $h = \lceil \log_{2}(w/K) \rceil$ ;

4: for s = 0 to h - 1 do

5: Compute  $\mathcal{I}^{(s)}$  and  $\mathcal{I}^{(s+1)}$  by Eqn. (1);

6:  $\mathbf{X}^{(s)} \leftarrow \text{LinearInterp}(\{X_{i} \in \mathbf{X} \mid i \in \mathcal{I}^{(s)}\})$ ,

 $\mathbf{X}^{(s+1)} \leftarrow \text{LinearInterp}(\{X_{i} \in \mathbf{X} \mid i \in \mathcal{I}^{(s+1)}\})$ ;

7:  $\mathbf{E}_{\mathrm{TM}}^{(s)} \leftarrow \text{Flow2Vec}((\mathbf{X}^{(s)})^{\top}, \Theta_{\mathrm{f2v}}^{(s)})$ ;

8:  $\mathbf{E}_{\text{prompt}}^{(s)} \leftarrow \text{TextEmbedder}(\text{Prompt}(\mathbf{X}^{(s)}))$ ;

9:  $\mathbf{E}^{(s)} \leftarrow [\mathbf{E}_{\text{prompt}}^{(s)}; \mathbf{E}_{\mathrm{TM}}^{(s)}]$ ;

10:  $\mathbf{X}_{\text{out}}^{(s)} \leftarrow \text{LLM}(\mathbf{E}^{(s)}; \Theta_{\text{norm}}^{(s)}, \Theta_{\text{ff}}^{(s)})$ ;

11:  $\mathbf{X}_{\text{TM}}^{\text{out}(s)} \leftarrow \mathbf{X}_{\text{out}}^{(s)}[P + 1 : P + n]$ ;

12:  $\widehat{\mathbf{X}}^{(s+1)} \leftarrow \text{MLP}(\mathbf{X}_{\text{TM}}^{\text{out}(s)}; \Theta_{\text{mlp}}^{(s)})$ ;

13:  $\mathcal{L}^{(s+1)} \leftarrow \text{SMAPE}(\widehat{\mathbf{X}}^{(s+1)}, \mathbf{X}^{(s+1)})$ ;

14:  $\nabla_{\Theta} L^{(s+1)} \leftarrow \text{Backpropagation}(\mathcal{L}^{(s+1)})$ ;

15:  $\Theta \leftarrow \Theta - \eta\nabla_{\Theta} L^{(s+1)}$ 

16: end for

17: return  $\Theta$
</div>

## IV. EXPERIMENTS

## A. Experimental Setup

1) Datasets: We use three real-world datasets from different network environments. The Abilene dataset [12], contains OD flows’ measurements between 12 network nodes, recorded every 5 minutes over a period of 168 days. The GEANT<sup>´</sup> dataset [39], contains the flows between 23 nodes, taken every 15 minutes for 112 consecutive days. The WS-DREAM dataset [40] focuses on throughput measurements between 4,500 web services and 142 users, collected at 15-minute intervals during 64 continuous time slots. We split each dataset into training, validation, and testing sets in an 8:1:1 ratio.

2) Evaluation Metrics: For imputation and forecasting, we employ three metrics: Normalized Mean Absolute Error (NMAE), Normalized Root Mean Square Error (NRMSE) and Kullback-Leibler Divergence (KL) to evaluate the performance of imputation and forecasting methods. NMAE and NRMSE evaluate the errors of the predicted values compared to the ground truth. KL divergence measures the similarity between the distributions of the predicted and real TM data, where a smaller KL value implies a closer match. Table II presents the definitions for these metrics. Here, $\boldsymbol { x } _ { i j }$ and $\hat { x } _ { i j }$ denote the real and predicted values of the j-th OD flow at time point i in X and Xb , respectively. $\begin{array} { r } { p _ { i j } = \frac { x _ { i j } } { \sum _ { ( i , j ) \in \hat { \Phi } } x _ { i j } } . } \end{array}$ $\begin{array} { r } { \hat { p } _ { i j } = \frac { \hat { x } _ { i j } } { \sum _ { ( i , j ) \in \bar { \Phi } } \hat { x } _ { i j } } } \end{array}$ represent the probability mass function of the real and predicted flows, respectively. Φ denotes index sets of unobserved data. These metrics are computed solely on unobserved data.

For anomaly detection, we adopt the affiliation-based precision (Aff P), recall (Aff R), and F1 score (Aff F1) [41].

TABLE II  
PERFORMANCE METRICS FOR IMPUTATION AND FORECASTING

<table><tr><td>Metric</td><td>Definition</td></tr><tr><td>NMAE</td><td> $\frac{\sum_{(i,j)\in\bar{\Phi}}|x_{ij}-\hat{x}_{ij}|}{\sum_{(i,j)\in\bar{\Phi}}|x_{ij}|}$ </td></tr><tr><td>NRMSE</td><td> $\frac{\sqrt{\sum_{(i,j)\in\bar{\Phi}}(x_{ij}-\hat{x}_{ij})^{2}}}{\sqrt{\sum_{(i,j)\in\bar{\Phi}}x_{ij}^{2}}}$ </td></tr><tr><td>KL</td><td> $\sum_{(i,j)\in\bar{\Phi}}p_{ij}\log\left(\frac{p_{ij}}{\hat{p}_{ij}}\right)$ </td></tr></table>

These metrics overcome the limitations of classical pointbased metrics by evaluating the temporal proximity between predicted anomaly intervals and ground truth events in a locally interpretable, parameter-free manner. Aff P measures the average probability that detected anomaly intervals are temporally close to true anomalous events, Aff R measures the average probability that true anomalous events are covered by detections, and Aff F1 is their harmonic mean. Table III presents the definitions for these metrics. Here, $G _ { j }$ denotes the j-th ground truth anomaly interval, D is the set of all detected anomaly intervals, and $N _ { \mathrm { g t } }$ denotes the number of ground-truth anomaly intervals. The affiliation zone $I _ { j }$ of $G _ { j }$ consists of all time points that are closer to $G _ { j }$ than to any other ground truth event. |·| represents the length (total measure) of an interval or union of intervals. $\boldsymbol { S } = \{ j \ \bar { | \mathcal { D } \cap I _ { j } } \neq \emptyset \}$ is the set of indices of ground truth events that have at least one affiliated prediction. The survival function $\tilde { F } _ { \mathrm { p r e c i s i o n } , j } ( d )$ gives the probability that a uniformly random detected point $; \in \mathcal { D } \cap I _ { j }$ lies at distance at least d from $G _ { j } ,$ i.e., $\tilde { F } _ { \mathrm { p r e c i s i o n } , j } ( d ) = \mathbb { P } ( \mathrm { d i s } \overleftarrow { \mathbf { t } } ( x , G _ { j } ) > d )$ . For recall, $\tilde { F } _ { \mathrm { r e c a l l } , j } ( \bar { d } )$ gives the probability that a uniformly random point $y \in G _ { j }$ lies at distance at least d from the detection set D, i.e., $\tilde { F } _ { \mathrm { r e c a l l } , j } ( d ) = \mathbb { P } ( \mathrm { d i s t } ( y , \mathcal { D } ) > d )$ . Finally, $\operatorname { d i s t } ( \cdot , \cdot )$ denotes the shortest temporal distance between a point and a set.

PERFORMANCE METRICS FOR ANOMALY DETECTION  
TABLE III

<table><tr><td>Metric</td><td>Definition</td></tr><tr><td>Aff_P</td><td> $\frac{1}{|\mathcal{S}|}\sum_{j\in\mathcal{S}}\frac{1}{|\mathcal{D}\cap I_j|}\int_{x\in\mathcal{D}\cap I_j}\tilde{F}_{\text{precision},j}(\text{dist}(x,G_j)) dx$ </td></tr><tr><td>Aff_R</td><td> $\frac{1}{N_{\text{gt}}}\sum_{j=1}^{N_{\text{gt}}}\frac{1}{|G_j|}\int_{y\in G_j}\tilde{F}_{y,\text{recall}}(\text{dist}(y,\mathcal{D}\cap I_j)) dy$ </td></tr><tr><td>Aff_F1</td><td> $2 \cdot \frac{\text{Aff\_P} \cdot \text{Aff\_R}}{\text{Aff\_P} + \text{Aff\_R}}$ </td></tr></table>

3) Baseline Methods: We compare MPA-LLM with representative methods across three tasks: imputation, forecasting, and anomaly detection. For imputation, we include seven methods: deep network embedding methods including CoSTCo [42], NTC [17], NTM [43], and PetTC [32]; temporal network embedding methods including NTF [44] and LTP [45]; and the GAN-based method DATC [27]. Among them, NTC, DATC, LTP, and PetTC are specifically designed for network TM imputation, while NTM, NTF, and CoSTCo are widely applied in recommendation systems. For forecasting, we compare against three state-of-the-art forecasting methods: ICTSP [46], an in-context predictor that leverages LLMs for zero-shot forecasting; LSINet [47], a lightweight spatiotemporal forecasting network; and RTS-PnO [48], a timing-aware and risk-sensitive forecasting framework. For anomaly detection, we evaluate against three state-of-theart methods: CATCH [33], a channel-aware anomaly detection method via frequency patching; DADA [49], a general anomaly detector with adaptive bottlenecks and dual adversarial decoders; and GCAD [34], which detects anomalies from the perspective of Granger causality with graph neural networks.

TABLE IV  
PARAMETERS SETTINGS

<table><tr><td>Parameters</td><td>Settings</td></tr><tr><td>LLM Backbone</td><td>GPT-2</td></tr><tr><td>Number of Layers</td><td>6</td></tr><tr><td>Hidden Size ( $d_{model}$ )</td><td>768</td></tr><tr><td>Attention Heads ( $n_{heads}$ )</td><td>4</td></tr><tr><td>Feed-Forward Size ( $d_{ff}$ )</td><td>768</td></tr><tr><td>Input Sequence Length</td><td>50</td></tr><tr><td>Batch Size</td><td>60/32/20</td></tr><tr><td>Learning Rate</td><td>0.001</td></tr><tr><td>Optimizer</td><td>Adam</td></tr><tr><td>Patience</td><td>5</td></tr></table>

4) Model Settings: The main parameters in our model are listed in Table IV. Our model is built upon GPT-2 architecture with 6 transformer layers, a hidden size of 768, 4 attention heads, and a feed-forward dimension of 768. The window size for each input TM is set to 50. The number of optimal input flows (i,e., the estimated TM rank $r _ { \mathrm { e s t } } )$ is set to 144, 300, and 550 for Abilene, GEANT, and WS-DREAM, respec-<sup>´</sup> tively. According to the intrinsic spatiotemporal correlations of the TMs, the optimal number of input flows is empirically estimated for each dataset based on the theoretical analysis in Section III-D. The selected $r _ { \mathrm { e s t } }$ values are used to determine the number of flows fed into the LLM in each batch. An MLP with one hidden layer is appended to the transformer output for final reconstruction. The model is optimized using the Adam optimizer with a learning rate of 0.001. An early stopping strategy is adopted with a patience of 5. All experiments were conducted on a single NVIDIA GeForce RTX 5090 GPU. All results presented below represent the average of ten runs. Further detailed settings of our experiments are available at https://github.com/Labman-Wangjunjie/MPA-LLM.

## B. TM Imputation Performance

Table V summarizes the performance of the nine TM imputation methods on three datasets under extremely low observation rates (OR) from 2% to 10%. From the table, MPA-LLM achieves the best performance on nearly all metrics, consistently outperforming the other eight comparison methods.

Compared with ARI-LLM, MPA-LLM demonstrates clear improvements on multiple datasets and metrics. On GEANT,<sup>´</sup> MPA-LLM consistently achieves lower NRMSE across all observation ratios, reducing the error by 25.2% to 37.8% relative to ARI-LLM. It also achieves lower NMAE at observation ratios of 6%, 8%, and 10%. On Abilene, MPA-LLM obtains lower NMAE at observation ratios of 4%, 6%, and 10%, as well as lower KL divergence at observation ratios of 4%, 6%, and 10%. These results indicate that the proposed stage-decoupled architecture can further improve reconstruction accuracy over the previous design of ARI-LLM.

Compared to the best-performing baseline PetTC, MPA-LLM improves the NMAE by 12.5% to 19.6% on Abilene, 2.2% to 8.3% on GEANT, and 20.6% to 36.9% on WS-<sup>´</sup> DREAM. For the NRMSE metric, the gains are 3.9% to 18.6% on Abilene, 24.1% to 39.3% on GEANT, and 16.7%<sup>´</sup> to 21.7% on WS-DREAM, respectively. The accuracy gains are especially pronounced on WS-DREAM, which involves high-dimensional traffic data. Across different observation ratios, MPA-LLM averagely reduces the errors of the bestperforming non-ARI-LLM baseline by 15.3%, 16.1%, 16.4%, 15.8%, and 20.7%, under observation rates from 10% to 2%, respectively. The performance gap widens as the observation rate decreases, demonstrating our model’s robustness under sparse imputation scenarios. Regarding KL divergence, MPA-LLM achieves gains of 31.1% to 48.8% on Abilene, 22.7% to 44.7% on GEANT, and 5.4% to 25.7% on WS-DREAM,<sup>´</sup> respectively. This demonstrates MPA-LLM can generate TMs that are significantly closer to the true distribution. These improvements, together with the direct comparison against ARI-LLM, demonstrate the effectiveness of the proposed stage-decoupled multi-parameterized autoregressive design. In particular, the substantial gains on the high-dimensional WS-DREAM dataset demonstrate MPA-LLM’s scalability and robustness, while the strong performance on GEANT validates<sup>´</sup> its ability to handle diverse traffic patterns.

## C. TM Forecasting Performance

Table VI compares the forecasting performance of MPA-LLM against three state-of-the-art forecasting methods, with a forecasting horizon of 96 time steps for all three datasets. As shown in Table VI, MPA-LLM consistently achieves the best performance across all datasets and metrics. On Abilene, MPA-LLM obtains an NMAE of 0.2877, outperforming the best baseline ICTSP by 26.8%. Its NRMSE is 0.3841, while ICTSP achieves 0.5210, corresponding to a 26.3% improvement. For KL divergence, MPA-LLM reaches 0.1551, a substantial reduction from ICTSP’s 1.8100, which represents a 91.4% improvement. On GEANT, MPA-LLM again leads<sup>´</sup> with NMAE 0.2894, NRMSE 0.2130, and KL 0.1538. It improves over ICTSP by 10.8% in NMAE, 22.5% in NRMSE, and 63.8% in KL. On WS-DREAM, the improvement is most striking. MPA-LLM reduces NMAE by 77.7%, NRMSE by 67.7%, and KL by 99.3% compared to the respective best baselines. Such significant gains highlight MPA-LLM’s superior ability to preserve global distributional characteristics of TMs, even in high-dimensional settings. These results demonstrate that the multi-parameterized design of MPA-LLM captures both temporal dynamics and cross-flow correlations more accurately than dedicated forecasting models.

## D. TM Anomaly Detection Performance

We further evaluate MPA-LLM on the task of TM anomaly detection. Following the common practice of anomaly labeling [50], we adopt a dynamic grouping baseline method with a dual-threshold mechanism to generate fine-grained temporal anomaly labels. Specifically, for a given flow, the absolute variation between two consecutive time points is defined as its fluctuation increment. A flow at a given time point is labeled as anomalous if its fluctuation increment simultaneously exceeds 1.5% of the total traffic volume across all flows at that time point (global condition) and, for all links traversed by the flow, exceeds 1% of the maximum link traffic value among those links (local condition). After applying this labeling process, the overall anomaly rates are 25% for the Abilene dataset, 1.5% for the GEANT dataset, and 4.6% for the WS-DREAM<sup>´</sup> dataset.

IMPUTATION PERFORMANCE ON ABILENE, GEANT<sup>´</sup> AND WS-DREAM. BOLD: BEST, UNDERLINED: SECOND BEST  
TABLE V

<table><tr><td colspan="2">Dataset</td><td colspan="5">Abilene</td><td colspan="5">GÉANT</td><td colspan="5">WS-DREAM</td></tr><tr><td>Metric</td><td>Model</td><td>OR 2%</td><td>OR 4%</td><td>OR 6%</td><td>OR 8%</td><td>OR 10%</td><td>OR 2%</td><td>OR 4%</td><td>OR 6%</td><td>OR 8%</td><td>OR 10%</td><td>OR 2%</td><td>OR 4%</td><td>OR 6%</td><td>OR 8%</td><td>OR 10%</td></tr><tr><td rowspan="9">NMAE</td><td>MPA-LLM</td><td>0.1870</td><td>0.1595</td><td>0.1513</td><td>0.1543</td><td>0.1360</td><td>0.2676</td><td>0.2373</td><td>0.2215</td><td>0.2081</td><td>0.1897</td><td>0.2215</td><td>0.2038</td><td>0.1957</td><td>0.1850</td><td>0.1998</td></tr><tr><td>ARI-LLM</td><td>0.1839</td><td>0.1638</td><td>0.1568</td><td>0.1543</td><td>0.1492</td><td>0.2666</td><td>0.2349</td><td>0.2242</td><td>0.2189</td><td>0.2076</td><td>0.2376</td><td>0.1940</td><td>0.1852</td><td>0.1833</td><td>0.1812</td></tr><tr><td>PetTC</td><td>0.2247</td><td>0.1925</td><td>0.1843</td><td>0.1764</td><td>0.1692</td><td>0.2917</td><td>0.2345</td><td>0.2264</td><td>0.2208</td><td>0.2014</td><td>0.3513</td><td>0.2974</td><td>0.2762</td><td>0.2647</td><td>0.2515</td></tr><tr><td>LTP</td><td>0.2585</td><td>0.2293</td><td>0.2257</td><td>0.2144</td><td>0.2031</td><td>0.3694</td><td>0.3286</td><td>0.3008</td><td>0.2858</td><td>0.2788</td><td>0.4087</td><td>0.3855</td><td>0.3525</td><td>0.3413</td><td>0.3405</td></tr><tr><td>DATC</td><td>0.2954</td><td>0.2748</td><td>0.2631</td><td>0.2596</td><td>0.2541</td><td>0.4939</td><td>0.4332</td><td>0.3651</td><td>0.3215</td><td>0.3037</td><td>0.9210</td><td>0.8431</td><td>0.8536</td><td>0.7734</td><td>0.8125</td></tr><tr><td>NTC</td><td>0.3702</td><td>0.3362</td><td>0.3243</td><td>0.3115</td><td>0.3073</td><td>0.7042</td><td>0.6796</td><td>0.6239</td><td>0.5781</td><td>0.4751</td><td>0.4931</td><td>0.4983</td><td>0.4818</td><td>0.4619</td><td>0.4355</td></tr><tr><td>NTM</td><td>1.2214</td><td>0.8818</td><td>0.7633</td><td>0.6686</td><td>0.6178</td><td>1.4547</td><td>1.3646</td><td>1.3266</td><td>1.2003</td><td>1.1978</td><td>0.6337</td><td>0.7210</td><td>0.6502</td><td>0.6390</td><td>0.6320</td></tr><tr><td>NTF</td><td>0.7529</td><td>0.4147</td><td>0.3637</td><td>0.3486</td><td>0.3353</td><td>0.9061</td><td>0.7783</td><td>0.7189</td><td>0.5958</td><td>0.5125</td><td>0.6788</td><td>0.5335</td><td>0.4976</td><td>0.4620</td><td>0.4114</td></tr><tr><td>CoSTCo</td><td>0.3857</td><td>0.3739</td><td>0.3381</td><td>0.3224</td><td>0.3145</td><td>0.8588</td><td>0.7826</td><td>0.7291</td><td>0.7241</td><td>0.7042</td><td>0.5412</td><td>0.5321</td><td>0.4655</td><td>0.4501</td><td>0.4430</td></tr><tr><td rowspan="9">NRMSE</td><td>MPA-LLM</td><td>0.2635</td><td>0.2119</td><td>0.1961</td><td>0.2128</td><td>0.1679</td><td>0.2048</td><td>0.1761</td><td>0.1662</td><td>0.1531</td><td>0.1291</td><td>0.3428</td><td>0.3156</td><td>0.2907</td><td>0.2800</td><td>0.2806</td></tr><tr><td>ARI-LLM</td><td>0.2316</td><td>0.2123</td><td>0.1966</td><td>0.1905</td><td>0.1818</td><td>0.2767</td><td>0.2360</td><td>0.2221</td><td>0.2206</td><td>0.2077</td><td>0.3525</td><td>0.2923</td><td>0.2830</td><td>0.2790</td><td>0.2729</td></tr><tr><td>PetTC</td><td>0.2413</td><td>0.2205</td><td>0.2113</td><td>0.2087</td><td>0.2062</td><td>0.3214</td><td>0.2321</td><td>0.2298</td><td>0.2285</td><td>0.2128</td><td>0.4116</td><td>0.3789</td><td>0.3632</td><td>0.3576</td><td>0.3425</td></tr><tr><td>LTP</td><td>0.3173</td><td>0.2937</td><td>0.2921</td><td>0.2908</td><td>0.2642</td><td>0.2954</td><td>0.2614</td><td>0.2446</td><td>0.2381</td><td>0.2329</td><td>0.4720</td><td>0.4375</td><td>0.4112</td><td>0.4042</td><td>0.3947</td></tr><tr><td>DATC</td><td>0.3453</td><td>0.3312</td><td>0.3226</td><td>0.3202</td><td>0.3178</td><td>0.3818</td><td>0.3415</td><td>0.2979</td><td>0.2547</td><td>0.2368</td><td>0.9276</td><td>0.8721</td><td>0.7992</td><td>0.7786</td><td>0.7473</td></tr><tr><td>NTC</td><td>0.4388</td><td>0.4072</td><td>0.3951</td><td>0.3858</td><td>0.3766</td><td>0.6412</td><td>0.6266</td><td>0.5888</td><td>0.5450</td><td>0.4310</td><td>0.5308</td><td>0.4737</td><td>0.4490</td><td>0.4259</td><td>0.4140</td></tr><tr><td>NTM</td><td>0.9720</td><td>0.7573</td><td>0.7234</td><td>0.6613</td><td>0.6197</td><td>0.9230</td><td>0.9057</td><td>0.8877</td><td>0.7854</td><td>0.7629</td><td>0.6229</td><td>0.5613</td><td>0.5788</td><td>0.5389</td><td>0.5128</td></tr><tr><td>NTF</td><td>0.6856</td><td>0.4201</td><td>0.3882</td><td>0.3848</td><td>0.3723</td><td>0.7110</td><td>0.6621</td><td>0.5838</td><td>0.4959</td><td>0.4128</td><td>0.6206</td><td>0.5105</td><td>0.4782</td><td>0.4757</td><td>0.4379</td></tr><tr><td>CoSTCo</td><td>0.4081</td><td>0.3929</td><td>0.3736</td><td>0.3666</td><td>0.3600</td><td>0.7215</td><td>0.6579</td><td>0.6252</td><td>0.6037</td><td>0.5927</td><td>0.5286</td><td>0.4643</td><td>0.4595</td><td>0.4234</td><td>0.4120</td></tr><tr><td rowspan="9">KL</td><td>MPA-LLM</td><td>0.0549</td><td>0.0340</td><td>0.0318</td><td>0.0343</td><td>0.0241</td><td>0.1433</td><td>0.1089</td><td>0.0936</td><td>0.0845</td><td>0.0775</td><td>0.2549</td><td>0.1361</td><td>0.1018</td><td>0.0801</td><td>0.0765</td></tr><tr><td>ARI-LLM</td><td>0.0493</td><td>0.0393</td><td>0.0355</td><td>0.0336</td><td>0.0302</td><td>0.1397</td><td>0.1011</td><td>0.0886</td><td>0.0843</td><td>0.0772</td><td>0.1463</td><td>0.0820</td><td>0.0652</td><td>0.0592</td><td>0.0587</td></tr><tr><td>PetTC</td><td>0.0532</td><td>0.0513</td><td>0.0501</td><td>0.0498</td><td>0.0471</td><td>0.2593</td><td>0.1408</td><td>0.1308</td><td>0.1419</td><td>0.1280</td><td>0.1237</td><td>0.1145</td><td>0.1076</td><td>0.1053</td><td>0.1029</td></tr><tr><td>LTP</td><td>0.5021</td><td>0.1832</td><td>0.1524</td><td>0.1336</td><td>0.1004</td><td>0.7012</td><td>0.4531</td><td>0.4254</td><td>0.3755</td><td>0.3491</td><td>0.4641</td><td>0.3573</td><td>0.3214</td><td>0.2561</td><td>0.2139</td></tr><tr><td>DATC</td><td>0.0994</td><td>0.0881</td><td>0.0794</td><td>0.0767</td><td>0.0736</td><td>0.4495</td><td>0.3338</td><td>0.2522</td><td>0.2327</td><td>0.2103</td><td>1.5789</td><td>1.2631</td><td>1.0789</td><td>0.7368</td><td>0.7894</td></tr><tr><td>NTC</td><td>0.1578</td><td>0.1326</td><td>0.1202</td><td>0.1157</td><td>0.1095</td><td>1.2776</td><td>1.0643</td><td>0.8378</td><td>0.8306</td><td>0.4765</td><td>0.4814</td><td>0.3476</td><td>0.3015</td><td>0.3289</td><td>0.1952</td></tr><tr><td>NTM</td><td>2.5215</td><td>0.9318</td><td>0.8276</td><td>0.7838</td><td>0.6946</td><td>2.0707</td><td>1.9729</td><td>1.8230</td><td>1.7226</td><td>1.5882</td><td>2.3166</td><td>0.2011</td><td>0.1974</td><td>0.1553</td><td>0.1102</td></tr><tr><td>NTF</td><td>0.4744</td><td>0.2114</td><td>0.1635</td><td>0.1591</td><td>0.1228</td><td>1.1552</td><td>0.7186</td><td>0.6736</td><td>0.6624</td><td>0.5734</td><td>0.2431</td><td>0.1572</td><td>0.1084</td><td>0.1057</td><td>0.1041</td></tr><tr><td>CoSTCo</td><td>0.3566</td><td>0.4370</td><td>0.3305</td><td>0.2851</td><td>0.2461</td><td>5.2273</td><td>3.7190</td><td>3.4680</td><td>3.3872</td><td>3.0307</td><td>0.2995</td><td>0.2439</td><td>0.1911</td><td>0.1768</td><td>0.1244</td></tr></table>

TABLE VI  
FORECASTING PERFORMANCE ON ABILENE, GEANT <sup>´</sup> AND WS-DREAM. BOLD: BEST, UNDERLINED: SECOND BEST

<table><tr><td>Dataset</td><td colspan="3">Abilene</td><td colspan="3">GÉANT</td><td colspan="3">WS-DREAM</td></tr><tr><td>Model</td><td>NMAE</td><td>NRMSE</td><td>KL</td><td>NMAE</td><td>NRMSE</td><td>KL</td><td>NMAE</td><td>NRMSE</td><td>KL</td></tr><tr><td>MPA-LLM</td><td>0.2877</td><td>0.3841</td><td>0.1551</td><td>0.2894</td><td>0.2130</td><td>0.1538</td><td>0.2222</td><td>0.3322</td><td>0.1121</td></tr><tr><td>ICTSP</td><td>0.3930</td><td>0.5210</td><td>1.8100</td><td>0.3245</td><td>0.2747</td><td>0.4241</td><td>1.7855</td><td>1.3483</td><td>16.6513</td></tr><tr><td>LSINet</td><td>0.4320</td><td>0.6035</td><td>6.9180</td><td>0.4992</td><td>0.5975</td><td>3.8546</td><td>1.4144</td><td>1.0958</td><td>48.4048</td></tr><tr><td>RTS-PnO</td><td>0.3895</td><td>0.5455</td><td>5.9994</td><td>0.4367</td><td>0.5754</td><td>3.2744</td><td>0.9984</td><td>1.0279</td><td>45.4322</td></tr></table>

Table VII reports the affiliation precision (Aff P), affiliation recall (Aff R), and affiliation F1 score (Aff F1) on three realworld datasets, comparing MPA-LLM with three state-of-theart anomaly detection methods. As shown in the table, MPA-LLM achieves the highest overall detection performance across all datasets. On the Abilene dataset, MPA-LLM attains the best Aff F1 of 0.7215, significantly outperforming the best baseline GCAD. Specifically, MPA-LLM offers a more balanced trade-off between precision and recall, resulting in the best F1 score. On GEANT, MPA-LLM substantially outperforms<sup>´</sup> all baselines, achieving an Aff F1 of 0.7085, compared to GCAD at 0.5188. Its Aff P reaches 0.9036, meaning nearly all detected anomalies correspond to true events. Moreover, its Aff R of 0.5827 is also the highest among all methods, demonstrating that MPA-LLM captures a substantial portion of ground truth anomalies while maintaining a low false positive rate. On WS-DREAM, the most challenging high-dimensional dataset, MPA-LLM again achieves the best Aff F1 of 0.4048. CATCH exhibits the highest recall of 0.5209 but suffers from a low precision, which results in a low F1 score of 0.3164. In contrast, MPA-LLM maintains a balanced tradeoff between precision and recall, confirming its robustness in large-scale network environments. These results underscore that the multi-parameterized autoregressive design of MPA-LLM yields superior anomaly detection capabilities by preserving fine-grained spatiotemporal patterns and enabling reliable identification of anomalous traffic intervals.

TABLE VII  
ANOMALY DETECTION PERFORMANCE ON ABILENE, GEANT <sup>´</sup> AND WS-DREAM. BOLD: BEST, UNDERLINED: SECOND BEST

<table><tr><td>Dataset</td><td colspan="3">Abilene</td><td colspan="3">GÉANT</td><td colspan="3">WS-DREAM</td></tr><tr><td>Model</td><td>Aff_P</td><td>Aff_R</td><td>Aff_F1</td><td>Aff_P</td><td>Aff_R</td><td>Aff_F1</td><td>Aff_P</td><td>Aff_R</td><td>Aff_F1</td></tr><tr><td>MPA-LLM</td><td>0.7410</td><td>0.7029</td><td>0.7215</td><td>0.9036</td><td>0.5827</td><td>0.7085</td><td>0.5255</td><td>0.3292</td><td>0.4048</td></tr><tr><td>GCAD</td><td>0.6895</td><td>0.7189</td><td>0.7039</td><td>0.4683</td><td>0.5815</td><td>0.5188</td><td>0.4555</td><td>0.1299</td><td>0.2021</td></tr><tr><td>CATCH</td><td>0.6502</td><td>0.7246</td><td>0.6853</td><td>0.5208</td><td>0.5045</td><td>0.5125</td><td>0.2272</td><td>0.5209</td><td>0.3164</td></tr><tr><td>DADA</td><td>0.5497</td><td>0.2930</td><td>0.3823</td><td>0.5518</td><td>0.2121</td><td>0.3064</td><td>0.4831</td><td>0.2455</td><td>0.3256</td></tr></table>

TABLE VIII

MULTI-TASK PERFORMANCE COMPARISON OF SEPARATE AND JOINTTRAIN MPA-LLM. BOLD: BETTER RESULT BETWEEN THE TWO TRAINING PROTOCOLS FOR EACH DATASET AND METRIC.

<table><tr><td colspan="2">Dataset</td><td colspan="3">Imputation</td><td colspan="3">Forecasting</td><td colspan="3">Anomaly Detection</td></tr><tr><td>Dataset</td><td>Training</td><td>NMAE</td><td>NRMSE</td><td>KL</td><td>NMAE</td><td>NRMSE</td><td>KL</td><td>Aff_P</td><td>Aff_R</td><td>Aff_F1</td></tr><tr><td rowspan="2">Abilene</td><td>MPA-LLM</td><td>0.1360</td><td>0.1679</td><td>0.0241</td><td>0.2877</td><td>0.3841</td><td>0.1551</td><td>0.7410</td><td>0.7029</td><td>0.7215</td></tr><tr><td>MPA-LLM (JointTrain)</td><td>0.1945</td><td>0.2513</td><td>0.0480</td><td>0.2802</td><td>0.4027</td><td>0.1498</td><td>0.7786</td><td>0.5002</td><td>0.6091</td></tr><tr><td rowspan="2">GÉANT</td><td>MPA-LLM</td><td>0.1897</td><td>0.1291</td><td>0.0775</td><td>0.2894</td><td>0.2130</td><td>0.1538</td><td>0.9036</td><td>0.5827</td><td>0.7085</td></tr><tr><td>MPA-LLM (JointTrain)</td><td>0.2216</td><td>0.1479</td><td>0.0884</td><td>0.2970</td><td>0.1958</td><td>0.1546</td><td>0.9339</td><td>0.6560</td><td>0.7706</td></tr><tr><td rowspan="2">WS-DREAM</td><td>MPA-LLM</td><td>0.1998</td><td>0.2806</td><td>0.0765</td><td>0.2222</td><td>0.3322</td><td>0.1121</td><td>0.5255</td><td>0.3292</td><td>0.4048</td></tr><tr><td>MPA-LLM (JointTrain)</td><td>0.2400</td><td>0.3110</td><td>0.0956</td><td>0.2512</td><td>0.3348</td><td>0.1131</td><td>0.8177</td><td>0.1951</td><td>0.3150</td></tr></table>

## E. Multi-Task Evaluation with Joint Training

To investigate whether the framework can instead be trained with a single shared training process, we further evaluate a JointTrain variant, denoted as MPA-LLM (JointTrain). The key difference is that JointTrain jointly trains the imputation and forecasting tasks within the same model, whereas the standard MPA-LLM uses separate training for the two tasks.

To distinguish the heterogeneous task requirements during joint training, we introduce a small number of additional trainable embedding parameters, including a task embedding and a mask-type embedding. The task embedding provides explicit information about the current task, while the mask-type embedding indicates the masking pattern of the input. These lightweight trainable parameters allow the shared model to distinguish different task-specific inputs and reduce parameter interference caused by jointly optimizing heterogeneous tasks within a shared parameter space.

Table VIII compares the performance of the separatetraining and joint-training protocols on the three datasets. For imputation, separate training consistently outperforms JointTrain across all three datasets. On Abilene, separate training achieves 30.1%, 33.2%, and 49.8% lower NMAE, NRMSE, and KL, respectively. On GEANT, the corresponding<sup>´</sup> reductions are 14.4%, 12.7%, and 12.3%, respectively. On WS-DREAM, separate training reduces NMAE, NRMSE, and KL by 16.8%, 9.8%, and 20.0%, respectively.

For forecasting, the results are more task- and datasetdependent. On Abilene, JointTrain reduces NMAE and KL by 2.6% and 3.4%, respectively, whereas separate training reduces NRMSE by 4.6%. On GEANT, JointTrain achieves an 8.1%<sup>´</sup> lower NRMSE, while separate training reduces NMAE and KL by 2.6% and 0.5%, respectively. On WS-DREAM, separate training performs better on all three metrics, reducing NMAE, NRMSE, and KL by 11.5%, 0.8%, and 0.9%, respectively.

For anomaly detection, JointTrain achieves higher affiliation precision on all three datasets, with relative improvements of 5.1%, 3.4%, and 55.6% on Abilene, GEANT, and WS-<sup>´</sup> DREAM, respectively. On GEANT, JointTrain further im-<sup>´</sup> proves affiliation recall and F1 by 12.6% and 8.8%, respectively. In contrast, separate training achieves higher affiliation recall and F1 on Abilene, with improvements of 40.5% and 18.5%, respectively, and on WS-DREAM, with improvements of 68.7% and 28.5%, respectively.

Overall, these results demonstrate that JointTrain can support the three-task workflow with a shared training process, but its performance remains task- and dataset-dependent. Particularly, JointTrain provides advantages for some forecasting and anomaly detection metrics, while separate training achieves more consistent imputation performance and shows advantages on several forecasting and anomaly detection metrics. This indicates that jointly optimizing heterogeneous tasks within a shared parameter space can introduce task-specific performance trade-offs. Therefore, we retain separate training for the main MPA-LLM results when task-specific performance consistency is prioritized, while JointTrain provides a practical alternative when simplified model management is preferred.

## F. Performance with Limited TM Snapshots

Considering the high cost of TM data collection, we evaluate the performance of the two methods under limited TM snapshots. Specifically, we train the model using only the first 5% or 10% of the full training snapshots, and then apply it to impute, forecast, and detect anomalies on the test set. Fig. 3, 4, and 5 summarize the few-shot performance for forecasting, anomaly detection, and imputation, respectively. We focus on NMAE for forecasting and imputation, and Aff F1 for anomaly detection.

Figure 3 shows the imputation performance of MPA-LLM and PetTC (the best baseline) at 100%, 10%, and 5% of training snapshots, respectively. MPA-LLM demonstrates exceptional robustness against data scarcity, whereas the baseline PetTC suffers significant performance degradation. Across the three datasets, the estimation error of MPA-LLM remains remarkably stable, showing a negligible error increase of only 0.2%–1.2% under 10% data availability, and capping at 3.2% increase even with 5% data. Conversely, PetTC is highly sensitive to the lack of training samples, yielding a substantial error increase of 9.0%–14.9% with 10% training data, which further widens to 12.9%–19.4% when the data ratio drops to 5%. These results demonstrate the strong few-shot learning capability of MPA-LLM, enabling significant reductions in training costs.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/fbb840b5cd1cccb0f58959c2318da3debf0921ae8a235ac6ff59bdcce1b21c3f.jpg)  
(a) Abilene

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/4562b92cc846434d586e6381211107f7fe1a5cce940663b0abd576e81c249bf0.jpg)  
(b) GÉANT

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/1bc9fa2a00ca7d5fc9137120ba09a7de8016ed54a668d907966a376b165d4c3f.jpg)  
(c) WS-DREAM  
Fig. 3. Imputation errors on limited TM snapshots.

Turning to the network traffic forecasting task, Figure 4 presents the NMAE performance of MPA-LLM and ICTSP (the best baseline) under three training scenarios. As shown, MPA-LLM maintains relatively stable performance even when the training data is significantly reduced. Specifically, across the three datasets, the estimation error of MPA-LLM increases by only 1.0%–6.2% with 10% training data and by 3.5%–7.5% with 5% training data compared to its full-training baseline. In contrast, although ICTSP also exhibits a seemingly small relative increase in error, this is mainly because its baseline estimation error under full training is already relatively high, leaving limited room for further degradation.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/c341e42a8b4222ef606e2f232de3458448a2cd7fab56a172d3bf7d35abe0f203.jpg)  
(a) Abilene

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/e2b580da51f1318f570ee23888a9681b0f0f0007fc8279acb4ca9cde4cdab605.jpg)  
(b) GÉANT

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/5ad5ed507b9c7f7edb5fdb46e1b6f4e18b6dd41deab757942aafa6e9610fdc9a.jpg)  
Fig. 4. Forecasting errors on limited TM snapshots.  
(c) WS-DREAM

Figure 5 presents the AFF F1 score of MPA-LLM and GCAD (the best baseline) under three training settings for the anomaly detection task. As shown, MPA-LLM still maintains relatively stable detection accuracy even when the training data is significantly reduced, whereas GCAD exhibits a sharp decline in accuracy. Specifically, averaged over the three datasets, the estimation accuracy of MPA-LLM drops by only 0.2%–1.5% with 10% training data and by 0.6%–4.7% with 5% training data. In contrast, GCAD suffers much larger degradation, with accuracy drops of 7.9%–45.3% and 17.1%–45.4%, respectively.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/b0733690014a9b2585277807432a345dec445f3286bea8cbf8e70741a8edb954.jpg)  
(a) Abilene

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/1c19df2c0c23b749d11240e5ec922c23d7268a3ae15fdfbc5f9ca646c760de8b.jpg)  
(b) GÉANT

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/8bd0efadd96ce1be2ad9ae37d7a980c4f41d5938193c13248e5b591546f25e0f.jpg)  
(c) WS-DREAM  
Fig. 5. Anomaly detection errors on limited TM snapshots.

## G. Performance in Unseen Networks

This subsection evaluates the zero-shot generalization capability of MPA-LLM under a challenging scenario: adapting to an entirely unseen network without any prior knowledge of its traffic distribution or topology. The model is trained on TM data from one source network and then directly applied to impute, forecast, or detect anomalies in a different target network.

In Fig. 6, A→A and G→G denote settings where both the training and testing TMs come from the same network (Abilene and GEANT, respectively), serving as the comparison<sup>´</sup> baselines; G→A indicates that the model is trained on GEANT<sup>´</sup> and tested on Abilene, while A→G represents the reverse. As shown, MPA-LLM consistently outperforms the strongest baselines across all three tasks.

Specifically, for the imputation task, the NMAE of MPA-LLM rises by just 2.9% in Abilene and 12.4% in GEANT.<sup>´</sup> In contrast, PetTC suffers from a severe degradation, with its error increasing by 14.1% in Abilene and 27.7% in GEANT.<sup>´</sup> For the forecasting task, although the NMAE increase of MPA-LLM under zero-shot transfer appears slightly larger than that of ICTSP, this is largely because ICTSP already yields relatively high estimation errors in the source domain (i.e., when trained and tested on the same network), leaving limited room for further degradation. Crucially, even under zero-shot conditions, MPA-LLM still achieves significantly lower absolute errors than ICTSP does on its own source domain. In the anomaly detection task, the disparity becomes even more pronounced: the Aff F1 score of MPA-LLM drops by 6.0% in Abilene and 20.1% in GEANT, whereas GCAD<sup>´</sup> undergoes a dramatic performance decline, dropping by 50.1% in Abilene and 73.0% in GEANT. This demonstrates the<sup>´</sup> pre-trained knowledge embedded in the LLM within MPA-LLM endows it with strong zero-shot and knowledge transfer capabilities, significantly enhancing its adaptability to unseen networks.

## H. Ablation Study

To validate the effectiveness of key components in MPA-LLM, we conduct ablation experiments on three datasets across two downstream tasks: imputation and anomaly detection. Since forecasting is essentially a numerical fitting task similar to imputation, the ablation results on imputation are expected to generalize. We compare the full MPA-LLM with three variants: (i) MPA-LLM w/o Prompt, which removes the task-specific prompt embedding; (ii) MPA-LLM w/o AR, which removes the autoregressive learning mechanism and adopts a single-step strategy; and (iii) MPA-LLM w/o Multi-Param, which replaces the decoupled multi-parameterized architecture with a single shared model (i.e., ARI-LLM [9]).

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/a0e925f5754a9fbc3546685c07ed9653f54f34c8cdcdfcf98a8814cda114828c.jpg)  
Fig. 6. Errors of three tasks on unseen networks (A: Abilene, G: GEANT).<sup>´</sup>

For the imputation task, as shown in Fig. 7, the full MPA-LLM achieves the lowest NMAE on all three datasets, confirming the contribution of each component. On Abilene, removing the prompt, autoregressive mechanism, and multiparameterized design degrades NMAE by 6.0%, 5.9%, and 9.7%, respectively. On GEANT, the corresponding degra-<sup>´</sup> dations are 4.1%, 8.8%, and 9.4%. On WS-DREAM, the degradations are 1.1%, 4.1%, and 1.5%. As shown in Fig. 8, we evaluate the same variants on anomaly detection, and the full MPA-LLM consistently achieves the highest Aff F1. On Abilene, removing the prompt, autoregressive mechanism, and multi-parameterized design degrades the Aff F1 by 0.5%, 2.0%, and 0.8%, respectively. On GEANT, the corresponding<sup>´</sup> degradations are 2.3%, 3.1%, and 2.4%. On WS-DREAM, the degradations are 2.3%, 3.5%, and 2.8%.

In summary, removing the prompt, the autoregressive mechanism, and the multi-parameterized design leads to average performance drops of 2.8%, 4.6%, and 4.5%, respectively, across both tasks. Across all datasets, the removal of either the autoregressive mechanism or the multi-parameterized architecture consistently causes a larger performance drop than removing the prompt, indicating that the coarse-to-fine reasoning and stage-decoupled design are the primary drivers of MPA-LLM’s superior accuracy. The prompt still provides useful guidance, especially on the Abilene and GEANT datasets. These results<sup>´</sup> collectively demonstrate the effectiveness and versatility of the proposed MPA-LLM architecture across different network analysis tasks.

## I. Sensitivity to the Initial Observation Ratio

To examine how the initial observation ratio affects MPA-LLM’s performance, we varied this ratio from 1% to 10% while keeping the remaining model configuration unchanged. For each setting, the refinement schedule was generated by progressively doubling the current observation ratio and stopping at 100%. Therefore, the number of refinement stages depends on the selected initial observation ratio. Specifically, the 1% setting requires seven refinement stages, the 2% and 3% settings require six refinement stages, the 4%–7% settings require five refinement stages, and the 8%–10% settings require four refinement stages. Table IX reports NMAE, NRMSE, KL divergence, training time, and inference time, averaged across the three datasets.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/abab7ecff3cfb91149667ef6f923daf6b4613244fb07d062f746f0068fec6590.jpg)  
Fig. 7. Ablation results for TM imputation.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/ca07d88a8ec340682da9aa7ad8e480d2963c4252c9753aaad1af523b6231c1af.jpg)  
Fig. 8. Ablation results for anomaly detection.

The 1% setting obtains the lowest average NMAE, NRMSE, and KL values. However, the 2% setting is very close, with relative increases of only 1.89%, 2.54%, and 1.69% in NMAE, NRMSE, and KL, respectively, compared with the 1% setting. Meanwhile, starting from 2% reduces the number of refinement stages from seven to six. As shown in Table IX, this reduction decreases the training time from 570.18 s to 492.34 s, corresponding to a 13.65% reduction, and decreases the inference time from 11.53 s to 9.19 s, corresponding to a 20.30% reduction. Therefore, although the 1% setting provides slightly better reconstruction accuracy, the 2% setting achieves a more favorable balance between reconstruction accuracy and computational cost.

TABLE IX  
SENSITIVITY TO THE INITIAL OBSERVATION RATIO. RESULTS ARE AVERAGED OVER ABILENE, GEANT, <sup>´</sup> AND WS-DREAM. BOLD: BEST, UNDERLINED: SECOND BEST

<table><tr><td>Initial Ratio</td><td>NMAE</td><td>NRMSE</td><td>KL</td><td>Training</td><td>Inferring</td></tr><tr><td>1%</td><td>0.1851</td><td>0.2083</td><td>0.0650</td><td>570.18</td><td>11.53</td></tr><tr><td>2%</td><td>0.1886</td><td>0.2136</td><td>0.0661</td><td>492.34</td><td>9.19</td></tr><tr><td>3%</td><td>0.1910</td><td>0.2141</td><td>0.0686</td><td>489.93</td><td>9.09</td></tr><tr><td>4%</td><td>0.1938</td><td>0.2088</td><td>0.0701</td><td>408.28</td><td>7.60</td></tr><tr><td>5%</td><td>0.1953</td><td>0.2093</td><td>0.0706</td><td>408.80</td><td>7.90</td></tr><tr><td>6%</td><td>0.1959</td><td>0.2103</td><td>0.0735</td><td>416.05</td><td>8.04</td></tr><tr><td>7%</td><td>0.1980</td><td>0.2117</td><td>0.0758</td><td>425.63</td><td>8.16</td></tr><tr><td>8%</td><td>0.1950</td><td>0.2106</td><td>0.0745</td><td>345.45</td><td>7.42</td></tr><tr><td>9%</td><td>0.2008</td><td>0.2152</td><td>0.0759</td><td>335.99</td><td>7.13</td></tr><tr><td>10%</td><td>0.1979</td><td>0.2128</td><td>0.0717</td><td>346.25</td><td>7.22</td></tr></table>

Table IX also shows that further increasing the initial observation ratio can reduce inference time, while the reconstruction error increases modestly. Therefore, when computational resources are limited, one can increase the initial observation ratio to shorten computation time, achieving a favorable tradeoff between accuracy and cost.

## J. Running Speed

TABLE X  
TRAINING AND INFERRING TIME IN SECONDS [S] FOR IMPUTATION TASKS. BOLD: BEST, UNDERLINED: SECOND BEST

<table><tr><td rowspan="2">Model / Datasets</td><td colspan="2">Abilene</td><td colspan="2">GÉANT</td><td colspan="2">WS-DREAM</td></tr><tr><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td></tr><tr><td>NTM</td><td>128.0</td><td>2.8</td><td>1460.5</td><td>9.2</td><td>5202.0</td><td>266.4</td></tr><tr><td>NTC</td><td>618.1</td><td>4.2</td><td>3506.3</td><td>13.7</td><td>2177.1</td><td>228.6</td></tr><tr><td>CoSTCo</td><td>596.2</td><td>3.2</td><td>526.2</td><td>65.1</td><td>1487.8</td><td>20.6</td></tr><tr><td>NTF</td><td>84.8</td><td>2.9</td><td>678.3</td><td>10.3</td><td>3019.4</td><td>207.9</td></tr><tr><td>LTP</td><td>239.6</td><td>2.9</td><td>1373.0</td><td>10.3</td><td>3829.0</td><td>209.0</td></tr><tr><td>DATC</td><td>1728.5</td><td>4.5</td><td>1876.2</td><td>6.1</td><td>7548.6</td><td>23.2</td></tr><tr><td>PetTC</td><td>160.3</td><td>4.0</td><td>1723.1</td><td>13.0</td><td>2127.8</td><td>253.3</td></tr><tr><td>ARI-LLM</td><td>93.2</td><td>1.3</td><td>360.7</td><td>8.4</td><td>1024.8</td><td>16.4</td></tr><tr><td>MPA-LLM</td><td>92.9</td><td>1.5</td><td>391.8</td><td>10.3</td><td>971.0</td><td>18.3</td></tr></table>

TABLE XI  
TRAINING AND INFERRING TIME IN SECONDS [S] FOR ANOMALY DETECTION TASKS. BOLD: BEST, UNDERLINED: SECOND BEST

<table><tr><td rowspan="2">Model / Datasets</td><td colspan="2">Abilene</td><td colspan="2">GÉANT</td><td colspan="2">WS-DREAM</td></tr><tr><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td><td>Training</td><td>Inferring</td></tr><tr><td>DADA</td><td>73.6</td><td>2.3</td><td>210.6</td><td>9.1</td><td>450.3</td><td>20.8</td></tr><tr><td>GCAD</td><td>104.5</td><td>2.6</td><td>404.7</td><td>14.2</td><td>1561.6</td><td>26.7</td></tr><tr><td>CATCH</td><td>557.4</td><td>3.8</td><td>550.2</td><td>22.5</td><td>2090.7</td><td>21.5</td></tr><tr><td>MPA-LLM</td><td>92.9</td><td>1.5</td><td>391.8</td><td>10.3</td><td>971.0</td><td>18.3</td></tr></table>

Tables X and XI compare the training and inference times of each method for the imputation and anomaly detection tasks, respectively. The training time refers to the duration from feeding the full training data into the model until convergence. The inference time of imputation is measured as the total time taken to recover all testing data under a 10% observation rate. For anomaly detection, the inference time includes the duration of reconstructing all testing data and identifying anomalies.

As shown in the tables, the training and inference times for all models are shortest on the Abilene dataset and longest on the WS-DREAM dataset, corresponding directly to their respective network sizes and TM dimensions. Remarkably, despite adopting a step-wise autoregressive strategy with six decoupled GPT modules, MPA-LLM remains highly competitive across both tasks. Compared with our previous ARI-LLM, MPA-LLM maintains comparable training efficiency, while the additional stage-decoupled design introduces only a moderate inference-time overhead.

Specifically, for the imputation task in Table X, MPA-LLM reduces the training time of ARI-LLM by 0.3% on Abilene and 5.3% on WS-DREAM, while requiring 8.6% more training time on GEANT. MPA-LLM achieves the second-shortest in-<sup>´</sup> ference time on Abilene and WS-DREAM, while on GEANT<sup>´</sup> its inference time is at an intermediate level. Although ARI-LLM is faster during inference, considering that MPA-LLM extends the original framework to support multi-task traffic analysis, its additional inference overhead is a reasonable cost incurred by the stage-decoupled architecture. Regarding the anomaly detection task in Table XI, MPA-LLM achieves the shortest inference time on two of the three datasets. Notably, on the large-scale WS-DREAM dataset, MPA-LLM achieves an inference time of just 18.3 seconds, which is 12.0% faster than the second-best DADA in the anomaly detection task. The key reasons for this efficiency are as follows. First, the autoregressive learning scheme in MPA-LLM generates TM blocks of varying resolutions at each step rather than individual flows, enabling efficient batch processing. Second, unlike other models that require full training of large parameter sets, MPA-LLM employs lightweight fine-tuning of the LLM backbone, with only the Flow2Vec embedder, normalization layers, feed-forward networks, and the MLP projection head being trainable. Finally, the coarse-to-fine autoregressive training paradigm, combined with task-specific prompt guidance, allows MPA-LLM to converge rapidly, typically within just 2–3 training epochs. As shown in Tables X and XI, the training and inference times of MPA-LLM are identical across the two tasks. This is because anomaly detection directly reuses the reconstruction process of imputation and involves no separate training. During inference, anomaly detection requires additional residual computation and percentile-based thresholding, but they incur only millisecond-level overhead.

## K. LLM Variants Analysis

To evaluate the impact of LLM backbone on our framework, we assess five representative LLM backbones of varying parameter sizes on the Abilene dataset, as detailed in Fig. 9. Performance is quantified using the NMAE metric for data imputation, alongside the Aff F1 score for anomaly detection.

As shown in Fig. 9, the Qwen model achieves the best overall performance across both tasks, followed closely by Llama-3. This is because Qwen and Llama-3 possess relatively large parameter capacities of 747M and 627M, respectively, endowing them with robust representational power. Notably, despite having only 81M parameters—the smallest among the compared models—GPT-2 does not suffer from significant performance degradation in imputation and anomaly detection. In fact, it exhibits a superior trade-off between task performance and resource consumption when compared to the much larger baselines.

We select GPT-2 as the backbone for MPA-LLM due to its minimal performance degradation. Specifically, its imputation error (NMAE of 0.1517) remains highly competitive, only 3.9% higher than that of the best Qwen model (0.1460). Its Aff F1 score of 0.7060 is within 1.8% of Qwen. Furthermore, unlike much larger models such as Gemma-2-2B-it (1,057M parameters) and DeepSeek-Coder-1.3B (435M parameters), which do not deliver proportional performance gains despite their scale, GPT-2 achieves superior or highly comparable results across core metrics while using far fewer parameters. Ultimately, since our framework emphasizes both task accuracy and computational efficiency, the lightweight GPT-2 offers the optimal balance: it delivers high-quality results with less than one-ninth of the parameters required by Qwen.

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/fdae79d509bff32a7c096a5052ae2eaaa53bf92121d165f2c349c30003ecddbc.jpg)

![](../01-mineru-output/2026-TDSC-Trustworthy_Traffic_Analysis_via_Large_Language_Models/images/e564b0c11acdf2b4850a275246f0a8749db94b7f760a3091c8334d2786ca5b89.jpg)  
Fig. 9. Imputation and anomaly detection performance (NMAE and Aff F1 Score) of MPA-LLM under different LLM backbones

## V. LIMITATIONS

Although MPA-LLM achieves promising performance on TM imputation, forecasting, and anomaly detection tasks, two limitations remain to be addressed. First, the multi-LLM design enhances stage-specific modeling capability and reduces interference across different refinement stages. However, compared with a single LLM architecture, maintaining multiple LLM instances inevitably introduces additional storage and deployment overhead. Although the lightweight fine-tuning strategy freezes a portion of parameters in each LLM and keeps the training and inference costs competitive, the overall resource consumption may still increase as the number of refinement stages grows. Second, the anomaly detection module relies on reconstruction residuals and dynamically calibrated thresholds. This design avoids training an additional anomaly classifier and enables unified utilization of reconstructed TMs. However, the detection performance may still be affected by threshold selection and the availability of prior anomaly ratios. In real-world deployments, when anomaly rates are unknown or change significantly over time, more robust threshold calibration strategies are required. Future research could explore more efficient multi-LLM coordination mechanisms, and anomaly detection approaches that reduce reliance on prior information, thereby further improving the scalability, adaptability, and robustness of our approach.

## VI. CONCLUSION

In this paper, we propose MPA-LLM, a trustworthy multitask traffic analysis framework that establishes a new state-ofthe-art for TM anomaly detection, imputation, and forecasting. To enhance the generalization capability and reliability of existing methods, MPA-LLM integrates multi-parameterized autoregressive mechanism with a multi-task adaptation design. Inspired by the coarse-to-fine human cognitive process, MPA-LLM conceptualizes progressive TM recovery as a stepwise autoregressive generation, decomposing sparse observations into multiple intermediate representations. It deploys six mutually independent, stage-specific LLM modules to capture distinct traffic manifolds without cross-scale parameter contamination, thereby rendering the recovery process highly transparent and auditable—a key enabler for trustworthy and secure data circulation across multi-party domains. A unified projection head then maps the latent states back to the raw numerical space, simultaneously supporting imputation, forecasting, and anomaly detection within a single framework. Extensive experiments on three real-world datasets demonstrate that MPA-LLM significantly outperforms state-of-theart methods in multi-task generalizability, and it maintains strong performance with only limited TM knowledge or even no prior knowledge of unseen networks. We make our source code publicly available to facilitate reproducibility.

## ACKNOWLEDGMENT

This research is supported by the National Natural Science Foundation of China (NSFC) (No. 62572168, 62472140, 62025201), the Young Scientists Fund (Category B) of National Nature Science Foundation of China (NSFC) (No. 62622209), the Anhui Provincial Natural Science Foundation (2508085MF151).

## REFERENCES

[1] S. H. Rafique, A. Abdallah, N. S. Musa, and T. Murugan, “Machine learning and deep learning techniques for internet of things network anomaly detection—current research trends,” Sensors, vol. 24, no. 6, p. 1968, 2024.

[2] Y. Qiao, X. Yuan, and K. Wu, “Routing-oblivious network tomography with flow-based generative model,” in IEEE INFOCOM 2024-IEEE Conference on Computer Communications (INFOCOM). IEEE, 2024, pp. 2139–2148.

[3] Y.-F. Liu, K. C.-J. Lin, and C.-C. Tseng, “Dynamic cluster-based flow management for software defined networks,” IEEE Transactions on Services Computing, vol. 15, no. 1, pp. 361–371, 2019.

[4] Z. Hu and J. Luo, “Cracking network monitoring in dcns with sdn,” in 2015 IEEE Conference on Computer Communications (INFOCOM), 2015, pp. 199–207.

[5] P. Phaal, S. Panchen, and N. McKee, “Inmon corporation’s sflow: A method for monitoring traffic in switched and routed networks,” RFC, vol. 3176, pp. 1–31, 2001. [Online]. Available: https://doi.org/10. 17487/RFC3176

[6] K. Xie, Y. Chen, X. Wang, G. Xie, J. Cao, and J. Wen, “Accurate and fast recovery of network monitoring data: A GPU accelerated matrix completion,” IEEE/ACM Transactions on Networking, vol. 28, pp. 958–971, 2020. [Online]. Available: https://doi.org/10.1109/TNET. 2020.2976129

[7] Y. Vardi, “Network tomography: Estimating source-destination traffic intensities from link data,” Journal of the American statistical association, vol. 91, no. 433, pp. 365–377, 1996.

[8] A. Medina, N. Taft, K. Salamatian, S. Bhattacharyya, and C. Diot, “Traffic matrix estimation: existing techniques and new directions,” in Conference on Applications, Technologies, Architectures, and Protocols for Computer Communication (SIGCOMM), 2002. [Online]. Available: https://api.semanticscholar.org/CorpusID:2830485

[9] F. Yan, K. Jiang, Y. Qiao, M. Li, Y. Li, P. Yu, and C. Feng, “Ari-llm: Autoregressive imputation for network traffic matrix via large language models,” in IEEE INFOCOM 2026-IEEE Conference on Computer Communications (INFOCOM). IEEE, 2026, pp. 1–10.

[10] M. Li, Y. Chen, Y. Qiao, G. Ye, Z. Zhang, L. Zhu, and M. Conti, “Trust in a decentralized world: Data governance from faithful, private, verifiable, and traceable data feeds,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 10 818–10 833, 2025.

[11] C. Tebaldi and M. West, “Bayesian inference on network traffic using link count data,” Journal ofthe American Statistical Association, vol. 93, no. 442, pp. 557–573, 1998.

[12] Y. Zhang, M. Roughan, N. Duffield, and A. Greenberg, “Fast accurate computation of large-scale ip traffic matrices from link loads,” ACM SIGMETRICS Performance Evaluation Review, vol. 31, no. 1, pp. 206– 217, 2003.

[13] X. Yuan, Y. Qiao, P. Zhao, R. Hu, and B. Zhang, “Traffic matrix estimation based on denoising diffusion probabilistic model,” 2023 IEEE Symposium on Computers and Communications (ISCC), pp. 316–322, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID: 261307471

[14] J. Li, H. He, S. Chen, D. Jin, and J. Yang, “Loggraph: Log event graph learning aided robust fine-grained anomaly diagnosis,” IEEE Transactions on Dependable and Secure Computing, vol. 21, pp. 1876–1889, 2024. [Online]. Available: https://doi.org/10.1109/TDSC. 2023.3293111

[15] M. Roughan, Y. Zhang, W. Willinger, and L. Qiu, “Spatio-temporal compressive sensing and internet traffic matrices (extended version),” IEEE/ACM Transactions on Networking, vol. 20, no. 3, pp. 662–676, 2011.

[16] P. Tune and M. Roughan, “Spatiotemporal traffic matrix synthesis,” in Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication (SIGCOMM), 2015, pp. 579–592.

[17] K. Xie, H. Lu, X. Wang, G. Xie, Y. Ding, D. Xie, J. Wen, and D. Zhang, “Neural tensor completion for accurate network monitoring,” in IEEE INFOCOM 2020-IEEE Conference on Computer Communications (IN-FOCOM). IEEE, 2020, pp. 1688–1697.

[18] H. Xie, Y. Gong, and X. Dong, “Spatial–temporal regularized tensor decomposition method for traffic speed data imputation,” International Journal of Data Science and Analytics, vol. 17, no. 2, pp. 203–223, 2024.

[19] T. Deng, M. Wan, K. Shi, L. Zhu, X. Wang, and X. Jiang, “Short term prediction of wireless traffic based on tensor decomposition and recurrent neural network,” SN Applied Sciences, vol. 3, no. 9, p. 779, 2021.

[20] X. Wang and L. Sun, “Diagnosing spatiotemporal traffic anomalies with low-rank tensor autoregression,” IEEE Transactions on Intelligent Transportation Systems, vol. 22, no. 12, pp. 7904–7913, 2021.

[21] R. H. Shumway and D. S. Stoffer, “Arima models,” in Time series analysis and its applications: with R examples. Springer, 2017, pp. 75–163.

[22] M. M. H. Khan, M. Mustafa, M. Hossain, S. Shams, and A. Julius, “Short-term and long-term rainfall forecasting using arima model,” International Journal of Environmental Science and Development, vol. 14, no. 5, pp. 292–298, 2023.

[23] M. K. PK, M. R. Gurram, A. A. Hossain, and F. Amsaad, “Arima-dcgan synergy: A novel adversarial approach to outlier detection in time series data,” in NAECON 2024 – IEEE National Aerospace and Electronics Conference (NAECON). IEEE, 2024, pp. 423–427.

[24] V. I. Kontopoulou, A. D. Panagopoulos, I. Kakkos, and G. K. Matsopoulos, “A review of arima vs. machine learning approaches for time series forecasting in data driven networks,” Future Internet, vol. 15, no. 8, p. 255, 2023.

[25] Y. Jaradat, M. Masoud, A. Manasrah, M. Alia, and I. Jannoud, “Review of data imputation techniques in time series data: Comparative analysis,” The Eurasia Proceedings of Science Technology and Mathematics, vol. 27, pp. 122–129, 2024.

[26] B. Huang, K. Ruan, W. Yu, J. Xiao, R. Xie, and J. Huang, “Odformer: Spatial–temporal transformers for long sequence origin–destination matrix forecasting against cross application scenario,” Expert Systems with Applications, vol. 222, p. 119835, 2023.

[27] K. Xie, Y. Ouyang, X. Wang, G. Xie, K. Li, W. Liang, J. Cao, and J. Wen, “Deep adversarial tensor completion for accurate network traffic measurement,” IEEE/ACM Transactions on Networking, vol. 31, no. 5, pp. 2101–2116, 2023.

[28] X. Yuan, Y. Qiao, Z. Wei, Z. Zhang, M. Li, P. Zhao, R. Hu, and W. Li, “Diffusion models meet network management: Improving traffic matrix analysis with diffusion-based approach,” IEEE Transactions on Network and Service Management, vol. 22, no. 2, pp. 1259–1275, 2025.

[29] W. Cui, P. Wang, and F. Yin, “Dg-stmtl: A novel graph convolutional network for multi-task spatio-temporal traffic forecasting,” Neurocomputing, p. 132421, 2025.

[30] S. Saha, S. Das, and G. H. S. Carvalho, “A hybrid deep learning model for adversarially resilient internet traffic prediction,” Computers and Electrical Engineering, vol. 130, p. 110832, 2026.

[31] J. Lu, X. Yang, Y. Liu, H. Zuo, F. Zhou, T. Yu, D. Liu, T. Deng, and L. Luo, “Transformer-autoencoder-based unsupervised temporal anomaly detection for network traffic with dual prediction and reconstruction,” Applied Sciences, vol. 16, no. 4, p. 2143, 2026.

[32] H. Wang, K. Xie, J. Wen, G. Zhang, W. Liang, G. Xie, and K. Li, “Pettc: Pairwise joint embedding based contrastive tensor completion for network traffic monitoring services,” IEEE Transactions on Services Computing, vol. 18, no. 1, pp. 357–371, 2024.

[33] X. Wu, X. Qiu, Z. Li, Y. Wang, J. Hu, C. Guo, H. Xiong, and B. Yang, “Catch: Channel-aware multivariate time series anomaly detection via frequency patching,” arXiv preprint, vol. abs/2410.12261, 2024. [Online]. Available: https://arxiv.org/abs/2410.12261

[34] Z. Liu, M. Gao, and P. Jiao, “Gcad: Anomaly detection in multivariate time series from the perspective of granger causality,” arXiv preprint, vol. abs/2501.13493, 2025. [Online]. Available: https://arxiv.org/abs/2501.13493

[35] D. Wu, X. Wang, Y. Qiao, Z. Wang, J. Jiang, S. Cui, and F. Wang, “Netllm: Adapting large language models for networking,” in Proceedings of the ACM SIGCOMM 2024 Conference (SIGCOMM), 2024, pp. 661–678.

[36] T. Cui, X. Lin, S. Li, M. Chen, Q. Yin, Q. Li, and K. Xu, “Trafficllm: Enhancing large language models for network traffic analysis with generic traffic representation,” arXiv preprint arXiv:2504.04222, 2025. [Online]. Available: https://arxiv.org/abs/2504.04222

[37] S. Wu, E. Dong, H. He, Z. Wang, D. Han, H. Hu, and J. Yang, “Alm: A two-stage traffic anomaly detection and analysis system via the large language model,” in NOMS 2025-2025 IEEE Network Operations and Management Symposium (NOMS), 2025, pp. 1–7.

[38] Y. Huang, P. Du, R. Li, X. Li, and L. Li, “Met-llm: Enhancing large language models for malicious encrypted traffic detection,” Expert Systems with Applications, p. 130621, 2025.

[39] S. Uhlig, B. Quoitin, J. Lepropre, and S. Balon, “Providing public intradomain traffic matrices to the research community,” ACM SIGCOMM Computer Communication Review, vol. 36, no. 1, pp. 83–86, 2006.

[40] Z. Zheng and M. R. Lyu, “Ws-dream: A distributed reliability assessment mechanism for web services,” in 2008 IEEE International Conference on Dependable Systems and Networks With FTCS and DCC (DSN), 2008, pp. 392–397.

[41] A. Huet, J. M. Navarro, and D. Rossi, “Local evaluation of time series anomaly detection algorithms,” in Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD), 2022, pp. 635–645.

[42] H. Liu, Y. Li, M. Tsang, and Y. Liu, “Costco: A neural tensor completion model for sparse tensors,” in Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (KDD), 2019, pp. 324–334.

[43] H. Chen and J. Li, “Neural tensor model for learning multi-aspect factors in recommender systems,” in Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence (IJCAI), 2020, pp. 2449–2455.

[44] X. Wu, B. Shi, Y. Dong, C. Huang, and N. V. Chawla, “Neural tensor factorization for temporal interaction learning,” in Proceedings of the Twelfth ACM international conference on web search and data mining (WSDM), 2019, pp. 537–545.

[45] Y. Ouyang, K. Xie, X. Wang, J. Wen, and G. Zhang, “Lightweight trilinear pooling based tensor completion for network traffic monitoring,” in IEEE INFOCOM 2022-IEEE Conference on Computer Communications (INFOCOM). IEEE, 2022, pp. 2128–2137.

[46] J. Lu, Y. Sun, and S. Yang, “In-context time series predictor,” in International Conference on Learning Representations (ICLR), vol. 2025, 2025, pp. 79 882–79 908.

[47] X. Zhang, Q. Wang, P. Wang, and W. Wang, “A lightweight sparse interaction network for time series forecasting,” in Proceedings of the AAAI Conference on Artificial Intelligence (AAAI), vol. 39, no. 12, 2025, pp. 13 304–13 312.

[48] F. Lyu, L. Du, Y. Weng, Q. Ying, Z. Xu, W. Zou, H. Wu, X. He, and X. Tang, “Timing is important: Risk-aware fund allocation based on time-series forecasting,” in Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 2 (KDD), 2025, pp. 4694–4704.

[49] Q. Shentu, B. Li, K. Zhao, Y. Shu, Z. Rao, L. Pan, B. Yang, and C. Guo, “Towards a general time series anomaly detector with adaptive bottlenecks and dual adversarial decoders,” in International Conference on Learning Representations (ICLR), 2025.

[50] Q. Zhang and T. Chu, “Structure regularized traffic monitoring for traffic matrix estimation and anomaly detection by link-load measurements,” IEEE Transactions on Instrumentation and Measurement, vol. 65, no. 12, pp. 2797–2807, 2016.
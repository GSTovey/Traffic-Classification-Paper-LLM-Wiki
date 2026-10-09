# PERO: Efficient Robust Post-Training Foundation Models for Encrypted Traffic Classification

Wumei Du <sup>1</sup> Jiarong Wen <sup>1</sup> Kaiyu Zhang <sup>1</sup> Zi Yang <sup>1</sup> Yiqin Lv <sup>1</sup> Longfei Zhang <sup>1</sup> Dong Liang <sup>\*</sup> <sup>1</sup> Zheng Xie <sup>\*</sup> <sup>1</sup>

## Abstract

Encrypted traffic classification is vital for network security, yet real-world deployments are inherently sensitive to rare but high-loss errors such as misclassification of malicious traffic. The encrypted traffic foundation model, as a promising general-purpose technique, can achieve impressive overall performance. However, employing standard objectives such as empirical risk minimization often overlooks high-risk tail events, and commonly used performance metrics hardly reflect robustness limitations in risk-sensitive scenarios. Directly applying robust optimization objectives, such as conditional value-at-risk, to posttraining is computationally prohibitive for large models, as identifying high-loss samples exhausts substantial computation. To this end, we propose Pre-Evaluation Robust Optimization (PERO), an efficient robust post-training framework for encrypted traffic foundation models. PERO employs a lightweight proxy to estimate sample-wise risk and selects a subset of high-risk samples to update the foundation model, decoupling risk estimation from expensive large-model optimization. Extensive experiments on typical encrypted traffic datasets show that PERO achieves competitive or superior robustness and average performance compared to outstanding robust posttraining methods, while significantly reducing computational and memory costs.

## 1. Introduction

In recent years, global Internet usage has surged, driven by advances such as fiber optics, 5G technology, the proliferation of IoT devices, and diverse online services (Tahaei et al., 2020; Wang et al., 2022; Azab et al., 2024; Babaria

## Comparison of Macro and Tail-Risk Performance

![](images/47546823eaf5e49b98416303c98533b8d6e344693873843a005836b4c201f2d9.jpg)  
Figure 1. Performance comparison between ERM and our method under macro and tail evaluation, with macro denoting classaveraged F1-score and α-tail denoting the average F1-score over the worst (1 − α) loss-ranked samples.

et al., 2025). This rapid growth creates both opportunities and challenges for network management, including maintaining quality of service, supporting network planning, and ensuring security (Wei et al., 2022; Ariffin et al., 2025). Encrypted traffic classification, which distinguishes normal and abnormal traffic or identifies application types, has thus become increasingly critical (Pacheco et al., 2019; Lotfollahi et al., 2020; Zheng et al., 2020; Zhang et al., 2023a; Wang et al., 2025b). Misclassifying traffic, particularly when it carries malicious payloads, can lead to undetected breaches and cascading service failures. Consequently, accurate encrypted traffic classification is essential for protecting privacy, maintaining reliable network operations, and enabling timely detection of intrusions and malware (Pacheco et al., 2019; Deldar & Abadi, 2023; Zhang et al., 2023b).

Recent advances in encrypted traffic foundation models have yielded substantial performance improvements (Zhao et al., 2021; 2023; Dong et al., 2025a; Chi et al., 2026). By leveraging self- or weakly supervised pre-training on large-scale unlabeled traffic, models built upon Transformer (Li et al., 2025) and BERT-style architectures acquire rich hierarchical representations that capture both packet-level patterns and long-range flow semantics (Zhao et al., 2022; Lin et al., 2022; Meng et al., 2023; Qu et al., 2024; Zhan et al., 2025;

Shi et al., 2026). These representations can be efficiently adapted to downstream tasks through post-training or finetuning with limited labeled data. Despite these advances, existing post-training procedures predominantly rely on standard empirical risk minimization (ERM) (Shalev-Shwartz & Ben-David, 2014), which prioritizes majority patterns and often overlooks high-risk tail events. As shown in Fig. 1, this bias inflates tail risk and degrades performance on high-loss samples. The resulting disparity between average performance and tail robustness underscores the need for robust post-training optimization.

Existing Challenges in Robust Post-training Encrypted Traffic Foundation Models: Despite the strong empirical performance of encrypted traffic foundation models, achieving robust behavior during post-training remains a fundamental challenge in encrypted traffic classification. Conditional value-at-risk (CVaR) optimization (Rockafellar et al., 2000) offers a principled framework for tail-risk minimization by concentrating updates on the fraction of samples with the highest losses, thereby enhancing robustness. However, directly integrating such robust optimization into the post-training of foundation models introduces several limitations.

Repeated loss evaluations and parameter updates across millions of parameters impose prohibitive time and energy costs, particularly in scenarios requiring frequent or continual post-training (Perez-Jove et al.´ , 2026). Furthermore, memory-limited batch processing restricts exploration of the full loss landscape, resulting in incomplete tail-risk estimation at scale. Together, these constraints render existing robust optimization frameworks ill-suited for high-throughput network environments, motivating the development of scalable post-training methods that mitigate the misclassification of high-risk encrypted traffic without substantial computational and memory overhead.

Developed Method: In this paper, we propose Pre-Evaluation Robust Optimization (PERO), an efficient robust post-training framework for encrypted traffic foundation models under limited computational and memory constraints. Rather than designing a new robust optimization objective, we introduce an efficient mechanism within the CVaR framework that decouples risk estimation from full-model parameter updates, enabling tail-focused posttraining at significantly reduced computational cost. Specifically, PERO employs a lightweight pre-evaluation module to estimate sample-wise risk and selects a high-risk subset of samples for updating the foundation model. The pre-evaluation module is refined online via loss feedback from the foundation model, progressively approximating the underlying risk distribution. By delegating costly sample screening to a lightweight proxy, PERO preserves the ability to prioritize high-risk samples while substantially reducing computational and memory overhead, making robust post-training of encrypted traffic foundation models more practical.

Outline and Primary Contributions: The remainder starts with related work in Section 2. Section 3 introduces notation and preliminaries. Section 4 presents the proposed method. Section 5 reports experimental results, followed by conclusions. Our contributions are threefold:

1. We propose an efficient robust post-training framework that leverages a lightweight pre-evaluation proxy to guide selective optimization of encrypted traffic foundation models, significantly reducing computational overhead.

2. We provide a theoretical analysis of PERO, characterizing post-training convergence behavior and deriving a generalization bound for the pre-evaluation module, offering analytical insight into proxy-guided robust post-training.

3. Extensive experiments on widely used benchmarks demonstrate that our method achieves competitive or superior robustness compared to outstanding robust post-training methods while incurring substantially lower computational and memory costs.

## 2. Related Work

## 2.1. Encrypted Traffic Foundation Models

Foundation models have become increasingly prominent in encrypted traffic classification, driven by advances in deep learning and the success of Transformer-based architectures such as BERT (Dong et al., 2025b). By first pre-training on massive unlabeled datasets to capture transferable representations and then fine-tuning for specific downstream tasks, these models achieve strong performance across diverse network environments.

Early efforts include PERT (He et al., 2020), the first Transformer-based pre-trained model for encrypted traffic, which demonstrated the feasibility of this approach. ET-BERT (Lin et al., 2022) further improves performance by modeling traffic structure and bidirectional payload associations, reaching over 97% accuracy across seven tasks. Building on these foundations, subsequent work addressed architectural and modeling limitations of ET-BERT, leading to specialized designs such as Flow-MAE (Hang et al., 2023), YaTC (Zhao et al., 2023), MTC-MAE (Xu et al., 2024), TrafficFormer (Zhou et al., 2025), and CETP (Lin et al., 2024). In parallel, generative pre-training has led to NetGPT (Meng et al., 2023), TrafficGPT (Qu et al., 2024), and the encoder-decoder-based Lens (Wang et al., 2024a), while NetMamba (Wang et al., 2024b) replaced the Transformer with an optimized Mamba architecture for efficient online classification. More recently, MIETT (Chen et al., 2025) introduces a two-level attention transformer to jointly capture intra-packet and inter-packet dependencies, outperforming prior token-centric foundation models on multiple benchmarks.

Despite their strong overall performance, these models are typically optimized with standard empirical objectives that underemphasize rare high-loss samples, while robust optimization during post-training remains prohibitively costly at this scale.

## 2.2. Robust Optimization for Large-Scale Models

Robust optimization has evolved from foundational theory to widely used methods in machine learning, aiming to train models that are reliable not only on average but also under worst-case conditions. Typical approaches are rooted in the distributionally robust optimization (DRO) framework, which addresses uncertainty in data distributions and was originally formalized with convex uncertainty and momentbased ambiguity sets (Ben-Tal & Nemirovski, 1998; 2002; Delage & Ye, 2010; Wiesemann et al., 2014; Zou et al., 2025). Representative methods include CVaR optimization (Rockafellar et al., 2000; Wang et al., 2023; Lv et al., 2024; Wang et al., 2026; Qu et al., 2025; Wang et al., 2025a), GroupDRO (Sagawa et al., 2020), and recent LogSumExpbased DRO formulations such as TDRO (Gladin et al., 2026). CVaR optimization minimizes the expected loss in the worstperforming tail of the data distribution, providing robustness to high-risk events. GroupDRO focuses on ensuring uniform accuracy across predefined subpopulations, thereby preventing the model from overfitting to the majority groups while neglecting minority groups. TDRO uses a smooth LogSum-Exp surrogate to emphasize high-loss samples and improve tractability in stochastic optimization. Related hard-sample mining strategies also aim to focus training on difficult examples. For example, online hard task mining (OHTM) (Kumar et al., 2023) maintains a buffer to store past difficult data points and integrates them into the training pipeline. By emphasizing worst-case performance, robust optimization offers a principled way to improve reliability when standard ERM underperforms.

In post-training large foundation models, CVaR incurs substantial computational and memory overhead from repeated tail-loss estimation and re-optimization, while memorylimited batching further degrades tail-risk estimation at scale. GroupDRO relies on predefined and often static group structures that may be misaligned with evolving or latent risk patterns, limiting its robustness in large-scale settings. TDRO’s scalability to budget-limited foundation-model post-training remains unexplored. OHTM heuristically selects high-loss samples without explicit tail-risk modeling and exhibits unstable behavior under nonstationarity.

## 3. Preliminary

## 3.1. Notations

Let $\mathbf { x } \in \mathcal { X }$ denote an input sample used for classification, and let $y \in \mathcal { V }$ be its corresponding label. The classification model is parameterized by $\theta \in \Theta$ , while the underlying data distribution is denoted by $p ( \mathbf { x } , y )$ . We consider a dataset $\mathcal { D } = \{ ( \mathbf { x } ^ { ( i ) } , y ^ { ( i ) } ) \} _ { i = 1 } ^ { N }$ with $N$ training sample pairs. The objective of encrypted traffic classification is to learn a mapping $f _ { \theta } : \mathcal { X }  \mathcal { Y }$ that minimizes classification errors, typically expressed as $\mathbb { E } _ { p ( \mathbf { x } , y ) } \left[ \mathbb { 1 } _ { \{ f _ { \theta } ( \mathbf { x } ) \neq y \} } \right]$ , where $\mathbb { 1 } _ { \{ \cdot \} }$ is the indicator function. For optimization, we adopt the cross-entropy loss, denoted by $\ell ( \cdot , \cdot )$ , and write

$$
\ell = \ell ( f _ { \pmb \theta } ( \mathbf x ) , y ) , \quad \ell ^ { ( i ) } = \ell ( f _ { \pmb \theta } ( \mathbf x ^ { ( i ) } ) , y ^ { ( i ) } ) ,
$$

where $\ell$ is the loss for a generic sample pair $\left( \mathbf { x } , y \right)$ , and $\ell ^ { ( i ) }$ is the loss for the i-th training sample pair in $\mathcal { D }$

## 3.2. ERM and Robust Optimization Methods

Empirical Risk Minimization (ERM) ERM is the standard principle for supervised learning, aiming to find a predictor that minimizes expected loss under the true data distribution $p ( \mathbf { x } , y )$ (Shalev-Shwartz $\&$ Ben-David, 2014). Since $p ( \mathbf { x } , y )$ is unknown, ERM minimizes the loss under the empirical distribution $\hat { p }$ induced by the training data:

$$
\operatorname* { m i n } _ { \pmb { \theta } \in \Theta } \mathbb { E } _ { \hat { p } ( \mathbf { x } , y ) } \big [ \ell \big ] = \operatorname* { m i n } _ { \pmb { \theta } \in \Theta } \frac { 1 } { N } \sum _ { i = 1 } ^ { N } \ell ^ { ( i ) } .\tag{1}
$$

Conditional Value-at-Risk (CVaR) CVaR focuses on the upper tail of the loss distribution. For a risk level $\alpha \in ( 0 , 1 )$ $\mathrm { e . g . , } \alpha = 0 . 9 $ , corresponding to the worst 10% of cases, it minimizes the expected loss among the worst-performing $( 1 - \alpha )$ fraction of samples (Rockafellar et al., 2000; Rockafellar & Uryasev, 2002):

$$
\operatorname* { m i n } _ { \eta \in \mathbb { R } } \eta + \frac { 1 } { 1 - \alpha } \mathbb { E } \big [ ( \ell - \eta ) _ { + } \big ] ,\tag{2}
$$

where $( a ) _ { + } = \operatorname* { m a x } ( a , 0 )$ , and $\eta$ approximates the Value-at-Risk(VaR) threshold. For large-scale applications, CVaR is commonly optimized using Monte Carlo-based stochastic approximation (Tamar et al., 2015), which we refer to as MC-CVaR for brevity. Specifically, given a mini-batch $\{ ( \mathbf { x } ^ { ( i ) } , y ^ { ( i ) } ) \} _ { i = 1 } ^ { B }$ with losses $\ell ^ { ( i ) }$ , the stochastic subgradient of $\mathrm { C V a R } _ { \alpha }$ with respect to $\pmb \theta$ is estimated as:

$$
\nabla _ { \theta } \mathrm { C V a R } _ { \alpha } \approx \frac { 1 } { ( 1 - \alpha ) B } \sum _ { i = 1 } ^ { B } \mathbb { 1 } _ { \{ \ell ^ { ( i ) } > \eta \} } \nabla _ { \theta } \ell ^ { ( i ) } ,\tag{3}
$$

with the threshold $\eta$ iteratively updated to approximate the α-quantile of the loss distribution.

Group Distributionally Robust Optimization (Group-DRO) GroupDRO aims to learn model parameters θ that minimize the maximum group-wise expected loss (Sagawa et al., 2020). Given a dataset split into G groups $\mathcal { D } =$ $\begin{array} { r } { \bigcup _ { g = 1 } ^ { G } \mathcal { D } _ { g } , } \end{array}$ where each group g indexes a subpopulation, $\mathrm { e . g . }$ application types, GroupDRO solves the min-max problem:

$$
\operatorname* { m i n } _ { \theta } \operatorname* { m a x } _ { g \in \left[ G \right] } \mathbb { E } _ { ( x , y ) \sim \mathcal { D } _ { g } } \left[ \ell \right] ,\tag{4}
$$

where the inner maximum seeks the group with the highest expected loss, focusing on the worst-performing subpopulation.

## 3.3. From ERM to Robust Post-training

Given a large-scale pre-trained foundation model $f _ { \theta }$ and a downstream encrypted traffic classification task defined by the data distribution $p _ { \mathrm { t a s k } } ( \mathbf { x } , y )$ , the post-training stage adapts the model parameters θ to the target task using a labeled dataset

$$
\begin{array} { r } { \mathcal { D } _ { \mathrm { t a s k } } = \{ ( \mathbf { x } ^ { ( i ) } , y ^ { ( i ) } ) \} _ { i = 1 } ^ { N } , \quad ( \mathbf { x } ^ { ( i ) } , y ^ { ( i ) } ) \sim p _ { \mathrm { t a s k } } ( \mathbf { x } , y ) . } \end{array}
$$

The standard post-training objective follows ERM, as shown in Eq. (1), and is typically optimized via stochastic gradient descent. ERM effectively adapts pre-trained representations when the training data $\mathcal { D } _ { \mathrm { t a s k } }$ is representative of the target distribution. However, this assumption is often violated in encrypted traffic classification, where high-risk traffic examples are significantly underrepresented. As a result, ERM disproportionately favors majority patterns, leading to severe performance degradation on high-risk tail examples. These limitations motivate robust post-training objectives that explicitly account for tail risk, aiming to ensure reliable classification performance even in high-risk traffic scenarios.

## 4. Method

Robust post-training of encrypted traffic foundation models incurs substantial computational overhead. Identifying highrisk samples typically requires full-model inference on large candidate batches, a process rendered prohibitively expensive by the model’s scale and complexity. To address this challenge, we propose Pre-Evaluation Robust Optimization (PERO), a resource-efficient framework for scalable robust post-training.

## 4.1. Overall Framework of PERO

PERO approximates robust post-training by using a lightweight proxy to guide selective optimization of the foundation model. We study encrypted traffic classification as a representative application because it is risk-sensitive, and robust post-training of large models incurs substantial computational overhead. The framework consists of a preevaluation module for risk estimation and a subset selection module that identifies risk-informative samples for updating the large classifier. The overall learning pipeline proceeds as follows (see Fig. 2): (i) the pre-evaluation module is updated using sample-wise losses from the previous iteration to approximate the classifier’s current loss landscape; (ii) the module predicts losses for a candidate pool of size B<sup>ˆ</sup> and identifies samples likely to contribute to tail risk; (iii) the subset selection module selects the B samples $( B < { \hat { B } } )$ with the highest predicted risk scores from the pool at each iteration to update the classifier.

## 4.2. Pre-Evaluation Module Formulation

The pre-evaluation module works as an online surrogate risk estimator that predicts sample-wise classification risk under the current model state. The module takes in the sample and aims to predict the cross-entropy loss induced by the evolving classifier, approximating the loss mapping $f : \Theta \times \mathcal { X } \to \mathbb { R } _ { + }$ , which evolves as the classifier parameters θ are updated iteratively. As cross-entropy reflects both prediction error and classifier confidence, the predicted loss serves as a principled proxy for the instantaneous risk and reveals sample-level uncertainty. This formulation casts pre-evaluation as a supervised learning problem that is intrinsically entangled with the main classifier’s training dynamics. Consequently, loss prediction is non-trivial, as the continual updates to θ create a non-stationary and evolving risk landscape.

We formulate the pre-evaluation module as a lightweight neural network $g : \Phi \times \mathcal { X } \to \mathbb { R } _ { + }$ , parameterized by $\phi \in \Phi$ and updated iteratively. Let $( \hat { \mathbf { x } } _ { t } ^ { ( i ) } , \hat { y } _ { t } ^ { ( i ) } ) \in \mathcal { X } \times \mathcal { Y }$ denote the i-th sample pair of the batch chosen at iteration t. The module $g _ { \phi _ { t } }$ takes a sample $\hat { \mathbf { x } } _ { t } ^ { ( i ) } \in \mathcal { X }$ as input and outputs an estimated loss value $\hat { g } _ { t } ^ { ( i ) }$ . Formally,

$$
\begin{array} { r } { g : \Phi \times \mathcal { X }  \mathbb { R } , \quad ( \phi _ { t } , \hat { \mathbf { x } } _ { t } ^ { ( i ) } ) \mapsto \hat { g } _ { t } ^ { ( i ) } : = g _ { \phi _ { t } } ( \hat { \mathbf { x } } _ { t } ^ { ( i ) } ) , } \end{array}
$$

where $\hat { g } _ { t } ^ { ( i ) }$ serves as an estimate of the true cross-entropy loss $\hat { \ell } _ { t } ^ { ( i ) } : = \ell ( f _ { \pmb { \theta } _ { t - 1 } } ( \hat { \mathbf { x } } _ { t } ^ { ( i ) } ) , \hat { y } _ { t } ^ { ( i ) } )$ that $( \hat { \mathbf x } _ { t } ^ { ( i ) } , \hat { y } _ { t } ^ { ( i ) } )$ would incur under the classifier parameters $\pmb { \theta } _ { t - 1 }$ . This mechanism facilitates exploration by highlighting samples with higher prediction risk, often located in regions of uncertainty or tail risk, thereby guiding the classifier to improve robustness under worst-case scenarios.

The pre-evaluation module is trained in a supervised manner to approximate the sample-wise classification loss. At iteration t, the classifier $f _ { \theta _ { t - 1 } }$ yields the true losses for a batch $\{ ( \mathbf { x } _ { t } ^ { ( i ) } , y _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { B } ;$

$$
\ell _ { t } ^ { ( i ) } : = \ell ( f _ { \theta _ { t - 1 } } ( \mathbf { x } _ { t } ^ { ( i ) } ) , y _ { t } ^ { ( i ) } ) , \quad i = 1 , \cdot \cdot \cdot , B .
$$

The module parameters $\phi _ { t }$ are updated online by mini-

![](images/27806482a3aabf3b787a24b477b18bfb28ef0fe70cf76fe78946e768473d233c.jpg)  
a. Pre-Evaluation for Online Subset Selection Pipeline for Post-training a Large Classifier

![](images/7c84de099dc6b8498ef308402b6e9ca2145189dce7cd510eca550dbb0b126fb9.jpg)  
b. Pre-Evaluation for Iterative Batch Selection  
Figure 2. Overview of PERO Framework. Panel (a) shows the optimization loop with the pre-evaluation module $\phi ,$ subset selection module, and classifier θ, with $\left| \phi \right| \ll \left| \theta \right|$ . Panel (b) depicts iterative batch selection guided by the pre-evaluation module.

mizing the mean squared error (MSE) between predictions $g _ { t } ^ { ( i ) } : = g _ { \phi _ { t } } ( \mathbf { x } _ { t } ^ { ( i ) } )$ and true losses $\ell _ { t } ^ { ( i ) }$ via gradient descent with a learning rate $\gamma _ { \phi } \mathrm { : }$

$$
\mathcal { L } _ { \mathrm { M S E } } ( \phi _ { t } ) = \frac { 1 } { B } \sum _ { i = 1 } ^ { B } \left[ g _ { t } ^ { ( i ) } - \ell _ { t } ^ { ( i ) } \right] ^ { 2 } , \phi _ { t + 1 } = \phi _ { t } - \gamma _ { \phi } \nabla _ { \phi } \mathcal { L } _ { \mathrm { M S E } } ( \phi _ { t }\tag{5}
$$

Through this iterative online optimization, the preevaluation module progressively learns a mapping from input samples to their expected classification difficulty under the evolving model state.

## 4.3. Pre-Evaluation for Online Subset Selection

To improve robustness while reducing computational cost, the subset selection module selects critical samples online at each iteration to update the large classifier. Each training batch is expanded into a candidate pool of size $\hat { B } > B$ . The pre-evaluation module predicts loss estimates for all candidates, which are then used to select a subset of $B$ samples with the highest potential to improve classifier performance in uncertain or high-risk regions of the data space.

Formally, let $\{ \hat { \mathbf { x } } _ { t } ^ { ( i ) } \} _ { i = 1 } ^ { \hat { B } }$ denote the candidate samples at iteration t. The pre-evaluation module outputs a prediction $\hat { g } _ { t } ^ { ( i ) } = g _ { \phi _ { t } } ( \hat { \mathbf { x } } _ { t } ^ { ( i ) } )$ , which is then assigned an acquisition score $a _ { t } ^ { ( i ) }$ that quantifies its informativeness or difficulty relative to the current classifier $f _ { \pmb { \theta } _ { t - 1 } } .$ . We introduce a binary indicator vector $\mathbf { z } _ { t } = [ z _ { t } ^ { ( 1 ) } , \ldots , z _ { t } ^ { ( \hat { B } ) } ] ^ { \top } \in \{ 0 , 1 \} ^ { \hat { B } }$ , where $\begin{array} { r } { \dot { z } _ { t } ^ { ( i ) } = 1 } \end{array}$ indicates that the candidate $\hat { \mathbf { x } } _ { t } ^ { ( i ) }$ is selected, and $z _ { t } ^ { ( i ) } = 0$ indicates that it is not. From a general perspective, the subset selection at iteration t can be formulated as a constrained set-function maximization problem:

$$
\begin{array} { r l } { \underset { \mathbf { z } _ { t } \in \{ 0 , 1 \} ^ { \hat { B } } } { \operatorname* { m a x } } } &  \displaystyle \mathcal { A } ( \mathbf { z } _ { t } ) = \underset { \mathrm { U i l i l y } } { \sum _ { i = 1 } ^ { \hat { B } } } z _ { t } ^ { ( i ) } \cdot a _ { t } ^ { ( i ) } + \lambda \cdot \underset { \mathrm { S e t - l e v e l ~ B o n u s } } { \underbrace { \underbrace { S ( \{ z _ { t } ^ { ( i ) } \hat { \mathbf { x } } _ { t } ^ { ( i ) } \} \} _ { i = 1 } ^ { \hat { B } } ) } } } \\ { \mathrm { s . t . } } & { \displaystyle \sum _ { i = 1 } ^ { \hat { B } } z _ { t } ^ { ( i ) } \cdot c _ { t } ^ { ( i ) } \leq C , \quad z _ { t } ^ { ( i ) } \in \{ 0 , 1 \} . } \end{array}\tag{6}
$$

Here, ${ \cal S } ( \{ z _ { t } ^ { ( i ) } \hat { \mathbf { x } } _ { t } ^ { ( i ) } \} _ { i = 1 } ^ { \hat { B } } )$ captures additional set-level incentives such as the coverage measure of $\mathcal { X }$ space, λ controls the trade-off between utility and bonus, $c _ { t } ^ { ( i ) }$ denotes the cost of the i-th sample used for modeling resource constraints, and $C$ represents the total resource budget per optimization iteration during post-training.

The subset selection strategy in PERO is an efficient instantiation of the general formulation. Since all preprocessed samples have uniform processing cost, we set $c _ { t } ^ { ( i ) } = 1$ and enforce $\begin{array} { r } { \sum _ { i = 1 } ^ { \hat { B } } z _ { t } ^ { ( i ) } = B } \end{array}$ . To avoid solving a complicated robust optimization problem, we set $\lambda = 0$ , reducing the objective to top-B selection by acquisition score. Meanwhile, PERO uses the predicted loss $\hat { g } _ { t } ^ { ( i ) }$ from the pre-evaluation module as the acquisition score $a _ { t } ^ { ( i ) }$ . Since cross-entropy loss reflects predictive uncertainty and worstcase risk, higher predicted losses correspond to samples that are more likely to lie in uncertain or underexplored regions of the input space. By prioritizing these examples, PERO selects $\bar { S } _ { t } ^ { B } = \arg \operatorname* { m a x } _ { \mathbf { z } _ { t } } \mathcal { A } ( \mathbf { z } _ { t } )$ and focuses post-training on challenging samples while maintaining computational efficiency.

Empirically, this straightforward top-B criterion yields substantial robustness gains and consistently outperforms alternative robust optimization methods with minimal overhead. Our results show that effective robust optimization can be achieved without resorting to complex subset selection objectives. The framework is also flexible, allowing more sophisticated selection criteria to be explored in future work.

## 4.4. Algorithm Overview

Building on the subset selection mechanism described above, the optimization restricts parameter updates to the selected high-risk subset. At iteration t, we perform a standard stochastic gradient descent step on the selected subset $S _ { t } ^ { B } = \{ ( \mathbf { x } _ { t } ^ { ( i ) } , y _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { B }$ to update the classifier parameters from $\pmb { \theta } _ { t - 1 }$ to $\pmb \theta _ { t } \mathbf { : }$

$$
\pmb { \theta } _ { t } = \pmb { \theta } _ { t - 1 } - \frac { \gamma _ { \theta } } { B } \sum _ { i = 1 } ^ { B } \nabla _ { \pmb { \theta } } \ell _ { t } ^ { ( i ) } ,\tag{7}
$$

where $\gamma _ { \theta }$ is the learning rate. This update concentrates optimization on high-risk samples while avoiding full-batch updates. The complete training procedure is summarized in Algorithm 1.

## 4.5. Theoretical Analysis

We provide a theoretical analysis of PERO under simplifying assumptions, focusing on (i) the convergence behavior of the proposed post-training procedure and (ii) a generalization bound for the pre-evaluation module. The results provide analytical insight into proxy-guided post-training rather than a full characterization of nonconvex foundationmodel optimization. Full proofs are provided in the online supplement.<sup>1</sup>

Algorithm 1 Pre-Evaluation Subset Selection in the Post-  
Training of a Large Pre-Trained Classifier   
1: Input: Task dataset $\mathcal { D } _ { \mathrm { t a s k } } ;$ pre-trained classifier $f _ { \pmb { \theta } _ { 0 } }$   
iterations $T ;$ batch size $B ;$ candidate batch size ${ \hat { B } } ;$ learn  
ing rates $\gamma _ { \phi } , \gamma _ { \theta } .$   
2: Output: Optimized classifier $f _ { \pmb { \theta } _ { T } }$   
3: Initialize pre-evaluation module $g _ { \phi _ { 0 } } .$   
4: Randomly sample an initial batch $\{ ( \mathbf { x } _ { 0 } ^ { ( i ) } , y _ { 0 } ^ { ( i ) } ) \} _ { i = 1 } ^ { B } \sim$   
$\mathcal { D } _ { \mathrm { t a s k } } .$   
5: Compute initial losses $\{ \ell _ { 0 } ^ { ( i ) } : = \ell ( f _ { \pmb { \theta } _ { 0 } } ( \mathbf { x } _ { 0 } ^ { ( i ) } ) , y _ { 0 } ^ { ( i ) } ) \} _ { i = 1 } ^ { B }$   
and pre-evaluation module predictions $\begin{array} { r l } { \{ g _ { 0 } ^ { ( i ) } } & { { } : = } \end{array}$   
$g _ { \phi _ { 0 } } ( \mathbf { x } _ { 0 } ^ { ( i ) } ) \} _ { i = 1 } ^ { B }$   
6: for $t = 1 : T$ do   
7: // Pre-Evaluation Module Online Update   
8: Update $\phi _ { t }$ from $\phi _ { t - 1 }$ using $\{ \ell _ { t - 1 } ^ { ( i ) } , g _ { t - 1 } ^ { ( i ) } \} _ { i = 1 } ^ { B }$ via   
$\operatorname { E q . } ( 5 ) \colon$   
$\phi _ { t }  \phi _ { t - 1 } - \gamma _ { \phi } \nabla _ { \phi } \mathcal { L } _ { \mathrm { M S E } } ( \phi _ { t - 1 } ) .$   
9: //Active Subset Selection   
10: Randomly sample a candidate batch   
$\{ ( \hat { \mathbf { x } } _ { t } ^ { ( i ) } , \hat { y } _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { \hat { B } } \sim \mathcal { D } _ { \mathrm { t a s k } } .$   
11: Predict losses: $\hat { g } _ { t } ^ { ( i ) } = g _ { \phi _ { t } } ( \hat { \mathbf { x } } _ { t } ^ { ( i ) } ) , \forall i \in \{ 1 , \dots , \hat { B } \}$   
12: Assign acquisition scores: $a _ { t } ^ { ( i ) } ~  ~ \hat { g } _ { t } ^ { ( i ) } , \forall i \in$   
$\{ 1 , \ldots , \hat { B } \}$   
13: Select the top-B samples with the largest $a _ { t } ^ { ( i ) }$ to form   
$S _ { t } ^ { B } = \{ ( \mathbf { x } _ { t } ^ { ( i ) } , y _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { B } .$   
14: // Loss Evaluation and Foundation Model Update   
15: Compute true losses: $\begin{array} { r l } { \{ \ell _ { t } ^ { ( i ) } } & { { } \mathrel { \mathop : } = } \end{array}$   
$\begin{array} { r } { \ell ( f _ { \pmb { \theta } _ { t - 1 } } ( \mathbf x _ { t } ^ { ( i ) } ) , y _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { B } . } \end{array}$   
16: Record module predictions $\{ g _ { t } ^ { ( i ) } : = g _ { \phi _ { t } } ( \mathbf { x } _ { t } ^ { ( i ) } ) \} _ { i = 1 } ^ { B } ,$   
17: Update the classifier parameters on $S _ { t } ^ { B }$ via Eq.(7):   
$\pmb \theta _ { t }  \pmb \theta _ { t - 1 } - \frac { \gamma _ { \theta } } B \sum _ { i = 1 } ^ { B } \nabla _ { \pmb \theta } \ell _ { t } ^ { ( i ) } .$   
18: end for

Preliminaries and Assumptions. We adopt the notation from Section 3.1 and assume access to n i.i.d. samples $\{ ( \mathbf { x } _ { i } , y _ { i } ) \} _ { i = 1 } ^ { n }$ drawn from the distribution $p ( \mathbf { x } , y )$ . To analyze the convergence of the coupled updates $\{ \theta _ { t } , \phi _ { t } \} _ { t }$ and the generalization bound of the pre-evaluation module, we impose the following assumptions on the functions $\ell ( f _ { \pmb { \theta } } ( \mathbf { x } ) , y )$ and $g _ { \phi } ( \mathbf { x } )$

Assumption 1 (Bounded Loss). $\ell ( f _ { \pmb { \theta } } ( \mathbf { x } ) , y )$ is uniformly bounded: $\ell ( f _ { \pmb \theta } ( \mathbf x ) , y ) \le L _ { \mathrm { m a x } }$ for all $\left( \mathbf { x } , y \right)$

Assumption 2 (Bounded Spectral Radius). $\ell ( f _ { \pmb { \theta } } ( \mathbf x ) , y )$ is twice continuously differentiable with respect to θ, and its Hessian satisfies $\dot { \lambda } _ { \mathrm { m a x } } \big ( \nabla _ { \pmb { \theta } \pmb { \theta } } ^ { 2 } \ell ( f _ { \pmb { \theta } } ( \mathbf { x } ) , y ) \big ) \dot { \leq } 1$ for all $\left( \mathbf { x } , y \right)$ Assumption 3 (Lipschitz Continuity). $g _ { \phi } ( \mathbf { x } )$ is Lipschitz continuous with respect to $\phi ,$ i.e., $| g _ { \phi _ { 1 } } ( \mathbf { x } ) - g _ { \phi _ { 2 } } ( \mathbf { x } ) | \ \leq$ $L \| \phi _ { 1 } - \phi _ { 2 } \| _ { 2 }$ for all x and some constant $L > 0$

Convergence Analysis. Building on the above assumptions, we analyze the convergence of the proposed post-training procedure. Theorem 4.1 shows that, under mild conditions, the parameter sequence $\{ \theta _ { t } , \phi _ { t } \} _ { i }$ converges to a stationary point.

Theorem 4.1 (Convergence to Stationary Points). Under Assumptions $1 , 2$ and 3, suppose that the prediction error holds: $g _ { \phi } ( \mathbf { x } ^ { ( i ) } ) - \ell ^ { ( i ) } < \delta ,$ ∀i for a constant $\delta > 0 ,$ and that the spectral radius of $\nabla _ { \phi \phi } ^ { 2 } g ( \mathbf { x } )$ is bounded $\begin{array} { r } { b y \frac 1 \delta \left( \frac 1 2 - L ^ { 2 } \right) } \end{array}$ Then, the sequence $\{ \theta _ { t } , \dot { \phi _ { t } } \} _ { t }$ converges to a stationary point $( \theta ^ { * } , \phi ^ { * } )$

We note that Theorem 4.1 relies on a uniformly bounded loss-Hessian spectral radius throughout optimization. This is a standard smoothness condition widely used in convergence analyses of gradient-based methods (Hu et al., 2023), although its global validity can be restrictive for large Transformer models. Accordingly, we use this assumption to obtain a tractable analytical characterization of the coupled update dynamics, and interpret Theorem 4.1 as an insight under explicit assumptions rather than a complete description of practical nonconvex optimization.

Generalization Bound. Denote by $R ( \theta ^ { * } , \phi ^ { * } )$ the expectation $\mathbb { E } _ { p ( \mathbf { x } , y ) } [ \ell ] ,$ , and let $\begin{array} { r } { \widehat { R } ( \pmb { \theta } ^ { * } , \pmb { \phi } ^ { * } ) = \frac { 1 } { \hat { B } } \sum _ { i = 1 } ^ { \hat { B } } z ^ { ( i ) } \ell ^ { ( i ) } } \end{array}$ and $\begin{array} { r } { \widetilde { R } ( \pmb { \theta } ^ { * } ) = \frac { 1 } { \hat { R } } \sum _ { i = 1 } ^ { \hat { B } } \ell ^ { ( i ) } } \end{array}$ . Theorem 4.2 addresses the following key question regarding generalization: How well does the learned risk estimator perform on unseen data?

Theorem 4.2 (Generalization Bound for the Pre-Evaluation Module). Under Assumption 1, thefollowing generalization bound holds with a probability of at least $1 - \epsilon f o r$ any $\epsilon \in ( 0 , 1 )$

$$
\begin{array} { r l } & { \Big | R ( \theta ^ { * } , \phi ^ { * } ) - \widehat { R } ( \theta ^ { * } , \phi ^ { * } ) \Big | < \sqrt { \left( \mathbb { V } [ \ell ] + \frac { L _ { \operatorname* { m a x } } } { 3 } \right) \frac { 2 \ln \left( \frac { 1 } { \epsilon } \right) } { \hat { B } } } } \\ & { \qquad + L _ { \operatorname* { m a x } } \sqrt { \frac { \hat { B } } { 2 B ^ { 2 } } \ln \left( \frac { 1 } { \epsilon } \right) } } \\ & { \qquad + \frac { L _ { \operatorname* { m a x } } \left( \hat { B } - B \right) } { \hat { B } } . } \end{array}
$$

with $\mathbb { V } [ \cdot ]$ denoting variance and $L _ { \mathrm { m a x } }$ as in Assumption 1.

In conjunction with the confidence ϵ and a sufficiently large candidate batch ${ \hat { B } } ,$ Theorem 4.2 reveals the generalization bound given the learned parameters $( \theta ^ { * } , \phi ^ { * } )$ . It is also associated with the variance $\mathbb { V } _ { \tau _ { i } \sim p _ { \alpha } ( \tau ) } [ \ell ( f _ { \pmb { \theta } ^ { * } } ( \mathbf { x } ) , y ) ]$ . This bound establishes a worst-case generalization guarantee under standard i.i.d. assumptions, and serves as a theoretical upper envelope for the non-stationary iterative process, ensuring the proxy’s selection error remains bounded.

## 4.6. Computational Complexity Analysis

We analyze the per-iteration computational complexity of PERO relative to ERM and MC-CVaR. Let $\mathcal { C } _ { f }$ and $\mathcal { C } _ { f } ^ { \mathrm { f w d } }$ denote the forward-backward and inference costs of the foundation model $f _ { \theta }$ , and similarly $\mathcal { C } _ { g } , \mathcal { C } _ { g } ^ { \mathrm { f w d } }$ for the preevaluation module $g _ { \phi }$ , with $\mathcal { C } _ { g } \ll \mathcal { C } _ { f }$

Table 1 summarizes the per-iteration complexity. ERM is most efficient but not robust, whereas MC-CVaR introduces a costly ${ \mathcal { O } } ( { \hat { B } } { \cdot } { \mathcal { C } } _ { f } ^ { \mathrm { f w d } } )$ large-model screening bottleneck. PERO mitigates this bottleneck by delegating sample selection to a lightweight proxy. Since ranking is negligible and $\mathcal { C } _ { g } , \mathcal { C } _ { g } ^ { \mathrm { f w \bar { d } } } \ll \mathcal { C } _ { f }$ , PERO achieves robust screening with computational overhead close to ERM.

Table 1. Per-iteration computational complexity.
<table><tr><td>Method</td><td>Computational Complexity</td></tr><tr><td>ERM</td><td> $\mathcal { O } ( B \cdot { \mathcal { C } } _ { f } )$ </td></tr><tr><td>MC-CVaR</td><td> $\mathcal { O } ( B \cdot \mathcal { C } _ { f } + \hat { B } \cdot \mathcal { C } _ { f } ^ { \mathrm { f w d } } )$ </td></tr><tr><td>PERO (Ours)</td><td> $\mathcal { O } ( B \cdot \mathcal { C } _ { f } + \hat { B } \cdot \mathcal { C } _ { g } ^ { \mathrm { f w d } } + B \cdot \mathcal { C } _ { g } )$ </td></tr></table>

## 5. Experimental Results and Analysis

In this section, we conduct extensive experiments on four typical encrypted traffic classification datasets (Section 5.1) to evaluate the effectiveness, robustness, and efficiency of PERO. We compare PERO with representative robust posttraining and sample-selection baselines (Section 5.2), examine the risk prediction fidelity of the pre-evaluation module (Section 5.3), and perform ablation studies to assess the impact of key hyper-parameters (Section 5.4).

## 5.1. Experimental setting

Datasets. Three commonly used benchmark datasets are employed to evaluate the effectiveness and robustness of PERO: USTC-TFC (Wang et al., 2017), ISCX-VPN-Service (Gil et al., 2016), and ISCX-VPN-App (Gil et al., 2016). Further details can be found in Appendix B.

Evaluation Metrics. We utilize four standard metrics to evaluate the performance of our method: Accuracy (AC), Precision (PR), Recall (RC), and F1-score (F1) (Telikani et al., 2021; Zhang et al., 2023b; Azab et al., 2024; Chi et al., 2024b). Accuracy is reported at the sample level, while Precision, Recall, and F1-score are macro-averaged across classes. To assess robustness, we further evaluate all metrics on the $( 1 - \alpha )$ tail subset identified by the $\mathrm { C V a R } _ { \alpha }$ criterion, yielding tail-conditional scores denoted as $\mathsf { A C } _ { \alpha }$ $\mathrm { P R } _ { \alpha } , \mathrm { R C } _ { \alpha }$ , and $\mathrm { F } 1 _ { \alpha }$ . Higher values indicate better classification performance.

Implementation Details. We adopt ET-BERT (Lin et al., 2022) as the backbone and implement the pre-evaluation module as a lightweight MLP for efficient risk estimation. To validate the generality across backbones, we further evaluate PERO with YaTC (Zhao et al., 2023). Detailed architectural configurations and implementation settings are provided in Appendix C.

## 5.2. Comparison with Baseline Methods

We compare PERO with representative baselines spanning standard training, sample selection, loss reweighting, and robust post-training: ERM (Shalev-Shwartz & Ben-David, 2014), Random Selection, Focal Loss (Lin et al., 2017), MC-CVaR (Rockafellar et al., 2000), GroupDRO (Sagawa et al., 2020), OHTM (Kumar et al., 2023), and TDRO (Gladin et al., 2026). Baseline details are provided in Appendix C. The main ET-BERT results on the three benchmarks are shown in Figs. 3–4 and Tables 2–4. Additional YaTC results are reported in Appendix D.

Overall and Tail Performance Comparison. Fig. 3 compares the accuracy of different methods across three benchmarks. Although all methods achieve strong overall accuracy, their performance drops on the $( 1 - \alpha )$ tail-risk subset, with larger degradation as α increases from 0.7 to 0.9. PERO and MC-CVaR consistently achieve the strongest overall and tail-conditioned accuracy, clearly outperforming the other baselines. At $\alpha = 0 . 9$ , PERO slightly outperforms MC-CVaR on USTC-TFC and shows a clearer advantage on ISCX-VPN-Service, while the two methods are nearly indistinguishable on ISCX-VPN-App. Tail degradation is most pronounced on USTC-TFC, where baselines such as ERM, Random, Focal, TDRO, and GroupDRO drop sharply under extreme risk. By contrast, PERO effectively mitigates tail degradation and achieves the highest $\mathrm { A C _ { 0 . 9 } }$ across all three datasets.

![](images/339fec25de76573081a43d65681b6a11d4dbeb4f83d48cd3ca37215d7591d3f7.jpg)  
Figure 3. Comparison of accuracy results across different datasets using various methods.

Tables 2-3 report overall and (1 − 0.9)-tail-conditioned accuracy, macro precision, macro recall, and macro F1- score. Consistent with Fig. 3, PERO achieves superior or competitive performance across all datasets, especially under tail-conditioned metrics. On ISCX-VPN-Service, PERO achieves the best $\mathrm { F 1 _ { 0 . 9 } }$ and improves over ERM, Random, Focal, OHTM, GroupDRO, TDRO, and MC-CVaR by 18.42%, 24.82%, 21.64%, 13.43%, 25.08%, 24.30%, and 7.29%, respectively. On ISCX-VPN-App, PERO also obtains the best tail-conditioned metrics, improving $\mathrm { F 1 _ { 0 . 9 } }$ over the same methods by 13.67%, 16.40%, 12.26%, 9.83%,

15.62%, 11.79%, and 2.67%, respectively, while trailing MC-CVaR by only 0.06% in overall PR. The advantages of PERO are most critical on USTC-TFC, where it achieves an $\mathrm { F 1 _ { 0 . 9 } }$ of 87.63%, outperforming the strongest baselines MC-CVaR (75.73%) and OHTM (72.87%) and far outperforming Focal (51.82%), TDRO (48.94%), GroupDRO (47.13%), Random (41.52%), and ERM (31.29%). These results show that average-risk training, random selection, focal reweighting, distributionally robust training, and CVaR optimization all struggle on extreme tail samples, whereas PERO maintains strong tail robustness across all three datasets.

Overall, PERO demonstrates superior generalization and tail robustness compared to existing baselines. By leveraging a lightweight proxy, it matches or exceeds state-of-the-art performance with minimal overhead, suggesting its potential as a low-overhead solution for practical post-training of foundation models.

Computational and Memory Efficiency. We evaluate the computational and memory efficiency of all methods by comparing their average per-iteration wall-clock runtime and GPU memory usage. Fig. 4 summarizes the runtime results across three benchmark datasets. MC-CVaR incurs the highest computational cost, exhibiting the longest runtime on all three datasets. In contrast, PERO is among the most efficient robustness-oriented methods, consistently running faster than all other robustness-oriented baselines (TDRO, GroupDRO, OHTM, Focal, and MC-CVaR) and remaining close to the lightweight ERM and Random baselines. This indicates that PERO improves tail-risk robustness without incurring substantial computational overhead.

![](images/b6f56d285dc16759da199391dcf8cea5eecde42fd020d5e583851520bc1dbaff.jpg)  
Figure 4. Runtime comparison across three datasets.

Table 4 further reports detailed efficiency statistics on ISCX-VPN-Service. PERO substantially reduces post-training time, requiring approximately half the runtime of MC-CVaR. This efficiency gain stems from delegating risk estimation to a lightweight pre-evaluation module and restricting optimization to high-risk samples, thereby avoiding unnecessary forward-backward passes over the full batch. Effectively, PERO shifts the bulk of computation from large model backpropagation to small model inference, addressing the real bottleneck in foundation model post-training. In terms of memory usage, PERO consumes 11.75 GB of GPU memory, compared to 26.18 GB for MC-CVaR, achieving a 55.1% reduction. While ERM, Focal Loss, and TDRO incur the lowest memory footprint, PERO remains comparable, with only a 0.16 GB difference.

Table 2. Comparison Results on ISCX-VPN-Service and ISCX-VPN- $\cdot \mathbf { A } \mathbf { p } \mathbf { p } .$
<table><tr><td>Dataset</td><td colspan="7">ISCX-VPN-Service</td><td colspan="8"> $\mathrm { I S C X - V P N - A p p }$ </td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td> $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td> $\mathrm { F 1 _ { 0 . 9 } }$ </td><td>AC PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td> $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td> $\mathrm { F 1 _ { 0 . 9 } }$ </td></tr><tr><td>ERM</td><td>97.68</td><td>97.71</td><td>97.68</td><td>97.69</td><td>76.83</td><td>67.05</td><td>62.13</td><td>59.61</td><td>98.08 96.49</td><td>96.71</td><td>96.51</td><td>80.80</td><td>72.12</td><td>66.42</td><td>67.93</td></tr><tr><td>Random</td><td>97.37</td><td>97.39</td><td>97.37</td><td>97.37</td><td>73.67</td><td>55.45</td><td>57.45</td><td>53.21</td><td>97.78 96.27</td><td>96.24</td><td>96.12</td><td>77.82</td><td>68.21</td><td>64.12</td><td>65.20</td></tr><tr><td>MC-CVaR</td><td>98.22</td><td>98.24</td><td>98.22</td><td>98.22</td><td>82.17</td><td>74.33</td><td>70.37</td><td>70.74</td><td>98.78 97.54</td><td>97.77</td><td>97.62</td><td>87.81</td><td>83.27</td><td>77.16</td><td>78.93</td></tr><tr><td>Focal</td><td>97.45</td><td>97.48</td><td>97.45</td><td>97.46</td><td>74.46</td><td>58.84</td><td>58.25</td><td>56.39</td><td>98.13 96.59</td><td>96.94</td><td>96.72</td><td>81.35</td><td>72.87</td><td>68.37</td><td>69.34</td></tr><tr><td>OHTM</td><td>97.57</td><td>97.58</td><td>97.57</td><td>97.57</td><td>75.67</td><td>64.66</td><td>66.63</td><td>64.60</td><td>98.42 96.97</td><td>97.44</td><td>97.18</td><td>84.17</td><td>75.68</td><td>70.09</td><td>71.77</td></tr><tr><td>GroupDRO</td><td>96.98</td><td>97.03</td><td>96.98</td><td>96.99</td><td>69.83</td><td>54.59</td><td>54.65</td><td>52.95</td><td>98.16 96.50</td><td>96.84</td><td>96.59</td><td>80.42</td><td>70.47</td><td>64.25</td><td>65.98</td></tr><tr><td>TDRO</td><td>96.47</td><td>96.49</td><td>96.47</td><td>96.47</td><td>64.67</td><td>55.88</td><td>56.18</td><td>53.73 98.25</td><td>96.79</td><td>96.99</td><td>96.79</td><td>82.51</td><td>73.93</td><td>68.15</td><td>69.81</td></tr><tr><td>PERO (Ours)</td><td>98.60</td><td>98.62</td><td>98.60</td><td>98.60</td><td>86.00</td><td>83.61</td><td>76.42</td><td>78.03</td><td>98.79 97.48</td><td>97.96</td><td>97.71</td><td>87.94</td><td>85.72</td><td>79.70</td><td>81.60</td></tr></table>

Note: Results are percentages. Best and second-best values are in bold and underlined, respectively.

Table 3. Comparison Results on USTC-TFC.
<table><tr><td>Dataset</td><td colspan="8">USTC-TFC</td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td> $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td> $\mathrm { F 1 _ { 0 . 9 } }$ </td></tr><tr><td>ERM</td><td>96.99</td><td>97.03</td><td>97.05</td><td>97.04</td><td>69.93</td><td>33.90</td><td>32.99</td><td>31.29</td></tr><tr><td>Random</td><td>96.39</td><td>96.49</td><td>96.39</td><td>96.38</td><td>63.89</td><td>45.37</td><td>41.07</td><td>41.52</td></tr><tr><td>MC-CVaR</td><td>98.08</td><td>98.13</td><td>98.13</td><td>98.12</td><td>80.84</td><td>72.01</td><td>82.65</td><td>75.73</td></tr><tr><td>Focal</td><td>96.96</td><td>97.04</td><td>97.02</td><td>97.03</td><td>69.65</td><td>52.71</td><td>54.40</td><td>51.82</td></tr><tr><td>OHTM</td><td>97.80</td><td>97.90</td><td>97.85</td><td>97.83</td><td>77.96</td><td>71.25</td><td>76.16</td><td>72.87</td></tr><tr><td>GroupDRO</td><td>96.75</td><td>96.80</td><td>96.83</td><td>96.81</td><td>67.46</td><td>46.87</td><td>48.55</td><td>47.13</td></tr><tr><td>TDRO</td><td>96.38</td><td>96.44</td><td>96.47</td><td>96.40</td><td>63.79</td><td>49.37</td><td>52.31</td><td>48.94</td></tr><tr><td>PERO (Ours)</td><td>98.23</td><td>98.29</td><td>98.27</td><td>98.26</td><td>82.29</td><td>88.38</td><td>87.86</td><td>87.63</td></tr></table>

Note: Results are percentages. Best and second-best values are in bold and underlined, respectively.

Table 4. Efficiency Comparison Results on ISCX-VPN-Service.
<table><tr><td>Method</td><td>Runtime / Iter. (s)</td><td>Memory Usage (GB)</td></tr><tr><td>ERM</td><td>0.864</td><td>11.59</td></tr><tr><td>Random</td><td>0.610</td><td>11.82</td></tr><tr><td>MC-CVaR</td><td>1.568</td><td>26.18</td></tr><tr><td>Focal</td><td>1.156</td><td>11.59</td></tr><tr><td>OHTM</td><td>1.164</td><td>17.27</td></tr><tr><td>GroupDRO</td><td>1.032</td><td>11.63</td></tr><tr><td>TDRO</td><td>1.170</td><td>11.59</td></tr><tr><td>PERO (Ours)</td><td>0.826</td><td>11.75</td></tr></table>

## 5.3. Risk Prediction Fidelity of the Pre-evaluation Module

We assess the pre-evaluation module as a surrogate risk estimator using Pearson correlation, Spearman correlation, and Precision@16, where $1 6 = B / 2$ under batch size $B =$ 32. These capture, respectively, linear agreement between predicted and exact losses, the consistency of their risk rankings, and the overlap between predicted and exact top-16 high-risk samples.

As shown in Fig. 5, Pearson and Spearman correlations rise from weak early-stage values and stabilize at moderate levels, typically around 0.5 to 0.6 with dataset-dependent variation. Precision@k also shows that many top-ranked samples selected by the module overlap with the true highest-loss samples, stabilizing around 0.65 to 0.7 in the later training stage. The initially low values are expected, as rapid early classifier updates weaken the alignment between exact losses and proxy predictions. Their stabilization indicates that the module captures informative relative risk patterns. Together, these results show that the pre-evaluation module provides sufficient functional fidelity, in both ranking and top-set identification, to support effective robust posttraining.

## 5.4. Ablation Study

We evaluate PERO’s sensitivity to key hyperparameters: the training batch size B, the candidate pool size B<sup>ˆ</sup>, and the depth of the MLP within the prediction head in the pre-evaluation module. Each hyperparameter is varied independently from the default settings of $B = 3 2 , \hat { B } = 6 4$ and a 3-layer MLP. All experiments are conducted on ISCX-VPN-App, with results summarized in Fig. 6.

Effect of batch size B. We vary $B \in \{ 1 6 , 3 2 , 6 4 \}$ . Fig. 6(a) shows that increasing B from 16 to 32 improves all metrics, particularly tail accuracy $\mathrm { A C _ { 0 . 9 } }$ , while further increasing B to 64 yields diminishing returns. These results suggest that a moderate batch size provides a better trade-off between optimization stability and tail sensitivity, while overly small or large batches are less effective. Notably, PERO remains strong under non-optimal batch sizes, outperforming all baselines except MC-CVaR at B = 64 and staying competitive with ERM and GroupDRO at B = 16.

![](images/7cf6662b05d2e8c1de754ce4ce926d841517c012e5bb66b5fcc795c18a073de8.jpg)

![](images/1885fdfbdaaa580a4a8810f57e89bbd84832a53ff9732f22769a3cb4e0b8296b.jpg)

![](images/0942a6cddd9212094f7d1a1631f60173fe76cf0031b4f270904cc82ad150eb31.jpg)  
Figure 5. Pearson correlation, Spearman correlation, and Precision@16 between predicted and exact risks during training across three benchmark datasets.

![](images/0bbf1c2fe5864ab807eab7896efa1c1ee59d87b930c8a740b8db174fd4b63221.jpg)

![](images/939fdeed21d277b8913147b0be9c6ed39ab3d347ff129abf87f614dc6816f67a.jpg)

![](images/065c549a3c4c95a6001ed9fff1d1300b5040486750c5216296e70ab39a2f1d09.jpg)  
Figure 6. Ablation study of key PERO hyperparameters. (a) Training batch size B. (b) Candidate pool size B<sup>ˆ</sup> and the selection ratio $r = B / { \hat { B } } .$ (c) MLP depth in the pre-evaluation module. Dark blue bars indicate PERO’s default settings.

Effect of candidate pool size B<sup>ˆ</sup>. We vary $\hat { B } \in$ {64, 128, 256}, using $r ~ = ~ B / \hat { B }$ to denote the selection ratio. The case ${ \hat { B } } = B$ is omitted as it degenerates to ERM. As shown in Fig. 6(b), all sizes achieve near-perfect performance at $\mathrm { { A C } , \mathrm { { A C } _ { 0 . 5 } } }$ , and $\mathrm { A C } _ { 0 . 7 } .$ . At higher risk levels, larger selection ratios consistently retain a slight advantage, with the gap becoming more noticeable at $\mathrm { A C _ { 0 . 9 } }$ . This suggests that sufficient exploration benefits both overall performance and tail robustness, whereas excessively small selection ratios mildly degrade robustness. In particular, at $r = 1 / 4$ PERO achieves the best $\mathrm { A C _ { 0 . 9 } }$ among all baselines except MC-CVaR, while maintaining comparable performance to MC-CVaR. $\mathbf { A } \mathfrak { t } r = 1 / 8$ , it retains its lead over ERM and GroupDRO and matches OHTM.

Effect of MLP depth. We evaluate MLP depths of 2, 3, and 4 layers for the prediction head in the pre-evaluation module. As shown in Fig. 6(c), the 3-layer MLP achieves the best performance across all risk levels. The 2-layer variant provides a lighter surrogate but has more limited expressive capacity, especially under the most stringent tail-risk setting. Increasing the depth to 4 layers does not bring further gains, suggesting that additional surrogate capacity is unnecessary for this task. Overall, the 3-layer MLP offers the best trade-off between risk estimation capacity, robustness, and efficiency, and the 4-layer variant remains competitive with ERM and GroupDRO on $\mathrm { A C _ { 0 . 9 } }$ . This underscores that moderate model complexity suffices for strong tail performance without requiring aggressive surrogate capacity.

## 6. Conclusion

This work proposes PERO, an efficient robust post-training framework for encrypted traffic foundation models. PERO introduces a lightweight pre-evaluation module that decouples sample-wise risk estimation from expensive foundationmodel optimization, enabling targeted updates on critical tail examples with low computational overhead. Experiments on three main benchmarks show that PERO consistently improves tail robustness over representative robust post-training baselines while substantially reducing computational and memory costs. Additional results with YaTC further support the scalability and backbone generality of PERO. These efficiency gains are particularly important for continual post-training scenarios, where limited update windows make direct CVaR-style optimization impractical. Beyond encrypted traffic classification, PERO may extend to other risk-sensitive large-scale learning settings with high update costs and limited budgets, which warrants further validation in future work.

## Appendix

## A. Limitations and Ethical Considerations

Data Privacy and Consent. We use publicly released encrypted traffic datasets provided by the original authors for research purposes. PERO does not inspect communication content, attempt payload decryption, or reconstruct user identities or behaviors.

Fairness and Bias. PERO improves tail-risk robustness during post-training by emphasizing high-risk samples, but it does not remove biases inherent in the training data. Tailrisk performance may therefore vary across network environments.

Potential Misuse. Encrypted traffic classification technology may be misused for intrusive monitoring if deployed without adequate security measures. Responsible use requires transparency and appropriate access safeguards.

Limitations. Our theoretical convergence result (Theorem 4.1) relies on a uniformly bounded loss-Hessian spectral radius throughout optimization. Although this is a standard smoothness condition in convergence analyses of gradientbased methods (Hu et al., 2023), it is strong and may not strictly hold for large Transformer models in general. Thus, Theorem 4.1 should be interpreted as analytical insight under explicit simplifying conditions rather than a complete characterization of practical optimization dynamics. Although the supplementary CICIoT2022 experiments evaluate PERO on a larger and more realistic dataset, all results are still based on publicly available benchmarks, which may not fully capture temporal drift and deployment dynamics in production encrypted traffic environments. The pre-evaluation module also provides approximate risk estimates rather than exact losses, which may affect subset selection under severe distribution shifts. Finally, PERO introduces additional hyperparameters, motivating future work on adaptive parameter selection and validation in more diverse network environments.

## B. Dataset Details

We evaluate PERO on multiple encrypted traffic classification benchmarks. The main ET-BERT experiments use USTC-TFC, ISCX-VPN-Service, and ISCX-VPN-App. For backbone validation, we further apply PERO to YaTC on USTC-TFC, ISCX-VPN, ISCX-Tor, and CICIoT2022.

• USTC-TFC (Wang et al., 2017) contains 97,115 encrypted traffic samples from 10 malware families and 10 benign applications.

• ISCX-VPN (Gil et al., 2016) contains encrypted traffic under VPN and non-VPN scenarios. Following ET-BERT, we use ISCX-VPN-Service with 60,000 samples and 12 service-level classes, and ISCX-VPN-App with 77,163 samples and 17 application-level classes. For YaTC-based experiments, we follow the YaTC setting and report results on ISCX-VPN.

• ISCX-Tor (Lashkari et al., 2017) contains Tor traffic across eight categories.

• CICIoT2022 (Dadkhah et al., 2022) covers diverse IoT device types and attack behaviors, and is used as a large-scale IoT traffic benchmark.

## C. Implementation Details

Model Architecture. We use pre-trained ET-BERT (Lin et al., 2022) as the primary backbone because it is widely adopted, achieves strong cross-benchmark performance, and has a large parameter scale that highlights the efficiency benefit of lightweight risk estimation. We further validate backbone generality with YaTC (Zhao et al., 2023) in supplementary experiments.

The pre-evaluation module is a lightweight regression network. It encodes sequence embeddings with a two-layer MLP followed by global mean pooling, embeds hard labels via a lookup table, and projects soft probability targets through a linear layer. The concatenated representations are then passed to a three-layer MLP head with dimensions 770, 385, and 385 to regress the loss value.

Data Preprocessing and Splits. For ET-BERT experiments, we use three publicly available datasets from prior ET-BERT studies,<sup>2</sup> following the same preprocessing and tokenization procedures. For YaTC experiments, we likewise adopt the original preprocessing pipeline.<sup>3</sup> All datasets are randomly split into training, validation, and test sets with an 8:1:1 ratio, preserving class distributions.

Training Protocol. The default training batch size is $B = 3 2 .$ For selection-based methods, each batch is expanded to a candidate pool of ${ \hat { B } } = 2 B ,$ , unless otherwise specified. The pre-evaluation module is optimized with Adam using a learning rate of $5 \times 1 0 ^ { - 6 }$ , supervised by historical risks from the primary classifier. The primary classifier is optimized with AdamW using a learning rate of $1 \times 1 0 ^ { - 6 }$ , following the standard ET-BERT fine-tuning protocol. Non-selection methods are trained for 10 epochs, while selection-based methods are trained for 20 epochs to keep the number of classifier-updated samples comparable. All results are averaged over five runs with different random seeds.

Baseline Implementations. All baselines use the same backbone, optimizer, learning rate, training schedule, and batch size as PERO. Selection-based baselines also use the same candidate pool size $\hat { B } = 6 4$

• Random Selection uniformly samples B candidates, serving as a na¨ıve selection baseline without risk estimation.

• MC-CVaR (Rockafellar et al., 2000) uses a Monte Carlo approximation with risk level $\alpha = 0 . 5 .$ , selecting the top-B highest-loss candidates to approximate conditional tail-risk optimization.

• Focal Loss (Lin et al., 2017) re-weights each loss by $( 1 - p _ { t } ) ^ { \gamma }$ to emphasize hard examples, without subset selection.

• TDRO (Gladin et al., 2026) minimizes a LogSumExp surrogate that smoothly up-weights high-loss samples, without subset selection.

Table 5. Supplementary Results on ISCX-VPN and ISCX-Tor with YaTC as Backbone.
<table><tr><td>Dataset</td><td colspan="7">ISCX-VPN</td><td colspan="8">ISCX-Tor</td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td> $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td> $\mathrm { F 1 _ { 0 . 9 } }$ </td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$   $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td> $\mathrm { F 1 _ { 0 . 9 } }$ </td></tr><tr><td>ERM</td><td>97.37</td><td>96.80</td><td>95.50</td><td>95.97</td><td>74.14</td><td>77.49</td><td>71.54</td><td>72.23</td><td>98.62 97.71</td><td>98.81</td><td>98.18</td><td>86.49</td><td>87.61</td><td>91.45</td><td>86.50</td></tr><tr><td>Random</td><td>96.50</td><td>96.24</td><td>94.27</td><td>95.15</td><td>65.52</td><td>59.65</td><td>54.16</td><td>54.79</td><td>98.08 96.88</td><td>98.33</td><td>97.46</td><td>81.08</td><td>87.79</td><td>87.38</td><td>84.81</td></tr><tr><td>MC-CVaR</td><td>97.54</td><td>97.28</td><td>95.56</td><td>96.35</td><td>75.86</td><td>70.67</td><td>78.13</td><td>71.37</td><td>98.90 98.36</td><td>99.16</td><td>98.71</td><td>89.19</td><td>87.50</td><td>91.27</td><td>87.01</td></tr><tr><td>Focal</td><td>97.20</td><td>95.83</td><td>95.61</td><td>95.61</td><td>72.41</td><td>62.97</td><td>58.32</td><td>59.62</td><td>98.35 97.25</td><td>98.67</td><td>97.86</td><td>83.78</td><td>91.63</td><td>83.33</td><td>84.56</td></tr><tr><td>OHTM</td><td>97.20</td><td>96.46</td><td>95.79</td><td>96.00</td><td>72.41</td><td>53.94</td><td>50.71</td><td>51.17</td><td>98.35 97.46</td><td>98.67</td><td>97.98</td><td>83.78</td><td>84.13</td><td>88.47</td><td>83.44</td></tr><tr><td>GroupDRO</td><td>97.55</td><td>96.51</td><td>95.20</td><td>95.70</td><td>75.86</td><td>76.57</td><td>75.38</td><td>74.25</td><td>98.63 97.84</td><td>98.51</td><td>98.14</td><td>86.49</td><td>76.56</td><td>80.21</td><td>76.84</td></tr><tr><td>TDRO</td><td>97.72</td><td>97.18</td><td>96.05</td><td>96.44</td><td>77.59</td><td>69.26</td><td>65.71</td><td>64.85 98.35</td><td>97.42</td><td>98.29</td><td>97.80</td><td>83.78</td><td>75.00</td><td>76.38</td><td>73.61</td></tr><tr><td>PERO (Ours)</td><td>97.90</td><td>97.68</td><td>96.32</td><td>96.88</td><td>79.31</td><td>82.22</td><td>78.05</td><td>76.56</td><td>98.63 97.86</td><td>98.90</td><td>98.32</td><td>86.49</td><td>87.93</td><td>91.67</td><td>87.87</td></tr></table>

Note: Results are percentages. Best and second-best values are in bold and underlined, respectively.

Table 6. Supplementary Results on USTC-TFC and CICIoT2022 with YaTC as Backbone.
<table><tr><td>Dataset</td><td colspan="7">USTC-TFC</td><td colspan="8">CICIoT2022</td></tr><tr><td>Method</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td> $\mathrm { P R } _ { 0 . 9 }$ </td><td> $\mathrm { R C } _ { 0 . 9 }$ </td><td>F10.9</td><td>AC</td><td>PR</td><td>RC</td><td>F1</td><td> $\mathrm { A C _ { 0 . 9 } }$ </td><td>PR0.9  $\mathrm { R C } _ { 0 . 9 }$ </td><td>F10.9</td></tr><tr><td>ERM</td><td>97.05</td><td>97.87</td><td>97.74</td><td>97.80</td><td>70.71</td><td>84.03</td><td>85.57</td><td>84.68</td><td>95.55 94.85</td><td>93.26</td><td>93.97</td><td>55.56</td><td>65.16</td><td>59.44</td><td>60.32</td></tr><tr><td>Random</td><td>96.94</td><td>97.79</td><td>97.67</td><td>97.72</td><td>69.70</td><td>78.01</td><td>81.83</td><td>79.28</td><td>95.32 94.83</td><td>92.79</td><td>93.66</td><td>53.28</td><td>64.07</td><td>62.85</td><td>61.84</td></tr><tr><td>MC-CVaR</td><td>97.35</td><td>98.09</td><td>97.96</td><td>98.02</td><td>73.73</td><td>87.10</td><td>88.07</td><td>87.54</td><td>95.61 95.69</td><td>92.32</td><td>93.63</td><td>56.13</td><td>73.17</td><td>65.78</td><td>67.13</td></tr><tr><td>Focal</td><td>96.54</td><td>97.57</td><td>96.44</td><td>96.91</td><td>65.66</td><td>87.40</td><td>84.61</td><td>84.76</td><td>95.23 94.67</td><td>91.89</td><td>92.91</td><td>52.13</td><td>62.42</td><td>62.05</td><td>59.78</td></tr><tr><td>OHTM</td><td>96.84</td><td>97.72</td><td>97.59</td><td>97.65</td><td>68.69</td><td>84.03</td><td>84.89</td><td>84.43</td><td>95.27 95.50</td><td>92.56</td><td>93.74</td><td>52.71</td><td>62.05</td><td>58.01</td><td>58.61</td></tr><tr><td>GroupDRO</td><td>97.35</td><td>98.11</td><td>97.98</td><td>98.03</td><td>73.74</td><td>89.94</td><td>87.47</td><td>86.97</td><td>95.78 95.24</td><td>92.64</td><td>93.67</td><td>57.83</td><td>61.86</td><td>59.26</td><td>59.52</td></tr><tr><td>TDRO</td><td>97.25</td><td>98.01</td><td>97.89</td><td>97.95</td><td>72.72</td><td>86.48</td><td>87.22</td><td>86.83 95.67</td><td>94.44</td><td>91.93</td><td>93.03</td><td>56.70</td><td>62.56</td><td>54.43</td><td>55.87</td></tr><tr><td>PERO (Ours)</td><td>97.56</td><td>98.24</td><td>98.11</td><td>98.17</td><td>75.76</td><td>86.87</td><td>87.33</td><td>87.09</td><td>96.01 94.90</td><td>94.02</td><td>94.39</td><td>60.11</td><td>66.50</td><td>67.69</td><td>64.84</td></tr></table>

Note: Results are percentages. Best and second-best values are in bold and underlined, respectively.

• GroupDRO (Sagawa et al., 2020) is adapted to the instance level by assigning softmax weights over detached per-sample losses and optimizing the weighted loss sum, without group labels or a candidate pool.

• OHTM (Kumar et al., 2023) selects candidates by greedy Gram–Schmidt orthogonalization over $\ell _ { 2 ^ { - } }$ normalized embeddings, encouraging geometrically diverse subsets.

• ERM (Shalev-Shwartz & Ben-David, 2014) trains on each mini-batch with standard empirical risk minimization, without re-weighting or selection.

Hardware and Code Availability. All experiments run on NVIDIA A100 GPUs with PyTorch. The complete implementation will be released upon acceptance. Core code is available at https://anonymous.4open. science/r/PERO-D0A7.

Potential Extension to RL Post-training Although PERO is developed for supervised post-training (Zou et al., 2025; 2026b), its pre-evaluation and selective optimization paradigm may naturally extend to LLMs (Chi et al., 2024a; Lv et al., 2026) and RL post-training (Guo et al., 2025; Qu et al., 2026; Mao et al., 2026; Zou et al., 2026a). Specifically, a lightweight proxy could predict the optimization utility of sampled trajectories, allowing the policy to focus expensive updates on the most informative trajectories.

## D. Additional Backbone Evaluation

To further assess scalability and backbone generality, we conduct additional experiments using YaTC (Zhao et al., 2023) as the backbone. Following the evaluation setting in YaTC, we evaluate PERO on four benchmarks: USTC-TFC (Wang et al., 2017), ISCX-VPN (Gil et al., 2016), ISCX-Tor (Lashkari et al., 2017), and CICIoT2022 (Dadkhah et al., 2022), with results reported in Tables 5–6.

PERO obtains the best F1 on ISCX-VPN, USTC-TFC, and CICIoT2022, and remains within 0.39% of the best F1 on ISCX-Tor. Under the tail-conditioned metrics, PERO achieves the best $\mathrm { A C _ { 0 . 9 } }$ on three of the four datasets and the best $\mathrm { F 1 _ { 0 . 9 } }$ on ISCX-VPN and ISCX-Tor. In particular, on CICIoT2022, PERO improves $\mathrm { A C _ { 0 . 9 } }$ from the second-best 57.83% to 60.11%. Although MC-CVaR obtains the highest $\mathrm { F 1 _ { 0 . 9 } }$ due to stronger tail precision, PERO achieves the best $\mathrm { A C _ { 0 . 9 } }$ and $\mathrm { R C } _ { 0 . 9 } .$ , suggesting that PERO provides broader tail coverage. Overall, while MC-CVaR and GroupDRO occasionally lead on individual metrics, PERO provides a more balanced trade-off between classification performance and tail robustness, confirming its effectiveness under a different backbone.

## References

Ariffin, A., Afifi, F., Zaki, F., Hanif, H., and Anuar, N. B. Federated learning in network traffic classification: Taxonomy of implementation, application, and impact on sixth-generation wireless networks. Engineering Applications of Artificial Intelligence, 158:111471, 2025. doi: https://doi.org/10.1016/j.engappai.2025.111471.

Azab, A., Khasawneh, M., Alrabaee, S., Choo, K.-K. R., and Sarsour, M. Network traffic classification: Techniques, datasets, and challenges. Digital Communications and Networks, 10(3):676–692, 2024.

Babaria, R. J., Lyu, M., Batista, G., and Sivaraman, V. Fastflow: Early yet robust network flow classification using the minimal number of time-series packets. Proc. ACM Meas. Anal. Comput. Syst., 9(2), 2025. doi: 10.1145/3727115.

Ben-Tal, A. and Nemirovski, A. Robust convex optimization. Mathematics ofoperations research, 23(4):769–805, 1998.

Ben-Tal, A. and Nemirovski, A. Robust optimization– methodology and applications. Mathematical programming, 92(3):453–480, 2002.

Chen, X.-Y., Han, L., Zhan, D.-C., and Ye, H.-J. MI-ETT: Multi-instance encrypted traffic transformer for encrypted traffic classification. In Proceedings of the AAAI Conference on Artificial Intelligence, pp. 15922– 15929, Philadelphia, PA, USA, 2025. AAAI Press. doi: 10.1609/aaai.v39i15.33748.

Chi, H., Li, H., Yang, W., Liu, F., Lan, L., Ren, X., Liu, T., and Han, B. Unveiling causal reasoning in large language models: Reality or mirage? Advances in Neural Information Processing Systems, 37:96640–96670, 2024a.

Chi, H., Yang, W., Liu, F., Lan, L., Qin, T., and Han, B. Does confusion really hurt novel class discovery? International Journal ofComputer Vision, 132(8):3191–3207, 2024b.

Chi, H., Wang, Q., Jiang, J., Yao, J., Liu, F., and Han, B. Trustworthy foundation models for web intelligence: Causal perspectives and challenges. In Companion Proceedings of the ACM Web Conference 2026, pp. 1123– 1124, 2026.

Dadkhah, S., Mahdikhani, H., Danso, P. K., Zohourian, A., Truong, K. A., and Ghorbani, A. A. Towards the development of a realistic multidimensional iot profiling dataset. In 2022 19th Annual International Conference on Privacy, Security & Trust (PST), pp. 1–11, Fredericton, NB, Canada, 2022. IEEE. doi: 10.1109/PST55820.2022. 9851966.

Delage, E. and Ye, Y. Distributionally robust optimization under moment uncertainty with application to data-driven problems. Operations research, 58(3):595–612, 2010.

Deldar, F. and Abadi, M. Deep learning for zero-day malware detection and classification: A survey. ACM Computing Surveys, 56(2):1–37, 2023.

Dong, W., Yu, J., Lin, X., Gou, G., and Xiong, G. Deep learning and pre-training technology for encrypted traffic classification: A comprehensive review. Neurocomputing, 617:128444, 2025a.

Dong, W., Yu, J., Lin, X., Gou, G., and Xiong, G. Deep learning and pre-training technology for encrypted traffic classification: A comprehensive review. Neurocomputing, 617:128444, 2025b. doi: 10.1016/j.neucom.2024. 128444.

Gil, G. D., Lashkari, A. H., Mamun, M., and Ghorbani, A. A. Characterization of encrypted and VPN traffic using time-related features. In Proceedings ofthe 2nd International Conference on Information Systems Security and Privacy (ICISSP 2016), pp. 407–414, Rome, Italy, 2016. SciTePress.

Gladin, E., Kroshnin, A., Zhu, J.-J., and Dvurechensky, P. Improved stochastic optimization of logsumexp, 2026. URL https://arxiv.org/abs/2509.24894.

Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv preprint arXiv:2501.12948, 2025.

Hang, Z., Lu, Y., Wang, Y., and Xie, Y. Flow-MAE: Leveraging masked autoencoder for accurate, efficient and robust malicious traffic classification. In Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses, pp. 297–314, New York, NY, USA, 2023. Association for Computing Machinery. doi: 10.1145/3607199.3607206.

He, H. Y., Yang, Z. G., and Chen, X. N. PERT: Payload encoding representation from transformer for encrypted traffic classification. In 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K), pp. 1–8, Piscataway, NJ, USA, 2020. IEEE.

Hu, Z., Wu, X., and Huang, H. Beyond Lipschitz smoothness: A tighter analysis for nonconvex optimization. In Proceedings of the 40th International Conference on Machine Learning (ICML), volume 202, pp. 13883–13909. PMLR, 2023.

Kumar, R., Deleu, T., and Bengio, Y. The effect of diversity in meta-learning. In Proceedings ofthe AAAI Conference on Artificial Intelligence, volume 37, pp. 8396–8404,

Washington, DC, USA, 2023. AAAI Press. doi: 10.1609/ aaai.v37i7.26012.

Lashkari, A. H., Gil, G. D., Mamun, M. S. I., and Ghorbani, A. A. Characterization of Tor traffic using time based features. In Proceedings ofthe 3rd International Conference on Information Systems Security and Privacy (ICISSP 2017), pp. 253–262, Porto, Portugal, 2017. SciTePress.

Li, H., Chi, H., Liu, M., Huang, W., Xu, L., and Yang, W. Transformer-based spatial-temporal counterfactual outcomes estimation. arXiv preprint arXiv:2506.21154, 2025.

Lin, T.-Y., Goyal, P., Girshick, R., He, K., and Dollar, P. Fo-´ cal loss for dense object detection. In Proceedings ofthe IEEE International Conference on Computer Vision, pp. 2980–2988, Venice, Italy, 2017. IEEE Computer Society.

Lin, X., Xiong, G., Gou, G., Li, Z., Shi, J., and Yu, J. ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted traffic classification. In Proceedings of the ACM Web Conference 2022, pp. 633–642, New York, NY, USA, 2022. Association for Computing Machinery. doi: 10.1145/3485447.3512217.

Lin, X., He, L., Gou, G., Yu, J., Guan, Z., Li, X., Guo, J., and Xiong, G. Cetp: A novel semi-supervised framework based on contrastive pre-training for imbalanced encrypted traffic classification. Computers & Security, 143:103892, 2024.

Lotfollahi, M., Jafari Siavoshani, M., Shirali Hossein Zade, R., and Saberian, M. Deep packet: A novel approach for encrypted traffic classification using deep learning. Soft Computing, 24(3):1999–2012, 2020.

Lv, X., Mao, Y., Li, H., Liang, K., Yang, J., Huang, W., Chi, H., Chen, H., Lan, L., Yang, W., et al. Breaking the gradient barrier: Unveiling large language models for strategic classification. Advances in Neural Information Processing Systems, 38:49145–49180, 2026.

Lv, Y., Wang, Q., Liang, D., and Xie, Z. Theoretical investigations and practical enhancements on tail task risk minimization in meta learning. Advances In Neural Information Processing Systems, 37:82921–82961, 2024.

Mao, Y., Qu, Y., Wang, Q., Zou, H., and Ji, X. Dynamicspredictive sampling for active rl finetuning of large reasoning models. In International Conference on Learning Representations, volume 2026, pp. 25242–25270, 2026.

Meng, X., Lin, C., Wang, Y., and Zhang, Y. NetGPT: Generative pretrained transformer for network traffic, 2023.

Pacheco, F., Exposito, E., Gineste, M., Baudoin, C., and Aguilar, J. Towards the deployment of machine learning solutions in network traffic classification: A systematic survey. IEEE Communications Surveys & Tutorials, 21(2):1988–2014, 2019. doi: 10.1109/COMST.2018. 2883147.

Perez-Jove, R., Munteanu, C. R., Dorado, J., Pazos, A.,´ and Vazquez-Naya, J. Network traffic foundation mod-´ els: A systematic review. Computer Networks, 276: 111998, 2026. doi: https://doi.org/10.1016/j.comnet.2026. 111998.

Qu, J., Ma, X., and Li, J. TrafficGPT: Breaking the token barrier for efficient long traffic analysis and generation, 2024.

Qu, Y., Wang, Q. C., Mao, Y., Lv, Y., and Ji, X. Fast and robust: Task sampling with posterior and diversity synergies for adaptive decision-makers in randomized environments. arXiv preprint arXiv:2504.19139, 2025.

Qu, Y., Wang, Q., Mao, Y., Hu, V. T., Ommer, B., and Ji, X. Can prompt difficulty be online predicted for accelerating rl finetuning of reasoning models? In Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V. 1, pp. 1240–1250, 2026.

Rockafellar, R. T. and Uryasev, S. Conditional value-atrisk for general loss distributions. Journal ofbanking & finance, 26(7):1443–1471, 2002.

Rockafellar, R. T., Uryasev, S., et al. Optimization of conditional value-at-risk. Journal ofrisk, 2:21–42, 2000.

Sagawa, S., Koh, P. W., Hashimoto, T. B., and Liang, P. Distributionally robust neural networks for group shifts: On the importance of regularization for worst-case generalization. In International Conference on Learning Representations, Addis Ababa, Ethiopia, 2020. Open-Review.net. URL https://openreview.net/ forum?id=ryxGuJrFvS.

Shalev-Shwartz, S. and Ben-David, S. Understanding Machine Learning: From Theory to Algorithms. Cambridge University Press, USA, 2014.

Shi, Y., Li, G., Wu, J., Li, J., and Fang, H. Bpf-dag: Bytepacket-flow features fusion via dynamic attributed graph for reliable encrypted traffic classification. IEEE Transactions on Information Forensics and Security, 21:197–211, 2026. doi: 10.1109/TIFS.2025.3643127.

Tahaei, H., Afifi, F., Asemi, A., Zaki, F., and Anuar, N. B. The rise of traffic classification in iot networks: A survey. Journal of Network and Computer Applications, 154: 102538, 2020.

Tamar, A., Glassner, Y., and Mannor, S. Optimizing the CVaR via sampling. In Proceedings ofthe Twenty-Ninth AAAI Conference on Artificial Intelligence, pp. 2993– 2999, Austin, TX, USA, 2015. AAAI Press.

Telikani, A., Gandomi, A. H., Choo, K.-K. R., and Shen, J. A cost-sensitive deep learning-based approach for network traffic classification. IEEE Transactions on Network and Service Management, 19(1):661–670, 2021.

Wang, Q., Lv, Y., Xie, Z., Huang, J., et al. A simple yet effective strategy to robustify the meta learning paradigm. Advances in Neural Information Processing Systems, 36: 12897–12928, 2023.

Wang, Q., Qian, C., Li, X., Yao, Z., Zhou, G., and Shao, H. LENS: A foundation model for network traffic, 2024a.

Wang, Q., Lv, Y., Mao, Y., Qu, Y., Xu, Y., and Ji, X. Robust fast adaptation from adversarially explicit task distribution generation. In Proceedings Of The 31st ACM SIGKDD Conference On Knowledge Discovery And Data Mining V. 1, pp. 1481–1491, 2025a.

Wang, Q. C., Xiao, Z., Mao, Y., Qu, Y., Shen, J., Lv, Y., and Ji, X. Model predictive task sampling for efficient and robust adaptation. Nature Communications, 2026.

Wang, T., Xie, X., Wang, W., Wang, C., Zhao, Y., and Cui, Y. NetMamba: Efficient network traffic classification via pre-training unidirectional mamba. In 2024 IEEE 32nd International Conference on Network Protocols (ICNP), pp. 1–11, Piscataway, NJ, USA, 2024b. IEEE.

Wang, W., Zhu, M., Zeng, X., Ye, X., and Sheng, Y. Malware traffic classification using convolutional neural network for representation learning. In 2017 International Conference on Information Networking (ICOIN), pp. 712– 717, Piscataway, NJ, USA, 2017. IEEE.

Wang, Z., Fok, K. W., and Thing, V. L. Machine learning for encrypted malicious traffic detection: Approaches, datasets and comparative study. Computers & Security, 113:102542, 2022.

Wang, Z., Zhang, A., Li, H. C., Yin, Y., Chen, W., Lam, C. T., Mak, P. U., Vai, M. I., Gao, Y., and Pun, S. H. DFE: Deep flow embedding for robust network traffic classification. IEEE Transactions on Network Science and Engineering, 12(3):1597–1612, 2025b. doi: 10.1109/ TNSE.2025.3535577.

Wei, W., Gu, H., Deng, W., Xiao, Z., and Ren, X. Abltc: A lightweight design for network traffic classification empowered by deep learning. Neurocomputing, 489:333– 344, 2022.

Wiesemann, W., Kuhn, D., and Sim, M. Distributionally robust convex optimization. Oper. Res., 62(6):1358–1376, 2014.

Xu, K., Zhang, X., Wang, Y., Ohtsuki, T., Adebisi, B., Sari, H., and Gui, G. Self-supervised learning malware traffic classification based on masked autoencoder. IEEE Internet ofThings Journal, 11(10):17330–17340, 2024. doi: 10.1109/JIOT.2024.3357072.

Zhan, M., Yang, J., Jia, D., and Fu, G. Eapt: An encrypted traffic classification model via adversarial pre-trained transformers. Computer Networks, 257:110973, 2025. doi: https://doi.org/10.1016/j.comnet.2024.110973.

Zhang, H., Yu, L., Xiao, X., Li, Q., Mercaldo, F., Luo, X., and Liu, Q. TFE-GNN: A temporal fusion encoder using graph neural networks for fine-grained encrypted traffic classification. In Proceedings of the ACM Web Conference 2023, pp. 2066–2075, New York, NY, USA, 2023a. Association for Computing Machinery. doi: 10. 1145/3543507.3583227.

Zhang, X., Hao, L., Gui, G., Wang, Y., Adebisi, B., and Sari, H. An automatic and efficient malware traffic classification method for secure internet of things. IEEE Internet ofThings Journal, 11(5):8448–8458, 2023b.

Zhao, J., Jing, X., Yan, Z., and Pedrycz, W. Network traffic classification for data fusion: A survey. Information Fusion, 72:22–47, 2021.

Zhao, R., Deng, X., Yan, Z., Ma, J., Xue, Z., and Wang, Y. Mt-flowformer: A semi-supervised flow transformer for encrypted traffic classification. In Proceedings ofthe 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD ’22, pp. 2576–2584, New York, NY, USA, 2022. Association for Computing Machinery. doi: 10.1145/3534678.3539314.

Zhao, R., Zhan, M., Deng, X., Wang, Y., Wang, Y., Gui, G., and Xue, Z. Yet another traffic classifier: A masked autoencoder based traffic transformer with multi-level flow representation. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 37, pp. 5420– 5427, Washington, DC, USA, 2023. AAAI Press. doi: 10.1609/aaai.v37i4.25674.

Zheng, W., Gou, C., Yan, L., and Mo, S. Learning to classify: A flow-based relation network for encrypted traffic classification. In Proceedings of The Web Conference 2020, pp. 13–22, New York, NY, USA, 2020. Association for Computing Machinery.

Zhou, G., Guo, X., Liu, Z., Li, T., Li, Q., and Xu, K. TrafficFormer: An efficient pre-trained model for traffic data. In 2025 IEEE Symposium on Security and Privacy (SP), pp. 1844–1860, Piscataway, NJ, USA, 2025. IEEE.

Zou, H., Mao, Y., Qu, Y., Wang, Q., and Ji, X. Utilitydiversity aware online batch selection for llm supervised fine-tuning. arXiv preprint arXiv:2510.16882, 2025.

Zou, H., Wang, Q., Qu, Y., Jiang, Y., Cai, L., Mao, Y., Peng, R., Xu, X., Liu, W., Yang, K., et al. Trace: A unified rollout budget allocation framework for efficient agentic reinforcement learning. arXiv preprint arXiv:2606.11119, 2026a.

Zou, H., Zang, Y., Xu, W., Zhu, Y., and Ji, X. Flylora: Boosting task decoupling and parameter efficiency via implicit rank-wise mixture-of-experts. Advances in Neural Information Processing Systems, 38:10386–10419, 2026b.
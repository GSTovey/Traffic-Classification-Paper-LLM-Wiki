の

USENIX

THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

# Towards Practical Few-shot Multi-tab Website Fingerprinting

Lin Liu and Ziling Wei, National University of Defense Technology; Zhuotao Liu and Xinhao Deng, Tsinghua University; Zixuan Dong and Shuhui Chen, National University of Defense Technology

# This paper is included in the Proceedings of the 35th USENIX Security Symposium.

August 12–14, 2026 • Baltimore, MD, USA

ISBN 978-1-939133-58-8

Open access to the Proceedings of the 35th USENIX Security Symposium is sponsored by

AgleU

King Abdullah University of

Science and Technology

# Towards Practical Few-shot Multi-tab Website Fingerprinting

<sub>Lin</sub> <sub>Liu</sub>1 <sub>Ziling</sub> <sub>Wei</sub>1 <sub>Zhuotao</sub> <sub>Liu</sub>2 <sub>Xinhao</sub> <sub>Deng</sub>2 <sub>Zixuan</sub> <sub>Dong</sub>1 <sub>Shuhui</sub> <sub>Chen</sub>1 <sup>1</sup> National University of Defense Technology <sup>2</sup> Tsinghua University

## Abstract

Website fingerprinting (WF) attacks can infer the vis ited websites to deanonymize Tor networks by analyzing encrypted traffic patterns. Recent few-shot WF methods reduce reliance on large-scale data collection, yet they predominantly formulate WF as a single-label classifica tion task and rely on meta-learning episodes that assume disjoint label sets and stable embedding spaces. These assumptions break down in the realistic multi-tab browsing, where traffic from multiple websites interleaves within a single observation window and the number of concurrent tabs is unknown. Meanwhile, the label space grows expo nentially as the monitored set expands, making existing multi-tab WF methods costly to update. To address these challenges, we propose MMF, a novel framework for few shot multi-tab WF. MMF shifts the meta-learning objec tive from single-label classification to support-guided presence detection. In each episode, we pair a mixed multi-tab query trace with a small set of single-tab support traces for each monitored website, and generate classspecific features by feature reweighting to decide which websites are present. This detection-centric formulation yields well-defined few-shot tasks in multi-tab scenarios and enables MMF to detect previously unseen websites from limited traces. We evaluate MMF on established public datasets and a new real-world dataset collected under varied browsing conditions. Results demonstrate that MMF consistently outperforms state-of-the-art multi tab WF attacks across all settings. Notably, in the 5-shot scenario, MMF achieves improvements of up to 300% in Novel Precision@k, highlighting its strong capability for few-shot detection in dynamically growing website sets.

## 1 Introduction

Anonymous communication systems seek to protect both message content and communication metadata from network surveillance. Tor, one of the most widely deployed privacy-enhancing technologies for web browsing [30], pursues this goal by routing traffic through multi-hop relays and applying layered (onion) encryption to reduce the linkability between users and their online activities [14].

However, a persistent line of research, known as website fingerprinting (WF), demonstrates that passive adversaries can still infer visited websites by analyzing observable side channels, such as sequences of incoming and outgoing packets, inter-packet timing, and burstlevel statistics [5, 8, 20, 33, 45, 47, 48]. Recent deep learning-based WF attacks have achieved high accuracy even under network noise and against various defenses [1, 32, 36, 40].

A critical barrier to a practical WF deployment is the unsustainable cost ofdata collection and model maintenance. Unlike many traffic classification tasks, in which class semantics are relatively stable, websites are dynamic monitored targets whose traffic patterns drift due to content updates, browser changes, and network dynamics. To retain effectiveness, attackers must continuously recollect labeled traces at scale and retrain models, an operationally expensive process. These constraints have motivated few-shot (low-data) WF, which aims to preserve strong inference performance using only a handful of labeled traces per website [7, 28, 40, 50, 52, 59, 60].

However, most prior work on few-shot WF implicitly assumes a single-tab setting, where each trace corresponds to an isolated visit to one website. In practice, web browsing is often multi-tab: users open multiple tabs within a short time window, causing their traffic to interleave within a single observation window. This interleaving corrupts the clean, site-specific fingerprints exploited by classic WF attacks, while the unknown and dynamic tab count further complicates the problem [13, 49, 55]. Recent studies have begun to revisit multi-tab WF with end-to-end models and report promising performance under more realistic conditions [10, 13, 18, 22, 31, 49, 53, 55, 56, 58]. Nevertheless, the multi-tab setting is typically more data-intensive than single-tab WF because the combinatorial diversity of tab-opening patterns substantially expands the space of possible mixtures, increasing the labeled data required for adequate coverage and robust performance.

This discrepancy prompts a fundamental question: Why hasfew-shot WF research remained confined to the single-tab setting, rather than extending effectively to the more realistic multi-tab setting? We argue that the key obstacle is not simply “harder inputs”, but a shift in the learning objective from classification to detection.

Existing few-shot WF methods [28, 40, 59, 60] for the single-tab setting typically follow either metric-based or optimization-based few-shot learning paradigms under a classification-centric formulation adapted from singlelabel classification [41,44]. These paradigms are effective because episodic training implicitly relies on three prop erties: (i) query traces and their supports are drawn from comparable distributions, (ii) each query corresponds to exactly one website class, and (iii) a globally coherent embedding geometry allows queries to be aligned with class prototypes or stable adaptation directions.

However, these properties no longer hold in multi-tab browsing. A query trace can contain multiple interleaved websites, so its representation is not expected to align with any single-class prototype [6, 25, 57]. As a result, prior few-shot WF formulations [7, 28, 40, 50, 52, 59, 60] can not directly extend to realistic multi-tab scenarios, leaving a critical gap between data-efficient methods and practical attack settings.

To bridge this gap, we present MMF, a framework for few-shot multi-tab website fingerprinting that makes episodic few-shot task construction feasible under the multi-tab setting via support-guided feature reweighting. Given a mixed multi-tab query trace, MMF encodes it into a feature map that preserves local burst-level microstructures, which remain informative even when mul tiple websites are interleaved. For each target website, MMF summarizes its K clean single-tab support traces into a class-conditioned reweighting vector. This vec tor performs channel-wise gating on the multi-tab query features to produce a class-specific feature map, and a presence head then predicts whether the target website appears in the mixed traces.

This detection-centric formulation, inspired by objectdetection paradigms, keeps few-shot episodes well defined in multi-tab settings. Each meta-training episode pairs (i) one multi-tab query trace with (ii) a K-shot single-tab support set for each website in a sampled target set, and supervises learning with per-class binary pres ence labels. Within an episode, the learner is trained to derive class-conditioned reweighting vectors from sup ports, use them to amplify target-class evidence while suppressing interference in the mixed query representation, and optimize independent presence predictions. As a result, MMF learns transferable mechanisms for extracting class-specific weights from single-tab traces, rather than relying on a globally coherent prototype geometry or brittle few-step adaptation.

After base training, MMF enables continual onboarding of previously unseen websites using only a handful of newly collected clean single-tab traces and a small number of labeled multi-tab traces for lightweight finetuning, substantially reducing the need for expensive long-horizon collection and full retraining over largescale mixed-traffic datasets.

The contributions of our work are given as follows.

• Problem reformulation: We identify the task mismatch that prevents conventional few-shot WF from scaling to multi-tab browsing, and reframe multi-tab WF as a few-shot presence detection problem.

• Framework design: We propose MMF, a novel framework which formulates few-shot multi-tab WF as support-guided presence detection and learns transferable class-conditioning via supportconditioned feature reweighting with episodic training, enabling fast adaptation to unseen websites with only limited data. By producing class-specific representations from a detection perspective, MMF further removes the need for any prior knowledge of the tab count using a single shared model.

• Extensive evaluation: We evaluate MMF on both public and self-collected datasets under closedworld, open-world, defense-aware, and dynamic tab settings. The results demonstrate that MMF significantly outperforms state-of-the-art baselines, achieving up to 300% higher Novel Precision@k in 5-shot scenarios while maintaining robust performance as the monitored set expands.

Our work bridges the gap between data efficiency and real-world applicability in website fingerprinting, advancing state-of-the-art towards practical deployment. We release code and data to support result reproducibility, as well as future exploration in this field.

## 2 Background

## 2.1 Website Fingerprinting Attacks

Website fingerprinting (WF) aims to infer which websites a user visits by passively analyzing traffic side channels (e.g., packet direction sequences, burst patterns), even when the application payload is encrypted and the intended destination is hidden by anonymity systems such as Tor [14, 33, 47].

Table 1: Summary of representative works.

<table><tr><td>Works</td><td>Multi-Tab $^{1}$ </td><td>Few-Shot $^{2}$ </td><td>Tabs-Unknown $^{3}$ </td><td>Detection $^{4}$ </td></tr><tr><td>DF [39]</td><td>×</td><td>×</td><td>×</td><td>×</td></tr><tr><td>BAPM [18]</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>MMD [42]</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>NetCLR [3]</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>DQF [60]</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>TMWF [22]</td><td>√</td><td>×</td><td>×</td><td>√</td></tr><tr><td>ARES [13]</td><td>√</td><td>×</td><td>√</td><td>×</td></tr><tr><td>FMWF [31]</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>MMF</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

<sup>1</sup> Multi-Tab: Users can open multiple tabs while browsing.  
2 Few-Shot: Using few samples to train the model for identifying unseen classes.  
3 Tabs-Unknown: The number of tabs that a user opens is dynamic and unknown.  
4 Detection: Uses an object-detection paradigm as the framework.

Early WF studies relied on hand-crafted features and conventional classifiers, and showed that encrypted traffic remains distinguishable [19, 32, 33, 47]. With the adoption of deep learning, WF attacks have increasingly shifted toward end-to-end representation learning, substantially improving accuracy and challenging WF defenses by extracting richer discriminative patterns di rectly from raw traces [4, 11, 12, 36, 39]. However, these high-performing models typically assume abundant and continuously refreshed training data. The adversary must repeatedly collect a large number of traces per monitored website, and retrain models whenever the monitored set or deployment environment changes [9, 49]. This maintenance burden has motivated a growing body of few-shot (low-data) WF research, including episodic meta-learning for rapid adaptation, metric- or contrastivebased objectives for learning discriminative embeddings under data scarcity, and augmentation expansion to mitigate label sparsity [3, 7, 29, 40, 52, 60]. Notably, existing few-shot WF works almost exclusively adopt a single-tab assumption, where each trace corresponds to browsing activity from a single tab, making the problem naturally amenable to episodic few-shot classification.

Recent work has therefore revisited multi-tab WF with more systematic end-to-end architectures, including Transformer-based designs and multi-tab-native frame works [13, 18, 22, 27, 31, 53, 56, 58]. Most existing multitab WF methods formulate the task primarily as a multilabel classification problem, following the conventional WF perspective [33, 39], while TMWF [22] is among the few works that consider WF from an object-detectioninspired perspective. However, TMWF does not fully address the tab-unknown setting and lacks few-shot capabilities. From a maintenance-cost perspective, multi-tab WF calls for stronger few-shot capabilities than singletab WF, because the space of feasible label combinations grows combinatorially with the monitored set size and the number of concurrently opened tabs. ARES [13] introduces a one-vs-all framework to support new-class onboarding, but it still requires non-trivial training samples and maintains a separate model for each monitored class, making the model-maintenance cost scale linearly with the monitored set size. FMWF [31] explores general few-shot strategies based on data augmentation and transfer learning, but it lacks effective designs tailored to the multi-tab scenario, leaving substantial room for improvement (see experimental results in § 5.3).

![](images/b35950a56b7f7a83e95f0d0d48387557fd7c8b00a255c48a34bdeb05892bf252.jpg)  
Note: � means number of classes, � means number of tabs opened by users  
Figure 1: The dilemma of FSL. Left: Adopting one center per class fails because a mixed trace containing multiple websites cannot align with any single-class prototype. Right: Alternatively, defining a unique center for every possible combination leads to a combinatorial explosion in the number of required prototypes (e.g., C(N, T)), making the metric space enormous.

## 2.2 Few-Shot Learning

Few-shot learning (FSL) studies generalization when only a small number of labeled examples are available per class. A dominant paradigm is episodic (meta-task) training: each episode consists of a support set and a query set, and the learner is trained over many episodes to acquire an inductive bias for rapid generalization from limited support data [16, 34, 41, 44]. In prior WF work, few-shot attacks largely fall into two families. First, metric-based approaches learn an embedding space and classify query examples by their distance to class prototypes or nearest neighbors; WF instantiations often adopt Triplet/Quadruplet-style objectives to promote separability under data scarcity [29, 40, 60]. Second, optimizationbased meta-learning targets rapid adaptation to novel classes, typically via a small number of gradient-based update steps on the support set (e.g., MAML-style methods) [7,16]. Although effective for single-tab traces, these designs largely assume a classification-centric formulation of the task.

A key challenge is that extending these classificationcentric few-shot paradigms to multi-tab WF is not merely a matter of increased difficulty, but a shift in the underlying task logic. Metric-based methods implicitly assume a stable global geometry that a query example should lie close to its class prototype in the embedding space. In the multi-tab scenario, temporal interleaving can break globally coherent single-tab fingerprints, causing a mixed trace to fall far from all single-tab prototypes. Alternatively, defining prototypes for each combination of co occurring websites leads to a combinatorial explosion in the number of centers [2, 43] (we illustrate this col lapse in Figure 1). Optimization-based meta-learning faces a related task-construction dilemma. When support traces (single-tab) and query traces (multi-tab) are drawn from markedly different distributions, a few adaptation steps may not bridge the gap. Moreover, updates can become unstable when multiple sources of evidence coexist within a single mixed trace.

![](images/67e4bdf0e2615ef3ef7fc95f47f0009ea46ea141c1884e4c2e359aae58b926ff.jpg)  
Figure 2: Threat model. The adversary passively monitors encrypted traffic between the user and the Tor entry node.The timeline illustrates the practical maintenance challenge: when content evolves and new targets are added (Phases 3-4), the attacker must efficiently update the model using limited newly collected data (Phase 5).

## 3 Threat Model

We consider website fingerprinting (WF) attacks against Tor. The adversary is a passive network observer, and it cannot decrypt application-layer content and does not modify, inject, delay, or drop traffic. Instead, it records externally observable metadata on the client-side link (e.g., on the client-to-entry (guard) relay link, at a local gateway, or from an ISP vantage point), including packet directions and timestamps [14, 33, 47]. Following prior WF work, the adversary can also obtain labeled training data by repeatedly visiting monitored websites, and train/evaluate models [9,36,37,39]. Figure 2 summarizes our threat model.

Beyond the conventional single-tab assumption, we focus on multi-tab browsing, where a user may open multiple tabs concurrently. Traffic streams from different websites then become temporally interleaved within the observation window, yielding a mixed multi-tab trace rather than an isolated single-website trace [13,22,53,55, 56]. Another key aspect of our setting is that the number of concurrently opened tabs is dynamic and unknown a priori to the attacker at inference time, while most prior works choose to ignore this [18, 22, 27, 31, 53, 55].

As illustrated by the lower half of the timeline in Figure 2, we also consider target dynamics over longer time horizons. In practice, an attacker typically pre-trains and deploys a model using historical data. However, the monitored set may evolve (e.g., newly added targets), and website content and resource-loading behavior can drift over time. These changes introduce distribution shift that can quickly degrade the reliability of a trained model [10, 23, 49]. From a maintenance standpoint, we assume the attacker can periodically update the deployed model using limited newly collected data, including a small number of labeled single-tab and multi-tab traces. We use these data to fine-tune the deployed model, avoiding prolonged collection and full retraining on large-scale datasets.

Finally, following prior WF evaluations, we consider both closed-world (CW) and open-world (OW) settings. In CW, all visited websites belong to the monitored set. In OW, the user may visit a large and unknown set of unmonitored websites. These pages generate background traffic that can be interleaved with monitored traffic, and the attacker must detect whether monitored websites are present despite this realistic interference.

## 4 Design of MMF

## 4.1 Overview

As discussed in § 1, extending few-shot website fingerprinting (FS-WF) from single-tab traces to realistic multi-tab browsing is not simply a “harder-input” variant. Multi-tab traffic temporally interleaves encrypted segments from multiple websites. This violates the singlelabel assumption and disrupts trace-level patterns that conventional episodic few-shot classification implicitly depends on [41]. The problem is further complicated by the fact that the number of concurrently opened tabs is dynamic and unknown.

To make episodic few-shot task construction well defined under multi-tab mixing, MMF draws inspiration from feature reweighting in few-shot detection [25] and reformulates FS-WF as presence prediction. Rather than deciding which class a mixed trace belongs to, MMF determines, for each target website, whether evidence of that website is present in the mixed trace. Concretely, for a target class c, MMF summarizes its K single-tab supports into a class-conditioned reweighting vector, uses it to modulate the channel semantics of the multi-tab query feature map, and trains a presence head with per-class binary supervision. This reformulation avoids reliance on globally coherent prototype geometry and brittle few-step adaptation. It instead learns a transferable mechanism for extracting class-specific evidence from obfuscated mixtures.

![](images/00042bf789bd486040eaf4cdc70f95e2b53511b4b0cd2fb5e89f04485bd55840.jpg)  
Figure 3: MMF overview. Each episode pairs a mixed multi-tab query trace with K clean single-tab support traces for each target website. MMF encodes the query into a feature map, derives a class-conditioned reweighting vector from the supports, reweights query channels to form a class-specific feature map, and predicts per-class presence probabilities.

Figure 3 gives an overview of the MMF framework. Training begins with an Episode Sampling module that constructs meta-learning tasks. Each episode samples K single-tab traces per target class as supports, pairs them with a multi-tab query trace, and uses multi-hot pres ence labels as supervision. Within each episode, MMF performs forward computation and parameter updates through three modules, namely Trace Encoding, Feature Reweighting, and Presence Detection.

Trace Encoding. MMF encodes a multi-tab query trace into a multi-channel feature map that preserves local, burst-level microstructure and avoids premature global pooling. These local patterns, induced by resource fetches, can remain informative even when multiple web sites are interleaved. In parallel, the support branch encodes single-tab traces and produces a compact classconditioned reweighting vector that captures which channel patterns are characteristic of the target class.

Feature Reweighting. Conditioned on this vector, MMF reweights the channels of the query feature map, ampli fying target-related responses while suppressing inter ference from other websites and background traffic, to produce a more robust class-specific feature map.

Presence Detection. Finally, the detection head aggregates the class-specific feature map and outputs the probability that the target website appears in the mixed trace. To remain sensitive to sparse, scattered evidence while mitigating diffuse correlations induced by heavy mixing, MMF incorporates two attention mechanisms and opti mizes a weighted binary objective to handle the extreme class imbalance.

## 4.2 Episode Sampling

The Episode Sampling module constructs training tasks for MMF in both meta-training (base) and meta-finetuning (few-shot). We follow a deployment-oriented workflow in which an attacker can typically collect labeled traces for a set of monitored base/seen websites over a long period, enabling offline meta-training. After deployment, the monitored set may expand or evolve. Newly added novel/unseen websites typically come with limited labeled traces, so the model must be updated without expensive full retraining.

During meta-training, we adopt episodic learning and reorganize the dataset into a large number of episodes. For both query and support traces, we use only the packet direction sequence. We encode outgoing packets as +1 and incoming packets as −1. Each multi-tab query trace is represented as $x _ { j } ^ { q } \in \{ - 1 , + 1 \} ^ { L _ { q } }$ and each single-tab support trace as $x _ { c , k } ^ { s } \in \{ - 1 , + 1 \} ^ { L _ { s } }$ , where $L _ { q }$ and $L _ { s }$ denote fixed sequence lengths after truncation/padding.

We denote each episode as $\mathcal { T } _ { j } = ( \boldsymbol { S } _ { j } , \boldsymbol { Q } _ { j } )$ . Specifically, the query set contains one labeled multi-tab example, $Q _ { j } = \{ ( x _ { j } ^ { q } , \mathbf { y } _ { j } ^ { q } ) \}$ with $\mathbf { y } _ { j } ^ { q } \in \{ 0 , 1 \} ^ { C }$ , and the support set provides K single-tab traces per class, $\begin{array} { r } { S _ { j } = \{ x _ { c , k } ^ { s } \mid c = } \end{array}$ $1 , \ldots , C ; k = 1 , \ldots , K \}$ . Here, C is the number of target classes sampled in the episode, and $\mathbf { y } _ { j } ^ { q }$ is a multi-hot presence label indicating which of these C websites appear in the multi-tab query. Unlike conventional single-tab FS-WF episodes formulated as a mutually exclusive classification task, MMF episodes are driven by presence supervision. The learner must decide, for each target website, whether it appears in the same obfuscated multi-tab query trace.

Meta-fine-tuning follows the same episode construction but uses drastically less data for novel websites. For each unseen website, the attacker has limited labeled single-tab and multi-tab traces that contain the novel website for fine-tuning. Accordingly, fine-tuning episodes use few-shot budgets for both supports and queries. We also subsample seen classes to comparable few-shot sizes so that updates are not dominated by abundant base data, thereby focusing adaptation on onboarding and calibrat ing novel websites.

![](images/b98f765630a478ec4af640423e19ea55785dec693617754b365c639cec4102f2.jpg)  
Figure 4: Weight generator. MMF summarizes K single tab support traces of class c into a class-conditioned reweighting vector $\mathbf { W } _ { c }$ by support encoding, shot aggregation, SE-style channel attention, and an MLP projection.

We emphasize that support traces are used only during training and fine-tuning. After training, MMF precom putes and stores the class-conditioned reweighting vector for each monitored website. At deployment time, the online detector takes only a multi-tab query trace as input and applies the stored class-conditioned vectors for classaware processing and presence prediction, avoiding extra parameters.

## 4.3 Trace Encoding

MMF builds on an observation commonly exploited in deep-learning WF [13]: even when global trace-level patterns are disrupted, website-specific local loading behaviors (e.g., short bursts and direction alternations induced by resource fetches) can remain informative and be captured by convolutional encoders. Accordingly, ${ \bf M N } ^ { \prime } { \bf s }$ trace encoder produces (i) a query feature map that preserves where local patterns occur and (ii) classconditioned reweighting vectors that summarize which channel patterns characterize each target website. These outputs share the same number of channels, enabling class-aware channel filtering that is robust to position shifts in later stages.

Feature extractor. For each multi-tab query trace, MMF adopts a DF-style 1D convolutional encoder that has proven effective for WF representation learning [39]. The encoder maps the input direction sequence to an intermediate feature map whose sequence dimension pre serves the positions of local patterns, while the channel dimension encodes types of discriminative local signa tures. Formally, given a labeled multi-tab query trace $x _ { j } ^ { q } ,$ the feature extractor outputs

$$
\mathbf {F} _ {j} = f _ {\boldsymbol {\theta}} (x _ {j} ^ {q}) \in \mathbb {R} ^ {L ^ {\prime} \times D},\tag{1}
$$

where $L ^ { \prime }$ is the reduced sequence length after convo lution/pooling, and D is the channel dimension shared across classes. This “position response + channel semantics” representation is well suited to interleaving because the same website may contribute local patterns at varying positions.

Weight generator. Given a target website class c with K clean single-tab support traces $\{ x _ { c , k } ^ { s } \} _ { k = 1 } ^ { K }$ , MMF generates a class-conditioned reweighting vector ${ \bf W } _ { c } \in \mathbb { R } ^ { D }$ as a compact channel-wise descriptor of class c. As illustrated in Figure 4, each support trace is first encoded by a 1D CNN encoder into a channelized feature map:

$$
\mathbf {U} _ {c, k} = g _ {\phi} (x _ {c, k} ^ {s}) \in \mathbb {R} ^ {L ^ {\prime} \times D}.\tag{2}
$$

We then aggregate the K shot-level feature maps by averaging:

$$
\mathbf {U} _ {c} = \frac {1}{K} \sum_ {k = 1} ^ {K} \mathbf {U} _ {c, k} \in \mathbb {R} ^ {L ^ {\prime} \times D}.\tag{3}
$$

To reduce sensitivity to shot-level noise when K is small, we apply an SE-style channel attention block that computes channel weights from $\mathbf { U } _ { c }$ :

$$
\begin{array}{l} \mathbf {a} _ {c} = \sigma \Big (\mathrm{MLP} _ {\mathrm{SE}} \big (\mathrm{GAP} (\mathbf {U} _ {c}) \big) \Big) \in \mathbb {R} ^ {D}, \\ \widetilde {\mathbf {U}} _ {c} = \mathbf {U} _ {c} \odot \mathbf {a} _ {c}, \end{array}\tag{4}
$$

where $\mathrm { G A P ( \cdot ) }$ averages over the $L ^ { \prime }$ positions, $\sigma ( \cdot )$ is the sigmoid function, and ⊙ denotes channel-wise multiplication with broadcasting over positions. Finally, we obtain a vector summary by global average pooling and map it to $\mathbf { W } _ { c }$ via an MLP:

$$
\mathbf {v} _ {c} = \operatorname{GAP} (\widetilde {\mathbf {U}} _ {c}) \in \mathbb {R} ^ {D}, \quad \mathbf {W} _ {c} = \operatorname{MLP} (\mathbf {v} _ {c}) \in \mathbb {R} ^ {D}.\tag{5}
$$

By construction, $\mathbf { W } _ { c }$ lies in the same channel space as the query feature map in Eq. (1), which enables direct class-aware channel filtering in the next stage.

## 4.4 Feature Reweighting

§ 4.3 produces a query feature map $\mathbf { F } \boldsymbol { j } \in \mathbb { R } ^ { L ^ { \prime } \times D }$ and classconditioned reweighting vectors $\mathbf { W } c _ { c = 1 } ^ { C }$ , where channels correspond to different local pattern types. In multi-tab traces, a target website may contribute patterns at arbitrary positions due to interleaving. MMF therefore does not attempt to learn a globally aligned template along the sequence dimension. Instead, inspired by [25], MMF uses Wc to filter the channel semantics of Fj in a positionagnostic manner. At each position, target-related channels are emphasized while irrelevant channels are attenuated, yielding a more stable class-specific representation under mixing and temporal shifts.

As shown in Figure 5, we implement feature reweighting as a 1D dynamic convolution whose kernel is parameterized by the reweighting vector $\mathbf { W } c .$ Given $\mathbf { W } _ { c } \in \mathbb { R } ^ { D }$ and $\mathbf { F } _ { j } \in \mathbb { R } ^ { L ^ { \prime } \times D }$ , the reweighted feature map for class c is defined as

![](images/893b725ddc10d0d41c0acf48d7a0fa0216ceb6b3effa54b259e0d20c4fab4d6f.jpg)  
Figure 5: Support-guided feature reweighting. The support-derived vector $\mathbf { W } _ { c }$ performs channel-wise gating on the query feature map $\mathbf { F } _ { j }$ (equivalently, a dynamic depthwise 1×1 Conv1D), producing a class-specific fea ture map $\mathbf { F } _ { j , c } .$

$$
\mathbf {F} _ {j, c} = \operatorname{DynConv1D} \left(\mathbf {F} _ {j}; \mathbf {W} _ {c}\right) \in \mathbb {R} ^ {L ^ {\prime} \times D}.\tag{6}
$$

In our implementation, this operation reduces to channel wise gating at each position.

$$
\begin{array}{l} \mathbf {F} _ {j, c} [ t, d ] = \mathbf {F} _ {j} [ t, d ] \cdot \mathbf {W} _ {c} [ d ], \\ t = 1, \ldots , L ^ {\prime}, d = 1, \ldots , D. \end{array}\tag{7}
$$

We apply Eq. (6) to each target class and obtain $\{ \mathbf { F } _ { j , c } \} _ { c = 1 } ^ { C } ,$ which are then fed into the presence detection head (§ 4.5).

Why channel reweighting is the right “matching” operation. The crucial difference between this stage and the SE block in § 4.3 is where the channel weights come from and what they represent. SE performs intra-sample refinement by using a trace’s own global summary to modulate its channels. In contrast, MMF’s reweighting is cross-sample and class-conditioned. The vector Wc is derived from the single-tab supports of class c and specifies which channel semantics should be highlighted in the multi-tab query. This design yields a support-guided matching operation that is robust to interleaving and positional shifts, laying the foundation for per-class presence prediction.

## 4.5 Presence Detection

Given the class-conditioned feature maps $\{ \mathbf { F } _ { j , c } \} _ { c = 1 } ^ { C }$ produced in § 4.4, MMF performs presence detection to determine whether each target website is present in an obfuscated multi-tab trace. Although feature reweighting suppresses class-irrelevant channels, heavy interleaving can still induce long-range and diffuse correlations in the sequence representation. We therefore adopt Top-m self-attention (as used in ARES [13]) to retain only the most salient interactions. Target evidence can be sparse and scattered, whereas interference tends to create dif fuse yet uninformative correlations. Pruning attention to the top-m links mitigates this diffusion while preserving a small set of informative long-range dependencies.

In addition, real browsing sessions may exhibit biased co-occurrence among websites, leading to weak but consistent cross-class dependencies in multi-tab traces. Although we do not inject any explicit preference over website combinations during training, we incorporate a cross-class attention module to model contextual interactions across classes. This allows each class decision to benefit from other classes’ representations in the realistic multi-tab traces, without requiring any prior knowledge or explicit enumeration of website combinations.

Next, we formulate presence detection. Let $\hat { \mathbf { F } } _ { j , c } \in$ $\mathbb { R } ^ { T \times D }$ denote the reweighted feature sequence for class c (we use $T = L ^ { \prime } )$ ). We first add positional embeddings to obtain

$$
\mathbf {H} _ {j, c} = \hat {\mathbf {F}} _ {j, c} + \mathbf {P}, \quad \mathbf {P} \in \mathbb {R} ^ {T \times D}.\tag{8}
$$

We then apply $L { = } 2$ stacked Top-m self-attention layers:

$$
\mathbf {H} _ {j, c} \leftarrow \operatorname{TopMAttn} (\mathbf {H} _ {j, c}), \quad \text { repeated   } L \text {   times },\tag{9}
$$

where each layer computes scaled dot-product attention and masks all but the top-m attention scores per query position before softmax normalization. We aggregate along time to obtain a class vector:

$$
\mathbf {g} _ {j, c} = \operatorname{Pool} (\mathbf {H} _ {j, c}) \in \mathbb {R} ^ {D},\tag{10}
$$

where Pool(·) is implemented as mean pooling over the $T$ positions.

To incorporate cross-class context, we stack the perclass vectors into $\mathbf { G } j = [ \mathbf { g } j , 1 ; \ldots ; \mathbf { g } j , C ] \in \mathbb { R } ^ { C \times D }$ and apply $L \times = 2$ layers of cross-class attention:

$$
\mathbf {G} _ {j} \leftarrow \text { CrossClassAttn } (\mathbf {G} _ {j}), \quad \text { repeated   } L _ {\times} \text {   times.   (11) }
$$

Finally, an MLP produces an independent presence logit for each class:

$$
z _ {j, c} = \operatorname{MLP} \left(\mathbf {G} _ {j, c}\right), p _ {j, c} = \sigma \left(z _ {j, c}\right), c = 1, \dots , C,\tag{12}
$$

where $\sigma ( \cdot )$ is the sigmoid function and $p _ { j , c }$ is the predicted probability that website c is present in query j. Training objective. Given the multi-hot presence label $\mathbf { y } _ { j } \in \{ 0 , 1 \} ^ { C }$ for query $j ,$ we optimize a weighted binary cross-entropy to address extreme class imbalance:

$$
\begin{array}{c} \mathcal {L} _ {\mathrm{WBCE}} = \frac {1}{C} \sum_ {c = 1} ^ {C} \Big (- \alpha y _ {j, c} \log \sigma (z _ {j, c}) \\ - (1 - y _ {j, c}) \log \big (1 - \sigma (z _ {j, c}) \big) \Big), \end{array}\tag{13}
$$

where $\alpha > 1$ up-weights positive classes and is set according to the empirical positive ratio. This objective keeps the detector sensitive to rare positives while preventing the optimization from being dominated by abundant negatives.

## 5 Evaluation

In this section, we evaluate MMF on thefew-shot multi tab WF task using both public datasets and a selfcollected dataset. We compare MMF against representative state-of-the-art baselines under matched experi mental settings. Our evaluation addresses the following questions: (1) Base Performance. Does MMF preserve strong base multi-tab performance, or does it trade off base performance for few-shot adaptability? (2) Few-Shot Adaptability. How does MMF perform in the stan dard few-shot multi-tab setting when onboarding unseen websites? (3) Scalability. How does the performance of MMF evolve as the number of unseen classes grows? (4) Robustness to Tab Dynamics. Can MMF remain robust under tab-count mismatch (dynamic and unknown numbers of tabs) during both base training and few-shot fine-tuning? (5) Resistance to Defenses. Is MMF more robust than prior works when different defense mecha nisms are deployed? (6) Open-World Robustness. Is MMF’s presence-detection formulation robust in the open-world setting with unmonitored background traf fic? (7) Stress Test. Is MMF more robust than baselines in higher tab counts and heavier interleaving scenarios? (8) Real-World Drift Effectiveness. Is MMF more effective than baselines in multi-tab settings under more realistic network conditions? (9) Analysis of Inference Overhead. Is the framework of MMF more efficient than prior onboarding frameworks?

## 5.1 Experimental Setup

Implementation. We implemented MMF in PyTorch. The hyperparameters of MMF are listed in Table 2.

Datasets. We use two data sources: (i) a self-collected dataset with real multi-tab traces and aligned single tab traces, and (ii) synthetically mixed multi-tab traces constructed from a widely used public single-tab WF dataset [12, 39].

Self-collected dataset. We extend the ARES data collection pipeline [13] to enable simultaneous acquisi tion of (a) mixed multi-tab traces and (b) their corresponding single-tab traces on the same machine. Concretely, we first select 50 popular websites based on public popu larity rankings. For each tab count setting in {3,4,5}, we randomly generate 20,000 website tab combinations and visit each of them three times. In parallel, we collect 30 single-tab visits per website to construct the single-tab traces. The collection spans approximately two months and uses servers located in Singapore. Further details are provided in Appendix A.2.

We further select 25 additional websites to expand the monitored set. For each newly added website, we generate only 25 combinations and collect 20 visits per combination, resulting in a data-limited scenario.

Table 2: Key hyperparameters used in our evaluation.

<table><tr><td>Component</td><td>Hyperparameter</td><td>Value</td></tr><tr><td rowspan="3">Episode sampling</td><td>Query length ( $L_q$ )</td><td>20000</td></tr><tr><td>Support length ( $L_s$ )</td><td>10000</td></tr><tr><td>Shots per class ( $K$ )</td><td>5</td></tr><tr><td rowspan="2">Input / dimension</td><td>Input channels</td><td>2 (direction, mask)</td></tr><tr><td>Output channels ( $D$ )</td><td>256</td></tr><tr><td rowspan="3">Model</td><td>DF blocks</td><td>4</td></tr><tr><td>#Top- $m$  self-attn layers ( $L$ )</td><td>2</td></tr><tr><td>#Cross-class attn layers ( $L_x$ )</td><td>2</td></tr><tr><td rowspan="5">Training</td><td>Loss</td><td>Weighted BCE</td></tr><tr><td>Dropout</td><td>0.15</td></tr><tr><td>Optimizer</td><td>Adam</td></tr><tr><td>Learning rate</td><td> $5 \times 10^{-5}$ </td></tr><tr><td>Weight decay</td><td> $10^{-4}$ </td></tr></table>

Public dataset with multi-tab synthesis. Existing public multi-tab datasets typically do not provide aligned single-tab visits for the same websites, which limits their use in support-guided few-shot evaluation. We therefore construct multi-tab traces for 60 base classes through controlled synthesis from public single-tab datasets. The resulting synthetic benchmark covers closed-world (CW) [39], open-world (OW) [39], and defended settings. For the defended setting, we use WTF-PAD [24] and Front [17], consistent with ARES [13]. All datasets are constructed from the same data source, WFlib [12], to ensure consistency across settings.

The synthesis code is built on TMWF’s mixing tool [22], which reports that synthetic traces can be harder to classify than multi-tab traces collected in the wild. We further improve the mixer to capture more realistic temporal relationships. Specifically, the original implementation enforces a strict overlap-ratio constraint to avoid cases where a long trace fully subsumes a shorter one. We relax this constraint and allow both partial overlap and full containment between tabs, which better reflects real browsing. We present details of the algorithm and data splits in Appendix A.1. The defended synthetic benchmark is used in § 5.6, the open-world synthetic benchmark is used in § 5.7, and the self-collected dataset is used only in § 5.9. The remaining experiments are conducted on the closed-world synthetic benchmark. Unless otherwise specified, we set $r _ { \operatorname* { m a x } } = 0 . 4$ in the synthesis algorithm.

Note that, for few-shot adaptation, we synthesize only a small number of samples for 30 novel websites. Each synthesized trace contains one novel website mixed with several base websites, and each novel website appears exactly K times in the query pool to match the K-shot setting.

Baselines. We compare MMF with representative multitab WF baselines, including BAPM [18], FMWF [31],

TMWF [22], and ARES [13]. These methods cover main stream design choices for multi-tab WF and few-shot multi-tab WF. We do not include few-shot single-tab WF methods as additional baselines because most assume mutually exclusive classification and rely on globally coherent metric geometry or fixed decision boundaries. These assumptions do not directly transfer to multi-tab traces [28, 40, 59, 60].

Metrics. Following the common multi-label evaluation protocol used in prior multi-tab WF studies [13], we report ROC-AUC and Precision@Top-k (P@k) for standard multi-tab evaluation. Let $p _ { i , c } \in [ 0 , 1 ]$ denote the predicted presence score of class c for query i, and let $y _ { i , c } \in \{ 0 , 1 \}$ denote the corresponding ground-truth presence label. We compute macro-averaged ROC-AUC over all monitored classes:

$$
\mathrm{AUC} = \frac {1}{C} \sum_ {c = 1} ^ {C} \mathrm{AUC} _ {\mathrm{ROC}} \left(\left\{y _ {i, c} \right\} _ {i = 1} ^ {N}, \left\{p _ {i, c} \right\} _ {i = 1} ^ {N}\right).\tag{14}
$$

For P@k, we rank all monitored classes by their predicted scores for each query i. Let k<sub>i</sub> denote the number of ground-truth monitored classes present in query i, and let ${ \mathrm { T o p } } { - } k _ { i } ( p _ { i } )$ be the corresponding set of top-ranked classes. We compute

$$
\mathrm{P} @ \mathrm{k} = \frac {1}{N} \sum_ {i = 1} ^ {N} \frac {1}{k _ {i}} \sum_ {c \in \operatorname{Top} - k _ {i} (p _ {i})} y _ {i, c}.\tag{15}
$$

For few-shot evaluations, we further consider whether newly incorporated websites can be identified from limited data. Accordingly, we report Novel P@k, which mea sures the precision of novel-class predictions selected in the Top-k set. Let $\boldsymbol { C _ { \mathrm { n o v e l } } }$ denote the set of novel classes. We have

$$
\text { Novel   P@k } = \frac {\sum_ {i = 1} ^ {N} \sum_ {c \in \mathcal {C} _ {\text { novel }}} \mathbb {I} [ c \in \operatorname{Top-} k _ {i} (p _ {i}) ] \cdot y _ {i , c}}{\sum_ {i = 1} ^ {N} \sum_ {c \in \mathcal {C} _ {\text { novel }}} \mathbb {I} [ c \in \operatorname{Top-} k _ {i} (p _ {i}) ]}.\tag{16}
$$

Novel Recall@k (R@k) is a recall-form variant based on the same calculation principle of Novel P@k, which can be formulated as:

$$
\text { Novel   R@k } = \frac {\sum_ {i = 1} ^ {N} \sum_ {c \in \mathcal {C} _ {\text { novel }}} \mathbb {I} [ c \in \operatorname{Top} - k _ {i} (p _ {i}) ] \cdot y _ {i , c}}{\sum_ {i = 1} ^ {N} \sum_ {c \in \mathcal {C} _ {\text { novel }}} y _ {i , c}}.\tag{17}
$$

## 5.2 Closed-World Multi-tab Evaluation

Few-shot capability should not come at the expense of standard multi-tab performance. In practice, an attacker may still collect substantial training data before deploy ment and train a model offline. Maintaining competitive performance in this standard multi-tab setting is therefore a prerequisite for a credible few-shot multi-tab framework.

Table 3: Closed-world (CW) multi-tab performance on the base monitored set. We report macro ROC-AUC and P@k for 3/4/5-tab settings.

<table><tr><td rowspan="2">Method</td><td colspan="2">3-tab</td><td colspan="2">4-tab</td><td colspan="2">5-tab</td></tr><tr><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td></tr><tr><td>BAPM</td><td>0.9076</td><td>0.7100</td><td>0.8783</td><td>0.6835</td><td>0.8352</td><td>0.6745</td></tr><tr><td>FMWF</td><td>0.9825</td><td>0.9268</td><td>0.9698</td><td>0.8966</td><td>0.9490</td><td>0.8534</td></tr><tr><td>TMWF</td><td>0.9791</td><td>0.9193</td><td>0.9746</td><td>0.9346</td><td>0.9757</td><td>0.9372</td></tr><tr><td>ARES</td><td>0.9887</td><td>0.9466</td><td>0.9823</td><td>0.9260</td><td>0.9725</td><td>0.8962</td></tr><tr><td>MMF</td><td>0.9952</td><td>0.9313</td><td>0.9920</td><td>0.9256</td><td>0.9899</td><td>0.9215</td></tr></table>

We first evaluate MMF in the closed-world (CW) multi-tab setting and compare it with representative baselines. Table 3 reports AUC and P@k for 3/4/5-tab settings. MMF achieves the best AUC performance across all tab counts. In the 3-tab setting, MMF achieves an AUC of 0.9952, outperforming the strongest baseline (ARES). Moreover, as the number of tabs increases from 3 to 5, MMF exhibits slight performance degradation, while other baselines suffer more noticeable drops. This stability suggests that the detection-centric formulation is less sensitive to tab counts. We further validate robustness under dynamic tab settings in § 5.5. Note that TMWF shows an increase in P@k, which is mainly due to its fixed maximum-tab setting, set to 6 by default [22].

## 5.3 Multi-tab Few-shot Adaptation on Unseen Websites

After establishing strong CW performance, we evaluate MMF in the core few-shot multi-tab setting. Starting from the checkpoint pre-trained in § 5.2, we introduce unseen websites as novel classes and perform few-shot fine-tuning using only K labeled traces per novel website. We vary $K \in \{ 5 , 1 0 , 1 5 , 2 0 , 3 0 \}$ } and evaluate under 3-5 tab queries, yielding 15 scenarios. Figure 6 reports Novel P@k.

The results show that existing multi-tab WF baselines exhibit limited few-shot adaptability. In extremely lowshot settings, baselines achieve low Novel P@k, and performance degrades further as the number of tabs increases from 3 to 5. This suggests that these approaches largely rely on decision structures learned in fully supervised CW training and adapt poorly with only a handful of new samples. We also tried both full-model fine-tuning and head-only updates with the hyperparameters from their open-source code, but neither produced satisfactory gains; BAPM can learn novel classes but exhibits severe base-class forgetting.

In contrast, MMF consistently outperforms all baselines across all tab counts and shot settings, and improves steadily with K. With only 20 samples per novel website, MMF achieves a Novel P@k close to 0.8. Moreover, under the most challenging 5-shot/5-tab and 10-shot/5- tab settings, MMF delivers over 300% relative improvement over prior methods. This advantage stems from episodic base training that learns a transferable support to-reweighting mechanism for extracting class-specific evidence from mixed traces. Moreover, the binary presence formulation avoids restructuring a fixed-cardinality classification head when the monitored set expands.

Table 4: Overall closed-world few-shot results after onboarding unseen websites. We report macro ROC-AUC and P@k over all monitored websites (base+novel) under different tab counts (3/4/5) and shot budgets (K shots per novel website).

<table><tr><td rowspan="2">Method (tabs)</td><td colspan="2">5-shot</td><td colspan="2">10-shot</td><td colspan="2">15-shot</td><td colspan="2">20-shot</td><td colspan="2">30-shot</td></tr><tr><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td><td>AUC</td><td>P@k</td></tr><tr><td>BAPM (3-tab)</td><td>0.7416</td><td>0.1863</td><td>0.7983</td><td>0.2712</td><td>0.8302</td><td>0.3324</td><td>0.8490</td><td>0.3697</td><td>0.8624</td><td>0.4007</td></tr><tr><td>FMWF (3-tab)</td><td>0.8083</td><td>0.5509</td><td>0.8342</td><td>0.5994</td><td>0.8472</td><td>0.6157</td><td>0.8548</td><td>0.6294</td><td>0.8632</td><td>0.6362</td></tr><tr><td>TMWF (3-tab)</td><td>0.8622</td><td>0.5881</td><td>0.8918</td><td>0.6138</td><td>0.8357</td><td>0.5989</td><td>0.9177</td><td>0.6355</td><td>0.9336</td><td>0.6842</td></tr><tr><td>ARES (3-tab)</td><td>0.8734</td><td>0.6370</td><td>0.9109</td><td>0.6669</td><td>0.9286</td><td>0.6932</td><td>0.9417</td><td>0.7137</td><td>0.9629</td><td>0.7675</td></tr><tr><td>MMF (3-tab)</td><td>0.9453</td><td>0.6825</td><td>0.9594</td><td>0.7302</td><td>0.9611</td><td>0.7399</td><td>0.9667</td><td>0.7612</td><td>0.9669</td><td>0.7824</td></tr><tr><td>BAPM (4-tab)</td><td>0.7147</td><td>0.2080</td><td>0.7697</td><td>0.2895</td><td>0.7906</td><td>0.3353</td><td>0.8076</td><td>0.3640</td><td>0.8218</td><td>0.3933</td></tr><tr><td>FMWF (4-tab)</td><td>0.7746</td><td>0.6090</td><td>0.8043</td><td>0.6524</td><td>0.8210</td><td>0.6680</td><td>0.8272</td><td>0.6754</td><td>0.8308</td><td>0.6774</td></tr><tr><td>TMWF (4-tab)</td><td>0.8464</td><td>0.6773</td><td>0.8632</td><td>0.6632</td><td>0.8628</td><td>0.6928</td><td>0.8873</td><td>0.7094</td><td>0.9042</td><td>0.6916</td></tr><tr><td>ARES (4-tab)</td><td>0.8511</td><td>0.6884</td><td>0.8792</td><td>0.6975</td><td>0.9018</td><td>0.7140</td><td>0.9162</td><td>0.7293</td><td>0.9380</td><td>0.7574</td></tr><tr><td>MMF (4-tab)</td><td>0.9362</td><td>0.7189</td><td>0.9507</td><td>0.7592</td><td>0.9572</td><td>0.7812</td><td>0.9610</td><td>0.7923</td><td>0.9669</td><td>0.7995</td></tr><tr><td>BAPM (5-tab)</td><td>0.6993</td><td>0.2460</td><td>0.7464</td><td>0.3286</td><td>0.7645</td><td>0.3644</td><td>0.7799</td><td>0.3939</td><td>0.7877</td><td>0.4181</td></tr><tr><td>FMWF (5-tab)</td><td>0.7531</td><td>0.6345</td><td>0.7947</td><td>0.6788</td><td>0.8078</td><td>0.6790</td><td>0.8110</td><td>0.6866</td><td>0.8125</td><td>0.6811</td></tr><tr><td>TMWF (5-tab)</td><td>0.8393</td><td>0.7273</td><td>0.8562</td><td>0.7410</td><td>0.8277</td><td>0.7420</td><td>0.8847</td><td>0.7570</td><td>0.9175</td><td>0.7821</td></tr><tr><td>ARES (5-tab)</td><td>0.8352</td><td>0.7078</td><td>0.8565</td><td>0.7125</td><td>0.8650</td><td>0.7150</td><td>0.8811</td><td>0.7267</td><td>0.9078</td><td>0.7409</td></tr><tr><td>MMF (5-tab)</td><td>0.9219</td><td>0.7364</td><td>0.9384</td><td>0.7635</td><td>0.9505</td><td>0.7869</td><td>0.9543</td><td>0.7964</td><td>0.9584</td><td>0.8048</td></tr></table>

![](images/6a42f0761fb8c477398cd6416c8aa48b9722441e2ed42dbffda1b1a8a94ba34d.jpg)

![](images/e1b7ef7daa67044a310eb89a4adf3cfac830ac44913b052cf5183f8ad80944d1.jpg)

![](images/16ae7703b6e9e35d99025e073c2deb42a4d6d21596712c5d7d6df173640b7bab.jpg)

![](images/cf7714b3d3af11989334acaf52b8c8708d4e1f9520f613e0af813c571206db66.jpg)

![](images/8f4f827f59ef98f5435f9670011d881063cccbd2c7a808dc525c7587a8079a4e.jpg)  
Figure 6: Few-shot onboarding under closed-world multi-tab settings. We report Novel P@k for unseen websites across tab counts (3/4/5 tabs) and shot budgets (K ∈ {5,10,15,20,30}).

Beyond Novel P@k, Table 4 reports the overall AUC and P@k computed over all monitored websites (base+novel) after adaptation. Most baselines fail to learn novel classes, yet their overall scores drop less because the metric is dominated by base classes learned during CW training. Even under this metric, MMF achieves the best performance and remains the most stable method across all shot and tab settings.

## 5.4 Multi-tab Continual Onboarding under Expanding Monitored Set

After validating few-shot adaptation under a fixed novelset size, we consider a more deployment-realistic setting in which the monitored set continuously expands over time. We fix the available samples to 20-shot per unseen website and progressively increase the number of novel classes from 5 to 35. For each setting, we evaluate novel website detection quality (Novel P@k), under 3/4/5-tab settings.

As shown in Figure 7, prior baselines degrade steadily as the monitored set grows. Most baselines quickly drop to low Novel P@k and remain there as the monitored set expands. In contrast, MMF remains markedly more scalable and stable across all tab settings. Its Novel P@k consistently stays around 0.75, whereas baselines progressively collapse to 0.1–0.2 under the most challenging 5-tab condition.

Table 5: Few-shot fine-tuning under tab-count mismatch. Models are fine-tuned under a fixed tab-count variant (3/4/5) or mixed-tab variant, and evaluated on the same mixed-tab test set (2–5 tabs). We report Overall ROC-AUC/P@k (base+novel) and Novel P@k.

<table><tr><td rowspan="2"></td><td colspan="3">3-tab train</td><td colspan="3">4-tab train</td><td colspan="3">5-tab train</td><td colspan="3">mixed-tab train</td></tr><tr><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td></tr><tr><td>BAPM</td><td>0.8399</td><td>0.3599</td><td>0.3076</td><td>0.8357</td><td>0.3251</td><td>0.3789</td><td>0.8300</td><td>0.3333</td><td>0.3274</td><td>0.8462</td><td>0.3821</td><td>0.3146</td></tr><tr><td>FMWF</td><td>0.8303</td><td>0.5944</td><td>0.1135</td><td>0.8187</td><td>0.5912</td><td>0.1062</td><td>0.8157</td><td>0.5854</td><td>0.0982</td><td>0.8468</td><td>0.6053</td><td>0.1190</td></tr><tr><td>TMWF</td><td>0.9127</td><td>0.6106</td><td>0.2394</td><td>0.9001</td><td>0.6181</td><td>0.2663</td><td>0.9185</td><td>0.6383</td><td>0.3176</td><td>0.9213</td><td>0.6351</td><td>0.2481</td></tr><tr><td>ARES</td><td>0.9311</td><td>0.6901</td><td>0.3541</td><td>0.9271</td><td>0.6610</td><td>0.3486</td><td>0.9135</td><td>0.6251</td><td>0.2591</td><td>0.9388</td><td>0.7130</td><td>0.3918</td></tr><tr><td>MMF</td><td>0.9612</td><td>0.7761</td><td>0.7290</td><td>0.9661</td><td>0.7892</td><td>0.8248</td><td>0.9653</td><td>0.7871</td><td>0.8184</td><td>0.9717</td><td>0.8111</td><td>0.7468</td></tr></table>

![](images/7aae114a3cf4c1687fbfe42e7e01ff87e7af765114141deee4d36f4b743f4617.jpg)  
Figure 7: Continual onboarding under an expanding monitored set (20-shot per newly added website). We report Novel P@k as the number of novel classes increases, under 3/4/5-tab mixtures.

## 5.5 Robustness to Dynamic Tab Settings

As discussed in § 3, the number of concurrently opened tabs is dynamic and typically unknown a priori, making it impractical to train and deploy a separate model for each tab count. While some multi-tab attacks attempt to relax this assumption, many prior designs still rely on a fixed tab count or an explicit upper bound to be effective [18, 22,31]. MMF’s decoupled presence detection is designed to reduce the reliance on a fixed tab-count configuration. We therefore evaluate MMF under a dynamic setting where the test set is a mixed-tab collection consisting of 2/3/4/5-tab traces.

We evaluate few-shot adaptation under tab-count mismatch. At the base-training stage, we train each model under four variants (3-tab, 4-tab, 5-tab, and mixed-tab). At the few-shot stage, we load the corresponding base checkpoints, fine-tune them under the same variant setting, and then evaluate on the mixed-tab test set again. We report Overall AUC/P@k together with Novel P@k in Table 5, and plot novel precision–recall curves in Figure 8 to characterize the precision–recall trade-off induced by the decision threshold.

Table 5 shows that MMF is largely insensitive to tab count configuration. Even when trained on fixed 3-tab data, MMF achieves an AUC of 0.9612 on the mixed tab test set, within 0.01 of training directly on mixed-tab data. This observation is consistent with § 5.2, suggesting that MMF’s class-conditioned reweighting and presencedetection formulation remains stable under varying tab settings.

Besides, starting from any base checkpoint (3/4/5/mixed), MMF consistently attains the best Overall AUC/P@k and substantially higher Novel P@k than all baselines, indicating that MMF can identify novel classes even when the tab count varies at test time. Figure 8 provides a finer-grained view. Across all four settings, MMF’s curves stay closer to the upper-right corner, indicating a better precision–recall trade-off for novel classes. (The curves can appear slightly jagged because they are computed over novel classes only. We do not report PR curves for FMWF due to its low performance in these settings.)

## 5.6 Robustness to WF Defenses

After evaluating MMF in standard multi-tab and fewshot settings, we further examine its robustness under website fingerprinting defenses. Specifically, we adopt datasets generated by two widely-recognized defense mechanisms in the WF community [17, 24], and follow the same few-shot protocol as in § 5.3 (3–5 tabs with 5–30 shots) to assess low-data adaptation under strong obfuscation. We report Novel P@k for consistency.

Figure 9 shows that defenses substantially increase the difficulty of few-shot multi-tab WF. All methods suffer pronounced performance drops due to the injected noise and disrupted patterns. Notably, even ARES, which is designed to be robust against WF defenses, fails to remain reliable in this setting, with Novel P@k dropping below 0.25. In contrast, MMF consistently achieves higher and more stable precision under both defenses. This suggests that MMF’s decoupled paradigm can relatively better focus on target-related local evidence even when global traffic signatures are heavily distorted. Overall, the results indicate that MMF remains the most robust and practical design among all compared approaches in the low-data and strong-defense settings.

Precision (Novel)  
![](images/4de2650263897c2e3b2d5ec13d9801afa31c1dbbad5f1200baa263b207dfbdb5.jpg)  
(a) 3-tab setting

![](images/4645a74d2b2649d0c4d8320c20cdb24fca487252b3ab8430015423950d32592e.jpg)  
recision (Novel) (b) 4-tab setting

![](images/3cb70f2ae3a4439dc571c1eff5f0f5e57641d7644fd2639b3c74e056b481205d.jpg)  
(c) 5-tab setting

![](images/2144fb59315a388f2a7059813a61dc7dbf10a08c7ae9414e07332c755f264f5c.jpg)  
(d) mixed-tab setting

Figure 8: Novel Precision–Recall trade-offs under dynamic tab settings. We plot Novel Precision versus Novel Recall induced by varying threshold, evaluated on the mixed-tab test set (2–5 tabs).  
![](images/8b9593f7db79bcadf930c4e8e2a97ada980420f51b4c5ae8a2cb4fa46e12d6b2.jpg)

![](images/2938058df1f9176da0d0ae92166b072a841fb2b30fad23253908e926a76653c2.jpg)  
Figure 9: 20-shot performance under defended multi-tab settings. We report Novel P@k across tab counts (3/4/5 tabs).

## 5.7 Robustness to Open-World Scenarios

We evaluate MMF’s robustness to background traffic from unmonitored websites and further introduce a distri bution shift to emulate deployment dynamics. Concretely, we synthesize open-world traces with $r _ { \operatorname* { m a x } } = 0 . 2$ during base training, but increase it to $r _ { \operatorname* { m a x } } = 0 . 4$ during fewshot fine-tuning, yielding stronger interleaving patterns than those seen during pre-training. As the influence of tab settings has been shown in § 5.3, we only report results in the 4-tab setting here.

As shown in Table 6, MMF remains stable and achieves the best performance under this shift. We fur ther visualize the learned reweighting coefficients for 20 classes in Figure 10. The heatmap shows that dif ferent classes activate and suppress markedly different channel combinations. The t-SNE plot shows clear class wise clustering of the reweighting vectors across multiple inference runs. These observations indicate that MMF learns stable class-specific channel patterns rather than being dominated by open-world background noise. During detection, MMF amplifies channels relevant to the target class, whereas spurious patterns introduced by unmonitored traffic lack a corresponding class-conditioned selector and are therefore less likely to produce stable responses.

Table 6: Open-world (OW) robustness under distribution mismatch (4-tab). We report Overall P@k and Novel P@k after few-shot adaptation.

<table><tr><td></td><td>BAPM</td><td>FMWF</td><td>TMWF</td><td>ARES</td><td>MMF</td></tr><tr><td>P@k</td><td>0.3574</td><td>0.6520</td><td>0.7063</td><td>0.6669</td><td>0.7782</td></tr><tr><td>Novel P@k</td><td>0.1775</td><td>0.0620</td><td>0.1520</td><td>0.1343</td><td>0.6236</td></tr></table>

## 5.8 Robustness to Higher Tab Counts and Heavier Interleaving Scenarios

To further explore the influence of tab counts and overlap ratios, we conduct two additional experiments. First, we consider heavier traffic interleaving. As described in § 5.1, our synthesis procedure follows the multi-tab mixing algorithm of TMWF [22], but removes its strict overlap-ratio constraint. The original TMWF mixer computes the overlap window with respect to the shorter of two traces, thereby avoiding cases where a long trace fully subsumes a shorter one. In contrast, our mixer computes the overlap window based on the duration of the previous trace. Thus, when a long trace is followed by a shorter trace, the actual overlap ratio can exceed the configured $r _ { \mathrm { m a x } }$ , and the shorter trace can even be entirely contained in the longer one. Figure 11 shows the distribution of actual overlap ratios between adjacent trace pairs under different $r _ { \mathrm { m a x } }$ values. Even when $r _ { \mathrm { m a x } } = 0 . 4 , 7 . 0 1$ % of adjacent pairs already involve full containment; when $r _ { \mathrm { m a x } } = 0 . 7$ , this fraction increases to 14.80%. We therefore further evaluate the 4-tab setting with $r _ { \operatorname* { m a x } } = 0 . 5$ and $r _ { \mathrm { m a x } } = 0 . 7$ to test whether MMF remains robust under heavier interleaving.

![](images/06b1b3f76bdd7d98bd0b12e4cd8bfcf16c973b75d60f318928e185f04b84d0e9.jpg)

![](images/c9751c250674761ef96dcb91e9871124f1e194a89bb50fcc6b0f2d207b83e892.jpg)  
Figure 10: Visualization of class-conditioned reweighting under open-world interference. Left: heatmap of reweighting coefficients over feature channels for 20 classes. Right: t-SNE projection of the corresponding reweighting vectors, showing per-class clustering across multiple inference rounds

Table 7: Higher tab counts and heavier traffic interleaving robustness. We report Overall ROC-AUC/P@k and Novel P@k after few-shot adaptation (20-shot).

<table><tr><td rowspan="2"></td><td colspan="3"> $r_{\text{max}} = 0.5,4$ -tab</td><td colspan="3"> $r_{\text{max}} = 0.7,4$ -tab</td><td colspan="3"> $r_{\text{max}} = 0.2,6$ -tab</td><td colspan="3"> $r_{\text{max}} = 0.2,8$ -tab</td></tr><tr><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td><td>AUC</td><td>P@k</td><td>Novel P@k</td></tr><tr><td>BAPM</td><td>0.8021</td><td>0.3593</td><td>0.2514</td><td>0.7611</td><td>0.2943</td><td>0.2052</td><td>0.7397</td><td>0.3829</td><td>0.1910</td><td>0.6735</td><td>0.3364</td><td>0.1446</td></tr><tr><td>FMWF</td><td>0.8228</td><td>0.6656</td><td>0.1527</td><td>0.8123</td><td>0.6188</td><td>0.1921</td><td>0.8023</td><td>0.7013</td><td>0.0407</td><td>0.7503</td><td>0.6166</td><td>0.0417</td></tr><tr><td>TMWF</td><td>0.8467</td><td>0.6938</td><td>0.0988</td><td>0.8329</td><td>0.6472</td><td>0.1160</td><td>0.8097</td><td>0.8419</td><td>0.0550</td><td>0.8386</td><td>0.8498</td><td>0.0479</td></tr><tr><td>ARES</td><td>0.8292</td><td>0.6668</td><td>0.0650</td><td>0.8105</td><td>0.6427</td><td>0.0770</td><td>0.8467</td><td>0.7389</td><td>0.0949</td><td>0.8026</td><td>0.6848</td><td>0.0618</td></tr><tr><td>MMF</td><td>0.9577</td><td>0.7818</td><td>0.7330</td><td>0.9203</td><td>0.6958</td><td>0.6344</td><td>0.9503</td><td>0.8734</td><td>0.7121</td><td>0.9282</td><td>0.8587</td><td>0.6796</td></tr></table>

![](images/23b53032c0f4f97889cecdfe38022107e9c207bc7326e247b52c9c87b097f963.jpg)  
Figure 11: Actual overlap distribution under different interleaving levels in the 4-tab scenario.

Second, we evaluate higher tab counts. Prior browser behavior studies [15, 21, 35] show that the number of simultaneously active tabs follows a long-tailed distri bution, and sessions with more than four or five concur rently loading tabs are relatively uncommon. Existing multi-tab WF studies [13, 18, 31] therefore mostly focus on settings with at most five tabs. Nevertheless, MMF performs class-wise presence detection rather than fixedcardinality combination classification, its prediction process is not inherently tied to a fixed number of concurrent tabs. To examine this property, we additionally construct 6-tab and 8-tab synthetic datasets and evaluate MMF with larger tab counts.

As shown in Table 7, heavier interleaving degrades all methods. This degradation is expected, as denser temporal overlap disrupts more local features and makes targetrelated patterns harder to separate from mixed traces. Nevertheless, MMF still achieves the best performance. This result suggests that channel reweighting, together with local feature extraction, helps reduce the interference caused by heavily interleaved traffic.

As the number of tabs increases, the fine-tuning traces become increasingly dominated by base classes, because each novel class still appears only in K shots. This makes novel-class adaptation more difficult, especially for strong multi-tab baselines that are primarily optimized to preserve knowledge of base classes. Larger tab counts have a milder impact on MMF than heavier overlap ratios: the Overall P@k decreases by only about 0.015. This indicates that MMF’s presence-detection formulation remains relatively stable when more tabs are mixed. Nevertheless, an operational tab-count threshold may still exist for current WF methods, as they commonly rely on fixed-length inputs. Quantitatively identifying this threshold is difficult because the degradation is jointly affected by tab count, trace length and website complexity. We further discuss this limitation in § 6.

Table 8: Multi-tab performance on the real-world col lected data. We report Overall P@k and novel P@k in few-shot fine-tuning stage (20shot) under 3/4/5-tab set tings.

<table><tr><td rowspan="2">Method</td><td colspan="2">3-tab</td><td colspan="2">4-tab</td><td colspan="2">5-tab</td></tr><tr><td>P@k</td><td>Novel P@k</td><td>P@k</td><td>Novel P@k</td><td>P@k</td><td>Novel P@k</td></tr><tr><td>BAPM</td><td>0.3067</td><td>0.3153</td><td>0.2445</td><td>0.2488</td><td>0.2476</td><td>0.1651</td></tr><tr><td>FMWF</td><td>0.5280</td><td>0.3935</td><td>0.4270</td><td>0.2632</td><td>0.4456</td><td>0.1252</td></tr><tr><td>TMWF</td><td>0.5073</td><td>0.3992</td><td>0.5200</td><td>0.3165</td><td>0.5396</td><td>0.2870</td></tr><tr><td>ARES</td><td>0.5820</td><td>0.4784</td><td>0.5360</td><td>0.3005</td><td>0.5292</td><td>0.1421</td></tr><tr><td>MMF</td><td>0.6187</td><td>0.5915</td><td>0.5960</td><td>0.5450</td><td>0.5484</td><td>0.4702</td></tr></table>

## 5.9 Real-World Multi-tab Evaluation

To further validate MMF under realistic conditions, we conduct a real-world multi-tab traffic collection study. Considering concept drift, we do not attempt to control or eliminate distribution shifts caused by collection time, network conditions, or evolving website content. Instead, we deliberately spread all tab-combination visits across an approximately two-month window, so that training and testing traces inevitably exhibit temporal and environmental mismatch, resembling what an attacker would face when maintaining a deployed model over time.

Table 8 reports the Overall P@k and Novel P@k results for the fine-tuning stage (20-shot). Compared to the controlled setting in § 5.3, all methods suffer a noticeable degradation, with P@k drops exceeding 20%, confirm ing that concept drift substantially challenges multi-tab WF models, while MMF maintains relatively higher performance. This suggests that existing multi-tab attacks tend to rely on large-scale retraining to recover accuracy under drift, while MMF can remain relatively effective with few-shot adaptation.

## 5.10 Scalability and Inference Overhead

In practical deployment, the monitored set may grow over time as new websites are added. Therefore, beyond reducing data-collection cost and supporting few-shot onboarding, the inference overhead induced by an expand ing monitored set is also an important consideration for practical few-shot multi-tab WF. We conduct a focused scalability analysis by measuring inference latency and peak GPU memory as the number of monitored classes increases.

To the best of our knowledge, ARES [13] is the only existing multi-tab WF framework that explicitly supports website onboarding through a generic one-vs-all archi tecture. It maintains a separate binary classifier for each monitored class and adds a new classifier whenever a new class is added. Following this deployment setting, we adapt FMWF [31] and BAPM [18] into one-vs-all framework, as they follow the same classification-centric formulation as ARES. We then compare these adapted

![](images/63942bea88f515e17c52d09a86b423b2cfb48ac74d2423292d2ff3825d16f424.jpg)

![](images/e4bd2a78e865ea2b4df475e16f791950c658ee3b873afb8e521451a8f1d076e5.jpg)  
Figure 12: Latency and peak GPU memory as the number of monitored classes increases.

baselines with MMF.

Figure 12 shows the results. The latency of the one-vsall framework grows almost linearly with the number of monitored classes, because inference requires forwarding the query through C independent binary classifiers. Their peak GPU memory also increases with the monitored set size, as class-specific models need to be maintained during the inference stage. In contrast, MMF maintains a single shared feature extractor and prediction head. Although MMF applies class-specific reweighting for each monitored class, its overhead is much lower because the query feature map is extracted only once and then reused across class-wise predictions.

MMF’s peak GPU memory remains nearly constant as the monitored set grows, since the additional memory required by cached reweighting vectors is much smaller than the cost of maintaining separate binary models. Among the one-vs-all baselines, FMWF shows lower inference latency but higher GPU memory usage than the other adapted baselines. This is likely due to its shorter operator path without attention layers, together with a large flattened fully connected layer. We note that the one-vs-all framework may reduce latency through more aggressive parallelization, at the cost of additional memory and hardware resources. However, such optimization does not remove the underlying scaling issue that the architecture must maintain and execute class-specific classifiers as the monitored set grows.

## 5.11 Ablation Study

Next, we conduct an ablation study under the 4-tab setting to quantify the contribution of each MMF component. Table 9 shows that replacing any core module substantially degrades performance in the standard multi-tab setting, indicating that these design choices are all important. Specifically, (i) replacing the Trace Encoding module with a simple CNN feature extractor and using an MLP to directly predict the reweighting vector reduces P@k to 0.3134; (ii) replacing the Presence Detection head with a plain MLP head yields an P@k of 0.8423; and (iii) substituting the dynamic reweighting coefficients in Feature Reweighting with a fixed per-class combination representation decreases P@k to 0.7432. These results suggest that MMF’s performance arises from the interplay among its components rather than any single module in isolation.

Table 9: Ablation analysis of MMF (4-tab).

<table><tr><td>Trace Encoding</td><td>Feature Reweighting</td><td>Presence Detection</td><td>P@k</td></tr><tr><td>×</td><td>√</td><td>√</td><td>0.3134</td></tr><tr><td>√</td><td>√</td><td>×</td><td>0.8423</td></tr><tr><td>√</td><td>×</td><td>√</td><td>0.7432</td></tr><tr><td>√</td><td>√</td><td>√</td><td>0.9591</td></tr></table>

## 6 Discussion

Research on more practical architectures and benchmarks. MMF advances practical few-shot multi-tab WF by removing the known-tab-count assumption and supporting efficient class updates with limited data. In realistic deployments, the number of concurrent tabs is often unknown, and mismatches between the assumed and actual tab counts are common. Future multi-tab WF studies should therefore evaluate attacks under this setting. However, our work still has two limitations.

First, although MMF achieves lower inference latency and GPU usage than prior onboarding-capable one-vs-all approaches for multi-tab WF [13], the feature reweight ing module still introduces additional computation as the monitored set grows. Designing more scalable archi tectures for large monitored sets remains an important direction for future work.

Second, we do not yet provide a full end-to-end benchmark with human-subject data collection. Such bench marks remain scarce in the community due to the substan tial collection effort involved, as well as the associated ethical and privacy challenges. Building realistic end to-end benchmarks would be a meaningful step toward more practical WF research.

Difficulty of quantifying a concurrent-tab threshold. The difficulty of identifying a precise tab-count threshold at which multi-tab WF becomes unreliable is closely tied to how current WF pipelines extract features from mixed traces. The feature extractor of current WF meth ods typically operates on fixed-length inputs, resulting the amount of useful evidence retained depends on the websites’ loading behavior and trace length. Our prelim inary analysis shows that even with a fixed tab count, performance can vary due to the varying complexity of the mixed websites. Specifically, when using mediumlength traces as targets and mixing them with three short or three long traces, the recognition rates are 94.93% and 77.43%, respectively. Therefore, varying only the tab count does not fully isolate the effect of tab concurrency itself. This is a broader limitation of current multi-tab

WF evaluation. Future work could address this issue by developing variable-length WF architectures, which may enable a more systematic analysis of how concurrent-tab count affects attack reliability.

Research on concept drift and defenses in multi-tab few-shot settings. Concept drift and defense deployment introduce non-negligible distribution shifts in multi-tab WF, which can materially affect performance. Studying multi-tab WF under these scenarios remains challenging, and, to the best of our knowledge, ARES is one of the few works that explicitly investigates robustness against such factors. This challenge becomes even more pronounced in the few-shot setting. As shown in our evaluation, Front [17] can already substantially reduce the performance of all baseline methods. Meanwhile, recent WF defense research has moved beyond classical lightweight padding schemes, with newer defenses exploring more principled, optimization-driven, and cluster-aware traffic shaping, such as cluster-level traffic anonymization in Palette [38], gradient-guided sequence perturbation in GAPDiS [51], and adaptive per-cluster Tamaraw regularization over preconstructed anonymity sets in Adaptive Tamaraw [26]. Therefore, developing more robust trace representations against WF defenses is a meaningful direction. Moreover, recent robustness studies on traffic classification models, such as Cert-TA [54] and BARS [46], may also provide useful insights for building a systematic framework to understand robustness against different WF defenses in a unified manner.

## 7 Conclusion

In this paper, we propose MMF, a novel framework for few-shot website fingerprinting in the multi-tab scenario. MMF reformulates WF from classification to class-wise presence detection, which makes episodic learning welldefined under interleaving by pairing each mixed multitab query trace with single-tab support traces for monitored websites. MMF encodes each mixed query into a feature map, uses a weight generator to produce classconditioned reweighting vectors, and applies an attentionguided presence head to detect per-class evidence. This detection-centric formulation avoids requiring tab-count knowledge at inference time and supports continual onboarding of newly added websites from limited newly collected data, without expensive full retraining on large mixed-traffic datasets. Across extensive experiments on public and self-collected datasets, including closed-world and open-world settings, defense-aware evaluation, dynamic tab scenarios, and real-world drift, MMF consistently achieves stronger and more robust performance than prior baselines.

## Ethical Considerations

Website fingerprinting (WF) research is inherently dualuse: it can advance the understanding and mitigation of privacy risks in anonymous communication systems, while also potentially enabling misuse for surveillance or de-anonymization.

Stakeholders. Our study may impact: (i) users of anonymous communication systems, whose visited websites could be inferred from encrypted traffic; (ii) the Tor network and its ecosystem, including relay operators, maintainers, and defense developers, who may use our findings to assess practical WF risks and prioritize protocol- or system-level mitigations; (iii) system and defense operators who may use our findings to harden defenses; (iv) website operators/content providers, whose sites may be included in monitored sets in WF evaluations; and (v) the research community, which benefits from more real istic multi-tab benchmarks and reproducible evaluation pipelines.

Positive Impacts. Our primary goal is to support defense oriented security research. We systematically analyze robustness boundaries and help the community evaluate multi-tab WF under more deployment-aligned assump tions.

Rationale for Conducting and Publishing This Work. We conducted this research because the settings in our paper are closer to realistic browsing conditions than the simplified single-tab or data-abundant settings commonly used in prior WF studies. We believe that studying these realistic settings is necessary for improving privacy protections, rather than merely extending attack capabil ity for its own sake. We decided to publish this work because openly characterizing the threat boundary can help Tor developers, anonymity-system researchers, and the broader privacy community identify where existing assumptions may be insufficient and where stronger defenses are needed.

Potential Negative Impacts and Misuse Risks. Despite the above benefits, our technique could be misused to infer real users’ browsing activities, which may harm pri vacy and safety. Moreover, the focus on few-shot adap tation and continual onboarding, while motivated by the practical maintenance challenges of WF, may lower the operational barrier for attackers to keep models up-to date.

Mitigation Measures (Data Collection & Experimentation). All data used in this work are collected via automated crawling and scripted browsing sessions in a controlled environment. The collection process does not involve real users, user accounts, or any interaction with human subjects; we only record network traces generated by visiting public websites, and our datasets do not include personal identifiers, credentials, or other sensitive user information. We also adopt conservative crawling practices (e.g., bounded concurrency and rate limiting) to avoid imposing abnormal load on websites or anonymity networks, and we do not bypass access controls or collect login-gated content.

Responsible Release and Reproducibility. We follow common practices in the security research community: (1) we position the study as defense-motivated, explicitly discussing robustness boundaries and potential countermeasures; and (2) we prioritize reproducibility while being cautious about direct weaponization. Consistent with our Open science goal, we provide an anonymized artifact containing the implementation, configurations, and scripts required to reproduce dataset synthesis and experimental results.

## Open Science

To support reproducibility and facilitate evaluation of our core contributions, we provide public research artifacts that contain the source code, configuration files, and scripts required to reproduce our dataset synthesis and experimental results. The artifacts are available on Zenodo and GitHub<sup>2</sup>. The repositories include instructions for environment setup, running base training and few-shot fine-tuning, and reproducing the reported metrics and figures.

## Acknowledgement

We thank our shepherd and the anonymous reviewers for their insightful feedback. This work was supported in part by the National Key R&D Program of China under Grant 2024YFB2906803, the National Natural Science Foundation of China (NSFC) under Grant 62472247, the Key Research and Development Project of Jiangsu Province under Grant BE2023004-4, and the Science and Technology Innovation Program of Hunan Province under Grant 2024RC3139.

## References

[1] Kota Abe and Shigeki Goto. Fingerprinting attack on tor anonymity using deep learning. Proceedings ofthe Asia-Pacific Advanced Network, 42(0):15–20, 2016.

[2] Amit Alfassy, Leonid Karlinsky, Amit Aides, Joseph Shtok, Sivan Harary, Rogerio Feris, Raja Giryes, and Alex M Bronstein. Laso: Label-set

operations networks for multi-label few-shot learning. In Proceedings ofthe IEEE/CVF conference on computer vision and pattern recognition, pages 6548–6557, 2019.

[3] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. Realistic website fingerprinting by augmenting network traces. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security, pages 1035–1049, 2023.

[4] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. Var-cnn: A data-efficient website fingerprinting attack based on deep learning. Proceed ings on Privacy Enhancing Technologies, 2019:292 – 310, 2018.

[5] Xiang Cai, Xin Cheng Zhang, Brijesh Joshi, and Rob Johnson. Touching from a distance: website fingerprinting attacks and defenses. In Computer and Communications Security, 2012.

[6] Hao Chen, Yali Wang, Guoyou Wang, and Yu Qiao. Lstd: A low-shot transfer detector for object detection. In Proceedings of the AAAI conference on artificial intelligence, volume 32, 2018.

[7] Mantun Chen, Yongjun Wang, and Xiatian Zhu. Few-shot website fingerprinting attack with metabias learning. Pattern Recognition, 130:108739, 2022.

[8] Heyning Cheng and Ron Avnur. Traffic analysis of ssl encrypted web browsing. Project paper, Univer sity ofBerkeley, 1998.

[9] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world. In 31st USENIX Security Symposium (USENIX Security 22), pages 753–770, 2022.

[10] Weiqi Cui, Tao Chen, Christian Fields, Julianna Chen, Anthony Sierra, and Eric Chan-Tin. Revisiting assumptions for website fingerprinting attacks. In Proceedings of the 2019 ACM asia conference on computer and communications security, pages 328–339, 2019.

[11] Xianwen Deng, Ruijie Zhao, Yanhao Wang, Ming wei Zhan, Zhi Xue, and Yijun Wang. Countmamba: A generalized website fingerprinting attack via coarse-grained representation and fine-grained prediction. In 2025 IEEE Symposium on Security and Privacy (SP), pages 1419–1437. IEEE, 2025.

[12] Xinhao Deng, Qi Li, and Ke Xu. Robust and reliable early-stage website fingerprinting attacks

via spatial-temporal distribution analysis. In Proceedings ofthe 2024 on ACM SIGSAC Conference on Computer and Communications Security, pages 1997–2011, 2024.

[13] Xinhao Deng, Xiyuan Zhao, Qilei Yin, Zhuotao Liu, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. Towards robust multi-tab website fingerprinting. arXiv preprint arXiv:2501.12622, 2025.

[14] Roger Dingledine, Nick Mathewson, and Paul Syverson. Tor: The second-generation onion router. In Proceedings of the 13th USENIX Security Symposium, 2004.

[15] Patrick Dubroy and Ravin Balakrishnan. A study of tabbed browsing among mozilla firefox users. In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems, pages 673–682, 2010.

[16] Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In Proceedings ofthe 34th International Conference on Machine Learning (ICML), 2017.

[17] Jiajun Gong and Tao Wang. Zero-delay lightweight defenses against website fingerprinting. In 29th USENIX security symposium (USENIX security 20), pages 717–734, 2020.

[18] Zhong Guan, Gang Xiong, Gaopeng Gou, Zhen Li, Mingxin Cui, and Chang Liu. Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor. In Proceedings of the 37th Annual Computer Security Applications Conference, pages 248–259, 2021.

[19] Jamie Hayes and George Danezis. k-fingerprinting: A robust scalable website fingerprinting technique. In USENIX Security Symposium, 2015.

[20] Dominik Herrmann, Rolf Wendolsky, and Hannes Federrath. Website fingerprinting: Attacking popular privacy enhancing technologies with the multinomial nave-bayes classifier. ACM, 2009.

[21] Jeff Huang and Ryen W White. Parallel browsing behavior on the web. In Proceedings of the 21st ACM conference on Hypertext and Hypermedia, pages 13–18, 2010.

[22] Z. Jin, T. Lu, S. Luo, and J. Shang. Transformerbased model for multi-tab website fingerprinting attack. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security (CCS), 2023.

[23] Marc Juárez, Sadia Afroz, Gunes Acar, Claudia Díaz, and Rachel Greenstadt. A critical eval uation of website fingerprinting attacks. Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security, 2014. URL: https://api.semanticscholar. org/CorpusID:5762455.

[24] Marc Juárez, Mohsen Imani, Mike Perry, Claudia Dıaz, and Matthew Wright. Wtf-pad: toward an efficient website fingerprinting defense for tor. CoRR, abs/1512.00524, 2015.

[25] Bingyi Kang, Zhuang Liu, Xin Wang, Fisher Yu, Jiashi Feng, and Trevor Darrell. Few-shot object detection via feature reweighting. In Proceedings ofthe IEEE/CVF International Conference on Computer Vision (ICCV), 2019.

[26] Khashayar Khajavi and Tao Wang. Lightening the load: A cluster-based framework for a loweroverhead, provable website fingerprinting defense. arXiv preprint arXiv:2509.01046, 2025.

[27] Lin Liu, Ziling Wei, Shuhui Chen, Zixuan Dong, and Jinshu Su. Fingermamba: Mamba-based efficient multi-tab website fingerprinting. In 2024 IEEE International Performance, Computing, and Communications Conference (IPCCC), pages 1–9. IEEE, 2024.

[28] Lin Liu, Ziling Wei, Shuhui Chen, Jinshu Su, and Yong Yuan. Kp-wf: Cross-domain few-shot website fingerprinting. In International Conference on Digital Forensics and Cyber Crime, pages 227–245. Springer, 2024.

[29] Chenxiang Luo, Wenyi Tang, Qixu Wang, and Danyang Zheng. Few-shot website fingerprinting with distribution calibration. IEEE Transactions on Dependable and Secure Computing, 22(1):632–648, 2024.

[30] Akshaya Mani, T Wilson-Brown, Rob Jansen, Aaron Johnson, and Micah Sherr. Understanding tor usage with privacy-preserving measurement. In Proceedings of the Internet Measurement Confer ence 2018, pages 175–187, 2018.

[31] Wenwen Meng, Chuan Ma, Ming Ding, Chunpeng Ge, Yuwen Qian, and Tao Xiang. Beyond single tabs: A transformative few-shot approach to multitab website fingerprinting attacks. In Proceedings ofthe ACM on Web Conference 2025, pages 1068– 1077, 2025.

[32] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. Website fingerprinting at internet scale. In Network and Distributed System Security Symposium, 2016. URL: https://api. semanticscholar.org/CorpusID:15302617.

[33] Andriy Panchenko, Lukas Niessen, Andreas Zinnen, and Thomas Engel. Website fingerprinting in onion routing based anonymization networks. In Proceedings ofthe 10th ACM Workshop on Privacy in the Electronic Society (WPES), 2011.

[34] Sachin Ravi and Hugo Larochelle. Optimization as a model for few-shot learning. In International conference on learning representations, 2017.

[35] Daisy Reyes, Eno Dynowski, Taryn Chovan, John Mikos, Eric Chan-Tin, Mohammed Abuhamad, and Shelia Kennison. Webtracker: Real webbrowsing behaviors. In 2023 Silicon Valley Cybersecurity Conference (SVCC), 2023.

[36] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. Automated website fingerprinting through deep learning. In Network and Distributed System Security Symposium, 2017.

[37] Vera Rimmer, Theodor Schnitzler, Tom Van Goethem, Abel Rodríguez Romero, Wouter Joosen, and Katharina Kohls. Trace oddity: Methodologies for data-driven traffic analysis on tor. Proceedings on Privacy Enhancing Technologies, 2022(3):314–335, 2022.

[38] Meng Shen, Kexin Ji, Jinhe Wu, Qi Li, Xiangdong Kong, Ke Xu, and Liehuang Zhu. Real-time website fingerprinting defense via traffic cluster anonymization. In 2024 IEEE Symposium on Security and Privacy (SP), pages 3238–3256. IEEE, 2024.

[39] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, pages 1928–1943, 2018.

[40] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew K. Wright. Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning. Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, 2019. URL: https://api.semanticscholar. org/CorpusID:207960329.

[41] Jake Snell, Kevin Swersky, and Richard Zemel. Prototypical networks for few-shot learning. In Advances in Neural Information Processing Systems (NeurIPS), 2017.

[42] Jingwen Tan, Huanran Wang, Shuai Han, Dapeng Man, and Wu Yang. An adaptability-enhanced fewshot website fingerprinting attack based on collu sion. IEEE Transactions on Information Forensics and Security, 2024.

[43] Grigorios Tsoumakas, Ioannis Katakis, and Ioannis Vlahavas. Random k-labelsets for multilabel classification. IEEE transactions on knowledge and data engineering, 23(7):1079–1089, 2010.

[44] Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Daan Wierstra, et al. Matching networks for one shot learning. Advances in neural information processing systems, 29, 2016.

[45] David Wagner, Bruce Schneier, et al. Analysis of the ssl 3.0 protocol. In The Second USENIX Workshop on Electronic Commerce Proceedings, volume 1, pages 29–40, 1996.

[46] Kai Wang, Zhiliang Wang, Dongqi Han, Wenqi Chen, Jiahai Yang, Xingang Shi, and Xia Yin. Bars: Local robustness certification for deep learning based traffic analysis systems. In NDSS, 2023.

[47] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. Effective attacks and provable defenses for website fingerprinting. USENIX Security Symposium, 2014.

[48] Tao Wang and Ian Goldberg. Improved website fingerprinting on tor. In Workshop on Privacy in the Electronic Society, 2013.

[49] Tao Wang and Ian Goldberg. On realistically attack ing tor with website fingerprinting. Proceedings on Privacy Enhancing Technologies, 2016.

[50] Zhiquan Wang, Tengyao Li, Meijuan Yin, Xiaoyun Yuan, Xiangyang Luo, and Lingling Li. Wf3a: A nshot website fingerprinting with effective fusion feature attention. Computers & Security, 140:103796, 2024.

[51] Ruotian Xie, Kun Xie, Pengcheng Zhao, Jiajun He, Xin Zeng, Jigang Wen, Yong Xie, Wei Liang, and Gaogang Xie. Gapdis: Gradient-assisted perturbation design via sequence editing for website fingerprinting defense. In Proceedings ofthe 2025 ACM SIGSAC Conference on Computer and Communications Security, pages 3012–3026, 2025.

[52] Yi Xie, Jiahao Feng, Wenju Huang, Yixi Zhang, Xueliang Sun, Xiaochou Chen, and Xiapu Luo. Contrastive fingerprinting: A novel website fingerprinting attack over few-shot traces. In Proceedings of the ACM Web Conference 2024, pages 1203– 1214, 2024.

[53] Yixiao Xu, Tao Wang, Qi Li, Qingyuan Gong, Yang Chen, and Yong Jiang. A multi-tab website fingerprinting attack. In Proceedings ofthe 34th Annual Computer Security Applications Conference, pages 327–341, 2018.

[54] Jinzhu Yan, Zhuotao Liu, Yuyang Xie, Shiyu Liang, Lin Liu, and Ke Xu. {CertTA}: Certified robustness made practical for {Learning-Based} traffic analysis. In 34th USENIX Security Symposium (USENIX Security 25), pages 7349–7368, 2025.

[55] Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, and Yixiao Xu. An automated multi-tab website fingerprinting attack. IEEE Transactions on Dependable and Secure Computing, 19(6):3656–3670, 2021.

[56] Yali Yuan, Weiyi Zou, and Guang Cheng. Mw3f: Improved multi-tab website fingerprinting attacks with transformer-based feature fusion. Journal of Network and Computer Applications, 236:104125, 2025.

[57] Gongjie Zhang, Zhipeng Luo, Kaiwen Cui, Shijian Lu, and Eric P Xing. Meta-detr: Image-level fewshot detection with inter-class correlation exploitation. IEEE transactions on pattern analysis and machine intelligence, 45(11):12832–12843, 2022.

[58] Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, and Ke Xu. Towards finegrained webpage fingerprinting at scale. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, pages 423–436, 2024.

[59] Qiang Zhou, Liangmin Wang, Huijuan Zhu, and Tong Lu. Few-shot website fingerprinting attack with cluster adaptation. Computer Networks, 229:109780, 2023.

[60] Hongcheng Zou, Jinshu Su, Ziling Wei, Shuhui Chen, Chunfang Yang, and Mantun Chen. Toward an effective few-shot website fingerprinting attack with quadruplet networks and deep local fingerprinting features. IEEE Transactions on Dependable and Secure Computing, 2025.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Time-consistent mixing for synthesizing an n-tab query trace.

Require: n single-tab traces  $\{T_{j}\}_{j=1}^{n}$ , overlap ratio range  $[r_{\min}, r_{\max}]$ 

Ensure: Mixed query direction sequence x

1: Each trace  $T_{j} = \{(t_{j,m}, d_{j,m})\}_{m=1}^{n_{j}}$ , where  $d_{j,m} \in \{+1, -1\}$ .

2: Normalize timestamps in each trace so that  $t_{j,1} = 0$ .

3: start $_{1} \leftarrow 0$ .

4: for j = 2 to n do

5: Sample  $r_{j} \sim \mathcal{U}(r_{\min}, r_{\max})$ .

6:  $D_{j-1} \leftarrow \text{duration of } T_{j-1}$ .

7:  $\Delta \leftarrow r_{j} \cdot D_{j-1}$ 

{overlap measured on the previous tab}

8: start $_{j} \leftarrow \text{start}_{j-1} + D_{j-1} - \Delta$ .

9: Shift timestamps in  $T_{j}: t_{j,m} \leftarrow t_{j,m} + \text{start}_{j} \quad \forall m$ .

10: end for

11:  $E \leftarrow \text{merge all events from } \{T_{j}\}$  and sort by timestamp.

12:  $x \leftarrow \text{the direction sequence } \{d\}$  extracted from E in temporal order.

13: return x
</div>

Table 10: Data Collection Environment Specifications  
```txt
Component Specification
Operating System Ubuntu 22.04 LTS (Dockerized)
Browser Tor Browser 13.5 (Standard Security Level)
Automation Framework Python Selenium with Geckodriver
Traffic Capture tcpdump
Display Environment Xvfb (Headless X Server)
Network Strategy Default Tor circuit construction (Random Guard/Exit)
```

## A Detailed Settings For Experiment

## A.1 Multi-tab synthesis procedure.

To emulate realistic multi-tab browsing, we synthesize an n-tab query trace by time-consistent mixing of mul tiple labeled single-tab traces (Algorithm 1). We use time-based composition (event-level merging) instead of sequential concatenation because it preserves bursty micro-structures that are important for WF. Each single tab trace is represented as timestamped packet directions, where an outgoing packet is encoded as +1 and an incoming packet as −1. Given n traces, we normalize their timestamps to start from zero and assign a start time to each trace so that tab openings partially overlap. For $j \geq 2$ , we sample an overlap ratio $r _ { j } \sim \mathcal { U } ( r _ { \operatorname* { m i n } } , r _ { \operatorname* { m a x } } )$ and set

$$
\operatorname{start} _ {j} = \operatorname{start} _ {j - 1} + (1 - r _ {j}) D _ {j - 1},
$$

where $D _ { j - 1 }$ is the duration of the previous trace. Equivalently, the intended overlap window between $T _ { j - 1 }$ and $T _ { j }$ is $\Delta _ { j } = r _ { j } \cdot D _ { j - 1 } , \mathrm { i . e . , } T _ { j }$ begins $\Delta _ { j }$ time units before $T _ { j - 1 }$ ends. This construction naturally allows containment when a previous tab is much longer than a newly opened tab: if $D _ { j } \leq r _ { j } D _ { j - 1 }$ , then $T _ { j }$ can be fully contained within $T _ { j - 1 } { \bf \dot { s } }$ time span. In extreme cases, a long-lived tab may contain multiple subsequently opened short tabs, matching real sessions. After shifting timestamps, we merge all packets and extract the mixed direction sequence in temporal order.

During base training, we split single-tab data into training and test sets with an 8:2 ratio and then the synthesis algorithm is applied to ensure strictly separation. For the few-shot stage, to mitigate evaluation bias under limited onboarding samples, we use a more stringent split where the test set is five times larger than the training set, improving result stability.

In the closed-world (CW) setting, we mix only monitored websites and use a larger overlap range (e.g., $r _ { \operatorname* { m a x } } = 0 . 4 )$ to induce stronger interleaving. In the openworld (OW) setting, we additionally insert an unmonitored trace at a random position in the tab combination.

## A.2 Data Collection Infrastructure and Protocol

We improved the data collection framework based on the method provided by ARES [13]. The collection pipeline is designed to simulate a realistic passive adversary while maintaining strict experimental controls.

Infrastructure Configuration. We utilized Docker containers to isolate browsing instances, allowing for parallel data collection without cross-talk. Each container was allocated independent system resources to prevent CPU throttling artifacts in the traffic traces. The key specifications of our collection environment are detailed in Table 10.

Collection Protocol. Our collection script orchestrates the browsing sessions following a strict protocol to ensure data quality:

• Session Isolation: For every collected trace (instance), a fresh Tor Browser profile is created. This ensures that no cache, cookies, or local storage artifacts persist between visits, guaranteeing statistical independence of the samples.

• Traffic Capture: We capture traffic at the container’s network interface using tcpdump. To isolate the browsing traffic from background noise, we filter strictly for TCP packets.

• Verification: To verify successful page loads, we capture a screenshot of the virtual framebuffer (via Xvfb). Traces where the screenshot indicates a loading error (e.g., Tor connection timeout) are discarded.

We will publicly release all code and configuration related to data collection to support reproducibility and future research.
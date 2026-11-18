# Fooling Multi-Tab Browsing: Few-Shot Website Fingerprinting Attacks and Lightweight Obfuscation Defenses

Yuwen Qian, Wenwen Meng, Chuan Ma, Senior Member, IEEE, Ming Ding, Senior Member, IEEE, Biwen Chen, Tao Xiang, Senior Member, IEEE,

Abstract—Website Fingerprinting (WF) enables passive adversaries to infer users’ browsing activity by analyzing encrypted traffic traces. While existing WF approaches have achieved remarkable success, they are often constrained to single-tab browsing scenarios or depend heavily on large-scale labeled datasets. These limitations reduce their applicability in dynamic and privacy-sensitive environments. To address these challenges, we introduce Few-shot Multi-tab Website Fingerprinting (FMWF), a novel attack framework that combines transfer learning with few-shot fine-tuning to classify traffic in multi-tab browsing scenarios. FMWF synthesizes multi-tab traffic patterns from easily available single-tab traces and requires only a small number of real multi-tab samples for fine-tuning. This design eliminates the need for extensive multi-tab training data while maintaining high classification accuracy. In parallel, we propose Template-Guided Traffic Obfuscation (TGTO), a lightweight yet robust defense mechanism that reshapes traffic to mislead fingerprinting models. TGTO consists of three core components: (1) a template library constructed from real traffic traces, (2) an efficient morphing module that applies trace transformations, and (3) an adaptive selection strategy that dynamically chooses templates based on real-time network conditions and adversarial feedback. Unlike conventional obfuscation strategies that depend on random padding or artificial delays that suffer from high overhead or limited adaptability, TGTO introduces template-driven obfuscation with minimal performance degradation. On average, it reduces WF attack accuracy by 60.84%, outperforming existing defenses by 36.53%. Meanwhile, in open-world settings, FMWF achieves an average accuracy improvement of 15.72% over stateof-the-art methods such as ARES (SP’23), TMWF (CCS’23), and BAPM (ACSAC’21). Code and datasets are available at https://github.com/WW-Meng/FMWF.

Index Terms—Multi-tab Website fingerprinting, Deep learning, Few-shot learning, privacy protection, Tor.

## I. INTRODUCTION

working and online banking [2] has made user privacy a paramount concern. Despite the widespread adoption of encryption protocols like HTTPS, adversaries can still infer sensitive browsing behavior by analyzing traffic metadata, such as packet sizes, directions, and timing patterns [3], [4], [5], [6]. Privacy-enhancing technologies (PETs) like Tor aim to counteract these threats by employing multi-layered encryption and anonymized routing to obfuscate user identities and traffic origins [7], [8]. However, the very encryption that PETs provide, while shielding legitimate users, inadvertently creates opaque channels that can be exploited by malicious actors to evade detection. This duality has spurred the development of encrypted traffic analysis techniques, not only for security purposes like intrusion detection but also, critically, by adversaries. Among the most potent of these are Website Fingerprinting attacks, which have demonstrated the ability to de-anonymize users, even within networks like Tor, by identifying distinctive patterns in encrypted traffic streams to infer visited websites [9], [10], [11], [12], [13], [14].

Early WF approaches used handcrafted features with traditional classifiers [15], [16], [17], but the introduction of deep learning models like Deep Fingerprinting (DF) [18] significantly boosted accuracy by automating feature extraction. However, most of these attacks assume single-tab browsing and suffer degraded performance in realistic multi-tab settings, where overlapping traffic complicates classification [19], [20], [21]. While early countermeasures, including adaptive padding [22] and WTF-PAD [23], initially proved effective against traditional WF by obfuscating traffic features, the sophisticated learning capabilities of modern deep learning models can often circumvent these defenses by extracting latent patterns from obfuscated data [24], [25]. This persistent cat-and-mouse dynamic underscores the critical need for robust defense mechanisms that can not only neutralize advanced WF attacks but also dynamically adapt to complex modern browsing behaviors and evolving adversarial strategies.

Many existing multi-tab WF attacks [26], [27], [28], [29] segment browsing sessions into discrete traffic chunks, each mapped to an individual website.However, this paradigm suffers from key limitations. Some methods assume prior knowledge of the number of active tabs, e.g., [26] operates under a fixed two-tab setting, which fails in dynamic real-world browsing scenarios. Even under ideal conditions, such models are vulnerable to defenses like traffic padding and packet delays [27]. Moreover, as the number of concurrent open tabs increases, the ability to distinguish individual website patterns diminishes significantly due to increased traffic entanglement and noise, further degrading identification performance. To overcome these challenges, recent approaches [19], [20], [21], [30] have leveraged deep architectures such as Transformers to better handle overlapping traffic. While effective, these methods rely heavily on large-scale multi-tab datasets, which are expensive to collect and quickly become outdated due to the dynamic nature of web content [20], [31]. Models trained on stale data rapidly lose accuracy, necessitating frequent retraining that incurs significant operational costs and privacy risks. These issues raise a pressing question: Can we build a more efficient multi-tab WF attack that avoids prior tab count assumptions and large training datasets, while retaining high performance?

We answer this question with the introduction of Few-shot Multi-tab Website Fingerprinting, a novel attack framework that combines transfer learning with data-efficient fine-tuning. FMWF bypasses the need for traffic segmentation and massive data collection by first pre-training on synthetic multi-tab traces generated from single-tab traffic, then fine-tuning with a small number of real multi-tab samples. This two-stage design captures key traffic patterns while significantly reducing data demands, improving adaptability to real-world multi-tab environments without sacrificing accuracy.

Furthermore, to counter the escalating sophistication of WF attacks, including advanced techniques potentially developed from principles similar to FMWF, we propose Template-Guided Traffic Obfuscation. TGTO is a novel defense mechanism engineered to disrupt salient traffic features critical to WF while preserving network efficiency. Unlike conventional obfuscation strategies that depend on random padding or artificial delays, TGTO utilizes a library of predefined traffic templates to strategically mold traffic characteristics such as burst structures and directionality. By dynamically selecting and adapting these templates based on real-time network conditions and perceived adversarial feedback, TGTO introduces controlled perturbations that effectively obfuscate traffic fingerprints with low performance overhead. This adaptive methodology not only fortifies defenses against state-of-the-art WF attacks but also promotes practical deployability by carefully balancing security enhancements with user experience.

Building on our prior conference version of FMWF, this journal article extends the work with refined overlap-aware augmentation, a new lightweight defense, and broader evaluation. We redesign the synthetic multi-tab augmentation by explicitly modeling positive/zero/negative inter-arrival types and provide an implementation-level specification (Section III.B and Algorithm 1), together with a controlled ablation that isolates the benefit of this refinement under identical backbones and training settings. We further propose TGTO, a templateguided obfuscation defense absent from the conference version, and validate its mechanism via an explicit template– obfuscation similarity analysis (Section V.E), alongside effectiveness and overhead evaluation (Section V). Finally, we conduct a joint attack–defense analysis (Section V) and expand the evaluation to a challenging 10-tab few-shot scenario (Experiment II-2) and a larger open-world setting, yielding a more stringent assessment under realistic multi-tab browsing

behaviors.

The primary contributions of this work are summarized as follows:

• We propose FMWF, the first few-shot multi-tab website fingerprinting attack framework that combines a tailored data augmentation strategy with a lightweight neural architecture. This design eliminates the need for large-scale multi-tab traffic datasets and computationally expensive models like Transformers, making FMWF practical for real-world deployment with limited data and resources.

• Through extensive experiments on real-world traffic collected from Tor, Microsoft Edge, and Google Chrome, we demonstrate that FMWF achieves competitive accuracy under both closed-world and open-world settings. Remarkably, FMWF reaches top-k accuracy of 0.917 on Tor with only 30-shot learning and 0.896 on Edge and Chrome with 3-shot learning in the 5-tab setting, outperforming state-of-the-art methods such as ARES (SP’23), TMWF (CCS’23), and BAPM (ACSAC’21) by an average margin of 15.72% in open-world scenarios.

• We propose Template-Guided Traffic Obfuscation, a novel and lightweight defense mechanism specifically designed to counteract advanced multi-tab WF attacks. TGTO strategically reshapes traffic patterns using predefined templates and dynamic adjustments, effectively disrupting the feature extraction capabilities of WF models while maintaining low overhead and preserving user experience. TGTO reduces attack accuracy by an average of 60.84%, surpassing existing defenses by 36.53% with low performance impact.

![](images/9fc1c5ba4de8d58a5aaade1ca3115a86e3c46beda50198af6fa1420587e659f8.jpg)  
Fig. 1. Threat model of FMWF. Users can simultaneously open multiple tabs to visit different websites, and an attacker can eavesdrop on the encrypted traffic within the Tor network.

## II. BACKGROUND AND RELATED WORK

## A. Threat Model

We consider a powerful passive network adversary who can observe and analyze encrypted traffic but cannot interfere with it. This setting follows standard assumptions in prior website fingerprinting (WF) studies [20], [25], [32], [33], [34]. As illustrated in Figure 1, users access websites through anonymous communication systems such as Tor, which employ multi-layer encryption and relay nodes to conceal the payload contents and route information.

The adversary is positioned at a network vantage point between the client and the first relay node, such as an ISP, an AS-level observer, or an on-path router, and can only passively capture coarse-grained traffic metadata from the encrypted tunnel, including packet direction, timing, and volume. The attacker cannot decrypt payloads, cannot modify, inject, delay, or drop packets, and cannot isolate per-website flows because traffic from multiple websites is multiplexed into a single encrypted connection. Normal network dynamics, including, congestion-induced jitter and burstiness, queueing delays, circuit/path changes, and CDN/content variability, naturally distort traffic patterns, and the adversary cannot reliably detect page-load boundaries. In multi-tab sessions, packets from different websites overlap unpredictably, and the attacker does not assume prior knowledge of the (possibly time-varying) number of active tabs. Following prior work, we consider both closed-world and open-world settings. Under these constraints, the adversary trains machine learning models on historical encrypted traces and aims to infer the set of websites visited by the user. All attack and defense evaluations in this paper are conducted under this threat model.

## B. Single-tab WF Attacks

Early research in website fingerprinting primarily focused on identifying websites accessed by a single user engaging in one browsing activity at a time (referred to as the singletab scenario). This foundational work laid the groundwork for understanding traffic patterns and developing recognition techniques, which have significantly advanced with the advent of deep learning and transfer learning methodologies.

Deep Learning-Based WF: The application of deep learning (DL) methods revolutionized WF attacks by moving beyond manually engineered features to automated feature extraction from raw network traffic. Abe et al. [35] were among the first to demonstrate this shift, utilizing stacked autoencoders to derive features from packet direction sequences, achieving performance comparable to state-of-theart traditional methods. This work highlighted the potential of neural networks to capture complex, subtle patterns in encrypted traffic.

Subsequent studies further solidified the role of DL. Rimmer et al. [31] showed that DL models maintained robustness against changes in website content, a crucial factor for practical attacks. A significant milestone was the introduction of DF by Sirinam et al. [18], which employed Convolutional Neural Networks (CNNs) to effectively learn fine-grained traffic features. DF achieved a notable 98.3% accuracy in a closed-world setting on a large dataset, establishing CNNs as a highly effective architecture for WF. Addressing the challenge of data dependency in supervised DL, Bhat et al. [36] proposed Var-CNN, which incorporated semi-automated feature learning to improve performance on smaller datasets, making DL-based WF more practical in data-scarce environments.

Transfer Learning-Based WF: Despite the successes of supervised DL, training high-performing models often necessitates large, labeled datasets, which are costly and timeconsuming to collect for WF tasks [37], [38]. Transfer learning (TL) offers a compelling solution to mitigate this data scarcity problem [39], [40]. By leveraging knowledge pre-trained on extensive source datasets, TL allows models to be effectively adapted to new WF tasks or datasets with limited labeled target data, enabling few-shot learning scenarios.

Recent WF research has actively integrated TL techniques to enhance feature extraction and model generalization under data constraints [41], [42], [25]. Triplet Fingerprinting (TF) [41] introduced metric learning via a triplet network to improve the separability of website traffic embeddings in a few-shot setting. Adaptive Fingerprinting (AF) [42] explored adversarial domain adaptation techniques to learn features that are more invariant to variations across different data collection environments. More recently, Contrastive Fingerprinting (CF) [25] applied contrastive learning paradigms coupled with data augmentation strategies to significantly improve the quality and robustness of learned traffic representations, leading to enhanced few-shot WF performance and training efficiency.

However, a fundamental limitation shared by the majority of the aforementioned WF studies is the assumption of a singletab Browse scenario. While these methods are effective under this assumption, they do not fully capture the complexity of real-world user behavior, where multiple websites are often loaded concurrently within a single session, leading to multiplexed traffic streams [26], [29], [43], [44]. Effectively performing WF attacks and developing robust defenses in such multi-tab environments remains a significant challenge.

## C. Multi-tab Website Fingerprinting Attacks

Acknowledging the limitations of single-tab assumptions, recent research has focused on the more realistic multi-tab website fingerprinting scenario, where concurrent browsing creates complex, multiplexed traffic streams that increase attack difficulty.

Advanced approaches, notably those based on the Transformer architecture [19], [20], [21], have been applied to process the intricate patterns in overlapping traffic. These methods typically model the problem as multi-tab classification or sequence prediction, leveraging mechanisms like selfattention to capture both local and global traffic dependencies and demonstrating improved accuracy on intertwined traffic. Despite these advancements, existing multi-tab WF techniques face critical limitations for real-world deployment. They exhibit heavy reliance on large labeled datasets [37], [38] and often assume a fixed number of open tabs. These constraints limit adaptability to dynamic user behavior with varying tab configurations and necessitate expensive data collection and frequent retraining.

## D. Website Fingerprinting Defenses

To protect user privacy against website fingerprinting attacks, numerous defense mechanisms have been proposed, including WTF-PAD [23], Walkie-Talkie [45], FRONT [46], Mockingbird [47], Surakav [48], and RegulaTor [49]. These defenses aim to obfuscate traffic patterns by injecting dummy packets or introducing artificial delays, thereby masking the distinctive features associated with individual websites and confusing WF classifiers. However, modern deep learning WF attacks have shown significant resilience to such noise-based

Phase Ⅰ: Pre-train attack model

![](images/694fa32e3ab9c8297921c3b9a4b1f8fff7b3d351dbfaaae5e1cba5315fb168e7.jpg)  
Fig. 2. Our lightweight WF attack, FMWF, consists of two key components: a feature extractor and a classifier, both built using lightweight neural networks These components work in tandem with a fine-tuning algorithm derived from transfer learning, enabling efficient and accurate multi-tab website fingerprintin with minimal training data.

defenses. DL models learn complex correlations that traditional padding/delay methods often fail to conceal, frequently requiring prohibitive overhead (bandwidth/latency) for limited effectiveness [18], [19], [20], [21], [25], [31].

## III. THE PROPOSED ATTACK METHOD

In this section, we present our proposed FMWF framework, providing a detailed description of its structure and operational workflow.

## A. Overview of FMWF

Addressing the data collection and retraining burden faced by state-of-the-art multi-tab WF attacks due to dynamic traffic, we propose Few-shot Multi-tab Website Fingerprinting. This novel framework employs transfer learning and a specialized data augmentation approach to enable effective multi-tab WF in few-shot scenarios, enhancing practical feasibility. Figure 2 illustrates the FMWF framework, which consists of two primary training stages and a final evaluation phase:

1) Pre-training with Synthetic Multi-tab Data: We propose a novel data augmentation technique to synthesize a large corpus of realistic multi-tab traffic traces from single-website patterns. This stage pre-trains a base model to learn general multi-tab representations without extensive real-world data.

2) Few-shot Fine-tuning on Real Data: Using a limited set of labeled real multi-tab traffic, the pre-trained model is fine-tuned. This process adapts the learned representations to real-world traffic variations, enabling rapid fewshot generalization and reducing the need for frequent retraining.

3) Evaluation: The fine-tuned model’s performance is assessed on various held-out datasets, covering both closed-world and open-world settings.

Subsequent subsections detail the architecture and operation of each FMWF component.

![](images/6e5f5aaee02b9247d0d69110221c50efd82f838d4ddb7d6af09cd53b77040953.jpg)  
Fig. 3. Three basic situations of 2-tab traffic traces. Depending on whether a user accesses Site B via a new tab before Site A finishes loading, 2-tab traffic patterns can be categorized into these three types.

## B. Pre-training with Synthetic Multi-tab Data

This subsection details the initial pre-training stage of the FMWF framework, designed to equip the model with the fundamental ability to recognize patterns in multi-tab traffic before fine-tuning on real-world data. This stage primarily involves constructing a large-scale pre-training dataset through synthetic data augmentation and training a base attack model comprised of a feature extractor and a classifier.

Synthetic Pre-training Dataset Generation. A significant challenge in multi-tab WF is the prohibitive cost and combinatorial complexity of collecting large, labeled datasets of real concurrent Browse sessions. As the number of monitored websites increases, the potential combinations of simultaneously visited sites, representing the label space, grow exponentially. For instance, monitoring just 100 websites can lead to over 4,000 possible labels for two-tab scenarios alone, making exhaustive real data collection and continuous updates impractical for an adversary. To alleviate this burden, we propose a novel data augmentation approach that generates a vast pretraining dataset by synthesizing multi-tab traffic traces from readily available single-tab traffic sequences.

Our synthesis methodology is informed by the classification of interarrival times in multi-tab traffic proposed by Wang et al. [29], which categorizes intervals between packets from different tabs into positive, zero, and negative types. Figure 3 illustrates these scenarios for 2-tab traffic traces. As conceptually illustrated in Figure 4, our augmentation function intelligently combines single-tab traces based on these temporal relationships to create realistic-looking synthetic multi-tab sequences.

![](images/acd48f2520e28009d1255664fac6a8eabccb748dc2629af9607d7464e7322bf6.jpg)  
Fig. 4. Manually Synthesized Multi-Tab Traffic Traces from single-tab sessions for the Pre-Training Stage.

Specifically, a traffic instance is represented as a sequence of packets $( t , y )$ , where t is the packet sequence and y is a multi-hot encoded label vector indicating the presence of multiple websites. For a monitored set of M websites, $y = [ y _ { 0 } , y _ { 1 } , \dots , y _ { M - 1 } ]$ , where $y _ { i } = 1$ if website i is active in the session, and $y _ { i } = 0$ otherwise. In our implementation, each single-tab trace t is represented as a direction-only sequence $t ~ = ~ [ d _ { 1 } , \ldots , d _ { L } ]$ with $d _ { \ell } \in \{ - 1 , + 1 \}$ (client-to-server vs. server-to-client), consistent with the feature representation used throughout the paper. To construct a synthetic multitab instance, we combine single-tab traces $\{ t _ { i _ { 1 } } , t _ { i _ { 2 } } , \ldots , t _ { i _ { k } } \}$ corresponding to websites $i _ { 1 } , i _ { 2 } , \ldots , i _ { k }$ using our data augmentation function $\operatorname { A u g } ( \cdot )$ . The resulting synthetic trace $\tilde { t } =$ $\mathbf { A u g } ( t _ { i _ { 1 } } , \dots , t _ { i _ { k } } )$ is assigned the multi-hot label y˜ representing the combination $\{ i _ { 1 } , \ldots , i _ { k } \}$ . This allows us to generate a diverse and large-scale dataset of synthetic multi-tab traffic covering numerous website combinations.

To make the augmentation procedure explicit and reproducible, we model the three inter-arrival types using a discrete type variable $\tau \in \mathsf { P O S } , Z \mathsf { E R O }$ , NEG and synthesize a 2- tab trace by controlling (i) whether two tabs overlap and (ii) the overlap/gap extent. Given two single-tab direction sequences $t ^ { ( A ) }$ and $t ^ { ( B ) }$ with lengths $L _ { A }$ and $L _ { B }$ , we use an overlap ratio $\rho \in [ 0 , 1 )$ to determine the overlap length $L _ { \mathrm { c r o s s } } = \lfloor \rho { \cdot } \mathrm { m i n } ( L _ { A } , L _ { B } ) \rfloor$ when $\tau = { \mathsf { N E G } }$ , and set $L _ { \mathrm { c r o s s } } = 0$ when $\tau \in \mathsf { P O S } , Z \mathsf { E R O } .$ . We then partition the traces into non-overlapping and (if applicable) overlapping segments and merge them using type-specific rules: (i) for $\tau = { \mathsf { N E G } }$ , we create an explicit overlap region by interleaving packets from the two tabs in the overlap part, capturing near-simultaneous mixed traffic; (ii) for $\tau = Z \mathsf { E } \mathsf { R } \mathsf { O }$ , we synthesize sequential tabs by directly concatenating $t ^ { ( B ) }$ after $\mathbf { \chi } _ { t ^ { ( A ) } }$ , corresponding to no idle gap; (iii) for $\tau = \mathsf { P O S }$ , we introduce a gap-length hyperparameter $g \in \mathbb { Z } _ { \geq 0 }$ and insert g dummy direction tokens, randomly sampled from $- 1 , + 1$ , between $t ^ { \dot { ( A ) } }$ and $t ^ { ( B ) }$

We emphasize that these dummy direction tokens are representation-level placeholders in the direction-only feature space, rather than physical website packets deliberately transmitted during a strictly idle interval. The rationale is two-fold. First, a user-level idle interval in Tor does not necessarily imply absolute silence on the observable encrypted connection, since Tor traffic may contain non-sitespecific background/control activities, such as circuit construction and maintenance, SENDME-based flow control, and padding/control cells used for keepalive [4], [8]. Thus, the inserted dummy direction tokens can be interpreted as a coarse approximation of ambient, non-site-specific traffic that may appear between two discrete browsing events. Second, since standard direction-only sequences remove timestamp information, a positive idle gap cannot be directly represented once the trace is converted into a sequence over −1, +1. Without these inserted tokens, the POS case with an idle gap and the ZERO case without an idle gap would become structurally indistinguishable. Therefore, the inserted $g$ dummy direction tokens act as a structural proxy to encode the existence and approximate extent of the gap in the synthetic sourcedomain trace, while random sampling avoids deterministic boundary artifacts or directional bias. This approximation is used only for synthetic pre-training, and the subsequent fewshot fine-tuning on real traces helps mitigate the remaining distribution mismatch. More fine-grained modeling of Tor background/control-cell dynamics is left as an important direction for future work. Algorithm 1 provides the step-bystep pseudocode that directly mirrors our implementation, including how $( \tau , \rho , g )$ are instantiated and how the merged direction sequence t<sup>˜</sup> is constructed.

We further generalize the above 2-tab operator to k-tab synthesis by iteratively composing it: starting from one randomly sampled single-tab trace, we add another trace at each step using independently sampled augmentation variables $( \tau , \rho , g )$ and update the multi-hot label accordingly. This iterative composition produces diverse k-tab direction sequences and corresponding k-hot labels while keeping the augmentation procedure simple and reproducible (Algorithm 1).

Base Model Architecture. The attack model trained during the pre-training phase comprises a feature extractor and a classifier, designed to process the synthetic multi-tab traffic and predict the corresponding multi-hot labels.

The feature extractor is based on a Convolutional Neural Network (CNN) architecture, commonly used in WF due to its effectiveness in capturing spatial and temporal patterns in traffic sequences [18]. Its role here is to learn robust feature representations from the synthetically augmented multi-tab traffic sequences. Standard techniques like Batch Normalization and Dropout are incorporated to aid training stability and improve the generalization capability of the learned features across different synthetic traffic patterns.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Overlap-/Gap-aware 2-tab Direction-Trace Synthesis from Single-tab Traces

Require: Single-tab packet-direction traces  $t^{(A)} \in \{-1, +1\}^{L_A}$  and  $t^{(B)} \in \{-1, +1\}^{L_B}$ ; inter-arrival type  $\tau \in \{POS, ZERO, NEG\}$ ; overlap ratio  $\rho \in [0, 1)$ ; gap length  $g \in Z_{\geq 0}$  (used only when  $\tau = POS$ ).

Ensure: Synthetic 2-tab trace  $\tilde{t}$  and its multi-hot label  $\tilde{y}$ .

1: Initialize  $\tilde{t} \leftarrow []$ .

2:  $L_A \leftarrow |t^{(A)}|$ ,  $L_B \leftarrow |t^{(B)}|$ .

3: /* Determine the overlap length */

4: if  $\tau = NEG$  then

5:  $L_{cross} \leftarrow \lfloor \rho \cdot \min(L_A, L_B) \rfloor$ .

6: else

7:  $L_{cross} \leftarrow 0$ .

8: end if

9: /* Partition traces into non-overlapping and (if applicable) overlapping segments */

10:  $A_{head} \leftarrow t^{(A)}[0 : L_A - L_{cross}]$ .

11:  $A_{tail} \leftarrow t^{(A)}[L_A - L_{cross} : L_A]$ .

12:  $B_{head} \leftarrow t^{(B)}[0 : L_{cross}]$ .

13:  $B_{tail} \leftarrow t^{(B)}[L_{cross} : L_B]$ .

14: /* (1) Append the non-overlapping prefix of tab A */

15: Append all packets in  $A_{head}$  to  $\tilde{t}$ .

16: /* (2) Type-specific synthesis */

17: if  $\tau = NEG$  then

18: /* Overlapping tabs: interleave packets within the overlap region */

19: for i = 0 to  $L_{cross} - 1$  do

20: Append  $A_{tail}[i]$  to  $\tilde{t}$ .

21: Append  $B_{head}[i]$  to  $\tilde{t}$ .

22: end for

23: else if  $\tau = POS$  then

24: /* Sequential tabs with an explicit idle gap: insert g dummy direction tokens */

25: for j = 1 to g do

26: Sample a dummy direction  $d_j^{(\text{dum})} \in \{-1, +1\}$ .

27: Append  $d_j^{(\text{dum})}$  to  $\tilde{t}$ .

28: end for

29: else if  $\tau = ZERO$  then

30: /* Sequential tabs without an idle gap: no additional tokens are inserted */

31: end if

32: /* (3) Append the remaining part of tab B */

33: Append all packets in  $B_{tail}$  to  $\tilde{t}$ .

34: /* (4) Construct the multi-hot label */

35: Initialize  $\tilde{y} \in \{0, 1\}^M$  as an all-zero vector.

36: Set  $\tilde{y}[i_A] \leftarrow 1$  and  $\tilde{y}[i_B] \leftarrow 1$ . ( $i_A, i_B$  are indices of sites A, B)

37: return ( $\tilde{t}, \tilde{y}$ ).
</div>

The classifier is implemented as a Multi-Layer Perceptron (MLP). It takes the feature embeddings produced by the CNN feature extractor as input and outputs a prediction for the multi-hot label vector y˜. A weighted loss function, such as Weighted Binary Cross-Entropy, is employed to handle the multi-tab nature of the task and potentially address imbalances in the distribution of website combinations in the synthetic dataset. The MLP consists of several fully connected layers with ReLU activations and Batch Normalization, culminating in a final layer trained to output the multi-hot class probabilities.

By pre-training this base model on a large volume of synthetically generated multi-tab traffic, we create a strong foundation for the subsequent few-shot fine-tuning phase, enabling the model to effectively interpret multi-tab patterns and significantly reducing the reliance on extensive real-world multi-tab data collection.

## C. Few-shot Fine-tuning for Real-world Adaptation

Following the pre-training phase, the FMWF model undergoes a crucial fine-tuning stage aimed at adapting the learned general multi-tab representations to the characteristics of real-world traffic using a small labeled dataset of real multi-tab traffic traces. This process refines the pre-trained parameters of both the feature extractor and the classifier, enhancing the model’s ability to accurately identify website labels within complex, dynamic Browse scenarios specific to the target environment. As demonstrated by studies in transfer learning [50], fine-tuning is highly effective in enabling models to quickly generalize to new domains or tasks with minimal target data. The inherent challenge of distinguishing traffic from multiple interleaved websites in real-world traces necessitates this adaptation. During fine-tuning, real multi-tab traffic sequences are fed into the pre-trained feature extractor, which, now being fine-tuned, produces refined feature embeddings that capture the nuances of real traffic while preserving essential website-specific characteristics learned during pre-training. These embeddings are then processed by the fine-tuned multi-layer perceptron (MLP) classifier to improve predictive accuracy on real data. By leveraging the robust foundation built on synthetic data and adapting it with only limited real examples in a few-shot manner, this structured fine-tuning process ensures FMWF’s effectiveness and practicality in dynamic, real-world web traffic scenarios without requiring extensive new data collection or retraining for each target environment.

## D. Attack Model Algorithm Summary

In summary, the proposed Few-shot Multi-tab Website Fingerprinting framework introduces a novel paradigm for multitab WF attacks. It specifically addresses the key limitations of prior approaches, namely their dependence on large real-world multi-tab datasets and their often-implicit assumption of fixed tab configurations. FMWF achieves enhanced practicality and efficiency by combining two core strategies: 1) pre-training on a large corpus of multi-tab traffic synthetically generated from single-tab traces using a novel data augmentation technique, and 2) few-shot fine-tuning on limited real multi-tab data to adapt the pre-trained model to real-world variations. Leveraging a CNN-based feature extractor and an MLP classifier, FMWF demonstrates improved adaptability and effectiveness in dynamic Browse environments. By enabling accurate multitab WF under few-shot conditions and without requiring prior knowledge of the number of open tabs, FMWF represents a significant advancement towards more feasible and scalable website fingerprinting attacks in realistic scenarios.

![](images/f1b67a2a0f632c848e2c7bc2b472230a64cfe936071ccd57efafcccc5e3aeb73.jpg)  
Fig. 5. Overview of the TGTO Architecture for Defending Against Website Fingerprinting Attacks.

## IV. THE PROPOSED DEFENSE METHOD

In this section, we introduce Template-Guided Traffic Obfuscation, a novel defense mechanism designed to obscure identifiable traffic patterns and mitigate website fingerprinting attacks. We first outline the fundamental principles and operational workflow of TGTO, which leverages predefined traffic templates to guide the obfuscation process. Next, we provide a detailed exposition of its key components, including their design and implementation.

## A. Overview of TGTO

TGTO is a modular framework that counteracts advanced WF attacks by reshaping traffic sequences to resemble those of benign websites. Unlike traditional approaches that rely on random noise injection or uniform padding, TGTO employs real traffic traces, referred to as traffic templates, as structural guides to perform semantically meaningful obfuscation. By aligning a user’s traffic to these templates, TGTO degrades the classification accuracy of fingerprinting models while maintaining usability with controlled overhead.

The TGTO framework can be formalized as a tuple:

$$
\mathrm{TGTO} = \left(\mathcal {T}, \mathcal {M}, \mathbf {p} (t)\right),
$$

where:

$\mathcal { T } = \{ T _ { 1 } , T _ { 2 } , \dots , T _ { K } \}$ denotes the Obfuscation Template Repository, consisting of K real-world traffic traces selected through a multi-stage curation process optimizing for obfuscation utility and minimal overhead.

$\mathcal { M } : \mathcal { X } \times T _ { k }  \widetilde { \mathcal { X } }$ is the Traffic Morphing Mechanism, which transforms an input traffic sequence $x \in \chi$ into an obfuscated version $\widetilde x \in \widetilde { \mathcal X }$ such that xe closely resembles traffic template $T _ { k }$ in temporal and structural characteristics.

$\mathbf { p } ( t ) = [ p _ { 1 } ( t ) , \ldots , p _ { K } ( t ) ]$ is the Adaptive Selection Strategy, a time-varying probability distribution over $\tau$ used to randomly select a template $T _ { k }$ at time t, conditioned on network feedback and potential adversarial behavior.

The defense goal of TGTO can be expressed as minimizing the classification success probability of a WF attacker A, while maintaining bounded network overhead:

$$
\min _ {\mathcal {M}, \mathbf {p} (t)} \mathbb {P} \left(\mathcal {A} (\widetilde {x}) = y\right) \quad \text { subject   to } \quad \text { Overhead } (\widetilde {x}, x) \leq \delta ,
$$

where $y$ is the true website label, and δ is an upper bound on acceptable performance overhead.

Figure 5 provides an overview of the TGTO architecture, highlighting the interactions between these components and illustrating how real-world traffic templates guide the dynamic obfuscation process. By integrating these components, TGTO provides a more effective and robust defense against stateof-the-art website fingerprinting attacks, achieving a superior balance between security guarantees and user experience compared to prior noise-based defenses.

## B. Traffic Morphing Mechanism

The Traffic Morphing Mechanism is the core operational module of TGTO, tasked with transforming a live user traffic stream into a new sequence that mimics a selected traffic template trace. In contrast to traditional approaches that inject random noise, this mechanism applies deterministic, templateguided transformations to produce structured and semantically meaningful obfuscation.

Let the user’s original traffic sequence be denoted as:

$$
U = \{u _ {1}, u _ {2}, \dots , u _ {n} \}, \quad u _ {i} \in \{- 1, + 1 \},
$$

and let the selected traffic template trace be:

$$
T = \{t _ {1}, t _ {2}, \dots , t _ {m} \}, \quad t _ {j} \in \{- 1, + 1 \},
$$

with $m \geq n$ . The objective of traffic morphing is to produce a morphed sequence $\hat { U }$ such that:

$$
\hat {U} = \mathcal {M} (U, T),
$$

where $\mathcal { M } ( \cdot , \cdot )$ is the morphing operator that injects dummy packets $d _ { k } \ ( { \mathrm { i . e . } }$ ., fake packets not present in U) to align U with $T ,$ while preserving the order and semantics of the original packets.

The morphing operator works by finding an injective mapping $\phi : \{ 1 , \dotsc , n \}  \{ 1 , \dotsc , m \}$ such that:

$$
u _ {i} = t _ {\phi (i)}, \quad \text { and } \quad \phi (i) <   \phi (i + 1) \text {   for   all   } i,
$$

ensuring the temporal order of original packets is preserved within the template. The remaining positions in $T \ ( \mathrm { i . e . }$ , indices $j \not \in \mathrm { I m } ( \phi ) )$ are filled with dummy packets:

$$
\hat {u} _ {j} = \left\{ \begin{array}{l l} u _ {i} & \text { if } j = \phi (i), \\ d _ {j} = t _ {j} & \text { otherwise }. \end{array} \right.
$$

Thus, the final morphed sequence $\hat { U } = \{ \hat { u } _ { 1 } , \hat { u } _ { 2 } , \dots , \hat { u } _ { m } \}$ retains all packets from U (no deletions) and augments them with structurally aligned dummy packets such that $\hat { U }$ statistically resembles $T \colon$ :

$$
\hat {U} \approx T, \quad \text { with } \quad \mathrm{WF} (\hat {U}) \not \approx \mathrm{WF} (U),
$$

where $\mathrm { W F } ( \cdot )$ represents the fingerprinting model’s output on a given traffic sequence.

This real-time transformation ensures that WF models trained on unaltered patterns cannot easily recognize or classify U<sup>ˆ</sup> . Importantly, the morphing process maintains the functional integrity of the communication session by preserving all genuine packets, thereby avoiding usability degradation.

TGTO core morphing logic. Given a user trace U and a template repository T , TGTO first selects a guiding template T and then reshapes the observable direction sequence by aligning real packets to the template when possible and injecting dummy packets otherwise. Algorithm 2 formalizes this process step by step, making the morphing procedure explicit and reproducible.

Bounded Morphing and Misalignment Handling. In dynamic real-world Tor environments, factors such as personalized ads, dynamic resource loading, or minor ordering variations may cause the user trace to deviate from the selected template, leading to consecutive strict-matching failures. To prevent cascading dummy-packet insertion during Phase 2 (Sequence Interleaving), TGTO incorporates an explicit online overhead budget. Let δ denote the maximum acceptable dummy-insertion overhead ratio and |U| denote the length of the original user trace. We define the maximum dummy-packet budget as $\begin{array} { r } { B _ { \mathrm { m a x } } = \lfloor \delta \lvert U \rvert . } \end{array}$ . During morphing, dummy packets are inserted to enforce the template structure only when the total number of inserted dummies remains below $B _ { \mathrm { m a x } }$ . Once this budget is exhausted, TGTO relaxes the template constraint and forwards the remaining real packets in their original order. Consequently, TGTO serves as a bounded structural guide rather than a rigid packet-level replay mechanism. Even under persistent sequence misalignment, the additional dummypacket overhead is explicitly bounded by the predefined threshold δ. While this design ensures bounded overhead and system stability, exploring more flexible alignment mechanisms, such as window-based look-ahead matching and edit-distance-based matching, remains an important direction for future optimization.

## C. Adaptive Selection Strategy

The Adaptive Selection Strategy is a critical component of the TGTO framework, ensuring that template selection remains unpredictable and context-aware in the face of evolving website fingerprinting threats. Unlike static obfuscation schemes that may expose recurring patterns, this strategy introduces controlled randomness and network-awareness into template selection to maintain both security robustness and communication efficiency.

Let $\mathcal { T } ~ = ~ \{ T _ { 1 } , T _ { 2 } , \dots , T _ { K } \}$ be the set of all available traffic templates in the repository. For each traffic session, the system selects a template $T _ { k } \in \mathcal T$ according to a time-varying probability distribution:

$$
\mathbf {p} (t) = [ p _ {1} (t), p _ {2} (t), \ldots , p _ {K} (t) ], \quad \sum_ {k = 1} ^ {K} p _ {k} (t) = 1,
$$

where $p _ { k } ( t )$ denotes the probability of selecting template $T _ { k }$ at time t.

To balance security and performance, the probability $p _ { k } ( t )$ is computed based on multiple dynamic factors, including:

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Template-Guided Traffic Morphing (TGTO Core Logic)

Require: User Trace  $U = \{u_{1}, u_{2}, \ldots, u_{n}\}$ , Template Repository T, Max Overhead Ratio  $\delta$ .

Ensure: Obfuscated Trace  $U'$ .

1: Initialization:
2:  $U' \leftarrow \emptyset$  // Initialize result sequence
3: ptr  $\leftarrow 1$  // Pointer for user trace U
4:  $L \leftarrow \text{Length}(U)$  // Length of original trace
5:  $B_{\max} \leftarrow \lfloor \delta \cdot L \rfloor$  // Maximum dummy-packet budget
6: current_dummies  $\leftarrow 0$  // Counter for injected dummy packets
7: Phase 1: Template Selection
8:  $T \leftarrow \text{TEMPLATESELECT}(T)$  // Select a template  $T = \{t_{1}, \ldots, t_{m}\}$  (cf. Sec. IVD)
9: Phase 2: Sequence Interleaving
10: for each token  $t_{k}$  in Template T do
11: if ptr  $\leq L$  and  $u_{ptr} = t_{k}$  then
12:  $U' .append(u_{ptr})$  // Match: Real packet aligns with template
13: ptr  $\leftarrow ptr + 1$ 
14: else if  $t_{k} \in \{-1, +1\}$  then
15: if current_dummies &lt;  $B_{max}$  then
16:  $U' .append(t_{k})$  // Morph: Inject dummy packet
17: current_dummies  $\leftarrow$  current_dummies + 1
18: else
19: break // Budget exhausted, exit strict template matching early
20: end if
21: else
22: continue // Skip zero-padding in template
23: end if
24: end for
25: Phase 3: Residual Handling
26: if ptr  $\leq L$  then
27:  $U' .append(U[\text{ptr}:L])$  // Append remaining real packets in original order
28: end if
29: Phase 4: Normalization
30: if Length( $U'$ ) &gt; L then
31:  $U' \leftarrow U'[1:L]$  // Truncate to maintain feature vector size
32: else if Length( $U'$ ) &lt; L then
33:  $U' \leftarrow U' + ZeroPad(L - Length(U'))$  // Pad if shorter
34: end if
35: return  $U'$
</div>

• Network Condition Weight $w _ { k } ^ { \mathrm { ( n e t ) } } ( t )$ : penalizes templates that introduce high latency or overhead under current network conditions;

• Adversarial Exposure Weight $w _ { k } ^ { \mathrm { ( a d v ) } } ( t ) { : }$ : penalizes templates frequently selected in recent sessions, reducing vulnerability to pattern recognition;

• Entropy Regularization Function: encourages exploration and maintains unpredictability.

As a result, the final selection probability is computed using a softmax-based mechanism:

$$
p _ {k} (t) = \frac {\exp \left(- \alpha w _ {k} ^ {(\mathrm{net})} (t) - \beta w _ {k} ^ {(\mathrm{adv})} (t)\right)}{\sum_ {j = 1} ^ {K} \exp \left(- \alpha w _ {j} ^ {(\mathrm{net})} (t) - \beta w _ {j} ^ {(\mathrm{adv})} (t)\right)},
$$

where $\alpha , \beta > 0$ are tunable hyperparameters controlling the trade-off between performance and security.

To further defend against adaptive attackers, the system may apply stochastic perturbations to the weight vectors or inject randomness in the template pool by periodically updating $\tau$ with newly curated templates, ensuring long-term unpredictability. The entropy of the selection distribution is also monitored:

$$
\mathcal {H} (\mathbf {p} (t)) = - \sum_ {k = 1} ^ {K} p _ {k} (t) \log p _ {k} (t),
$$

and maintained above a threshold ${ \mathcal { H } } _ { \operatorname* { m i n } }$ to avoid degenerate selection behaviors dominated by a small subset of templates.

By continuously adapting $\mathbf { p } ( t )$ in response to both environmental conditions and adversarial behaviors, this strategy ensures that TGTO maintains a high degree of variability in its obfuscation patterns, reducing the effectiveness of pattern recognition techniques used in modern WF attacks while ensuring that the overhead remains tolerable under real-world conditions.

## D. Summary of the TGTO Defense Framework

In summary, TGTO presents a structured and adaptive defense framework against website fingerprinting attacks. By leveraging real traffic templates as semantic guides, TGTO performs meaningful traffic morphing that disrupts fingerprinting models without sacrificing usability. Distinct from traditional defenses based on random padding or timing perturbations, TGTO integrates template-driven obfuscation with a dynamic selection strategy, providing robustness against both static and adaptive WF adversaries. Its design strikes a balance between obfuscation strength and practical deployability, making it a promising direction for privacy-preserving defenses in dynamic, real-world browsing environments.

Deployment considerations. TGTO is designed as an endhost (client-side) traffic-shaping defense that operates before traffic enters the Tor tunnel, and therefore does not require modifications to Tor relays. In deployment, the Template Repository can be maintained locally, where each template is stored as a compact packet-direction sequence (with associated constraints), resulting in a small storage footprint. This enables practical distribution/update strategies such as (i) shipping a bundled template set with the client software, and (ii) providing an optional authenticated update channel that periodically refreshes a subset of templates to track long-term website evolution. Notably, TGTO does not require a unique template for every page load; a moderate pool of high-utility templates per site (or per site category) is sufficient and can be updated incrementally.

Our evaluation already incorporates realistic variability by collecting traces over two months from 15 geographically distributed servers (US and Singapore), which captures heterogeneous network latency and system performance. Nevertheless, we acknowledge that live Tor introduces additional factors (e.g., congestion dynamics, circuit churn, background activity) that may shift absolute attack/defense accuracy. TGTO does not aim to replay a template at fine-grained timing resolution; rather, it biases the observable trace toward template-induced structural patterns, which we quantify via the templatealignment analysis (TFS) in Section V.E.

Finally, TGTO is largely orthogonal to wire-level obfuscation provided by pluggable transports (PTs) (e.g., obfs4), since it shapes traffic before encryption/transport transformation; however, if a PT applies its own padding/shaping, interactions between mechanisms should be evaluated. We also clarify that repository scalability is controlled by bounding the number of templates and periodically refreshing a subset, keeping overhead manageable on commodity clients. Regarding adaptive attackers, we assume the attacker may know the defense algorithm but not the per-session randomness (template choice and parameter instantiation). The adaptive selection strategy in Section IV.D discourages repeatedly selecting the same templates (via exposure-aware weighting), improving diversity; we treat long-term attacker retraining on defended traces as an important limitation and future direction rather than claiming complete immunity.

## V. PERFORMANCE EVALUATION

This section empirically evaluates our proposed Few-shot Multi-tab Website Fingerprinting attack and the Template-Guided Traffic Obfuscation defense. We conduct a series of experiments to address the following research questions, aiming to assess their performance, practicality, and effectiveness under conditions relevant to real-world multi-tab browsing and defense against modern attacks:

• RQ I: How effective is FMWF in realistic multi-tab scenarios with varying numbers of opened tabs and limited fine-tuning traces, in terms of top-K accuracy, Precision, Recall, and F1-Score, compared to state-of-theart methods?

• RQ II: How robust is FMWF across different mainstream browsers (Google Chrome and Microsoft Edge) and varying levels of traffic complexity, particularly under limited fine-tuning samples and high-concurrency scenarios such as the 10-tab setting?

• RQ III: How effective is FMWF in open-world settings featuring non-monitored websites?

• RQ IV: How effective is TGTO in mitigating multitab WF attacks across different models, and how does its performance and overhead compare to conventional defenses in terms of top-K accuracy, Precision, Recall, and F1-Score?

• RQ V: To what extent do TGTO-obfuscated traces structurally align with their guiding real-traffic templates, i.e., does TGTO perform template-guided morphing rather than injecting unstructured noise?

The experimental results presented based on these questions validate FMWF’s capabilities as a practical few-shot multi-tab attack and demonstrate TGTO’s efficacy and efficiency as a countermeasure.

## A. Experiment Setup

1) Datasets: For this study, we constructed three distinct datasets comprising web traffic traces captured from three widely used browsers: Tor Browser, Microsoft Edge, and Google Chrome. These datasets were utilized to evaluate the performance and generalization capabilities of our proposed

FMWF attack and TGTO defense under various browsing scenarios.

Tor Dataset. Following the methodology outlined in [19], we collected Tor traffic traces over a two-month period. Data was captured using 15 Alibaba Cloud servers with varying hardware configurations, strategically located in the US and Singapore. This setup was designed to simulate diverse user environments, accounting for variations in network latency, system performance, and temporal conditions. We selected the top 100 most popular websites from the Majestic Million ranking<sup>1</sup>as our monitored targets. For each monitored website, we collected 100 single-tab traffic traces by repeatedly accessing the site via the Tor Browser, resulting in a total of 10,000 single-tab traces. To collect multi-tab datasets, we randomly combined these 100 websites to generate 2-tab, 3-tab, 4-tab, and 5-tab scenarios, also using the Tor Browser. For the openworld evaluation, we utilized the open-world dataset provided by [19].

To address template realism, we clarify that the Obfuscation Template Repository used by TGTO is constructed from the same real Tor traces collected above, rather than from synthetic or ad-hoc generation. Our collection protocol follows the rigorous methodology in Deng et al. [19] and is consistent with established automation-based collection practices in prior WF studies (e.g., [2]).

Specifically, the raw candidate pool for templates is extracted from Tor Browser traces collected over two months using 15 geographically distributed cloud servers (US and Singapore) with heterogeneous hardware configurations, which captures realistic variability in circuits, latency, and system conditions. We extract direction-only sequences from these real traces and then apply the multi-stage curation pipeline described in Section IV.B to select a compact set of highutility templates.

Microsoft Edge and Google Chrome Datasets. We adopted a traffic collection methodology aligned with previous research [2] for clear-web traffic. Traffic capture was performed using Tshark, while Python with the PyAutoGUI library was employed for automating Browse sessions. Using Microsoft Edge and Google Chrome, we collected singletab traffic traces by visiting a monitored set of 100 websites selected from the top sites on chinaz.com<sup>2</sup>. For each monitored website and each browser, we collected 50 traces, resulting in a total of 5,000 single-tab traces per browser. We randomly combined the 100 target websites to collect 2-tab, 3-tab, 4-tab, and 5-tab datasets.

2) Parameter Settings: We conducted an extensive search of the hyperparameter space to evaluate and select the optimal hyperparameters for FMWF. Table I lists the key hyperparameters we tuned, the range of candidate values, and the final selected values.

TABLE I  
HYPERPARAMETER SELECTION FOR THE FMWF

<table><tr><td>Parameters</td><td>Search Space</td><td>Selected Value</td></tr><tr><td>Feature Extractor</td><td>GoogleNet, ResNet, DF</td><td>DF</td></tr><tr><td>Classifier</td><td>MLP, Linear</td><td>MLP</td></tr><tr><td>Optimizer</td><td>SGD, Adam</td><td>Adam</td></tr><tr><td>Batch Size</td><td>[32,64,128]</td><td>32</td></tr><tr><td>Embedded Vector&#x27;s Size</td><td>[64,128,256,512]</td><td>512</td></tr></table>

## B. Metrics

To assess the effectiveness of our multi-tab website fingerprinting attack, we adopt evaluation metrics commonly used in prior studies [18], [19], [31], [51], [52].

Closed-world Scenario. In the closed-world scenario, multi-tab WF attacks are framed as a multi-tab multi-class classification problem, where each traffic instance may correspond to multiple concurrently visited websites. For this, we employ the multi-tab-specific metric, Top-k Accuracy (A@K), and conventional multi-class metrics such as Precision, Recall, and F1-score. These metrics comprehensively evaluate the model’s performance by assessing the prediction outcomes for each website across all instances. Let y denote the true label vector for an instance x, where $y _ { i } = 1$ indicates that x visited the i-th website, and $y _ { i } = 0$ otherwise. Similarly, yˆ represents the predicted label vector, where each element corresponds to the predicted probability that x visited a specific website. A@K is used to measure how many of them visited websites appear in the top-k predicted websites based on yˆ. The formulation of A@K is as follows: $\mathbf { A } @ \mathbf { k } =$ $\frac { 1 } { k } \sum _ { l \in r _ { k } ( \hat { y } ) } y _ { l }$ , where $r _ { k } ( \hat { y } )$ denotes the set of websites with the top-k highest probabilities in the predicted label vector yˆ. This metric evaluates the effectiveness of the model in ranking the true websites among the top predictions. Additionally, we compute Precision, Recall, and F1-score to assess the performance of our model further. These metrics are calculated based on the number of true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN) for each website. The formulas for these metrics are given as: Precision $\begin{array} { r } { = \frac { T P } { T P + F P } , \mathrm { R e c a l l } = \frac { T P } { T P + F N } } \end{array}$ , and $\begin{array} { r } { \mathrm { F 1 - S c o r e } = \frac { \mathrm { 2 } \times \mathrm { P r e c i s i o n } \times \mathrm { R e c a l l } } { \mathrm { P r e c i s i o n } + \mathrm { R e c a l l } } } \end{array}$ The average values of these metrics are computed across all websites to provide an overall performance measure.

Open-world Scenario. In the open-world scenario, we assess the proposed method by following established practices from previous studies [18], [31]. In this context, all nonmonitored websites are aggregated into a single category, enabling us to evaluate the model’s performance in accurately identifying the websites a user visits, even amidst a vast array of potentially unseen sites. This approach not only tests the adaptability and robustness of FMWF but also reflects more realistic browsing conditions, where users interact with a mix of known and unknown websites.

## C. Closed-world Evaluation

We evaluate our proposed FMWF attack within the closedworld setting by comparing its performance against three representative state-of-the-art multi-tab WF baselines: ARES

Enhanced-FMWF (Ours) ARES (SP’23) TMWF (CCS’23) ∗ BAPM (ACSAC’21) FMWF (WWW’25)

![](images/f901b76751266c6314aa3e9f166fa13c7c11e69948141425fb6a51999abfda64.jpg)  
(a) 2-tab setting (A@2)

![](images/e34a09d1dfdbe90ef54e5e2faf6b7aa7723a6a8e6d6fcbbadadb4ae406c800a7.jpg)  
(b) 3-tab setting (A@3)

![](images/0504cd1e1dbe23ef0d969991a5f691cd07dc562e062a5e6378199bf7a2366869.jpg)  
(c) 4-tab setting (A@4)

![](images/0d23beeac3fc1aa70cd17a5e902e2c8b7cdd4e0ba97b52ef951796c51ecf0a69.jpg)  
(d) 5-tab setting (A@5)  
Fig. 6. Comparison of FMWF with state-of-the-art multi-tab WF attacks, where A@K represents the top-k Accuracy.

TABLE II  
COMPARISON OF FMWF WITH PRIOR ARTS IN PRECISION, RECALL, AND F1-SCORE ACROSS DIFFERENT TABS AND SAMPLE NUMBERS (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="3">2-tab</td><td colspan="3">3-tab</td><td colspan="3">4-tab</td><td colspan="3">5-tab</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">BAPM (ACSAC&#x27;21)</td><td>10</td><td>0.714</td><td>0.715</td><td>0.676</td><td>0.651</td><td>0.643</td><td>0.622</td><td>0.680</td><td>0.661</td><td>0.650</td><td>0.675</td><td>0.685</td><td>0.668</td></tr><tr><td>20</td><td>0.777</td><td>0.810</td><td>0.769</td><td>0.733</td><td>0.739</td><td>0.715</td><td>0.753</td><td>0.774</td><td>0.752</td><td>0.762</td><td>0.781</td><td>0.764</td></tr><tr><td>30</td><td>0.809</td><td>0.836</td><td>0.804</td><td>0.779</td><td>0.784</td><td>0.761</td><td>0.801</td><td>0.817</td><td>0.800</td><td>0.815</td><td>0.839</td><td>0.819</td></tr><tr><td>40</td><td>0.821</td><td>0.856</td><td>0.822</td><td>0.808</td><td>0.819</td><td>0.795</td><td>0.818</td><td>0.838</td><td>0.820</td><td>0.851</td><td>0.865</td><td>0.850</td></tr><tr><td rowspan="4">TMWF (CCS&#x27;23)</td><td>10</td><td>0.712</td><td>0.762</td><td>0.724</td><td>0.638</td><td>0.691</td><td>0.654</td><td>0.633</td><td>0.680</td><td>0.647</td><td>0.656</td><td>0.704</td><td>0.673</td></tr><tr><td>20</td><td>0.784</td><td>0.819</td><td>0.794</td><td>0.727</td><td>0.780</td><td>0.745</td><td>0.741</td><td>0.783</td><td>0.756</td><td>0.774</td><td>0.816</td><td>0.789</td></tr><tr><td>30</td><td>0.822</td><td>0.853</td><td>0.831</td><td>0.785</td><td>0.816</td><td>0.792</td><td>0.787</td><td>0.823</td><td>0.799</td><td>0.824</td><td>0.859</td><td>0.837</td></tr><tr><td>40</td><td>0.858</td><td>0.887</td><td>0.866</td><td>0.817</td><td>0.854</td><td>0.830</td><td>0.824</td><td>0.866</td><td>0.840</td><td>0.850</td><td>0.884</td><td>0.863</td></tr><tr><td rowspan="4">ARES (SP&#x27;23)</td><td>10</td><td>0.881</td><td>0.823</td><td>0.827</td><td>0.860</td><td>0.835</td><td>0.820</td><td>0.858</td><td>0.793</td><td>0.808</td><td>0.868</td><td>0.790</td><td>0.810</td></tr><tr><td>20</td><td>0.877</td><td>0.895</td><td>0.875</td><td>0.873</td><td>0.905</td><td>0.872</td><td>0.907</td><td>0.865</td><td>0.876</td><td>0.913</td><td>0.910</td><td>0.909</td></tr><tr><td>30</td><td>0.890</td><td>0.905</td><td>0.882</td><td>0.897</td><td>0.910</td><td>0.882</td><td>0.914</td><td>0.918</td><td>0.914</td><td>0.922</td><td>0.920</td><td>0.917</td></tr><tr><td>40</td><td>0.914</td><td>0.915</td><td>0.904</td><td>0.894</td><td>0.925</td><td>0.902</td><td>0.939</td><td>0.915</td><td>0.918</td><td>0.935</td><td>0.924</td><td>0.928</td></tr><tr><td rowspan="4">FMWF (WWW&#x27;25)</td><td>10</td><td>0.885</td><td>0.800</td><td>0.794</td><td>0.779</td><td>0.725</td><td>0.724</td><td>0.890</td><td>0.770</td><td>0.775</td><td>0.849</td><td>0.740</td><td>0.757</td></tr><tr><td>20</td><td>0.883</td><td>0.865</td><td>0.849</td><td>0.867</td><td>0.840</td><td>0.835</td><td>0.903</td><td>0.893</td><td>0.889</td><td>0.929</td><td>0.892</td><td>0.894</td></tr><tr><td>30</td><td>0.894</td><td>0.896</td><td>0.879</td><td>0.893</td><td>0.881</td><td>0.875</td><td>0.935</td><td>0.918</td><td>0.909</td><td>0.927</td><td>0.908</td><td>0.912</td></tr><tr><td>40</td><td>0.916</td><td>0.920</td><td>0.904</td><td>0.902</td><td>0.926</td><td>0.909</td><td>0.928</td><td>0.920</td><td>0.914</td><td>0.925</td><td>0.920</td><td>0.915</td></tr><tr><td rowspan="4">Enhanced-FMWF (Ours)</td><td>10</td><td>0.880</td><td>0.855</td><td>0.833</td><td>0.848</td><td>0.855</td><td>0.818</td><td>0.857</td><td>0.803</td><td>0.814</td><td>0.840</td><td>0.796</td><td>0.804</td></tr><tr><td>20</td><td>0.892</td><td>0.910</td><td>0.874</td><td>0.868</td><td>0.910</td><td>0.874</td><td>0.905</td><td>0.898</td><td>0.897</td><td>0.923</td><td>0.906</td><td>0.912</td></tr><tr><td>30</td><td>0.903</td><td>0.905</td><td>0.889</td><td>0.900</td><td>0.910</td><td>0.885</td><td>0.925</td><td>0.913</td><td>0.911</td><td>0.921</td><td>0.924</td><td>0.921</td></tr><tr><td>40</td><td>0.919</td><td>0.930</td><td>0.910</td><td>0.907</td><td>0.915</td><td>0.906</td><td>0.929</td><td>0.918</td><td>0.920</td><td>0.928</td><td>0.926</td><td>0.925</td></tr></table>

(SP’23) [19], TMWF (CCS’23) [20], and BAPM (AC-SAC’21) [21]. These methods represent leading end-to-end approaches for multi-tab traffic analysis. Performance is assessed using datasets collected from Google Chrome, Microsoft Edge, and Tor Browser to evaluate FMWF’s crossbrowser generalizability and robustness. To ensure statistical reliability, results for each scenario are averaged over five independently sampled test sets. Unless otherwise specified (e.g., in RQ II), results primarily report performance on the Tor Browser dataset, which offers a realistic representation of multi-tab traffic under privacy-preserving conditions.

AQ I-1: Evaluating the Influence of N on Top-K Accuracy (A@K) Performance. This experiment assesses the impact of varying the number of few-shot fine-tuning traces per label (N ∈ {10, 15, 20, 25, 30, 35, 40}) on FMWF’s A@K performance in 100-way multi-tab settings [19], [51].

To directly quantify the incremental improvement of this journal extension over our WWW’25 version, we additionally include a controlled ablation under identical backbone and training/evaluation protocol, where the only change is the augmentation module (WWW’25 augmentation vs. our refined overlap-aware augmentation). For clarity, Enhanced-FMWF refers to this setting where the backbone and training recipe remain unchanged and only the augmentation is updated. We report A@K with K = m (e.g., top-3 for 3-tab), which measures how well the model ranks the true visited websites within the top-m predictions.

As shown in Figure 6, FMWF achieves competitive performance against SOTA multi-tab WF baselines (ARES, TMWF, BAPM) across 2-tab to 5-tab few-shot scenarios. FMWF consistently outperforms TMWF and BAPM; for example, at N=15 in the 2-tab setting, its A@2 exceeds 0.8, significantly higher than their sub-0.70 scores. FMWF remains competitive with ARES, demonstrating strong accuracy despite its lightweight structure. Performance generally improves with increasing N. High A@K for larger K indicates robustness in identifying multiple sites, validating its few-shot effectiveness in challenging multi-tab environments.

Moreover, the controlled ablation shows that the refined augmentation yields consistent and quantifiable improvements in A@K under identical settings. For example, A@3 increases from 0.690 to 0.737 in the 3-tab, N=10 setting (+4.7 points), A@5 increases from 0.850 to 0.880 in the 5-tab, N=25 setting (+3.0 points), and A@2 increases from 0.760 to 0.800 in the

2-tab, N=15 setting (+4.0 points), as summarized in Figure 6.

AQ I-2: Effect of Fine-Tuning Traces N on Precision, Recall, and F1-Score. We evaluate how the number of finetuning traces per label (N) impacts FMWF’s classification performance across different multi-tab settings using Precision, Recall, and F1-Score as evaluation metrics.

As reported in Table II, FMWF consistently outperforms state-of-the-art baselines across all tab configurations. For example, in the 2-tab, 100-way 40-shot setting, FMWF achieves an F1-Score of 0.910, significantly exceeding BAPM (0.822) and TMWF (0.866). This advantage persists as the number of concurrent tabs increases, with FMWF maintaining high scores in more challenging 3-tab, 4-tab, and 5-tab scenarios.

Notably, FMWF demonstrates strong performance even with fewer fine-tuning traces. In the 5-tab case with only 20 traces per label, it achieves an F1-Score of 0.912, outperforming ARES (0.909), TMWF (0.789), and BAPM (0.764). These results highlight FMWF’s robustness and adaptability in complex, data-scarce multi-tab environments.

In addition, Table II reports the controlled ablation between the WWW’25 augmentation and our refined overlap-aware augmentation (Enhanced-FMWF). The largest gain in multitab quality is observed at 3-tab, N=10, where the F1-score increases from 0.724 to 0.818 (+9.4 points). Overall, under identical backbones and training settings, the refined augmentation improves A@K by up to 4.7 points and F1-score by up to 9.4 points across the few-shot multi-tab configurations.

TABLE III  
PERFORMANCE OF FMWF WITHOUT PRIOR KNOWLEDGE OF THE NUMBER OF TABS, ACROSS SAMPLE NUMBERS (N).

<table><tr><td>The value of N</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>10</td><td>0.787</td><td>0.689</td><td>0.685</td></tr><tr><td>15</td><td>0.852</td><td>0.805</td><td>0.795</td></tr><tr><td>20</td><td>0.870</td><td>0.825</td><td>0.816</td></tr><tr><td>25</td><td>0.872</td><td>0.851</td><td>0.837</td></tr><tr><td>30</td><td>0.886</td><td>0.877</td><td>0.861</td></tr><tr><td>35</td><td>0.894</td><td>0.893</td><td>0.876</td></tr><tr><td>40</td><td>0.908</td><td>0.920</td><td>0.905</td></tr></table>

AQ I-3: Comparison with RobustWF (INFOCOM’24). To strengthen the baseline coverage, we further compare our method with RobustWF [9], a recent lightweight multi-tab WF approach. We implement RobustWF following the description in [9] and evaluate it under the same few-shot multi-tab settings as our main closed-world experiments (same dataset, tab configurations, shot budgets N, and evaluation protocol). Figure 7 reports the Top-k accuracy (A@3 and A@5), and Table IV reports the multi-tab metrics (Precision, Recall, and F1-score).

As shown in Figure 7, Enhanced-FMWF consistently outperforms RobustWF across all evaluated shot budgets. For example, in the 3-tab setting with N=20, Enhanced-FMWF achieves A@3 of 0.838 compared to 0.430 for RobustWF; in the 5-tab setting with N=20, Enhanced-FMWF achieves A@5 of 0.823 while RobustWF reaches 0.370. Table IV shows the same trend in multi-tab quality: in the 5-tab setting with N=20, Enhanced-FMWF attains an F1-score of 0.925 versus 0.563 for RobustWF, and under the most data-scarce case (N=10), Enhanced-FMWF maintains an F1-score above 0.80 while RobustWF remains below 0.40.

A plausible reason is that the two approaches target different data regimes. RobustWF leverages causality correlation and context learning to model cross-tab dependencies, which can benefit from richer labeled multi-tab data; in contrast, Enhanced-FMWF is tailored to the few-shot regime via transfer learning with large-scale synthetic multi-tab pretraining, enabling stronger adaptation with limited real multitab supervision.

![](images/a6c3fbf6ae3d248f8e88051a999e83059f5756907c8214fd237ca896d8d55c97.jpg)

![](images/21c9d29582d1b1c41a0a4edf9ae786532b56c1b59328d68c3727bd24b4daf45f.jpg)  
(a) 3-tab setting (A@3)  
(b) 5-tab setting (A@5)  
Fig. 7. Top-k accuracy comparison between Enhanced-FMWF and RobustWF under the same few-shot multi-tab setting. We report A@K with K = m for m-tab sessions (A@3 for 3-tab and A@5 for 5-tab) across different shot budgets N.

TABLE IV  
COMPARISON OF FMWF WITH ROBUSTWF IN PRECISION, RECALL, AND F1-SCORE ACROSS DIFFERENT TABS AND SAMPLE NUMBERS (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="3">3-tab</td><td colspan="3">5-tab</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">RobustWF (INFOCOM&#x27;24)</td><td>10</td><td>0.659</td><td>0.397</td><td>0.424</td><td>0.550</td><td>0.354</td><td>0.385</td></tr><tr><td>20</td><td>0.713</td><td>0.497</td><td>0.516</td><td>0.609</td><td>0.471</td><td>0.491</td></tr><tr><td>30</td><td>0.735</td><td>0.590</td><td>0.596</td><td>0.632</td><td>0.546</td><td>0.559</td></tr><tr><td>40</td><td>0.720</td><td>0.617</td><td>0.618</td><td>0.647</td><td>0.554</td><td>0.563</td></tr><tr><td rowspan="4">Enhanced-FMWF (Ours)</td><td>10</td><td>0.848</td><td>0.855</td><td>0.818</td><td>0.840</td><td>0.796</td><td>0.804</td></tr><tr><td>20</td><td>0.868</td><td>0.910</td><td>0.874</td><td>0.923</td><td>0.906</td><td>0.912</td></tr><tr><td>30</td><td>0.900</td><td>0.910</td><td>0.885</td><td>0.921</td><td>0.924</td><td>0.921</td></tr><tr><td>40</td><td>0.907</td><td>0.915</td><td>0.906</td><td>0.928</td><td>0.926</td><td>0.925</td></tr></table>

AQ I-4: Evaluating FMWF Without Prior Knowledge of the Number of Tabs. To simulate realistic user behavior, we assess FMWF in a setting where the number of simultaneously opened tabs is unknown to the attacker. We construct a mixed dataset comprising equal proportions of 2-tab, 3-tab, 4-tab, and 5-tab traces to reflect this uncertainty.

As shown in Table III, FMWF achieves consistently strong results across different values of N, demonstrating its robustness in the absence of tab-count information. For example, with N = 25, FMWF reaches a Precision of 0.872, Recall of 0.851, and F1-Score of 0.837. Notably, the model exhibits consistent and robust performance as N increases, indicating that FMWF can effectively handle multi-tab traffic even without prior knowledge of the number of tabs. This showcases the adaptability and effectiveness of FMWF in real-world browsing environments.

AQ II-1: Performance of FMWF on Google Chrome and Microsoft Edge. We assess the generalization of FMWF on two mainstream non-anonymous browsers, Google Chrome and Microsoft Edge, which exhibit richer traffic characteristics (e.g., packet size and direction) compared to Tor. Due to these features, FMWF achieves high performance with significantly fewer fine-tuning samples.

TABLE V  
COMPARISON OF FMWF WITH PRIOR ARTS IN A@K ACROSS DIFFERENT TABS AND SAMPLE NUMBERS (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">The value of N</td><td colspan="2">2-tab (A@2)</td><td colspan="2">3-tab (A@3)</td><td colspan="2">4-tab (A@4)</td><td colspan="2">5-tab (A@5)</td></tr><tr><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td></tr><tr><td rowspan="3">BAPM (ACSAC&#x27;21)</td><td>1</td><td>0.598</td><td>0.643</td><td>0.514</td><td>0.578</td><td>0.462</td><td>0.457</td><td>0.343</td><td>0.361</td></tr><tr><td>2</td><td>0.752</td><td>0.794</td><td>0.659</td><td>0.737</td><td>0.644</td><td>0.632</td><td>0.537</td><td>0.525</td></tr><tr><td>3</td><td>0.797</td><td>0.830</td><td>0.724</td><td>0.784</td><td>0.710</td><td>0.671</td><td>0.618</td><td>0.646</td></tr><tr><td rowspan="3">TMWF (CCS&#x27;23)</td><td>1</td><td>0.363</td><td>0.496</td><td>0.237</td><td>0.357</td><td>0.197</td><td>0.262</td><td>0.135</td><td>0.213</td></tr><tr><td>2</td><td>0.554</td><td>0.721</td><td>0.507</td><td>0.619</td><td>0.413</td><td>0.548</td><td>0.323</td><td>0.424</td></tr><tr><td>3</td><td>0.684</td><td>0.803</td><td>0.628</td><td>0.711</td><td>0.598</td><td>0.664</td><td>0.482</td><td>0.579</td></tr><tr><td rowspan="3">ARES (SP&#x27;23)</td><td>1</td><td>0.821</td><td>0.823</td><td>0.876</td><td>0.695</td><td>0.711</td><td>0.663</td><td>0.612</td><td>0.606</td></tr><tr><td>2</td><td>0.929</td><td>0.949</td><td>0.905</td><td>0.897</td><td>0.826</td><td>0.875</td><td>0.835</td><td>0.847</td></tr><tr><td>3</td><td>0.965</td><td>0.970</td><td>0.927</td><td>0.915</td><td>0.908</td><td>0.906</td><td>0.857</td><td>0.894</td></tr><tr><td rowspan="3">FMWF (Ours)</td><td>1</td><td>0.799</td><td>0.831</td><td>0.737</td><td>0.699</td><td>0.720</td><td>0.677</td><td>0.593</td><td>0.619</td></tr><tr><td>2</td><td>0.938</td><td>0.945</td><td>0.909</td><td>0.862</td><td>0.845</td><td>0.873</td><td>0.829</td><td>0.844</td></tr><tr><td>3</td><td>0.969</td><td>0.974</td><td>0.920</td><td>0.918</td><td>0.900</td><td>0.909</td><td>0.872</td><td>0.896</td></tr></table>

TABLE VI  
EVALUATING FMWF PERFORMANCE (PRECISION, RECALL, F1-SCORE) IN THE 10-TAB SCENARIO.

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="3">10-tab</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="5">BAPM (ACSAC&#x27;21)</td><td>1</td><td>0.323</td><td>0.103</td><td>0.121</td></tr><tr><td>2</td><td>0.607</td><td>0.398</td><td>0.422</td></tr><tr><td>3</td><td>0.685</td><td>0.535</td><td>0.560</td></tr><tr><td>4</td><td>0.649</td><td>0.372</td><td>0.396</td></tr><tr><td>5</td><td>0.894</td><td>0.397</td><td>0.412</td></tr><tr><td rowspan="5">TMWF (CCS&#x27;23)</td><td>1</td><td>0.562</td><td>0.070</td><td>0.084</td></tr><tr><td>2</td><td>0.709</td><td>0.119</td><td>0.128</td></tr><tr><td>3</td><td>0.568</td><td>0.231</td><td>0.250</td></tr><tr><td>4</td><td>0.584</td><td>0.298</td><td>0.319</td></tr><tr><td>5</td><td>0.653</td><td>0.303</td><td>0.326</td></tr><tr><td rowspan="5">AERS (SP&#x27;23)</td><td>1</td><td>0.626</td><td>0.160</td><td>0.191</td></tr><tr><td>2</td><td>0.636</td><td>0.405</td><td>0.457</td></tr><tr><td>3</td><td>0.742</td><td>0.689</td><td>0.691</td></tr><tr><td>4</td><td>0.871</td><td>0.789</td><td>0.812</td></tr><tr><td>5</td><td>0.908</td><td>0.834</td><td>0.851</td></tr><tr><td rowspan="5">FMWF (Ours)</td><td>1</td><td>0.448</td><td>0.166</td><td>0.171</td></tr><tr><td>2</td><td>0.635</td><td>0.440</td><td>0.468</td></tr><tr><td>3</td><td>0.748</td><td>0.679</td><td>0.690</td></tr><tr><td>4</td><td>0.840</td><td>0.811</td><td>0.814</td></tr><tr><td>5</td><td>0.857</td><td>0.837</td><td>0.840</td></tr></table>

We compare FMWF against ARES, TMWF, and BAPM under 2-tab to 5-tab scenarios, using varying shot values N. As shown in Table V, FMWF consistently achieves the highest top-k accuracy across both browsers. Notably, with only 3 samples per label in the 2-tab setting, FMWF attains a top-2 accuracy of 0.969 on Chrome and 0.974 on Edge, outperforming ARES (0.960 and 0.970), TMWF (0.684 and 0.803), and BAPM (0.797 and 0.830). This advantage remains across more complex tab settings, demonstrating FMWF’s strong adaptability and robustness in diverse browser environments.

AQ II-2: Performance in High Concurrent Tabs (10- tab Scenario). We evaluate FMWF’s performance in the challenging 10-tab scenario under extreme few-shot conditions $( N ~ \in ~ \{ 1 , 2 , 3 , 4 , 5 \} )$ , reporting Precision, Recall, and F1- Score. This experiment is conducted using the Google Chrome dataset. As shown in Table VI, the 10-tab setting is difficult, especially at low N.

FMWF consistently and significantly outperforms other baselines, BAPM and TMWF, across all tested N. FMWF also proves highly competitive with the strongest baseline, ARES. While ARES achieves slightly higher F1 at N = 5 (0.851 vs FMWF’s 0.840), FMWF achieves a higher F1 at N = 4 (0.814 vs ARES’s 0.812), often demonstrating stronger Recall. Performance for FMWF and ARES improves considerably from N = 1 to N = 5. These results demonstrate FMWF’s effectiveness and robustness in complex 10-tab scenarios, achieving SOTA-level performance even with very limited fine-tuning data $( N \leq 5 )$ , and substantially surpassing BAPM and TMWF.

## D. AQ III: Open-world Evaluation

We evaluate FMWF in the open-world setting, where the adversary must distinguish monitored websites from a large pool of unmonitored ones. Following prior work [19], [21], [20], all unmonitored sites are grouped into a single class, while each monitored site remains a distinct class. To address class imbalance, we adopt the same strategy as [19], [25] by integrating closed-world and open-world traffic under the same tab configurations. For example, in the 2-tab setting, both closed- and open-world samples are combined to perform the 2-tab open-world evaluation.

We conduct few-shot fine-tuning with N = {1, 3, 5, 7, 10} traces per monitored class, and evaluate on a query set containing 4000 monitored and 10000 unmonitored instances. Table VII reports the top-2 accuracy of several baselines and our method. As shown, FMWF consistently outperforms prior state-of-the-art baselines (BAPM, TMWF, ARES) across all values of N. These results demonstrate FMWF’s ability to generalize well under highly imbalanced and realistic traffic conditions, while maintaining strong performance and efficiency compared to more complex transformer-based approaches.

TABLE VII  
PERFORMANCE EVALUATION OF FMWF IN THE OPEN-WORLD SCENARIO WITH DIFFERENT NUMBERS OF TRACES (N) FOR FEW-SHOT FINE-TUNING.

<table><tr><td rowspan="2">Method</td><td colspan="5">Number of Traces (N)</td></tr><tr><td>N=1</td><td>N=3</td><td>N=5</td><td>N=7</td><td>N=10</td></tr><tr><td>BAPM (ACSAC&#x27;21)</td><td>0.374</td><td>0.564</td><td>0.603</td><td>0.637</td><td>0.644</td></tr><tr><td>TMWF (CCS&#x27;23)</td><td>0.383</td><td>0.508</td><td>0.570</td><td>0.580</td><td>0.595</td></tr><tr><td>ARES (SP&#x27;23)</td><td>0.620</td><td>0.663</td><td>0.721</td><td>0.759</td><td>0.821</td></tr><tr><td>FMWF(Ours)</td><td>0.708</td><td>0.717</td><td>0.729</td><td>0.768</td><td>0.878</td></tr></table>

## E. AQ IV: Effectiveness of TGTO in Mitigating Multi-Tab WF Attacks

We evaluate the effectiveness and efficiency of TGTO in the closed-world Tor 2-tab scenario against four attack models (BAPM, TMWF, ARES, FMWF) and conventional defenses (Random Packet, Front, WTF-PAD). Figure 8 shows residual attack accuracy and average bandwidth overhead, while Table VIII shows residual attack Precision, Recall, and F1- Score. In addition, we further compare TGTO with a stronger modern defense baseline (TrafficSliver) in AQ IV-2.

Across all tested models and N values, TGTO consistently achieves the lowest residual attack accuracy and F1- score. TGTO substantially reduces attack performance for all tested models, whereas other defenses yield significantly higher residual accuracies and F1-scores. For example, against FMWF at 40-shot, TGTO reduces accuracy from 0.904 (No Defense) to 0.292 and F1-score from 0.910 to 0.308. Similarly, against TMWF, it reduces accuracy from 0.822 to 0.168 and F1-score from 0.866 to 0.216 at 40-shot.

TGTO achieves this high security with a competitive average bandwidth overhead of 45.31%, similar to WTF-PAD (45.54%) and Front Defense (38.40%), and significantly lower than Random Packet Defense (133.01%). This demonstrates that TGTO offers significantly better security at a competitive average overhead. In summary, TGTO is a practical, effective, and efficient defense, providing a superior security-performance balance against multi-tab WF attacks by achieving substantially lower residual attack accuracy and F1- score compared to conventional methods. We further validate the underlying template-guided mechanism by measuring the structural alignment between TGTO outputs and their selected real templates in AQ V. We further present a systematic bandwidth/latency trade-off analysis of TGTO under different overhead budgets in AQ IV-3.

AQ IV-2: Comparison with a Stronger Modern Defense Baseline To strengthen the baseline coverage beyond older padding defenses, we additionally compare TGTO with TrafficSliver [53], a representative modern defense against learning-based WF attacks. We implement TrafficSliver and evaluate it under the same closed-world Tor 2-tab setting and the same few-shot protocol used in AQ IV (same dataset, $N \in$ {10, 20, 30, 40}, and the same evaluation metrics). Table IX reports the residual Top-2 accuracy (A@2) against Enhanced-FMWF together with the corresponding Precision/Recall/F1- score. Overall, TGTO consistently yields lower residual accuracy and lower F1-score than TrafficSliver; for example, at N=40, TGTO reduces residual accuracy to 0.292 versus 0.540 for TrafficSliver, and reduces the F1-score to 0.308 versus 0.545 for TrafficSliver. These results suggest that TGTO’s template-guided structural morphing more effectively disrupts direction-sequence fingerprints in this multi-tab setting than traffic splitting alone.

TABLE X  
EXPANDED CROSS-DEFENSE COMPARISON OF OVERHEAD AND RESIDUAL ACCURACY AGAINST ENHANCED-FMWF (2-TAB).

<table><tr><td>Defense</td><td>N</td><td>Bandwidth overhead</td><td>Latency overhead</td><td>Residual accuracy</td></tr><tr><td rowspan="4">Random Packet Defense</td><td>10</td><td>130.40%</td><td>111.65%</td><td>0.348</td></tr><tr><td>20</td><td>133.82%</td><td>114.06%</td><td>0.486</td></tr><tr><td>30</td><td>134.33%</td><td>114.64%</td><td>0.566</td></tr><tr><td>40</td><td>134.45%</td><td>114.57%</td><td>0.622</td></tr><tr><td rowspan="4">FRONT</td><td>10</td><td>37.80%</td><td>0%</td><td>0.426</td></tr><tr><td>20</td><td>38.99%</td><td>0%</td><td>0.584</td></tr><tr><td>30</td><td>39.42%</td><td>0%</td><td>0.642</td></tr><tr><td>40</td><td>39.31%</td><td>0%</td><td>0.684</td></tr><tr><td rowspan="4">WTF-PAD</td><td>10</td><td>48.81%</td><td>0%</td><td>0.504</td></tr><tr><td>20</td><td>46.19%</td><td>0%</td><td>0.642</td></tr><tr><td>30</td><td>46.57%</td><td>0%</td><td>0.718</td></tr><tr><td>40</td><td>46.46%</td><td>0%</td><td>0.752</td></tr><tr><td rowspan="4">TGTO</td><td>10</td><td>44.87%</td><td>28.16%</td><td>0.112</td></tr><tr><td>20</td><td>46.81%</td><td>29.71%</td><td>0.190</td></tr><tr><td>30</td><td>46.80%</td><td>29.77%</td><td>0.234</td></tr><tr><td>40</td><td>47.04%</td><td>29.47%</td><td>0.292</td></tr></table>

AQ IV-3: Bandwidth/Latency Overhead Trade-offs of TGTO To assess practical deployability, we report the security–cost trade-off of TGTO under different configurations. We measure bandwidth overhead as the relative increase in transmitted Tor cells and latency overhead as the relative increase in trace duration / page-load time under the defense. All results are measured in the same closed-world Tor 2-tab setting against Enhanced-FMWF.

TABLE XI  
TGTO TRADE-OFF UNDER DIFFERENT TEMPLATE-LENGTH BUDGETS (m ≈ α · L<sub>REF</sub>) AGAINST ENHANCED-FMWF (2-TAB).

<table><tr><td>Budget α</td><td>N</td><td>Bandwidth overhead</td><td>Latency overhead</td><td>Residual accuracy</td></tr><tr><td rowspan="4">α = 1.37</td><td>10</td><td>36.96%</td><td>25.96%</td><td>0.130</td></tr><tr><td>20</td><td>37.32%</td><td>26.68%</td><td>0.214</td></tr><tr><td>30</td><td>37.29%</td><td>26.74%</td><td>0.286</td></tr><tr><td>40</td><td>37.93%</td><td>27.06%</td><td>0.338</td></tr><tr><td rowspan="4">α = 1.46</td><td>10</td><td>43.87%</td><td>28.16%</td><td>0.112</td></tr><tr><td>20</td><td>44.81%</td><td>29.71%</td><td>0.190</td></tr><tr><td>30</td><td>46.04%</td><td>29.77%</td><td>0.234</td></tr><tr><td>40</td><td>46.50%</td><td>29.47%</td><td>0.292</td></tr><tr><td rowspan="4">α = 1.75</td><td>10</td><td>72.66%</td><td>36.63%</td><td>0.071</td></tr><tr><td>20</td><td>74.69%</td><td>37.33%</td><td>0.133</td></tr><tr><td>30</td><td>75.36%</td><td>38.11%</td><td>0.200</td></tr><tr><td>40</td><td>76.37%</td><td>38.51%</td><td>0.242</td></tr></table>

Table X summarizes bandwidth overhead, latency overhead, and residual attack accuracy for TGTO and representative baselines across $N \in \{ 1 0 , 2 0 , 3 0 , 4 0 \}$ . The results show that, at comparable bandwidth budgets around 40–50%, TGTO consistently achieves substantially lower residual accuracy than WTF-PAD and FRONT across all N. For example, at

WTF-PAD

![](images/d690bb90dd1cd5440fe48dc3eb255cda0b4b1c62ed11463e74a1d9b214f4d002.jpg)  
(a) BAPM (ACSAC’21)

Front Defense

![](images/9e56753ee7d3c0d9fb9ecb99977d2e5b148083114821c1a191b6ab328782c7ba.jpg)  
(b) TMWF (CCS’23)

![](images/2ed267f220bab1e153f32dcad818459ae0c3f69fb028a927f269c8747c275da1.jpg)  
(c) ARES (SP’23)

![](images/fabe622e49fbc359c946c9693a274bfa56e602599041e9d57156c3c46bff59df.jpg)  
(d) FMWF (Ours)  
Fig. 8. Effectiveness Comparison of TGTO and Baseline Defenses effectiveness in Tor 2-Tab Scenario Against state-of-the-art multi-tab WF attacks, where Residual Attack Accuracy represents the top-2 Accuracy. TGTO achieves competitive protection with an average bandwidth overhead of 45.31%, compared to WTF-PAD (45.54%), Front (38.40%), and Random Packet Defense (133.01%).

TABLE VIII  
PERFORMANCE COMPARISON OF TGTO AND BASELINE DEFENSES AGAINST MULTI-TAB WF ATTACKS.

<table><tr><td rowspan="2">Method</td><td rowspan="2">Defence</td><td colspan="3">10shot</td><td colspan="3">20shot</td><td colspan="3">30shot</td><td colspan="3">40shot</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">BAPM (ACSAC&#x27;21)</td><td>No Defense</td><td>0.714</td><td>0.715</td><td>0.676</td><td>0.777</td><td>0.810</td><td>0.769</td><td>0.809</td><td>0.836</td><td>0.804</td><td>0.821</td><td>0.856</td><td>0.822</td></tr><tr><td>Random Packet Defense</td><td>0.479</td><td>0.421</td><td>0.385</td><td>0.547</td><td>0.536</td><td>0.486</td><td>0.578</td><td>0.592</td><td>0.538</td><td>0.591</td><td>0.630</td><td>0.574</td></tr><tr><td>Front Defense</td><td>0.617</td><td>0.582</td><td>0.546</td><td>0.663</td><td>0.676</td><td>0.630</td><td>0.694</td><td>0.704</td><td>0.663</td><td>0.720</td><td>0.734</td><td>0.695</td></tr><tr><td>WTF-PAD</td><td>0.563</td><td>0.596</td><td>0.537</td><td>0.634</td><td>0.660</td><td>0.613</td><td>0.674</td><td>0.705</td><td>0.661</td><td>0.695</td><td>0.764</td><td>0.701</td></tr><tr><td></td><td>TGTO</td><td>0.278</td><td>0.136</td><td>0.128</td><td>0.359</td><td>0.210</td><td>0.191</td><td>0.324</td><td>0.213</td><td>0.197</td><td>0.340</td><td>0.215</td><td>0.203</td></tr><tr><td rowspan="4">TMWF (CCS&#x27;23)</td><td>No Defense</td><td>0.712</td><td>0.762</td><td>0.724</td><td>0.784</td><td>0.819</td><td>0.794</td><td>0.822</td><td>0.853</td><td>0.831</td><td>0.858</td><td>0.887</td><td>0.866</td></tr><tr><td>Random Packet Defense</td><td>0.385</td><td>0.393</td><td>0.344</td><td>0.469</td><td>0.550</td><td>0.483</td><td>0.529</td><td>0.609</td><td>0.547</td><td>0.575</td><td>0.657</td><td>0.594</td></tr><tr><td>Front Defense</td><td>0.496</td><td>0.554</td><td>0.495</td><td>0.598</td><td>0.674</td><td>0.612</td><td>0.620</td><td>0.716</td><td>0.640</td><td>0.663</td><td>0.751</td><td>0.687</td></tr><tr><td>WTF-PAD</td><td>0.474</td><td>0.543</td><td>0.479</td><td>0.583</td><td>0.684</td><td>0.605</td><td>0.672</td><td>0.753</td><td>0.691</td><td>0.675</td><td>0.776</td><td>0.706</td></tr><tr><td></td><td>TGTO</td><td>0.216</td><td>0.161</td><td>0.142</td><td>0.383</td><td>0.184</td><td>0.171</td><td>0.381</td><td>0.225</td><td>0.206</td><td>0.536</td><td>0.238</td><td>0.216</td></tr><tr><td rowspan="4">ARES (SP&#x27;23)</td><td>No Defense</td><td>0.881</td><td>0.823</td><td>0.827</td><td>0.877</td><td>0.895</td><td>0.875</td><td>0.890</td><td>0.905</td><td>0.882</td><td>0.914</td><td>0.915</td><td>0.904</td></tr><tr><td>Random Packet Defense</td><td>0.624</td><td>0.385</td><td>0.391</td><td>0.704</td><td>0.494</td><td>0.500</td><td>0.718</td><td>0.584</td><td>0.582</td><td>0.792</td><td>0.616</td><td>0.625</td></tr><tr><td>Front Defense</td><td>0.736</td><td>0.357</td><td>0.324</td><td>0.792</td><td>0.420</td><td>0.370</td><td>0.787</td><td>0.431</td><td>0.380</td><td>0.816</td><td>0.458</td><td>0.404</td></tr><tr><td>WTF-PAD</td><td>0.798</td><td>0.627</td><td>0.644</td><td>0.830</td><td>0.736</td><td>0.745</td><td>0.868</td><td>0.792</td><td>0.794</td><td>0.871</td><td>0.818</td><td>0.819</td></tr><tr><td></td><td>TGTO</td><td>0.491</td><td>0.206</td><td>0.214</td><td>0.538</td><td>0.292</td><td>0.297</td><td>0.586</td><td>0.337</td><td>0.344</td><td>0.672</td><td>0.370</td><td>0.375</td></tr><tr><td rowspan="4">FMWF (Ours)</td><td>No Defense</td><td>0.880</td><td>0.855</td><td>0.833</td><td>0.892</td><td>0.910</td><td>0.874</td><td>0.903</td><td>0.905</td><td>0.889</td><td>0.919</td><td>0.930</td><td>0.910</td></tr><tr><td>Random Packet Defense</td><td>0.671</td><td>0.449</td><td>0.442</td><td>0.677</td><td>0.571</td><td>0.559</td><td>0.708</td><td>0.635</td><td>0.618</td><td>0.735</td><td>0.686</td><td>0.672</td></tr><tr><td>Front Defense</td><td>0.680</td><td>0.552</td><td>0.546</td><td>0.724</td><td>0.687</td><td>0.673</td><td>0.730</td><td>0.734</td><td>0.706</td><td>0.779</td><td>0.781</td><td>0.751</td></tr><tr><td>WTF-PAD</td><td>0.673</td><td>0.589</td><td>0.577</td><td>0.762</td><td>0.738</td><td>0.718</td><td>0.792</td><td>0.803</td><td>0.779</td><td>0.826</td><td>0.843</td><td>0.817</td></tr><tr><td></td><td>TGTO</td><td>0.413</td><td>0.136</td><td>0.139</td><td>0.603</td><td>0.234</td><td>0.234</td><td>0.737</td><td>0.270</td><td>0.275</td><td>0.797</td><td>0.309</td><td>0.308</td></tr></table>

TABLE IX

COMPARISON OF TRAFFICSLIVER AND TGTO AGAINST ENHANCED-FMWF, REPORTED IN A@2, PRECISION, RECALL, AND F1-SCORE ACROSS DIFFERENT N.

<table><tr><td>Defence Method</td><td>N</td><td>A@2</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">TrafficSliver</td><td>10</td><td>0.290</td><td>0.510</td><td>0.295</td><td>0.292</td></tr><tr><td>20</td><td>0.390</td><td>0.485</td><td>0.325</td><td>0.324</td></tr><tr><td>30</td><td>0.530</td><td>0.610</td><td>0.530</td><td>0.522</td></tr><tr><td>40</td><td>0.540</td><td>0.660</td><td>0.560</td><td>0.545</td></tr><tr><td rowspan="4">TGTO</td><td>10</td><td>0.112</td><td>0.413</td><td>0.136</td><td>0.139</td></tr><tr><td>20</td><td>0.190</td><td>0.603</td><td>0.234</td><td>0.234</td></tr><tr><td>30</td><td>0.234</td><td>0.737</td><td>0.270</td><td>0.275</td></tr><tr><td>40</td><td>0.292</td><td>0.797</td><td>0.309</td><td>0.308</td></tr></table>

N=40, TGTO reduces residual accuracy to 0.292 versus 0.684 (FRONT) and 0.752 (WTF-PAD), while using a similar bandwidth overhead (47.04% vs. 39.31% and 46.46%). Random Packet Defense exhibits the highest cost (over 130% bandwidth and over 110% latency overhead) yet still leaves a nontrivial residual accuracy (0.348–0.622), indicating poor costeffectiveness in this setting. We note that the 0% latency overhead reported for FRONT and WTF-PAD follows the common evaluation convention where padding is injected without intentionally delaying transmissions; by contrast, TGTO may introduce controlled waiting to satisfy template-guided timing constraints, resulting in non-zero latency overhead.

Table XI further characterizes TGTO’s internal trade-off by sweeping template-length budgets. Concretely, we compute a reference trace length $L _ { \mathrm { r e f } }$ as the average length of all 10,000 real 2-tab traces in our dataset, and parameterize TGTO using a budget factor α that controls the average template length in the repository $( m \approx \alpha \cdot L _ { \mathrm { r e f } } )$ . Since TGTO morphing follows the selected template, increasing α induces more dummy insertions and thus higher bandwidth and latency overhead, but yields stronger obfuscation. For instance, at $N { = } 1 0 ,$ , increasing α from 1.37 to 1.75 reduces residual accuracy from 0.130 to 0.071, while bandwidth overhead increases from 36.96% to 72.66% and latency overhead increases from 25.96% to 36.63%. The same monotonic trend holds at larger N (e.g., at $N { = } 4 0 , 0 . 3 3 8 \to 0 . 2 4 2$ with bandwidth $3 7 . 9 3 \%  7 6 . 3 7 \% )$ showing that α provides a direct and reproducible knob for selecting an operating point under a desired overhead budget.

AQ V: Template-guidance validation of TGTO via Traffic Feature Similarity (TFS). We validate whether TGTO indeed performs template-guided structural morphing (rather than injecting unstructured padding noise) by quantitatively measuring how closely TGTO-obfuscated traces align with their selected real-traffic templates. Specifically, we introduce Traffic Feature Similarity (TFS), a direction-sequence similarity metric motivated by normalized Hamming similarity and consistent with the common practice of modeling encrypted traffic as packet-direction sequences in WF (e.g., [18], [54], [55]). Figure 9 reports the empirical distribution of TFS values over 10,000 defended multi-tab traces.

Distribution of TFS between Template and TGTO-obfuscated Traces  
![](images/0e9fc8ba8ce0b70e5522d9a362e111c5eb8a52444502d9ed2c69874d4ac7afed.jpg)  
Fig. 9. Empirical distribution of Traffic Feature Similarity between traffic templates and 10, 000 TGTO-obfuscated traces. Most defended traces achieve TFS values around 0.9, and 83.98% of them satisfy $\mathrm { T F S } > 0 . 8 ,$ showing that TGTO effectively reshapes original traces to closely mimic the guiding templates.

Formally, we model each trace as a packet-direction sequence. Let $T ~ = ~ [ t _ { 1 } , \ldots , t _ { m } ]$ denote the guiding template extracted from real traces, and let $\hat { U } = [ \hat { u } _ { 1 } , \dots , \hat { u } _ { m } ]$ denote the TGTO-morphed sequence, where $t _ { i } , \hat { u } _ { i } \in \{ - 1 , + 1 \}$ . We define:

$$
\operatorname{TFS} (T, \hat {U}) = \frac {1}{m} \sum_ {i = 1} ^ {m} \mathbb {I} (t _ {i} = \hat {u} _ {i}),
$$

where I(·) is the indicator function. Intuitively, higher TFS indicates stronger structural alignment between the defended trace and its selected template, whereas values near chance level (around 0.5 under an uncorrelated baseline in this representation) indicate weak template structure.

As shown in Fig. 9, TGTO achieves a mean TFS of 0.921, with most samples tightly clustering around 0.9. Moreover, 8,398 out of 10,000 traces (83.98%) satisfy $\mathrm { T F S } ~ > ~ 0 . 8$ These results provide direct quantitative evidence that TGTO systematically reshapes traffic to follow the structure of real templates, supporting the fidelity of TGTO’s template-guided mechanism and complementing the effectiveness/overhead results reported in AQ IV.

## VI. CONCLUSION

In this work, we introduced a transformative few-shot multitab website fingerprinting attack framework that addresses the limitations of prior WF methods in realistic browsing scenarios. Existing approaches often rely on large-scale multitab datasets or rigid assumptions such as fixed tab counts, limiting their applicability and scalability. To overcome these constraints, we proposed a two-stage strategy combining synthetic data augmentation and few-shot fine-tuning, allowing FMWF to effectively identify websites in overlapping traffic streams with minimal real-world multi-tab data. Through pretraining on synthetic traces and few-shot fine-tuning with a small number of real multi-tab samples, FMWF achieves robust classification performance even in complex open-world scenarios, significantly outperforming state-of-the-art methods. To counteract this novel threat, we proposed Template-Guided Traffic Obfuscation, a practical and adaptive defense mechanism that reshapes traffic patterns using a template-driven strategy. TGTO incorporates a dynamic selection policy and a lightweight obfuscation module, offering robust resistance against advanced WF attacks while maintaining low overhead. Through comprehensive experiments across traffic from Tor, Microsoft Edge, and Google Chrome, we demonstrated that FMWF achieves state-of-the-art performance with significantly reduced data and computational requirements. Simultaneously, TGTO effectively degrades the accuracy of advanced WF attacks, outperforming existing defense mechanisms in both protection capability and efficiency. Our findings highlight both the growing threat posed by advanced WF models and the necessity of adaptable, practical defense mechanisms that can evolve alongside adversarial strategies.

## REFERENCES

[1] W. Meng, C. Ma, M. Ding, C. Ge, Y. Qian, and T. Xiang, “Beyond single tabs: A transformative few-shot approach to multi-tab website fingerprinting attacks,” in Proceedings of the ACM on Web Conference 2025, 2025, pp. 1068–1077.

[2] G. Huang, C. Ma, M. Ding, Y. Qian, C. Ge, L. Fang, and Z. Liu, “Efficient and low overhead website fingerprinting attacks and defenses based on tcp/ip traffic,” in Proceedings of the ACM Web Conference 2023, 2023, pp. 1991–1999.

[3] A. Mani, T. Wilson-Brown, R. Jansen, A. Johnson, and M. Sherr, “Understanding tor usage with privacy-preserving measurement,” in Proceedings of the Internet Measurement Conference 2018, 2018, pp. 175–187.

[4] T. Wang and I. Goldberg, “Improved website fingerprinting on tor,” in Proceedings of the 12th ACM workshop on Workshop on privacy in the electronic society, 2013, pp. 201–212.

[5] Q. Zhang, Z. Teng, X. Wang, Y. Gao, Q. Liu, and J. Shi, “Hsdirsniper: A new attack exploiting vulnerabilities in tor’s hidden service directories,” in Proceedings ofthe ACM Web Conference 2024, 2024, pp. 1812–1823.

[6] R. Jansen, R. Wails, and A. Johnson, “A measurement of genuine tor traces for realistic website fingerprinting,” arXiv preprint arXiv:2404.07892, 2024.

[7] L. Qiao, B. Wu, H. Li, C. Gao, W. Yuan, and X. Luo, “Trace-agnostic and adversarial training-resilient website fingerprinting defense,” in IEEE INFOCOM 2024-IEEE Conference on Computer Communications. IEEE, 2024, pp. 211–220.

[8] P. Syverson, R. Dingledine, and N. Mathewson, “Tor: The secondgeneration onion router,” in Usenix Security, vol. 10. USENIX Association Berkeley, CA, 2004.

[9] S. Chen, S. Chen, H. He, X. Jiang, J. Yang, and S. Cheng, “Causality correlation and context learning aided robust lightweight multi-tab website fingerprinting over encrypted tunnel,” in IEEE INFOCOM 2024- IEEE Conference on Computer Communications. IEEE, 2024, pp. 761– 770.

[10] Y. Liu, X. Wang, B. Qu, and F. Zhao, “Atvitsc: A novel encrypted traffic classification method based on deep learning,” IEEE Transactions on Information Forensics and Security, 2024.

[11] G. Mitra, P. K. Vairam, S. Saha, N. Chandrachoodan, and V. Kamakoti, “Snoopy: A webpage fingerprinting framework with finite query model for mass-surveillance,” IEEE Transactions on Dependable and Secure Computing, vol. 20, no. 5, pp. 3734–3752, 2022.

[12] D. Li, J. Xiao, P. Jiang, J. Gui, D. Song, Y. Ma, G. Huang, and X. Liu, “Provaudit: Enhance high-level privacy inference through system provenance data,” IEEE Transactions on Dependable and Secure Computing, 2024.

[13] A. Bahramali, A. Bozorgi, and A. Houmansadr, “Realistic website fingerprinting by augmenting network traces,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1035–1049.

[14] C. Luo, W. Tang, Q. Wang, and D. Zheng, “Few-shot website fingerprinting with distribution calibration,” IEEE Transactions on Dependable and Secure Computing, 2024.

[15] A. Panchenko, F. Lanze, J. Pennekamp, T. Engel, A. Zinnen, M. Henze, and K. Wehrle, “Website fingerprinting at internet scale.” in NDSS, vol. 1, 2016, p. 23477.

[16] T. Wang, X. Cai, R. Nithyanand, R. Johnson, and I. Goldberg, “Effective attacks and provable defenses for website fingerprinting,” in 23rd USENIX Security Symposium (USENIX Security 14), 2014, pp. 143– 157.

[17] J. Hayes and G. Danezis, “k-fingerprinting: A robust scalable website fingerprinting technique,” in 25th USENIX Security Symposium (USENIX Security 16), 2016, pp. 1187–1203.

[18] P. Sirinam, M. Imani, M. Juarez, and M. Wright, “Deep fingerprinting: Undermining website fingerprinting defenses with deep learning,” in Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, 2018, pp. 1928–1943.

[19] X. Deng, Q. Yin, Z. Liu, X. Zhao, Q. Li, M. Xu, K. Xu, and J. Wu, “Robust multi-tab website fingerprinting attacks in the wild,” in 2023 IEEE symposium on security and privacy (SP). IEEE, 2023, pp. 1005– 1022.

[20] Z. Jin, T. Lu, S. Luo, and J. Shang, “Transformer-based model for multitab website fingerprinting attack,” in Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, 2023, pp. 1050–1064.

[21] Z. Guan, G. Xiong, G. Gou, Z. Li, M. Cui, and C. Liu, “Bapm: block attention profiling model for multi-tab website fingerprinting attacks on tor,” in Proceedings of the 37th Annual Computer Security Applications Conference, 2021, pp. 248–259.

[22] M. Perry, “Padding negotiation. tor protocol specification proposal,” Tor Protocol Specification Proposal, Oct, 2015.

[23] M. Juarez, M. Imani, M. Perry, C. Diaz, and M. Wright, “Toward an efficient website fingerprinting defense,” in Computer Security– ESORICS 2016: 21st European Symposium on Research in Computer Security, Heraklion, Greece, September 26-30, 2016, Proceedings, Part I 21. Springer, 2016, pp. 27–46.

[24] X. Deng, Q. Li, and K. Xu, “Robust and reliable early-stage website fingerprinting attacks via spatial-temporal distribution analysis,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 1997–2011.

[25] Y. Xie, J. Feng, W. Huang, Y. Zhang, X. Sun, X. Chen, and X. Luo, “Contrastive fingerprinting: A novel website fingerprinting attack over few-shot traces,” in Proceedings of the ACM Web Conference 2024, 2024, pp. 1203–1214.

[26] Y. Xu, T. Wang, Q. Li, Q. Gong, Y. Chen, and Y. Jiang, “A multitab website fingerprinting attack,” in Proceedings of the 34th Annual Computer Security Applications Conference, 2018, pp. 327–341.

[27] Q. Yin, Z. Liu, Q. Li, T. Wang, Q. Wang, C. Shen, and Y. Xu, “An automated multi-tab website fingerprinting attack,” IEEE Transactions on Dependable and Secure Computing, vol. 19, no. 6, pp. 3656–3670, 2021.

[28] W. Cui, T. Chen, C. Fields, J. Chen, A. Sierra, and E. Chan-Tin, “Revisiting assumptions for website fingerprinting attacks,” in Proceedings of the 2019 ACM asia conference on computer and communications security, 2019, pp. 328–339.

[29] T. Wang and I. Goldberg, “On realistically attacking tor with website fingerprinting,” Proceedings on Privacy Enhancing Technologies, 2016.

[30] N. Mathews, J. K. Holland, N. Hopper, and M. Wright, “Laserbeak: Evolving website fingerprinting attacks with attention and multi-channel feature representation,” IEEE Transactions on Information Forensics and Security, 2024.

[31] V. Rimmer, D. Preuveneers, M. Juarez, T. Van Goethem, and W. Joosen, “Automated website fingerprinting through deep learning,” arXiv preprint arXiv:1708.06376, 2017.

[32] A. Mitseva and A. Panchenko, “Stop, don’t click here anymore: boosting website fingerprinting by considering sets of subpages,” in 33rd USENIX Security Symposium (USENIX Security 24), 2024, pp. 4139–4156.

[33] A. Shusterman, Z. Avraham, E. Croitoru, Y. Haskal, L. Kang, D. Levi, Y. Meltser, P. Mittal, Y. Oren, and Y. Yarom, “Website fingerprinting

through the cache occupancy channel and its real world practicality,” IEEE Transactions on Dependable and Secure Computing, vol. 18, no. 5, pp. 2042–2060, 2020.

[34] J. K. Holland, J. Carpenter, S. E. Oh, and N. Hopper, “Detorrent: an adversarial padding-only traffic analysis defense,” arXiv preprint arXiv:2302.02012, 2023.

[35] K. Abe and S. Goto, “Fingerprinting attack on tor anonymity using deep learning,” Proceedings of the Asia-Pacific Advanced Network, vol. 42, no. 0, pp. 15–20, 2016.

[36] S. Bhat, D. Lu, A. Kwon, and S. Devadas, “Var-cnn: A data-efficient website fingerprinting attack based on deep learning,” arXiv preprint arXiv:1802.10215, 2018.

[37] R. Chalapathy and S. Chawla, “Deep learning for anomaly detection: A survey,” arXiv preprint arXiv:1901.03407, 2019.

[38] Z. Zhang, P. Cui, and W. Zhu, “Deep learning on graphs: A survey,” IEEE Transactions on Knowledge and Data Engineering, vol. 34, no. 1, pp. 249–270, 2020.

[39] C. Tan, F. Sun, T. Kong, W. Zhang, C. Yang, and C. Liu, “A survey on deep transfer learning,” in Artificial Neural Networks and Machine Learning–ICANN 2018: 27th International Conference on Artificial Neural Networks, Rhodes, Greece, October 4-7, 2018, Proceedings, Part III 27. Springer, 2018, pp. 270–279.

[40] F. Zhuang, Z. Qi, K. Duan, D. Xi, Y. Zhu, H. Zhu, H. Xiong, and Q. He, “A comprehensive survey on transfer learning,” Proceedings of the IEEE, vol. 109, no. 1, pp. 43–76, 2020.

[41] P. Sirinam, N. Mathews, M. S. Rahman, and M. Wright, “Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning,” in Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, 2019, pp. 1131–1148.

[42] C. Wang, J. Dani, X. Li, X. Jia, and B. Wang, “Adaptive fingerprinting: Website fingerprinting over few encrypted traffic,” in Proceedings of the Eleventh ACM Conference on Data and Application Security and Privacy, 2021, pp. 149–160.

[43] M. Juarez, S. Afroz, G. Acar, C. Diaz, and R. Greenstadt, “A critical evaluation of website fingerprinting attacks,” in Proceedings of the 2014 ACM SIGSAC conference on computer and communications security, 2014, pp. 263–274.

[44] X. Gu, M. Yang, B. Song, W. Lan, and Z. Ling, “A practical multitab website fingerprinting attack,” Journal of Information Security and Applications, vol. 79, p. 103627, 2023.

[45] T. Wang and I. Goldberg, “{Walkie-Talkie}: An efficient defense against passive website fingerprinting attacks,” in 26th USENIX Security Symposium (USENIX Security 17), 2017, pp. 1375–1390.

[46] J. Gong and T. Wang, “Zero-delay lightweight defenses against website fingerprinting,” in 29th USENIX security symposium (USENIX security 20), 2020, pp. 717–734.

[47] M. S. Rahman, M. Imani, N. Mathews, and M. Wright, “Mockingbird: Defending against deep-learning-based website fingerprinting attacks with adversarial traces,” IEEE Transactions on Information Forensics and Security, vol. 16, pp. 1594–1609, 2020.

[48] J. Gong, W. Zhang, C. Zhang, and T. Wang, “Surakav: Generating realistic traces for a strong website fingerprinting defense,” in 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022, pp. 1558–1573.

[49] J. K. Holland and N. Hopper, “Regulator: A straightforward website fingerprinting defense,” Proceedings on Privacy Enhancing Technologies, 2022.

[50] X. Luo, H. Wu, J. Zhang, L. Gao, J. Xu, and J. Song, “A closer look at few-shot classification again,” in International Conference on Machine Learning. PMLR, 2023, pp. 23 103–23 123.

[51] J. Liu, W.-C. Chang, Y. Wu, and Y. Yang, “Deep learning for extreme multi-label text classification,” in Proceedings of the 40th international ACM SIGIR conference on research and development in information retrieval, 2017, pp. 115–124.

[52] X. Deng, R. Zhao, Y. Wang, M. Zhan, Z. Xue, and Y. Wang, “Countmamba: A generalized website fingerprinting attack via coarse-grained representation and fine-grained prediction,” in 2025 IEEE Symposium on Security and Privacy (SP). IEEE, 2025, pp. 1419–1437.

[53] W. De la Cadena, A. Mitseva, J. Hiller, J. Pennekamp, S. Reuter, J. Filter, T. Engel, K. Wehrle, and A. Panchenko, “Trafficsliver: Fighting website fingerprinting attacks with traffic splitting,” in Proceedings of the 2020 ACM SIGSAC Conference on Computer and Communications Security, 2020, pp. 1971–1985.

[54] G. Cherubin, R. Jansen, and C. Troncoso, “Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world,” in 31st USENIX Security Symposium (USENIX Security 22), 2022, pp. 753–770.

[55] X. Zhao, X. Deng, Q. Li, Y. Liu, Z. Liu, K. Sun, and K. Xu, “Towards fine-grained webpage fingerprinting at scale,” in Proceedings of the

2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 423–436.

![](images/2b32d05e2f09d63626009d97a0c0a4a0a968b7e8536bf6e22c93e00cf87e0230.jpg)  
Yuwen Qian received the Ph.D. degree in automatic engineering from Nanjing University of Science and Technology, Nanjing, China, in 2011. From July 2002 to June 2011, he was a Lecturer with the Automation School, Nanjing University of Science and Technology, China, where he has been an Associate Professor with the School of Electronic and Optical Engineering since May 2019.

![](images/72fc15bc26092e841af04102d923b07f46c205709c283c4e9a4a8b0037f37966.jpg)  
Biwen Chen Biwen Chen received the PhD degree from the School of Computer, Wuhan University, in 2020. He is currently an associate professor of the School of Computer, Chongqing University, China. His main research interests include cryptography, information security and blockchain.

![](images/5b0bab36cca194014130af2909bd90de0f67b9355f162415dcfee2d9f61ae559.jpg)

Wenwen Meng received the B.S. degree in automation from Nanjing University Jinling College, Nanjing, China, in 2022. He is currently pursuing the Graduate degree with Nanjing University of Science and Technology, Nanjing, China. His research interests include privacy protection and machine learning.

![](images/09bd2921bf787c155b248a9605257a8700b8b33f9b26a0af4e0905f4a2fdfff4.jpg)

Tao Xing (Senior Member, IEEE) received the BEng, MS and PhD degrees in computer science from Chongqing University, China, in 2003, 2005, and 2008, respectively. He is currently a professor with the College of Computer Science, Chongqing University. His research interests include multimedia security, cloud security, data privacy and cryptography. He has published more than 150 papers on international journals and conferences. He also served as a referee for numerous international journals and conferences.

![](images/2737ba62cd95b3d4a36426b78f585f2e224543856102a3401358faee863ce557.jpg)

Chuan Ma (Senior Member, IEEE) received the B.S. degree from Beijing University of Posts and Telecommunications, Beijing, China, in 2013, and the Ph.D. degree from the University of Sydney, Australia, in 2018. From 2018 to 2022, he was a Lecturer with Nanjing University of Science and Technology. He is currently an Associate Professor with the School of Computer Science, Chongqing University. He has published more than 40 journals and conference papers, including a Best Paper in WCNC 2018 and a Best Paper Award in IEEE Signal

Processing Society in 2022. His research interests include stochastic geometry, wireless caching networks, and distributed machine learning, and now focuses on the big data analysis and privacy-preserving.

![](images/3ac6f9ad4c0244153e31a9e5520fc08b580e73c09fadad195e1df7f612d0902a.jpg)

Ming Ding (Senior Member, IEEE) received the B.S. (Hons.) and M.S. degrees in electronics engineering and the Doctor of Philosophy (Ph.D.) degree from Shanghai Jiao Tong University (SJTU), China, in 2004, 2007, and 2011, respectively. From April 2007 to September 2014, he was with the Sharp Laboratories of China as a Researcher/Senior Researcher/Principal Researcher. Currently, he is a Principal Research Scientist and the Science Lead of Data61, CSIRO, Sydney, NSW, Australia. Also, he is an Adjunct Professor with the Swinburne University of Technology, Australia. His research interests include data privacy and security, machine learning and AI, and information technology. He has coauthored more than 250 papers in IEEE/ACM journals and conferences, all in recognized venues and around 20 3GPP standardization contribution; and two books, i.e., Multi-Point Cooperative Communication Systems: Theory and Applications (Springer, 2013) and Fundamentals of Ultra-Dense Wireless Networks (Cambridge University Press, 2022). Also, he holds 21 U.S. patents and has co-invented another more than 100 patents on 4G/5G technologies. Currently, he is an Editor of IEEE COMMUNICATIONS SURVEYS AND TUTORIALS. Besides, he has served as a guest editor/co-chair/co-tutor/TPC member for multiple IEEE top-tier journals/conferences and received several awards for his research work and professional services, including the prestigious IEEE Signal Processing Society Best Paper Award in 2022.
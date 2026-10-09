# LotBoNC: Novel Botnet Trafic Classification under Long-tailed Distributions

Huancheng Hu Hasso Plattner Institute & University of Potsdam Potsdam, Germany huancheng.hu@hpi.de

Ziyun Li KTH Royal Institute of Technology Stockholm, Sweden ziyli@kth.se

Christian Doerr Hasso Plattner Institute & University of Potsdam Potsdam, Germany christian.doerr@hpi.de

## Ab<sub>s</sub>t<sub>rac</sub>t

Botnets are a persistent cyber threat, leveraging global infrastruc tures to launch large-scale attacks. Yet, most existing classification methods are evaluated under balanced and closed-set assumptions, which fail to capture real-world conditions. In practice, botnet trafic is both long-tailed and open-world: unknown variants continually emerge, and rare threats are buried under dominant trafic, often evading detection. To reflect real-world conditions, we define a deployment-oriented setting where unlabeled trafic follows a long tailed distribution, with dominant known classes in the head and rare novel botnet variants in the tail. We propose LotBoNC, a uni fied framework for encrypted trafic classification under long-tailed open-world conditions. LotBoNC first performs self-supervised pre training to learn transferable representations, then applies entropy regularized optimal transport to assign pseudo-labels aligned with estimated class priors. An EM-style loop iteratively refines proto types and priors, improving class separation between frequent and rare categories. We evaluate LotBoNC on three public encrypted trafic datasets with diverse long-tailed scenarios. LotBoNC consistently outperforms prior state-of-the-art methods and accurately classifies known botnets and discovers unseen botnet variants in diverse, imbalanced open-world scenarios.

## Ke<sub>y</sub>words

Network Security, Machine Learning, Out-of-Distribution, Intrusion Detection

## ACM Reference Format:

Huancheng Hu, Ziyun Li, and Christian Doerr. 2026. LotBoNC: Novel Botnet Trafic Classification under Long-tailed Distributions. In ACM Asia Conference on Computer and Communications Security (ASIA CCS ’26), June 1–5, 2026, Bangalore, India. ACM, New York, NY, USA, 15 pages. https: //doi.org/10.1145/3779208.3785276

## 1 I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>

Botnets are pervasive and adaptive cyber threats, enabling largescale attacks such as DDoS [44], credential stufing, spam propa gation, and malware distribution [17, 29]. These attacks are driven by globally distributed infrastructures of compromised devices, ranging from enterprise systems to consumer IoT that generate

![](images/4578262440c8771838833af73fd9cacf6ff2d7f6db69c0058b18f4fc4370a455.jpg)

This work is licensed under a Creative Commons Attribution-NonCommercial NoDerivatives 4.0 International License. ASIA CCS ’26, Bangalore, India © 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2356-8/26/06 https://doi.org/10.1145/3779208.3785276

![](images/4b9988f189b38928b6cbfd902d06d206f68aa736ac98208982a7fe3cf1052eba.jpg)  
Fi<sub>gure</sub> 1<sub>:</sub> Ill<sub>us</sub>t<sub>ra</sub>ti<sub>on o</sub>f l<sub>ong-</sub>t<sub>a</sub>il<sub>e</sub>d b<sub>o</sub>t<sub>ne</sub>t t<sub>ra</sub>fi<sub>c</sub> i<sub>n</sub> th<sub>e open-</sub> world setting. A few known botnet families (e.g., Mirai, Mozi and Gafgyt) have abundant labeled samples, while many emer<sub>g</sub>in<sub>g</sub> unknown botnets a<sub>pp</sub>ear s<sub>p</sub>arsel<sub>y</sub> and without l<sub>a</sub>b<sub>e</sub>l<sub>s.</sub> Th<sub>e</sub> di<sub>s</sub>t<sub>r</sub>ib<sub>u</sub>ti<sub>on</sub> i<sub>s</sub> hi<sub>g</sub>hl<sub>y</sub> i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub>d<sub>, an</sub>d th<sub>e goa</sub>l i<sub>s</sub> t<sub>o</sub> <sub>accura</sub>t<sub>e</sub>l<sub>y</sub> di<sub>scover</sub> th<sub>ese</sub> <sub>un</sub>k<sub>nown</sub> l<sub>ow-</sub>f<sub>requency</sub> <sub>c</sub>l<sub>asses</sub> <sub>w</sub>ithi<sub>n un</sub>l<sub>a</sub>b<sub>e</sub>l<sub>e</sub>d t<sub>ra</sub>fi<sub>c.</sub>

persistent, high-volume trafic [28, 67]. To evade detection, botnets rapidly evolve into polymorphic variants and adopt encrypted communications [19, 20, 56], rendering signature-based methods and deep packet inspection increasingly inefective [1, 37]. As a result, accurate trafic classification has become a critical requirement for modern cyber defense and threat intelligence [41, 47, 65].

In real-world deployments, botnet trafic exhibits two compounding characteristics: a continuous emergence ofunseen botnet variants and a highly imbalanced distribution ofclass frequencies. Network streams often contain a mix of benign flows, known botnets, and rare unknown/novel families [3], forming an open-world setting with long-tailed distribution [19, 20]. In this structure, as shown in Figure 1, a few dominant botnet classes (e.g., Mirai, Mozi, Gafgyt) account for most labeled trafic, while rare and emerging threats appear sparsely and without annotation information, often buried deep in the tail. This imbalance introduces two coupled challenges: (i) unknown classes are dificult to detect without supervision, and (ii) long-tailed distributions bias models toward head classes, causing rare unknown botnets to be misclassified as known malware or even benign trafic. These realistic settings mirror operational environments, where rare threats are overwhelmed by dominant trafic and frequently go undetected.

Recent research on encrypted trafic classification has explored diferent paradigms [37, 61, 72, 74]. However, these methods assume that all classes are known in advance and labels are suficiently represented during training, evaluating models in closed-world or balanced-class settings. Although these assumptions simplify evaluation, they fail to capture the realistic nature of real-world deployments, where new botnet families emerge infrequently and annotation supervision is sparse or missing. Some recent works explore novel class discovery on rare trafic [64], but fail to consider class imbalance, which is critical for modeling realistic network con ditions. Consequently, the ability of existing methods to generalize under realistic, long-tailed distribution remains limited.

To address the gap, we propose LotBoNC, short for Long-tail Botnet Novel Classification, a unified framework for encrypted trafic classification that jointly tackles the challenges of novel class discovery and severe class imbalance. LotBoNC is designed for scenarios with both labeled and unlabeled trafic, where labeled samples come from known classes and unlabeled data may con tain novel botnet variants. LotBoNC begins with self-supervised pre-training to learn transferable representations from raw trafic sequences. It then performs pseudo-label assignment using entropy regularized optimal transport [11, 48], aligning predictions with estimated class priors. A central component of LotBoNC is an EM style iterative refinement loop. In each round, pseudo-labels for unlabeled data are assigned via optimal transport, aligned with esti mated class priors. These assignments are then used to update class prototypes and priors, progressively improving class separation, especially between dominant and rare classes in open-world and long-tailed distribution. Source code: https://github.com/watsonhu hpi/LotBoNC

Our main contributions are summarized as follows:

• We introduce a realistic setting for encrypted trafic analy sis, where unlabeled data exhibits a long-tailed distribution and unknown botnet classes are rare, making the setting inherently imbalanced and challenging.

• We propose LotBoNC, a unified framework that simultaneously classifies known botnet trafic and discovers unknown classes in long-tailed distribution. It combines self supervised pre-training, optimal transport pseudo-labeling, and iterative refinement to enable rare-class discovery in open-world, long-tailed trafic.

• We demonstrate that LotBoNC consistently outperforms existing methods across three public botnet trafic datasets, achieving state-of-the-art results in both labelled and un labelled data classes, up to 19.4% in ISCX-2014, 17.2% in CTU-13 and 14.7% in IoT-23.

## 2 B<sub>ac</sub>k<sub>groun</sub>d

This section introduces the key foundations necessary to understand our problem setting and technical approach. We first describe the characteristics and challenges of botnet trafic classification. Next, we present the novel category discovery (NCD) framework, which enables simultaneous classification of known threats and discovery of unknown attack types in unlabeled data. Finally, we explain the long-tailed learning setting, which reflects the severe imbalance between common and rare classes in real-world network trafic.

## 2<sub>.</sub>1 B<sub>o</sub>tn<sub>e</sub>t Tr<sub>a</sub>fi<sub>c</sub> Cl<sub>ass</sub>ifi<sub>ca</sub>ti<sub>o</sub>n <sub>a</sub>nd D<sub>e</sub>t<sub>ec</sub>ti<sub>o</sub>n

Botnets remain one of the most persistent and damaging threats to modern networks, enabling adversaries to conduct distributed denial-of-service (DDoS) attacks, deliver malware at scale, and exfiltrate sensitive information. Their infrastructure spans a wide range of compromised devices, from enterprise servers to consumer IoT endpoints, making them highly distributed and dificult to disrupt [58]. As botnets adopt more evasive and adaptive strategies, detecting their presence in real-world network trafic has become increasingly complex.

Traditional detection techniques based on rule matching or deep packet inspection are no longer suficient. The widespread use of trafic encryption, combined with protocol mimicry and fastflux domains, has made payload-level inspection largely inefective. In response, recent eforts have focused on analyzing flow-level metadata, such as timing patterns, connection frequencies, and statistical features of encrypted streams. While this shift enables detection under encryption, it introduces new challenges: botnet command-and-control (C2) trafic often mimics benign services in volume, timing, and protocol usage [14].

To overcome limitations of rule-based detection, early methods in trafic classification used handcrafted statistical features with traditional classifiers such as support vector machines, decision trees, or naïve Bayes, often underperforming in noisy or encrypted environments [46]. Deep learning marked a substantial advancement: recurrent neural networks (RNNs) demonstrated superior performance in detecting botnet trafic in smart-home environments by learning hierarchical representations [49]. Hybrid CNN–LSTM models further improved detection by extracting spatial then temporal patterns from encrypted trafic flows [2]. More recently, transformer-based architectures have demonstrated better performance. [43] applies the transformer mechanism to flow-level features for intrusion detection, capturing long-term dependencies across trafic sessions. Similarly, Vision Transformers (ViT) have been adapted for IoT botnet detection, converting flow data into image-like inputs for classification tasks [66]. Additionally, ensemble deep learning frameworks combining CNN and GRU layers have enhanced detection performance in IoT botnet scenarios, especially when optimized with advanced algorithms like [50]. These approaches collectively demonstrate the increasing sophistication of machine learning in handling encrypted, adaptive, and low-visibility botnet behaviors.

## 2.2 Novel Cate<sub>g</sub>or<sub>y</sub> Discover<sub>y</sub>

In conventional closed-set classification, models assume that all test instances belong to a fixed set of known classes. However, this assumption fails in dynamic environments such as cybersecurity, where unknown botnet variants continuously appear and pose immediate threats. Novel Category Discovery (NCD) provides a principled solution to this challenge by considering a joint labeled-unlabeled learning setup, where the goal is to both classify known classes and discover unknown categories within the unlabeled data [34, 35]. Unlike unsupervised clustering, NCD leverages supervision from known classes to structure the embedding space. By aligning labeled and unlabeled examples in feature space, models can both preserve separation of known classes and induce semantic grouping among unknowns. The success of NCD methods often depends on the quality of representations and the ability to propagate structural constraints into the unlabeled region. $\mathrm { A p \cdot }$ proaches such as OpenMatch [51] and DTC have demonstrated strong performance in image domains, and prototype refinement, cluster consistency, pseudo-label sharpening which are directly applicable to network trafic analysis. In botnet classification, NCD allows simultaneous adaptation to known threat signatures and structural discovery of novel attack behaviors, even in the presence of noise and imbalance.

## 2.3 Lon<sub>g</sub>-Tailed Learnin<sub>g</sub>

Long-tailed label distributions frequently appear in network traf fic domains, implying that a small number of categories dominate trafic while many remain rare [13, 71]. Under such skewed distri butions, supervised models often overfit to head classes and fail to generalize to the tail. Addressing this requires algorithms that preserve decision boundaries for underrepresented classes without sacrificing overall performance. Popular approaches include class balanced loss functions, margin-based calibration, and decoupled optimization of feature extractors and classifiers [10, 24, 73].

Long-tailed learning becomes significant in open-world scena rios, where data may include samples from classes that are entirely absent during training. In the context of trafic classification, these unknowns often correspond to novel botnet families or previously unseen attack behaviors. This setting imposes a dual requirement: models must learn to represent and distinguish rare known classes under severe imbalance, while also maintaining the flexibility to reject or discover unfamiliar categories without explicit supervi sion. Recent approaches leverage calibrated decision boundaries, uncertainty-aware scoring, and dynamic sample reweighting to mitigate the dominance of head classes and increase sensitivity to novel inputs [32, 33]. Prototype-based methods further support this objective by representing each class with an explicit centroid in feature space, which reduces the reliance on frequency-correlated classifier norms and preserves structure for tail categories [52]. Building on these ideas, frameworks such as [38, 39] integrate long tail classification with open-set recognition and few-shot learning.

## 3 R<sub>e</sub>l<sub>a</sub>t<sub>e</sub>d W<sub>or</sub>k

Botnet detection has been extensively studied, with early eforts relying on signature matching [68], payload analysis [42], or behavioral heuristics. While efective against known threats, these sys tems fail to generalize to novel variants, especially as botnets evolve rapidly and increasingly use encrypted communication. Anomaly based systems attempt to detect unknown attacks by modeling statistical deviations from normal behavior [30], but typically focus on binary detection and sufer from high false positives and poor interpretability.

To address encrypted trafic, recent works propose using flow level statistical features as a basis for classification [40], enabling detection even when payloads are inaccessible. Supervised deep learning approaches [26, 59] have shown promise but assume all classes are known during training. This closed-world assumption is unrealistic in real deployments, where novel botnet variants are constantly emerging and most flows are unlabeled.

Open-world and unknown class detection has been studied in both security and learning communities. Security-oriented methods simulate unknown threat detection by excluding botnets during training, but often treat the task as one-class or binary detection, which fails to characterize multiple emerging threats. Recent work has explored clustering-based approaches to discover unknown attack types [21], but typically rely on ofline heuristics and are not optimized for class imbalance.

Learning under class imbalance has been recognized as a key challenge in security datasets [60], where known botnets dominate and rare classes are underrepresented. Existing methods mitigate imbalance using re-weighting [10], synthetic oversampling [7], or cost-sensitive loss [55], but these assume full label availability. Semisupervised and pseudo-labeling approaches [69] attempt to infer class structure under limited supervision, but are fragile under noisy predictions and often amplify bias toward majority classes.

Despite these advances, no prior work provides a principled framework for multiclass discovery of novel botnet trafic under encrypted, unlabeled, and long-tailed conditions. Existing approaches either ignore class granularity, assume balanced label priors, or lack mechanisms to prevent pseudo-label collapse. Our work addresses this gap by introducing a novel trafic classification framework that estimates class priors from noisy predictions and regularizes pseudolabel assignments using constrained optimal transport. This design enables robust discovery of minority botnet classes and brings practical open-world capability to encrypted trafic analysis.

## 4 LotBoNC Model

This section introduces our EM-based training framework for longtailed novel botnet classification. The E-step assigns pseudo-labels to unlabeled trafic via entropy-regularized optimal transport, aligning them with estimated class priors to mitigate distributional bias. The M-step then updates class prototypes and priors through prototypebased optimization. Finally, we integrate both unsupervised and supervised objectives to promote semantic alignment across classes and preserve instance-level discriminability.

## 4.1 Problem Setu<sub>p</sub>

We denote $( \mathbf { X } _ { \mathrm { I } } , Y _ { l } )$ and $\left( \mathbf { X } u , Y _ { u } \right)$ as samples from labeled and unlabeled probability measures $\mathbb { P } _ { \mathbf { X } , Y }$ and $\mathbb { Q } _ { \mathbf { X } , Y }$ , respectively. Here, $\mathbf { X } _ { l } \ \in \ X _ { l }$ and $\mathbf { X } _ { u } \ \in \ \mathcal { X } _ { u }$ are feature vectors in $\mathbb { R } ^ { d } .$ , and $Y _ { l } \ \in \ y _ { l } .$ $Y _ { u } \in \mathcal { Y } _ { u }$ are class labels, with $y _ { u } = y _ { l } \cup y _ { n }$ where $y _ { l }$ are known classes and $y _ { n } = y _ { u } \ \backslash y _ { l }$ are novel classes. The goal of LotBoNC is to predict labels $Y _ { u }$ for instances $\mathbf { X } _ { u }$ in an unlabeled dataset ${ { \mathcal { U } } _ { m } }$ from $\mathbb { Q } _ { \mathbf { X } _ { u } , Y _ { u } }$ , by leveraging information from a balanced labeled dataset L� from $\mathbb { P } _ { \mathbf { X } _ { l } , Y _ { l } }$ . The unlabeled distribution $\mathbb { Q } _ { Y _ { u } }$ is imbalanced, with known classes in $y _ { l }$ more frequent than novel ones in $y _ { n } \left( \mathrm { i . e . , } \mathbb { Q } _ { Y _ { u } } ( i ) > \mathbb { Q } _ { Y _ { u } } ( j ) \right)$ ) for $i \in \mathcal { Y } _ { l } , j \in \mathcal { Y } _ { n } )$ , reflecting real-world scenarios where known trafic dominates and unknown threats are rare.

## 4.2 Data Pre<sub>p</sub>rocessing

Tokenization. To prepare raw encrypted trafic for representation learning, we adopt a burst-level tokenization strategy, following the design principles established in [12, 37, 74]. This approach captures meaningful mid-level structure within encrypted sessions and has been shown efective for modeling trafic semantics. Each session is first segmented into bursts, which are defined as sequences of temporally contiguous packets traveling in a single direction within the same TCP or UDP flow. This directional grouping approximates application-layer boundaries and provides more structured input than raw packet sequences. Given a flow $F = \left\{ p 1 , p 2 , \dots , p _ { n } \right\}$ , we decompose it into bursts $B = \{ b _ { 1 } , b _ { 2 } , . . . , b _ { k } \}$ , where each $b _ { i }$ is a maximal unidirectional subsequence. Within each burst, we re move low-level protocol headers and concatenate the remaining payloads to form a clean byte stream. This stream is then tok enized into a sequence of fixed-size 2-byte bigrams. To support self-supervised training, we append special tokens including [CLS], [SEP], [MASK], and [PAD] as needed, mirroring standard practices in masked language modeling and contrastive pretraining. The resulting tokenized burst is represented as $X ~ = ~ [ x _ { 1 } , x _ { 2 } , \dots , x _ { T } ]$ where each $x _ { i }$ is a 2-byte token. The input embedding for each position combines token, positional, and segment encodings. This encoding structure enables our model to leverage both spatial and contextual information within burst-level trafic segments.

![](images/24ac077929539669e37b135608cd26f36a2a5a86cd51f1dfcf25f717cfb452c1.jpg)  
Fi<sub>g</sub>ure 2: Overview of masked token <sub>p</sub>re-trainin<sub>g</sub> recon-<sub>s</sub>t<sub>ruc</sub>t<sub>s</sub> <sub>mas</sub>k<sub>e</sub>d t<sub>o</sub>k<sub>ens</sub> f<sub>rom</sub> <sub>encryp</sub>t<sub>e</sub>d t<sub>ra</sub>fi<sub>c</sub> <sub>sequences.</sub>

Data Augmentation. We employ a principled and minimal aug mentation strategy inspired by [15], introducing stochastic variability exclusively through dropout applied within the encoder. This design choice is critical in network trafic domains, where input level perturbations can distort flow structure, particularly for tail class samples that are both rare and structurally fragile. Concretely, given a tokenized burst-level flow �, we perform two stochastic forward passes using independently sampled dropout masks, yielding feature representations $\mathbf { h } _ { 1 } = f _ { \boldsymbol { \theta } _ { 1 } } ( \boldsymbol { X } )$ and $\mathbf { h } _ { 2 } = f _ { \boldsymbol { \theta } _ { 2 } } ( \boldsymbol { X } )$ , where $f _ { \theta }$ denotes the shared encoder with dropout. These views are treated as positive pairs in our contrastive objective. By introducing latent variability through encoder-level stochasticity, this approach pre serves the semantic integrity of input flows while promoting robust representation learning under long-tailed and open-world settings. Importantly, it eliminates the need for heuristic, domain-specific augmentations that may compromise tail-class fidelity.

## 4<sub>.</sub>3 M<sub>as</sub>k<sub>e</sub>d <sub>a</sub>nd C<sub>o</sub>ntr<sub>as</sub>ti<sub>ve</sub> Pr<sub>e</sub>-tr<sub>a</sub>inin<sub>g</sub>

Our framework incorporates two self-supervised objectives, masked modeling and contrastive learning.

4.3.1 Masked Token Pre-training. We use a masked token prediction task [12, 37] to train context-aware representations for encrypted trafic shown in Figure 2. Given a tokenized burst-level input sequence $\boldsymbol { x } = [ x _ { 1 } , x _ { 2 } , \dots , x _ { T } ]$ , we randomly select a subset of positions $M \subset \{ 1 , . . . , T \}$ and replace the corresponding tokens with a special [MASK] symbol, yielding a corrupted sequence �˜. The model is then trained to recover the original tokens at the masked positions by minimizing the following cross-entropy loss:

$$
\mathcal {L} _ {\mathrm{mask}} = - \sum_ {i \in \mathcal {M}} \log p _ {\theta} (x _ {i} \mid \tilde {x}),\tag{1}
$$

where $\phi \theta$ denotes the predicted token distribution. This objective encourages the model to capture contextual dependencies within trafic flows, which is critical for handling encrypted and protocolobfuscated data.

To enhance generalization and robustness, we pre-train this objective on a diverse collection of trafic datasets covering a wide range of encryption protocols, application types, and network behaviors. We include CTU-MALWARE-CAPTURE [53], VNAT [23], ISCX-VPN-2016 [18], and Ton-IoT [45]. Dataset details are given in Section 5.1 and Table 1. This multi-source pre-training equips the model with contextually robust representations.

![](images/84055a7401434fdf1f67dc286252a3f3d57578f8c960abc2a2256eb1f50dacf1.jpg)  
Fi<sub>g</sub>ure 3: Overview of contrastive learnin<sub>g</sub> levera<sub>g</sub>es unlab<sub>e</sub>l<sub>e</sub>d i<sub>ns</sub>t<sub>ances</sub> <sub>an</sub>d <sub>augmen</sub>t<sub>e</sub>d <sub>v</sub>i<sub>ews</sub> t<sub>o</sub> l<sub>earn</sub> di<sub>scr</sub>i<sub>m</sub>i<sub>na</sub>ti<sub>ve</sub> instance-level re<sub>p</sub>resentations.

4.3.2 Contrastive Pre-training. To complement masked modeling, we incorporate a contrastive pre-training objective [15] aimed at learning semantically discriminative and instance-aware representations shown in Figure 3. For each tokenized burst-level input � and encoder $f _ { \theta } ,$ , we obtain two latent views $h = f _ { \theta _ { 1 } } ( x )$ and $h ^ { \prime } = f _ { \theta _ { 2 } } ( x )$ through stochastic forward passes. These views constitute a positive pair, while all other samples in the batch serve as implicit negatives. The model is trained using the standard InfoNCE loss [8, 57]:

$$
\mathcal {L} _ {\mathrm{contrast}} = - \sum_ {i = 1} ^ {B} \log \frac {\exp (\mathrm{sim} (h _ {i} , h _ {i} ^ {\prime}) / \tau)}{\sum_ {j = 1} ^ {B} \exp (\mathrm{sim} (h _ {i} , h _ {j} ^ {\prime}) / \tau)},\tag{2}
$$

where sim $\begin{array} { r } { ( u , v ) = u ^ { \top } \colon } \end{array}$ � denotes cosine similarity and � is a temperature hyperparameter. This objective encourages the model to align latent representations of structurally similar flows while preserving inter-instance separation.

![](images/339eb77fee5278319b426b563d7f270788dec9f4f2bba586692b37c3e707d2fc.jpg)  
Fi<sub>g</sub>ure 4: Overview of the EM-loo<sub>p</sub>. To<sub>p</sub>: E-ste<sub>p</sub> assi<sub>g</sub>ns <sub>pseu</sub>d<sub>o-</sub>l<sub>a</sub>b<sub>e</sub>l<sub>s</sub> t<sub>o</sub> <sub>un</sub>l<sub>a</sub>b<sub>e</sub>l<sub>e</sub>d t<sub>ra</sub>fi<sub>c</sub> <sub>v</sub>i<sub>a</sub> <sub>en</sub>t<sub>ropy-regu</sub>l<sub>ar</sub>i<sub>ze</sub>d <sub>op-</sub> timal trans<sub>p</sub>ort ali<sub>g</sub>ned to estimated class <sub>p</sub>riors. Bottom: M ste<sub>p</sub> refines <sub>p</sub>rotot<sub>yp</sub>es and class <sub>p</sub>riors usin<sub>g</sub> <sub>p</sub>seudo-labels <sub>an</sub>d i<sub>ns</sub>t<sub>ance em</sub>b<sub>e</sub>ddi<sub>ngs</sub> t<sub>o</sub> i<sub>mprove</sub> f<sub>ea</sub>t<sub>ure c</sub>l<sub>us</sub>t<sub>er</sub>i<sub>ng an</sub>d <sub>correc</sub>t f<sub>or</sub> <sub>c</sub>l<sub>ass</sub> i<sub>m</sub>b<sub>a</sub>l<sub>ance.</sub>

## 4.4 E-ste<sub>p</sub>: Pseudo-Label Assi<sub>g</sub>nment via O<sub>p</sub>timal Trans<sub>p</sub>ort

In long-tailed novel botnet classification, the distribution of unla beled trafic is inherently imbalanced, with dominant known classes and sparsely represented unknown threats. This imbalance can cause prediction collapse toward frequent classes during training. To address this, we employ entropy-regularized Optimal Transport (OT) [11, 48] for pseudo-label assignment, as illustrated in Figure 4. Specifically, OT aligns the model’s predictions with an estimated class prior, enforcing balanced label assignments even under severe skew. Given a batch of� unlabeled samples, let $\mathbf { P } \in \mathbb { R } ^ { m \times K }$ denote the model’s softmax outputs over � classes (including both known and unknown). We define a target class prior $\mathbf { r } \in \Delta ^ { K }$ and a uniform distribution over samples w $\in \Delta ^ { m }$ . The resulting pseudo-label as signment matrix $\mathbf { A } \in \bar { \mathbb { R } } ^ { m \times K }$ is computed by solving the following entropy-regularized OT problem:

$$
\min _ {\mathbf {A} \in \Pi (\mathbf {r}, \mathbf {w})} \left\langle \mathbf {A}, - \log \mathbf {P} \right\rangle - \eta H (\mathbf {A}),\tag{3}
$$

where $\Pi ( \mathbf { r } , \mathbf { w } ) = \left\{ \mathbf { A } \in \mathbb { R } _ { + } ^ { m \times K } \mid \mathbf { A } ^ { \top } \mathbf { 1 } _ { m } = \mathbf { r } , \mathbf { A } \mathbf { 1 } _ { K } = \mathbf { w } \right\}$ ensures marginal constraints, and $\begin{array} { r } { H ( \mathbf { A } ) = - \sum _ { i , j } \mathbf { A } _ { i j } } \end{array}$ log $\mathbf { A } _ { i j }$ promotes smooth pseudo-label distributions. This formulation ensures proportional allocation of pseudo-labels aligned to class priors, efectively ad dressing class imbalance.

To eficiently solve the entropy-regularized optimal transport problem in Eq. (3), we apply the Sinkhorn-Knopp algorithm [11]. Let $\mathbf { K } = \exp ( - \log \mathbf { P } / \eta )$ denote the element-wise exponentiated similarity matrix, where � is the regularization coeficient. The optimal transport matrix $\mathbf { A } \in \mathbb { R } ^ { m \times K }$ admits a factorized form:

$$
\mathbf {A} = \operatorname{diag} (\alpha) \mathbf {K} \operatorname{diag} (\beta),\tag{4}
$$

where � $\in \mathbb { R } ^ { K }$ and $\beta \in \mathbb { R } ^ { m }$ are scaling vectors updated iteratively to enforce the marginal constraints. The updates follow:

$$
\alpha \leftarrow \mathbf {r} \oslash (\mathbf {K} \beta), \quad \beta \leftarrow \mathbf {w} \oslash (\mathbf {K} ^ {\top} \alpha),\tag{5}
$$

where ⊘ denotes element-wise division. This procedure is repeated until convergence. The resulting transport A satisfies the desired row and column marginals, and each row of A yields a refined pseudo-label distribution used as soft supervision in iterative training.

## 4.5 M-ste<sub>p</sub>: Protot<sub>yp</sub>e Ali<sub>g</sub>nment and Prior Estimation

The M-step refines class priors and prototype representations using the pseudo-label matrix A from the E-step (Figure 4). We optimize a prototype-based classification loss and apply momentum updates to both priors and prototypes.

Prototype-based classification loss. Let � be the number of unlabeled samples and � the total number of classes (including both known and novel) in the unlabeled set. Each input $\mathbf { x } _ { i }$ is encoded into a normalized feature vector $\mathbf { v } _ { i } = f _ { \theta } ( \mathbf { x } _ { i } )$ via the encoder $f _ { \theta } .$ For each class �, we maintain a prototype vector $\mathbf { c } _ { k } \in \mathbb { R } ^ { d }$ representing the structure center of this class, and an estimated prior $r _ { k }$ reflecting its frequency in the unlabeled distribution.

Given the pseudo-label assignment matrix $\mathbf { A } \in \mathbb { R } ^ { m \times K }$ from the E-step, we define a prototype-based classification objective as:

$$
\mathcal {L} _ {\mathrm{proto}} = - \sum_ {i = 1} ^ {m} \sum_ {k = 1} ^ {K} \mathbf {A} _ {i k} \left[ \log \frac {\exp (\mathbf {v} _ {i} ^ {\top} \mathbf {c} _ {k})}{\sum_ {j = 1} ^ {K} \exp (\mathbf {v} _ {i} ^ {\top} \mathbf {c} _ {j})} - \log p _ {k} \right],\tag{6}
$$

This loss encourages the embedding v� to be close to the class prototype $\mathbf { c } _ { k }$ if sample � is confidently assigned to class � (i.e., large ${ \bf A } _ { i k } )$ The subtraction of log $\mathcal { P } k$ acts as a prior correction term, penalizing overconfidence on frequent classes and promoting balanced assignments. This loss follows directly from an EM-based objective with prototype likelihoods and class priors. A complete derivation is provided in Appendix A.1.

Class prior estimation. Following [9, 31], we estimate class priors using the model’s predicted labels over the unlabeled set. Given softmax predictions $\mathbf { P } \in \mathbb { R } ^ { m \times K }$ , we construct an empirical distribution z by counting the predicted class for each sample, and apply a momentum update:

$$
z _ {k} = \frac {1}{m} \sum_ {i = 1} ^ {m} \mathbb {I} \left[ k = \arg \max _ {j} \mathbf {P} _ {i j} \right],\tag{7}
$$

$$
r _ {k} \leftarrow \mu r _ {k} + (1 - \mu) z _ {k},\tag{8}
$$

where $\mu \in \left[ 0 , 1 \right]$ is the momentum coeficient, and � is initialized as a uniform distribution over classes. This moving average improves the stability of class prior estimates across training epochs, particularly in the early stages when predictions are noisy.

Prototype updates. We maintain a prototype vector ${ \bf c } _ { k }$ for each class � using a momentum-based strategy [31]. Specifically, for each class, we aggregate embeddings from samples most confidently assigned to class �:

$$
\mathbf {c} _ {k} \leftarrow \mu \mathbf {c} _ {k} + (1 - \mu) \cdot \frac {\sum_ {i = 1} ^ {m} \mathbb {I} [ \arg \max _ {j} \mathbf {A} _ {i j} = k ] \mathbf {v} _ {i}}{\sum_ {i = 1} ^ {m} \mathbb {I} [ \arg \max _ {j} \mathbf {A} _ {i j} = k ]}.\tag{9}
$$

This ensures that prototypes evolve smoothly over time, reflecting both current embeddings and previously learned structure. We update class priors and prototypes once per epoch using the same momentum coeficient $\mu .$

## 4.6 Re<sub>p</sub>resentation Im<sub>p</sub>rovement

To maintain instance-level discriminability, we employ contrastive learning on unlabeled data. The augmentation strategy is mentioned in Section 4.2. Let $( \mathbf { x } _ { i } , \mathbf { x } _ { i } ^ { \prime } )$ be two augmentations of the same input, with corresponding feature embeddings $( \mathbf { v } _ { i } , \mathbf { v } _ { i } ^ { \prime } )$ . The contrastive loss for instance � is defined as:

$$
\mathcal {L} _ {i n s} ^ {(i)} = - \log \frac {\exp (\mathbf {v} _ {i} \cdot \mathbf {v} _ {i} ^ {\prime} / \tau)}{\sum_ {m} \mathbb {1} _ {[ n \neq i ]} \exp (\mathbf {v} _ {i} \cdot \mathbf {v} _ {m} / \tau)},\tag{10}
$$

where $\mathbb { 1 } _ { [ n \neq i ] }$ is an indicator function evaluating to 1 if $n \neq i ,$ and � is a temperature value. The overall unsupervised contrastive loss is:

$$
\mathcal {L} _ {\mathrm{ins}} = \frac {1}{m} \sum_ {i = 1} ^ {m} \mathcal {L} _ {\mathrm{ins}} ^ {(i)}.\tag{11}
$$

This loss pulls together positive pairs (same instance under aug mentation) while pushing away all other instances within the batch as negatives.

In addition, we apply supervised contrastive loss [25] for the labeled data. Let $y _ { i }$ be the true label of sample $\mathbf { x } _ { i } ,$ , and define the positive set for anchor � as $N ( i ) = \{ q \neq i \mid y _ { q } = y _ { i } \}$ . The supervised contrastive loss is given by:

$$
\mathcal {L} _ {s u p} ^ {(i)} = - \frac {1}{| \mathcal {N} (i) |} \sum_ {q \in \mathcal {N} (i)} \log \frac {\exp (\mathbf {v} _ {i} \cdot \mathbf {v} _ {q} / \tau)}{\sum_ {n} \mathbb {1} _ {[ n \neq i ]} \exp (\mathbf {v} _ {i} \cdot \mathbf {v} _ {n} / \tau)},\tag{12}
$$

where $\tau > 0$ is a temperature parameter that sharpens the similarity distribution. The loss pulls embeddings of the same class closer while pushing others apart. The denominator sums over all other labeled samples in the batch, serving as negatives.

## 4.7 Overall Loss Objective

The final objective integrates instance-level and class-level cues from unlabeled trafic, alongside supervised signals from labeled data:

$$
\mathcal {L} _ {\text { overall }} = \underbrace {\mathcal {L} _ {\text { ins }} + \lambda_ {\text { proto }} \mathcal {L} _ {\text { proto }}} _ {\mathcal {L} _ {\text { unlabeled }}} + \underbrace {\lambda_ {\sup} \mathcal {L} _ {\sup}} _ {\mathcal {L} _ {\text { labeled }}}\tag{13}
$$

The overall objective combines unsupervised and supervised components. The unsupervised loss $\scriptstyle \mathcal { L } _ { \mathrm { u n l a b e l e d } }$ includes: (i) instancelevel contrastive loss $\mathcal { L } _ { \mathrm { i n s } }$ that promotes local discriminability via data augmentation and (ii) a prototype-based classification loss $\mathcal { L } _ { \mathrm { p r o t o } }$ that aligns embeddings to class prototypes with prior correction. The supervised term $\mathcal { L } _ { \mathrm { l a b e l e d } }$ applies a contrastive loss $\mathcal { L } _ { \mathrm { s u p } }$ over labeled data to enhance intra-class compactness. Hyperparameters $\lambda _ { \mathrm { p r o t o } }$ and $\lambda _ { \mathrm { s u p } }$ control the relative importance of each term.

## 5 Ex<sub>p</sub>eriment

Our goal is to evaluate model robustness under realistic deployment conditions, where only partial supervision is available and unseen botnet variants occur with extreme class imbalance. Specifically, we simulate a network monitoring scenario in which (i) a set of known botnet families has been previously labeled through sandbox analysis or historical incident response, while (ii) new or evolving families appear unlabeled and with skewed prevalence. To reflect this asymmetry, we construct two disjoint splits for each dataset.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 EM training for novel botnet traffic classification under long-tailed distributions.

1: Input: labeled set  $D_{l}$ , unlabeled set  $D_{u}$ , classifier  $f_{\theta}$ , uniform marginals r, w, and hyperparameters  $\lambda_{proto}$ ,  $\lambda_{sup}$ ,  $\mu$ ,  $\eta$ 

2: for each epoch do

3: // sample batch  $B \subset D_{u}$  of size  $n_{B}$ 

4: for each step do

5: // E-step: estimate pseudo-label matrix A

6:  $P \leftarrow \text{softmax}(f_{\theta}(B))$ 

7:  $K \leftarrow \exp(-\log P/\eta)$ 

8: // Sinkhorn's fixed-point iteration

9: for t = 1 to T do

10:  $\alpha \leftarrow w \oslash (K\beta)$ 

11:  $\beta \leftarrow r \oslash (K^{\top}\alpha)$ 

12: end for

13:  $A \leftarrow n_{B} \cdot \text{diag}(\alpha) \cdot K \cdot \text{diag}(\beta)$ 

14: // M-step: update model parameters

15:  $L_{proto} \leftarrow L_{proto}(A, \{c_{k}\}, Du)$  // training on  $D_{u}$ 

16: // training on  $D_{u}$ ,  $v_{i}$ ,  $v_{i}'$  are augmented views

17:  $L_{ins} \leftarrow L_{ins}(v_{i}, v_{i}')$ 

18:  $L_{sup} \leftarrow L_{sup}(D_{l})$  // training on  $D_{l}$ 

19:  $L_{overall} \leftarrow \lambda_{proto} L_{proto} + L_{ins} + \lambda_{sup} L_{sup}$ 

20:  $\theta \leftarrow \theta - \eta \nabla_{\theta} L_{overall}$  // update model parameters

21: end for

22: for each class k do

23:  $z_{k} \leftarrow Eq.(7)$  // calculate empirical distribution

24:  $r_{k} \leftarrow \mu r_{k} + (1 - \mu) z_{k}$  // class prior update

25:  $c_{k} \leftarrow Eq.(9)$  // prototype update

26: end for

27: end for
</div>

The labelled set contains trafic from known botnet families and is explicitly class-balanced to simulate curated training corpora. The unlabelled set includes trafic from previously unseen botnet families as well as unlabeled residuals from known ones. Importantly, we impose a long-tailed distribution only on the unlabelled portion, thereby isolating the efect of imbalance in novel class discovery while keeping the supervised baseline fixed. This design reflects operational practice, where security teams have no control over the prevalence or labeling of newly emerging ones. Our experiments vary the severity of imbalance in the unlabelled set while holding the class identities fixed, allowing us to assess whether a method maintains high accuracy on known classes while correctly discovering rare variants in the tail. The remainder of this section describes the datasets, construction of long-tailed splits, baseline methods, implementation details, and evaluation metrics.

## 5.1 Datasets

Pre-training Datasets. We utilize four datasets from varied trafic environment to ensure comprehensive coverage. CTU-MALWARE-CAPTURE [53] comprises a mixture of malware, normal, and background trafic, with long-term captures categorized by malware type. VNAT [23] contains both encrypted and unencrypted trafic across 10 applications and 5 categories, including streaming, VoIP, chat, and file transfer. ISCX-VPN-2016 [18] includes VPN trafic spanning 14 diferent trafic categories such as VoIP, VPN-VoIP, and P2P, and incorporates services like Skype and Facebook. Addition ally, Ton-IoT [45] encompasses trafic ranging from DDoS attacks to scanning activities and normal operations.

Table 1: Summar<sub>y</sub> of Datasets Used in Ex<sub>p</sub>eriments for Pretrainin<sub>g</sub> and E<sub>v</sub>aluation

<table><tr><td colspan="2">Pre-training</td><td colspan="2">Fine-tuning</td></tr><tr><td>Dataset</td><td># Flows $^{\dagger}$ </td><td>Dataset</td><td># Flows $^{\dagger}$ </td></tr><tr><td>CTU-MAL-CAP[53]</td><td> $3.25 \times 10^{8}$ </td><td>IoT-23[17]</td><td> $3.25 \times 10^{6}$ </td></tr><tr><td>VNAT[23]</td><td> $3.17 \times 10^{6}$ </td><td>ISCX-Bot-2014[4]</td><td> $3.17 \times 10^{5}$ </td></tr><tr><td>ISCX-VPN-2016[18]</td><td> $2.80 \times 10^{6}$ </td><td>CTU-13[16]</td><td> $2.80 \times 10^{6}$ </td></tr><tr><td>Ton-IoT[45]</td><td> $2.0 \times 10^{5}$ </td><td></td><td></td></tr></table>

<sup>†</sup> Flow counts are reported after preprocessing steps, including filtering by size and packet count, and capping per-class samples for balance.

Training Datasets. In training and evaluation stages, we chose three public datasets for reliable assessment of long-tailed recognition that combine realism, diversity, and public ground truth. IoT-23 [17] was published by the Stratosphere Aposemat project in 2020. It comprises twenty malware types and three benign reference traces recorded from consumer devices. The dataset contains more than 30 GB of trafic. ISCX-2014 [4] is from the Canadian Institute for Cybersecurity. This dataset records ten consecutive days of enterprise activity that include seven botnet families, with packet captures and 80 flow features per record, for a total of 50.0M flows. CTU-13 [16] dataset captures thirteen distinct botnet campaigns executed in a controlled university network in 2011. The extended release encloses both PCAP and CSV representations, yielding 147.3M packets that translate to 1.3M labelled flows. The dataset includes various malware families, ofering opportunities for cross domain generalisation. For each dataset, we reconstruct bidirectional flows, discard non-IP control trafic, and retain only TCP/UDP records with at least five packets. Table 1 summarizes the resulting statistics. We create two disjoint splits per dataset. We then form two disjoint splits per dataset. The labelled split consists only of known families and is class balanced by stratified sampling so that each labelled class contributes the same number of flows. The unlabeled dataset is the place where class imbalance is introduced and contains both known and unknown botnets following the long-tailed distribution. This design simulates the challenge in real-world scenario.

Long-Tailed Dataset Construction. To construct exponential long tailed dataset, we introduce a single parameter $\gamma = n _ { k } / n _ { u }$ , where $n _ { k }$ and $n _ { u }$ denote the number of unlabeled samples from known and unknown classes, respectively. We vary $\gamma \in \{ 1 , \ 5 ,$ 10} to simulate deployment scenarios with diferent levels of known-class dominance in the unlabeled trafic. Given $C _ { u }$ unknown classes, we allocate the number of samples for each class � as:

$$
n _ {i} = \max (n _ {\mathrm{min}}, \lfloor n _ {\mathrm{max}} \cdot \gamma^ {i - 1} \rfloor), i = 1, \ldots , C _ {u},
$$

where $n _ { \mathrm { m a x } }$ is the sample count of the head class and $n _ { \mathrm { { m i n } } }$ enforces a lower bound to avoid collapse in the tail. The resulting distribution is normalized to match the total $n _ { u }$ specified by $\gamma .$

## 5<sub>.</sub>2 B<sub>ase</sub>li<sub>nes</sub>

We compare against strong baselines used in encrypted trafic classification and recent open world recognition. All methods are trained and evaluated under the same setting: a balanced labelled split over known families and a long-tailed unlabeled split that introduces unknown botnets. Hyperparameters follow the original papers unless adaptation to mixed labelled unlabeled training is necessary. We chose the following baselines: 1DCNN [62]. An end to end CNN for encrypted trafic classification that learns directly from raw flow derived sequences. LSTM Att [70]. A temporal model with attention that focuses on informative segments of encrypted flows. TSCRNN [36]. A hybrid that uses CNNs for spatial features and Bi LSTMs for long range temporal patterns with burst level preprocessing. DeepTrafic [63]. A CNN that treats trafic as images and performs malware classification through representation learning from raw traces. ET BERT [37]. A Transformer pre trained on large unlabeled trafic via masked BURST modeling and same origin BURST prediction, with strong few shot transfer. NetMamba [61]. A linear time sequence architecture tailored for trafic analysis that reduces inference latency while preserving accuracy. RoNeTC [64]. An open set oriented model with multi view packet representations and uncertainty estimation for unknown detection.

## 5.3 Ex<sub>p</sub>erimental Setu<sub>p</sub> and H<sub>yp</sub>er<sub>p</sub>arameters

Pre-training Settings and Hyperparameters. During pre-training, each packet is limited to 64 bytes of data following the Ethernet layer to focus on meaningful payload information, excluding Ethernet addresses and encrypted payload content as they are irrelevant for classification tasks. The training process utilizes a batch size of 64. The Adam optimizer is employed with a learning rate of $1 \times 1 0 ^ { - 5 }$ to ensure stable and gradual learning. The model is trained for a total of 580,000 steps, with the loss function monitored to ensure convergence. A linear decay scheduling strategy with a warmup ratio of 0.1 is used to stabilize the initial training phases.

Fine-tuning Settings and Hyperparameters. We set the learning rate to $2 \times 1 0 ^ { - 5 }$ and the weight decay to $1 \times 1 0 ^ { - 4 }$ to balance optimization stability and prevent overfitting. The contrastive learning temperature was fixed at 0.5 to regulate the similarity distribution in the representation space, while a dropout rate of 0.1 was applied to reduce overfitting. The batch size was set to 32, optimizing the trade-of between computational eficiency and gradient estimation accuracy.

## 5<sub>.</sub>4 E<sub>va</sub>l<sub>ua</sub>ti<sub>on</sub> M<sub>e</sub>t<sub>r</sub>i<sub>cs</sub>

We follow the evaluation protocol of [5, 54] and compute four complementary metrics that together measure both recognition of known classes and discovery of novel ones. Let $\mathcal { D } _ { u }$ denote the unlabeled subset, $M = | \mathcal { D } _ { u } |$ , and $\mathcal { P } ( y _ { u } )$ the set of all permutations of the unknown class indices. Given ground-truth labels $y _ { i }$ and model predictions $\hat { y } _ { i } ,$ , clustering accuracy is:

$$
\mathrm{ACC} = \max _ {p \in \mathcal {P} (\mathcal {Y} _ {u})} \frac {1}{M} \sum_ {i = 1} ^ {M} \mathbb {1} \bigl \{y _ {i} = p \bigl (\hat {y} _ {i} \bigr) \bigr \},\tag{14}
$$

where the optimal one-to-one assignment $p ( \cdot )$ is obtained over all categories with the Hungarian algorithm[27].

Table 2: Performance across datasets when all classes are balanced (<sub>�</sub> = 1). Each entr<sub>y</sub> is mean ± std over multi<sub>p</sub>le runs.

<table><tr><td></td><td>Dataset</td><td>Metrics</td><td>1DCNN</td><td>LSTM-Att</td><td>TSCRNN</td><td>DeepTraffic</td><td>ET-BERT</td><td>NetMamba</td><td>RoNeTC</td><td>LotBoNC</td></tr><tr><td rowspan="12">γ = 1</td><td rowspan="4">IoT-23</td><td>Overall</td><td>48.52 ± 0.27</td><td>50.36 ± 0.48</td><td>49.45 ± 0.55</td><td>73.78 ± 0.24</td><td>75.93 ± 0.37</td><td>78.18 ± 0.31</td><td>91.34 ± 0.30</td><td>94.48 ± 0.41</td></tr><tr><td>Labelled</td><td>82.53 ± 0.24</td><td>83.24 ± 0.30</td><td>83.05 ± 0.40</td><td>86.08 ± 0.33</td><td>92.56 ± 0.40</td><td>98.76 ± 0.12</td><td>97.10 ± 0.20</td><td>98.51 ± 0.31</td></tr><tr><td>Unlabelled-Aware</td><td>25.69 ± 0.61</td><td>23.17 ± 0.35</td><td>22.35 ± 0.40</td><td>55.33 ± 0.13</td><td>59.99 ± 0.29</td><td>52.07 ± 0.62</td><td>86.50 ± 0.35</td><td>90.42 ± 0.46</td></tr><tr><td>Unlabelled-Agnostic</td><td>19.43 ± 0.76</td><td>20.38 ± 0.30</td><td>19.85 ± 0.50</td><td>50.21 ± 0.15</td><td>54.72 ± 0.26</td><td>40.05 ± 0.70</td><td>91.45 ± 0.32</td><td>88.20 ± 0.40</td></tr><tr><td rowspan="4">ISCX-2014</td><td>Overall</td><td>50.64 ± 0.20</td><td>49.83 ± 0.38</td><td>52.16 ± 0.10</td><td>63.77 ± 0.50</td><td>73.48 ± 0.26</td><td>65.31 ± 0.16</td><td>92.10 ± 0.28</td><td>92.56 ± 0.33</td></tr><tr><td>Labelled</td><td>84.96 ± 0.30</td><td>84.03 ± 0.27</td><td>87.50 ± 0.60</td><td>81.21 ± 0.28</td><td>97.49 ± 0.49</td><td>99.15 ± 0.72</td><td>99.35 ± 0.20</td><td>99.12 ± 0.43</td></tr><tr><td>Unlabelled-Aware</td><td>24.75 ± 0.57</td><td>22.16 ± 0.60</td><td>26.80 ± 0.50</td><td>37.62 ± 0.40</td><td>42.46 ± 0.36</td><td>39.85 ± 0.85</td><td>79.20 ± 0.30</td><td>86.73 ± 0.28</td></tr><tr><td>Unlabelled-Agnostic</td><td>18.98 ± 0.31</td><td>19.55 ± 0.44</td><td>20.90 ± 0.32</td><td>33.49 ± 0.42</td><td>37.25 ± 0.34</td><td>27.06 ± 0.12</td><td>64.85 ± 0.28</td><td>82.55 ± 0.30</td></tr><tr><td rowspan="4">CTU-13</td><td>Overall</td><td>52.24 ± 0.48</td><td>54.13 ± 0.30</td><td>56.95 ± 0.70</td><td>70.78 ± 0.34</td><td>76.38 ± 0.27</td><td>69.28 ± 0.18</td><td>88.02 ± 0.32</td><td>93.29 ± 0.34</td></tr><tr><td>Labelled</td><td>82.61 ± 0.36</td><td>84.58 ± 0.50</td><td>90.27 ± 0.65</td><td>82.95 ± 0.11</td><td>95.63 ± 0.18</td><td>97.89 ± 0.46</td><td>98.01 ± 0.22</td><td>97.90 ± 0.25</td></tr><tr><td>Unlabelled-Aware</td><td>25.84 ± 0.12</td><td>27.53 ± 0.18</td><td>31.45 ± 0.45</td><td>65.03 ± 0.48</td><td>67.52 ± 0.22</td><td>43.57 ± 0.82</td><td>80.05 ± 0.42</td><td>88.12 ± 0.50</td></tr><tr><td>Unlabelled-Agnostic</td><td>19.79 ± 0.44</td><td>21.14 ± 0.80</td><td>27.50 ± 0.17</td><td>60.12 ± 0.50</td><td>62.46 ± 0.24</td><td>31.13 ± 0.14</td><td>71.62 ± 0.38</td><td>80.05 ± 0.45</td></tr><tr><td rowspan="12">γ = 5</td><td rowspan="4">IoT-23</td><td>Overall</td><td>57.36 ± 0.30</td><td>61.97 ± 0.55</td><td>69.93 ± 0.67</td><td>78.48 ± 0.31</td><td>83.31 ± 0.29</td><td>87.27 ± 0.04</td><td>93.93 ± 0.50</td><td>95.56 ± 0.76</td></tr><tr><td>Labelled</td><td>91.76 ± 0.26</td><td>93.48 ± 0.32</td><td>99.43 ± 0.38</td><td>93.46 ± 0.40</td><td>97.90 ± 0.70</td><td>99.40 ± 0.13</td><td>99.70 ± 0.15</td><td>99.23 ± 0.08</td></tr><tr><td>Unlabelled-Aware</td><td>19.55 ± 0.67</td><td>19.32 ± 0.20</td><td>22.17 ± 0.11</td><td>28.48 ± 0.34</td><td>33.62 ± 0.08</td><td>39.37 ± 0.66</td><td>51.50 ± 0.65</td><td>75.73 ± 0.20</td></tr><tr><td>Unlabelled-Agnostic</td><td>18.36 ± 0.80</td><td>18.09 ± 0.29</td><td>17.88 ± 0.15</td><td>15.69 ± 0.68</td><td>24.33 ± 0.05</td><td>28.11 ± 0.75</td><td>38.40 ± 0.55</td><td>73.54 ± 0.60</td></tr><tr><td rowspan="4">ISCX-2014</td><td>Overall</td><td>57.91 ± 0.14</td><td>52.87 ± 0.46</td><td>62.55 ± 0.08</td><td>68.60 ± 0.03</td><td>76.26 ± 0.17</td><td>72.96 ± 0.18</td><td>93.21 ± 0.60</td><td>93.07 ± 0.02</td></tr><tr><td>Labelled</td><td>94.85 ± 0.34</td><td>92.67 ± 0.28</td><td>97.86 ± 0.61</td><td>98.53 ± 0.39</td><td>97.96 ± 0.35</td><td>99.50 ± 0.72</td><td>99.40 ± 0.22</td><td>98.57 ± 0.64</td></tr><tr><td>Unlabelled-Aware</td><td>18.03 ± 0.61</td><td>17.26 ± 0.60</td><td>19.42 ± 0.47</td><td>23.32 ± 0.15</td><td>27.68 ± 0.31</td><td>34.18 ± 0.83</td><td>45.50 ± 0.42</td><td>68.27 ± 0.79</td></tr><tr><td>Unlabelled-Agnostic</td><td>16.69 ± 0.29</td><td>15.85 ± 0.49</td><td>17.25 ± 0.30</td><td>18.64 ± 0.73</td><td>16.75 ± 0.06</td><td>21.53 ± 0.14</td><td>32.52 ± 0.84</td><td>67.79 ± 0.61</td></tr><tr><td rowspan="4">CTU-13</td><td>Overall</td><td>58.01 ± 0.53</td><td>60.74 ± 0.29</td><td>67.37 ± 0.71</td><td>74.69 ± 0.82</td><td>80.20 ± 0.58</td><td>75.27 ± 0.20</td><td>90.56 ± 0.34</td><td>90.55 ± 0.49</td></tr><tr><td>Labelled</td><td>91.79 ± 0.40</td><td>94.12 ± 0.55</td><td>99.29 ± 0.66</td><td>97.72 ± 0.25</td><td>98.01 ± 0.18</td><td>98.25 ± 0.46</td><td>99.00 ± 0.10</td><td>98.93 ± 0.38</td></tr><tr><td>Unlabelled-Aware</td><td>23.90 ± 0.14</td><td>21.58 ± 0.19</td><td>25.10 ± 0.40</td><td>21.57 ± 0.11</td><td>37.48 ± 0.04</td><td>42.43 ± 0.83</td><td>47.54 ± 0.24</td><td>72.86 ± 0.57</td></tr><tr><td>Unlabelled-Agnostic</td><td>19.24 ± 0.48</td><td>16.57 ± 0.81</td><td>21.62 ± 0.18</td><td>18.65 ± 0.09</td><td>20.82 ± 0.05</td><td>24.30 ± 0.16</td><td>34.50 ± 0.39</td><td>71.93 ± 0.55</td></tr><tr><td rowspan="12">γ = 10</td><td rowspan="4">IoT-23</td><td>Overall</td><td>59.34 ± 0.27</td><td>64.25 ± 0.52</td><td>71.07 ± 0.61</td><td>80.75 ± 0.28</td><td>86.43 ± 0.26</td><td>89.74 ± 0.03</td><td>94.66 ± 0.48</td><td>96.93 ± 0.19</td></tr><tr><td>Labelled</td><td>84.33 ± 0.24</td><td>85.92 ± 0.31</td><td>91.24 ± 0.36</td><td>86.56 ± 0.38</td><td>96.94 ± 0.73</td><td>99.34 ± 0.12</td><td>99.65 ± 0.16</td><td>99.93 ± 0.41</td></tr><tr><td>Unlabelled-Aware</td><td>29.06 ± 0.61</td><td>26.03 ± 0.18</td><td>31.07 ± 0.10</td><td>26.23 ± 0.31</td><td>28.42 ± 0.07</td><td>32.93 ± 0.62</td><td>45.30 ± 0.54</td><td>60.01 ± 0.78</td></tr><tr><td>Unlabelled-Agnostic</td><td>24.84 ± 0.76</td><td>21.56 ± 0.26</td><td>21.56 ± 0.14</td><td>24.04 ± 0.65</td><td>19.24 ± 0.05</td><td>26.14 ± 0.72</td><td>37.46 ± 0.57</td><td>56.05 ± 0.13</td></tr><tr><td rowspan="4">ISCX-2014</td><td>Overall</td><td>59.34 ± 0.13</td><td>54.74 ± 0.42</td><td>64.47 ± 0.07</td><td>71.16 ± 0.03</td><td>79.07 ± 0.15</td><td>75.46 ± 0.16</td><td>94.05 ± 0.55</td><td>93.23 ± 0.57</td></tr><tr><td>Labelled</td><td>87.06 ± 0.31</td><td>84.95 ± 0.25</td><td>89.84 ± 0.62</td><td>90.33 ± 0.37</td><td>93.86 ± 0.34</td><td>99.44 ± 0.72</td><td>99.24 ± 0.55</td><td>98.54 ± 0.71</td></tr><tr><td>Unlabelled-Aware</td><td>25.56 ± 0.59</td><td>27.06 ± 0.58</td><td>26.56 ± 0.43</td><td>24.86 ± 0.14</td><td>25.66 ± 0.30</td><td>29.27 ± 0.83</td><td>38.14 ± 0.40</td><td>57.55 ± 0.68</td></tr><tr><td>Unlabelled-Agnostic</td><td>20.74 ± 0.28</td><td>19.46 ± 0.46</td><td>23.55 ± 0.27</td><td>21.04 ± 0.70</td><td>22.14 ± 0.05</td><td>23.35 ± 0.13</td><td>31.27 ± 0.81</td><td>52.78 ± 0.33</td></tr><tr><td rowspan="4">CTU-13</td><td>Overall</td><td>61.33 ± 0.48</td><td>63.77 ± 0.26</td><td>70.34 ± 0.64</td><td>76.86 ± 0.77</td><td>81.57 ± 0.55</td><td>79.05 ± 0.18</td><td>91.66 ± 0.01</td><td>93.93 ± 0.70</td></tr><tr><td>Labelled</td><td>84.13 ± 0.36</td><td>87.04 ± 0.52</td><td>92.86 ± 0.64</td><td>90.37 ± 0.23</td><td>95.16 ± 0.16</td><td>98.66 ± 0.46</td><td>99.55 ± 0.09</td><td>99.44 ± 0.08</td></tr><tr><td>Unlabelled-Aware</td><td>26.04 ± 0.12</td><td>24.05 ± 0.16</td><td>23.10 ± 0.38</td><td>26.23 ± 0.10</td><td>28.16 ± 0.04</td><td>33.83 ± 0.82</td><td>42.91 ± 0.22</td><td>60.15 ± 0.59</td></tr><tr><td>Unlabelled-Agnostic</td><td>21.03 ± 0.44</td><td>21.07 ± 0.79</td><td>19.06 ± 0.15</td><td>24.57 ± 0.08</td><td>22.24 ± 0.04</td><td>29.67 ± 0.15</td><td>34.60 ± 0.37</td><td>56.07 ± 0.06</td></tr></table>

First, Overall accuracy reflects the classification performance across both labeled and unlabeled samples. Second, Labelled accuracy reports the standard classification accuracy restricted to labeled data from known categories. Third, Unlabelled-Aware accu racy evaluates clustering performance by assuming ideal separation of novel samples and then measuring cluster-to-class alignment. Finally,Unlabelled-Agnostic accuracy removes this assumption and evaluates clustering on the entire unlabeled data without any indi cator ofwhether a sample belongs to a known or unknown class. All results are averaged over five random seeds to mitigate variability caused by stochastic initialisation and data shufling.

surpassing the strongest baseline, which reaches 86.50. As the imbalance increases, LotBoNC maintains its robustness with unlabelledaware accuracies of 75.73 at $\gamma = 5$ and 60.01 at $\gamma = 1 0 ,$ while the top baseline declines to 51.50 and 45.30, respectively. In the unlabelled-agnostic setting, LotBoNC records accuracies of 88.20, 73.54, and 56.05 for � = 1, 5, and 10, respectively. The best baseline starts at 91.45 under balanced conditions but drops sharply to 38.40 and 37.46 as the imbalance grows. These results confirm that Lot-BoNC generalizes well to under-represented and unseen classes, maintaining high accuracy even under severe long-tail skew. While LotBoNC also achieves competitive overall accuracy—up to 96.93 at � = 10—and strong labelled accuracy of 99.93 at the same setting, its most critical contribution lies in retaining reliable unlabelled predictions under increasingly imbalanced and open-world trafic distributions.

## 5.5 Com<sub>p</sub>arison <sub>w</sub>ith SOTA

IoT-23. On the IoT-23 dataset, LotBoNC achieves significant im provements in discovering novel classes under long-tailed distributions. In the unlabelled-aware evaluation, LotBoNC attains an accuracy of 90.42 when the class distribution is balanced (� = 1),

ISCX-2014. On the ISCX-2014 dataset, LotBoNC demonstrates strong and consistent performance in discovering novel classes across varying imbalance levels. In the unlabelled-aware setting,

LotBoNC achieves an accuracy of 86.73 when the class distribution is balanced $( \gamma = 1 )$ , outperforming the strongest baseline at 79.20. As the imbalance increases, LotBoNC maintains its advantage, reaching 68.27 at $\gamma = 5$ and 57.55 at $\gamma = 1 0 ,$ , while the best baseline falls to 45.50 and 38.14, respectively. In the unlabelledagnostic metric, LotBoNC attains 82.55 at $\gamma = 1 , 6 7 . 7 9$ at $\gamma = 5 ,$ and 52.78 at $\gamma = 1 0$ . The top baseline in this setting reaches 64.85 under balanced conditions but drops significantly to 32.52 and 31.27 as the imbalance increases. These results confirm that LotBoNC con sistently outperforms existing methods in discovering unlabelled trafic classes.

CTU-13. The CTU-13 results further confirm LotBoNC’s efective ness in handling long-tailed distributions for novel class discovery. In the unlabelled-aware setting, LotBoNC achieves an accuracy of 88.12 under the balanced condition $( \gamma = 1 )$ , notably higher than the strongest baseline at 80.05. When the imbalance factor increases to $\gamma = 5$ and $\gamma = 1 0 ;$ , LotBoNC maintains unlabelled-aware accuracies of 72.86 and 60.15, respectively. In contrast, the best competing method drops to 47.54 and 42.91, showing a substantial degrada tion. For the unlabelled-agnostic metric, LotBoNC reaches 80.05 at $\gamma = 1$ , 71.93 at $\gamma = 5 ,$ and 56.07 at $\gamma = 1 0 ,$ , outperforming all baselines across the board. Other methods perform significantly worse, with the closest baseline at $7 1 . 6 2 $ for $\gamma = 1$ , falling to 34.50 at $\gamma = 5$ and $3 4 . 6 0$ at $\gamma = 1 0$ . These consistent improvements on unlabelled samples suggest that LotBoNC is particularly well suited to discovering unlabelled botnet classes in imbalanced scenarios.

Class Distribution Prediction. We evaluate the ability of each method to recover the true class distribution under varying levels of imbalance. We conduct experiments under three settings: $\gamma = 1 ,$ $\gamma = 5 ,$ , and $\gamma = 1 0 _ { ; }$ , where the ground-truth class prior follows an exponential decay with a head-to-tail ratio of $\gamma .$ When $\gamma = 1$ , the true distribution is uniform across all classes. In this case, LotBoNC produces predictions that are closely aligned with the target, while DeepTrafic deviates more noticeably. $_ { \mathrm { A } s }$ the imbalance increases to $\gamma = 5 ,$ DeepTrafic exhibits significant prediction errors, particularly in underestimating several classes. In contrast, LotBoNC remains substantially closer to the true distribution, with all class-level predictions within a reasonable range of the ground-truth values. When $\gamma = 1 0 _ { ; }$ , the task becomes more challenging due to the severe skew. DeepTrafic’s prediction quality continues to degrade under this setting. LotBoNC also experiences performance drop, but its output remains consistently more faithful to the expected class distribution than the baseline. Across all three imbalance levels, LotBoNC achieves more accurate and reliable recovery of the class prior. The prediction gap between the two methods widens as � increases, highlighting the advantage of LotBoNC in handling extreme long-tail distributions.

## 5<sub>.</sub>6 I<sub>mpac</sub>t <sub>o</sub>f L<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d<sub>-</sub>t<sub>o-</sub>U<sub>n</sub>l<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d Cl<sub>ass</sub> Ratio $\rho$

This experiment evaluates the robustness of our method under diferent proportions of labelled and unlabelled class categories. Specifically, we vary the labelled-to-unlabelled class ratio, denoted as $\rho = C _ { L } / C _ { U } ,$ , where $C _ { L }$ is the number of classes with available labels and $C _ { U }$ is the number of unlabelled classes during training.

![](images/53c9a81c119631cae2e2fc50136da802022befd1a428b9d028fccedc9338d84d.jpg)  
Fi<sub>g</sub>ure 5: Heatma<sub>p</sub>s of <sub>p</sub>seudo-label assi<sub>g</sub>nment wei<sub>g</sub>hts f<sub>or un</sub>l<sub>a</sub>b<sub>e</sub>l<sub>e</sub>d <sub>samp</sub>l<sub>es un</sub>d<sub>er</sub> dif<sub>eren</sub>t l<sub>a</sub>b<sub>e</sub>l<sub>-</sub>t<sub>o-un</sub>l<sub>a</sub>b<sub>e</sub>l<sub>e</sub>d <sub>c</sub>l<sub>ass</sub> <sub>ra</sub>ti<sub>os</sub> $\rho \in \{ 0 . 5 , 1 , 2 \}$ <sub>.</sub> E<sub>ac</sub>h h<sub>ea</sub>t<sub>map s</sub>h<sub>ows con</sub>fid<sub>ence</sub> scores across class indices (columns) for individual samples (rows), with color intensity indicating the pseudo-label weight (darker is higher). Red and black boxes highlight k<sub>nown</sub> <sub>an</sub>d <sub>un</sub>k<sub>nown</sub> <sub>c</sub>l<sub>ass</sub> i<sub>n</sub>di<sub>ces,</sub> <sub>respec</sub>ti<sub>ve</sub>l<sub>y.</sub> A<sub>s</sub> $\rho$ i<sub>n-</sub> <sub>creases,</sub> d<sub>ar</sub>k <sub>ver</sub>ti<sub>ca</sub>l b<sub>an</sub>d<sub>s cons</sub>i<sub>s</sub>t<sub>en</sub>tl<sub>y appear w</sub>ithi<sub>n</sub> th<sub>e</sub> unknown class region (right side of each heatmap), indicati<sub>ng</sub> th<sub>a</sub>t <sub>our me</sub>th<sub>o</sub>d <sub>ass</sub>i<sub>gns</sub> hi<sub>g</sub>h<sub>-con</sub>fid<sub>ence pseu</sub>d<sub>o-</sub>l<sub>a</sub>b<sub>e</sub>l<sub>s</sub> t<sub>o un</sub>k<sub>nown</sub> t<sub>a</sub>il <sub>c</sub>l<sub>asses even un</sub>d<sub>er severe</sub>l<sub>y</sub> i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub>d <sub>con-</sub> diti<sub>ons.</sub>

![](images/921aa90f4c6d9ae37a670d6d2ef8750fa39881d87878f87bd7c539dc82f7be25.jpg)  
Fi<sub>g</sub>ure 6: t-SNE visualization of IoT-23 embeddin<sub>g</sub>s for one head and two tail classes. LotBoNC (right) forms clearer b<sub>oun</sub>d<sub>ar</sub>i<sub>es</sub> b<sub>e</sub>t<sub>ween</sub> h<sub>ea</sub>d <sub>an</sub>d t<sub>a</sub>il <sub>c</sub>l<sub>asses,</sub> <sub>w</sub>hil<sub>e</sub> D<sub>eep</sub>T<sub>ra</sub>fi<sub>c</sub> (left) shows significant overlap.

A smaller value of $\rho$ reflects a more challenging setup, where the model must generalize from a smaller labelled class set while handling a larger pool of unknown classes. We test three representative ratios: $\rho = 0 . 5 , \rho = 1 _ { : }$ , and $\rho = 2 .$ . In all settings, we maintain a fixed total number of classes and only adjust how many of them are labelled versus unlabelled.

![](images/70bcaf31804984fb775cad3e2ab8016cc3af7808d527631ee3da6def03965d1a.jpg)

![](images/3b0cb582179f51266e8ab9e0ceef1330914691b8d1cffafe67c11145dceb4c54.jpg)  
Fi<sub>g</sub>ure 7: Class-wise <sub>p</sub>seudo-label distribution recover<sub>y</sub> com-<sub>p</sub>arison for Dee<sub>p</sub>Trafic and LotBoNC a<sub>g</sub>ainst the <sub>g</sub>round t<sub>ru</sub>th <sub>un</sub>d<sub>er</sub> $\gamma \in \{ 1 , 5 , 1 0 \}$ <sub>.</sub> L<sub>o</sub>tB<sub>o</sub>NC <sub>re</sub>li<sub>a</sub>bl<sub>y</sub> t<sub>rac</sub>k<sub>s</sub> l<sub>ong-</sub>t<sub>a</sub>il<sub>e</sub>d t<sub>arge</sub>t<sub>s</sub> <sub>across</sub> <sub>a</sub>ll i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub> l<sub>eve</sub>l<sub>s,</sub> <sub>w</sub>hil<sub>e</sub> D<sub>eep</sub>T<sub>ra</sub>fi<sub>c</sub> <sub>co</sub>l<sub>-</sub> l<sub>apses</sub> min<sub>o</sub>rit<sub>y es</sub>tim<sub>a</sub>t<sub>es.</sub>

Table 3 summarizes the results across all three datasets. When $\rho = 0 . 5$ , meaning only one labelled class for every two unlabelled classes, the method already achieves strong performance. For ex ample, the all-class accuracy reaches 83.56 on IoT-23, 78.37 on ISCX-2014, and 81.55 on CTU-13. Despite the limited supervision, the accuracy on the labelled subset remains consistently above 98.5 across all datasets, indicating that our method preserves head-class performance even under reduced label coverage. When the ratio is increased to $\rho = 1 _ { \cdot }$ where the number of labelled and unlabelled classes is equal, we observe a consistent improvement across all evaluation settings. The all-class accuracy improves to 88.88 on IoT-23, 84.22 on ISCX-2014, and 87.89 on CTU-13. More importantly, the accuracy on the unlabelled-aware setting shows substantial gains, reaching 84.01 on IoT-23 and 82.46 on $C T U - 1 3 .$ This indicates that including more labelled categories helps the model construct a more structured latent space that benefits generalization to un seen classes. Further increasing the ratio to $\rho = 2$ continues to enhance performance, though with diminishing returns. The all class accuracy reaches 94.41 on IoT-23 and 93.60 on CTU-13, while unlabelled-aware accuracy improves to 92.59 and 91.33, respectively. The performance gap between unlabelled-aware and unlabelled agnostic settings narrows as the ratio increases, suggesting that the model becomes increasingly capable of uncovering the structure of unseen classes even when they are not explicitly labelled. To better understand this behavior, Figure 5 visualizes the pseudo-label assignment weights for unlabeled samples under each � setting. Each heatmap displays the predicted confidence scores across all class indices, where each row represents a sample and each column corresponds to a predicted class. Higher intensity (darker) values indicate stronger assignment confidence. The known and unknown class indices are marked with red and black vertical borders, re spectively. $\operatorname { A s } \rho$ increases, the model assigns stronger and more structured pseudo-label weights to unknown classes, reflecting its improved ability to generalize to novel categories. This visualiza tion complements the quantitative results by revealing how the latent space becomes increasingly disentangled and class-separable as more labelled classes are introduced.

<table><tr><td> $\rho$ </td><td>Dataset</td><td>Overall</td><td>Labelled</td><td>Unlabelled-Aw $^{\dagger}$ </td><td>Unlabelled-Ag $^{\dagger}$ </td></tr><tr><td rowspan="3">0.5</td><td>IoT-23</td><td>83.56 ± 0.76</td><td>99.23 ± 0.08</td><td>75.73 ± 0.20</td><td>73.54 ± 0.60</td></tr><tr><td>ISCX-2014</td><td>78.37 ± 0.02</td><td>98.57 ± 0.64</td><td>68.27 ± 0.79</td><td>67.79 ± 0.61</td></tr><tr><td>CTU-13</td><td>81.55 ± 0.49</td><td>98.93 ± 0.38</td><td>72.86 ± 0.57</td><td>71.93 ± 0.55</td></tr><tr><td rowspan="3">1</td><td>IoT-23</td><td>88.88 ± 0.19</td><td>98.61 ± 0.41</td><td>84.01 ± 0.78</td><td>82.82 ± 0.13</td></tr><tr><td>ISCX-2014</td><td>84.22 ± 0.57</td><td>97.39 ± 0.71</td><td>77.64 ± 0.68</td><td>76.70 ± 0.33</td></tr><tr><td>CTU-13</td><td>87.89 ± 0.70</td><td>98.75 ± 0.08</td><td>82.46 ± 0.59</td><td>80.96 ± 0.06</td></tr><tr><td rowspan="3">2</td><td>IoT-23</td><td>94.41 ± 0.69</td><td>98.04 ± 0.48</td><td>92.59 ± 0.47</td><td>85.34 ± 0.31</td></tr><tr><td>ISCX-2014</td><td>88.79 ± 0.72</td><td>97.74 ± 0.46</td><td>84.31 ± 0.69</td><td>77.68 ± 0.11</td></tr><tr><td>CTU-13</td><td>93.60 ± 0.52</td><td>98.14 ± 0.16</td><td>91.33 ± 0.49</td><td>85.30 ± 0.51</td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 3<sub>:</sub> P<sub>er</sub>f<sub>ormance o</sub>f L<sub>ot</sub>B<sub>o</sub>NC <sub>un</sub>d<sub>er</sub> dif<sub>eren</sub>t l<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d<sub>-</sub> t<sub>o-un</sub>l<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d <sub>c</sub>l<sub>ass ra</sub>ti<sub>os.</sub> ${ \dot { \vec { \uparrow } } } \mathbf { \nabla } { \boldsymbol { \mathsf { n } } } _ { \mathbf { A } \mathbf { w } " }$ <sub>s</sub>t<sub>an</sub>d<sub>s</sub> f<sub>or</sub> A<sub>ware an</sub>d "A<sub>g</sub>" <sub>s</sub>t<sub>an</sub>d<sub>s</sub> f<sub>or</sub> A<sub>gnos</sub>ti<sub>c.</sub>

## 5.7 Ablation Stud<sub>y</sub>

5.7.1 Impact ofclass imbalance distribution. To assess the impact of unknown-class distribution shape, we perform an ablation study where the exponential long-tailed distribution is replaced with a step-decreasing alternative, following the protocol introduced in LDAM [6]. This variant groups unknown classes into buckets with equal sample counts, decreasing in discrete steps. Importantly, we keep the total number of unknown samples fixed via the same $\gamma = n _ { k } / n _ { u }$ , ensuring that the global class ratio remains unchanged. This isolates the efect of distribution shape alone. Table 4 reports the overall and unlabeled accuracy across three datasets and three imbalance levels $( \gamma \in \{ 1 , 5 , 1 0 \} )$ , comparing our method and a representative baseline (DeepTrafic). We observe that switching to a step-decreasing histogram consistently improves performance across all settings. The gains are especially pronounced on the unlabelled metric, with improvements ranging from 3–5% for both DeepTrafic and LotBoNC. This demonstrates that models benefit from reducing the severity of the extreme tail classes. In addition, the relative performance gap remains consistent that LotBoNC continues to outperform the strongest baseline under both distribution shapes and all imbalance settings. These findings suggest that while distribution shape afects absolute accuracy, LotBoNC’s advantage is robust across diferent structures.

5.7.2 Impact of Pre-training. We assess the efectiveness of pretraining in improving novel class discovery under varying levels of imbalance $( \gamma \in \{ 1 , 5 , 1 0 \} )$ ). As summarized in Table 5, pre-training consistently enhances performance across all datasets and imbalance settings. For instance, at $\gamma = 1 _ { : }$ , the unlabelled-agnostic accuracy improves from 60.21% to 75.73% on IoT-23, from 52.18% to 68.27% on ISCX-2014, and from 58.34% to 72.86% on CTU-13. The improvements are even more substantial at higher imbalance levels; at $\gamma = 1 0 ;$ , accuracy increases from 77.82% to 92.59% on IoT-23, from 66.48% to 84.31% on ISCX-2014, and from 75.10% to 91.33% on CTU-13. These results confirm that our pre-training is crucial for discovering novel botnet under severe long-tailed conditions.

5.7.3 Impact ofLoss Ratio. We study the influence of the loss ratio $\lambda _ { \mathrm { p r o t o } } ,$ which controls the trade-of between prototype-level supervision and instance-level contrastive learning. We vary � ∈ $\{ 0 . 1 , 0 . 3 , 0 . 5 , 0 . 7 , 1 . 0 \}$ across three imbalance scenarios defined by $\gamma \in \{ 1 , 5 , 1 0 \}$ , where a higher � indicates a more severe long-tailed distribution in the unlabeled data. The results are reported in Figure 8 over four evaluation metrics: All, Labelled, Unlabelled-Aware, and Unlabelled-Agnostic. We observe that as the class imbalance increases from $\gamma = 1 \tan \gamma = 1 0$ , the unlabelled-aware and unlabelled agnostic accuracies gradually decrease, reflecting the increasing dificulty in discovering novel tail classes. Conversely, the labelled and overall accuracies show a slight increase, as the higher imbal ance implies a larger volume of labeled data relative to unknowns. This trend is consistent across all loss ratios. Across all three imbal ance levels, we find that $\lambda _ { \mathrm { p r o t o } } = 0 . 7$ yields the best performance in every metric. For instance, under the balanced setting $( \gamma = 1 )$ increasing � from 0.1 to 0.7 improves the unlabelled-aware accuracy from 73.8% to 79.5%, and unlabelled-agnostic accuracy from 71.0% to 76.5%, while maintaining high labelled accuracy (above 98.0%) and improving the all-class accuracy from 83.5% to 86.2%. Similar improvements are observed at $\gamma = 5 ,$ , where unlabelled-aware accu racy rises from 66.5% to 74.0%, and at $\gamma = 1 0 ;$ , from 64.0% to 72.0%, with labelled accuracy exceeding 98.9% in both cases. Moreover, the diference in overall accuracy across � remains within three percentage points for each �, suggesting that the model is stable to moderate changes in this hyperparameter. Nevertheless, the consistent peak at $\lambda _ { \mathrm { p r o t o } } = 0 . 7$ highlights the importance of moderately strong prototype supervision in aligning pseudo-labels with evolving class prototypes, especially in imbalanced open-world settings.

<table><tr><td rowspan="3"> $\gamma$ </td><td rowspan="3">Metric</td><td colspan="4">IoT-23</td><td colspan="4">ISCX-2014</td><td colspan="4">CTU-13</td></tr><tr><td colspan="2">DeepTraffic</td><td colspan="2">LotBoNC</td><td colspan="2">DeepTraffic</td><td colspan="2">LotBoNC</td><td colspan="2">DeepTraffic</td><td colspan="2">LotBoNC</td></tr><tr><td>Exponential</td><td>Step</td><td>Exponential</td><td>Step</td><td>Exponential</td><td>Step</td><td>Exponential</td><td>Step</td><td>Exponential</td><td>Step</td><td>Exponential</td><td>Step</td></tr><tr><td rowspan="2">1</td><td>Overall</td><td> $59.22±0.61$ </td><td> $61.22±0.60$ </td><td> $89.88±0.19$ </td><td> $90.88±0.19$ </td><td> $53.53±0.07$ </td><td> $55.53±0.07$ </td><td> $85.72±0.57$ </td><td> $86.52±0.57$ </td><td> $60.78±0.64$ </td><td> $62.78±0.64$ </td><td> $88.89±0.70$ </td><td> $91.39±0.70$ </td></tr><tr><td>Unlabelled</td><td> $31.01±0.10$ </td><td> $35.00±0.55$ </td><td> $63.01±0.78$ </td><td> $66.01±0.80$ </td><td> $25.21±0.43$ </td><td> $28.50±0.40$ </td><td> $58.23±0.68$ </td><td> $62.23±0.70$ </td><td> $32.60±0.38$ </td><td> $36.00±0.38$ </td><td> $61.84±0.59$ </td><td> $66.84±0.60$ </td></tr><tr><td rowspan="2">5</td><td>Overall</td><td> $63.50±0.61$ </td><td> $65.00±0.61$ </td><td> $91.30±0.19$ </td><td> $92.30±0.19$ </td><td> $56.80±0.07$ </td><td> $58.20±0.07$ </td><td> $88.30±0.57$ </td><td> $89.30±0.57$ </td><td> $63.90±0.64$ </td><td> $65.30±0.64$ </td><td> $90.90±0.70$ </td><td> $92.00±0.70$ </td></tr><tr><td>Unlabelled</td><td> $20.15±0.10$ </td><td> $23.50±0.10$ </td><td> $40.96±0.78$ </td><td> $44.50±0.80$ </td><td> $17.65±0.43$ </td><td> $20.50±0.43$ </td><td> $40.76±0.68$ </td><td> $43.00±0.70$ </td><td> $22.82±0.38$ </td><td> $25.80±0.38$ </td><td> $43.29±0.59$ </td><td> $46.00±0.60$ </td></tr><tr><td rowspan="2">10</td><td>Overall</td><td> $68.00±0.61$ </td><td> $69.20±0.61$ </td><td> $92.90±0.19$ </td><td> $93.90±0.19$ </td><td> $60.40±0.07$ </td><td> $61.60±0.07$ </td><td> $90.20±0.57$ </td><td> $91.20±0.57$ </td><td> $67.30±0.64$ </td><td> $68.50±0.64$ </td><td> $92.90±0.70$ </td><td> $94.00±0.70$ </td></tr><tr><td>Unlabelled</td><td> $13.00±0.10$ </td><td> $16.00±0.10$ </td><td> $29.00±0.78$ </td><td> $32.00±0.80$ </td><td> $12.50±0.43$ </td><td> $15.00±0.43$ </td><td> $30.50±0.68$ </td><td> $33.00±0.70$ </td><td> $14.10±0.38$ </td><td> $17.00±0.38$ </td><td> $30.10±0.59$ </td><td> $33.50±0.60$ </td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 4<sub>:</sub> F<sub>or eac</sub>h i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub> l<sub>eve</sub>l $\gamma ,$ <sub>we repor</sub>t <sub>per</sub>f<sub>ormance on overa</sub>ll <sub>accuracy an</sub>d <sub>on</sub> th<sub>e un</sub>l<sub>a</sub>b<sub>e</sub>l<sub>e</sub>d <sub>accuracy.</sub> E<sub>ac</sub>h d<sub>a</sub>t<sub>ase</sub>t com<sub>p</sub>ares baseline Dee<sub>p</sub>trafic with our LotBoNC under the ex<sub>p</sub>onential and ste<sub>p</sub>-decreasin<sub>g</sub> distribution.

<table><tr><td>γ</td><td>Setting</td><td>IoT-23</td><td>ISCX-2014</td><td>CTU-13</td></tr><tr><td rowspan="2">1</td><td>w/ Pre-train</td><td>88.20</td><td>82.55</td><td>80.05</td></tr><tr><td>w/o Pre-train</td><td>74.21</td><td>72.18</td><td>68.34</td></tr><tr><td rowspan="2">5</td><td>w/ Pre-train</td><td>73.54</td><td>67.79</td><td>71.93</td></tr><tr><td>w/o Pre-train</td><td>65.75</td><td>58.13</td><td>60.89</td></tr><tr><td rowspan="2">10</td><td>w/ Pre-train</td><td>56.05</td><td>52.78</td><td>56.07</td></tr><tr><td>w/o Pre-train</td><td>47.82</td><td>41.23</td><td>45.19</td></tr></table>

Table 5: Unlabelled-agnostic accuracy (%) of evaluating the im<sub>p</sub>act of the <sub>p</sub>re-trainin<sub>g</sub> across var<sub>y</sub>in<sub>g</sub> imbalance ratios $( \gamma \in 1 , 5 , 1 0 )$ <sub>.</sub> Pr<sub>e</sub>-tr<sub>a</sub>inin<sub>g y</sub>i<sub>e</sub>ld<sub>s su</sub>b<sub>s</sub>t<sub>a</sub>nti<sub>a</sub>l im<sub>p</sub>r<sub>ove</sub>m<sub>e</sub>nt<sub>s</sub> in <sub>nove</sub>l <sub>c</sub>l<sub>ass</sub> di<sub>scovery w</sub>h<sub>en c</sub>l<sub>ass</sub> i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub> i<sub>ncreases.</sub>

5.7.4 Impact of Loss Components. We explore the contribution of each loss component in our framework under varying class imbal ance settings defined by $\gamma \in \{ 1 , 5 , 1 0 \}$ . Specifically, we remove one loss term at a time: the prototype-based loss $( { \mathcal { L } } _ { \mathrm { p r o t o } } ) ,$ the instancelevel contrastive loss $( \mathcal { L } _ { \mathrm { i n s } } )$ , and the supervised loss $( \mathcal { L } _ { \mathrm { s u p } } )$ , and compare each variant to the full LotBoNC model. Results across all four evaluation metrics are reported in Figure 9. Across all imbalance levels, the full model outperforms its ablated variants. At $\gamma = 1 ,$ , where class distribution is balanced, removing the supervised loss leads to the most severe degradation: all-class accuracy drops from 86.2% to $6 1 . 0 \%$ , and unknown-aware accuracy falls from 79.5% to 46.0%. This shows that supervision from labeled samples is crucial to anchor representation learning even in balanced scenarios. Removing $\scriptstyle { \mathcal { L } } _ { \mathrm { p r o t o } }$ or $\mathcal { L } _ { \mathrm { i n s } }$ also weakens performance, reducing unlabelled-aware accuracy to 73.0% and 50.0%, respectively. As the imbalance intensifies at $\gamma = 5 ,$ the gap becomes more pronounced. LotBoNC achieves 74.0% unknown-aware accuracy, while its no-$\mathcal { L } _ { \mathrm { s u p } }$ variant drops to $2 8 . 0 \% ,$ and no- $\mathcal { L } _ { \mathrm { i n s } }$ variant to 35.0%. The full model also maintains a high labelled accuracy of 99.1%, compared to 75.0% without $\mathcal { L } _ { \mathrm { s u p } } .$ This underscores the importance of both supervised grounding and instance-level consistency when facing long-tailed unknown-class distributions. $\mathrm { A t } \ \gamma = \ 1 0$ , the hardest setting, we observe similar patterns. The full method maintains 72.0% unknown-aware accuracy and 69.5% unknown-agnostic accu racy. In contrast, omitting $\mathcal { L } _ { \mathrm { { s u p } } }$ leads to a substantial drop to 25.0% and 23.0%, respectively. Meanwhile, removing $\mathcal { L } _ { \mathrm { i n s } }$ still causes a notable degradation to 32.0% in unknown-aware accuracy. Overall, while all three components contribute meaningfully especially in severely imbalanced settings. These results validate the necessity of combining global prototype alignment, local contrastive regularization, and supervised signals to robustly discover novel classes under open-world imbalance.

![](images/1e85428d7748605533d7ce0da13420294d7d90bcbc2145916b31d40fad602c1c.jpg)  
Figure 8: Im<sub>p</sub>act o<sup>f</sup> <sub>p</sub>rotot<sub>yp</sub>e <sup>l</sup>oss ratio <sup>�</sup> on <sub>p</sub>er<sup>f</sup>ormance und<sub>er</sub> dif<sub>eren</sub>t l<sub>a</sub>b<sub>e</sub>l<sub>-un</sub>l<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d <sub>c</sub>l<sub>ass ra</sub>ti<sub>os</sub> $\rho .$ Hi<sub>g</sub>her � consistentl<sub>y</sub> im<sub>p</sub>roves unknown-aware and unknown-a<sub>g</sub>nostic accurac<sub>y</sub>, in<sup>d</sup>icating stronger <sub>p</sub>rotot<sub>yp</sub>e su<sub>p</sub>ervision en<sup>h</sup>ances <sub>nove</sub>l <sub>c</sub>l<sub>ass</sub> di<sub>scovery.</sub>

![](images/70bcd4d1fe6b4fb043c7ef44dc218c3aa06eca1b1485cc8b06cd649a4850efbe.jpg)  
Fi<sub>gure</sub> 9<sub>:</sub> Abl<sub>a</sub>ti<sub>on o</sub>f l<sub>oss componen</sub>t<sub>s un</sub>d<sub>er vary</sub>i<sub>ng</sub> l<sub>a</sub>b<sub>e</sub>l <sub>un</sub>l<sub>a</sub>b<sub>e</sub>ll<sub>e</sub>d <sub>c</sub>l<sub>ass ra</sub>ti<sub>os</sub> $\gamma \in \{ 1 , 5 , 1 0 \}$ . <sup>R</sup>emov<sup>i</sup>ng any compo-<sub>nen</sub>t d<sub>egra</sub>d<sub>es per</sub>f<sub>ormance, w</sub>ith th<sub>e</sub> l<sub>arges</sub>t d<sub>rop o</sub>b<sub>serve</sub>d when omittin<sub>g</sub> su ervised loss $( \mathcal { L } _ { \mathbf { s u p } } ) .$ . <sup>P</sup>rotot<sub>yp</sub>e <sup>l</sup>oss $\scriptstyle ( \mathcal { L } _ { \mathbf { p r o t o } } )$ i<sub>s</sub> <sub>essen</sub>ti<sub>a</sub>l f<sub>or</sub> <sub>nove</sub>l <sub>c</sub>l<sub>ass</sub> <sub>separa</sub>ti<sub>on,</sub> <sub>w</sub>hil<sub>e</sub> i<sub>ns</sub>t<sub>ance</sub> <sub>con-</sub> t<sub>ras</sub>ti<sub>ve</sub> l<sub>oss</sub> $( \mathcal { L } _ { \mathrm { i n s } } )$ <sub>a</sub>id<sub>s s</sub>t<sub>a</sub>bilit<sub>y un</sub>d<sub>er</sub> h<sub>eavy</sub> i<sub>m</sub>b<sub>a</sub>l<sub>ance.</sub>

5.7.5 Impact ofEncoder Dropout Rate. We evaluate the efect of encoder-level stochasticity by varying the dropout rate across four values: 0, 0.05, 0.10, and 0.50. while keeping all other settings fixed. Experiments are conducted on three datasets under imbalance levels of 1,5 and10, consistent with the previous experiments. As shown in Table 6, all datasets exhibit a consistent trend: performance is lowest at $\hbar = 0$ , improves with mild dropout, and peaks at $p = 0 . 1 0$ . Heavier noise $( \mathinner { p \mathopen { / { \vphantom { ( p \mathopen { / { \vphantom { ( p \mathstrut } }  \kern - delimiterspace } } }  \kern - delimiterspace } } = 0 . 5 0 )  $ leads to a clear decline. These results confirm that moderate dropout is essential for learning stable representations, while excessive noise impairs generalization particularly under class imbalance. We therefore adopt $p = 0 . 1 0$ as the default in all experiments.

## 6 Ethi<sub>ca</sub>l C<sub>o</sub>n<sub>s</sub>id<sub>e</sub>r<sub>a</sub>ti<sub>o</sub>n<sub>s a</sub>nd O<sub>pe</sub>n S<sub>ou</sub>r<sub>ce</sub>

All experiments in this study were conducted exclusively on pub licly available datasets were released by academic and research institutions under licenses permitting non-commercial research. We strictly adhere to their respective usage terms and confirm that no private, personally identifiable, or proprietary information is involved. No trafic was intercepted, collected, or analyzed outside the scope of these public datasets. LotBoNC is intended to improve the robustness and reliability of network defense systems through automated discovery of novel botnet behaviors. However, we acknowledge that any trafic classification system, if misused, may pose ethical risks such as non-consensual monitoring, profiling, or censorship. To mitigate this, we emphasize that our framework is designed for deployment in regulated, legally compliant environments such as enterprise security operations centers, academic research networks, or CERTs, where oversight and data governance structures are in place. We explicitly discourage the application of this research in surveillance infrastructures that lack transparent accountability mechanisms or operate outside democratic oversight. While our system does not target user content and operates solely on encrypted flow-level metadata, we recognize that any form of automated trafic analysis must be handled with care to avoid unintended consequences.

<table><tr><td rowspan="2">p</td><td colspan="3">IoT-23</td><td colspan="3">ISCX</td><td colspan="3">CTU-13</td></tr><tr><td>γ=1</td><td>5</td><td>10</td><td>1</td><td>5</td><td>10</td><td>1</td><td>5</td><td>10</td></tr><tr><td>0.00</td><td>58.2</td><td>61.3</td><td>63.5</td><td>60.2</td><td>62.5</td><td>64.8</td><td>62.0</td><td>64.5</td><td>66.8</td></tr><tr><td>0.05</td><td>88.1</td><td>89.7</td><td>90.9</td><td>83.9</td><td>86.0</td><td>88.0</td><td>87.0</td><td>89.2</td><td>91.4</td></tr><tr><td>0.10</td><td>89.9</td><td>91.3</td><td>92.9</td><td>85.7</td><td>88.3</td><td>90.2</td><td>88.9</td><td>90.9</td><td>92.9</td></tr><tr><td>0.50</td><td>70.1</td><td>71.5</td><td>72.3</td><td>65.6</td><td>67.3</td><td>69.0</td><td>69.0</td><td>70.7</td><td>72.4</td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 6<sub>:</sub> O<sub>vera</sub>ll <sub>accuracy</sub> f<sub>or</sub> dif<sub>eren</sub>t d<sub>ropou</sub>t <sub>ra</sub>t<sub>es</sub> ${ \boldsymbol { p } } ,$ <sub>an</sub>d i<sub>m</sub>b<sub>a</sub>l<sub>ance</sub> l<sub>eve</sub>l<sub>s �.</sub>

To support responsible innovation and reproducibility, we will release related code and scripts upon publication. We encourage the research community to build upon our work within the bounds of ethical, lawful, and privacy-respecting usage.

## 7 C<sub>o</sub>n<sub>c</sub>l<sub>us</sub>i<sub>o</sub>n

This work introduces LotBoNC, a framework for long-tailed novel botnet trafic classification under open-world conditions. By integrating entropy-regularized optimal transport with prototype refinement, LotBoNC achieves calibrated pseudo-label assignments that preserve tail semantics while avoiding collapse into dominant known classes. Our extensive evaluations across diverse trafic domains demonstrate consistent state-of-the-art performance, especially under severe imbalance and low supervision. Beyond classification accuracy, LotBoNC exhibits robustness in discovering novel botnet clusters, setting a new baseline for practical open-world encrypted trafic analysis.

## R<sub>e</sub>f<sub>erences</sub>

[1] Sina Ahmadi. Evolving botnet defenses: A survey of machine learning approaches, 2024.

[2] M. Asadi, A. Heidari, and N. Jafari Navimipour. A new flow-based approach for enhancing botnet detection eficiency using convolutional neural networks and long short-term memory. Knowledge and Information Systems, 67:6139–6170, 2025.

[3] Jesse Atuhurra, Takanori Hara, Yuanyu Zhang, et al. Dealing with imbalanced classes in bot-iot dataset. arXiv preprint arXiv:2403.18989, 2024.

[4] Ehsan Biglar Beigi, Hossein Hadian Jazi, Natalia Stakhanova, and Ali A. Ghorbani. Towards efective feature selection in machine learning-based botnet detection approaches. In 2014 IEEE Conference on Communications and Network Security (CNS), 2014.

[5] Kaidi Cao, Maria Brbic, and Jure Leskovec. Open-world semi-supervised learning. arXiv preprint arXiv:2102.03526, 2021.

[6] Kaidi Cao, Colin Wei, Adrien Gaidon, Nikos Arechiga, and Tengyu Ma. Learning imbalanced datasets with label-distribution-aware margin loss. Advances in neural information processing systems, 32, 2019.

[7] Nitesh V. Chawla, Kevin W. Bowyer, Lawrence O. Hall, and W. Philip Kegelmeyer. Smote: Synthetic minority over-sampling technique. Journal ofArtificial Intelligence Research, 2002.

[8] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geofrey Hinton. A simple framework for contrastive learning of visual representations. In International Conference on Machine Learning (ICML), 2020.

[9] Xinlei Chen, Haoqi Fan, Ross Girshick, and Kaiming He. Improved baselines with momentum contrastive learning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 14471–14480, 2021.

[10] Yin Cui, Menglin Jia, Tsung-Yi Lin, Yang Song, and Serge Belongie. Class-balanced loss based on efective number of samples. In CVPR, 2019.

[11] Marco Cuturi. Sinkhorn distances: Lightspeed computation of optimal transport. In Advances in Neural Information Processing Systems (NeurIPS), volume 26, 2013.

[12] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. Bert: Pre training of deep bidirectional transformers for language understanding. In Proceedings ofthe 2019 conference ofthe North American chapter ofthe association for computational linguistics: human language technologies, volume 1 (long and short papers), pages 4171–4186, 2019.

[13] A. B. Downey. Evidence for long-tailed distributions in the internet. In Proceedings ofthe Internet Measurement Workshop, 2001. Highly cited foundational study.

[14] K. Friday, E. Bou-Harb, and J. Crichigno. Inc: In-network classification of botnet propagation at line rate. In ESORICS / Industry-grade SDN botnet detection, 2022.

[15] Tianyu Gao, Xingcheng Yao, and Danqi Chen. Simcse: Simple contrastive learning of sentence embeddings. arXiv preprint arXiv:2104.08821, 2021.

[16] Sebastian Garcia, Martin Grill, Jan Stiborek, and Alejandro Zunino. An empirical comparison of botnet detection methods. Computers & Security, 2014.

[17] Sebastian Garcia, Agustin Parmisano, and Maria Jose Erquiaga. IoT-23: A labeled dataset with malicious and benign IoT network trafic (version 1.0.0), 2020.

[18] Gerard Drapper Gil, Arash Habibi Lashkari, Mohammad Mamun, and Ali A Ghorbani. Characterization of encrypted and vpn trafic using time-related features. In Proceedings ofthe 2nd international conference on information systems security and privacy (ICISSP 2016), pages 407–414, 2016.

[19] Harm Grifioen and Christian Doerr. Examining mirai’s battle over the internet of things. In Proceedings ofthe 2020 ACM SIGSAC Conference on Computer and Communications Security, pages 743–756, 2020.

[20] Ragini Gupta, Shinan Liu, Ruixiao Zhang, Xinyue Hu, Pranav Kommaraju, Xi aoyang Wang, Hadjer Benkraouda, Nick Feamster, and Klara Nahrstedt. Genera tive active adaptation for drifting and imbalanced network intrusion detection. arXiv preprint arXiv:2503.03022, 2025

[21] Huancheng Hu, Ziyun Li, and Christian Doerr. Bonc: Discovering and classifying novel encrypted botnet trafic. IEEE Open Journal of the Communications Society, pages 1–1, 2025.

[22] Johan Jensen. Sur les fonctions convexes et les inégalités entre les valeurs moyennes. Acta Mathematica, 30:175–193, 1906.

[23] Steven Jorgensen, John Holodnak, Jensen Dempsey, Karla de Souza, Ananditha Raghunath, Vernon Rivet, Noah DeMoes, Andrés Alejos, and Allan Wollaber. Extensible machine learning for encrypted network trafic application labeling via uncertainty quantification. IEEE Transactions on Artificial Intelligence, 5(1):420– 433, 2024.

[24] Bingyi Kang et al. Decoupling representation and classifier for long-tailed recog nition. In ICLR, 2020.

[25] Prannay Khosla, Piotr Teterwak, Chen Wang, Aaron Sarna, Yonglong Tian, Phillip Isola, Aaron Maschinot, Ce Liu, and Dilip Krishnan. Supervised contrastive learning. In Advances in Neural Information Processing Systems (NeurIPS), 2020.

[26] G. Kirubavathi and R. Anitha. Botnet detection via mining of trafic flow charac teristics. Computers & Electrical Engineering, 2016.

[27] Harold W Kuhn. The hungarian method for the assignment problem. Naval research logistics quarterly, 2(1-2):83–97, 1955.

[28] Pranita Kumari et al. A comprehensive study of ddos attacks over iot network. Computers and Security, 2023.

[29] CUJO AI Labs. 2022–2023 internet-wide botnet threat report. https://cujo.com/ resources/2022-23-botnet-report-download/, 2022.

[30] Aleksandar Lazarevic, Levent Ertöz, Aysel Ozgur, Vipin Kumar, and Jaideep Srivastava. A comparative study of anomaly detection schemes in network intrusion detection. In Proceedings ofthe Third SIAM International Conference on Data Mining (SDM), pages 25–36. SIAM, 2003.

[31] Junnan Li, Pan Zhou, Caiming Xiong, and Steven C.H. Hoi. Prototypical con trastive learning of unsupervised representations. In ICLR, 2021.

[32] Ziyun Li, Ben Dai, Christoph Meinel, and Haojin Yang. Imbagcd: Imbalanced generalized category discovery. In CVPR Workshop, 2023. Spotlight.

[33] Ziyun Li, Ben Dai, Christoph Meinel, and Haojin Yang. Otem-igcd: An optimal transport-based em framework for imbalanced generalized category discovery. In 2024 International Joint Conference on Neural Networks (IJCNN), 2024.

[34] Ziyun Li, Jona Otholt, Ben Dai, Di Hu, Christoph Meinel, and Haojin Yang. A closer look at novel class discovery from the labeled set. In Workshop on Distribution Shifts, NeurIPS, 2022

[35] Ziyun Li, Jona Otholt, Ben Dai, Di Hu, Christoph Meinel, and Haojin Yang. Supervised knowledge may hurt novel class discovery performance. Transactions on Machine Learning Research (TMLR), 2023.

[36] Kunda Lin, Xiaolong Xu, and Honghao Gao. Tscrnn: A novel classification scheme of encrypted trafic based on flow spatiotemporal features for eficient management of iiot. Computer Networks, 2021.

[37] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. ET-BERT: A contextualized datagram representation with pre-training transformers for encrypted trafic classification. In WWW ’22: The ACM Web Conference 2022, Virtual Event, Lyon, France, April 25 - 29, 2022, 2022.

[38] Ziwei Liu et al. Open long-tailed recognition in a dynamic world. arXiv preprint, 2022.

[39] Ziwei Liu, Zhongqi Miao, Xiaohang Zhan, Jiayun Wang, Boqing Gong, and Stella X. Yu. Large-scale long-tailed recognition in an open world. arXiv preprint, 2019.

[40] Mohammad Lotfollahi, Mahdi Jafari Siavoshani, Ramin Shirali Hossein Zade, and Mahdi Saberian. Deep packet: A novel approach for encrypted trafic classification using deep learning. Soft Computing, 24(3):1999–2012, 2020.

[41] Ramy Maarouf, Danish Sattar, and Ashraf Matrawy. Evaluating resilience of en crypted trafic classification against adversarial evasion attacks. arXiv:2105.14564, 2021. arXiv preprint.

[42] M.V. Mahoney and P.K. Chan. Learning rules for anomaly detection of hostile network trafic. In Third IEEE International Conference on Data Mining, pages 601–604, 2003.

[43] L. D. Manocchio, S. Layeghy, W. W. Lo, G. K. Kulatilleke, M. Sarhan, and M. Portmann. Flowtransformer: A transformer framework for flow-based network intrusion detection systems. arXiv preprint, 2023.

[44] Jelena Mirkovic and Peter Reiher. A taxonomy of ddos attack and ddos defense mechanisms. ACM SIGCOMM Computer Communication Review, 34(2):39–53, 2004.

[45] Nour Moustafa. A new distributed architecture for evaluating ai-based security systems at the edge: Network ton-iot datasets. Sustainable Cities and Society, 72:102994, 2021.

[46] A. Nazir et al. Advancing iot security: A systematic review of machine learningbased intrusion detection methods. Journal of King Saud University Computer and Information Sciences, 2023.

[47] C. Oh et al. A survey on tls-encrypted malware network trafic. Applied Sciences, 2021.

[48] Gabriel Peyré and Marco Cuturi. Computational optimal transport. Foundations and Trends in Machine Learning, 11(5-6):355–607, 2019.

[49] S. I. Popoola, B. Adebisi, M. Hammoudeh, H. Gacanin, and G. Gui. Stacked recurrent neural network for botnet detection in smart homes. Computers and Electrical Engineering, 92:107039, 2021.

[50] A. Sagu, N. S. Gill, P. Gulia, M. A. Shah, et al. Advances to iot security using a gru-cnn deep learning model trained on the sucmo algorithm. Scientific Reports, 15, 2025.

[51] Kuniaki Saito, Donghyun Kim, and Kate Saenko. Openmatch: Open-set consistency regularization for semi-supervised learning with outliers. arXiv preprint arXiv:2105.14148, 2021.

[52] Saurabh Sharma, Yongqin Xian, Ning Yu, and Ambuj Singh. Learning prototype classifiers for long-tailed recognition. In IJCAI, 2023.

[53] stratospherelab. Malware capture facility project. https://www.stratosphereips. org/datasets-malware, 2015.

[54] Yiyou Sun and Yixuan Li. Opencon: Open-world contrastive learning. arXiv preprint arXiv:2208.02764, 2022.

[55] Akbar Telikani, Amir H. Gandomi, Kim-Kwang Raymond Choo, and Jun Shen. A cost-sensitive deep learning-based approach for network trafic classification. IEEE Transactions on Network and Service Management, 19(1):661–670, 2022.

[56] Nam Thanh, Simon, Mads Stege, Issam El-Habr, Peter, Jesper Bang, and Nicola Dragoni. Survey on botnets: Incentives, evolution, detection and current trends.

Future Internet, 13(8):198, 2021.

[57] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Representation learning with contrastive predictive coding. arXiv preprint arXiv:1807.03748, 2018.

[58] J. Velasco-Mata. Real-time botnet detection on large network bandwidths. Scientific Reports, 2023.

[59] Ly Vu, Hoang V. Thuy, Quang Uy Nguyen, Tran N. Ngoc, Diep N. Nguyen, Dinh Thai Hoang, and Eryk Dutkiewicz. Time series analysis for encrypted trafic classification: A deep learning approach. In 2018 18th International Symposium on Communications and Information Technologies (ISCIT), pages 120–125. IEEE, 2018.

[60] Pan Wang, Shuhang Li, Feng Ye, Zixuan Wang, and Moxuan Zhang. Packetcgan: Exploratory study of class imbalance for encrypted trafic classification using cgan. IEEE International Conference on Communications, 2020.

[61] Tongze Wang, Xiaohui Xie, Wenduo Wang, Chuyi Wang, Youjian Zhao, and Yong Cui. Netmamba: Eficient network trafic classification via pre-training unidirectional mamba, 2024.

[62] Wei Wang, Ming Zhu, Jinlin Wang, Xuewen Zeng, and Zhongzhen Yang. End to-end encrypted trafic classification with one-dimensional convolution neural networks. In 2017 IEEE International Conference on Intelligence and Security Informatics (ISI), 2017.

[63] Wei Wang, Ming Zhu, Xuewen Zeng, Xiaozhou Ye, and Yiqiang Sheng. Mal ware trafic classification using convolutional neural network for representation learning. In 2017 International Conference on Information Networking (ICOIN), 2017.

[64] Xueman Wang, Yipeng Wang, Yingxu Lai, Zhiyu Hao, and Alex X. Liu. Reliable open-set network trafic classification. IEEE Transactions on Information Forensics and Security, 2025.

[65] Zihao Wang, Kar-Wai Fok, and Vrizlynn L. L. Thing. Machine learning for encrypted malicious trafic detection: Approaches, datasets and comparative study. arXiv:2203.09332, 2022. arXiv preprint.

[66] H. Wasswa, T. Lynar, A. Nanyonga, and H. Abbass. Iot botnet detection: Applica tion of vision transformer to classification of network flow trafic. arXiv preprint, 2025.

[67] Mohamed Wazzan et al. Internet of things botnet detection approaches: Analysis. Applied Sciences, 2021.

[68] George M. Weaver and Rob Thomas. Managing the threat of denial-of-service attacks. CERT Coordination Center, 2001.

[69] Chen Wei, Kihyuk Sohn, Clayton Mellina, Alan Yuille, and Fan Yang. Crest: A class-rebalancing self-training framework for imbalanced semi-supervised learning. In Proceedings ofthe IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 10857–10866, June 2021.

[70] Haipeng Yao, Chong Liu, Peiying Zhang, Sheng Wu, Chunxiao Jiang, and Shui Yu. Identification of encrypted trafic through attention mechanism based long short term memory. IEEE Transactions on Big Data, 2022.

[71] Chongsheng Zhang, George Almpanidis, Gaojuan Fan, Binquan Deng, Yanbo Zhang, Ji Liu, Aouaidjia Kamel, Paolo Soda, and João Gama. A systematic review on long-tailed learning. IEEE Transactions on Neural Networks and Learning Systems, 2025.

[72] Ruijie Zhao, Mingwei Zhan, Xianwen Deng, Yanhao Wang, Yijun Wang, Guan Gui, and Zhi Xue. Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation. In Proceedings of the AAAI Conference on Artificial Intelligence, 2023.

[73] Bolei Zhou et al. Bbn: Bilateral-branch network with cumulative learning for long-tailed visual recognition. In CVPR, pages 9719–9728, 2020.

[74] Guangmeng Zhou, Xiongwen Guo, Zhuotao Liu, Tong Li, Qi Li, and Ke Xu. TraficFormer: An Eficient Pre-trained Model for Trafic Data . In 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 2025.

## A A<sub>pp</sub>endix

## A.1 Protot<sub>yp</sub>e Loss for Unlabeled Data

We aim to learn the model parameters � that maximize the log likelihood over a set of� unlabeled samples:

$$
\theta^ {*} = \arg \max _ {\theta} \sum_ {i = 1} ^ {m} \log p \left(x ^ {(i)} \mid \theta\right)\tag{15}
$$

Here, the observed data $\left\{ x ^ { ( i ) } \right\} _ { i = 1 } ^ { m }$ is assumed to be associated with latent variables $C = \left\{ c _ { k } \right\} _ { k = 1 } ^ { | y _ { u } | }$ , where each $c _ { k }$ denotes a prototype representing a class. The total set of classes in the unlabeled data is denoted by $y _ { u } ,$ , which includes both the known classes $y _ { l }$ from the labeled data and the additional unknown classes $\mathcal { Y } _ { n } = \mathcal { Y } _ { u } \backslash \mathcal { Y } _ { l }$

The joint distribution of each input $x _ { i }$ with its associated proto type �� can be expressed as:

$$
\begin{array}{l} \theta^ {*} = \underset {\theta} {\arg \max} \sum_ {i = 1} ^ {m} \log p (x ^ {(i)} | \theta) \\ = \underset {\theta} {\arg \max} \sum_ {i = 1} ^ {m} \log \sum_ {c _ {k} \in C} p (x ^ {(i)}, c _ {k} ^ {(i)} | \theta) \end{array}\tag{16}
$$

Directly optimizing this objective is intractable, so we instead opti mize a lower bound via variational approximation:

$$
\begin{array}{l} \sum_ {i = 1} ^ {m} \log \sum_ {c _ {k} \in C} p \left(x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta\right) \\ = \sum_ {i = 1} ^ {m} \log \sum_ {c _ {k} \in C} Q \left(c _ {k} ^ {(i)}\right) \frac {p \left(x ^ {(i)} , c _ {k} ^ {(i)} \mid \theta\right)}{Q \left(c _ {k} ^ {(i)}\right)} \\ \geq \sum_ {i = 1} ^ {m} \sum_ {c _ {k} \in C} Q \left(c _ {k} ^ {(i)}\right) \log \frac {p \left(x ^ {(i)} , c _ {k} ^ {(i)} \mid \theta\right)}{Q \left(c _ {k} ^ {(i)}\right)} \end{array}\tag{17}
$$

In the above, $Q \left( c _ { k } ^ { ( i ) } \right)$ represents a variational distribution over the prototypes. The inequality follows from Jensen’s inequality [22]. Equality holds when the ratio $\frac { \mathcal { P } \left( x ^ { ( i ) } , c _ { k } ^ { ( i ) } | \theta \right) } { Q \left( c _ { k } ^ { ( i ) } \right) }$ is constant, which leads to:

$$
\begin{array}{l} Q \left(c _ {k} ^ {(i)}\right) = \frac {p \left(x ^ {(i)} , c _ {k} ^ {(i)} \mid \theta\right)}{\sum_ {c _ {k} \in C} p \left(x ^ {(i)} , c _ {k} ^ {(i)} \mid \theta\right)} \\ = \frac {p \left(x ^ {(i)} , c _ {k} ^ {(i)} \mid \theta\right)}{p \left(x ^ {(i)} \mid \theta\right)} \\ = p \left(c _ {k} ^ {(i)} \mid x ^ {(i)}, \theta\right) \end{array}\tag{18}
$$

By omitting the constant entropy term $\begin{array} { r } { - \sum _ { i = 1 } ^ { n } \sum _ { c _ { k } \in C } Q \left( c _ { k } ^ { ( i ) } \right) \log Q \left( c _ { k } ^ { ( i ) } \right) } \end{array}$ the surrogate objective becomes:

$$
\sum_ {i = 1} ^ {m} \sum_ {c _ {k} \in C} Q (c _ {k} ^ {(i)}) \log p (x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta)\tag{19}
$$

Using the E-step result, we then optimize $\operatorname { E q } .$ 19 with respect to $\theta { : }$

$$
\begin{array}{l} \sum_ {i = 1} ^ {n} \sum_ {c _ {k} \in C} Q \left(c _ {k} ^ {(i)}\right) \log p \left(x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta\right) \\ = \sum_ {i = 1} ^ {n} \sum_ {c _ {k} \in C} p \left(c _ {k} ^ {(i)} \mid x ^ {(i)}, \theta\right) \log p \left(x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta\right) \\ = \sum_ {i = 1} ^ {n} \sum_ {c _ {k} \in C} \underbrace {\mathbb {1} \left(x ^ {(i)} \in c _ {k} ^ {(i)}\right)} _ {k ^ {*} = \underset {k} {\arg \max A [ i ] [ k ], \text {then}} x ^ {(i)} \in c _ {k ^ {*}}} \log p \left(x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta\right) \end{array}\tag{20}
$$

Furthermore, we decompose the joint probability as:

$$
p \left(x ^ {(i)}, c _ {k} ^ {(i)} \mid \theta\right) = p \left(x ^ {(i)} \mid c _ {k} ^ {(i)}, \theta\right) p \left(c _ {k} ^ {(i)} \mid \theta\right)
$$

Following the formulation in [31], we model $p \left( \boldsymbol { x } ^ { ( i ) } \mid c _ { k } ^ { ( i ) } , \theta \right)$ as an isotropic Gaussian centered at the prototype $\boldsymbol { c } _ { k } ^ { ( i ) }$ , with shared variance �:

$$
\begin{array}{c} p \left(x ^ {(i)} \mid c _ {k} ^ {(i)}, \theta\right) \\ = \exp \left(\frac {- \left(v _ {i} - c _ {k} ^ {(i)}\right) ^ {2}}{2 \sigma^ {2}}\right) / \sum_ {j = 1} ^ {| C |} \exp \left(\frac {- \left(v _ {i} - c _ {j} ^ {(i)}\right) ^ {2}}{2 \sigma^ {2}}\right), \end{array}\tag{21}
$$

Here, $v _ { i } = f _ { \theta } ( x ^ { ( i ) } )$ denotes the embedding of input $x ^ { ( i ) }$ , and we apply $\ell _ { 2 }$ normalization to both $v _ { i }$ and each prototype $c _ { k } ^ { ( i ) }$ . Substituting into the likelihood, the optimization problem becomes:

$$
\begin{array}{l} \theta^ {*} = \underset {\theta} {\arg \min} \sum_ {i = 1} ^ {n} (- \log \frac {\exp \left(v _ {i} \cdot c _ {k} ^ {(i)}\right)}{\sum_ {j = 1} ^ {| \mathcal {Y} _ {u} |} \exp \left(v _ {i} \cdot c _ {j} ^ {(i)}\right)} \\ - \log p \left(c _ {k} ^ {(i)} \mid \theta\right)) \end{array}\tag{22}
$$

This leads to the following prototype-based loss for unlabeled instances:

$$
\mathcal {L} _ {p r o t o} ^ {(i)} = - \log \frac {\exp (v _ {i} \cdot c _ {k} ^ {(i)})}{\sum_ {j = 1} ^ {k} \exp (v _ {i} \cdot c _ {j} ^ {(i)})} - \log p (c _ {k} ^ {(i)} | \theta)\tag{23}
$$
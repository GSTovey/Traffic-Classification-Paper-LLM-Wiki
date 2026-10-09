# RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization

Haeseung Jeon haeseungjeon@ewha.ac.kr Ewha Womans University Division of Artificial Intelligence & Software Seoul, South Korea

Sujin Kim<sup>∗</sup> sml09181@ewha.ac.kr Ewha Womans University Division of Artificial Intelligence & Software Seoul, South Korea

Hosung Kang kanghsung717@ewhain.net Ewha Womans University Division of Artificial Intelligence & Software Seoul, South Korea

Nate Mathews njm3308@rit.edu Rochester Institute of Technology Rochester, United States

Se Eun Oh<sup>†</sup> seoh@ewha.ac.kr Ewha Womans University Division of Artificial Intelligence & Software Seoul, South Korea

## Ab<sub>s</sub>t<sub>rac</sub>t

Website Fingerprinting (WF) attacks infer visited websites from encrypted trafic patterns, threatening the anonymity of Tor users. While deep learning has improved WF accuracy on synthetic datasets its efectiveness on real Tor trafic remains unclear. We present RoFiRe, a novel WF model explicitly designed for real Tor exit traf fic. It employs dynamic window-level augmentation and RMS-based pre-normalization tailored to irregular burst patterns and variablelength traces observed in the realistic GTT23 dataset, improving data eficiency and robustness. Across standard WF, concept-drift, and real-world open-world evaluations on GTT23, RoFiRe con sistently outperforms state-of-the-art baselines by up to 9%. This study presents the first comprehensive analysis of WF on real Tor trafic, showing that WF models incorporating augmentation remain efective under realistic, data-limited conditions and can pose significant privacy risks.

## CCS Conce<sub>p</sub>ts

• Security and privacy → Network security; • Computing methodologies → Machine learning; Artificial intelligence.

## Ke<sub>y</sub>words

Tor, Trafic Analysis, Website Fingerprinting, Privacy

## ACM Reference Format:

Haeseung Jeon, Sujin Kim, Nate Mathews, Hosung Kang, and Se Eun Oh. 2026. RoFiRe: Robust Website Fingerprinting on Real-World Tor Trafic via Improved Augmentation and Normalization. In Proceedings of the ACM Web Conference 2026 (WWW’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3774904.3792592

## 1 I<sub>n</sub>t<sub>ro</sub>d<sub>uc</sub>ti<sub>on</sub>

Online privacy is an increasingly urgent concern as everyday web activities—such as searching and messaging—are routinely tracked and analyzed. To counter such surveillance, Tor [7] provides anonymity by routing trafic through multiple relays, thereby precluding source–destination linkage by any single observer. Tor further conceals packet attributes by encapsulating data into fixed-size cells. Nevertheless, despite these mechanisms, Tor remains susceptible to trafic analysis that exploits side-channel metadata.

One such attack is Website Fingerprinting (WF), which infers the websites a user visits by analyzing patterns within their encrypted trafic—such as packet direction, timing, and size [1, 13, 26, 27, 29, 33, 34, 36, 37]. In essence, it reveals the user’s online activity without decrypting their trafic. Recent deep learning (DL) models [24, 27, 32–34, 36] have achieved high accuracy by replacing handcrafted features used in traditional machine learning (ML) approaches [13, 29] with automatically learned representations.

However, DL-based WF attacks face two persistent challenges. First, they require large-scale training data and degrade rapidly over time due to concept drift, where evolving website content and delivery patterns alter trafic distributions [20]. Second, most WF research depends on artificial datasets collected under controlled lab conditions [25, 33], which fail to capture the heterogeneity of real Tor trafic–such as multiplexed circuits, user interactions, and diverse network conditions. As a result, the near-perfect accuracy (often exceeding 95%) reported in prior work [24, 34, 36] rarely translates to practical, real-world performance.

Cherubin,Jansen, and Troncoso [4] first revealed this gap through live exit-relay experiments, showing that models trained on synthetic traces fail under real Tor conditions. To explore this issue, Jansen et al. [17] collected GTT23, the first large-scale dataset of genuine Tor exit trafic, capturing diverse user behaviors, authentic base rates (the ratio of monitored to unmonitored sites), and realistic circuit-level noise, but introducing a mismatch with traditional WF models trained on entry-side observations. Building on this, CellShift [14] proposed a transduction model mapping exit-side traces to entry-side representations, showing that fingerprints from real Tor trafic remain identifiable under network distortions and realistic base rates.

Despite these advances, WF on real exit-relay trafic still faces a fundamental challenge: how to design a model that can learn robust and generalizable fingerprints from the noisy, sparse, and highly variable nature of genuine Tor trafic. Prior models were largely designed and evaluated on synthetic data, leaving them ill-equipped for the complexities of real-world conditions.

We address this gap with Robust Website Fingerprinting on Realistic and Limited Network Trafic (RoFiRe) <sup>1</sup>. Our work focuses on the exit-side threat model by building an efective classifier using realistic, ground-truth data with no trafic filtering. RoFiRe is therefore designed to better handle the statistical challenges in herent in genuine user trafic, such as very short traces and high sample variance within a website.

Unlike prior analysis-only studies [1, 14, 37] lacking dedicated architectures, RoFiRe achieves robust generalization through two key components: (1) a Dynamic Window-level augmentation (DyWin), that adapts perturbations to each trace’s length and structure, improving feature diversity and class separability; and (2) a CNN architecture integrating Root Mean Square Normal ization (RMSNorm) [43] with pre-normalization to stabilize learning under sparse, high-variance trafic. These techniques are motivated by the need for a resilient WF model capable of adapting to continuously changing website trafic patterns.

We conduct extensive evaluations across three complementary settings—a standard fingerprinting scenario, a temporal drift scenario, and a realistic open-world scenario—to capture distinct aspects of WF performance in practice. RoFiRe consistently outperforms state-of-the-art baselines such as DF [36], NetAugment [1], LaserBeak [24], and Swallow [35], while requiring no large-scale pre-training. Moreover, the model trained on genuine exit traffic generalizes efectively to synthetic datasets (BigEnough [25], AWF [33]) despite their substantially diferent trafic distributions, demonstrating strong cross-domain robustness.

These findings indicate that WF tailored to exit trafic, through tailored architectural design and dynamic augmentation, remains a realistic threat to Tor, underscoring the need for efective defenses to protect user anonymity on the web.

Our key contributions are summarized as follows:

• A WF model for Genuine Tor trafic. We present RoFiRe, a WF model designed for real-world Tor trafic, integrating RMS-based pre-normalization and DyWin to improve robustness and feature diversity under data-limited, high-variance conditions.

• Model robustness and generalization. The resulting RoFiRe not only outperforms state-of-the-art WF baselines but also generalizes efectively to synthetic WF datasets. Moreover, DyWin consistently improves upon prior augmentation strategies designed for synthetic Tor trafic, including NetAugment [1] and Swallow [35], demonstrating stronger adapt ability and efectiveness with only a few samples per site and no pretraining.

• Extensive evaluation. We comprehensively evaluate RoFiRe on GTT23 [17], BigEnough [25], AWF [33], and Deep Fingerprinting (DF) [36], showing up to 8-9% gains under standard settings and concept drift, and superior precision–recall (PR) tradeofs in realistic OW that reflect true Tor base rates.

## 2 B<sub>ac</sub>k<sub>groun</sub>d

This section reviews prior WF research, from early lab-based approaches to recent work improving realism via live Tor trafic measurements, while Appendix A.1 summarizes early WF classifiers based on synthetic datasets.

Early WF datasets, such as AWF [33] and DF [36], were generated by automated crawlers that repeatedly visited the front pages of popular websites using a small number of clients. Subsequent datasets, including GoodEnough [30], BigEnough [25], and Laserbeak [24], enhanced realism by incorporating subpages and varying browser security settings. Nevertheless, these datasets were collected in controlled lab settings with a limited set of sites, failing to reflect the heterogeneity of real Tor trafic, such as diverse user behaviors, circuit usage distributions, and fluctuating network conditions.

A major shift toward realism began with Cherubin, Jansen, and Troncoso [4], who conducted the first WF evaluation using genuine Tor trafic collected at exit relays while avoiding entry-side classification for ethical and safety reasons. They proposed an online WF framework capable of dynamically updating models without storing trafic traces, demonstrating the importance of capturing real-world diversity to assess the practical feasibility of WF attacks.

Building on this direction, Jansen et al. [17] introduced the GTT23 dataset, a 13-week corpus of genuine Tor cell traces collected from multiple exit nodes. Their work provided a detailed statistical comparison with synthetic WF datasets, highlighting GTT23’s superior realism, scale, and temporal variability. To complement this empirical dataset, subsequent research leveraged the Shadow simulator [15] to generate corresponding entry-side traces, aligning with traditional WF threat models in which the adversary monitors entry trafic to infer destinations [18].

More recently, CellShift [14] advanced this line of inquiry by devising network-level transduction from exit-side to entry-side trafic. Using GTT23, CellShift simulated realistic circuit distortions with Shadow [16] and showed that the transduced traces, despite measurable signal decay, remain informative and preserve patterns compatible with real entry-side trafic.

While previous research has characterized network-level distortions or dataset realism, our study complements them from a model-centric perspective, emphasizing how exit-based learning and dynamic augmentation strategies can enhance robustness under genuine Tor trafic. A detailed comparison between GTT23 and synthetic datasets is provided in Appendix A.2.

## 3 Th<sub>rea</sub>t M<sub>o</sub>d<sub>e</sub>l

A WF attack is executed by a local adversary who can observe a target user’s encrypted trafic as it enters the Tor network, for instance, by operating a malicious entry or guard relay. In this position, the adversary knows the user’s identity but not their ultimate destination. The objective is to infer the websites the user visits by applying an ML classifier to the distinctive fingerprints of the encrypted trafic stream.

![](images/470c48b97ef22ca65c55a6f0fffc71cc1582930ad6e452ab213fe13a03eecfe7.jpg)  
Fi<sub>gure</sub> 1<sub>:</sub> Th<sub>rea</sub>t <sub>mo</sub>d<sub>e</sub>l <sub>o</sub>f <sub>a rea</sub>li<sub>s</sub>ti<sub>c</sub> WF <sub>a</sub>d<sub>versary.</sub> Th<sub>e a</sub>d<sub>ver</sub> sar<sub>y</sub> collects trainin<sub>g</sub> data from Tor exit rela<sub>y</sub>s and a<sub>pp</sub>lies <sub>c</sub>l<sub>ass</sub>ifi<sub>ers</sub> t<sub>o</sub> i<sub>n</sub>f<sub>er we</sub>b<sub>s</sub>it<sub>e</sub> fi<sub>ngerpr</sub>i<sub>n</sub>t<sub>s.</sub>

A primary challenge for this adversary is acquiring a large and realistic dataset of labeled trafic to train their classifier. The most ef fective strategy for data collection is to operate exit relays [4, 17] to enable labeling with its ground-truth website destination. However, this methodology introduces a train-test mismatch: the adversary trains the classifier on data collected at an exit relay but must de ploy it for an attack at an entry relay. Trafic patterns at these two points difer due to Tor circuit efects such as queuing, latency, and cell reordering, which can degrade classifier performance.

Fortunately, recent research has demonstrated that this mismatch is not an insurmountable obstacle. Work by Cherubin, Jansen, and Troncoso [4] first established that while performance degrades when moving from an exit-to-exit to an exit-to-entry scenario, the signal is often strong enough for a successful attack. More recently, the concurrent work of Jansen on CellShift [14] has shown that exit-side traces can be intelligently transduced to accurately model the patterns an entry-side attacker would observe.

Given that the exit-to-entry transduction has been shown to be feasible, our study instead focuses on a more fundamental prereq uisite for successful WF attacks: building the most powerful and robust classifier using the best available real-world data. We use the GTT23 dataset [17], the largest and most realistic collection of Tor exit traces currently available, and train and evaluate models exclusively on these exit traces. This threat model is depicted in Figure 1.

This exit-only setting allows us to isolate the core ML challenge and establish a realistic upper bound on WF performance under genuine Tor trafic, free from confounding factors introduced by synthetic network simulation.

We evaluate attacks under two standard scenarios:

Closed-world (CW). The adversary assumes the user visits only a fixed set of monitored sites, enabling controlled multi-class clas sification comparisons across WF models.

Open-world (OW). The user may visit any site, monitored or not, reducing the task to binary classification: distinguishing monitored from unmonitored sites.

## 4 Ke<sub>y</sub> Characteristics of GTT23

The GTT23 dataset ofers an unparalleled level of realism for WF research compared to prior datasets collected under controlled or synthetic conditions. Unlike crawler-based corpora generated in laboratory environments, GTT23 captures trafic from genuine Tor user sessions encompassing over 1.1 million distinct domains. This scale and authenticity enable GTT23 to reflect real browsing behaviors, heterogeneous network conditions, and diverse circuit usage patterns, thereby providing a substantially richer and more representative benchmark for evaluating WF techniques.

Table 1: Ke<sub>y</sub> statistical com<sub>p</sub>arison of Bi<sub>g</sub>Enou<sub>g</sub>h and GTT23.

<table><tr><td rowspan="2">Metric (median)</td><td colspan="2">Dataset</td></tr><tr><td>BigEnough</td><td>GTT23</td></tr><tr><td>Total Duration (s)</td><td>16.21</td><td>62.57</td></tr><tr><td>Valid Cells (cnt)</td><td>680</td><td>72</td></tr><tr><td>Bursts (cnt)</td><td>47</td><td>9</td></tr></table>

![](images/ae430282b9180ad90ade9284fb1025fb67c8e59dfc7e8a1e9c1abb04174209d7.jpg)

![](images/d70939b09db5f540fe913dd5510d960c806072185121bd48e20644e1de941257.jpg)  
(a) Intra vs inter-class variance with log- (b) Intra vs inter-class variance with Fscaled F-ratio using cell count. ratio using circuit duration.  
Fi<sub>g</sub>ure 2: F-ratio com<sub>p</sub>arison of GTT23 and other s<sub>y</sub>nthetic d<sub>a</sub>t<sub>ase</sub>t<sub>s.</sub>

The GTT23 report [17] presented detailed statistical comparisons with synthetic datasets, highlighting its authenticity, scale, and circuit-level variability. Building on this, we quantify how inherent sparsity, irregular burst patterns, and reduced class separability translate into concrete modeling challenges, motivating exit-specific architectural adaptations and augmentation strategies.

In this section, we perform a quantitative analysis of GTT23 to characterize its diversity and variability across multiple dimensions. We select the 200 largest classes by instance count and randomly sample 1,000 traces per class to compute key statistics, allowing a direct comparison with BigEnough, the most recent large-scale synthetic WF dataset. Table 1 summarizes the statistics, and additional results are provided in Appendix A.3.

Shorter Trafic Length and Longer Duration. Table 1 shows that GTT23 traces are substantially sparser yet longer than BigEnough: more than half (57%) include fewer than 50 cells, and nearly one-third (29%) exceed 100 seconds. This sparsity stems from the dataset’s exit-side vantage point. As noted in prior work [28], exitside trafic often exhibits reduced cell volume and irregular sequencing due to circuit multiplexing and relay scheduling, resulting in a fragmented representation of user sessions. Furthermore, traces often capture only partial webpage transfers, as most circuits contain few cells while webpages typically exceed 450 KB [17]. Such sparsity and irregularity reflect the complex temporal structure of real Tor trafic and challenge traditional WF architectures designed for dense traces. For instance, Swallow employs interval-based augmentation that relies on stable packet density—a condition rarely met in these sparse traces.

Fewer Burst Count. A burst—two or more consecutive packets or cells transmitted in the same direction—has been widely recognized as an informative structural feature in WF attacks [8, 13, 39, 42]. While BigEnough traces exhibit a median of 47 bursts per trace, GTT23 traces contain only nine bursts on average, primarily due to their lower cell counts and session fragmentation. This sparsity restricts burst-level augmentation like NetAugment [1], which rely on frequent burst patterns for temporal expansion. To adapt to this constraint, we introduce a window-level augmentation approach (Section 5.1) that is better suited to handling sparse, asynchronous, and irregular trafic segments in exit-side datasets like GTT23.

Lower Class Separability. We measure the intrinsic discriminabil ity of GTT23 using Fisher’s ratio (F-ratio) [9, 12], which quantifies the balance between inter-class and intra-class variance: $\begin{array} { r } { \dot { F } = \frac { V _ { \mathrm { i n t e r } } } { V _ { \mathrm { i n t r a } } } ; } \end{array}$ where $\begin{array} { r } { V _ { \mathrm { i n t r a } } = \frac { 1 } { N } \sum _ { c = 1 } ^ { C } N _ { c } \sigma _ { c } ^ { 2 } } \end{array}$ and $\begin{array} { r } { V _ { \mathrm { i n t e r } } = \frac { 1 } { N } \sum _ { c = 1 } ^ { C } N _ { c } ( \mu _ { c } - \mu ) ^ { 2 } . } \end{array}$ . Here, $N _ { c }$ is the number of instances in class $c , \sigma _ { c } ^ { 2 }$ its variance, � the total number of instances, $\mu _ { c }$ the class mean, and $\mu$ the overall mean. Using both circuit length (or cell count) and duration as features, GTT23 exhibits significantly lower class separability than synthetic datasets. Based on cell count, GTT23 shows high intra-class variance $( 1 . 3 8 \times 1 0 ^ { 6 } )$ but relatively low inter-class variance $( 1 . 0 0 \times 1 0 ^ { 6 } )$ yielding an F-ratio of 0.728, considerably lower than BigEnough (1.093), AWF (8.165), and DF (5.403). When computed using du ration, the F-ratio drops further to 0.012, compared to 0.182 for BigEnough, 0.096 for AWF, and 0.039 for DF. These results high light the intrinsic dificulty of discriminating website classes under real exit-side conditions, where trafic variability, multiplexed cir cuits, and timing noise obscure distinctive patterns (Figure 2).

Implications. These characteristics, specifically sparse cell counts, irregular bursts, and low class separability, distinguish GTT23 from prior synthetic datasets, rendering existing WF architectures inef fective. This motivates our design of window-level augmentation and normalization, specifically tailored to handle such data sparsity and temporal variability.

## 5 DyWin Au<sub>g</sub>mentation

We introduce window-level augmentation, a fine-grained and flexi ble approach that improves upon burst-level augmentation [1] and time-interval-based augmentation [35]. The entire framework is illustrated in Figure 3, with the augmentation applied to the original trace, and the attack model is trained on the augmented trace.

## 5.1 Motivation

Bursts are among the most informative structural features in Tor trafic, as they capture directional packet groupings that often en code website-specific behavior. NetAugment [1] relies on burst-level transformations such as burst insertion, merging, and timestamp perturbation; however, GTT23 traces lack suficient burst structures and demonstrate sparse and irregular patterns (See Section 4), mak ing this strategy inherently restricted. Swallow’s fixed time-interval windowing struggles to adapt to the high variance of Tor trafic, often yielding sparse time bins. This limitation motivates a central question: How can augmentation be designed to generalize efectively across trafic with sparse structures and high temporal variability?

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Window-level Augmentation: Mask Window (MW), Jitter Window (JW), or No Augmentation (NONE).

1: Input: A trace $T_i$, augmentation probability $\alpha$, the number of windows $N_w$
2: Output: Augmented trace $T_i'$
3: Initialize $T_i' \leftarrow \{\}$
4: $C_t \leftarrow$ total cell count of $T_i$
5: $C_w \leftarrow \max(2, \lfloor C_t / N_w \rfloor)$
6: for each window $W_j$ in $T_i$ do
7:    Sample $\delta \sim \mathcal{U}(0.2, 1.0)$
8:    Select $aug \in \{MW, JW, NONE\} \sim (\frac{\alpha}{2}, \frac{\alpha}{2}, 1 - \alpha)$
9:    switch (aug):
10:    case MW: $W_j \leftarrow \{\}$
11:    case JW: Append $W_j$ to $T_i'$; update $t_k \leftarrow t_k + \delta$ for each $(t_k, d_k) \in W_j$
12:    case NONE: pass
13:    Append $W_j$ to $T_i'$
14: end for
15: return $T_i'$
</div>

To address this challenge, we redefine the goal of augmentation as achieving broad applicability while enhancing both representational diversity and class separability. We therefore propose DyWin, a dynamic window-based augmentation scheme that automatically adjusts the window size according to each trace’s total length. This design is inspired by patch-based augmentation in computer vision (CV) [6, 31], which adjusts to variable input resolutions with adap tive segments. Similarly, network trafic traces vary substantially in length and temporal scale, especially in realistic exit-side datasets such as GTT23. By adapting augmentation granularity to each trace, DyWin maintains applicability across both short and long sessions while preserving trafic semantics.

We design two complementary mutations for window-level augmentation, drawing inspiration from advanced techniques in CV and NLP. The first, masking, randomly removes selected windows to prevent overfitting to localized trafic patterns and encourage learning of broader contextual dependencies [6]. Conceptually, masking can be interpreted as applying dropout in the input space, thereby reducing sensitivity to fine-grained temporal variations. The second, copy–paste, is adapted from augmentation strategies in CV [10], where copied segments are spatially perturbed and reinserted into the input. This operation introduces localized variability without altering global semantics, a property that remains efective even when contextual continuity is limited [10].

Building on prior findings that applying identical transformations to all patches yields limited diversity, whereas heterogeneous perturbations promote richer representation learning [23], we integrate both mutations within a unified framework. Specifically, we randomly assign diferent mutation types across windows within a trace, thereby increasing both intra- and inter-trace diversity while preserving structural coherence. This heterogeneous strategy expands representational coverage and enables models to capture more invariant, context-aware features under the irregular trafic patterns observed in GTT23.

## 5.2 Al<sub>g</sub>orithm Details

Algorithm 1 and Figure 3 1 illustrate the overall workflow of Dy-Win. Each trace $T _ { i }$ with a total of $C _ { t }$ Tor cells is divided into $N _ { w }$ non-overlapping windows, each containing $C _ { w } = \operatorname* { m a x } ( 2 , \lfloor C _ { t } / N _ { w } \rfloor )$

(a) Single class visualization.  
![](images/e23dff8fc64b972368d5b753b38af5dbc435bf655487669b8092bb0dcf34fb3d.jpg)  
Fi<sub>g</sub>ure 3: Overview of window-level au<sub>g</sub>mentation and RoFiRe architecture.

![](images/805b9ba5274145d0fbcaa3e494fdeea791931bc1e156eea4ba62d1ff612a855d.jpg)

![](images/5531b104936ac77c18715e435c808e36d7e8d5c9d71cc9db4ae6bf15907d631e.jpg)  
(b) Three randomly selected classes visualization.  
Fi<sub>g</sub>ure 4: t-SNE visualization of 400 instances’ embeddin<sub>g</sub>s from the <sub>p</sub>enultimate FC la<sub>y</sub>er, com<sub>p</sub>aring the before (origi nal) and after (ours) au mentation when $N = 1 0 \mathbf { a n d } \mathcal { T } = 1 0 0 0 .$

cells. This partitioning ensures approximately uniform segmenta tion across traces while preventing excessively small windows. We exclude traces with $C _ { t } \leq 4$ 4 to avoid unstable perturbations.

Two hyperparameters control augmentation: $N _ { w } ,$ which determines segmentation granularity, and �, the augmentation probability that specifies how frequently window mutations are applied. We empirically chose $N _ { w } = 9$ and the augmentation probability $\alpha = 0 . 1$ for AWF and DF, and $\alpha = 0 . 3$ for BigEnough and GTT23.

For each window $W _ { j } ,$ , the algorithm samples an augmentation type ��� ∈ {MW, JW, NONE} according to probabilities $\ : ( \frac { \alpha } { 2 } , \frac { \alpha } { 2 } , 1 - $ �). This formulation ensures that each window has a total proba bility � of being perturbed, split evenly between the two mutation types. We also sample a temporal ofset $\delta \sim \mathcal { U } ( 0 . 2 , 1 . 0 )$ to control the jitter magnitude. The operations are defined as follows:

• Mask Window (MW): the current window is removed, efec tively simulating packet dropout or trafic truncation

• Jiter Window (JW): the window is first appended to the augmented trace, then duplicated with timestamps perturbed by �, emulating temporal variations.

• None (NONE): the window remains unmodified.

Each processed window (modified or not) is appended to the augmented trace $T _ { i } ^ { \prime } ,$ which is then used for model training. Larger � values increase augmentation frequency, producing stronger perturbations and greater representational diversity.

Overall, DyWin performs adaptive window-level augmentation that generalizes across both short and long flows. Unlike cell-level perturbations that alter uninformative units or burst-level methods that fail under sparse traces, DyWin operates at a robust mid-level granularity, maintaining structural coherence while introducing controlled variability across trafic segments.

## 5<sub>.</sub>3 Ef<sub>ec</sub>ti<sub>ve</sub>n<sub>ess o</sub>f DyWin

Representational-Level Efects. As visualized in Figure 4(a), embeddings of the original traces are sparsely distributed along the periphery, whereas those of the augmented traces fill previously empty regions, forming tighter and more coherent clusters. This indicates that DyWin introduces meaningful variations, enriching the latent feature space. Moreover, as illustrated in Figure 4(b), DyWin softens overly rigid inter-class boundaries, resulting in smoother decision surfaces that improve generalization and crossdomain applicability.

We further quantify these efects using the F-ratio, which measures the ratio of inter-class to intra-class variance. Quantitatively, DyWin improves both intra-class compactness and inter-class sep aration. For cell length, intra-class variance decreases by roughly 12% (from 1.61M to 1.41M), while inter-class variance increases by about 15% (from 1.06M to 1.21M), yielding an F-ratio gain from 0.66 to 0.86. For duration, the inter-class variance grows nearly fivefold (from 60K to 302K), leading to an F-ratio improvement from 0.04 to 0.12 despite a moderate increase in intra-class variance (from 1.40M to 2.57M). These results align with the qualitative observations, confirming that DyWin produces tighter within-class representations and clearer inter-class boundaries in the learned feature space.

Classification-Level Performance. To empirically assess the efectiveness of DyWin, we compared it with a simple duplication baseline under a CW configuration $( N = 1 0 , \mathcal { T } = 1 0 0 0 )$ . DyWin achieved an accuracy of 48%, surpassing simple duplication by 6 percentage points. This improvement confirms that dynamic, window-level perturbations yield richer and more balanced feature distributions than naive replication, thereby enhancing classifier generalization. DyWin also demonstrates strong benefits across various DL-based models, highlighting its overall efectiveness. Further details can be found in Table 7 in Appendix A.4.

## 6 RoFiRe A<sub>rc</sub>hit<sub>ec</sub>t<sub>ure an</sub>d N<sub>orma</sub>li<sub>za</sub>ti<sub>on</sub> Design

RMSNorm for Robust Normalization. To improve architectural stability under sparse and high-variance trafic, we explore alternative normalization strategies. Previous studies have shown that traditional methods such as BatchNorm and LayerNorm, which rely on stable mean estimates across batches or features, can degrade in performance under non-stationary conditions [43]. RMSNorm addresses this by removing mean subtraction and normalizing solely by the root mean square (RMS) value, thereby improving robustness across datasets with irregular feature distributions.

$$
\hat {x} _ {i} = \frac {x _ {i}}{\mathrm{RMS} (\mathbf {x})}, y _ {i} = \gamma \hat {x} _ {i}
$$

$$
\operatorname{RMS} (\mathbf {x}) =
$$

$\begin{array} { r } { \sqrt { \frac { 1 } { n } \sum _ { i = 1 } ^ { n } x _ { i } ^ { 2 } + \epsilon } , } \end{array}$ , and $x _ { i } , y _ { i } , n , \gamma ;$ , and � denote the input feature, output feature, feature dimension, learnable gain, and a small constant, respectively. This formulation simplifies computation and improves consistency across datasets with irregular trafic patterns.

Pre-Normalization for Gradient Stability. The placement of normalization layers also afects training stability in deep architectures. While post-normalization applies normalization after residual addition $( x _ { l + 1 } = \mathrm { N o r m } ( \mathcal { F } ( x _ { l } ) + x _ { l } ) )$ ), this formulation can lead to gradient instability. We instead adopt pre-normalization $( x _ { l + 1 } ~ =$ $\mathcal { F } ( \mathrm { N o r m } ( x _ { l } ) ) + x _ { l } )$ , which allows gradients to propagate more di rectly through residual paths, mitigating vanishing and exploding gradients. This design has become standard in modern architectures such as LLaMA and Mistral [19, 38], and is particularly efective when combined with RMSNorm.

Overall Model Architecture. As illustrated in Figure 3 2 , RoFiRe adopts a CNN-based architecture composed of five convolutional blocks for feature extraction, followed by two fully connected (FC) layers for classification. RMSNorm is applied within all convolutional blocks. Specifically, each block begins with RMSNorm to sta bilize feature scaling before convolution and includes two Conv1D layers for hierarchical feature extraction. RMSNorm is implemented as a custom TensorFlow layer with a learnable scale parameter � and a small constant � to prevent division by zero.

This design choice was further supported by our ablation study, which showed that RMSNorm and pre-norm substantially improve accuracy by 39 and 6 percentage points, respectively, with their combination yielding the best performance (+43%).

## 7 E<sub>va</sub>l<sub>ua</sub>ti<sub>on</sub>

This section presents a comprehensive evaluation of RoFiRe against state-of-the-art WF models, including DF [36], RF [34], k-FP [13], LaserBeak [24], CUMUL [29], Swallow [35], and NetAugment [1].

Experimental Setup. All experiments were conducted on a work station equipped with a single NVIDIA RTX A6000 GPU (40 GB VRAM), 7 TB SATA SSDs, and two NVMe SSDs, running Ubuntu 20.04. TensorFlow 2.9.0 and PyTorch 2.6.0 with CUDA 11.4 were used for implementation. Each model was trained for 30 epochs, except NetAugment, which required 100 epochs for pre-training. For RoFiRe, we used the Adamax optimizer with a learning rate of 0.002 and label smoothing with a factor of 0.1. For the Consistent Interaction Feature (CIF) in Swallow, the minimum and maximum time slot durations were set to 0.1 and 1.2, representing approximately 60% and 95% of the maximum timestamp in the fine-tuning training set. Every experiment was repeated three times, and we report the mean accuracy across runs with negligible variance.

## 7<sub>.</sub>1 D<sub>a</sub>t<sub>ase</sub>t<sub>s a</sub>nd Ex<sub>pe</sub>rim<sub>e</sub>nt<sub>a</sub>l S<sub>ce</sub>n<sub>a</sub>ri<sub>os</sub>

We evaluate the robustness of RoFiRe across diverse real-world conditions by designing multiple experimental scenarios. To ensure realistic trafic diversity, we exclude classes whose median cell count is below 10, while retaining all individual traces, both for training and testing in all scenarios. Unlike many prior WF studies that discard traces shorter than 100 cells, we avoid such restrictive filtering since only about 37% of GTT23 traces exceed 100 cells. The three evaluation scenarios are summarized below.

(1) Standard WF Scenario. This scenario benchmarks WF models on widely accessed domains with ample data per class:

• GTT-Mon: Top 200 classes by instance count (median cell count ≥ 10), yielding 168 classes after filtering. We randomly sample 1,000 instances per class to represent monitored sites.

• GTT-Unmon: 280,000 remaining classes (median cell count ≥ 10), split into 40K training, 40K validation, and 200K testing traces to represent unmonitored trafic.

• GTT-Pre: Pre-training set for NetAugment, containing 100 classes (500 instances each) disjoint from both GTT-Mon and GTT-Unmon.

(2) Concept Drift Scenario. This scenario evaluates temporal robustness by introducing time gaps between training and testing:

• GTT-Mon-Drift: Classes (median cell count ≥ 10) that appear consistently across Weeks 1, 7, and 13. The set contains 81 classes with 290 instances from Week 1 and 100 instances each from Weeks 7 and 13.

• GTT-Pre-Drift: Pre-training set for NetAugment, composed of 100 classes (500 instances each) sampled from Week 1, excluding GTT-Mon-Drift classes.

(3) Realistic OW Scenario. This scenario preserves the natural base rates of monitored and unmonitored trafic in Tor, avoiding artificial class balancing. We evaluate performance across three temporal spans, one week, one month, and the full 13-week dataset, while retaining the original trafic distribution:

• GTT-Week1: Top 168 classes (median cell count ≥ 10) sampled from Days 1–7, with 580 instances per class. Additionally, 100 of these classes have 500 distinct instances for NetAugment pre-training.

• GTT-Month1: Same configuration as GTT-Week1, but sam pled from Days 1–28.

• GTT-Entire: Same configuration as GTT-Week1, but sampled from Days 1–91 (Weeks 1–13).

Parameter Definitions. We used following notation throughout our experiments:

• N = number of original instances per class

• T = total instances per class (original + augmented)

• M = T /N, augmentation multiplier

Here, M represents the augmentation multiplier; related ablation results are provided in Appendix A.4.

## 7.2 CW Results

Results on GTT23. We evaluate RoFiRe and baseline WF models on the GTT-Mon dataset while varying N. Because RoFiRe generates synthetic traces through augmentation, its diversity and coverage naturally scale with N.

Table 2 shows that RoFiRe consistently outperforms all baselines across diferent N values. In particular, it achieves 5–9% higher accuracy than NetAugment, despite not relying on resource-intensive pre-training. RoFiRe’s window-level augmentation strategy yields robust performance while maintaining computational eficiency. For the trade-of between computational cost in augmentation scale, see Figure 10 in Appendix A.4.

Table 2: CW experiment results in accuracy (%) of RoFiRe and baseline models across N ∈ {1, 5, 10, 20, 90} in GTT23.

<table><tr><td rowspan="2">Model</td><td colspan="5">N</td></tr><tr><td>1</td><td>5</td><td>10</td><td>20</td><td>90</td></tr><tr><td>RoFiRE (T=250)</td><td>22</td><td>40</td><td>48</td><td>53</td><td>61</td></tr><tr><td>RoFiRE (T=500)</td><td>23</td><td>42</td><td>49</td><td>55</td><td>63</td></tr><tr><td>RoFiRE (T=1000)</td><td>23</td><td>42</td><td>51</td><td>56</td><td>63</td></tr><tr><td>DF</td><td>1</td><td>1</td><td>3</td><td>10</td><td>23</td></tr><tr><td>LaserBeak</td><td>0</td><td>3</td><td>6</td><td>4</td><td>9</td></tr><tr><td>RF</td><td>0</td><td>5</td><td>5</td><td>11</td><td>12</td></tr><tr><td>CUMUL</td><td>20</td><td>32</td><td>39</td><td>45</td><td>54</td></tr><tr><td>k-FP</td><td>1</td><td>1</td><td>2</td><td>3</td><td>9</td></tr><tr><td>NetAugment</td><td>18</td><td>34</td><td>42</td><td>49</td><td>60</td></tr><tr><td>Swallow</td><td>3</td><td>2</td><td>5</td><td>4</td><td>4</td></tr></table>

Table 3: CW experiment results in accuracy (%) of RoFiRe $( \mathcal { T } = 1 0 0 0 )$ and baseline models across N ∈ {1, 5, 10, 20, 90} in AWF<sub>,</sub> Bi<sub>g</sub>Enou<sub>g</sub>h<sub>,</sub> and DF.

<table><tr><td rowspan="2">Dataset</td><td rowspan="2">Model</td><td colspan="5">N</td></tr><tr><td>1</td><td>5</td><td>10</td><td>20</td><td>90</td></tr><tr><td rowspan="2">BigEnough</td><td>RoFiRe</td><td>30</td><td>61</td><td>74</td><td>87</td><td>97</td></tr><tr><td>NetAugment</td><td>21</td><td>49</td><td>63</td><td>76</td><td>92</td></tr><tr><td rowspan="2">AWF</td><td>RoFiRe</td><td>40</td><td>84</td><td>92</td><td>95</td><td>97</td></tr><tr><td>NetAugment</td><td>39</td><td>77</td><td>87</td><td>91</td><td>96</td></tr><tr><td rowspan="2">DF</td><td>RoFiRe</td><td>50</td><td>81</td><td>89</td><td>93</td><td>97</td></tr><tr><td>NetAugment</td><td>41</td><td>76</td><td>86</td><td>90</td><td>96</td></tr></table>

As expected, increasing N generally improves model accuracy, with the notable exceptions of LaserBeak and Swallow. LaserBeak exhibits instability, likely due to insuficient data for its attention based architecture. Similarly, Swallow relies on consistent packet counts to handle heterogeneous networks; this design conflicts with GTT23’s extreme variance, generating excessively sparse feature matrices that lead to performance fluctuations.

Interestingly, CUMUL achieves moderate accuracy even without augmentation, indicating that cumulative features (e.g., packet or cell statistics) still capture meaningful trafic patterns in sparse traces. Conversely, �-FP performs poorly, as its handcrafted features fail to generalize to sparse, high-variance Tor trafic.

Compared with the baseline models, RoFiRe demonstrates im proved computational and parameter eficiency (See Figure 11 in Appendix A.5) and greater training stability than the CNN-based DF model (See Appendix A.6).

Results on S nthetic Datasets. To further assess the generaliza tion capability of RoFiRe, we evaluate it on synthetic WF datasets, including BigEnough, AWF, and DF (Table 3). Because GTT23 is currently the only publicly available dataset containing genuine Tor exit trafic, relying on a single real-world dataset is insufi cient to verify model robustness across diverse trafic distributions. Therefore, we use synthetic datasets with distinct collection method ologies and statistical characteristics to examine whether RoFiRe can generalize beyond GTT23’s distribution. For NetAugment pretraining, we always used AWF, since BigEnough and DF lacked suficient classes for both pre-training and fine-tuning. Across all datasets, RoFiRe consistently outperforms the previous state-ofthe-art model, NetAugment, achieving accuracy improvements of 5–12% on BigEnough, 1–7% on AWF, and 1–9% on DF.

T<sub>a</sub>bl<sub>e</sub> 4<sub>:</sub> Att<sub>ac</sub>k <sub>accuracy o</sub>f R<sub>o</sub>F<sub>i</sub>R<sub>e an</sub>d b<sub>ase</sub>li<sub>ne mo</sub>d<sub>e</sub>l<sub>s</sub> under conce<sub>p</sub>t drift scenario, when N = 5.

<table><tr><td rowspan="2">Model</td><td colspan="3">Accuracy (%)</td></tr><tr><td>Week 1</td><td>Week 7</td><td>Week 13</td></tr><tr><td>RoFiRe ( $\mathcal{T} = 250$ )</td><td>43</td><td>34</td><td>31</td></tr><tr><td>RoFiRe ( $\mathcal{T} = 500$ )</td><td>44</td><td>36</td><td>32</td></tr><tr><td>RoFiRe ( $\mathcal{T} = 1000$ )</td><td>46</td><td>38</td><td>35</td></tr><tr><td>DF</td><td>3</td><td>3</td><td>3</td></tr><tr><td>LaserBeak</td><td>6</td><td>5</td><td>4</td></tr><tr><td>RF</td><td>6</td><td>5</td><td>5</td></tr><tr><td>CUMUL</td><td>37</td><td>30</td><td>26</td></tr><tr><td>k-FP</td><td>4</td><td>3</td><td>4</td></tr><tr><td>NetAugment</td><td>40</td><td>31</td><td>26</td></tr><tr><td>Swallow</td><td>6</td><td>4</td><td>5</td></tr></table>

Notably, the performance gap is most pronounced on GTT23, the only dataset with genuine Tor exit trafic, and on BigEnough, a synthetic dataset designed to more closely approximate real browsing behavior than DF or AWF. Both datasets exhibit the lowest class separability (F-ratio) among all evaluated datasets (see Section 4). These results highlight the robustness and strong generalization ability of RoFiRe across both genuine and synthetic trafic distributions with varying degrees of realism.

Results on CellShift-Transduced Traces. To better understand the attainable lower bound, we trained a classifier on GTT-Mon and evaluated it on CellShift-transduced versions of the same traces. In the CW setting $( N = 5 , \mathcal { T } = 1 , 0 0 0 )$ , we observed a 10% performance degradation. These results indicate that our exit-to-exit scenario serves as a performance upper-bound, though the gap is modest.

## 7.3 Conce<sub>p</sub>t Drift Ex<sub>p</sub>eriments

To evaluate the temporal robustness of WF models, we conduct concept drift experiments using the GTT-Mon-Drift dataset. We simulate temporal drift by introducing three training-testing gaps: one week, seven weeks, and 13 weeks, reflecting short-, medium-, and long-term temporal shifts in Tor trafic. All models are trained with $N = 5 ,$ while RoFiRe is additionally tested with $\mathcal { T } = 2 5 0 , 5 0 0 ,$ and 1, 000 to examine the efect of augmentation scale.

As summarized in Table 4, RoFiRe consistently outperforms all baselines across every temporal gap, exceeding NetAugment by up to 9% at T = 1, 000. While CUMUL and NetAugment show moderate resilience, other baselines struggle with accuracies below 6%.

While all models degrade over time, RoFiRe sufers the least degradation, maintaining substantially higher accuracy across all intervals and outperforming competitors even after 13 weeks. These results underscore both the severity of concept drift in real-world Tor trafic while validating the efectiveness of our augmentation and normalization in sustaining long-term generalization.

## 7.4 OW Results

We evaluate RoFiRe and baseline models in the OW setting using the GTT-Mon and GTT-Unmon datasets. Each model is trained as a 169-class classifier, consisting of 168 monitored sites plus one unmonitored class, but performance is reported in binary form us ing PR metrics, which measure the ability to distinguish monitored from unmonitored traces. Experiments are conducted with varying unmonitored set sizes (50K, 100K, 150K, 200K) and monitored sample counts of N ∈ {5, 10, 20} per class.

![](images/1905da2a9ad5178c5e2e9f9c21f5bda4a4d303228c21d6e8db491646434649b1.jpg)  
(a) Comparison with GTT-Week1

![](images/635a044b99e6a30eab64d373de038f15332c5867bdd9fc4608f44873a7a3a562.jpg)  
(b) Comparison with GTT-Month1

![](images/97158a347740ea30ee5f8c5749a58a791c7a64e0894fe613001dd97054edd816.jpg)  
(c) Comparison with GTT-Entire

![](images/32df83c8e89ab8172ebddbdbb298ed36626dd0aeff51a512848603a53f3d0256.jpg)

![](images/50a62883f238bb480881d1453eed1728a5789e36832ef9d4ef0af98f50dd782f.jpg)  
(a) 100K unmonitored in- (b) 200K unmonitored instances stances  
Figure 6: Per-class F1-scores (N = 20, T = 1000, and � = 0.2). Red bars denote hi<sub>g</sub>hl<sub>y</sub> fi<sub>ngerpr</sub>i<sub>n</sub>t<sub>a</sub>bl<sub>e c</sub>l<sub>asses.</sub>

Fi<sub>gure</sub> 5<sub>:</sub> R<sub>ea</sub>l OW <sub>resu</sub>lt<sub>s o</sub>f RoF<sub>i</sub>Re <sub>an</sub>d b<sub>ase</sub>li<sub>ne mo</sub>d<sub>e</sub>l<sub>s across</sub> dif<sub>eren</sub>t <sub>unmon</sub>i<sub>-</sub> tored set sizes when N = 20.  
![](images/69ae4fd0bc53f17e2d72020fbdca7e3895bfe3ef43a14f63dbc19f044d3496c8.jpg)

![](images/3082a2dd9d2ba0edc59b65bac6ea25e0ffcb416a2b038026c20fa1a3093a9013.jpg)  
(a) Comparison of models with $N = 1 0 .$ (b) Comparison of models with $N = 2 0 .$  
Fi<sub>gure</sub> 7<sub>:</sub> OW <sub>resu</sub>lt<sub>s</sub> <sub>o</sub>f RoF<sub>i</sub>Re <sub>an</sub>d b<sub>ase</sub>li<sub>ne</sub> <sub>mo</sub>d<sub>e</sub>l<sub>s</sub> <sub>across</sub> dif<sub>eren</sub>t <sub>unmon</sub>it<sub>ore</sub>d <sub>se</sub>t <sub>s</sub>i<sub>zes.</sub>

Traditional OW Setting. As shown in Figure 7, RoFiRe consistently outperforms DF and NetAugment across all unmonitored set sizes and N ∈ {10, 20}. However, precision for all models—including RoFiRe —drops as the unmonitored set expands, illustrating the dificulty of maintaining accuracy under growing class imbalance. Similar to prior WF studies, these experiments use arbitrarily fixed base rates that do not reflect real Tor trafic distributions. Because GTT23 preserves authentic trafic proportions, we further conduct experiments under its true base rates to assess real-world viability.

Realistic OW Evaluation. Previous studies have highlighted the base rate fallacy in WF, that is, reporting high true positive rates (TPR) without considering the real proportion of monitored sites in Tor trafic [21, 29]. In contrast, GTT23 captures the natural ratio of monitored to unmonitored traces, ofering a realistic and challenging benchmark. We evaluate three observation windows: GTT-Week1, GTT-Month1, and GTT-Entire. As the monitoring duration increases, the proportion of monitored trafic decreases, from about 6% (67 K of 1.07 M traces) in GTT-Week1 to 4% in GTT Month1 and 1% in GTT-Entire, reflecting the growing imbalance encountered in practice.

Figure 5 shows that RoFiRe consistently achieves superior PR curves compared to DF and NetAugment across all base-rate settings when N = 20; additional results for other N are reported in Appendix A.7. Even in the GTT-Entire scenario, RoFiRe maintains better PR tradeofs than both baselines, although absolute precision remains low (≈0.2 in the best case), which underscores the intrinsic dificulty of accurate WF in realistic OW conditions.

Specifically, Figure 6 shows that a non-trivial subset of sites (5– 7%) in GTT-Week1 maintains consistently high F1 scores, rendering them reliably identifiable despite the noise. Although the overall precision is 0.32, the burden decreases substantially when considering only sites with high per-class F1 scores. Precision reaches 0.8 for sites with F1 scores above 0.8, and targeting high-prevalence websites (e.g., the top-10 in GTT23 cover 48% of trafic [17]) further minimizes false positives. Crucially, this implies that low overall precision does not negate privacy risks. An attacker can efectively boost operational accuracy by narrowing the candidate set to such high-confidence targets or aggregating observations from multiple vantage points.

Lastly, we vary the �-cell threshold (� ∈ {10, 100, 1,000}) to study the trade-of between data retention and accuracy. CellShift [14] fixed � = 1,000, discarding nearly 70% of websites in GTT23. Although larger � harms realism by excluding short sessions, GTT23 also contains many circuits that are not full page transfers [17], so a higher threshold can heuristically target likely page loads. We therefore report results with and without filtering to avoid bias and expose operating-point trade-ofs.

As shown in Figure 12 and Table 8 of Appendix A.7, stricter thresholds raise per-trace precision but sharply reduce coverage and realism. Operationally, this threshold acts as a triage rule—classify only flows with at least � cells and abstain otherwise—so increasing � trades recall for precision; we quantify the resulting precision–recall curve on GTT23 (see Appendix A.7 for details).

Collectively, these findings indicate that while large-scale OW fingerprinting remains challenging, realistic attacks leveraging parallelized observation or target prioritization can still inflict serious privacy harm on a non-negligible fraction of web destinations.

## 8 C<sub>o</sub>n<sub>c</sub>l<sub>us</sub>i<sub>o</sub>n

By integrating RMS-based normalization and dynamic windowlevel augmentation, RoFiRe outperforms state-of-the-art WF baselines across various scenarios on realistic and synthetic datasets, demonstrating that WF remains feasible for a meaningful subset of real-world targets despite trafic variability and drift.

## A<sub>c</sub>k<sub>now</sub>l<sub>e</sub>d<sub>gmen</sub>t<sub>s</sub>

We thank our reviewers for helpful comments. This work was supported by the National Research Foundation of Korea(NRF) grant funded by the Korea government(MSIT) (No. RS-2025- 02263915, RS-2025-16071657).

## R<sub>e</sub>f<sub>erences</sub>

[1] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic website fingerprinting by augmenting network traces. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 1035–1049.

[2] Matthias Beckerle, Jonathan Magnusson, and Tobias Pulls. 2022. Splitting Hairs and Network Traces: Improved Attacks Against Trafic Splitting as a Website Fingerprinting Defense. In Proceedings ofthe 21st Workshop on Privacy in the Electronic Society (Los Angeles, CA, USA) (WPES’22). Association for Computing Machinery, New York, NY, USA, 15–27. doi:10.1145/3559613.3563199

[3] Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geofrey Hinton. 2020. A simple framework for contrastive learning of visual representations. In International conference on machine learning. PmLR, 1597–1607.

[4] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online website fingerprinting: Evaluating website fingerprinting attacks on tor in the real world. In 31st USENIX Security Symposium (USENIX Security 22). 753–770.

[5] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust Multi-tab Website Fingerprinting Attacks in the Wild. In 2023 IEEE Symposium on Security and Privacy (SP). 1005–1022. doi:10.1109/SP46215.2023.10179464

[6] Terrance DeVries and Graham W Taylor. 2017. Improved regularization of convolutional neural networks with cutout. arXiv preprint arXiv:1708.04552 (2017).

[7] Roger Dingledine, Nick Mathewson, and Paul F. Syverson. 2004. "Tor: The second-generation Onion router". In USENIX Security Symposium. 303–320.

[8] Kevin P Dyer, Scott E Coull, Thomas Ristenpart, and Thomas Shrimpton. 2012. Peek-a-boo, i still see you: Why eficient trafic analysis countermeasures fail. In 2012 IEEE symposium on security and privacy. IEEE, 332–346.

[9] Ronald A Fisher. 1936. The use of multiple measurements in taxonomic problems. Annals ofeugenics 7, 2 (1936), 179–188.

[10] Golnaz Ghiasi, Yin Cui, Aravind Srinivas, Rui Qian, Tsung-Yi Lin, Ekin D Cubuk, Quoc V Le, and Barret Zoph. 2021. Simple copy-paste is a strong data augmenta tion method for instance segmentation. In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition. 2918–2928.

[11] Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec, Pierre Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires, Zhaohan Guo, Mohammad Gheshlaghi Azar, et al. 2020. Bootstrap your own latent-a new approach to self-supervised learning. Advances in neural information processing systems 33 (2020), 21271–21284.

[12] Wolfgang Härdle and Léopold Simar. 2007. Applied multivariate statistical analysis. Springer.

[13] Jamie Hayes and George Danezis. 2016. k-fingerprinting: A robust scalable website fingerprinting technique. In 25th USENIX Security Symposium (USENIX Security 16). 1187–1203.

[14] Rob Jansen. 2026. CellShift: RTT-Aware Trace Transduction for Real-World Website Fingerprinting. In Network and Distributed System Security Symposium. doi:10.14722/ndss.2026.231004

[15] Rob Jansen and Nicholas Hopper. 2012. Shadow: Running Tor in a Box for Accu rate and Eficient Experimentation. In Network and Distributed System Security Symposium.

[16] Rob Jansen and Nicholas J Hopper. 2011. Shadow: Running Tor in a box for accurate and eficient experimentation. (2011).

[17] Rob Jansen, Ryan Wails, and Aaron Johnson. 2024. A measurement of genuine tor traces for realistic website fingerprinting. arXiv preprint arXiv:2404.07892 (2024).

[18] Rob Jansen, Ryan Wails, and Aaron Johnson. 2024. Repositioning Real-World Website Fingerprinting on Tor. In ACM Workshop on Privacy in the Electronic Society (WPES).

[19] Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, De vendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023. Mistral 7B. arXiv:2310.06825 [cs.CL] https: //arxiv.org/abs/2310.06825

[20] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Rachel Greenstadt. 2014. A critical evaluation of website fingerprinting attacks. In Proceedings ofthe 2014 ACM SIGSAC conference on computer and communications security. 263–274.

[21] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Rachel Greenstadt. 2014. A critical evaluation of website fingerprinting attacks. In Proceedings ofthe 2014 ACM SIGSAC Conference on Computer and Communications Security. 263–274

[22] Marc Juarez, Mohsen Imani, Mike Perry, Claudia Diaz, and Matthew Wright. 2016. Toward an eficient website fingerprinting defense. In Computer Security– ESORICS 2016: 21st European Symposium on Research in Computer Security, Heraklion, Greece, September 26-30, 2016, Proceedings, Part I 21. Springer, 27–46.

[23] Xiaofeng Mao, Gege Qi, Yuefeng Chen, Xiaodan Li, Ranjie Duan, Shaokai Ye, Yuan He, and Hui Xue. 2022. Towards robust vision transformer. In Proceedings ofthe IEEE/CVF conference on Computer Vision and Pattern Recognition. 12042–12051.

[24] Nate Mathews, James K Holland, Nicholas Hopper, and Matthew Wright. 2024. LASERBEAK: Evolving Website Fingerprinting Attacks with Attention and Multi-Channel Feature Representation. IEEE Transactions on Information Forensics and Security (2024).

[25] Nate Mathews, James K Holland, Se Eun Oh, Mohammad Saidur Rahman, Nicholas Hopper, and Matthew Wright. 2023. Sok: A critical evaluation of eficient website fingerprinting defenses. In 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 969–986.

[26] Se Eun Oh, Nate Mathews, Mohammad Saidur Rahman, Matthew Wright, and Nicholas Hopper. 2021. GANDaLF: GAN for Data-Limited Fingerprinting. Proceedings on Privacy Enhancing Technologies (PETS) 2021, 2 (2021), 305–322.

[27] Se Eun Oh, S Sunkam, and N Hopper. 2019. p-fp: Extraction, classification, and predication of website fingerprints. In Proc. ofPETS, Vol. 19.

[28] Se Eun Oh, Taiji Yang, Nate Mathews, James K Holland, Mohammad Saidur Rahman, Nicholas Hopper, and Matthew Wright. 2022. DeepCoFFEA: Improved flow correlation attacks on Tor via metric learning and amplification. In 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 1915–1932.

[29] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale.. In NDSS.

[30] Tobias Pulls. 2020. Towards efective and eficient padding machines for Tor. arXiv preprint arXiv:2011.13471 (2020).

[31] Yao Qin, Chiyuan Zhang, Ting Chen, Balaji Lakshminarayanan, Alex Beutel, and Xuezhi Wang. 2022. Understanding and improving robustness of vision transformers through patch-based negative augmentation. Advances in Neural Information Processing Systems 35 (2022), 16276–16289.

[32] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gangadhara, and Matthew Wright. 2020. Tik-Tok: The utility of packet timing in website fingerprinting attacks. Proceedings on Privacy Enhancing Technologies 2020, 3 (2020), 5–24.

[33] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. 2018. Automated Website Fingerprinting Through Deep Learning. In Proceedings 2018 Network and Distributed System Security Symposium. The Internet Society. doi:10.14722\/ndss.2018.23105 25th Annual Network and Distributed System Security Symposium, NDSS 2018 ; Conference date: 18-02-2018 Through 21-11-2018.

[34] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subverting website fingerprinting defenses with robust trafic representation. In 32nd USENIX Security Symposium (USENIX Security 23). 607–624.

[35] Meng Shen, Jinhe Wu, Junyu Ai, Qi Li, Chenchen Ren, Ke Xu, and Liehuang Zhu. 2025. Swallow: A Transfer-Robust Website Fingerprinting Attack via Consistent Feature Learning. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security. 1574–1588.

[36] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings ofthe 2018 ACM SIGSAC conference on computer and communications security. 1928–1943.

[37] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security. 1131–1148.

[38] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288 (2023).

[39] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective Attacks and Provable Defenses for Website Fingerprinting. In 23rd USENIX Security Symposium (USENIX Security 14). USENIX Association, San Diego, CA, 143–157.

[40] Tao Wang and Ian Goldberg. 2017. Walkie-Talkie: An eficient defense against passive website fingerprinting attacks. In 26th USENIX Security Symposium (USENIX Security 17). 1375–1390.

[41] Yixiao Xu, Tao Wang, Qi Li, Qingyuan Gong, Yang Chen, and Yong Jiang. 2018. A Multi-Tab Website Fingerprinting Attack. In Proceedings of the 34th Annual Computer Security Applications Conference (San Juan, PR, USA) (ACSAC ’18). Association for Computing Machinery, New York, NY, USA, 327–341. doi:10. 1145/3274694.3274697

[42] Junhua Yan, Hasan Faik Alan, and Jasleen Kaur. 2020. Fingerprinting Search Keywords over HTTPS at Scale. arXiv preprint arXiv:2008.08161 (2020).

[43] Biao Zhang and Rico Sennrich. 2019. Root mean square layer normalization. Advances in Neural Information Processing Systems 32 (2019).

[44] Qiang Zhou, Liangmin Wang, Huijuan Zhu, and Tong Lu. 2023. Few-shot website fingerprinting attack with cluster adaptation. Computer Networks 229 (2023), 109780. doi:10.1016/j.comnet.2023.109780

[45] Qiang Zhou, LiangMin Wang, HuiJuan Zhu, Tong Lu, and Victor.S Sheng. 2023. WF-Transformer: Learning Temporal Features for Accurate Anonymous Trafic identification by Using Transformer Networks. IEEE Transactions on Information Forensics and Security (2023), 1–1. doi:10.1109/TIFS.2023.331896

## A A<sub>pp</sub>endix

## A<sub>.</sub>1 T<sub>ra</sub>diti<sub>ona</sub>l W<sub>e</sub>b<sub>s</sub>it<sub>e</sub> Fi<sub>ngerpr</sub>i<sub>n</sub>ti<sub>ng</sub>

From Statistical Features to Deep Learning. The evolution of WF attacks began with traditional ML models using hand-crafted statistical features. Early examples include CUMUL [29], which used Support Vector Machines, and k-FP [13], which employed Random Forests. The paradigm shifted with DL, pioneered by Rimmer et al.’s AWF [33], which demonstrated how architectures like CNNs could automatically learn feature hierarchies from raw trafic. This led to highly efective 1D-CNN models such as DF [36] and Tik-Tok [32], which significantly outperformed prior methods and broke several contemporary WF defenses [22, 40].

Recent Architectural Innovations. Architectural innovations in DL-based models have driven further progress in WF. Beckerle et al. introduced Maturesc [2], an optimized ResNet variant that evaluated trafic-splitting defenses with a 2-channel input design. Zhou et al. proposed WF-Transformer [45], applying multi-head attention layers atop CNNs, while Deng et al.’s ARES [5] leveraged multi-headed self-attention for multi-tab WF [41]. Shen et al.’s Robust Fingerprinting (RF) [34] introduced the Trafic Aggregation Matrix (TAM), a statistical feature representation for 2D CNNs. Laserbeak [24] further advanced WF by combining Transformer architectures with multi-channel features, outperforming several earlier methods against padding defenses.

Data-Limited Fingerprinting and Augmentation. A major chal lenge for DL-based WF models is their dependence on large training datasets, which are impractical to collect and maintain for WF. The problem is exacerbated by "concept drift" [20], where website traf fic patterns evolve over time, degrading model performance and necessitating frequent, costly retraining. To address this, research has focused on developing data-eficient methods to reduce data requirements and re-training needs.

Early approaches like Triplet Fingerprinting [37] used metric learning with a triplet loss to learn a feature space where samples from the same website are clustered together, enabling efective few shot learning. Other strategies have employed generative models like GANs (GANDaLF [26]) to create synthetic training data or semi-supervised techniques like pseudo-labeling (CWFA [44]) to leverage unlabeled data.

Among the most prominent works, NetAugment [1] introduced a two-stage framework that combines data augmentation with self supervised contrastive learning. In the first stage, a feature extractor is pre-trained on a large, unlabeled dataset using SimCLR [3]. For each trafic trace, NetAugment generates two augmented "views" by applying transformations at the trafic burst level, such as split ting or delaying bursts. The model is then trained to maximize the agreement between views of the same trace while minimizing agreement between views of diferent traces. This process yields a powerful and generalized feature representation. In the second stage, the pre-trained model is fine-tuned for the final classification task using only a small number of labeled examples per website.

Swallow [35] improves transfer robustness against network heterogeneity and defenses by mitigating packet distribution shifts. It employs a tripartite framework: CIF for distribution alignment,

CIF-based time-interval-based augmentations, and BYOL [11] selfsupervised pre-training. This design ensures robustness against network shifts through eficient few-shot fine-tuning.

These techniques facilitate eficient learning from limited data and reduce reliance on large-scale datasets. This principle also serves as the foundation for our work.

## A<sub>.</sub>2 Ch<sub>a</sub>r<sub>ac</sub>t<sub>e</sub>ri<sub>s</sub>ti<sub>cs o</sub>f R<sub>ea</sub>li<sub>s</sub>ti<sub>c a</sub>nd S<sub>y</sub>nth<sub>e</sub>ti<sub>c</sub> Datasets

This section outlines GTT23’s key distinctions from prior WF datasets [4, 17, 25, 30, 33, 36], focusing on data realism, trafic granularity, browsing behavior, and circuit usage distributions, as summarized in Table 5.

Data Realism and Origin. GTT23 is the first dataset to capture genuine Tor user trafic directly from exit relays, reflecting real user behavior and network conditions. In contrast, prior WF datasets

– such as DF, AWF, GoodEnough, and BigEnough – are generated in controlled environments using automated crawlers or scripted browsing on virtualized clients, often with limited diversity in origins and usage patterns.

Trafic Granularity. As done by GTT23 (and previously by GoodEnough and BigEnough), trafic is captured at the Tor cell level rather than the TCP packet level, aligning with Tor’s protocol semantics. Early datasets such as DF and AWF rely on TCP packets, which have variable sizes that can unintentionally leak information and skew fingerprinting results. Fixed-size cell-level capture removes these packet size clues while preserving subtle signals such as cell order and timing, providing a more faithful foundation for evaluation.

Natural Browsing Behavior. While later WF datasets [25, 30] introduced diverse subpage visits and controlled Tor Browser security settings, GTT23 inherently captures a broader, more natural spectrum of real-world browsing behavior. Unlike existing datasets with diversity constrained to predefined subpages and fixed client configurations, GTT23 reflects authentic user configurations, destinations, and browsing habits across the Tor network, with approximately 80% of domains appearing only once.

Real-World Variability in Circuit Usage. Existing WF datasets often employ periodic circuit rotation, introducing artificial uniformity that deviates from natural Tor usage. In contrast, GTT23 preserves the natural distribution of circuits – like circuits of varying lengths – by capturing live trafic from real user sessions, introducing greater variability and providing a more challenging benchmark for WF models.

## A<sub>.</sub>3 St<sub>a</sub>ti<sub>s</sub>ti<sub>ca</sub>l C<sub>o</sub>m<sub>pa</sub>ri<sub>so</sub>n <sub>o</sub>f R<sub>ea</sub>li<sub>s</sub>ti<sub>c a</sub>nd S<sub>y</sub>nthetic Datasets

In this section, we discuss the additional characteristics of GTT23 and its key diferences compared to BigEnough. Table 6 shows the statistics in inter-cell delays (ICD) and the trace length.

ICD. ICD, the time between two consecutive cells, is a key characteristic of Tor trafic. As presented in Table 6, GTT23 traces exhibit significantly longer and more variable ICDs, with a mean of 0.84 seconds and a standard deviation of 5.27, compared to BigEnough’s

Table 5: Com<sub>p</sub>arison of Data Collection Methodolo<sub>g</sub>ies in WF Studies

<table><tr><td>Dataset</td><td>CW</td><td>OW</td><td>Page Scope</td><td>Distinctive Features</td><td>Collection Point</td><td>Data Format</td><td>TBB Version</td><td>Period</td></tr><tr><td>AWF [33]</td><td>900 sites × 2.5k tr.</td><td>400k traces</td><td>Index pages</td><td>15 VMs (private cloud); Time-gap data (200 sites × 500 tr.)</td><td>Entry Relay</td><td>TCP stream</td><td>TB v6.5; Tor v0.2.8.11</td><td>2017</td></tr><tr><td>DF [36]</td><td>95 sites × 1k tr.</td><td>100k traces</td><td>Index pages</td><td>10 phys. machines (acad. network)</td><td>Entry Relay</td><td>TCP stream</td><td>Not specified</td><td>2018</td></tr><tr><td>GoodEnough [30]</td><td>50 sites × 10 sub. × 20 tr.</td><td>10k traces</td><td>10 sub-pages/site</td><td>OW URLs from Reddit.com; 3 security modes tested</td><td>Entry Relay</td><td>Tor cell trace</td><td>TB v9.0.2</td><td>2020</td></tr><tr><td>BigEnough [25]</td><td>95 sites × 10 sub. × 20 tr.</td><td>19k traces</td><td>10 sub-pages/site</td><td>3 security modes tested</td><td>Entry Relay</td><td>Tor cell trace</td><td>TB v10.0.18</td><td>2021</td></tr><tr><td>Cherubin et al. [4]</td><td colspan="2">3.9M total traces</td><td>Full domains</td><td>Genuine exit traffic with hashed labels</td><td>Exit Relay</td><td>Tor cell trace</td><td>Unknown (real users)</td><td>2020-2021</td></tr><tr><td>GTT23 [17]</td><td colspan="2">13.9M total traces</td><td>Full domains</td><td>Genuine exit traffic with hashed labels</td><td>Exit Relay</td><td>Tor cell trace</td><td>Unknown (real users)</td><td>2023</td></tr></table>

Table 6: Statistical com<sub>p</sub>arison of Bi<sub>g</sub>Enou<sub>g</sub>h and GTT23.

<table><tr><td rowspan="2">Metric (median)</td><td colspan="2">Dataset</td></tr><tr><td>BigEnough</td><td>GTT23</td></tr><tr><td>Total Duration (s)</td><td>16.21</td><td>62.57</td></tr><tr><td>20 Cell&#x27;s Duration (s)</td><td>1.86</td><td>33.98</td></tr><tr><td>ICD Mean. (s)</td><td>0.03</td><td>0.84</td></tr><tr><td>ICD Std. (s)</td><td>0.34</td><td>5.27</td></tr><tr><td>Valid Cells (cnt)</td><td>680</td><td>72</td></tr><tr><td>Incoming Cells (cnt)</td><td>602</td><td>44</td></tr><tr><td>Outgoing Cells (cnt)</td><td>77</td><td>20</td></tr><tr><td>Cells /s (cnt)</td><td>36.30</td><td>1.21</td></tr><tr><td>Bursts (cnt)</td><td>47</td><td>9</td></tr></table>

0.03 seconds and 0.34, respectively. This variability reflects the di verse network conditions, circuit congestion, and user behaviors inherent in real-world Tor trafic.

Circuit Lengths. GTT23 contains a substantial number of traces (or circuits) with fewer than 10 cells. Specifically, as shown in Table 6, BigEnough traces have a median of 680 cells per trace (602 incoming, 77 outgoing) over 16.2 seconds, while GTT23 traces have a median of 72 cells over 62.57 seconds. Furthermore, many of these short traces exhibit similar patterns across diferent domains (i.e., classes).

## A<sub>.</sub>4 C<sub>o</sub>m<sub>pu</sub>t<sub>a</sub>ti<sub>o</sub>n<sub>a</sub>l C<sub>os</sub>t An<sub>a</sub>l<sub>ys</sub>i<sub>s</sub> <sub>o</sub>n A<sub>ug</sub>m<sub>e</sub>nt<sub>a</sub>ti<sub>o</sub>n S<sub>ca</sub>l<sub>e</sub>

In this section, we discuss the trade-of between augmentation scale and computational cost. Although larger M and T values increase computational costs, they can enhance data diversity, which can improve model generalization. Separating M and T allows finegrained control over the augmentation ratio per instance (M) and the overall data volume (T).

Figure 10 shows the impact of varying T with N = 5. Accuracy improves steadily up to $\mathcal { T } \approx 5 0 0$ , beyond which gains plateau, while computational costs grow sharply beyond M = 500. Based on these findings, we focus on M = 250, 500, 1000 in our experiments.

With N = 5 and M = 100, RoFiRe achieves a 10% accuracy improvement over the no-augmentation baseline, demonstrating the efectiveness of window-level augmentation for GTT23.

Table 7: CW experiment results in accuracy (%) of RoFiRe <sub>an</sub>d b<sub>ase</sub>li<sub>ne mo</sub>d<sub>e</sub>l<sub>s across</sub> $\mathcal { M } \in \{ 2 , 4 , . . . , 2 0 0 \}$ <sub>w</sub>h<sub>en</sub> $N = 5 .$

<table><tr><td rowspan="2">Model</td><td colspan="9"> $\mathcal{M}$ </td></tr><tr><td>2</td><td>4</td><td>8</td><td>10</td><td>20</td><td>50</td><td>100</td><td>150</td><td>200</td></tr><tr><td>RoFiRe</td><td>6</td><td>14</td><td>29</td><td>31</td><td>37</td><td>40</td><td>41</td><td>41</td><td>41</td></tr><tr><td>DF</td><td>4</td><td>8</td><td>11</td><td>13</td><td>19</td><td>25</td><td>28</td><td>31</td><td>31</td></tr><tr><td>LaserBeak</td><td>3</td><td>3</td><td>6</td><td>7</td><td>15</td><td>20</td><td>24</td><td>25</td><td>28</td></tr><tr><td>RF</td><td>6</td><td>14</td><td>20</td><td>20</td><td>22</td><td>20</td><td>20</td><td>21</td><td>21</td></tr></table>

T<sub>a</sub>bl<sub>e</sub> 8<sub>:</sub> St<sub>a</sub>ti<sub>s</sub>ti<sub>cs o</sub>f t<sub>o</sub>t<sub>a</sub>l <sub>c</sub>l<sub>ass coun</sub>t<sub>,</sub> i<sub>ns</sub>t<sub>ance coun</sub>t<sub>, an</sub>d <sub>per-c</sub>l<sub>ass</sub> i<sub>ns</sub>t<sub>ance</sub> <sub>coun</sub>t <sub>w</sub>h<sub>en</sub> <sub>vary</sub>i<sub>ng</sub> th<sub>res</sub>h<sub>o</sub>ld<sub>s.</sub>

<table><tr><td>Thresholds</td><td>Total Instances</td><td>Total Classes</td><td>Per Class Instances</td></tr><tr><td>original</td><td>13,900,621</td><td>1,343,841</td><td>10.3 (± 1830)</td></tr><tr><td>10</td><td>9,024,944</td><td>1,152,797</td><td>7.8 (± 615)</td></tr><tr><td>100</td><td>5,123,716</td><td>797,152</td><td>6.4 (± 425)</td></tr><tr><td>1000</td><td>2,303,931</td><td>402,438</td><td>5.7 (± 287)</td></tr></table>

Additionally, Table 7 shows that applying DyWin benefits not only our attack model but also other DL-based models (e.g., DF, LaserBeak, RF) as M increases, demonstrating the efectiveness of window-level augmentation on GTT23.

## A<sub>.</sub>5 C<sub>o</sub>m<sub>pu</sub>t<sub>a</sub>ti<sub>o</sub>n<sub>a</sub>l C<sub>os</sub>t An<sub>a</sub>l<sub>ys</sub>i<sub>s o</sub>n M<sub>o</sub>d<sub>e</sub>l

In this section, we evaluate the model complexity and computational cost of RoFiRe. RoFiRe achieves superior performance while maintaining a lightweight architecture in terms of both parameter count and computational cost. We evaluate model complexity using two metrics: parameter count and FLOPs (floating-point operations). FLOPs quantify the total number of computations required for a single forward pass, providing a hardware-agnostic measure of computational eficiency.

Figure 11 illustrates the trade-ofs between accuracy, parameter count, and FLOPs for all models. Each circle’s size represents the parameter count, while FLOPs are plotted on the x-axis and accuracy on the y-axis. Notably, RoFiRe achieves the highest accuracy with significantly fewer parameters and FLOPs than prior models.

NetAugment, which extends DF with a projection head for contrastive learning, has the largest parameter count and high FLOPs, reflecting its computational overhead. LaserBeak also exhibits a high computational footprint due to its attention-based architecture. In contrast, CUMUL, despite its lower complexity, falls short in performance. This demonstrates that RoFiRe strikes an efective balance between eficiency and accuracy, outperforming resourceintensive models like NetAugment without requiring additional projection heads or complex architectures.

![](images/99827bbc3b165dcee8e40d33e4b882c94d716e9e94043c1a416b90a92591c0f9.jpg)

![](images/32dcae432981fdd325d904c56d932151c2b52745e66ff28d592056e52342b8b9.jpg)

![](images/4bf7ec25ba52a08604050930a60894ad224d8e9489cc2e3349f80a494115ecdf.jpg)  
(a) Comparison with GTT-(b) Comparison with GTT-(c) Comparison with GTT-Week1 Month1 Entire

![](images/89748771f0a5280972c89f10a72efccaeadee24feb38b76f84d3f5502571cc7c.jpg)  
(a) Comparison with GTT-Week1  
(b) Comparison with GTT-Month1

![](images/cb66a4d3ddac49c975ad732f3d8bf6949f7a55f07ec58bbc29557fbe4ccb24e0.jpg)  
(c) Comparison with GTT-Entire

Fi <sub>u</sub>r<sub>e</sub> 8: R<sub>ea</sub>l OW r<sub>esu</sub>lt<sub>s o</sub>f RoFiRe <sub>a</sub>nd b<sub>ase</sub>lin<sub>e</sub> m<sub>o</sub>d<sub>e</sub>l<sub>s</sub> <sub>across</sub> dif<sub>eren</sub>t <sub>unmon</sub>it<sub>ore</sub>d <sub>se</sub>t <sub>s</sub>i<sub>zes w</sub>h<sub>en</sub> $N = 5$  
![](images/671fe57a21c4539af82f803d4931ee0d1ec389d919065900d7d9fbfe54ae67da.jpg)

![](images/2ae7541deef00d36da323dfb9953291b1a7c0b1013584c3f08e6134f625254e0.jpg)  
Fi<sub>g</sub>ure 10: Accurac<sub>y</sub> and com<sub>p</sub>utational <sub>cos</sub>t t<sub>ra</sub>d<sub>e-o</sub>f <sub>o</sub>f <sub>augmen</sub>t<sub>a</sub>ti<sub>on</sub> i<sub>n</sub> RoFiRe under var<sub>y</sub>in<sub>g</sub> T settin<sub>g</sub>s with $N = 5 .$

![](images/b7183cb04f3d34c092f22df84a592072d080eeabab713e6c0880957b314d2204.jpg)  
Fi<sub>g</sub>ure 11: Com<sub>p</sub>arison of RoFiRe and baseline models<sub>,</sub> in terms of FLOPs<sub>, p</sub>a-<sub>rame</sub>t<sub>ers, an</sub>d <sub>accuracy w</sub>h<sub>en</sub> $N = 9 0$ <sub>an</sub>d $\mathcal { T } = 1 0 0 0$

![](images/df2c5ac37fc07d2c3f1eb4d2a03059ee05de8642c3c20763aa56831e6cf5b1b2.jpg)  
Fi<sub>g</sub>ure 12: Real OW results of RoFiRe und<sub>er vary</sub>i<sub>ng</sub> t<sub>race-</sub>l<sub>eng</sub>th filt<sub>er</sub>i<sub>ng</sub> th<sub>res</sub>h<sub>-</sub> <sub>o</sub>ld<sub>s.</sub>

![](images/76ad643d0668f3d6d2e0143de52ae0308d2947c463f10167486d7dd8e100df0b.jpg)  
(a) Validation Loss.

![](images/006338d573ef29dd81fc75489096b833aba10a6f736c848477ec84b5c62b1493.jpg)  
(b) Training and Validation Accuracies.  
Fi <sub>u</sub>r<sub>e</sub> 9: R<sub>ea</sub>l OW r<sub>esu</sub>lt<sub>s o</sub>f RoFiRe <sub>a</sub>nd b<sub>ase</sub>lin<sub>e</sub> m<sub>o</sub>d<sub>e</sub>l<sub>s</sub> <sub>across</sub> dif<sub>eren</sub>t <sub>unmon</sub>it<sub>ore</sub>d <sub>se</sub>t <sub>s</sub>i<sub>zes w</sub>h<sub>en</sub> $N = 1 0$  
Fi<sub>g</sub>ure 13: Com<sub>p</sub>arison of DF and RoFiRe com<sub>p</sub>lexit<sub>y</sub> when $N = 9 0$ and without au<sub>g</sub>mentation.

## A.6 Stabilit<sub>y</sub> Anal<sub>y</sub>sis on Model

Compared to the CNN-based DF model, RoFiRe also demonstrates smoother convergence, lower validation loss, and reduced overfitting (Figures 13(a) and 13(b)). DF exhibits higher variance and stronger overfitting tendencies (red-shaded area), validating the stability improvements introduced by RMSNorm and pre-normalization.

## A.7 OW Base Rate Ex<sub>p</sub>eriments

Beyond the case of $N = 2 0 ,$ , realistic OW experiments were also conducted for $N = 5$ and $N = 1 0$ . Figure 8 and 9 illustrate as with the $N = 2 0$ setting, RoFiRe consistently outperforms other models across all cases; however, it still fails to surpass random guessing. These results indicate that in highly challenging scenarios – such as low base rate environments – the model’s performance significantly deteriorates when faced with extremely limited �-shot learning conditions.

In addition, cell-count filtering selects which traces are retained for training and evaluation. Unlike CellShift [14], which fixed the threshold at 1,000 cells, we sweep thresholds � ∈ {10, 100, 1,000} and measure both dataset coverage (classes and instances) and OW performance. As shown in Figure 12 and Table 8, stricter filtering raises per-trace precision and precision-recall AUC but sharply reduces coverage and realism, and drifts the natural base rate of GTT-Entire $( \pi = 0 . 0 1 0 6 1 1 )$ . To control for base-rate shifts, we fix both class and instance counts: train on 62 monitored classes (20 traces each) plus 20 unmonitored traces, and test on the same 62 monitored classes (100 traces each) with 578,096 unmonitored traces. This yields a deliberately small training set – more challenging yet far less resource-intensive for an attacker than the CellShift setup [14]. At low-recall operating points (recall≤ 0.15), performance improves as the cell-threshold � increases.

A cell threshold acts as a minimum-evidence triage: higher � yields cleaner signals but fewer opportunities. Let $C ( \tau ) = \mathrm { P r } [ C _ { t } \geq$ �] denote coverage, with recall $R ( \tau )$ , false-positive rate $F ( \tau )$ , and base rate �. Then $\mathrm { P r e c } ( \tau ) = \frac { \pi R ( \tau ) } { \pi R ( \tau ) + \left( 1 - \pi \right) F ( \tau ) }$ . Increasing � typically decreases �(�) and $R ( \tau )$ while reducing $F ( \tau )$ , producing precision gains at the cost of coverage and representativeness.
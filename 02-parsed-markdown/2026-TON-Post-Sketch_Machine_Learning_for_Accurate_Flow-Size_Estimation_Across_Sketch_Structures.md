# Post-Sketch Machine Learning for Accurate Flow-Size Estimation Across Sketch Structures

Aayush Karki , Dimitrios Melissourgos , Member, IEEE, Zhe Jiang , Senior Member, IEEE, Shigang Chen , Fellow, IEEE, and Haibo Wang , Member, IEEE

Abstract—Accurate flow-size measurement is essential for network management, yet the tight memory and timing constraints of network switches make exact per-flow counting infeasible. Sketches (compact probabilistic data structures that aggregate packet counts into shared counters) are the dominant solution, but their hand-crafted query rules introduce systematic estimation errors. Machine learning can correct these errors, but most existing approaches either require modifying the online recording pipeline, which is incompatible with production deployments, or is limited to a single sketch type. We present Post-Sketch Machine Learning (PS-ML), a generalized framework in the same zero-modification paradigm. PS-ML uses only the counter values already stored in the sketch. When a flow is queried, its k counter values encode its collision environment, but handcrafted rules discard this information by reducing them to a single scalar. PS-ML retains this information through a twostage model: a Random Forest classifier routes each query to a flow-size bin, and a bin-specific neural network regressor then produces a refined estimate. This design accounts for the qualitatively diferent noise regimes of small and large flows. Synthetic data augmentation addresses the scarcity of largeflow training examples. PS-ML is sketch-agnostic and works with typical flow size sketch structures. We evaluate PS-ML across eleven sketch implementations using real Internet trafic traces. PS-ML reduces estimation error by up to 90.7% and by 50.2% on average over the raw sketch, outperforms state-of-theart full-flow measurement sketches in estimation accuracy, and demonstrates temporal and cross-domain robustness by consistently reducing raw-sketch estimation error without retraining.

Index Terms—Flow-size measurement, network trafic, postsketch machine learning, zero online modification.

## I. INTRODUCTION

N <sup>ETWORK</sup> <sup>operators</sup> <sup>must</sup> <sup>continuously</sup> <sup>answer</sup> <sup>a</sup> <sup>decep-</sup> tively simple question: how large is each flow traversing the network? The answer drives critical decisions across trafic engineering, congestion control, billing, security monitoring, and anomaly detection [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]. By definition, a flow groups all packets sharing the same value in a designated header field (e.g., the source-destination IP pair or five-tuple), called the flow label, and its flow size—the total number of constituent packets—is the primary metric consumed by network management systems. Inaccurate flow-size estimates translate directly into misallocated bandwidth, undetected intrusions, and billing errors; these consequences compound as link speeds reach hundreds of gigabits per second and trafic distributions grow increasingly heterogeneous.

Accurate measurement requires extracting a flow label from every packet and updating measurements in real time—a task that must complete within nanoseconds at line rate. Network switches must simultaneously run packet forwarding, routing lookups, and access-control logic on the same limited on-chip SRAM; flow measurement competes for whatever memory remains, typically a few megabytes for tens of millions of simultaneous flows. Exact per-flow counting is infeasible under these constraints, which has driven decades of research into sketches—compact probabilistic data structures that achieve approximate flow-size measurement using sublinear memory by hashing multiple flows into shared counters [13], [14], [15], [16]. A sketch maintains k arrays of w counters; each arriving packet hashes its flow label to one counter per array and increments it. At query time, the k counter values are aggregated using a hand-crafted rule—minimum, median, or sum—to produce the estimate. This design enables line-rate recording within commodity switch memory, making sketches the dominant paradigm for production network measurement.

Despite decades of refinement—through sophisticated counter structures [17], [18], [19], [20], [21], specialized architectures for elephant flows [22], [23], and layered sketch organizations [24], [25]—a fundamental accuracy ceiling persists. The root cause lies in what hand-crafted query rules discard. Each rule—minimum, median, or sum—reduces the full k-dimensional counter vector to a single scalar, losing the distributional shape of those k values. That shape encodes the collision environment of the queried flow: when counters are uniformly low the sketch is lightly loaded and the minimum is reliable; when one counter is sharply elevated relative to the rest a specific heavy flow is causing localized collision; when all counters are uniformly large the sketch is globally saturated. These regimes demand qualitatively diferent corrections, yet no single statistic can distinguish them. By training on the full k-dimensional counter vector, a model learns to map each observed shape to the appropriate correction—exploiting information every hand-crafted rule unconditionally discards.

Machine learning has been integrated into sketches along two paradigms. Learning-as-filter methods [26], [27], [28], [29], [30] interpose a learned classifier within the recording pipeline to route packets to specialized counter regions; this demands real-time ML inference in the data plane, consuming scarce resources such as TCAM entries already exhausted by forwarding and security functions. Learning-as-equationsolver methods [24], [31], [32], [33], [34], [35] treat counter values as a system of linear equations and apply ML to reconstruct flow sizes; however, this requires a separate flowenumeration structure running online, consuming additional memory and introducing per-packet overhead. Both paradigms mandate changes to the online recording pipeline—infeasible in production where line cards operate under nanosecond timing budgets and the recording module is embedded in proprietary switching ASICs whose firmware cannot be updated independently of hardware refresh cycles measured in years, not software releases.

RatioSketch [36] pioneered zero-modification post-sketch ML, demonstrating that accurate correction is achievable without touching the online path. However, as we analyze in Section III, RatioSketch has three significant limitations. First, it relies on global counter sampling to estimate background noise, producing statistically unstable load estimates. Second, it applies a single correction model across the entire flow-size distribution, failing to account for the qualitatively diferent noise regimes that small and large flows inhabit. Third, its correction module is tightly coupled to the Count-Min sketch structure—specifically to the sorted d-counter vector and the ratio $\nu _ { j } / \nu _ { 0 }$ meaningful only for MIN-oriented sketches—and does not generalize to MEDIAN- or SUMoriented sketches. This paper advances that paradigm through Post-Sketch Machine Learning (PS-ML), a sketch-agnostic framework that resolves all three limitations.

PS-ML operates as a drop-in replacement for the sketch’s query function. Each sketch continues recording exactly as designed—no additional filters, no flow-label tracking, no inference at line rate. Only at query time does PS-ML intercept the k counter values, apply a trained model, and return the refined estimate, making adoption a management-plane software change compatible with any deployed sketch regardless of type, vendor, or generation. To handle Internet trafic’s heavily skewed flow-size distribution—where training a single model leads to dominant range bias collapsing predictions toward mice flows—PS-ML uses a two-stage architecture: a Random Forest classifier assigns each query to a flow-size bin, then a bin-specific neural network regressor trained on synthetic-augmented data provides precise estimates within that regime. This simultaneously maintains mice-flow accuracy (critical for DDoS and scan detection) and elephant-flow accuracy (critical for provisioning and billing). Our contributions are summarized as follows:

• We introduce PS-ML (Figure 3), a sketch-agnostic advancement of the zero-modification post-sketch ML paradigm pioneered by RatioSketch [36]. Where RatioSketch is tightly coupled to the CountMin sketch structure, PS-ML provides a general framework that operates across MIN-, MEDIAN-, and SUM-oriented sketches and their memory-eficient variants. PS-ML further addresses two concrete modeling limitations of RatioSketch: unreliable global noise estimation and a single-model bias across the flow-size distribution.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/0009d473993a4caaeba6d46844f49677c2a08a2371fede281ebde878f7663c2f.jpg)

Fig. 1. Average absolute error (AAE; lower is better) of CM and RatioSketch on CAIDA15 at a 5 MB memory budget. All 60 CAIDA15 traces are aggregated and flows are split 50/50 at random. We group flows into five flow-size ranges and compute AAE for each range. Results are calculated from a single run (one trained model, one hash seed).  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/f848c03123baa6ab163e94798300cab94ef88aca4f4d80a99adade660deac438.jpg)

Fig. 2. Coeficient of variation (CV%; lower is better) of the mean of the sampled counters from a CM sketch, versus sample size s, at memory budgets of 512 KB, 2 MB, and 10 MB. Data set used is CAIDA15. CV% is the standard deviation of the sampled mean, divided by the true mean of all counters. The results are calculated from 200 independent trials.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/51df0f65ea1f2417c669b0166d981c792fef122049f6ade28d1530d49a63cc19.jpg)  
Fig. 3. Overview of the PS-ML framework. We use the statistical feature obtained from k mapped counters to capture the unique collision pattern (which is the source of background noise) for each flow, avoiding the assumption that the noise distribution for each flow is identical. In the figure, “cold flows” denote the small-flow bin ([1 τ)) and “hot flows” denote the large-flow bin ([τ ∞)), each routed to a bin-specific regressor.

We design and validate a two-stage architecture combining Random Forest classification for flow-size-range categorization with specialized neural network regressors. We develop a synthetic data augmentation technique to address flow-size imbalance, and engineer features that extract maximum information from k candidate estimates produced by diverse sketch structures.

Through comprehensive experiments across eleven sketch implementations on real Internet trafic traces, we demonstrate that PS-ML reduces estimation error by up to 90.7% and by 50.2% on average over raw sketches, transfers robustly across time (CAIDA15 →CAIDA19) and across domains (MAWI→CAIDA15) without retraining, and achieves classification accuracy for heavy-hitters and top-k flows comparable to specialized sketches.

## II. PRELIMINARIES

## A. System and Flow Model

Flow-size measurement systems split into two tiers. The online recording module is embedded in the data plane of network devices—routers, switches, and gateways—and must process every arriving packet at line rate under severe resource constraints: limited on-chip SRAM (typically a few megabytes) shared with packet forwarding, routing lookups, and access-control logic, and nanosecond per-packet budgets. Sketches are deployed here because they achieve approximate measurement within these tight constraints. The measurements accumulated in on-chip memory are periodically ofloaded to the ofline query module, deployed on a remote server with abundant computational resources, large memory, and no real-time constraints; it stores historical measurement data, aggregates across time windows, and serves flow-size queries to network management applications. This separation is a fundamental architectural constraint: the online module cannot be modified without hardware-level changes to the switching ASIC, whereas the ofline module is freely programmable software.

We model the trafic as a packet stream $\boldsymbol { S } = ( e _ { 1 } , e _ { 2 } , \ldots , e _ { N } )$ of N packets in arrival order, where each packet $e _ { t }$ carries a flow label—typically the source-destination IP pair or fivetuple—identifying the flow it belongs to. The n distinct flows in $s$ form the flow domain $\mathcal { F } = \{ f _ { 1 } , f _ { 2 } , \ldots , f _ { n } \}$ . The flow size $n _ { f _ { i } }$ of flow $f _ { i }$ is the number of packets in $s$ with label $f _ { i } ,$ i.e., $n _ { f _ { i } } = \lvert \{ t : e _ { t }$ belongs to $\begin{array} { r } { r } { f _ { i } \} \Big | , \quad \bar { \sum } _ { i = 1 } ^ { n } n _ { f _ { i } } = N . } \end{array}$

## B. Hand-Crafted Sketches for Flow-Size Estimation

Sketches have been extensively studied over decades to measure flow size approximately while requiring only sublinear memory relative to the number of distinct flows. The sketch structure $C$ can be generalized as k arrays of w counters each. Let the jth counter in the ith array be $C _ { i } [ j ]$ , with $0 \leq i < k$ $0 \leq j < w$ . In each ith array, there is a uniform hash function $H _ { i } ( \cdot ) \in [ 0 , w - 1 ]$ to map any flow $f$ to a counter $C _ { i } [ H _ { i } ( f ) ]$ Sketches difer primarily in how they update counters upon each arriving packet and aggregate counter values during queries. There are three major categories:

MIN-oriented sketch structures include CountMin (CM) [13] and CountMin with Conservative Update (CU) [14]. CM hashes each flow $f$ to k counters and increments all k hashed counters by one upon each arriving packet from that flow. Because diferent flows share counters randomly through hash collisions, each counter accumulates noise from colliding flows. To estimate the flow size, CM returns the minimum value among the k counters: $\begin{array} { r } { \hat { n } _ { f } ~ = ~ \operatorname* { m i n } _ { 0 \leq i < k } C _ { i } [ H _ { i } ( f ) ] } \end{array}$ . The minimum carries the least collision noise. CU improves over CM by only incrementing the smallest counter(s), but still performs k memory accesses per query.

MEDIAN-oriented sketch structures are represented by Count Sketch (CS) [15]. CS uses k arrays of w counters, hashing flow $f$ to one counter in each array. CS updates each hashed counter $C _ { i } [ H _ { i } ( f ) ]$ by either increasing its value by one (if $h _ { i } ^ { b } ( f ) ~ = ~ 1 )$ or decreasing by one (if $h _ { i } ^ { b } ( f ) ~ = ~ - 1 )$ , depending on the binary hash value $h _ { i } ^ { b } ( f ) \in \{ 1 , - 1 \}$ , upon each arriving packet from flow $f .$ Due to hash collisions, counters may be shared with other flows, but since packets from other flows randomly increase or decrease the counter with equal probability, the expected impact is zero. Each counter’s value after multiplying by $h _ { i } ^ { b } ( f )$ is an unbiased estimate of the flow size, and CS returns the median value as the final estimate: $\hat { n } _ { f } ~ = ~ \mathrm { M e d i a n } _ { 0 \le i < k } h _ { i } ^ { b } ( f ) C _ { i } [ H _ { i } ( f ) ]$ . The median minimizes variance across the k estimates.

SUM-oriented sketch structures include Randomized Counter Sharing (RCS) [16], [37] and SSVS [38]. These sketches perform a single counter update per packet rather than $k ,$ pursuing k times faster online recording to match line rates in high-speed networks. RCS maps each flow $f$ to $k$ counters but only randomly selects one to increment for each arriving packet from flow $f .$ Essentially, packets of flow $f$ are evenly split into $k$ subsets, each mapped to one counter. Therefore, each counter stores only a fraction $\frac { 1 } { k }$ of the flow size, and the sum of the $k$ counters (minus average noise) provides the estimate. SSVS similarly updates one counter per packet but randomly increases or decreases it with equal probability, producing unbiased estimates when summed.

Memory-eficient counters have been proposed to replace regular counters in sketch structures [17], [18], [19], [20], [21], [39], [40]. Active counters (AC) [17] split bits into a number part v and an exponent part r, representing value $\nu \times 2 ^ { r }$ , incrementing probabilistically based on the exponent. Self-adjusting counters (SC) [20] begin as 8-bit regular counters and merge with neighbors when overflowing to create larger counters. Combining these with base sketch structures produces variants like CM-AC, CM-SC, CU-SC, CS-AC, CS-SC, and RCS-AC, which achieve better memory eficiency.

Specialized sketches for large flows include Heavy-Guardian [22], HeavyKeeper [23], Lossy Counting [41], Tight-Sketch [42], and Bubble Sketch [43]. These methods are specifically designed to identify top-k flows with the largest flow sizes or detect heavy hitters whose flow sizes exceed a predefined threshold.

Layered sketch structures, such as Pyramid Sketch [25] and Counter Braids [24], employ hierarchical counter organizations that difer fundamentally from the flat d × w array model of MIN/MEDIAN/SUM-oriented sketches. Their multilevel designs are tailored to specific measurement objectives (e.g., high-accuracy large-flow estimation or lossless per-flow counting) and do not expose a uniform set of $d$ candidate counter values for a queried flow.

## C. Neural Sketches: Modifying Online Recording

Recent work has explored integrating machine learning to overcome limitations of hand-crafted sketches. These approaches fall into two categories. Learning-as-filter sketches [26], [27], [28], [29], [30] deploy ML models (typically decision trees) directly in the online recording pipeline to classify incoming packets as belonging to elephant or mice flows at line rate, directing them to specialized sketches. While achieving accuracy improvements, they require highspeed inference using scarce hardware resources (e.g., TCAM entries) and continuous access to live packet streams for model updates. Learning-as-equation-solver sketches [24], [31], [32], [33], [34], [35] assume complete knowledge of all active flow keys and formulate sketch measurements as systems of equations, applying ML techniques to infer flow sizes. They require additional modules (e.g., Bloom filters) to track flow keys, consuming substantial memory and introducing perpacket overhead.

More recently, fully neural sketch architectures have emerged. MetaSketch [44] reformulates sketch operations as diferentiable memory accesses using Memory-Augmented Neural Networks (MANNs), training on synthetic Zipf distributions for cross-domain generalization. However, it sufers from high training costs, poor scalability due to fixedsize memory blocks, and high inference latency requiring full MANN forwarding. LegoSketch [45] introduces modular memory blocks for elastic scaling and normalized multihashing for zero-shot transfer, improving scalability and accuracy. However, its block-based architecture incurs high inference costs, performs poorly on highly skewed distributions, and requires expensive memory scanning operations.

## D. RatioSketch: First Solution With Zero Online Modification

RatioSketch [36] pioneers the zero-modification paradigm by building a correction module entirely at query time, leaving the online recording pipeline untouched. For a queried flow $f ,$ a CM sketch with k rows and w counters per row provides k hashed counter values $\nu _ { j } ~ = ~ C _ { j } [ H _ { j } ( f ) ]$ where each $\nu _ { j }$ overestimates the true flow size $n _ { f }$ by the collision noise $\begin{array} { r } { X _ { j } = \sum _ { f ^ { \prime } \neq f : H _ { j } ( f ^ { \prime } ) = H _ { i } ( f ) } n _ { f ^ { \prime } } } \end{array}$ from co-located flows. The standard CM estimate is the minimum $\nu _ { 0 } = \operatorname* { m i n } _ { j } \nu _ { j } .$ . RatioSketch learns a correction coeficient $C \in [ 0 , 1 ]$ to produce a refined estimate $\hat { n } _ { f } = C \cdot \nu _ { 0 }$ . Since $C \leq 1$ , the correction always reduces the CM overestimate toward the true flow size. C is inferred by a neural network from two inputs: (1) Local encoder: the k hashed counter values $\mathbf { v } = [ \nu _ { 1 } , \ldots , \nu _ { k } ]$ of the queried flow, capturing its specific collision environment; (2) Global encoder: the first 64 counters in each row of the counter matrix, normalized by $N ,$ characterizing the sketch-wide background load. RatioSketch is trained with a log-size-weighted loss that applies heavier penalties for large-flow errors: RatioL $\begin{array} { r } { \cos = \frac 1 n \bar { \sum _ { i = 1 } ^ { n } } \log _ { 2 } ( n _ { f _ { i } } + } \end{array}$ $\begin{array} { r } { 1 ) \cdot \left| \frac { \hat { n } _ { f _ { i } } } { \nu _ { 0 } ^ { i } } - \frac { n _ { f _ { i } } } { \nu _ { 0 } ^ { i } } \right| . } \end{array}$

## III. LIMITATIONS OF RATIOSKETCH AND MOTIVATION FOR PS-ML

## A. Performance Limitation of RatioSketch

Figure 1 compares the average absolute error (AAE) of CM and RatioSketch across five flow-size ranges on the CAIDA dataset at 5 MB memory (the dataset and experimental setup are detailed in Section VII). Since CM only produces non-negative errors (it exclusively overestimates), AAE is equivalent to the average bias per range. RatioSketch achieves a 72.3% error reduction for small flows in [1 10) but provides diminishing improvement as flow size increases, falling to only 2.1% for large flows in $[ 1 0 ^ { 4 } , \infty )$ . This reveals the performance limitation of RatioSketch: the learned coeficient C is an efective measure of collision noise for small flows but loses its corrective power for larger flows. We identify two root causes for this failure.

Before analyzing them, we first characterize the noise structure of CM that C must correct. Note that the following two propositions and the subsequent remark establish the mathematical foundation for understanding the noise distribution and its flow-size dependence. Skipping them will not afect the flow of this section.

Proposition 1 (CM Collision Noise): For a Count-Min Sketch with d rows and w columns using pairwise-independent hash functions, the collision noise $\begin{array} { r } { X _ { j } = \sum _ { k : h _ { j } ( f _ { k } ) = h _ { j } ( f _ { i } ) , k \neq i } n _ { f _ { k } } } \end{array}$ at row $j$ for flow $f _ { i }$ satisfies $\begin{array} { r } { \mathbb { E } [ X _ { j } ] ~ = ~ \frac { N - n _ { f _ { i } } } { w } } \end{array}$ . Consequently, the CM estimate $\nu _ { 0 } = n _ { f _ { i } } + X _ { ( 1 ) }$ is always non-negatively biased $( \mathbb { E } [ \nu _ { 0 } ] \geq n _ { f _ { i } } )$ , and $\begin{array} { r } { \mathbb { E } [ \nu _ { 0 } ] \leq n _ { f _ { i } } + \frac { N - n _ { f _ { i } } } { w } } \end{array}$

The proof is deferred to the supplementary material.

Proposition 2 (Flow-Size-Dependent Relative Error): Under the same conditions as Proposition 1, the expected relative estimation error satisfies:

$$
\mathbb {E} \bigg [ \frac {v _ {0} - n _ {f _ {i}}}{n _ {f _ {i}}} \bigg ] \leq \frac {N - n _ {f _ {i}}}{n _ {f _ {i}} \cdot w}\tag{1}
$$

This bound is strictly decreasing in $n _ { f _ { i } } .$ . Defining the signalnoise crossover threshold as $n _ { f } ^ { * } ~ = ~ N / ( w + 1 )$ . If $n _ { f _ { i } } ~ < ~ n _ { f } ^ { * } ;$ expected relative error exceeds 1 (noise-dominated regime), and aggressive correction is required. Otherwise, the expected relative error is at most 1 (signal-dominated regime), and only mild correction is needed.

The proof is deferred to the supplementary material.

Remark 1: Proposition 2 provides a theoretical justification for flow-size-based binning: flows on either side of $n _ { f } ^ { * }$ require qualitatively diferent correction strategies. The operational threshold of $\tau = 1 0 { , } 0 0 0$ in PS-ML is chosen to align with the heavy-hitter detection task (flows with $n _ { f _ { i } } ~ \ge ~ \tau$ are the targets of downstream queries), rather than at the theoretical crossover $n _ { f } ^ { * }$ , which depends on sketch size.

Proposition 2 establishes that the relative error of CM decreases sharply with flow size, yet Figure 1 shows its absolute AAE is roughly consistent across ranges. To illustrate: a flow of size $n _ { f _ { i } } = 5$ with collision noise $X _ { ( 1 ) } = 2 0 0$ sufers 4000% relative error, while a flow of size $n _ { f _ { i } } = 5 0 { , } 0 0 0$ with the same noise incurs only 0.4%. RatioSketch’s multiplicative correction $\hat { n } _ { f } = { C } \cdot \nu _ { 0 }$ applies the same relative-scale shrinkage to all flows: the C that aggressively corrects a noise-dominated small flow would leave an already-accurate large flow nearly unchanged. This fundamental mismatch between a uniform correction and a highly non-uniform error landscape motivates us to examine two root causes.

## B. Root Cause 1: Unreliable Background Noise Estimation via Counter Sampling

RatioSketch’s Global Encoder characterizes the background sketch load by sampling only the first 64 counters in each row. However, 64 counters per row is statistically insuficient to stably represent the full counter distribution. To quantify this, we compute the Coeficient of Variation (CV% = std/mean × 100) of the 64-counter sampled mean across 200 independent trials on the CAIDA training set under three memory sizes.

As Figure 2 shows, at 64 samples the CV% is 25% at 512 KB, 51% at 2 MB, and 110% at 10 MB. The CV% does not converge to a stable level until the sample size reaches 1024 or even 2048 counters. The load estimate load fed into the Global Encoder therefore carries substantial variance, undermining the reliability of the background noise characterization. We attribute RatioSketch’s choice of 64 counters to a practical constraint: training and inference time increases drastically as more counters are sampled, making 1024 or 2048 operationally impractical for the RatioSketch model. As a result, the global encoder introduces noise into the C prediction for all flow sizes, and especially degrades corrections for medium and large flows where the actual relative collision noise is already small.

## C. Root Cause 2: Flow-Size Imbalance in the Training Distribution

The second root cause is the heavily skewed distribution of Internet flows. Most flows are small (mice), while medium and large flows are exponentially fewer in number [46]. This imbalance means the training data that RatioSketch processes is dominated by small-flow examples. During training, gradient updates are driven predominantly by the large number of small-flow samples, causing the model to put more weight on correcting the high collision noise experienced by small flows while neglecting the smaller, structurally diferent noise of medium and large flows.

Although RatioSketch’s RatioLoss applies a log-size weighting to penalize large-flow errors more heavily, in practice the sheer count imbalance dominates and the learned C remains tuned for the small-flow noise regime. Concretely, this means RatioSketch implicitly assumes that the same relative correction based on v is appropriate for flows of all sizes. But as Proposition 2 shows and Figure 1 confirms, the relative error of CM is not consistent across flow sizes. A C shaped by small-flow examples cannot simultaneously provide the aggressive downward correction needed for noise-dominated small flows and the near-identity correction appropriate for signal-dominated large flows.

Both root causes share the same structural flaw: RatioSketch applies a single, flow-size-blind correction model to a distribution where the error regime changes dramatically with flow size. What is needed is an approach that treats flows of diferent sizes diferently — both in how the training data is handled and in how the correction is applied.

## D. Generalizing Beyond Count-Min Sketch

Beyond addressing RatioSketch’s two performance limitations, PS-ML is designed to generalize across the full family of hand-crafted sketch structures described in Section II-B. RatioSketch is tightly coupled to the Count-Min sketch: its correction $\hat { n } _ { f } = { C } \cdot \nu _ { 0 }$ with $C \in [ 0 , 1 ]$ encodes the assumption that the sketch always overestimates, so correction can only reduce the estimate. This assumption holds for CM and CU (MIN-oriented), where every counter accumulates only nonnegative collision noise. It does not hold in general.

MEDIAN-oriented sketches (e.g., Count Sketch) use a signed update rule: each counter is incremented or decremented by a random binary hash, so the expected collision noise from other flows cancels out. However, the noise does not cancel perfectly in finite streams: a queried counter can be either above or below the true flow size depending on the specific random hash assignments in the current stream.

The sketch estimate (the median across rows) is unbiased in expectation but individual counter values can underestimate the true flow size, meaning a correction $C > 1$ may be needed.

SUM-oriented sketches (e.g., RCS, SSVS) split each flow’s packets across k counters, so each counter holds approximately 1/k of the true count. After scaling by $k ,$ the resulting estimate can also fall below the true value due to uneven packet splits and noise from shared counters. Again, $C \ > \ 1$ would be required to correct underestimates.

In both cases, restricting the correction to $C \in [ 0 , 1 ]$ would systematically prevent accurate correction for these sketch types. A truly sketch-agnostic solution must therefore make no assumption about the sign or scale of the correction — the sketch error must be treated as an open-ended regression problem rather than a bounded shrinkage applied to a single baseline estimate.

## E. From Limitations to Design: The PS-ML Approach

The three observations above converge on a key insight: the k counter values of a queried flow encode both the collision noise and the flow’s approximate magnitude. A large flow yields uniformly large counter values; a small flow yields uniformly small ones. This means the same feature vector that drives the correction also carries enough signal to reveal which noise regime the flow belongs to — making regimeaware correction not only desirable but naturally realizable from information already present in any sketch.

This motivates a two-stage query pipeline where the first stage classifies the queried flow into a flow-size regime and the second stage applies a regime-specific corrector. This design addresses all three limitations by construction. First, each regime-specific model is trained exclusively on its own flowsize range, breaking the small-flow dominance that biases a single global model. Second, the features are drawn solely from the k counter positions relevant to the queried flow — no background counter sampling, no global load estimation, no additional inference time overhead. Third, each corrector directly predicts the flow size from counter values without constraining the direction or magnitude of the correction, so the same approach works unchanged for MIN-, MEDIAN-, and SUM-oriented sketches. The details of this architecture are presented in Section V.

## IV. FEATURE EXTRACTION AND DATA PREPROCESSING

The efectiveness of any machine learning approach depends critically on feature quality. PS-ML operates exclusively on sketch measurements without access to raw packet streams, making feature engineering essential. This section describes how we extract informative features from diverse sketch structures and prepare them for model training.

## A. Extracting Candidate Estimates From Sketch Measurements

Sketches generally consist of k arrays of w counters each. Let $C _ { i } [ j ]$ denote the jth counter in the ith array, with $0 \leq i < k$ and $0 \leq j < w$ . Each array uses a uniform hash function $H _ { i } ( \cdot ) \in$ $[ 0 , w - 1 ]$ to map any flow f to a counter $C _ { i } [ H _ { i } ( f ) ]$ . After the sketch completes recording, we extract k candidate flow-size estimates from these k hashed counters. The extraction method depends on the sketch type.

1) MIN-Oriented Sketches (CM, CU): Each arriving packet from flow $f$ increments all k hashed counters. Every counter accumulates non-negative collision noise from flows that share the same bucket, so all k values overestimate the true flow size. The k candidate estimates are the raw counter values:

$$
e _ {j} = C _ {j} [ H _ {j} (f) ], \quad 0 \leq j <   k\tag{2}
$$

The traditional MIN query $( \hat { n } _ { f } = \operatorname* { m i n } _ { j } e _ { j } )$ selects the leastoverestimated value.

2) MEDIAN-Oriented Sketches (CS): Each arriving packet updates $C _ { i } [ H _ { i } ( f ) ]$ by $+ \ 1 \ \mathrm { o r \ - } 1$ depending on a binary hash $h _ { i } ^ { b } ( f ) \in \{ 1 , - 1 \}$ . Collision noise from other flows cancels in expectation, so multiplying a counter by its sign hash yields an unbiased flow-size estimate per row. The k candidate estimates are:

$$
e _ {j} = h _ {j} ^ {b} (f) C _ {j} [ H _ {j} (f) ], \quad 0 \leq j <   k\tag{3}
$$

The traditional MEDIAN query takes the median of the k values $\{ e _ { j } \}$

3) SUM-Oriented Sketches (RCS, SSVS): Each arriving packet updates only one of the k counters, chosen uniformly at random. Packets of flow $f$ are therefore split roughly evenly, so each hashed counter holds approximately $\frac { 1 } { k }$ of the true count. Scaling by k (and subtracting average background noise $\mathrm { N o i s e } _ { \mathrm { a v g } }$ where applicable) recovers a per-row flow-size estimate:

$$
e _ {j} = k \left(h _ {j} ^ {b} (f) C _ {j} \left[ H _ {j} (f) \right] - \text { Noise } _ {\text { avg }}\right), \quad 0 \leq j <   k\tag{4}
$$

For RCS, $h _ { i } ^ { b } ( f ) = 1$ (increment-only) and $\mathrm { N o i s e } _ { \mathrm { a v g } } = N / ( k w )$ where N is the total packet count. For SSVS, $h _ { i } ^ { b } ( f ) \in \{ 1 , - 1 \}$ and $\mathbf { N o i s e _ { a v g } } \ = \ 0$ since the signed noise is unbiased. The traditional SUM query averages or sums the k values.

In all three cases the candidate vector $[ e _ { 0 } , e _ { 1 } , \ldots , e _ { k - 1 } ]$ forms the foundation of our feature vector, providing consistent feature generation regardless of underlying sketch structure.

## B. Constructing the Feature Vector

Beyond the k candidate estimates, we include the sketch’s original flow-size estimate $\hat { n } _ { f _ { i } }$ computed by its traditional query method. This provides the model with both raw measurements and the sketch’s aggregated judgment, enabling it to learn when to trust the sketch versus applying corrections.

Using $e _ { j }$ to denote the per-row candidate estimate from Equations (2)–(4), the feature vector for flow $f _ { i }$ is:

$$
\mathbf {x} _ {i} = [ \mathrm {\it e} _ {0}, \mathrm {\it e} _ {1}, \ldots , \mathrm {\it e} _ {k - 1}, \mu_ {r}, \sigma_ {r} ^ {2}, m _ {r}, \hat {n} _ {f _ {i}} ]\tag{5}
$$

The sketch estimate $\hat { n } _ { f _ { i } }$ aggregates the k candidates using the sketch’s traditional query:

$$
\hat {n} _ {f _ {i}} = \left\{ \begin{array}{l l} \min _ {j} e _ {j} & \text { MIN - oriented   (CM,   CU) } \\ \text { Median } _ {j} e _ {j} & \text { MEDIAN - oriented   (CS) } \\ \frac {1}{k} \sum_ {j} e _ {j} & \text { SUM - oriented   (RCS,   SSVS) } \end{array} \right.\tag{6}
$$

1) Statistical Summary of Counter Values: Let $\nu _ { \operatorname* { m i n } } ~ =$ min ${ \mathfrak { i } } e _ { j }$ and define ratio features $r _ { j } = ( e _ { j } \mathrm { ~ - ~ } \nu _ { \mathrm { m i n } } ) / ( \nu _ { \mathrm { m i n } } \mathrm { ~ + ~ } 1 )$ We compute three summary statistics appended to Equation (5):

$$
\begin{array}{l} \mu_ {r} = \frac {1}{k} \sum_ {j = 0} ^ {k - 1} r _ {j}, \quad \sigma_ {r} ^ {2} = \frac {1}{k} \sum_ {j = 0} ^ {k - 1} (r _ {j} - \mu_ {r}) ^ {2} \\ m _ {r} = \text { Median } _ {j} \{r _ {j} \} \end{array}\tag{7}
$$

High $\mu _ { r }$ and $\sigma _ { r } ^ { 2 }$ indicate heavy collision noise typical of small flows; low values signal tight convergence typical of large dominating flows, giving the classifier and regressors an explicit measure of estimation reliability.

2) Normalization: We apply min-max normalization to scale all features to $\begin{array} { r } { [ 0 , 1 ] \colon x ^ { \prime } = \frac { x - \operatorname* { m i n } ( x ) } { \operatorname* { m a x } ( x ) - \operatorname* { m i n } ( x ) } . } \end{array}$ where min(x) and max(x) are computed on the training set and applied identically to validation, test, and inference data to prevent information leakage. All features in Equation (5) derive solely from sketch measurements, preserving the zero-modification principle.

## C. Synthetic Instance Generation for Large Flows

Real-world network trafic exhibits severe flow-size skew, resulting in insuficient training examples for large flows. The US backbone network trafic traces [47] follow a Zipf distribution with $\alpha = 1 . 6 3 \colon$ a few hundred flows with flow sizes exceeding 10,000 in a 1-minute period. Training neural networks on such imbalanced data leads to poor performance on rare but critical large flows.

We address this through systematic synthetic augmentation. Flows in a packet stream are identified by flow keys (e.g., source-destination IP pairs). We create artificial flows with non-existent IP pairs like h777 777 777 777 888 888 888 888i, ensuring they are absent from actual trafic. To generate a training instance for a large flow with target flow size $n ^ { \prime } ,$ , we:

1) Process all real trafic through the sketch until recording completes

2) Identify the k counters mapped to the artificial flow and save their complete pre-insertion states.<sup>1</sup> Insert the $n ^ { \prime }$ packets using the sketch’s native insertion operation, extract the feature vector following the same procedure as for real flows, and store it with target size $n ^ { \prime }$ as a training sample

3) Restore the saved states by overwriting the same k counters. We do not apply inverse updates to undo the $n ^ { \prime }$ packet insertions

This copy–insert–measure–restore procedure is statepreserving for every evaluated sketch. Because the complete stored representations of the k mapped counters, including associated AC/SC metadata, are restored by overwrite, temporary probabilistic AC increments or $\mathrm { \bf S C }$ adjustments are discarded rather than reversed. The sketch therefore returns exactly to its pre-insertion state after each artificial flow, preventing cumulative drift across synthetic samples without copying the entire sketch.

Exact restoration and sample equivalence are separate properties. Restoration by overwrite does not require order independence. However, equivalence between inserting an artificial flow after the recorded stream and placing its packets at an arbitrary position in the original stream does require order independence. Proposition 3 is therefore limited to that stronger equivalence. For order-dependent AC and SC variants, each feature vector is still the exact result of applying the sketch’s native insertion rule to the recorded state, but we do not claim invariance to every possible packet interleaving.

For each flow-size bin in our two-stage architecture, we generate synthetic samples to achieve roughly balanced representation. For the large-flow bin, we generate samples uniformly spanning the bin to ensure comprehensive coverage. For the small-flow bin, we focus synthetic generation on the upper portion where real samples are relatively scarce but the bin boundary makes accurate classification important.

We now formally verify that these synthetic feature vectors are statistically valid training samples.

Proposition 3 (Synthetic Sample Validity): For any orderindependent sketch, let $\phi$ denote the sketch state after recording stream $s ,$ and let $f _ { \mathrm { s y n } } \notin { \mathcal { S } }$ be an artificial flow. Let $\mathbf { X } _ { \mathrm { s y n } }$ be the feature vector extracted after recording $n ^ { \prime }$ packets from $f _ { \mathrm { s y n } }$ into $\phi$ and reverting. Let $\mathbf { X } _ { \mathrm { n a t } }$ be the feature vector that would be extracted for $f _ { \mathrm { s y n } }$ if instead its $n ^ { \prime }$ packets had been present in the original stream from the start (i.e., the sketch processed $S _ { + } = S \cup \{ f _ { \mathrm { s y n } } : n ^ { \prime } \} )$ . Then $\mathbf { x } _ { \mathrm { s y n } } = \mathbf { x } _ { \mathrm { n a t } }$ for every realization of the hash functions and any internal randomness fixed by the sketch update rule.

The proof is deferred to the supplementary material.

## V. POST-SKETCH MACHINE LEARNING (PS-ML)

Having established our feature extraction methodology, we now describe the PS-ML architecture. This section details our exploration of diferent modeling approaches, explains why we arrived at our two-stage design, and presents the complete training and inference workflow.

## A. Empirical Validation: Why Unified Models Cannot Succeed

Section III established theoretically that sketch estimation error is qualitatively diferent across flow sizes, and that a single correction model cannot handle both noise-dominated and signal-dominated regimes simultaneously. We empirically tested whether practitioners could bypass this structural limitation through standard ML techniques.

Linear regression on the feature vector exhibited what we call dominant range bias: with over 80% of CAIDA flows below size 100, the model converged to predicting in the small-flow range regardless of input, directly instantiating Proposition $2 \mathrm { { : } } \mathrm { { s } }$ threshold $n _ { f } ^ { * }$ . Nonlinear extensions (polynomial regression, basic neural networks) reproduced the same behavior. Standard imbalanced-learning remedies failed systematically: oversampling large flows caused over-prediction on small flows; undersampling small flows discarded useful data; synthetic augmentation (Section IV-C) reduced class imbalance but could not reconcile two conflicting correction strategies within a single parameter space.

These experiments confirm that the obstacle is structural. No resampling strategy resolves the need for aggressive correction on noise-dominated flows alongside near-identity mapping on signal-dominated ones within the same model. The two-stage design in Section V-B is the direct response: separate the two error regimes so each model specializes on a problem with consistent noise characteristics.

## B. Two-Stage Architecture: Specialization Through Binning

PS-ML partitions the problem into two sequential stages. First, a classifier categorizes flows into flow-size-based bins. Second, specialized regressors trained specifically for each bin predict final flow sizes. This design allows each model component to focus on a narrower problem with consistent error characteristics.

Theorem 1 (Optimality of Two-Stage Regression): Let $\ell ( y , \hat { y } ) = ( y - \hat { y } ) ^ { 2 } \sqrt { 1 + y }$ be the PS-ML loss. Let H be the class of feedforward neural networks used as regressors, D the training distribution, and $D = D _ { L } \cup D _ { H }$ the partition by flow-size threshold τ (with ${ \cal D } _ { L } \cap { \cal D } _ { H } = \emptyset , p _ { L } = | { \cal D } _ { L } | / | { \cal D } | ,$ $p _ { H } = | D _ { H } | / | D | )$ . Define the expected risk of a unified regressor $\textit { h } \in \textit { \textbf { \mathscr { H } } }$ as $\begin{array} { r l r } { \mathcal { R } ( h ) } & { { } = } & { \mathbb { E } _ { ( \mathbf { x } , \boldsymbol { y } ) \sim \mathcal { D } } \big [ \ell ( \boldsymbol { y } , h ( \mathbf { x } ) ) \big ] } \end{array}$ and the expected risk of the two-stage scheme with oracle bin assignment as $\mathcal { R } _ { \mathrm { 2 S } } ( h _ { L } , h _ { H } ) \ = \ p _ { L } \mathbb { E } _ { D _ { L } } [ \ell ( y , h _ { L } ( { \bf x } ) ) ] \ + \ p _ { H } \mathbb { E } _ { D _ { H } } [ \ell ( y , h _ { H } ( { \bf x } ) ) ]$ Then, $\begin{array} { r l r } { \operatorname* { i n f } _ { h _ { L } , h _ { H } \in \mathcal { H } } \mathcal { R } _ { 2 \mathrm { S } } ( h _ { L } , h _ { H } ) } & { { } \leq } & { \operatorname* { i n f } _ { h \in \mathcal { H } } \mathcal { R } ( h ) } \end{array}$ with strict inequality whenever the optimal $h _ { L } ^ { * } \neq h _ { H } ^ { * }$ on their respective partitions.

Remark 2: The proof is deferred to the supplementary material. Theorem 1 guarantees that two-stage regression is always at least as good as single-stage regression at the population level. In practice the inequality is strict because—as established by Proposition 2—the noise-to-signal structure difers qualitatively between $D _ { L }$ and $D _ { H } \colon$ any single $h ^ { \ast } \in \mathcal { H }$ that approximates both flow-size regimes simultaneously will be suboptimal on each individually. This theorem is an oracle statement: it assumes that each query is assigned to the correct flow-size bin. The deployed PS-ML pipeline approximates this assignment using the Random Forest classifier; Section VII-G measures its routing quality and compares its range-level AAE with threshold and oracle routing.

1) Stage 1: Random Forest Classification: We employ a Random Forest classifier to categorize flows based on sketchderived features. Random Forest is an ensemble method that constructs multiple decision trees during training. Each tree is trained on a bootstrap sample of the data and considers random feature subsets at each split. For a given feature vector x, each tree $T _ { i }$ in the forest votes for a class label. The final prediction is determined by majority vote:

$$
\hat {y} _ {\text { class }} = \operatorname{mode} \left\{T _ {1} (\mathbf {x}), T _ {2} (\mathbf {x}), \dots , T _ {m} (\mathbf {x}) \right\}\tag{8}
$$

We partition flows into two bins separated by a tunable threshold $\tau \colon [ 1 , \tau )$ for small flows and $[ \tau , \infty )$ for large flows (labeled cold and hot flows, respectively, in Fig. 3). τ should be chosen so that the two bins correspond to meaningfully different noise regimes; the large-flow bin will inevitably contain few real training examples due to the heavy-tailed nature of trafic, which is addressed by the synthetic augmentation in Section IV-C. In principle, more than two bins could provide finer-grained specialization—each regressor would operate over a narrower and more homogeneous error landscape—and we leave this multi-bin extension as future work. In practice, our two-bin design already captures the dominant structural divide identified in Section III: below $n _ { f } ^ { * }$ flows are noisedominated; above it they are signal-dominated. For CAIDA trafic we set $\tau = 1 0 { , } 0 0 0$ , which aligns well with the theoretical threshold $n _ { f } ^ { * }$ (Section III) and keeps the two bins reasonably balanced.

Random Forest ofers several advantages for this task: ensemble voting reduces overfitting, the model is robust to noisy features, and axis-aligned decision splits are naturally interpretable. Since wrong routing can send a query to a less suitable regressor, especially near τ, we measure classifier routing quality and its efect on range-level AAE directly in Section VII-G.

2) Stage 2: Specialized Neural Network Regression: After classification, flows are routed to bin-specific neural network regressors. Each regressor is a feedforward network with two hidden layers of 64 neurons each, using ReLU activation functions. The architecture for a single regressor follows:

$$
\mathbf {h} ^ {(1)} = \operatorname{ReLU} (\mathbf {W} ^ {(1)} \mathbf {x} + \mathbf {b} ^ {(1)})\tag{9}
$$

$$
\mathbf {h} ^ {(2)} = \operatorname{ReLU} (\mathbf {W} ^ {(2)} \mathbf {h} ^ {(1)} + \mathbf {b} ^ {(2)})\tag{10}
$$

$$
\hat {y} = \mathbf {W} ^ {(3)} \mathbf {h} ^ {(2)} + \mathbf {b} ^ {(3)}\tag{11}
$$

where $\mathbf { W } ^ { ( l ) }$ and $\mathbf { b } ^ { ( l ) }$ are learnable weights and biases for layer l. We keep the architecture modest (two hidden layers of 64 neurons) since the feature dimensionality is low (typically 5–10 values) and deeper networks overfit, especially in the sparse large-flow bin.

Each regressor trains on its target bin with the flow-sizeweighted loss:

$$
\mathcal {L} (\mathbf {y}, \hat {\mathbf {y}}) = \frac {1}{N} \sum_ {i = 1} ^ {N} (y _ {i} - \hat {y} _ {i}) ^ {2} \sqrt {1 + y _ {i}}\tag{12}
$$

This loss penalizes errors proportionally to flow size $( \sqrt { 1 + y _ { i } }$ ranges from ≈ 3 3 at $y _ { i } = 1 0 \mathrm { ~ t o ~ } \approx \mathrm { ~ 1 0 0 ~ }$ at $y _ { i } = 1 0 { , } 0 0 0 )$ , ensuring the model prioritizes large flows where errors have the greatest impact on downstream applications.

Each regressor trains exclusively on data from its target bin (augmented with synthetic samples, Section IV-C), allowing it to specialize on a consistent noise regime: the small-flow regressor handles collision-dominated features (high counter variance, weak signal), while the large-flow regressor handles signal-dominated features (tight counter clustering, near-true values).

## C. Deployment and Practical Considerations

PS-ML targets the ofline query module in Section II-A, not the line-rate recording path: the sketch records packets unchanged, and correction runs only when a management application queries a flow label via the two-stage pipeline of Section V-B (feature extraction, Random Forest routing, and bin-specific neural regression on the stored k counters). PS-ML is therefore a management-plane extension to existing sketch query infrastructure and operators can deploy learned correction without modifying the data plane.

Because the data plane is unchanged, PS-ML adds no line-rate recording cost; the main limitation is a querytime speed–accuracy tradeof. PS-ML suits management-plane applications that query selected flows after collection, not settings requiring minimal-latency scalar queries on every stored label at line rate. Section VII-B reports measured query throughput to help operators judge this tradeof.

Deployment also incurs one-time ofline training and ongoing maintenance when trafic distributions shift. Models should match the production sketch configuration (memory budget, k, and counter type); operators may retrain, recalibrate, or fall back to raw sketch estimates when deployment conditions diverge from training.

## VI. ANALYSIS

This section provides two complementary analyses of PS-ML. Let $Y = n _ { f }$ and let X denote the counter-derived feature vector from Section IV-B; write $\begin{array} { r } { \cal { S } } \ = \ q ( { \bf X } )  \end{array}$ for the scalar from the hand-crafted query rule (minimum, median, or sum), so the raw sketch is $\widehat { Y } \ = \ S$ . Theorem 2 shows that X is informationally at least as useful as S for oracle MSE estimators. Theorem 3 then imposes a finite-variance regime model, derives closed-form MSE expressions, and gives a suficient condition under which the deployed pipeline beats the raw sketch, accounting for learning and routing errors; we require only the second moments below, not Gaussian noise.

Theorem 2 (Estimation Advantage Over Scalar Sketch Queries): Define $\begin{array} { r l r } { R _ { \mathbf { X } } ^ { \star } } & { = } & { \operatorname* { m i n } _ { g } \mathbb { E } [ ( Y - g ( \mathbf { X } ) ) ^ { 2 } ] } \end{array}$ and $\begin{array} { r l } { R _ { S } ^ { \star } } & { { } = } \end{array}$ $\mathrm { m i n } _ { h } \mathbb { E } [ ( Y - h ( S ) ) ^ { 2 } ]$ , where g may use X and h may use only S . Then $R _ { \mathbf { X } } ^ { \star } \leq R _ { S } ^ { \star }$ , with exact gap $R _ { S } ^ { \star } - R _ { \mathbf { X } } ^ { \star } = \mathbb { E } [ \mathrm { V a r } ( \mathbb { E } [ Y \mid \mathbf { X } ] \mid |$ $S ) ] \geq 0$ . The inequality is strict whenever compressing X into S discards predictive information about Y.

The proof is deferred to the supplementary material. Theorem 2 is distribution-free and compares oracle estimator classes; it does not guarantee that trained PS-ML regressors beat the raw sketch, though the same ordering holds for PS-ML’s weighted squared training loss because every predictor of S can be implemented from X.

For Theorem 3, define B = L if Y < τ and B = H otherwise, with $\pi _ { b } = \operatorname* { P r } ( B = b ) , \mu _ { b } = \mathbb { E } [ Y \mid B = b ]$ , and $\nu _ { b } = \operatorname { V a r } ( Y \mid B =$ b). In regime b, write $S = Y + \beta _ { b } + Z _ { b }$ with $\beta _ { b } = \mathbb { E } [ S - Y \ |$ $B = b ] , \mathbb { E } [ Z _ { b } \mid B = b ] = 0 , \operatorname { V a r } ( Z _ { b } \mid B = b ) = \sigma _ { b } ^ { 2 } ,$ and $Z _ { b }$ uncorrelated with Y given $B = b .$ . The raw sketch $\widehat { Y } _ { \mathrm { s k e t c h } } = S$ has MSE $R _ { \mathrm { s k e t c h } }$ . With oracle label $B = b ;$ , the afine reference $\widetilde { Y } _ { b } ( a _ { b } ) = \mu _ { b } + a _ { b } ( S - \beta _ { b } - \mu _ { b } ) - a$ tractable scalar baseline with oracle routing, not the deployed PS-ML model—minimizes at $a _ { b } ^ { \star } ~ = ~ \nu _ { b } / ( \nu _ { b } + \sigma _ { b } ^ { 2 } )$ , yielding MSE $R _ { \mathrm { l i n } }$ and gain $\Delta _ { \operatorname* { m i n } } \ =$ $R _ { \mathrm { s k e t c h } } - R _ { \mathrm { l i n } }$ . Deployed PS-ML routes via $\widehat { B }$ and regresses on X (MSE $R _ { \mathrm { P S } } ) _ { \mathrm { \ell } }$ ; oracle routing of the same regressors yields $R _ { \mathrm { t r u e } }$ . We measure the learning gap by $\eta = \operatorname* { m a x } \{ 0 , R _ { \mathrm { t r u e } } - R _ { \mathrm { l i n } } \}$ and routing/deployment error by $\epsilon \Gamma = \operatorname* { m a x } \{ 0 , R _ { \mathrm { P S } } - R _ { \mathrm { t r u e } } \}$

Theorem 3 (Suficient Condition for Two-Stage MSE Gain:) Under the setup above, $\begin{array} { r c l } { R _ { \mathrm { s k e t c h } } } & { = } & { \sum _ { b \in \{ L , H \} } \overline { { \pi } } _ { b } ( \beta _ { b } ^ { 2 } \ + \ \sigma _ { b } ^ { 2 } ) , } \end{array}$ $\begin{array} { r } { R _ { \mathrm { l i n } } = \sum _ { b \in \{ L , H \} } \pi _ { b } \nu _ { b } \sigma _ { b } ^ { 2 } / ( \nu _ { b } + \sigma _ { b } ^ { 2 } ) , } \end{array}$ , and $\begin{array} { r } { \Delta _ { \operatorname* { m i n } } = \sum _ { b \in \{ L , H \} } \pi _ { b } ( \beta _ { b } ^ { 2 } + } \end{array}$ $\sigma _ { b } ^ { 4 } / ( \nu _ { b } \ + \ \stackrel { . } { \sigma _ { b } ^ { 2 } } ) )$ . Deployed PS-ML satisfies $R _ { \mathrm { s k e t c h } } - R _ { \mathrm { P S } } \geq$ $\Delta _ { \operatorname* { m i n } } - \eta - \epsilon \Gamma$ , so it improves over the raw sketch whenever $\eta + \epsilon \Gamma < \Delta _ { \mathrm { m i n } }$

The proof is deferred to the supplementary material. All quantities can be estimated on validation data from labeled samples with $B _ { i } ~ = ~ L ~ \mathrm { i f } ~ Y _ { i } ~ < ~ \tau$ and $B _ { i } ~ = ~ H$ otherwise: compute $\begin{array} { r } { \widehat { \mu } _ { b } , \widehat { \pi } _ { b } , \widehat { \beta } _ { b } , \widehat { \sigma } _ { b } ^ { 2 } = N _ { b } ^ { - 1 } \sum _ { i : B _ { i } = b } ( ( S _ { i } - Y _ { i } ) - \widehat { \beta } _ { b } ) ^ { 2 } } \end{array}$ , and $\begin{array} { r } { \widehat { \nu } _ { b } = N _ { b } ^ { - 1 } \sum _ { i : B _ { i } = b } ( Y _ { i } - \widehat { \mu } _ { b } ) ^ { 2 } } \end{array}$ , then $\widehat { R } _ { \mathrm { s k e t c h } } , \widehat { R } _ { \mathrm { l i n } } , \widehat { R } _ { \mathrm { t r u e } }$ , and $\widehat { R } _ { \mathrm { P S } }$ with slacks $\widehat { \eta } = \operatorname* { m a x } \{ 0 , \widehat { R } _ { \mathrm { t r u e } } - \widehat { R } _ { \mathrm { l i n } } \} , \widehat { \epsilon } \widehat { \Gamma } = \operatorname* { m a x } \{ 0 , \widehat { R } _ { \mathrm { P S } } - \widehat { R } _ { \mathrm { t r u e } } \}$ and optionally misrouting rate $\widehat { \epsilon } = N ^ { - 1 } \textstyle \sum _ { i } { \bf 1 } \{ \widehat { B } _ { i } \not = B _ { i } \} .$

For CM at 5 Mbits on CAIDA15 $\begin{array} { r l r l r l } { ( k } & { { } = } & { 4 , } & { \tau } & { { } = } \end{array}$ 10 000), representative validation estimates $( \beta _ { L } , \sigma _ { L } , \sqrt { \nu _ { L } } ) \ =$ (150 200 1500), $( \beta _ { H } , \sigma _ { H } , \sqrt { \nu _ { H } } ) = ( 1 2 0 $ 160 25000), and $\pi _ { H } \approx$ $7 \times 1 0 ^ { - 4 }$ give $R _ { \mathrm { s k e t c h } } ~ \approx ~ 6 . 2 5 ~ \times ~ 1 0 ^ { 4 }$ and $\Delta _ { \operatorname* { m i n } } \approx 2 . 3 2 \times 1 0 ^ { 4 }$ (37.1% relative gain from the afine reference alone). With $\eta = 0 . 0 5 R _ { \mathrm { s k e t c h } }$ and $\epsilon \Gamma = 0 . 0 2 R _ { \mathrm { s k e t c h } }$ , the certified reduction is about 30.1%. These values are illustrative and should be recomputed for each sketch-memory setting.

## VII. EVALUATION

We validate PS-ML through comprehensive experiments on real network trafic traces across eleven diverse sketch implementations. Our evaluation is organized as follows: we first establish experimental conditions, then position PS-ML against competing baselines, followed by a broad accuracy analysis across all sketch implementations. We then compare PS-ML with recent full-flow measurement sketches (DHS and BitMatcher) and evaluate temporal and cross-domain transfer. We conclude with three case studies: two demonstrating that PS-ML, built on a general-purpose sketch, achieves accuracy comparable to specialized sketches designed for large-flow detection tasks, and one measuring sensitivity under attackinduced distribution shifts.

## A. Experimental Setup

1) Datasets and Evaluation Metrics: The first dataset we use is CAIDA [46], collected from routers in US backbone networks. We use two subsets: CAIDA15 (2015, 60 traces, ∼18M packets and ∼430K flows per trace, Zipf skewness $\alpha = 1 . 6 3 )$ and CAIDA19 (2019, diferent routers, 60 traces, ∼35.7M packets, ∼1.81M flows per trace, Zipf skewness $\alpha = 2 . 0 8 )$ . CAIDA15 is partitioned into training (40 traces), validation (10 traces), and testing (10 traces); CAIDA19 is used exclusively as a temporal generalization test with no traces seen during training. The second dataset we use is MAWI [48], which captures backbone trafic from the WIDE project network in Japan. Specifically, we use 2 traces from samplepoint-F (January 2024), each a 15-minute capture, comprising ∼4.77M unique flows and ∼19.95M total packets. Unlike CAIDA, the MAWI traces are randomly partitioned 50/50 into training and test sets. With a Zipf skewness of $\alpha = 0 . 6 1$ . We will also use multiple simulated attack datasets for case studies in Section VII-J.

2) Baseline Methods: RatioSketch [36] is the only directly comparable prior work—query-time neural correction with no recording-pipeline change—and serves as our primary baseline. We also include LAA [28] and LegoSketch [45] as contextual online-ML sketch baselines: both modify packet recording (LAA routes updates with a learned classifier; LegoSketch adds modular neural operations online), so their results benchmark alternative online-ML designs rather than drop-in competitors to PS-ML, which changes only query-time estimation. For full-flow measurement, we further compare against DHS [49] and BitMatcher [50], which improve accuracy via adaptive counter organization rather than post-sketch correction. CM is the uncorrected baseline throughout.

3) Implementation Details: All compared methods are built on top of Count-Min Sketch (CM) [13]. CM is configured with $k \ = \ 4$ hash functions. The Random Forest classifier uses scikit-learn with 100 estimators, maximum tree depth of 20, minimum 20 samples per split, and fixed random state 42 for reproducibility. Code is publicly available at https:// github.com/aka334/PS-ML.git. Each regressor has two hidden layers of 64 neurons with ReLU activation, trained using the Adam optimizer with default learning rate 0.001. We apply early stopping based on validation loss with patience of 10 epochs to prevent overfitting. All experiments run on a machine with 13th Generation Intel Core i7-13700 processor (30 MB cache, 16 cores, 2.1-5.2 GHz) and 16 GB RAM, with an NVIDIA GeForce RTX 3090 GPU (24 GB GDDR6X) for neural network training.

For all experiments, CAIDA15 traces are split at the trace level into training (40 traces), validation (10 traces), and test (10 traces) sets to prevent information leakage. MAWI traces are split 50/50 into training and test sets. For cross-domain transfer, the feature-normalization parameters, Random Forest classifier, and bin-specific neural regressors are fitted using only the MAWI training data, frozen, and applied to the CAIDA15 test split without retraining or recalibration. The in-domain reference is trained on the CAIDA15 training/validation split and evaluated on the same CAIDA15 test split.

4) Evaluation Metrics: We measure accuracy using Average Absolute Error (AAE) defined as $\begin{array} { r } { \mathrm { A A E } ~ = ~ \frac { \sum _ { f \in D } | n _ { f } - \hat { n } _ { f } | } { | D | } } \end{array}$ where $n _ { f }$ is the true flow size of flow $f , \hat { n } _ { f }$ is the estimated flow size, and D is the set of queried flows. AAE directly quantifies the average magnitude of flow-size estimation errors across all flows. We also report AAE separately for flows in diferent flow-size ranges to understand performance across the distribution. We additionally evaluate speed using store and query throughput, both measured in millions of operations per second (Mops). Store throughput measures the rate at which packets are inserted into the sketch during the recording phase; query throughput measures the rate at which flow-size estimates are retrieved, with one operation corresponding to one flow-label query.

## B. Comparison With Baselines

We compare PS-ML with RatioSketch [36], LAA [28], and LegoSketch [45]. All methods use CM as the underlying sketch. RatioSketch is the closest apples-to-apples baseline because, like PS-ML, it applies correction only at query time. LAA and LegoSketch are included as representative onlinemodification ML sketches; their results are useful context, but they target a diferent deployment setting because they change the recording pipeline. Figure 4 shows the normalized AAE (each model’s AAE divided by the CM baseline at the same memory level) across memory budgets on both CAIDA and MAWI; values below 1.0 indicate improvement over the raw CM sketch.

1) Accuracy on CAIDA: As shown in Figure 4(a), PS-ML achieves the lowest normalized AAE at every memory level on CAIDA. Under the minimum memory budget of 0.5 MB, the AAE of PS-ML is 6 2×, 6 5×, and 8 0× lower than those of RatioSketch, LAA, and LegoSketch, respectively, and 16 2× lower than the CM baseline. At memory budgets of 5 MB and above, both LAA and LegoSketch produce normalized AAE above 1.0—meaning they yield higher error than the uncorrected CM sketch in this experimental setting (up to 1 95× higher for LegoSketch at 5 MB). We do not interpret this as a general failure of those methods. Rather, it indicates that online ML sketch designs optimized under diferent assumptions do not directly substitute for a query-time correction module under the highly skewed CAIDA workload without flow-sizerange specialization. PS-ML remains consistently below 1.0 across all memory configurations.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/f6cf18366fd6b2156b26a2522ac4bc07e806b2d2ce3076800ad06f61d5dcd393.jpg)

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/568690659b2316a7671cd3838fdfd95b08728ec5eb54c70aa436ee94e1b906b8.jpg)

Fig. 4. Normalized AAE (divided by CM baseline) for RatioSketch, PS-ML, LAA, and LegoSketch on CAIDA and MAWI across memory budgets. RatioSketch and PS-ML are query-time correction methods, whereas LAA and LegoSketch modify the online recording pipeline. The gray dotted line at 1.0 represents the CM baseline; values above 1.0 indicate higher error than the uncorrected sketch in that experimental setting. Lower is better.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/b414b05539de67b2ca3dc17a0d8275905851b2536b11a399411dafefd75a76f0.jpg)

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/b30f84fd6fca244d88462763e48e5b6ffba6243b0501ef9a787c2c7cb62fb996.jpg)  
Fig. 5. Store and query throughput (Mops) for CM, RatioSketch, PS-ML, LAA, and LegoSketch on CPU (a) and GPU (b). Y-axis is log-2 scale. CM, RatioSketch, and PS-ML preserve the CM recording path; LAA and LegoSketch are online-modification baselines included to contextualize the cost of changing the recording pipeline.

2) Accuracy on MAWI: On MAWI, PS-ML’s advantage is even more pronounced, as shown in Figure 4(b). Under the minimum memory budget of 0.5 MB, PS-ML achieves 27 3×, 30 5×, and 26 9× lower AAE than RatioSketch, LAA, and LegoSketch, respectively, and 53 9× lower than CM. At 10 MB, LegoSketch’s normalized AAE is 2 19× the CM baseline, i.e., above the uncorrected CM result in this configuration. This should again be read as evidence that an online-modification sketch architecture is not directly interchangeable with query-time post-sketch correction under MAWI’s flatter flow-size distribution. RatioSketch consistently improves over CM across all memory levels on both datasets but remains well above PS-ML, confirming that the two-stage flow-size-binning design yields accuracy gains beyond what a single-stage ratio correction can provide.

3) Throughput: Throughput is measured on the CAIDA15 test set with a memory budget of 2 MB using $k = 4$ hash functions. As shown in Figure 5, CM, RatioSketch, and PS-ML have identical store throughput at 49.16 Mops on CPU and 1290.11 Mops on GPU because their recording paths are unchanged and all ML computation is deferred to ofline queries. LAA and LegoSketch change the online processing model, so their throughput should be interpreted as contextual evidence for alternative online-ML sketch designs rather than as a drop-in cost comparison with PS-ML. LegoSketch’s online neural operations reduce its store throughput to 0.07 Mops on CPU and 17.51 Mops on GPU, roughly 700× slower than CM-based query-time methods. For query throughput, we test the query overhead of PS-ML and other methods on both CPU and GPU for a complete query process, including feature extraction, Random Forest routing, and neural-network regression. PS-ML achieves 8.54 Mops on CPU and 115.21 Mops on GPU, which is closely comparable to RatioSketch (9.16 Mops CPU, 138.74 Mops GPU) while delivering substantially higher accuracy. Query throughput is measured per flow label. Raw CM achieves 51.34 and 1085.82 Mflow-queries/s on CPU and GPU, respectively; PS-ML achieves 8.54 and 115.21 Mflow-queries/s. Tables I and II vary the queried workload from 0 5× to 8× the default; throughput remains stable, indicating linear scaling with query volume. LegoSketch’s query throughput is limited to 0.09 Mops on CPU and 16.41 Mops on GPU more than 94× slower than PS-ML on CPU, confirming that its block-based architecture incurs significant eficiency costs at both store and query time.

TABLE I  
PER-FLOW QUERY THROUGHPUT (MFLOW-QUERIES/S) VS. QUERY VOLUME MULTIPLIER ON CPU

<table><tr><td>Sketch</td><td>0.5×</td><td>1×</td><td>2×</td><td>4×</td><td>8×</td></tr><tr><td>CM</td><td>8.49</td><td>8.54</td><td>8.57</td><td>8.52</td><td>8.56</td></tr><tr><td>CU</td><td>8.41</td><td>8.47</td><td>8.50</td><td>8.45</td><td>8.48</td></tr><tr><td>CS</td><td>8.34</td><td>8.39</td><td>8.43</td><td>8.38</td><td>8.41</td></tr><tr><td>SSVS</td><td>8.46</td><td>8.51</td><td>8.54</td><td>8.49</td><td>8.53</td></tr></table>

TABLE II

PER-FLOW QUERY THROUGHPUT (MFLOW-QUERIES/S) VS. QUERY VOLUME MULTIPLIER ON GPU

<table><tr><td>Sketch</td><td>0.5×</td><td>1×</td><td>2×</td><td>4×</td><td>8×</td></tr><tr><td>CM</td><td>114.62</td><td>115.21</td><td>115.48</td><td>115.16</td><td>115.39</td></tr><tr><td>CU</td><td>113.98</td><td>114.55</td><td>114.83</td><td>114.46</td><td>114.71</td></tr><tr><td>CS</td><td>113.36</td><td>113.92</td><td>114.18</td><td>113.85</td><td>114.07</td></tr><tr><td>SSVS</td><td>114.43</td><td>115.02</td><td>115.29</td><td>114.91</td><td>115.18</td></tr></table>

## C. Generality of PS-ML Across Sketch Types

Unlike RatioSketch [36] and other neural sketch approaches [45], which are designed around a specific underlying sketch (e.g., CM), PS-ML is a general post-sketch framework that can be applied to any sketch structure without modification. To demonstrate this, we evaluate PS-ML across eleven sketch variants spanning three major categories. The MIN-oriented category includes CM, CU, CM-AC (CM with active counters [17]), CM-SC (CM with self-adjusting counters [20]), and CU-SC. The MEDIAN-oriented category includes CS, CS-AC, and CS-SC. The SUM-oriented category includes RCS, SSVS, and RCS-AC. They represent the most classical flow size sketches [38]. For all sketches, we use k = 4 hash functions. Active counters and self-adjusting counters follow the typical parameter settings for these sketch designs [38]. Each trace is recorded by an independent sketch instance, after which features are extracted for PS-ML training or evaluation.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/4800e9c1bd0ab8b3d192082d1672444844cb71eb880f919ff52aeb50765e3c68.jpg)  
Fig. 6. Accuracy comparison between sketches and PS-ML under CAIDA15 across four memory budgets. Each group of bars shows the raw sketch AAE (blue) vs. PS-ML AAE (orange) for all 11 sketch variants.

Figure 6 presents the AAE results for all eleven sketch variants under four memory configurations. PS-ML consistently and substantially reduces estimation error across all sketches, achieving up to 90.7% error reduction (RCS-AC at 5 Mbits) and averaging 50.2% reduction across all sketch types and memory configurations. Notably, PS-ML further improves accuracy even for the highest-performing sketches—CS-AC, CS-SC, and SSVS—reducing their AAE by 50.5%, 49.3%, and 56.2% respectively at 500 kbits, demonstrating that PS-ML extends accuracy beyond the limits of existing sketch designs rather than merely correcting weak baselines.

A notable exception to this uniform trend appears in the MIN-oriented sketch category. For CM, CU, CM-AC, CM-SC, and CU-SC, error reduction becomes more pronounced as memory increases for CM specifically, reduction grows from 36.0% at 500 kbits to 52.0% at 5 Mbits. We attribute this to the positive bias inherent in MIN-oriented structures: as memory decreases, hash collisions intensify, overwhelming the k candidate estimates with noise that PS-ML cannot fully overcome. This behavior does not appear in MEDIAN- and SUM-oriented sketches, which maintain consistent and significant error reduction across all memory levels.

Figure 7 shows the error reduction by flow-size range for four representative sketches at 2 Mbits. PS-ML is most efective for small and medium-sized flows, achieving up to 8 9× and 8 0× lower AAE than the raw RCS sketch in the [10<sup>0</sup> 10<sup>1</sup>) and [10<sup>1</sup> 10<sup>2</sup>) ranges respectively, where collision noise most severely masks true flow sizes. For large flows ([10<sup>4</sup> ∞)), error reduction is more modest but remains positive across all sketches. Beyond flow-size estimation accuracy, we additionally evaluate PS-ML on task-specific applications, heavy hitter detection and top-k item identification, to assess whether PS-ML, built on a general-purpose sketch, can compete with sketches specifically designed for these tasks.

## D. Temporal and Cross-Domain Transfer Robustness

In this section, we evaluate the robustness of PS-ML across diferent trafic domains. The first is temporal in-domain validation: the model is trained on CAIDA15 and applied to CAIDA19 without retraining. CAIDA19 was collected four years later, from diferent routers, and at a larger trafic volume, but it still belongs to the CAIDA backbone-trafic ecosystem. The second is cross-domain validation: the model is trained on MAWI and applied directly to CAIDA15 without retraining, testing transfer from WIDE/MAWI trafic in Japan to CAIDA backbone trafic in the United States.

TABLE III  
FULL-FLOW SIZE ESTIMATION ON MAWI: AAE VS. MEMORY BUDGET FOR DHS, BITMATCHER, AND REPRESENTATIVE PS-ML VARIANTS. LOWER IS BETTER

<table><tr><td>Memory</td><td>DHS</td><td>BitMatcher</td><td>PS-ML (CS-AC)</td><td>PS-ML (SSVS)</td><td>PS-ML (CU-SC)</td></tr><tr><td>500 kbits</td><td>143.2</td><td>24.0</td><td>5.67</td><td>6.01</td><td>4.51</td></tr><tr><td>1 Mbit</td><td>59.1</td><td>12.4</td><td>4.29</td><td>3.92</td><td>4.09</td></tr><tr><td>2 Mbits</td><td>24.6</td><td>11.2</td><td>3.27</td><td>3.37</td><td>3.35</td></tr><tr><td>5 Mbits</td><td>7.1</td><td>3.9</td><td>2.94</td><td>2.94</td><td>2.89</td></tr></table>

For temporal in-domain validation, we apply the CAIDA15- trained models directly to CAIDA19 without any retraining. Figure 8 shows that PS-ML maintains comparable error reductions across all sketch variants despite CAIDA19 containing approximately twice the number of flows per trace and being collected from diferent infrastructure four years later, which supports temporal transfer within a related trafic ecosystem.

Figure 9 shows that, across the five flow-size ranges, the frozen MAWI-trained model reduces raw-sketch AAE by 30.1–71.2% for CM, 26.8–61.0% for CS-AC, 61.9–84.2% for RCS, and 13.3–57.1% for SSVS. The gains are largest for collision-dominated small flows and are particularly consistent for RCS. The in-domain CAIDA15-trained model remains more accurate in every plotted range, as expected from its matched training and test distributions, but the frozen model still improves every raw-sketch result without retraining. Thus, MAWI-to-CAIDA15 transfer preserves substantial correction benefit across MIN-, MEDIAN-, and SUM-oriented sketches, while the remaining gap quantifies the cost of domain shift and motivates recalibration or retraining under larger shifts.

## E. Comparison With Modern Full-Flow Sketches

Section VII-B compares PS-ML with query-time and online-ML baselines built on CM. Here we ask whether learned correction remains competitive with stronger sketch structures, comparing against DHS [49] and BitMatcher [50]—recent full-flow designs that improve accuracy via adaptive memory organization and that, unlike PS-ML, change the online recording path. On MAWI across four memory budgets, we report the strongest PS-ML variants from Section VII-C: PS-ML(CS-AC), PS-ML(SSVS), and PS-ML(CU-SC). Table III shows that all three achieve lower AAE than both DHS and BitMatcher at every budget: at 500 kbits the best PS-ML variant reduces AAE by 96.9% vs. DHS and 81.2% vs. BitMatcher; at 5 Mbits the reductions are 59.3% and 25.9%. Thus query-time correction of general-purpose sketches can remain competitive with—and often substantially outperform—modern full-flow structures with adaptive counter layouts. We do not claim universal dominance on every design and workload; rather, PS-ML is not limited to improving weak legacy baselines when measured against recent full-flow methods.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/dcecd3885688f218a0b0019c788c71d3e1f84fea3dd6386a9d1a6d8f6bca9de0.jpg)  
(a) CM

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/80d6794dd11332b2c049a6700e2fee4d7a91f6431dae470921d7f9fa22d1bb94.jpg)  
(b) CS-AC

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/db6d964f3f68ee0bf3c38b2edabe4f818b2f96accb48a60112a95410f2e0f862.jpg)  
(c) RCS

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/d1032666ade2b03d4fcd9643acfdcaf06677e30662ab440e00798e94195731fa.jpg)  
(d) SSVS

Fig. 7. Accuracy comparison of CM, CS-AC, RCS, and SSVS with their corresponding PS-ML across diferent flow-size ranges. The memory is 2 Mbits for CM, CS-AC, and RCS, and 500 kbits for SSVS.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/e1b0274c03c414c4ce6d61aa19a2d9ec9bb0e9a0f79f72f29577820550317fcd.jpg)  
Fig. 8. Temporal in-domain validation on CAIDA19 across four memory budgets. PS-ML is applied via direct inference using the model trained on CAIDA15—no retraining on CAIDA19 is performed. Each group of bars shows the raw sketch AAE (blue) vs. PS-ML AAE (orange) for all 11 sketch variants.

TABLE IV  
AAE W.R.T. THRESHOLD τ (CAIDA15, 1 MBIT)

<table><tr><td>Sketch</td><td> $\tau=10^{3}$ </td><td> $\tau=5\times10^{3}$ </td><td> $\tau=10^{4}$ </td><td> $\tau=2\times10^{4}$ </td><td> $\tau=5\times10^{4}$ </td></tr><tr><td>CM</td><td>800.3</td><td>750.8</td><td>590.2</td><td>790.9</td><td>807.9</td></tr><tr><td>CU</td><td>78.6</td><td>80.7</td><td>69.8</td><td>73.2</td><td>73.5</td></tr><tr><td>CS</td><td>115.3</td><td>113.9</td><td>91.3</td><td>84.3</td><td>110.0</td></tr><tr><td>SSVS</td><td>69.6</td><td>68.8</td><td>62.4</td><td>65.5</td><td>64.4</td></tr></table>

## F. Impact of Parameter Settings

We investigate the sensitivity of PS-ML to the key hyperparameters of the Random Forest classifier. As illustrated in Figure 11(a), the classification error rate minimizes at n = 100 trees, which we adopt as our default configuration. Figure 11(b) shows that training time increases approximately linearly with the number of trees, confirming that n = 100 strikes a good balance between accuracy and computational cost.

Figure 10 shows the efect of tree depth on both Out-of-Bag (OOB) error and test error. Both metrics converge to their minimum values at a depth of 20, which we adopt as our default. Beyond depth 20, neither metric improves, indicating that additional depth introduces no benefit while increasing training time.

We also study the deployment parameters used throughout the evaluation: the flow-size threshold τ, the number of bins, and the number of hash functions k. Unless stated otherwise, these sweeps use 1 Mbit total sketch memory on CAIDA15 and report PS-ML AAE for representative MIN-, MEDIAN-, and SUM-oriented sketches (CM, CU, CS, and SSVS). The same $\tau = 1 0 { , } 0 0 0$ is used on both CAIDA15 and MAWI in the main experiments. Tables IV and V vary τ while keeping two bins. On CAIDA15, $\tau = 1 0 { , } 0 0 0$ achieves the lowest PS-ML AAE for CM, CU, CS, and SSVS. On MAWI, $\tau = 1 0 { , } 0 0 0$ is also best or near-best for all four sketches despite the diferent flow-size distribution, supporting the use of a common default across datasets.

TABLE V  
AAE W.R.T. THRESHOLD τ (MAWI, IN-DOMAIN, 1 MBIT)

<table><tr><td>Sketch</td><td> $\tau=10^{3}$ </td><td> $\tau=5\times10^{3}$ </td><td> $\tau=10^{4}$ </td><td> $\tau=2\times10^{4}$ </td><td> $\tau=5\times10^{4}$ </td></tr><tr><td>CM</td><td>2.73</td><td>2.99</td><td>2.50</td><td>3.35</td><td>4.85</td></tr><tr><td>CU</td><td>24.60</td><td>26.34</td><td>20.42</td><td>23.79</td><td>22.01</td></tr><tr><td>CS</td><td>4.72</td><td>3.16</td><td>2.72</td><td>3.15</td><td>3.09</td></tr><tr><td>SSVS</td><td>2.40</td><td>2.10</td><td>1.93</td><td>2.35</td><td>2.73</td></tr></table>

TABLE VI

AAE W.R.T. BIN COUNT $( \mathrm { C A I D A } 1 5 ,$ 1 MBIT). BIN EDGES: 2 $\mathrm { \bf B I N S } = \{ 1 0 ^ { 4 } \}$ 3 BINS = {10<sup>2</sup> 10<sup>4</sup>}; 4 BINS = {10<sup>2</sup> 10<sup>3</sup> 10<sup>4</sup>}

<table><tr><td>Sketch</td><td>1 bin</td><td>2 bins</td><td>3 bins</td><td>4 bins</td></tr><tr><td>CM</td><td>720.4</td><td>590.2</td><td>610.4</td><td>596.3</td></tr><tr><td>CU</td><td>95.3</td><td>69.8</td><td>72.3</td><td>71.4</td></tr><tr><td>CS</td><td>102.3</td><td>91.3</td><td>89.3</td><td>95.6</td></tr><tr><td>SSVS</td><td>68.8</td><td>65.4</td><td>74.2</td><td>67.4</td></tr></table>

TABLE VII

AAE SENSITIVITY TO k (CM, CAIDA15, FIXED 1 MBIT TOTAL MEMORY)

<table><tr><td></td><td>k=2</td><td>k=3</td><td>k=4</td><td>k=5</td><td>k=6</td></tr><tr><td>Raw AAE</td><td>1230.2</td><td>980.2</td><td>1020.9</td><td>1269.7</td><td>1532.2</td></tr><tr><td>PS-ML AAE</td><td>647.3</td><td>724.5</td><td>590.2</td><td>813.4</td><td>832.3</td></tr></table>

Table VI compares one global regressor with two, three, and four flow-size bins. Two-bin specialization lowers AAE relative to a single global model for every sketch (e.g., CM drops from 720.4 to 590.2). Adding a third or fourth bin does not consistently improve accuracy and can slightly hurt, consistent with reduced training data per bin and weaker routing at finer granularity. The default two-bin design therefore ofers the best accuracy–complexity trade-of for CM, CU, and SSVS. Table VII fixes total sketch memory at 1 Mbit on CAIDA15 and varies k for CM. PS-ML AAE is minimized at k = 4, matching our default configuration, while larger k degrades performance because each counter array shrinks and collisions increase.

## G. Ablation Study: Two-Stage Specialization and Random Forest Routing

We isolate the two-stage design on CM, CS-AC, and SSVS (MIN-, MEDIAN-, and SUM-oriented) at 1 Mbit with $\tau = 1 0 { , } 0 0 0$ on CAIDA15. Tables VIII–X compare the raw sketch with five learned variants that share the same features, training data, normalization, and synthetic augmentation: (i) one global regressor matching either bin-specific architecture; (ii) one capacity-matched global regressor approximating the combined parameter count of both bin-specific regressors; (iii) two bin-specific regressors selected by thresholding the raw-sketch estimate; (iv) the proposed Random Forest–routed two-stage model; and (v) the same regressors with oracle (truebin) routing. Comparing (i)–(ii) tests specialization beyond capacity; (iii) versus (iv) isolates learned routing; and (iv) versus (v) measures the residual cost of imperfect routing.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/1c2c8e006dc2e96e08003a325bbc8f67c8c5300695bf524dd232314c51493a5e.jpg)  
(a) CM

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/a2648c74ff408d777a1797a7189d49cbf53496caaef0b4c65ea96e7dea18c9ac.jpg)  
(b) CS-AC

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/025521311a9e8388b6b9aa96fa61469a0e0a986544210aaef4a0247fb8b3c857.jpg)  
(c) RCS

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/523b688c570fc7af8c1aab79a7f2976423de9601a34ee937d71738741a178604.jpg)  
(d) SSVS

Fig. 9. MAWI-to-CAIDA15 cross-domain transfer for CM, CS-AC, RCS, and SSVS. The underlying raw-sketch memory budget is 2 Mbits for panels (a)–(c) and 500 kbits for panel (d); each PS-ML result uses the same sketch memory budget as its raw baseline. Bars report AAE on held-out CAIDA15 traces by flow-size range for the raw sketch, the frozen MAWI-trained PS-ML model applied without retraining or recalibration, and the in-domain CAIDA15-trained PS-ML model. Lower is better.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/a62ea106a97ccd2e5709750d8b01e705b5a063d65d93619b2fd9c54f70d7ddc5.jpg)

Fig. 10. The impact of tree depth on the classification accuracy.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/8ec16b7f43f055f7275aa5765d0ce7a7b01c88e430a2d04dda96ea001fa73f82.jpg)

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/3dd18b5e8898569997968e185e9df8e207605fb0711db15be94fa6e3111d1e1c.jpg)  
(a) Number of trees  
(b) Training time  
Fig. 11. The impact of the number of trees in the random forest classifier on the error rate and training time.

TABLE VIII  
CM ABLATION: AAE BY FLOW-SIZE RANGE AT 1 MBIT WITH $\tau = 1 0 { , } 0 0 0$

<table><tr><td>Variant</td><td> $10^{0}-10^{1}$ </td><td> $10^{1}-10^{2}$ </td><td> $10^{2}-10^{3}$ </td><td> $10^{3}-10^{4}$ </td><td> $\geq 10^{4}$ </td></tr><tr><td>Raw</td><td>1016.65</td><td>1017.18</td><td>1014.55</td><td>1021.10</td><td>1013.20</td></tr><tr><td>(i) Single</td><td>335.2</td><td>390.1</td><td>403.7</td><td>1501.4</td><td>1628.4</td></tr><tr><td>(ii) Capacity-matched</td><td>407.8</td><td>470.5</td><td>474.2</td><td>1418.8</td><td>1328.2</td></tr><tr><td>(iii) Threshold</td><td>330.3</td><td>345.8</td><td>354.6</td><td>405.3</td><td>724.5</td></tr><tr><td>(iv) Proposed</td><td>320.1</td><td>342.3</td><td>353.4</td><td>393.4</td><td>423.1</td></tr><tr><td>(v) Oracle</td><td>326.4</td><td>343.2</td><td>360.4</td><td>397.3</td><td>415.3</td></tr></table>

Tables VIII–X show that a single global regressor is insuficient: (i) and (ii) improve small-flow AAE but degrade sharply for medium and large flows—on CM both exceed the raw AAE (≈ 1013–1021) above $1 0 ^ { 3 } .$ , with the same pattern on CS-AC and SSVS—confirming that one model cannot jointly handle collision- and signal-dominated regimes. Extra capacity does not explain the gap: (ii) does not consistently beat (i), and both still fail on large flows. Relative to (ii), the proposed model (iv) lowers AAE by 21.5–72.3% on CM, 5.9–60.7% on CS-AC, and 11.1–57.0% on SSVS across ranges. Learned routing is most useful when the raw sketch is a weak binning signal. On SSVS, (iii) and (iv) difer by at most 3.5% in every range, so threshold routing already nearly matches Random Forest; on CM and CS-AC, Random Forest reduces AAE by 41.6% for CM flows above $1 0 ^ { 4 }$ and by 22.9% and 21.0% for CS-AC in the $1 0 ^ { 3 } – 1 0 ^ { 4 }$ and above-10<sup>4</sup> ranges, respectively, relative to (iii). On all three sketches, (iv) remains close to oracle (v).

TABLE IX  
CS-AC ABLATION: AAE BY FLOW-SIZE RANGE AT 1 MBIT WITH = 10 000

<table><tr><td>Variant</td><td> $10^{0}-10^{1}$ </td><td> $10^{1}-10^{2}$ </td><td> $10^{2}-10^{3}$ </td><td> $10^{3}-10^{4}$ </td><td> $\geq 10^{4}$ </td></tr><tr><td>Raw</td><td>143.2</td><td>154.6</td><td>223.5</td><td>293.4</td><td>494.3</td></tr><tr><td>(i) Single</td><td>83.4</td><td>105.2</td><td>154.3</td><td>380.4</td><td>504.2</td></tr><tr><td>(ii) Capacity-matched</td><td>87.4</td><td>120.3</td><td>152.3</td><td>370.8</td><td>510.5</td></tr><tr><td>(iii) Threshold</td><td>61.3</td><td>53.1</td><td>142.5</td><td>210.4</td><td>330.7</td></tr><tr><td>(iv) Proposed</td><td>56.5</td><td>47.3</td><td>143.3</td><td>162.2</td><td>261.2</td></tr><tr><td>(v) Oracle</td><td>53.7</td><td>59.3</td><td>149.3</td><td>175.7</td><td>274.3</td></tr></table>

TABLE X

SSVS ABLATION: AAE BY FLOW-SIZE RANGE AT  
1 MBIT WITH τ = 10 000

<table><tr><td>Variant</td><td> $10^0-10^1$ </td><td> $10^1-10^2$ </td><td> $10^2-10^3$ </td><td> $10^3-10^4$ </td><td> $\geq 10^4$ </td></tr><tr><td>Raw</td><td>146.1</td><td>152.8</td><td>191.3</td><td>364.4</td><td>499.6</td></tr><tr><td>(i) Single</td><td>82.2</td><td>85.4</td><td>105.3</td><td>719.4</td><td>634.3</td></tr><tr><td>(ii) Capacity-matched</td><td>79.3</td><td>84.5</td><td>103.9</td><td>640.1</td><td>596.4</td></tr><tr><td>(iii) Threshold</td><td>64.2</td><td>65.7</td><td>89.3</td><td>280.6</td><td>302.5</td></tr><tr><td>(iv) Proposed</td><td>61.3</td><td>59.4</td><td>92.4</td><td>275.2</td><td>292.9</td></tr><tr><td>(v) Oracle</td><td>58.2</td><td>60.3</td><td>85.5</td><td>272.1</td><td>289.3</td></tr></table>

TABLE XI

RANDOM FOREST ROUTING ACCURACY AT τ = 10 000. ACCURACY IS THE FRACTION OF FLOWS ASSIGNED TO THE CORRECT FLOW-SIZE BIN

<table><tr><td>Sketch</td><td>All flows</td><td> $[\tau/2, 2\tau]$ </td><td> $[\tau/5, 5\tau]$ </td></tr><tr><td>CM</td><td>1.000000</td><td>0.9813</td><td>0.9955</td></tr><tr><td>CU</td><td>0.999998</td><td>0.9979</td><td>0.9995</td></tr><tr><td>CS</td><td>0.999976</td><td>0.9711</td><td>0.9932</td></tr><tr><td>SSVS</td><td>0.999988</td><td>0.9858</td><td>0.9967</td></tr></table>

Table XI reports routing accuracy (fraction of flows assigned to the correct bin). Overall accuracy is at least 0.999976 across four sketches, but is dominated by abundant small flows; accuracy is 0.9711–0.9979 in [τ/2 2τ] and 0.9932–0.9995 in $[ \tau / 5 , 5 \tau ]$ . Thus Random Forest routing is highly reliable, residual errors concentrate near τ, and accurate binning—from a strong raw sketch or from the classifier—is what lets the two-stage design approach the oracle upper bound.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/3f4b60da29ef08c44dd250518b7366a6bd7c0620c9e19c03020c27d4af900065.jpg)  
(a) Precision

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/067abcd5e44fdbbd59358dba4b64112fe62e0fc740f8703aedbc636cf9c7ac75.jpg)  
(b) Recall

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/d8b217f47bddced7c198bcab562934d7bb692d49026aad0097a9e5c97ee39396.jpg)  
(c) F1-score

Fig. 12. Precision, recall, and F1-score for heavy-hitter detection with CM, HeavyGuardian (HG), Tight-Sketch (TS), PS-ML(CM), and PS-ML(SSVS). Memory is set to 1 Mbits and the heavy-hitter threshold to τ = 10 000.  
![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/4b1de537dfc0cad2ae8d7c2ac1837c98093205991dba3c5d5985ddc0e8d74c27.jpg)  
(a)

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/5b581810abe49d79681b838d2484257284610e6b0fbb54d1ea820f41c5deb606.jpg)  
(b)  
Fig. 13. (a) Heavy-hitter F1-score of PS-ML(SSVS) and Tight-Sketch across thresholds ∈ [10 10 000]. (b) F1-score for top-k flow identification with CM, HeavyGuardian (HG), HeavyKeeper (HK), Lossy Counting (LC), Bubble Sketch (BS), PS-ML(CM), and PS-ML(SSVS).

## H. Case Study 1: Heavy Hitter Detection

Heavy-hitter detection applies a binary threshold to flowsize regression: a flow is declared a heavy hitter when $\hat { n } _ { f } \geq$ τ. We compare PS-ML with CM, HeavyGuardian (HG) [22], and Tight-Sketch (TS) [42], evaluating PS-ML(CM) and PS-ML(SSVS) [38] at 1 Mbits and $\tau = 1 0 { , } 0 0 0$ (142 true heavy hitters) and reporting precision, recall, and F1-score. Figure 12 shows that PS-ML(SSVS) and Tight-Sketch both achieve F1 = 0 98, with complementary profiles (TS: precision 1.00, recall 0.97; PS-ML(SSVS): precision 0.96, recall 1.00). A generalpurpose sketch corrected only at query time thus matches a recent heavy-hitter specialist; PS-ML(CM) also raises CM’s F1-score from 0.77 to 0.92, versus 0.87 for HG. Figure 13(a) varies τ from 10 to 10,000 and PS-ML(SSVS) consistently matches or exceeds Tight-Sketch, so this competitiveness does not depend on a single favorable threshold.

## I. Case Study 2: Top-k Item Identification

For top-k identification, all queried flows are ranked by their predicted flow size $\hat { n } _ { f }$ and the k flows with the highest predicted sizes are returned as the top-k set.

We compare PS-ML against HeavyGuardian (HG) [22], HeavyKeeper (HK) [23], Lossy Counting (LC) [41], and the recent Bubble Sketch (BS) [43], which is specialized for topk identification. We evaluate PS-ML with CM and SSVS as the underlying flow-size sketches. Memory is set to 500 kbits and performance is measured by F1-score. As shown in Figure 13(b), Bubble Sketch achieves the highest F1-score of 0.99, while PS-ML(SSVS) reaches a comparable 0.96 and PS-ML(CM) reaches 0.94. Both PS-ML variants outperform

TABLE XII  
WORST-CASE RELATIVE PS-ML AAE UNDER ATTACK (RATIO TO B -O T )

<table><tr><td>Sketch</td><td>Flood (100%)</td><td>Burst ( $\tau$ , 100 flows)</td><td>Zipf ( $\alpha=0.6$ )</td></tr><tr><td>CM</td><td> $1.25\times$ </td><td> $1.03\times$ </td><td> $1.18\times$ </td></tr><tr><td>CU</td><td> $\mathbf{1.57\times}$ </td><td> $1.02\times$ </td><td> $\mathbf{1.24\times}$ </td></tr><tr><td>CS</td><td> $1.00\times$ </td><td> $1.03\times$ </td><td> $1.05\times$ </td></tr></table>

HG (0.91), HK (0.87), and LC (0.86), despite operating on general-purpose per-flow size sketches rather than a top-kspecific data structure. The comparison therefore does not claim universal dominance over specialized sketches; instead, it shows that PS-ML can elevate an existing full-flow measurement sketch to near state-of-the-art top-k accuracy without replacing its online recording structure.

## J. Case Study 3: Attack Scenario Sensitivity

PS-ML is trained on benign collision patterns. To test sensitivity under deployment shift, we train on benign CAIDA15, freeze all learned components (feature normalization, Random Forest router, and bin-specific regressors), and evaluate on attack-augmented CAIDA15 test traces for CM, CU, and CS $( k ~ = ~ 4 , ~ \tau ~ = ~ 1 0 , 0 0 0 )$ . Each value is the ratio of PS-ML AAE under attack to PS-ML AAE on the unmodified benign test. We inject three shifts: (i) small-flow flood at 10%, 25%, 50%, and 100% extra one- to few-packet flows; (ii) elephantflow burst of 10, 50, or 100 elephants sized near τ, 5τ, or 10τ; and (iii) skewness shift with synthetic Zipf flows, $\alpha \in \{ 0 . 6 , 1 . 0 , 1 . 5 , 2 . 0 \}$ . Flood and Zipf report full-trace AAE; burst reports AAE on flows with true size ≥ τ, because a few injected elephants barely move aggregate AAE over ∼570K flows. Table XII shows the worst case per family (flood at 100%, burst at 100 flows near τ, Zipf at α = 0 6).

Across 51 settings (17 attack configurations ×3 sketches), relative AAE stays modest (≤ 1 57×); much of the flood increase reflects the larger augmented test set rather than model failure alone. Flood and Zipf show the largest sketchdependent efects, while burst remains small (1.02–1 03×) even near τ. CS is most stable under flood and Zipf; CU is most flood-sensitive but most stable under burst; CM is intermediate. These rankings difer from cross-domain transfer (Section VII-D), so attack robustness is a distinct property. Because PS-ML is workload-dependent, a benign-trained model may lose accuracy when attacks change flow-size skewness or collision statistics; operators should validate on representative shifted trafic, monitor feature drift, and retrain, recalibrate, or fall back to raw sketch estimates when deployment diverges materially from training.

## VIII. CONCLUSION AND FUTURE WORK

We presented PS-ML, a post-sketch machine learning framework that substantially improves sketch-based flow-size estimation without modifying the recording pipeline. PS-ML reduces average estimation error by 50.2% across eleven sketch implementations, transfers to unseen temporal and cross-domain traces without retraining while retaining substantial correction benefit, and achieves heavy-hitter and top-k classification accuracy comparable to specialized sketches—all while preserving the same store throughput as the underlying sketch.

Several practical limitations remain. PS-ML depends on representative training trafic and suficient sketch memory to preserve informative counter patterns; at very low memory, collision saturation can limit correction gain (Section VII-C). Although store throughput is unchanged, query-time correction introduces a speed–accuracy tradeof: better estimates require higher per-flow compute than a raw sketch query and are suited to management-plane use rather than line-rate scalar queries on every stored label (Section V-C). Learned models should also be retrained or recalibrated when deployment trafic diverges substantially from training—including under attack-induced distribution shifts (Case Study 3)—or operators can fall back to raw sketch estimates for conservative operation.

Going forward, we plan to explore finer-grained flow-size bin partitioning to better capture heterogeneous noise regimes, and to evaluate more advanced model architectures that may further improve accuracy, particularly for large flows where training data is inherently scarce.

## REFERENCES

[1] T. Tanhua et al., “Ocean FAIR data services,” Frontiers Mar. Sci., vol. 6, p. 440, Aug. 2019.

[2] X. Guo et al., “Intelligent online selling point extraction for e-commerce recommendation,” in Proc. AAAI Conf. Artif. Intell., 2022, vol. 36, no. 11, pp. 12360–12368.

[3] J. Li, X. Wang, Y. Lin, A. Sinha, and M. Wellman, “Generating realistic stock market order streams,” in Proc. AAAI Conf. Artif. Intell., vol. 34, 2020, pp. 727–734.

[4] Y. Ma, Z. Guo, Z. Ren, J. Tang, and D. Yin, “Streaming graph neural networks,” in Proc. 43rd Int. ACM SIGIR Conf. Res. Develop. Inf. Retr., Jul. 2020, pp. 719–728.

[5] J. Frommel, C. Phillips, and R. L. Mandryk, “Gathering self-report data in games through NPC dialogues: Efects on data quality, data quantity, player experience, and information intimacy,” in Proc. CHI Conf. Hum. Factors Comput. Syst., May 2021, pp. 1–12.

[6] M. Breunig et al., “Geospatial data management research: Progress and future directions,” ISPRS Int. J. Geo-Inf., vol. 9, no. 2, p. 95, Feb. 2020.

[7] F. Li et al., “Online distributed IoT security monitoring with multidimensional streaming big data,” IEEE Internet Things J., vol. 7, no. 5, pp. 4387–4394, May 2020.

[8] H. Wang, D. Zhang, and K. G. Shin, “SYN-dog: Snifing SYN flooding sources,” in Proc. 22nd Int. Conf. Distrib. Comput. Syst., 2002, pp. 421–428.

[9] F. Hao, M. Kodialam, and T. Lakshman, “ACCEL-RATE: A faster mechanism for memory eficient per-flow trafic estimation,” in Proc. Joint Int. Conf. Meas. Modeling Comput. Syst., 2004, pp. 155–166.

[10] X. Dimitropoulos, P. Hurley, and A. Kind, “Probabilistic lossy counting: An eficient algorithm for finding heavy hitters,” ACM SIGCOMM Comput. Commun. Rev., vol. 38, no. 1, p. 5, Jan. 2008.

[11] R. B. Basat, G. Einziger, R. Friedman, M. C. Luizelli, and E. Waisbard, “Constant time updates in hierarchical heavy hitters,” in Proc. Conf. ACM Special Interest Group Data Commun., Aug. 2017, pp. 127–140.

[12] H. Wang, H. Xu, L. Huang, J. Wang, and X. Yang, “Load-balancing routing in software defined networks with multiple controllers,” Comput. Netw., vol. 141, pp. 82–91, Aug. 2018.

[13] G. Cormode and S. Muthukrishnan, “An improved data stream summary: The count-min sketch and its applications,” J. Algorithms, vol. 55, no. 1, pp. 58–75, Apr. 2005.

[14] C. Estan and G. Varghese, “New directions in trafic measurement and accounting,” in Proc. Conf. Appl., Technol., Architectures, Protocols Comput. Commun., New York, NY, USA, Aug. 2002, pp. 323–336.

[15] M. Charikar, K. Chen, and M. Farach-Colton, “Finding frequent items in data streams,” in Proc. Int. Colloq. Automata, Lang., Program., Malaga, Spain, Jul. 2002, pp. 693–703.

[16] T. Li, S. Chen, and Y. Ling, “Fast and compact per-flow trafic measurement through randomized counter sharing,” in Proc. IEEE INFOCOM, Apr. 2011, pp. 1799–1807.

[17] R. Stanojevic, “Small active counters,” in Proc. IEEE INFOCOM - 26th IEEE Int. Conf. Comput. Commun., 2007, pp. 2153–2161.

[18] C. Hu et al., “DISCO: Memory eficient and accurate flow statistics for network measurement,” in Proc. IEEE 30th Int. Conf. Distrib. Comput. Syst., Jun. 2010, pp. 665–674.

[19] R. B. Basat, G. Einziger, M. Mitzenmacher, and S. Vargaftik, “Faster and more accurate measurement through additive-error counters,” in Proc. IEEE INFOCOM - IEEE Conf. Comput. Commun., Jul. 2020, pp. 1251–1260.

[20] R. B. Basat, G. Einziger, M. Mitzenmacher, and S. Vargaftik, “SALSA: Self-adjusting lean streaming analytics,” in Proc. IEEE 37th Int. Conf. Data Eng. (ICDE), Apr. 2021, pp. 864–875.

[21] T. Yang et al., “A generic technique for sketches to adapt to diferent counting ranges,” in Proc. IEEE INFOCOM - IEEE Conf. Comput. Commun., Apr. 2019, pp. 2017–2025.

[22] T. Yang, J. Gong, H. Zhang, L. Zou, L. Shi, and X. Li, “HeavyGuardian: Separate and guard hot items in data streams,” in Proc. 24th ACM SIGKDD Int. Conf. Knowl. Discovery Data Mining, Jul. 2018, pp. 2584–2593, doi: 10.1145/3219819.3219978.

[23] T. Yang et al., “HeavyKeeper: An accurate algorithm for finding top-k elephant flows,” IEEE/ACM Trans. Netw., vol. 27, no. 5, pp. 1845–1858, Oct. 2019.

[24] Y. Lu, A. Montanari, B. Prabhakar, S. Dharmapurikar, and A. Kabbani, “Counter braids: A novel counter architecture for per-flow measurement,” ACM SIGMETRICS Perform. Eval. Rev., vol. 36, no. 1, pp. 121–132, 2008.

[25] T. Yang, Y. Zhou, H. Jin, S. Chen, and X. Li, “Pyramid sketch: A sketch framework for frequency estimation of data streams,” Proc. VLDB Endowment, vol. 10, no. 11, pp. 1442–1453, Aug. 2017.

[26] C.-Y. Hsu, P. Indyk, D. Katabi, and A. Vakilian, “Learning-based frequency estimation algorithms,” in Proc. Int. Conf. Learn. Represent., 2019, pp. 1–20.

[27] T. Jiang, Y. Li, H. Lin, Y. Ruan, and D. P. Woodruf, “Learningaugmented data stream algorithms,” in Proc. ICLR, 2020, pp. 1–17.

[28] E. Du, F. Wang, and M. Mitzenmacher, “Putting the ‘learning’ into learning-augmented algorithms for frequency estimation,” in Proc. Int. Conf. Mach. Learn., 2021, pp. 2860–2869.

[29] X. Cheng, X. Jing, Z. Yan, X. Li, P. Wang, and W. Wu, “ALSketch: An adaptive learning-based sketch for accurate network measurement under dynamic trafic distribution,” J. Netw. Comput. Appl., vol. 216, Jul. 2023, Art. no. 103659.

[30] A. Aamand, J. Chen, H. Nguyen, S. Silwal, and A. Vakilian, “Improved frequency estimation algorithms with and without predictions,” in Proc. Adv. Neural Inf. Process. Syst. 36, 2023, pp. 14387–14399.

[31] G. M. Lee, H. Liu, Y. Yoon, and Y. Zhang, “Improving sketch reconstruction accuracy using linear least squares method,” in Proc. 5th ACM SIGCOMM Conf. Internet Meas. - IMC, 2005, p. 1.

[32] Y. Fu, D. Li, S. Shen, Y. Zhang, and K. Chen, “Clustering-preserving network flow sketching,” in Proc. IEEE INFOCOM - IEEE Conf. Comput. Commun., Jul. 2020, pp. 1309–1318.

[33] S. Sheng, Q. Huang, S. Wang, and Y. Bao, “PR-sketch: Monitoring per-key aggregation of streaming data with nearly full accuracy,” Proc. VLDB Endowment, vol. 14, no. 10, pp. 1783–1796, Jun. 2021.

[34] Q. Huang et al., “Toward nearly-zero-error sketching via compressive sensing,” in 18th USENIX Symp. Networked Syst. Design Implement. (NSDI), 2021, pp. 1027–1044.

[35] J. He, J. Zhu, and Q. Huang, “HistSketch: A compact data structure for accurate per-key distribution monitoring,” in Proc. IEEE 39th Int. Conf. Data Eng. (ICDE), Apr. 2023, pp. 2008–2021.

[36] M. Wang et al., “RatioSketch: Towards more accurate frequency estimation in data streams via a lightweight neural network,” in Proc. AAAI Conf. Artif. Intell., 2026, vol. 40, no. 31, pp. 26380–26389.

[37] T. Li, S. Chen, and Y. Ling, “Per-flow trafic measurement through randomized counter sharing,” IEEE/ACM Trans. Netw., vol. 20, no. 5, pp. 1622–1634, Oct. 2012.

[38] D. Melissourgos, H. Wang, S. Chen, C. Ma, and S. Chen, “Single update sketch with variable counter structure,” Proc. VLDB Endowment, vol. 16, no. 13, pp. 4296–4309, Sep. 2023.

[39] E. Tsidon, I. Hanniel, and I. Keslassy, “Estimators also need shared values to grow together,” in Proc. IEEE INFOCOM, Mar. 2012, pp. 1889–1897.

[40] G. Einziger, B. Fellman, and Y. Kassner, “Independent counter estimation buckets,” in Proc. IEEE Conf. Comput. Commun. (INFOCOM), Apr. 2015, pp. 2560–2568.

[41] G. S. Manku and R. Motwani, “Approximate frequency counts over data streams,” in Proc. 28th Int. Conf. Very Large Databases (VLDB), 2002, pp. 346–357. [Online]. Available: https://www.vldb.org/ conf/2002/S10P03.pdf

[42] W. Li and P. Patras, “Tight-sketch: A high-performance sketch for heavy item-oriented data stream mining with limited memory size,” in Proc. 32nd ACM Int. Conf. Inf. Knowl. Manage., Oct. 2023, pp. 1328–1337.

[43] L. Cao et al., “Bubble sketch: A high-performance and memory-eficient sketch for finding top- k items in data streams,” in Proc. 33rd ACM Int Conf. Inf. Knowl. Manage., Oct. 2024, pp. 3653–3657.

[44] Y. Cao, Y. Feng, H. Wang, X. Xie, and S. K. Zhou, “Learning to sketch: A neural approach to item frequency estimation in streaming data,” IEEE Trans. Pattern Anal. Mach. Intell., vol. 46, no. 11, pp. 7136–7153, Nov. 2024.

[45] Y. Feng, Y. Cao, H. Wang, X. Xie, and S. K. Zhou, “LegoSketch: A scalable memory-augmented neural network for sketching data streams,” in Proc. 42nd Int. Conf. Mach. Learn. (ICML), 2025, pp. 16589–16603.

[46] UCSD. CAIDA UCSD Anonymized Internet Traces. Accessed: Mar. 21, 2019. [Online]. Available: https://www.caida.org/catalog/datasets/ passive dataset download

[47] UCSD. (2015). CAIDA UCSD Anonymized 2015 Internet Traces on Jan 17. [Online]. Available: https://www.caida.org/data/passive/ passive 2015 dataset.xml

[48] MAWI Working Group. (Jan. 2024). MAWI Working Group Trafic Archive. Accessed: 2024. [Online]. Available: https://mawi.wide.ad.jp/ mawi/

[49] B. Zhao, X. Li, B. Tian, Z. Mei, and W. Wu, “DHS: Adaptive memory layout organization of sketch slots for fast and accurate data stream processing,” in Proc. 27th ACM SIGKDD Conf. Knowl. Discovery Data Mining, Aug. 2021, pp. 2285–2293.

[50] Q. Shi et al., “BitMatcher: Bit-level counter adjustment for sketches,” in Proc. IEEE 40th Int. Conf. Data Eng. (ICDE), May 2024, pp. 4815–4827.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/ec9f16ccd517bfc38b83d1ca81ce51c26ee69cdfa42ca4f10838f0a5adca27ba.jpg)  
Aayush Karki received the B.Sc. degree in computer science and mathematics and the M.S. degree in computer science from the University of Kentucky, Lexington, KY, USA, in 2022 and 2025, respectively, where he is currently pursuing the Ph.D. degree in computer science with the Department of Computer Science. His main research interests include network trafic measurement, sketch-based data structures, streaming algorithms, and machine learning for network analytics.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/bf4ce36853f9968adbe1e412528b131259c116994c37bb5e953c24b3df9e52b3.jpg)

Dimitrios Melissourgos (Member, IEEE) received the master’s and Ph.D. degrees in computer science from the University of Florida in 2023. He is an Assistant Professor at the Department of Computer Science, College of Computing, Grand Valley State University, Allendale, MI, USA. His publications have appeared in venues, including IEEE INFO-COM, PVLDB, and ACM SIGMETRICS. His work focuses on sketch-based network measurement and privacy-preserving machine learning. He develops compact structures for collecting trafic statistics and methods for protecting data during remote neural-network training.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/fc2d6a7db414fa8797060d46f2bf58c092ac0eb2cd020e91df3739a8e3711986.jpg)

Zhe Jiang (Senior Member, IEEE) received the B.E. degree in electrical engineering from the University of Science and Technology of China in 2010 and the Ph.D. degree in computer science from the University of Minnesota in 2016. He is an Associate Professor with the Department of Computer and Information Science and Engineering, University of Florida, where he is also afiliated with the Center for Coastal Solutions. His research interests include data mining, machine learning, and artificial intelligence, with a particular focus on spatiotemporal data mining for interdisciplinary applications in Earth sciences, including floods and storm surges, agriculture, transportation, health, and medicine. He is a Senior Member of ACM. He received the ACM SIGSPATIAL 2023 Best Paper Award and the Best Paper Runner-Up Award in the Blue Sky Vision Track of SIAM Data Mining 2024. He has served as the Program Co-Chair for SDM 2024, the Proceedings Co-Chair for KDD 2023–2026, the Publicity Co-Chair for SDM 2023 and ACMGIS 2022, and the Student Travel Award Chair for ICDM 2022. He has served as a Senior Program Committee Member or the Area Chair for AAAI, ICDM, ICML, ACM SIGSPATIAL, SDM, and PAKDD.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/6eca57b65cbcb64eed3e280b48b29f316b2b6c171221ba1540110d336dfd6c59.jpg)

Shigang Chen (Fellow, IEEE) received the B.S. degree in computer science from the University of Science and Technology of China in 1993 and the M.S. and Ph.D. degrees in computer science from the University of Illinois at Urbana–Champaign in 1996 and 1999, respectively. After graduation, he worked with Cisco Systems for three years before joining the University of Florida in 2002. He is currently a Professor with the Department of Computer and Information Science and Engineering, University of Florida. He has published over 300

peer-reviewed journal/conference papers. He holds 13 U.S. patents, and many of them were used in software products. His research interests include big data, the Internet of Things, cybersecurity, RFID technologies, and intelligent cybertransportation systems. He received the NSF CAREER Award and several best paper awards. He served in various chair positions or as a committee member for numerous conferences. He served as an Associate Editor for IEEE TRANSACTIONS ON MOBILE COMPUTING, IEEE/ACM TRANSACTIONS ON NETWORKING, and a number of other journals. He is an ACM Distinguished Scientist.

![](../01-mineru-output/2026-TON-Post-Sketch_Machine_Learning_for_Accurate_Flow-Size_Estimation_Across_Sketch_Structures/images/64422a4b6eaafce648e7254deb4fc16d4a489b56fed87529de7c0dbbea0756d4.jpg)

Haibo Wang (Member, IEEE) received the B.E. and master’s degrees in computer science from the University of Science and Technology of China, Hefei, China, in 2016 and 2019, respectively, and the Ph.D. degree in computer science from the University of Florida, Gainesville, FL, USA. He is an Assistant Professor with the Department of Computer Science, University of Kentucky, Lexington, KY, USA. He has published 50 articles in refereed journals and conferences, including IEEE/ACM TRANSACTIONS ON NETWORKING, IEEE TRANS-

ACTIONS ON MOBILE COMPUTING. IEEE TRANSACTIONS ON PARALLEL AND DISTRIBUTED SYSTEMS, VLDB, ICDE, ACM SIGMETRICS, and IEEE INFOCOM. His research interests include Internet trafic measurement, big data analytics, software-defined networking, and the Internet of Things. He received the IEEE ICNP 2021 Best Paper Award.
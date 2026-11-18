# DualGuard: An Adaptive Detection Framework for Concurrent Malicious and Normality Drifts in Network Traffic

Xingkai Kang, Jiang Xie, Tao Yin, Hongbo Xu, Peishuai Sun,

Zijian Zhang, Senior Member, IEEE, Liehuang Zhu, Senior Member, IEEE, Shuhao Li, Xiaochun Yun

Abstract—Machine learning-based malware detection systems face a critical challenge from concept drift in dynamic environments where network traffic patterns constantly evolve. While existing research predominantly focuses on isolated drift types, real-world deployments must contend with a dual-drift scenario: the simultaneous evolution of both malicious mutational drift (MMD) from new malware families and normality drift (ND) from changing normal network traffic. Through a comprehensive decade-long empirical analysis, we reveal that spatial ND degrades detection performance more severely than temporal ND, and that multi-class classification and binary anomaly detection paradigms exhibit distinct vulnerabilities to these drifts.

We introduce DualGuard, the first framework to explicitly disentangle and jointly adapt to MMD and spatial ND within a unified, sample-level gating pipeline, instantiated through scenario-specific workflows. At its core is a unified drift detection engine, powered by Hierarchical Contrastive Learning and robust Median Absolute Deviation (MAD)-based statistics, that provides explicit, sample-level gating for MMD and ND signals. A value-aware adaptation mechanism, powered by finegrained clustering to identify novel threat structures, minimizes expert labeling requirements by 200×. Extensive experiments validate its effectiveness across challenging dual-drift scenarios: for classification, it boosts F1 scores by up to 33.74%; for anomaly detection, it improves F1 scores by 21.64% while slashing false positives by 42.78%. An evaluation on real-world ISP traffic further demonstrated DualGuard’s practical value: it achieved a 96.87% F1 score and outperformed the best adaptive baseline by 8.73%.

Index Terms—Concept Drift, Malware Detection, Network Security, Machine Learning.

## I. INTRODUCTION

ACHINE learning (ML) and Deep Learning (DL) cious software by analyzing network traffic [1]. However, the dynamic nature of both malware and network environments poses a significant challenge: concept drift [2]. Concept drift refers to the phenomenon where the statistical properties of the data distribution change over time or across environments, rendering previously trained models obsolete and degrading their detection performance [3].

![](images/9b0d15286d25b7d09e68cd5178e7ecb96ed89925bbe68a5dee28cc68d5489897.jpg)  
Fig. 1: Paradigm-specific vulnerabilities to drift types: Multiclass classification is sensitive to MMD and spatial ND but resilient to temporal ND; anomaly detection is insensitive to MMD but fragile to all ND.

In malware traffic analysis, we focus on two drift types: (i) MMD, driven by new or heavily modified families; and (ii) ND, the evolution of normal traffic due to protocol changes and user behavior [4]. In practice, these often co-occur, forming a dual-drift scenario that single-drift methods struggle to handle.

Dual drift is particularly relevant to advanced persistent threat (APT) detection [5], [6]. Joint U.S. government advisories on AppleJeus and TraderTraitor document multiple malware versions and evolving campaigns by North Korean state-sponsored actors, including the Lazarus Group [7], [8]. Such malicious evolution can induce MMD, while changes in the surrounding network baseline introduce ND.

Prior research has often adopted a one-size-fits-all view of concept drift, overlooking the differences between MMD and ND. MMD-oriented approaches typically assume a static benign baseline and thus tend to raise excessive alarms under ND. Conversely, ND-oriented anomaly detectors are highly sensitive to benign shifts and fail to disentangle temporal from spatial variations in normal traffic [9]. While existing work has established that multi-class classifiers are vulnerable to MMD and anomaly detectors are robust to it, a critical gap remains in systematically understanding how temporal and spatial drift differentially affect these paradigms [10].

To address this gap, we conducted a systematic empirical analysis (Subsection III-B). As shown in Fig. 1, multi-class classifiers remain relatively stable under temporal ND but degrade sharply under spatial ND, frequently misclassifying benign samples as malicious. In contrast, anomaly detectors depend on an accurate model of normality and are therefore vulnerable to both temporal and spatial ND, which can trigger a surge in false positives. Collectively, these findings underscore the necessity of scenario-specific solutions tailored to distinct drift paradigms.

A second bottleneck is expert bandwidth: the conflict between the volume of potentially drifted data requiring expert verification and the limited availability of security analysts [11]. Existing methods typically forward samples suspected of drift for manual analysis without considering sample diversity or informational value, leading to redundant analysis of similar instances and inefficient use of expert resources [12].

To address these fundamental challenges, we propose DualGuard, a novel framework designed to simultaneously handle the dual challenges of MMD and ND in network-based malware detection. DualGuard provides two distinct workflows, each tailored to the unique vulnerabilities of multi-class classification and binary anomaly detection paradigms. Both workflows are built upon a unified core of drift detection and adaptation mechanisms.

The main contributions of this work are:

• First Systematic Analysis of Dual Drift Impact: We reveal the disparate impact of MMD and ND on different malware detection paradigms. This demonstrates that spatial ND is the dominant challenge and that paradigmspecific vulnerabilities necessitate tailored solutions.

• A Novel Dual-Framework for Dual-Drift Adaptation: We propose DualGuard, the first framework to explicitly disentangle and jointly adapt to MMD and spatial ND within a single, sample-level gating pipeline. Its technical core is a novel drift detection engine that combines Hierarchical Contrastive Learning with robust MAD-based statistics to explicitly characterize MMD and ND at the sample level, driving two tailored adaptation workflows for different detection paradigms.

• Value-Aware Adaptation with Minimized Expert Effort: DualGuard incorporates a value-aware sampling mechanism that uses fine-grained clustering to identify and select the most representative samples from drifted data. This reduces expert labeling requirements by 200× while achieving equivalent performance, overcoming the expert bottleneck.

• Extensive Experimental and Real-World Validation: We validate DualGuard’s effectiveness across challenging dual-drift scenarios. For classification, it boosts F1 scores by up to 33.74%; for anomaly detection, it improves F1 scores by 21.64% while slashing false positives by 42.78%. A real-world ISP evaluation further supports its practical value: DualGuard achieved a 96.87% F1 score and outperformed the best adaptive baseline by 8.73%.

## II. RELATED WORK

Concept drift in security-related machine learning tasks has attracted substantial attention in recent years, as adaptive threats and evolving normal behaviors can rapidly undermine the effectiveness of static models [20]. In this section, we review representative approaches for concept drift detection and adaptation, particularly focusing on applicability to network traffic, drift coverage, human-in-the-loop design, and expert efficiency [21].

## A. Plug-and-Play Capability and Detection Target

Table I summarizes the plug-and-play capability of representative methods. Our approach exhibits full plug-and-play compatibility (✓), enabling seamless integration into both classical machine learning and deep learning–based detection systems. Transcend and CADE share this model-agnostic property, whereas INSOMNIA is limited to deep neural network architectures (◦). In contrast, ContraMTD depends on customized channel-level aggregation and contrastive representation learning with task-specific data structures, rendering it non–plug-and-play (✗).

In parallel with adaptive methods for drift/incremental scenarios, recent works such as ET-BERT [22] and ASNet [23] have focused on developing strong representations for encrypted traffic. Unlike this paper, these methods are mostly evaluated in fixed environments, without explicitly modeling concept drift or supporting incremental class/environment arrivals. Therefore, we consider them as orthogonal and reusable encoders: under the same adaptive training schedule, replacing the base feature extractor with them can raise the discrimination upper bound, while this paper focuses on maintaining performance under drift and incremental conditions.

A second, orthogonal family is open-world recognition and out-of-distribution (OOD) detection. OpenMax [24] replaces the softmax layer with an extreme-value model that estimates the probability of an input belonging to an unknown class; ODIN [25] distinguishes in-distribution from out-ofdistribution inputs by combining temperature scaling with input perturbation, while energy-based scoring [26] uses a parameter-free free-energy statistic as the OOD score. These methods effectively flag inputs that fall outside a fixed, closed training label set, which is conceptually aligned with detecting MMD. They nonetheless address a problem different from ours. These methods produce a single novelty score over a static label space and do not model normality drift. As a result, a benign flow that shifts across environments may be scored as out of distribution, leading to the false positives under spatial ND that DualGuard is designed to suppress. Moreover, they do not provide an expert-efficient mechanism for sampling or adaptation. We therefore regard them as orthogonal and complementary, usable as an alternative novelty front-end rather than as end-to-end dual-drift baselines.

## B. Drift Detection Types

Concept drift in security data can manifest as:

TABLE I: Detailed comparison of existing drift detection and adaptation approaches.

<table><tr><td rowspan="3">Method</td><td rowspan="3">Plug-and-Play</td><td colspan="3">Drift Detection</td><td rowspan="3">Human-in-Loop</td><td rowspan="3">Human Efficiency</td><td rowspan="3">Sample Selection Strategy</td></tr><tr><td rowspan="2">MMD</td><td colspan="2">ND</td></tr><tr><td>Temporal</td><td>Spatial</td></tr><tr><td>Transcend [13]</td><td>√</td><td>√</td><td>○</td><td>○</td><td>✕</td><td>✕</td><td>Full ranking</td></tr><tr><td>Transcendent [14]</td><td>√</td><td>√</td><td>√</td><td>○</td><td>✕</td><td>✕</td><td>Full ranking</td></tr><tr><td>CADE [15]</td><td>√</td><td>√</td><td>✕</td><td>✕</td><td>√</td><td>○</td><td>Full ranking</td></tr><tr><td>INSOMNIA [16]</td><td>○</td><td>√</td><td>✕</td><td>✕</td><td>√</td><td>○</td><td>Full ranking</td></tr><tr><td>NormalityShift [17]</td><td>√</td><td>✕</td><td>√</td><td>○</td><td>√</td><td>√</td><td>Full ranking</td></tr><tr><td>ContraMTD [18]</td><td>✕</td><td>√</td><td>✕</td><td>✕</td><td>✕</td><td>✕</td><td>Full ranking</td></tr><tr><td>UnDiff [19]</td><td>○</td><td>√</td><td>✕</td><td>√</td><td>✕</td><td>✕</td><td>Full ranking</td></tr><tr><td>DualGuard</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>Diversity-guided selection</td></tr></table>

✓ Fully Supported ◦ Partially Supported ✗ Not Supported

• MMD, where new attack variants or unseen malware families emerge. Most existing works can detect unseen attacks or anomalies to varying degrees [27].

• Temporal normality drift (temporal ND), resulting from the gradual evolution of behaviors over time. Methods such as Transcendent explicitly consider temporal evolution, but often lack mechanisms for handling spatial ND [28], [29].

• Spatial normality drift (spatial ND), caused by distributional differences across networks, organizations, or geographic regions. Few works explicitly address spatial ND [30].

We next position DualGuard against recent approaches to joint adaptation under normality and malicious drift.

## C. Joint Adaptation to Normality and Malicious Drift

Recent NIDS work includes both direct joint-adaptation studies and closely related generic-drift methods. Net-Guard [31] addresses co-evolving benign and malicious traffic, long-tail attack bias, and labeling cost via density-aware target selection and conditional generation. Strategic Selection and Forgetting (SSF) [32] maintains a bounded memory as normal behavior and threat landscapes change by retaining driftrepresentative samples and forgetting obsolete ones, whereas Task-Aware Memory Replay (TAMR) [33] uses task-aware replay to incorporate new attacks and normal-traffic variations without catastrophic forgetting. As a generic-drift alternative, A-NIDS [34] combines unsupervised clustering-based drift detection with stacked CTGAN replay for lightweight continual updates.

These synthesis and memory mechanisms feed drifted samples into a common model-update path; in their cited formulations, they do not assign an explicit MMD/ND meaning to each candidate. DualGuard instead assigns drift semantics before adaptation: its classifier routes MMD to novelfamily characterization and ND to environmental adaptation, while its benign-only anomaly workflow uses an ND-versusanomaly gate. The distinction is explicit drift-source gating and workflow-specific routing.

## D. Human-in-the-Loop and Expert Efficiency

Efficient use of expert annotation is crucial for sustainable concept drift adaptation. Existing works can be grouped into

three categories:

Methods without any human-in-the-loop or expert feedback (✗), such as Transcend, ContraMTD, and UnDiff, are prone to uncalibrated updates and error accumulation under drift, leading to unstable or even degraded performance.

General-level methods (◦) incorporate basic active learning or explanation modules to alleviate expert dependence, but their feedback mechanisms remain coarse-grained and insufficient to ensure stable adaptation under evolving conditions.

Our approach is explicitly designed for high expert efficiency (✓), employing diversity-aware selection to minimize redundant labeling and ensure that only the most informative samples are routed to experts, thus achieving a favorable tradeoff between annotation effort and post-drift model recovery.

## E. Sample Selection Strategies

Our method adopts a diversity-guided sample selection strategy to maximize the information value of each expert label, enabling efficient model adaptation with minimal intervention. In contrast, most existing approaches rely on full ranking of candidate samples based on uncertainty estimation or statistical significance (e.g., p-value). This strategy tends to select redundant samples from dominant drift patterns, leading to inefficient use of the labeling budget and biased model updates that fail to generalize across the full spectrum of distributional changes [31], [35].

## III. MOTIVATION: EMPIRICAL INSIGHTS INTO DUAL DRIFT

We analyze temporal ND and spatial ND to quantify their impact and derive requirements for a dual-drift framework.

## A. Experimental Setup for Drift Investigation

Our investigation employed two complementary datasets: MAWI (2016–2025), providing ten years of normal network traffic from a Japanese backbone network, and CICIDS2017, offering both benign and malicious traffic from a laboratory environment. This combination enables systematic investigation of temporal evolution and environmental differences.

We conducted experiments under two detection paradigms: multi-class classification using MLP classifiers to distinguish between multiple malware families and normal traffic, and binary anomaly detection trained exclusively on normal traffic to identify anomalous behavior. For each paradigm, we simulated temporal ND (models trained on MAWI 2016–2020 tested on MAWI 2021–2025) and spatial ND (models trained on MAWI tested on CICIDS2017 environments) to isolate the impact of time-based evolution versus environmental differences.

![](images/10bc83dc24d545212e48a54454f6f165bd08415316fdc8f643f7e65c20d50958.jpg)  
Fig. 2: Impact of temporal ND vs. spatial ND on two detection paradigms. (a) Classifier F1 under temporal ND (2020–2025); (b) Anomaly-detection FPR under temporal ND; (c) Classifier summary: baseline vs. temporal ND vs. spatial ND; (d) Anomaly-detection summary for the same three settings.

## B. Key Empirical Findings

Our experiments revealed two insights that fundamentally challenge existing approaches:

Finding 1: Spatial ND Dominates Temporal ND. As illustrated in Fig. 2, spatial ND inflicts an order-of-magnitude harsher penalty than temporal ND. For the multi-class classifier, panel (a) shows that its F1 score remains perfect (˜99.8%) across five years of pure temporal ND, while anomaly detection’s false-positive rate (FPR) in panel (b) rises only moderately—from 17.50% in 2020 to an average 41.24%. In stark contrast, migrating the same models to a new network environment (panel (c) and (d)) drops the classifier F1 to 89.4% (−10.6 %) and drives the anomaly detector’s FPR up to 78.64% (≈ 9× the baseline), revealing a strong reliance on environment-specific artefacts.

Finding 2: Paradigm-Specific Vulnerabilities. Panels (c) and (d) of Fig. 2 further expose that different detection approaches exhibit remarkably distinct sensitivities to drift types. Multi-class classification demonstrates unexpected resilience against temporal ND due to the “anchoring effect” of known malicious patterns—as long as evolving benign patterns don’t resemble known malware families, models maintain accuracy. Conversely, anomaly detection models are inherently vulnerable to any distributional shift in normal behavior, as they rely entirely on maintaining accurate representations of “normal” traffic patterns.

## C. Implications for Dual Drift Handling

These empirical findings establish two fundamental requirements for effective dual drift handling:

Environmental Adaptation Priority. Given that spatial ND from operating in new target environments has a greater impact than temporal ND, any practical solution for malware traffic detection must prioritize rapid adaptation to new network environments.

Scenario-Specific Design. The distinct vulnerability patterns of multi-class classification and anomaly detection paradigms necessitate tailored approaches rather than one-sizefits-all solutions. Each paradigm requires specialized mechanisms optimized for its specific drift sensitivities.

## IV. PROBLEM FORMULATION

Based on our empirical insights, we formalize the dual drift problem and outline our approach to address the unique challenges of concurrent MMD and ND in network-based malware detection.

## A. Threat Model

Our threat model encompasses the challenges posed by the evolving nature of both malicious software and the network environment itself, with particular emphasis on the environmental dependency revealed by our empirical findings.

Adversary. Our threat model considers a sophisticated adversary, such as a state-sponsored or well-funded group, conducting an APT campaign. This adversary rapidly develops and iterates bespoke malware, often deploying new variants to evade detection. Their goal is typically espionage or sabotage rather than immediate financial gain.

Attack Surface. The system monitors network traffic data generated by hosts within a network. Malicious traffic originates from infected hosts communicating with C&C servers, performing lateral movement, downloading malicious code, or exfiltrating data.

Drift Threats. The detection system’s performance is primarily degraded by two forms of concept drift:

(i) MMD: This arises from the adversary’s continuous development of custom tools. The emergence of entirely new malware families or significant modifications to existing variants (e.g., novel C&C channels, new evasion techniques) can lead to abrupt shifts in traffic characteristics, rendering models trained on historical data obsolete.

(ii) ND: In our framework, we strictly define ND as changes occurring in normal traffic. This decision is rooted in several critical methodological and practical considerations, primarily addressing why we do not model a separate “malware normality drift”:

• Statistical Dominance of Normal Traffic: The overwhelming majority of background traffic, and thus the dominant source of statistical distribution changes, is benign. By focusing on the drift within this normal traffic, our approach directly addresses the most significant operational challenge: baseline degradation and the resulting false alarms.

![](images/064b87016109498a2420cf8a8594016084778c3b72fa44a5cf743ad42a83e2ce.jpg)  
Fig. 3: The taxonomy of concept drift in network security addressed by this paper. It comprises MMD and ND. ND is further divided into temporal ND and spatial ND.

• Redundancy from an Adversarial Perspective: The concept of “malware normality drift” is largely superfluous for an adaptive defense system. Any minor malware evolution that does not alter its detectability requires no model update. Conversely, any change significant enough to evade detection constitutes a new adversarial tactic and is more accurately captured by our MMD concept. This distinction avoids ambiguity and focuses defensive efforts on genuine threats.

• Practicality and Data Scarcity: Obtaining reliable, longitudinal data for specific malware families over extended periods is notoriously difficult. Their short lifecycles and the constant flux of C&C infrastructure make it impractical to model their subtle evolutionary patterns as a distinct form of normality drift.

To formalize ND, we further categorize it into two dimensions as shown in Fig. 3: temporal ND, representing the gradual evolution of normal traffic over time due to protocol updates and user behavior changes, and spatial ND, denoting differences in traffic characteristics across data-collection environments, such as network infrastructure and geographical locations.

## V. DESIGN OF DUALGUARD

## A. Approach Overview

DualGuard bridges representation learning and dual-drift detection through a unified, sample-level recognition core. At its heart is a Hierarchical Contrastive Learning (HCL) powered Contrastive Autoencoder (CAE) coupled with robust MAD statistics. This core shapes the embedding geometry so that dual-drift signals become directly discriminable at the sample level: (i) ND manifests as a stable shift of the benign centroid, and (ii) MMD is reflected by the violation of interclass margins, where a sample lies far away from all known class centroids within the HCL-structured space. A lightweight triage then produces explicit, per-sample gating among three outcomes (MMD/ND/None) that drive the appropriate adaptation actions. This core is shared by both workflows.

DualGuard offers two scenario-specific workflows that consume the same recognition core: (i) DualGuard-Classifier, designed for multi-class threat characterization, uses the gating to decide whether to perform threat characterization; (ii) DualGuard-Anomaly, designed for binary anomaly detection, uses the gating to maintain an accurate normal baseline.

## B. DualGuard Architecture

1) Multi-Class Classification Workflow: The classifier workflow specializes in handling both MMD and spatial ND. Fig. 4 illustrates the complete pipeline.

Multi-Class Initialization. In addition to the shared CAE, a multi-class classifier is trained on known malware families and normal traffic. Class centroids are established in the HCLstructured space and used by the recognition core.

Per-Sample Triage. For every incoming sample, the recognition core CAE produces a sample-level gating among MMD, ND, or None (details in Section V-C).

Fine-Grained Threat Analysis. The fine-grained clustering module applies an ensemble of unsupervised algorithms to the MMD-gated candidate pool to obtain complementary pseudolabels. A dedicated divider model then refines representations to maximize separation among emergent groups. Prototypes are selected by combining Gaussian kernel density estimation with centroid proximity to maximize expert value.

Prototype-Based Adaptation. Prototypes are labeled by experts and labels are propagated to nearby samples within refined groups. Both the multi-class classifier and the CAE are incrementally updated with exemplar rehearsal to integrate new families while mitigating catastrophic forgetting. The effectiveness of this exemplar rehearsal in preserving previously learned families is validated empirically in Section VI-C (Table XII).

2) Binary Anomaly Detection Workflow: The anomaly workflow focuses on maintaining an accurate benign baseline, reflecting the binary paradigm’s sensitivity to normality drift.

Binary Initialization. The binary detector is trained exclusively on normal traffic. The shared CAE is trained under the degraded HCL loss that retains only intra-benign compaction (Section V-C3).

Per-Sample Triage. The shared recognition core provides the same sample-level gating, which in this binary setting reduces to a two-way benign-baseline decision (details in Section V-C2).

Baseline Adaptation. Samples that exhibit benign centroid shift are used to update the benign centroid, while the gate thresholds calibrated from $T _ { 0 }$ remain fixed. This keeps the benign representation current without test-time threshold retuning.

## C. Drift detect module

The drift detect module forms DualGuard’s recognition core. It couples Hierarchical Contrastive Learning with robust MAD-based statistics to yield sample-level, geometrically interpretable drift signals. HCL structures the embedding space by compacting intra-class geometry while expanding interclass margins (benign vs. malicious and inter-malware), so that: (i) ND appears as a stable shift of the benign centroid; (ii) MMD appears as margin violations where a sample is far from all known class centroids. A lightweight triage converts these signals into explicit gating among MMD/ND/None to drive adaptation within each workflow.

![](images/287e7aea04f34589e1478aec3d48a09cfebf820923fa12964495fe6726100faf.jpg)  
Fig. 4: The architecture of the DualGuard framework. A unified recognition core uses a Contrastive Autoencoder with Hierarchical Contrastive Learning to generate structured embeddings. A MAD-based statistical triage then gates each sample as MMD, ND, or no drift. This signal drives two tailored workflows: the Classifier workflow uses fine-grained clustering to adapt to MMD, while the Anomaly workflow performs baseline adaptation to handle ND.

1) Hierarchical Contrastive Learning: The central innovation of our drift detection mechanism lies in the hierarchical contrastive learning framework implemented through our CAE. Unlike traditional contrastive learning methods that typically optimize representations at a single granularity by distinguishing similar and dissimilar samples, our method addresses the multi-granular nature of network traffic classification by optimizing representations at multiple hierarchical levels simultaneously.

The CAE learns discriminative embeddings using a specialized contrastive loss function, explicitly modeling four distinct types of relationships within each training batch:

• Intra-Benign: Legitimate traffic samples are encouraged to form compact clusters in the latent space.

• Intra-Malware: Malware samples within the same family are encouraged to cluster closely.

• Inter-Malware: Malware samples from different families are explicitly pushed apart to maintain distinct representations.

• Benign-Malicious: Benign and malicious samples are clearly separated, reinforcing robust binary classification capabilities.

The complete loss function combines hierarchical con-

trastive learning with autoencoder reconstruction:

$$
\mathcal {L} _ {C A E} = \lambda \cdot \mathcal {L} _ {h} + \mathcal {L} _ {r}\tag{1}
$$

where λ is a weighting coefficient that balances the contribution of contrastive learning and reconstruction objectives. The reconstruction loss $\mathcal { L } _ { r } = \mathbf { M } \mathbf { S } \mathbf { E } ( X , \hat { X } )$ ensures that the learned representations preserve the essential characteristics of the input data, where X is the input and $\hat { X }$ is the reconstructed output. The hierarchical contrastive loss is formulated as:

$$
\mathcal {L} _ {h} = \alpha_ {1} \mathcal {L} _ {i n t r a} ^ {b} + \alpha_ {2} \mathcal {L} _ {i n t r a} ^ {m} + \alpha_ {3} \mathcal {L} _ {i n t e r} ^ {m} + \alpha_ {4} \mathcal {L} _ {b i n a r y}\tag{2}
$$

where each component is defined as follows:

$$
\mathcal {L} _ {i n t r a} ^ {b} = \sum_ {i, j \in \mathcal {B}} M (i, j) \cdot d (z _ {i}, z _ {j})\tag{3}
$$

$$
\mathcal {L} _ {i n t r a} ^ {m} = \sum_ {i, j \in \mathcal {F} _ {k}} M (i, j) \cdot d (z _ {i}, z _ {j})\tag{4}
$$

$$
\mathcal {L} _ {i n t e r} ^ {m} = \sum_ {i, j \in \mathcal {M}} M (i, j) \cdot \max (0, \gamma - d (z _ {i}, z _ {j}))\tag{5}
$$

$$
\mathcal {L} _ {\text {binary}} = \sum_ {i \in \mathcal {B}, j \in \mathcal {M}} M (i, j) \cdot \max (0, 2 \gamma - d (z _ {i}, z _ {j}))\tag{6}
$$

Here, $d ( z _ { i } , z _ { j } )$ represents the Euclidean distance between the latent representations $z _ { i }$ and $z _ { j }$ . The matrix $M ( i , j )$ is a binary mask that equals 1 if the sample pair $( i , j )$ belongs to the same class, and 0 otherwise. For the inter-class loss $\mathcal { L } _ { i n t e r } ^ { m } ,$ the mask $M ( i , j )$ is 1 if the samples belong to different classes. The margin hyperparameter $\gamma$ controls the separation between classes.

Our distance function employs a hybrid approach that combines normalized Euclidean distance with cosine similarity:

$$
d (z _ {i}, z _ {j}) = \beta \cdot \frac {\| z _ {i} - z _ {j} \| _ {2}}{\max (\| \mathbf {Z} \| _ {2})} + (1 - \beta) \cdot \left(1 - \frac {z _ {i} ^ {T} z _ {j}}{\| z _ {i} \| _ {2} \| z _ {j} \| _ {2}}\right)\tag{7}
$$

where β is a weighting parameter (set to 0.7 because it achieved the highest mean Macro-F1 in the sensitivity sweep while retaining the directional cosine term (Supplementary Table S4)), Z represents the full embedding matrix, and the normalization ensures both distance components operate in comparable ranges. This hybrid distance captures both magnitude and directional differences, providing more robust similarity assessment in high-dimensional latent spaces.

2) MAD-based drift detection and sample-level gating: Once the CAE establishes discriminative embeddings under HCL, we operationalize dual-drift detection as a sample-level gating problem built on robust, per-class statistics. For each known class $c ,$ we compute its centroid and intra-class distance set:

$$
\mu_ {c} = \frac {1}{| \mathcal {S} _ {c} |} \sum_ {i \in \mathcal {S} _ {c}} z _ {i}, \qquad D _ {c} = \{d (z _ {i}, \mu_ {c}): i \in \mathcal {S} _ {c} \}.\tag{8}
$$

MAD provides robust outlier detection that is less sensitive to extreme values compared to standard deviation-based methods, making it particularly suitable for noisy network traffic data. We then derive a robust dispersion estimate via MAD:

$$
\mathrm{MAD} _ {c} = b \cdot \operatorname{median} \left(\left| D _ {c} - \operatorname{median} \left(D _ {c}\right) \right|\right)\tag{9}
$$

We use the Gaussian consistency constant $b = \textstyle { \frac { 1 } { \Phi ^ { - 1 } ( 0 . 7 5 ) } }$ so that $\mathrm { M A D } _ { c }$ is a consistent estimator of the standard deviation under normality.

For a test sample x with embedding z, we define a per-class standardized distance:

$$
s _ {c} (x) = \frac {d (z , \mu_ {c}) - \operatorname{median} (D _ {c})}{\mathrm{MAD} _ {c}}, \quad s _ {\min} (x) = \min _ {c} s _ {c} (x).\tag{10}
$$

Building on the geometry shaped by HCL—compact intraclass structure and expanded inter-class margins—we implement a lightweight, per-sample triage with the priority order MMD → ND → None:

• MMD: if $s _ { \mathrm { m i n } } ( x ) \ \geq \ \theta _ { \mathrm { m m d } }$ , the sample violates interclass margins against all known centroids and is gated as MMD.

• ND: else if the nearest class is the benign class b and $s _ { b } ( x ) \in [ \theta _ { \mathrm { n d } } ^ { \mathrm { l o w } } , \theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } } ]$ , the sample is gated as ND.

• None: otherwise, no adaptation is triggered.

All gate thresholds are determined from the $T _ { 0 }$ training statistics alone and are never estimated, tuned, or selected on any drift-stage or test data. They are fixed from the same robust per-class location and dispersion estimates that standardize $s _ { c } ( \cdot )$ , and satisfy the strict ordering $\theta _ { \mathrm { n d } } ^ { \mathrm { l o w } } < \theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } } < \theta _ { \mathrm { m m d } } .$ The ND band $[ \theta _ { \mathrm { n d } } ^ { \mathrm { i o w } } , \theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } } ]$ is determined by robust quantiles of the benign $T _ { 0 }$ distances. Thus, a sample is assigned to the ND gate when its deviation from the benign centroid is moderate, indicating drift while remaining within the benign regime. In contrast, $\theta _ { \mathrm { m m d } }$ is defined by a much more extreme uppertail quantile computed over all known classes, so a sample is assigned to the MMD gate only when it is far from every centroid. The margin $\theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } } < \theta _ { \mathrm { m m d } }$ is precisely what lets the triage disentangle the two under concurrent drift: moderate benign drift is routed to baseline adaptation, while an all-class outlier is characterized as a novel family. All thresholds are fixed once using $T _ { 0 }$ and are then reused without modification across all post-drift stages. Therefore, neither held-out data nor test data is used for calibration, and the gate is free of test-set leakage by construction. Supplementary Table S3 consolidates the fixed quantile levels, the dataset/workflowspecific $T _ { 0 }$ computation of the resulting numerical thresholds, and the window size, adaptation rate, and update cadence.

Limitations of the MMD/ND boundary. The MMD/ND/None gates are operational decisions in a learned representation, not semantic guarantees. Benign-looking malicious traffic may be routed to ND and contaminate benign-baseline adaptation, or to None and therefore evade adaptation. Conversely, strongly shifted benign traffic may be routed to MMD, increasing expert effort and delaying benign adaptation. Malicious-family updates wait for expert-confirmed MMD prototypes, while dynamic centroid adjustment tempers the impact of contamination in benign updates. These safeguards reduce but do not eliminate misrouting; adversarial attempts to imitate the opposite drift type remain a direction for future work.

3) Loss Degradation in Anomaly Detection: In binary anomaly detection scenarios, the hierarchical contrastive loss naturally degrades due to the absence of multi-class supervision. This degradation transforms the loss function into:

$$
\mathcal {L} _ {a} = \alpha_ {1} \mathcal {L} _ {i n t r a} ^ {b} + \mathcal {L} _ {r}\tag{11}
$$

This degraded form focuses entirely on learning compact representations of normal traffic for anomaly detection. The system instead uses conservative MAD-based scoring relative to the dynamically maintained benign centroid, while retaining the gate thresholds calibrated from $T _ { 0 }$

In binary anomaly detection, only the benign centroid $\mu _ { b }$ exists, so the MMD branch of the triage is inactive by construction: with no other centroids, $s _ { \mathrm { m i n } } ( x )$ reduces to the standardized deviation from $\mu _ { b } .$ , and a distant sample is a candidate anomaly rather than a margin violation. The triage thus degrades to a two-way baseline-adaptation gate (ND when $s _ { b } ( x ) \in [ \theta _ { \mathrm { n d } } ^ { \mathrm { l o w } } , \theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } } ]$ and no update otherwise); samples above $\theta _ { \mathrm { n d } } ^ { \mathrm { h i g h } }$ remain candidate anomalies for the base detector, consistent with the anomaly-detection paradigm, where novel malicious behavior is surfaced as deviation from the benign baseline rather than characterized as a new family.

4) Dynamic Centroid Adaptation Mechanism: To address the spatial ND dominance revealed by our empirical findings (Section III), the drift detection module incorporates environmental adaptation through dynamic centroid adjustment. When deployed in new environments, the system maintains a sliding window of recent samples and incrementally updates class centroids C using exponential moving averages:

$$
\mathbf {C} _ {c} ^ {(t + 1)} = (1 - \alpha) \cdot \mathbf {C} _ {c} ^ {(t)} + \alpha \cdot \frac {1}{| \mathcal {W} _ {c} |} \sum_ {i \in \mathcal {W} _ {c}} z _ {i}\tag{12}
$$

where $\mathcal { W } _ { c }$ represents recent samples assigned to class $c ,$ and α is the adaptation rate. This mechanism enables rapid adaptation to new network environments while maintaining stability against noise and temporary fluctuations.

## D. Fine-grained Clustering

Within the DualGuard-Classifier workflow, the Fine-grained Clustering module is invoked only for samples triaged as MMD by the recognition core. It does not detect or decide the drift type; instead, it structurally characterizes the MMD candidate pool by performing fine-grained clustering to reveal the underlying organization of novel threats, selecting highly representative prototypes, and enabling label propagation. By turning a heterogeneous alert set into coherent groups and prioritizing prototypes that maximize expert information value, the module reduces redundant analysis, focuses expert effort on the most informative instances, and supports efficient incremental learning for rapid model adaptation with minimal manual effort.

The Fine-grained Clustering module employs a multi-stage ensemble approach to characterize MMD candidates. The key steps include:

1) Neighborhood Relationship Modeling: Rather than relying on a single clustering algorithm with inherent biases, the Fine-grained Clustering module simultaneously applies multiple unsupervised clustering methods (K-Means, DBSCAN, and DEC) to the initial embeddings. Since each algorithm operates on different assumptions about data distribution, this ensemble approach allows for analyzing the data from multiple perspectives, revealing diverse behavioral patterns characteristic of different attack types and significantly reducing singlemethod bias. The outputs of these algorithms are used to construct a neighborhood relationship table, which effectively captures a voting-based consensus on sample-pair similarity.

For each clustering method M, we define a neighborhood relationship table that captures the pair-wise relationships of input samples. Given a pair of samples $( x _ { i } , x _ { j } )$ , their neighborhood relationship $y _ { i j } ^ { ( m ) }$ for method m is defined as:

$$
y _ {i j} ^ {m} = \left\{ \begin{array}{l l} 1 & \text { pair   in   the   same   cluster } \\ 0 & \text { otherwise } \end{array} \right.\tag{13}
$$

2) Metric Learning: This consensus, encoded in the neigh borhood relationship tables, guides a metric learning process. We train a dedicated divider network with an autoencoder architecture to map the original high-dimensional embeddings into a refined, low-dimensional latent space. This transformation is designed to overcome clustering difficulties inherent in high-dimensional data by fusing the neighborhood relationships from the ensemble. The network learns to strengthen the similarity between samples that multiple algorithms agree are of the same type, effectively restoring the data’s true clustering structure.

First, we define the distance between samples in the embedding space as:

$$
d (x _ {i}, x _ {j}) = \| h _ {i} - h _ {j} \| _ {2}\tag{14}
$$

where $h _ { i }$ is the refinement embedding of $x _ { i }$ .

Then, the network is trained with a contrastive loss function:

$$
L (x _ {i}, x _ {j}) = \sum_ {m \in M} \pi_ {m} \left[ y _ {i j} ^ {m} d ^ {2} + (1 - y _ {i j} ^ {m}) [ \delta - d ] _ {+} ^ {2} \right]\tag{15}
$$

where $\pi _ { m }$ is the weight for clustering method $m , \ y _ { i j } ^ { ( m ) }$ indicates whether samples i and $j$ belong to the same cluster according to method m, δ is a margin parameter, and $[ \cdot ] _ { + } ~ = ~ \operatorname* { m a x } ( 0 , \cdot )$ denotes the hinge loss. This contrastive loss function has two components: the first term minimizes distances between samples that should be neighbors (positive pairs), while the second term maximizes distances between samples that should not be neighbors (negative pairs), but only up to the margin δ.

3) Final Clustering: In the refined latent space, we perform a final clustering (typically K-Means) using Euclidean distances. The number of clusters K is selected with silhouette coefficients to obtain well-separated, interpretable groups that often correspond to distinct novel threat types.

## E. Drift Adaptation

For prototype selection, we combine Gaussian kernel density with centroid proximity to pick a few representative samples per cluster. Experts label these prototypes, and labels then propagate to nearby members; if expert labels conflict within a cluster, a lightweight semi-supervised re-clustering splits impure groups.

This turns heterogeneous drift alerts into structured threat groups and enables value-aware sampling that focuses expert effort on the most informative instances, markedly improving adaptation efficiency.

## VI. EXPERIMENTS

## A. Experimental Setup

1) Implementation: We implemented the DualGuard framework in Python 3.11 using TensorFlow 2.16 and Scikit-learn, with GPU acceleration on NVIDIA RTX 4090. We employ an autoencoder with hidden layer dimensions of 512-128-32 to learn compact representations in the latent space. The autoencoder is trained with the Adam optimizer using a learning rate of 0.001 and a batch size of 256 for 50 epochs. All features are min-max normalized based on the initial training set, and this normalizer is saved and consistently applied across all drift stages to ensure uniform feature scaling. The complete hyperparameter settings are listed in Appendix C (Table S3) of the supplementary material.

For the CICIDS2017 classifier-MMD workload, Dual-Guard’s post-feature-extraction triage and classifier-inference path processed 38,610 flow records/s with an inference batch size of 256 on one RTX 4090; per-stage characterization, incremental-update, memory, and expert-review overheads are detailed in Supplementary Table S6.

2) Datasets: We evaluate on three datasets representing diverse network environments and attack characteristics.

(i) MAWI [36]: A decade-long real-world backbone traffic archive from the WIDE project containing anonymized Internet flows. We use MAWI as clean benign data after applying official MAWILab filtering to remove known anomalies, ensuring a baseline of normal network behavior. The existence of temporal ND in this dataset is validated through comprehensive analysis detailed in Appendix B of the supplementary material;

(ii) CICIDS2017 [37]: A widely used intrusion detection benchmark collected in enterprise networks by the Canadian Institute for Cybersecurity;

(iii) DAPT2020 [38]: An APT detection dataset containing stealthy, multi-stage attack campaigns that mimic normal traffic patterns, including both internal lateral movement and external communications. This dataset reflects realistic APT scenarios where attacks are deliberately designed to evade detection. DAPT2020 provides a more challenging evaluation environment than CICIDS2017, as APT campaigns naturally exhibit the dual drift characteristics that our framework is designed to address.

3) Dataset Construction and Preprocessing: Drift Simulation Strategy. We synthesize drift along three independent axes, summarized in Table II. Attack composition controls MMD through the known/unknown split. Benign provenance controls ND: temporal ND draws benign traffic from later MAWI years, while spatial ND replaces the MAWI backbone benign with the target dataset benign. A time index $T _ { 0 } , \ldots , T _ { k }$ orders the stages. For the classifier, the $T _ { 0 }$ benign set is MAWI 2016–2017 for CICIDS2017 and MAWI 2016–2020 for DAPT2020, and unknown families or spatial ND data enter from $T _ { 1 }$ . The anomaly temporal setting advances one MAWI year per stage across $T _ { 1 }$ to $T _ { 5 } ,$ , covering 2021 to 2025. The anomaly spatial settings train on MAWI and test on CICIDS2017 or DAPT2020. Each scenario trains at $T _ { 0 }$ and is evaluated at a single post-drift stage $T _ { 1 }$ , except the temporal and concurrent anomaly settings, which advance one MAWI year per stage and therefore span $T _ { 0 } – T _ { 5 }$

Feature extraction and alignment. All datasets are processed with CICFlowMeter V4.0<sup>1</sup>. This produces a 77- dimensional bidirectional-flow feature set whose definition and ordering are identical across MAWI, CICIDS2017, and DAPT2020. The full schema is listed in Appendix A (Table S1) of the supplementary material. Each flow also stores an identifier that records its source dataset and year (e.g., MAWI 2016 1), which makes every split auditable.

Normalization. A single min–max scaler is fit on the $T _ { 0 }$ training data and then applied without change to all later stages and to every cross-dataset target. Since the feature schema is identical across datasets, the source-fitted scaler remains well defined on each target, which is a prerequisite for the spatial ND study.

Class balancing. Attack families in CICIDS2017 and DAPT2020 differ in frequency by several orders of magnitude. We balance each class to a fixed size so that frequent families do not dominate training. Majority classes are down-sampled and minority classes are up-sampled by resampling under a fixed random seed. The benign class is subsampled from MAWI separately for each year, with each year contributing a controlled and equal share. This design keeps the benign composition uniform across years and preserves the temporal ND signal across stages. Every class is balanced to 10,000 flows and split 80/20 into 8,000 training and 2,000 test flows; the complete per-class composition is reported in Supplementary Table S7. At $T _ { 0 } ,$ , the classifier is trained on benign traffic and the known families. At each subsequent test stage, it is evaluated on a disjoint set of benign traffic and all families present at that stage, namely the known families and the newly introduced unknown families. The anomaly detector is trained only on benign flows and is evaluated on the pooled attack families together with 2,000 benign flows from each ND source, corresponding to 4,000 benign flows under temporal ND + spatial ND.

As a robustness check against evaluation-set resampling, we additionally evaluate the concurrent classifier on an identifierdisjoint CICIDS2017 holdout that retains the natural class distribution without resampling; DualGuard achieves the highest Macro-F1 $( 7 1 . 1 9 \pm 8 . 2 2 \%$ Supplementary Table S5).

Known and unknown families. The known/unknown division applies only to the multi-class classifier, where each attack family forms its own label. Known families appear in the $T _ { 0 }$ training set. Unknown families are withheld from every training stage and occur only in the test stages, where they act as previously unseen malware and induce MMD. The binary anomaly detector uses no such division: it trains on benign traffic only, and at test time all attack families form a single anomaly class. Supplementary Table S7 lists the family assignment and the counts for both datasets.

Training, test, and adaptation data. Each scenario trains the model on the $T _ { 0 }$ training set listed in Table II. The class centroids and the robust MAD statistics that define the drift thresholds are computed on these $T _ { 0 }$ training embeddings, so no separate validation split is needed. Every later stage $T _ { i }$ provides a disjoint test set for evaluation. When adaptation is enabled, the test-stream samples flagged as drift at $T _ { i }$ are labeled and, together with rehearsed exemplars carried over from the previous stage, drive the incremental update. To keep adaptation and evaluation strictly separate, only the drift-gated samples from a given stage are used for model updating. The updated model is then evaluated on the next disjoint stage $T _ { i + 1 }$ . For the single post-drift classifier setting, evaluation is performed on a held-out split of $T _ { 1 }$ that is not used for adaptation. Thus, the samples used for updating never contribute to the reported metrics.

Scope of the spatial ND evaluation. In this study, the cross-dataset protocol operationalizes spatial ND as an aggregate end-to-end cross-environment shift; it is not intended to estimate the isolated causal contribution of geographic or topological change. The MAWI-to-CICIDS2017/DAPT2020 transfer changes the benign-traffic distribution while also entailing differences in capture hardware and link location, traffic volume and collection period, and annotation or curation procedures. The common CICFlowMeter V4.0 extractor, identical 77-dimensional schema, and source-fitted scaler establish a common feature definition, ordering, and scaling interface, but cannot remove these residual dataset-level factors.

TABLE II: Construction of all evaluation scenarios from the three datasets. The notation $\ "  \ "$ indicates the change in the benign source from the $T _ { 0 }$ training set to the drift stages, either to a later MAWI year for temporal ND or to the target dataset for spatial ND. #Test denotes the size of each post-drift evaluation stage.

<table><tr><td>Workflow</td><td>Setting</td><td>Benign source</td><td>Attack source</td><td>T-range</td><td>#Train/#Test</td></tr><tr><td rowspan="6">Classifier</td><td>MMD</td><td>MAWI 2016–17</td><td>CICIDS2017</td><td> $T_0-T_1$ </td><td>80,000/28,000</td></tr><tr><td>MMD</td><td>MAWI 2016–20</td><td>DAPT2020</td><td> $T_0-T_1$ </td><td>48,000/20,000</td></tr><tr><td>spatial ND</td><td>MAWI → CICIDS2017</td><td>CICIDS2017</td><td> $T_0-T_1$ </td><td>80,000/20,000</td></tr><tr><td>spatial ND</td><td>MAWI → DAPT2020</td><td>DAPT2020</td><td> $T_0-T_1$ </td><td>48,000/12,000</td></tr><tr><td>MMD + spatial ND</td><td>MAWI → CICIDS2017</td><td>CICIDS2017</td><td> $T_0-T_1$ </td><td>80,000/28,000</td></tr><tr><td>MMD + spatial ND</td><td>MAWI → DAPT2020</td><td>DAPT2020</td><td> $T_0-T_1$ </td><td>48,000/20,000</td></tr><tr><td rowspan="6">Anomaly (benign-only training)</td><td>temporal ND</td><td>MAWI 2016–20 → 2021–25</td><td>CICIDS2017</td><td> $T_0-T_5$ </td><td>8,000/20,000</td></tr><tr><td>temporal ND</td><td>MAWI 2016–20 → 2021–25</td><td>DAPT2020</td><td> $T_0-T_5$ </td><td>8,000/20,000</td></tr><tr><td>spatial ND</td><td>MAWI → CICIDS2017</td><td>CICIDS2017</td><td> $T_0-T_1$ </td><td>8,000/20,000</td></tr><tr><td>spatial ND</td><td>MAWI → DAPT2020</td><td>DAPT2020</td><td> $T_0-T_1$ </td><td>8,000/20,000</td></tr><tr><td>temporal ND + spatial ND</td><td>MAWI 2016–20 → 2021–25 &amp; CICIDS2017</td><td>CICIDS2017</td><td> $T_0-T_5$ </td><td>8,000/22,000</td></tr><tr><td>temporal ND + spatial ND</td><td>MAWI 2016–20 → 2021–25 &amp; DAPT2020</td><td>DAPT2020</td><td> $T_0-T_5$ </td><td>8,000/22,000</td></tr></table>

4) Baselines: We compare DualGuard against four representative baseline methods:

(i) No-Update: A non-adaptive baseline representing the original model without any mechanism for handling concept drift.

(ii) CADE: A contrastive learning method that detects drift through representation distances. Since CADE inevitably requires all-class data to build its contrastive model, we adapt it for anomaly detection by incorporating anomaly samples from $T _ { 0 }$ to enable binary classification. High drift scores indicate priority samples for labeling.

(iii) TRANSCENDENT: A conformal prediction framework using non-conformity measures (NCM) for drift detection. For multi-class tasks, we optimize credibility and confidence thresholds via random search; for anomaly detection, we use fixed quartile-based credibility thresholds. We employ Inductive Conformal Evaluator (ICE) for computational efficiency. Lower P-values indicate priority samples for adaptation.

(iv) UnDiff: A state-of-the-art approach explicitly addressing drift through uncertainty-inspired modeling. We faithfully implemented this baseline according to the original specifications.

The same labeling budget is used for all approaches to ensure a fair comparison.

5) Metrics: The metrics for evaluating adaptation performance are similar to those used for evaluating classifier or anomaly detection models in their works as our work is to recover the original performance after adapting to drift. For multi-class classification, we use Accuracy and F1 score to assess performance. For binary anomaly detection, we use AUC-ROC as the primary metric, supplemented by F1 and FPR. We place particular emphasis on FPR because benign traffic vastly outnumbers malicious events, so even a low FPR can generate many false alerts in high-volume networks.

## B. End-to-end Performance Evaluation

We evaluate the end-to-end performance of both DualGuard workflows under realistic dual-drift scenarios. Our evaluation methodology reflects the distinct challenges each workflow is designed to address, as identified in our empirical investigations.

1) DualGuard-Classifier Performance: The classifier workflow’s performance is evaluated against the two primary challenges identified in our empirical study: MMD from new malware and spatial ND from environmental changes.

MMD Evaluation. As summarized in Table III, DualGuard consistently outperforms adaptive baselines under unseen families across both datasets. On the CICIDS2017 dataset, DualGuard achieves an F1 score of 97.34%, substantially outperforming the non-adaptive baseline by 38.20%. The gains are stable rather than idiosyncratic, indicating that the recognition–adaptation split captures novel malicious structure instead of overfitting to a few high-confidence cases.

Robustness to the known/unknown split. To check that these gains do not hinge on one particular choice of heldout families, we repeat the MMD evaluation over five random known/unknown partitions per dataset, with split sizes fixed at 9/4 for CICIDS2017 and 5/4 for DAPT2020 (Table VI). On both datasets the mean F1 closely matches the fixed-split result (97.57±3.00 vs. 97.34 on CICIDS2017; 79.02±1.55 vs. 79.14 on DAPT2020), with small variance across partitions. This confirms that the partition used in our main experiments is representative rather than cherry-picked.

Spatial ND Evaluation. Table IV shows DualGuard attains the best overall recovery while preserving family discrimination (F1 99.11% on CICIDS2017 and 79.80% on DAPT2020), validating that environment-aware updates in the shared core mitigate spatial ND without destabilizing the classifier. These results also constitute a direct static-versus-adaptive comparison under spatial ND in isolation: the No-Update baseline is the static model that performs no adaptation, whereas DualGuard performs environment-aware adaptation. Adaptation alone raises F1 from 84.63% to 99.11% on CICIDS2017 and from 60.57% to 79.80% on DAPT2020, with the corresponding result for the anomaly-detection workflow reported in Table VII.

Concurrent Drift Evaluation. The MMD + spatial ND setting tests the system’s ability to handle the complex interplay between different drift types without mutual interference. The results, presented in Table V, underscore that DualGuard maintains near pre-drift accuracy while alternatives degrade (F1 98.45% on CICIDS2017 and 78.37% on DAPT2020). The superior recovery under concurrent drift validates the intended role of the explicit gate: it allows DualGuard to adapt to spatial shifts in benign traffic while simultaneously characterizing novel malicious behavior.

TABLE III: Classifier performance against MMD

<table><tr><td rowspan="2"></td><td colspan="4">CICIDS2017</td><td colspan="4">DAPT2020</td></tr><tr><td>Accuracy</td><td> $\Delta$ Acc</td><td>F1</td><td> $\Delta$ F1</td><td>Accuracy</td><td> $\Delta$ Acc</td><td>F1</td><td> $\Delta$ F1</td></tr><tr><td>No-Update</td><td>69.16%</td><td>-</td><td>59.14%</td><td>-</td><td>72.44%</td><td>-</td><td>60.99%</td><td>-</td></tr><tr><td>CADE</td><td>84.58%</td><td>+15.42%</td><td>79.10%</td><td>+19.96%</td><td>74.45%</td><td>+2.01%</td><td>67.98%</td><td>+6.99%</td></tr><tr><td>Transcendent</td><td>90.52%</td><td>+21.36%</td><td>87.20%</td><td>+28.06%</td><td>78.07%</td><td>+5.63%</td><td>73.96%</td><td>+12.97%</td></tr><tr><td>UnDiff</td><td>93.24%</td><td>+24.08%</td><td>92.77%</td><td>+33.63%</td><td>74.97%</td><td>+2.53%</td><td>68.22%</td><td>+7.23%</td></tr><tr><td>DualGuard</td><td>97.36%</td><td>+28.20%</td><td>97.34%</td><td>+38.20%</td><td>79.01%</td><td>+6.57%</td><td>79.14%</td><td>+18.15%</td></tr></table>

TABLE IV: Classifier performance against spatial ND

<table><tr><td rowspan="2"></td><td colspan="4">CICIDS2017</td><td colspan="4">DAPT2020</td></tr><tr><td>Accuracy</td><td> $\Delta$ Acc</td><td>F1</td><td> $\Delta$ F1</td><td>Accuracy</td><td> $\Delta$ Acc</td><td>F1</td><td> $\Delta$ F1</td></tr><tr><td>No-Update</td><td>84.02%</td><td>-</td><td>84.63%</td><td>-</td><td>58.85%</td><td>-</td><td>60.57%</td><td>-</td></tr><tr><td>CADE</td><td>87.39%</td><td>+3.37%</td><td>87.36%</td><td>+2.73%</td><td>73.90%</td><td>+15.05%</td><td>75.75%</td><td>+15.18%</td></tr><tr><td>Transcendent</td><td>96.20%</td><td>+12.18%</td><td>96.89%</td><td>+12.26%</td><td>61.50%</td><td>+2.65%</td><td>63.94%</td><td>+3.37%</td></tr><tr><td>UnDiff</td><td>98.69%</td><td>+14.67%</td><td>98.70%</td><td>+14.07%</td><td>68.70%</td><td>+9.85%</td><td>71.34%</td><td>+10.77%</td></tr><tr><td>DualGuard</td><td>99.25%</td><td>+15.23%</td><td>99.11%</td><td>+14.48%</td><td>77.93%</td><td>+19.08%</td><td>79.80%</td><td>+19.23%</td></tr></table>

TABLE V: Classifier performance under MMD + spatial ND

<table><tr><td rowspan="2"></td><td colspan="4">CICIDS2017</td><td colspan="4">DAPT2020</td></tr><tr><td>Accuracy</td><td>ΔAcc</td><td>F1</td><td>ΔF1</td><td>Accuracy</td><td>ΔAcc</td><td>F1</td><td>ΔF1</td></tr><tr><td>No-Update</td><td>69.09%</td><td>-</td><td>64.71%</td><td>-</td><td>58.62%</td><td>-</td><td>57.72%</td><td>-</td></tr><tr><td>CADE</td><td>69.18%</td><td>+0.09%</td><td>64.82%</td><td>+0.11%</td><td>74.53%</td><td>+15.91%</td><td>71.42%</td><td>+13.70%</td></tr><tr><td>Transcendent</td><td>89.12%</td><td>+20.03%</td><td>85.91%</td><td>+21.20%</td><td>64.78%</td><td>+6.16%</td><td>62.36%</td><td>+4.64%</td></tr><tr><td>UnDiff</td><td>84.07%</td><td>+14.98%</td><td>82.04%</td><td>+17.33%</td><td>69.95%</td><td>+11.33%</td><td>68.19%</td><td>+10.47%</td></tr><tr><td>DualGuard</td><td>98.22%</td><td>+29.13%</td><td>98.45%</td><td>+33.74%</td><td>77.96%</td><td>+19.34%</td><td>78.37%</td><td>+20.65%</td></tr></table>

TABLE VI: Robustness to the known/unknown partition: DualGuard MMD performance over five random partitions per dataset (mean±std, %).

<table><tr><td>Dataset</td><td>Accuracy (%)</td><td>F1 (%)</td></tr><tr><td>CICIDS2017</td><td>97.84±2.59</td><td>97.57±3.00</td></tr><tr><td>DAPT2020</td><td>78.13±1.68</td><td>79.02±1.55</td></tr></table>

2) DualGuard-Anomaly Performance: The anomaly detection workflow’s performance is evaluated against both spatial ND and temporal ND.

Spatial ND Evaluation. Across all three detectors, Dual-Guard delivers substantial FPR reductions while maintaining or improving F1 (Table VII). The results reveal a critical trade-off: some competing methods reduce FPR only at the cost of severe F1 degradation. For instance, on CICIDS2017 with LOF detector, Transcendent reduces FPR by 67.90% but experiences a dramatic 36.02% decline in F1 score. In contrast, DualGuard achieves substantial FPR reductions while maintaining or even improving F1 scores.

Temporal ND Evaluation. We conduct a longitudinal evaluation to examine the temporal adaptation capability under the Single Adaptation setting, where each method performs a one-time drift adaptation at a designated time point (@T1) and subsequently employs the adapted model for detection over later periods (@T2–@T5). As discussed in Section III, temporal ND primarily manifests as an increase in FPR, thus we focus our analysis on FPR dynamics.

As shown in Fig. 5, DualGuard exhibits advantages in both immediate adaptation and long-term stability. When drift is introduced at @T1, DualGuard shows the smallest FPR increase across all detectors and datasets.

More importantly, DualGuard sustains this advantage throughout subsequent periods (@T2–@T5). While competing approaches show pronounced fluctuations and cumulative FPR degradation, DualGuard maintains a consistently low and stable FPR. This combination of swift initial adaptation and enduring temporal robustness underscores its suitability for real-world deployment, ensuring sustained resilience against false alarms in dynamic network environments.

![](images/753f4a44be1cc588f462162415d412a1389b35d2bde0de5172b37b8deaacb919.jpg)  
No-Update  CADETranscendentUnDiffDualGuard (ours)  
Fig. 5: Temporal ND adaptation performance: FPR over five periods after one-time adaptation at T1.

TABLE VII: Anomaly detection performance against spatial ND

<table><tr><td rowspan="2">Detector</td><td rowspan="2">Model</td><td colspan="6">CICIDS2017</td><td colspan="6">DAPT2020</td></tr><tr><td>AUC</td><td>ΔAUC</td><td>F1</td><td>ΔF1</td><td>FPR</td><td>ΔFPR</td><td>AUC</td><td>ΔAUC</td><td>F1</td><td>ΔF1</td><td>FPR</td><td>ΔFPR</td></tr><tr><td rowspan="5">Isolation Forest [39]</td><td>No-Update</td><td>80.28%</td><td>-</td><td>85.27%</td><td>-</td><td>72.33%</td><td>-</td><td>74.01%</td><td>-</td><td>77.69%</td><td>-</td><td>55.47%</td><td>-</td></tr><tr><td>CADE</td><td>83.54%</td><td>+3.26%</td><td>85.58%</td><td>+0.31%</td><td>38.39%</td><td>-33.94%</td><td>82.30%</td><td>+8.29%</td><td>73.22%</td><td>-4.47%</td><td>22.70%</td><td>-32.77%</td></tr><tr><td>Transcendent</td><td>93.56%</td><td>+13.28%</td><td>75.97%</td><td>-9.30%</td><td>2.04%</td><td>-70.29%</td><td>62.80%</td><td>+8.79%</td><td>33.89%</td><td>-23.80%</td><td>19.76%</td><td>-35.71%</td></tr><tr><td>UnDiff</td><td>86.70%</td><td>+6.42%</td><td>90.08%</td><td>+4.81%</td><td>13.70%</td><td>-58.63%</td><td>75.83%</td><td>+1.82%</td><td>67.73%</td><td>-9.96%</td><td>40.33%</td><td>-15.14%</td></tr><tr><td>DualGuard</td><td>99.29%</td><td>+19.01%</td><td>95.56%</td><td>+10.29%</td><td>21.26%</td><td>-51.07%</td><td>83.90%</td><td>+9.89%</td><td>77.17%</td><td>-0.52%</td><td>31.34%</td><td>-24.13%</td></tr><tr><td rowspan="5">SVM [40]</td><td>No-Update</td><td>99.95%</td><td>-</td><td>84.22%</td><td>-</td><td>85.67%</td><td>-</td><td>65.81%</td><td>-</td><td>68.07%</td><td>-</td><td>52.06%</td><td>-</td></tr><tr><td>CADE</td><td>88.93%</td><td>-11.02%</td><td>81.71%</td><td>-2.51%</td><td>72.61%</td><td>-13.06%</td><td>62.71%</td><td>-3.10%</td><td>67.36%</td><td>-0.71%</td><td>19.11%</td><td>-32.95%</td></tr><tr><td>Transcendent</td><td>98.08%</td><td>-1.87%</td><td>88.89%</td><td>+4.67%</td><td>57.14%</td><td>-28.53%</td><td>79.52%</td><td>+13.71%</td><td>45.88%</td><td>-22.19%</td><td>11.99%</td><td>-40.07%</td></tr><tr><td>UnDiff</td><td>75.18%</td><td>-24.77%</td><td>82.66%</td><td>-1.56%</td><td>47.40%</td><td>-38.27%</td><td>80.20%</td><td>+14.39%</td><td>48.27%</td><td>-19.80%</td><td>17.67%</td><td>-34.39%</td></tr><tr><td>DualGuard</td><td>99.87%</td><td>-0.08%</td><td>95.77%</td><td>+11.55%</td><td>20.19%</td><td>-65.48%</td><td>81.10%</td><td>+15.29%</td><td>69.81%</td><td>+1.74%</td><td>25.71%</td><td>-26.35%</td></tr><tr><td rowspan="5">LOF [41]</td><td>No-Update</td><td>98.41%</td><td>-</td><td>85.89%</td><td>-</td><td>75.11%</td><td>-</td><td>52.16%</td><td>-</td><td>78.83%</td><td>-</td><td>63.59%</td><td>-</td></tr><tr><td>CADE</td><td>85.20%</td><td>-13.21%</td><td>86.94%</td><td>+1.05%</td><td>24.16%</td><td>-50.95%</td><td>78.43%</td><td>+26.27%</td><td>76.97%</td><td>-1.86%</td><td>26.36%</td><td>-37.23%</td></tr><tr><td>Transcendent</td><td>58.00%</td><td>-40.41%</td><td>49.87%</td><td>-36.02%</td><td>7.21%</td><td>-67.90%</td><td>77.07%</td><td>+24.91%</td><td>64.14%</td><td>-14.69%</td><td>22.70%</td><td>-40.89%</td></tr><tr><td>UnDiff</td><td>82.07%</td><td>-16.34%</td><td>86.20%</td><td>+0.31%</td><td>14.27%</td><td>-60.84%</td><td>54.42%</td><td>+2.26%</td><td>55.68%</td><td>-23.15%</td><td>43.36%</td><td>-20.23%</td></tr><tr><td>DualGuard</td><td>99.99%</td><td>+1.58%</td><td>97.72%</td><td>+11.83%</td><td>10.64%</td><td>-64.47%</td><td>78.60%</td><td>+26.44%</td><td>82.66%</td><td>+3.83%</td><td>34.20%</td><td>-29.39%</td></tr></table>

TABLE VIII: Anomaly detection performance under concurrent temporal ND and spatial ND

<table><tr><td rowspan="2">Detector</td><td rowspan="2">Model</td><td colspan="6">CICIDS2017</td><td colspan="6">DAPT2020</td></tr><tr><td>AUC</td><td>ΔAUC</td><td>F1</td><td>ΔF1</td><td>FPR</td><td>ΔFPR</td><td>AUC</td><td>ΔAUC</td><td>F1</td><td>ΔF1</td><td>FPR</td><td>ΔFPR</td></tr><tr><td rowspan="5">Isolation Forest [39]</td><td>No-Update</td><td>73.74%</td><td>-</td><td>84.69%</td><td>-</td><td>77.30%</td><td>-</td><td>63.12%</td><td>-</td><td>64.66%</td><td>-</td><td>60.00%</td><td>-</td></tr><tr><td>CADE</td><td>89.23%</td><td>+15.49%</td><td>91.35%</td><td>+6.66%</td><td>43.23%</td><td>-34.07%</td><td>66.50%</td><td>+3.38%</td><td>63.44%</td><td>-1.22%</td><td>58.78%</td><td>-1.22%</td></tr><tr><td>Transcendent</td><td>79.38%</td><td>+5.64%</td><td>76.39%</td><td>-8.30%</td><td>45.67%</td><td>-31.63%</td><td>75.16%</td><td>+12.04%</td><td>44.73%</td><td>-19.93%</td><td>18.01%</td><td>-41.99%</td></tr><tr><td>UnDiff</td><td>86.66%</td><td>+12.92%</td><td>91.17%</td><td>+6.48%</td><td>39.57%</td><td>-37.73%</td><td>68.27%</td><td>+5.15%</td><td>41.82%</td><td>-2.84%</td><td>56.99%</td><td>-3.01%</td></tr><tr><td>DualGuard</td><td>96.34%</td><td>+22.60%</td><td>95.14%</td><td>+10.45%</td><td>19.34%</td><td>-57.96%</td><td>86.78%</td><td>+23.66%</td><td>81.93%</td><td>+17.27%</td><td>28.74%</td><td>-31.26%</td></tr><tr><td rowspan="5">SVM [40]</td><td>No-Update</td><td>47.89%</td><td>-</td><td>85.02%</td><td>-</td><td>80.54%</td><td>-</td><td>58.93%</td><td>-</td><td>66.29%</td><td>-</td><td>74.01%</td><td>-</td></tr><tr><td>CADE</td><td>72.00%</td><td>+24.11%</td><td>63.77%</td><td>-21.25%</td><td>22.20%</td><td>-58.34%</td><td>43.66%</td><td>-15.27%</td><td>77.65%</td><td>+11.36%</td><td>98.69%</td><td>+24.68%</td></tr><tr><td>Transcendent</td><td>53.20%</td><td>+5.31%</td><td>88.32%</td><td>+3.30%</td><td>84.69%</td><td>+4.15%</td><td>50.81%</td><td>-8.12%</td><td>6.63%</td><td>-59.66%</td><td>14.73%</td><td>-59.28%</td></tr><tr><td>UnDiff</td><td>61.77%</td><td>+13.88%</td><td>63.96%</td><td>-21.06%</td><td>24.49%</td><td>-56.05%</td><td>65.27%</td><td>+6.34%</td><td>57.39%</td><td>-8.90%</td><td>63.94%</td><td>-10.07%</td></tr><tr><td>DualGuard</td><td>93.16%</td><td>+45.27%</td><td>95.36%</td><td>+10.34%</td><td>18.56%</td><td>-61.98%</td><td>84.63%</td><td>+25.70%</td><td>87.93%</td><td>+21.64%</td><td>31.23%</td><td>-42.78%</td></tr><tr><td rowspan="5">LOF [41]</td><td>No-Update</td><td>41.46%</td><td>-</td><td>85.24%</td><td>-</td><td>79.13%</td><td>-</td><td>49.31%</td><td>-</td><td>77.86%</td><td>-</td><td>69.63%</td><td>-</td></tr><tr><td>CADE</td><td>60.39%</td><td>+18.93%</td><td>72.44%</td><td>-12.80%</td><td>41.71%</td><td>-37.42%</td><td>43.20%</td><td>-6.11%</td><td>77.42%</td><td>-0.44%</td><td>78.00%</td><td>+8.37%</td></tr><tr><td>Transcendent</td><td>89.40%</td><td>+47.94%</td><td>94.47%</td><td>+9.23%</td><td>26.66%</td><td>-52.47%</td><td>68.66%</td><td>+19.35%</td><td>60.44%</td><td>-17.42%</td><td>22.39%</td><td>-47.24%</td></tr><tr><td>UnDiff</td><td>73.14%</td><td>+31.68%</td><td>75.64%</td><td>-9.60%</td><td>17.67%</td><td>-61.46%</td><td>73.57%</td><td>+24.26%</td><td>77.79%</td><td>-0.07%</td><td>31.66%</td><td>-37.97%</td></tr><tr><td>DualGuard</td><td>97.42%</td><td>+55.96%</td><td>98.49%</td><td>+13.25%</td><td>19.63%</td><td>-59.50%</td><td>86.01%</td><td>+36.70%</td><td>89.16%</td><td>+11.30%</td><td>29.44%</td><td>-40.19%</td></tr></table>

Concurrent Drift Evaluation. Under simultaneous temporal and spatial shifts, as shown in Table VIII, the concurrent drift causes a catastrophic failure for the non-adaptive models, with AUC scores on CICIDS2017 approaching random guessing (50%). While some baselines achieve partial recovery, they do so at the cost of significant performance degradation in other aspects. For instance, on DAPT2020 with SVM, Transcendent achieves the lowest FPR but at the cost of a near-total collapse in its F1 score (6.63%).

In stark contrast, DualGuard achieves the highest AUC and F1 scores by a significant margin while simultaneously delivering dramatic FPR reductions (-61.98% for SVM). This demonstrates that DualGuard effectively adapts the normality baseline to counteract the severe impact of combined drift types, maintaining high detection efficacy while minimizing operational burden from false positives.

3) Trade-off between Labeling Overhead and Adaptation Performance: We evaluate the efficiency of our value-aware sampling using the DualGuard-Classifier workflow under MMD, representing the most challenging scenario requiring expert characterization of diverse threat types.

As shown in Fig. 6, the labeling budget is a fraction of a fixed candidate pool of N=8,000 drifted samples (0.5%=40 labels, 100%=8,000). With only 40 labels, DualGuard attains an F1 of 78.14%, whereas the three adaptive baselines remain near 64% at the same budget and reach a comparable F1 only at the full pool. DualGuard therefore matches the best fullbudget baseline while using 8,000/40=200× fewer labels. The non-adaptive No-Update baseline uses no labels and serves as a static reference.

## C. Component-wise Ablation Study

To validate the effectiveness of individual components within DualGuard, we conduct comprehensive ablation studies isolating each module’s contribution to overall performance. Our analysis focuses on three core innovations: the drift detection module, the fine-grained clustering mechanism, and the value-aware sample selection strategy.

Drift Detection Module Ablation: Hierarchical vs. Traditional Contrastive Learning. To quantify the contribution of our hierarchical contrastive learning method, we replaced it with a traditional contrastive learning (TCL) approach. The TCL baseline was trained to distinguish only between benign and malicious traffic in a binary manner, without the multilevel constraints of HCL that enforce separation between different malware families. We evaluated both approaches within the DualGuard-Classifier workflow under a concurrent drift scenario on the CICIDS2017 dataset. As shown in Table IX, the HCL-based module significantly outperforms the TCL baseline, achieving a 12.58% higher F1 score in identifying drifted samples. This demonstrates that by learning a more structured and discriminative latent space, HCL provides a more robust foundation for distinguishing subtle normality drifts from genuine malicious mutations.

![](images/0a71fb7bca21ae1551dfae0701ba3d7e0f11e9d3fee4152b691f817a63a3592a.jpg)  
Fig. 6: Impact of labeling budget on classifier adaptation performance under MMD. Budget is a fraction of the $N { = } 8 { , } 0 0 0 { \cdot }$ sample candidate pool $( 0 . 5 \% { = } 4 0$ labels); the dashed line is DualGuard.

TABLE IX: Ablation of drift detection: Hierarchical (HCL) vs. Traditional (TCL) contrastive learning

<table><tr><td>Method</td><td>Accuracy</td><td>F1</td></tr><tr><td>DualGuard (w/ TCL)</td><td>84.15%</td><td>85.87%</td></tr><tr><td>DualGuard (w/ HCL, ours)</td><td>98.22%</td><td>98.45%</td></tr></table>

Gating-Statistic Ablation: Robust vs. Classical Standardization. The triage standardizes each per-class distance by a location and a scale estimate and gates a sample as MMD when its standardized score $s _ { \mathrm { m i n } }$ exceeds a single threshold $\theta _ { \mathrm { m m d } }$ fixed as an upper-tail quantile of the $T _ { 0 }$ scores (Section V-C2). To isolate the contribution of the robust statistic, we hold the HCL embedding, the class centroids, and the quantile-threshold rule fixed and replace only the median/MAD pair that defines $s _ { c }$ with the classical mean/standard-deviation pair; a one-sided $k \sigma$ rule and a mean/std z-score rule coincide under this scheme and are therefore reported as a single classical baseline. Because the threshold is a $T _ { 0 }$ quantile, both estimators are calibrated to the same operating point on $T _ { 0 }$ (a 1% false-trigger rate) and differ only in how faithfully that one-shot $T _ { 0 }$ calibration transfers to the drifted test stream. As reported in Table X, the operating point of the classical estimator degrades sharply after $T _ { 0 } .$ Its false-trigger rate increases from 1.00% to 4.57%, while novel-family recall decreases to 95.82%. This degradation occurs because the non-robust mean and standard deviation are affected by outlier in-class flows that are unavoidable in noisy network traffic, such as residual anomalies that remain after benign filtering. As a result, the per-class scale estimated by this approach does not transfer reliably beyond $T _ { 0 }$ (Section V-C2). The robust MAD estimator instead preserves the calibrated operating point and attains 99.13% novel-family recall and 99.1% AUPRC. This is exactly the property that lets the $\mathrm { o n c e - o n - } T _ { 0 }$ , leakage-free calibration of Section V-C2 transfer reliably under drift: the robust scale keeps the gate on its intended operating point without any test-time re-tuning.

TABLE X: Gating-statistic ablation (concurrent-drift CI-CIDS2017).

<table><tr><td>Estimator</td><td>FPRdrift</td><td>Recall</td><td>AUPRC</td></tr><tr><td>Classical (mean/std)</td><td>4.57%</td><td>95.82%</td><td>95.9%</td></tr><tr><td>Robust (MAD), ours</td><td>1.21%</td><td>99.13%</td><td>99.1%</td></tr></table>

Fine-grained Clustering Evaluation: Ensemble vs. Single Algorithm. We assessed the effectiveness of our ensemble clustering approach by comparing it against its individual component algorithms (K-Means, DBSCAN, DEC). We used the silhouette score on the set of drifted samples to measure clustering quality, where a higher score indicates betterdefined and more separated clusters. The results, summarized in Table XI, show that the ensemble method achieves a silhouette score of 85.28%, an absolute increase of 16.23 percentage points over the best-performing single algorithm, DEC (69.05%). This superiority stems from the ensemble’s ability to mitigate the inherent biases of any single method, resulting in a more accurate and robust recovery of the underlying structure of novel threats.

TABLE XI: Ablation of fine-grained clustering: Ensemble vs. single-algorithm performance

<table><tr><td>Clustering Method</td><td>Silhouette Score</td></tr><tr><td>K-Means</td><td>62.39%</td></tr><tr><td>DBSCAN</td><td>55.82%</td></tr><tr><td>DEC</td><td>69.05%</td></tr><tr><td>Ensemble (Ours)</td><td>85.28%</td></tr></table>

Value-aware Sample Selection Assessment. To evaluate our value-aware sampling strategy, we quantified its performance by varying two key parameters: the number of representative prototypes selected for labeling and the proportion of cluster samples that receive propagated labels. For clarity, we analyzed each parameter independently using a control variable approach on the CICIDS2017 dataset under an MMD scenario.

First, we fixed the label propagation ratio at 90% and varied the number of prototypes selected per discovered cluster from 1 to 5. As illustrated in Fig. 7(a), performance gains are most substantial when selecting the first one to three prototypes, with the F1 score rising sharply. The marginal return diminishes with additional prototypes, indicating that our selection strategy effectively identifies the most informative samples early. This supports our strategy’s premise that a few wellchosen prototypes can capture the core characteristics of a novel threat cluster.

![](images/9f0bd9bba0e55ab659dbd828a71a1da9b96460de56a0e288d1aa92857648f429.jpg)

![](images/bd409471b62bbf24e1f057f48c53d66e1e30d50c78087b8c0bdb44ca72e0a046.jpg)  
Fig. 7: Ablation of value-aware sampling: (a) Impact of prototype count on F1 score. (b) Impact of label propagation ratio on F1 score.

Second, we fixed the number of prototypes at three per cluster—the point of diminishing returns identified above—and varied the label propagation ratio. Fig. 7(b) shows that performance improves as the propagation ratio increases, peaking at approximately 90%. Beyond this point, a slight decline is observed. This outcome aligns with the practical reality that no clustering is perfect; propagating labels to 100% of samples risks including noisy instances from the cluster periphery, which can marginally degrade model performance. This demonstrates that the propagation ratio acts as a valuable control mechanism, allowing the system to leverage highquality clusters for reliable label extension while mitigating the impact of potential outliers.

Although we analyze these factors independently for experimental clarity, they are linked in a practical deployment. The number of prototypes and the consistency of their expertassigned labels can inform the optimal propagation ratio, creating a dynamic and robust adaptation loop.

Exemplar Rehearsal and Catastrophic Forgetting. A practical deployment must integrate newly discovered families without eroding its accuracy on the families it has already learned. We isolate the exemplar-rehearsal mechanism of the incremental update: starting from the same $T _ { 0 }$ model, both arms expand the classifier head to the new families and finetune, differing only in whether the $T _ { 0 }$ -known exemplars are replayed. On the classifier MMD setting (CICIDS2017), after adapting to the $T _ { 1 }$ unknown families, we measure the per-class F1 on the $T _ { 0 } .$ -known families. As Table XII shows, rehearsal retains the known attack families near their pre-adaptation level (mean F1 98.75%), whereas removing it degrades them by over 30 points (to 65.72%). This confirms that the rehearsal mechanism is what mitigates catastrophic forgetting.

TABLE XII: Mean per-class F1 (%) with vs. without exemplar rehearsal.

<table><tr><td>Configuration</td><td> $T_0$ -known F1</td><td>New-family F1</td></tr><tr><td>DualGuard (w/o rehearsal)</td><td>65.72%</td><td>71.67%</td></tr><tr><td>DualGuard (w/ rehearsal, ours)</td><td>98.75%</td><td>93.36%</td></tr></table>

![](images/76fbd544c4e48f99b37045075e97d53fdb796e9081548b4419a24534317dc5f4.jpg)  
-- No-Update-- CADE-- Transcendent- UnDiff DualGuard  
Fig. 8: Sensitivity to dataset-mismatch severity under spatial ND.

## D. Sensitivity to Dataset-Mismatch Severity

To examine robustness as the source–target mismatch intensifies, we vary the proportion $\rho$ of target-domain benign traffic in the post-drift benign stream from 0% to 100%, holding the attack composition, training set, and adaptation budget fixed. At $\rho { = } 0 \%$ , the post-drift benign stream contains no targetdomain traffic, whereas $\rho { = } 1 0 0 \%$ recovers the full spatial ND setting of Table IV and Table VII. MMD and temporal ND are evaluated separately through the unknown-family MMD splits and the longitudinal MAWI stages reported above.

As shown in Fig. 8, increasing $\rho$ steadily degrades the non-adaptive model and only partially affects the adaptive baselines, whereas DualGuard remains the most stable and retains the largest margin at every level. The gap is widest on the more challenging DAPT2020, where the No-Update classifier F1 falls to 60.57% at $\rho { = } 1 0 0 \%$ while DualGuard retains 79.80%. Since this endpoint coincides with Table IV and Table VII, the analysis extends the fixed cross-dataset evaluation along a continuous target-benign prevalence axis and confirms that DualGuard remains robust as the aggregate cross-environment mismatch increases.

Gate-threshold sensitivity. Under ±10% perturbations of each gate threshold, accuracy and F1 vary by at most 0.17 percentage points, indicating that the reported gains do not depend on a finely tuned operating point (Supplementary Table S8).

## VII. EVALUATION ON REAL-WORLD ISP TRAFFIC

To demonstrate DualGuard’s effectiveness under real-world conditions, we conducted a large-scale evaluation using traffic collected in collaboration with an ISP vendor. The evaluation targeted the malicious-traffic classification task and used highconfidence Suricata alerts generated from a curated subset of the ET Ruleset as an operational reference rather than absolute ground truth.

Traffic was collected from a 40 Gbps egress node at the ISP’s last hop to the public Internet and evaluated by offline replay of the extracted flow records. Benign-reference background traffic was obtained by mirroring the live stream and discarding any flows that triggered ET Ruleset signatures; this stream represents the production environment in which the model must operate. The initial model was trained on a mixture of (i) historical attack traces from the Malware Traffic Analysis archive and the ANY.RUN sandbox (2015–2025), selected to emphasize APT campaigns, and (ii) the rulefiltered benign-reference traffic described above. This dataset reflects the typical knowledge available to a defender prior to deployment.

To construct the MMD candidate pool, we configured a Suricata sensor with the up-to-date ET Ruleset on the same link and captured all previously unseen, rule-matched flows during the 11-month trial. The resulting pool represents newly observed, signature-visible threat behaviors.

Two complementary sources were used to emulate ND. First, one year after the initial baseline was recorded we collected a fresh 24-hour slice of the ISP’s outbound traffic, again filtering it with ET Ruleset to obtain ET-negative benignreference flows; this slice embodies temporal ND. Second, we injected benign flows from the 2025 MAWI backbone trace to model spatial ND stemming from deployment in a topologically dissimilar network.

For reproducibility, Table XIII reports the traffic-collection window, ET ruleset version, Suricata sensor setup, and the flow counts used in the training and offline-replay evaluation sets. Importantly, ET hits were not used as positive labels without filtering. We first performed signature-level curation, retaining only high-confidence malware-related signatures (malware, C2/CNC, exploit, trojan, downloader, and exfiltration) while discarding policy, informational, scan-only, and ambiguous alerts. This process yielded 11,866 curated ET-matched MMD candidate flows. These samples are disjoint from the training set according to sample identifiers, reducing the risk of training contamination.

Although this high-confidence curation reduces obvious false positives, residual false alerts may remain, while malicious traffic outside the retained signature coverage may enter the ET-negative pool. Rule coverage and signature design can therefore bias the evaluation toward signature-visible behaviors. Manual verification was conducted during signature selection: analysts reviewed the retained high-confidence categories before the reference set was finalized. Together, this high-confidence curation and manual review establish a carefully curated operational reference for the ISP-scale experiment.

Table XIV reports the accuracy and F1 score of DualGuard and three state-of-the-art adaptive baselines after the full adaptation cycle. The static no-update model suffers a dramatic collapse, its F1 score dropping below 68%, confirming that concurrent MMD and ND severely undermine non-adaptive detectors. Existing adaptive methods restore part of the lost performance: CADE and Transcendent recover roughly 17% and 10% of F1 respectively, while the stronger UnDiff regains about 21%. DualGuard, however, achieves an F1 score of 96.87%, recovering nearly 30 percentage points and surpassing the best baseline by 8.73%.

TABLE XIII: Real-world ISP traffic collection and referenceset composition.

<table><tr><td>Item</td><td>Value</td></tr><tr><td>Traffic-collection period</td><td>June 2024 – April 2025</td></tr><tr><td>Monitored egress-link capacity</td><td>40 Gbps</td></tr><tr><td>Reference-label source</td><td>ET Open Ruleset v10587</td></tr><tr><td>Sensor</td><td>Suricata 7.0.6 RELEASE</td></tr><tr><td>Key capabilities</td><td>AF_PACKET capture, NFQUEUE, packet fanout, TLS parsing, Lua/LuaJIT, JSON output, Rust support</td></tr><tr><td>Training set</td><td>19,996 flows: 9,996 malware and 10,000 rule-filtered benign-reference flows</td></tr><tr><td>Evaluation set</td><td>16,866 flows: 11,866 curated ET-matched MMD candidates and 5,000 benign-reference flows (2,500 from each ND source)</td></tr></table>

TABLE XIV: Classifier performance on real-world ISP traffic

<table><tr><td rowspan="2"></td><td colspan="4">Real-world data</td></tr><tr><td>Accuracy</td><td> $\Delta$ Acc</td><td>F1</td><td> $\Delta$ F1</td></tr><tr><td>No-Update</td><td>67.28%</td><td>-</td><td>67.46%</td><td>-</td></tr><tr><td>CADE</td><td>84.59%</td><td>+17.31%</td><td>84.87%</td><td>+17.41%</td></tr><tr><td>Transcendent</td><td>79.95%</td><td>+12.67%</td><td>77.79%</td><td>+10.33%</td></tr><tr><td>UnDiff</td><td>90.14%</td><td>+22.86%</td><td>88.14%</td><td>+20.68%</td></tr><tr><td>DualGuard</td><td>96.46%</td><td>+29.18%</td><td>96.87%</td><td>+29.41%</td></tr></table>

## VIII. CODE AND DATA AVAILABILITY

The source code, configuration, and feature schema are publicly available at https://github.com/ghostghost66/DualGuard. The ISP packet captures and flow records cannot be released because they may reveal subscriber activity and operator topology; complete in-house security rules are withheld because disclosure could weaken operational monitoring; and raw third-party sandbox traces remain subject to provider-specific terms.

## IX. CONCLUSION

This paper addressed the critical and largely overlooked challenge of dual concept drift in network security, where concurrent MMD and ND degrade detection systems. We introduced DualGuard, a framework featuring a unified drift detection core and scenario-specific workflows. DualGuard resolves the critical performance trade-off, improving F1 scores by 21.64% while slashing false positives by 42.78% in complex concurrent drift settings. The framework’s practical readiness was confirmed in a real-world ISP deployment, where it achieved a 96.87% F1 score, outperforming the best adaptive baseline by a significant 8.73%. These results validate DualGuard as a powerful, efficient, and practical solution for building resilient network security analytics.

## REFERENCES

[1] N. Malekghaini, E. Akbari, M. A. Salahuddin, N. Limam, R. Boutaba, B. Mathieu, S. Moteau, and S. Tuffin, “Data drift in dl: Lessons learned from encrypted traffic classification,” in 2022 IFIP Networking Conference (IFIP Networking). IEEE, 2022, pp. 1–9.

[2] B. Anderson and D. McGrew, “Machine learning for encrypted malware traffic classification: accounting for noisy labels and non-stationarity,” in Proceedings of the 23rd ACM SIGKDD International Conference on knowledge discovery and data mining, 2017, pp. 1723–1732.

[3] M. Dragoi, E. Burceanu, E. Haller, A. Manolache, and F. Brad, “Anoshift: A distribution shift benchmark for unsupervised anomaly detection,” Advances in Neural Information Processing Systems, vol. 35, pp. 32 854–32 867, 2022.

[4] M. A. Shyaa, N. F. Ibrahim, Z. Zainol, R. Abdullah, M. Anbar, and L. Alzubaidi, “Evolving cybersecurity frontiers: A comprehensive survey on concept drift and feature dynamics aware machine and deep learning in intrusion detection systems,” Engineering Applications of Artificial Intelligence, vol. 137, p. 109143, 2024.

[5] S. Li, F. Dong, X. Xiao, H. Wang, F. Shao, J. Chen, Y. Guo, X. Chen, and D. Li, “NODLINK: An online system for fine-grained APT attack detection and investigation,” in Proceedings of the 31st Network and Distributed System Security Symposium (NDSS), 2024.

[6] W. Han, J. Xue, Y. Wang, F. Zhang, and X. Gao, “APTMalInsight: Identify and cognize APT malware based on system call information and ontology knowledge framework,” Information Sciences, vol. 546, pp. 633–664, 2021.

[7] Cybersecurity and Infrastructure Security Agency (CISA), Federal Bureau of Investigation (FBI), and U.S. Department of the Treasury, “AppleJeus: Analysis of North Korea’s Cryptocurrency Malware,” Cybersecurity Advisory AA21-048A, Feb. 2021, [Online]. Available: https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-048a. Accessed: Aug. 7, 2026.

[8] “TraderTraitor: North Korean State-Sponsored APT Targets Blockchain Companies,” Cybersecurity Advisory AA22-108A, Apr. 2022, [Online]. Available: https://www.cisa.gov/news-events/ cybersecurity-advisories/aa22-108a. Accessed: Aug. 7, 2026.

[9] T. Qin, G. Cheng, Z. Chen, and Y. Zhou, “Prime: Plasticity-robust incremental model for encrypted traffic classification in dynamic network environments,” arXiv preprint arXiv:2508.02031, 2025.

[10] J. Yang, K. Zhou, Y. Li, and Z. Liu, “Generalized out-of-distribution detection: A survey,” Int. J. Comput. Vision, vol. 132, no. 12, p. 5635–5662, Jun. 2024.

[11] Y. Feng, J. Li, D. Sisodia, and P. Reiher, “On explainable and adaptable detection of distributed denial-of-service traffic,” IEEE Transactions on Dependable and Secure Computing, vol. 21, no. 4, pp. 2211–2226, 2024.

[12] N. Malekghaini, E. Akbari, M. A. Salahuddin, N. Limam, R. Boutaba, B. Mathieu, S. Moteau, and S. Tuffin, “Deep learning for encrypted traffic classification in the face of data drift: An empirical study,” Computer Networks, vol. 225, p. 109648, 2023.

[13] R. Jordaney, K. Sharad, S. K. Dash, Z. Wang, D. Papini, I. Nouretdinov, and L. Cavallaro, “Transcend: Detecting concept drift in malware classification models,” in 26th USENIX security symposium (USENIX security 17), 2017, pp. 625–642.

[14] F. Barbero, F. Pendlebury, F. Pierazzi, and L. Cavallaro, “Transcending transcend: Revisiting malware classification in the presence of concept drift,” in 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 2022, pp. 805–823.

[15] L. Yang, W. Guo, Q. Hao, A. Ciptadi, A. Ahmadzadeh, X. Xing, and G. Wang, “{CADE}: Detecting and explaining concept drift samples for security applications,” in 30th USENIX Security Symposium (USENIX Security 21), 2021, pp. 2327–2344.

[16] G. Andresini, F. Pendlebury, F. Pierazzi, C. Loglisci, A. Appice, and L. Cavallaro, “Insomnia: Towards concept-drift robustness in network intrusion detection,” in Proceedings of the 14th ACM workshop on artificial intelligence and security, 2021, pp. 111–122.

[17] D. Han, Z. Wang, W. Chen, K. Wang, R. Yu, S. Wang, H. Zhang, Z. Wang, M. Jin, J. Yang et al., “Anomaly detection in the open world: Normality shift detection, explanation, and adaptation.” in NDSS, 2023.

[18] X. Han, S. Cui, J. Qin, S. Liu, B. Jiang, C. Dong, Z. Lu, and B. Liu, “Contramtd: An unsupervised malicious network traffic detection method based on contrastive learning,” in Proceedings of the ACM Web Conference 2024, 2024, pp. 1680–1689.

[19] X. Lian, C. Cao, Y. Liu, X. Xu, Y. Zheng, and F. Zhou, “Facing anomalies head-on: Network traffic anomaly detection via uncertaintyinspired inter-sample differences,” in Proceedings of the ACM on Web Conference 2025, ser. WWW ’25. New York, NY, USA: Association for Computing Machinery, 2025, p. 3908–3917.

[20] Z. Chen, Z. Zhang, Z. Kan, L. Yang, J. Cortellazzi, F. Pendlebury, F. Pierazzi, L. Cavallaro, and G. Wang, “Is it overkill? analyzing featurespace concept drift in malware detectors,” in 2023 IEEE Security and Privacy Workshops (SPW), 2023, pp. 21–28.

[21] J. Lu, A. Liu, F. Dong, F. Gu, J. Gama, and G. Zhang, “Learning under concept drift: A review,” IEEE transactions on knowledge and data engineering, vol. 31, no. 12, pp. 2346–2363, 2018.

[22] X. Lin, G. Xiong, G. Gou, Z. Li, J. Shi, and J. Yu, “Et-bert: A contextualized datagram representation with pre-training transformers

for encrypted traffic classification,” in Proceedings of the ACM Web Conference 2022, ser. WWW ’22. New York, NY, USA: Association for Computing Machinery, 2022, p. 633–642.

[23] W. Peng, L. Cui, W. Cai, W. Wang, X. Cui, Z. Hao, and X. Yun, “Bottom aggregating, top separating: An aggregator and separator network for encrypted traffic understanding,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 1794–1806, 2025.

[24] A. Bendale and T. E. Boult, “Towards open set deep networks,” in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 1563–1572.

[25] S. Liang, Y. Li, and R. Srikant, “Enhancing the reliability of out-ofdistribution image detection in neural networks,” in 6th International Conference on Learning Representations, ICLR 2018, Vancouver, BC, Canada, April 30 - May 3, 2018, Conference Track Proceedings. OpenReview.net, 2018.

[26] W. Liu, X. Wang, J. Owens, and Y. Li, “Energy-based out-of-distribution detection,” Advances in neural information processing systems, vol. 33, pp. 21 464–21 475, 2020.

[27] X. Zhang, Y. Wang, T. Ohtsuki, G. Gui, C. Yuen, M. Di Renzo, and H. Sari, “Malware traffic classification via expandable class incremental learning with architecture search,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 6074–6085, 2025.

[28] H. Zhang, X. Xiao, L. Yu, Q. Li, Z. Ling, and Y. Zhang, “One train for two tasks: An encrypted traffic classification framework using supervised contrastive learning,” CoRR, vol. abs/2402.07501, 2024.

[29] K. Xu, L. Chen, and S. Wang, “Drift2matrix: Kernel-induced self representation for concept drift adaptation in co-evolving time series.” arXiv preprint arXiv:2501.01480, 2025.

[30] S. Cui, X. Han, D. Han, Z. Wang, W. Wang, B. Jiang, B. Liu, and Z. Lu, “Fg-sat: Efficient flow graph for encrypted traffic classification under environment shifts,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 5326–5339, 2025.

[31] R. Gupta, S. Liu, R. Zhang, X. Hu, X. Wang, H. Benkraouda, P. Kommaraju, P. Cao, N. Feamster, and K. Nahrstedt, “Generative active adaptation for drifting and imbalanced network intrusion detection,” arXiv preprint arXiv:2503.03022, 2025.

[32] X. Zhang, R. Zhao, Z. Jiang, H. Chen, Y. Ding, E. C. Ngai, and S.-H. Yang, “Continual learning with strategic selection and forgetting for network intrusion detection,” in IEEE INFOCOM 2025-IEEE Conference on Computer Communications. IEEE, 2025, pp. 1–10.

[33] N. FathimaAH, A. Khraisat, S. Ibrahim, and G. Li, “Adaptive memory replay for network intrusion detection: Tackling data drift and catastrophic forgetting,” Computer Networks, p. 111712, 2025.

[34] C. Zha, Z. Wang, Y. Fan, B. Bai, Y. Zhang, S. Shi, and R. Zhang, “Anids: Adaptive network intrusion detection system based on clustering and stacked ctgan,” IEEE Transactions on Information Forensics and Security, vol. 20, pp. 3204–3219, 2025.

[35] X. Wu, Z. Jin, X. Chen, J. Zhou, and K. Liu, “Boosting incremental intrusion detection system with adversarial samples,” Expert Systems with Applications, vol. 271, p. 126632, 2025.

[36] MAWI Working Group, “MAWI Working Group Traffic Archive,” https: //mawi.wide.ad.jp/mawi/, WIDE Project, accessed August 31, 2025.

[37] L. Liu, G. Engelen, T. Lynar, D. Essam, and W. Joosen, “Error prevalence in nids datasets: A case study on cic-ids-2017 and cse-cicids-2018,” in 2022 IEEE Conference on Communications and Network Security (CNS). IEEE, 2022, pp. 254–262.

[38] S. Myneni, A. Chowdhary, A. Sabur, S. Sengupta, G. Agrawal, D. Huang, and M. Kang, “Dapt 2020-constructing a benchmark dataset for advanced persistent threats,” in International workshop on deployable machine learning for security defense. Springer, 2020, pp. 138– 163.

[39] S. A. Elsaid and A. Binbusayyis, “An optimized isolation forest based intrusion detection system for heterogeneous and streaming data in the industrial internet of things (iiot) networks,” Discover Applied Sciences, vol. 6, no. 9, p. 483, 2024.

[40] K. Suresh, K. Jayasakthi Velmurugan, R. Vidhya, S. Rahini sudha, and Kavitha, “Deep anomaly detection: A linear one-class svm approach for high-dimensional and large-scale data,” Applied Soft Computing, vol. 167, p. 112369, 2024.

[41] R. Rabih, H. Vahdat-Nejad, W. Mansoor, and J. H. Joloudari, “Highly accurate anomaly based intrusion detection through integration of the local outlier factor and convolutional neural network,” Scientific Reports, vol. 15, no. 1, p. 21147, 2025.
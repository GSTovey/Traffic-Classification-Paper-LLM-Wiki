# ResAware: Cross-Environment Website Fingerprinting via Resource-Privileged Distillation

Chongru Fan

Chongrufan@bupt.edu.cn

Beijing University of Posts and

Telecommunications

Beijing, China

Zhongguancun Laboratory

Beijing, China

Wei Wang

Zhongguancun Laboratory

Beijing, China

Wentao Huang

Beijing University of Posts and

Telecommunications

Beijing, China

Zhenquan Ding∗

dingzq@zgclab.edu.cn

Zhongguancun Laboratory

Beijing, China

Jinqiao Shi†

shijinqiao@bupt.edu.cn

Beijing University of Posts and

Telecommunications

Beijing, China

Lei Cui

Zhongguancun Laboratory

Beijing, China

Zhiyu Hao

Zhongguancun Laboratory

Beijing, China

Xiaochun Yun

Zhongguancun Laboratory

Beijing, China

## Abstract

While Website Fingerprinting (WF) attacks achieve high accuracy in controlled laboratory settings, they often degrade substantially in real-world environments due to spatio-temporal drift, browser heterogeneity, proxy obfuscation and etc. This limitation stems from their sole reliance on low-level traffic features that are noisy and highly sensitive to environmental perturbations. To address this problem, we propose ResAware, a cross-environment resourceaware distillation framework under a training-rich/inference-poor asymmetric setting. Specifically, ResAware trains a teacher model on resource-level features, and then distills the resulting privileged knowledge into a student model through heterogeneous knowledge distillation. At deployment time, the student model performs inference using only encrypted traffic, incurring zero additional cost. We evaluate ResAware on a large-scale dataset collected over five months from six globally distributed vantage points, comprising more than 160,000 paired samples. The results show that ResAware significantly enhances the cross-environment robustness of diverse WF baselines. Under a 150-day temporal drift, for example, ResAware improves the F1-score of Var-CNN from 72.77% to 81.49% and the open-world ?? ????@1%?????? from 22.40% to 27.20%. Our results demonstrate that resource-level supervision improves WF robustness without expanding online observation capabilities.

## CCS Concepts

• Networks → Network privacy and anonymity; • Security and privacy → Pseudonymity, anonymity and untraceability;  
• Computing methodologies → Machine learning algorithms.

![](images/7203671480121cf7e9bcc30e28d6e32bd10ebee81bfd5dac1ffe2811eb198b98.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
  A["Application Layer Resource"] --> B[" HTML "]
  A --> C[" CSS "]
  A --> D[" PNG "]
  A --> E[" CSS "]
  A --> F[" JS "]
  G["Transport Layer Traffic"] --> H[" HTML "]
  G --> I[" CSS "]
  G --> J[" JS "]
  G --> K[" PNG "]
  G --> L[" JPG "]
  G --> M["Aa"]
  N["Website Static Definition"] --> O[" www.example.com "]
  P["Higher Stability"] --> Q[" Greater Stability "]
  R["Indentity"] --> S[" Architecture "]
  T[" Page Resources"] --> U[" Page Resources "]
  V[" Higher Volatility"] --> W[" Transport Layer Traffic "]
```
</details>

Figure 1: A website’s identity is reflected in its architecture and resource loading patterns. A browsing instance can be viewed as a sequence of resource deliveries, which, after being shaped by environmental noise, appears as the observable network traffic.

## Keywords

Website Fingerprinting, Encrypted Traffic Analysis, Knowledge Distillation, Cross-Environment Robustness

## 1 Introduction

With the widespread adoption of HTTPS and related encryption protocols, the contents of web traffic are now largely hidden from direct inspection [16, 32]. However, encryption does not eliminate side-channel leakage: observable traffic patterns, such as packet length, direction, and timing, can still reveal sensitive information about user activities. Website Fingerprinting (WF) exploits such leakage to infer visited websites from encrypted traffic traces [13, 15, 46], making it an important privacy threat to encrypted web communications.

Although deep learning-based WF models have achieved strong performance in closed, IID experimental settings [3, 10, 31, 39], a substantial deployment gap remains between laboratory scenarios and real-world network environments. In practice, traffic features are highly susceptible to temporal evolution, geographic variation, and obfuscated proxy protocol conversion, all of which induce significant distribution shifts [7, 8, 22, 38]. When a model is trained in one environment and evaluated in another with substantial feature discrepancies, the accuracy of mainstream WF models deteriorates markedly. This degradation suggests that existing models rely heavily on transient, environment-specific network artifacts and therefore generalize poorly across environments.

Prior work on mitigating this problem generally follows two trajectories. The first seeks more robust traffic representations through manual feature engineering, data augmentation, or contrastive learning [1, 36, 48]. The second adopts domain adaptation, such as few-shot fine-tuning or inference-time calibration on unlabeled target traffic [9, 40, 50]. Despite these efforts, existing methods remain confined to a traffic-only observational perspective: both training and inference rely exclusively on signals derived from encrypted traffic. Such signals are readily distorted by network variation, browser scheduling, and protocol encapsulation. As a result, current methods attempt to recover website identities from unstable observations, while overlooking the deterministic application-layer resources that give rise to these traffic patterns.

As illustrated in Figure 1, our key insight is that a website’s identity determines its application-layer resource composition and dependency patterns [25, 47]. During page loading, the resulting resource sequence reflects relatively stable website-specific loading logic. By contrast, the observed network traffic is only a noisy projection of this process, shaped by substantial stochasticity and environmental variation [19]. Recent resource-aware WF studies suggest that resource-level information enjoys a natural robustness advantage in cross-environment settings [5, 6, 12]. However, obtaining such information in practice typically requires traffic decryption or end-host compromise, both of which exceed the capabilities of a standard passive eavesdropper [27].

To exploit resource-level stability without expanding the online attack surface, we formalize an asymmetric threat setting termed training-rich/inference-poor. During offline fingerprint database construction, the attacker can collect both encrypted traffic and resource-level information using controlled crawlers; during online inference, however, the attacker remains a standard passive eavesdropper limited to encrypted traffic alone. Under this setting, resource-level information is available during training but unavailable during online inference, which naturally qualifies it as Privileged Information [42]: an auxiliary supervisory signal that guides learning without being available as an input at inference time.

Motivated by the Learning Using Privileged Information (LUPI) paradigm [23, 42], we propose ResAware, a resource-aware distillation framework for cross-environment WF under the trainingrich/inference-poor setting. Using paired traffic-resource samples, ResAware trains a resource-side teacher model on resource-level features and distills the resulting privileged knowledge into a student model through cross-modal knowledge distillation [14, 23]. The student model operates on encrypted traffic alone. At deployment time, the resource sequences and the teacher model are removed, leaving a standard traffic-only WF classifier. In this way, ResAware improves robustness without strengthening the online attacker beyond the standard passive threat model.

We evaluate ResAware under multidimensional distribution shifts, including temporal, spatial, browser, and proxy variations, on a large-scale dataset spanning five months across six globally distributed nodes and more than 160,000 samples. The results show that ResAware robustly improves the cross-environment generalization of mainstream WF baselines with zero additional inference cost. Moreover, ResAware is orthogonally complementary to existing target-domain adaptation techniques [9, 40, 50].

The main contributions of this paper are as follows:

• Asymmetric Threat Model Formalization. We introduce and formalize a training-rich/inference-poor asymmetric setting for WF. Under this setting, application-layer resource information is available only during training and naturally serves as privileged information, improving the robustness of traffic-only WF models while preserving the standard passive eavesdropper assumption.  
• Cross-Modal Distillation Framework. We propose ResAware, a cross-modal knowledge distillation framework for cross-environment WF. ResAware trains a resource-side teacher model on resource-level features and distills the resulting privileged knowledge into a traffic-only student model, injecting stable resource-side supervision without requiring resource access at inference time.  
• Plug-and-Play Integration with Zero Inference Overhead. ResAware can be incorporated into existing WF models through the training objective alone, without modifying backbone architectures. At deployment time, it operates directly on encrypted traffic with zero additional inference overhead and remains complementary to existing domain adaptation techniques.  
• Large-Scale Benchmark and Evaluation. We construct a large-scale paired traffic-resource dataset spanning multidimensional cross-environment scenarios. On this benchmark, ResAware robustly improves the robustness of mainstream WF baselines. Under a 150-day temporal drift, it raises the F1-score of Var-CNN from 72.77% to 81.49% and improves the open-world TPR from 22.40% to 27.20% at 1% FPR. Under the more challenging obfuscated proxy drift setting, it further delivers absolute F1-score gains of 8.96% and 3.88% for Var-CNN and RF, respectively.

## 2 Threat Model

As depicted in Figure 2, we formalize an asymmetric threat model for cross-environment WF, termed training-rich/inference-poor. The asymmetry lies in the fact that resource-level information is available during offline training but unavailable during online inference.

Offline Construction Phase. As shown in the upper portion of Figure 2, the attacker deploys instrumented crawlers in a controlled environment to visit websites and collect both encrypted traffic and the corresponding TLS key logs. These key logs are generated solely by attacker-controlled crawlers during offline data collection and are not available from the victim during online inference. This enables offline parsing of encrypted traffic and extraction of highfidelity application-layer resource information, which is used solely as privileged supervision during training.

![](images/8c5d402a1a8d094dc8973d3fe6a22174d2c054f4676863b123025c632e966245.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
  A["Training Rich (Attacker)"] --> B["TLS Session Key"]
  C["Inference Poor (User)"] --> D["Encrypted Traffic"]
  B --> E["Encrypted Traffic"]
  D --> F["Encrypted Traffic"]
  E --> G["Offline Analysis"]
  F --> G
  G --> H["Decrypt"]
  H --> I["Plaintext"]
  I --> J["Index.html 100KB\nStyle1.css 45KB\nApp1.js 20KB\nHero.png 80KB..."]
  B --> K["TLS Session Key"]
  D --> L["Encrypted Traffic"]
  L --> M["Encrypted Traffic"]
  M --> N["TLS Session Key"]
  N --> O["Encrypted Traffic"]
```
</details>

Figure 2: The training-rich / inference-poor asymmetric threat model. During offline construction, the attacker collects paired traffic and resource sequences via TLS key logging; at online inference, only encrypted traffic is observable.

Online Inference Phase. The lower portion of Figure 2 depicts the online attacker as a client-side path observer, such as a local Autonomous System (AS), an Internet Service Provider (ISP), or a malicious local router. The attacker can only passively observe packet-level characteristics of the victim’s encrypted connections, including packet direction, length, and timing. The attacker cannot decrypt payloads, inject, modify, delay, or drop packets, and has no control over the victim’s endpoint. We further exclude side-channel metadata that could directly reveal the target website, including DNS queries, TLS SNI fields, certificate contents, HTTP Host headers, IP-to-domain mappings, and browser-side API fingerprints. Consistent with mainstream page-load-level WF research [5, 17, 39], we assume that each test sample corresponds to a single isolated page-load event.

## 3 Motivating Analysis: Stability and Transferability of Resource-Level Features

To motivate ResAware, we examine two fundamental questions. (1) Resource-Level Feature Robustness: Are resource-level features stable and discriminative under cross-environment distribution shifts? (2) Knowledge Transferability: Can knowledge derived from offline resource-level information be effectively distilled into a traffic-only student model?

## 3.1 Are Resource-Level Features Stable and Discriminative Across Environments?

Modern web page loading follows a structured process shaped by HTML, CSS, JavaScript, and asynchronous resource fetching [11]. While dynamic updates, advertisement injections, and A/B testing may introduce localized variation, the overall resource loading sequence of a website typically retains stable macroscopic patterns across visits [20, 28]. In contrast, low-level traffic features, such as packet length, direction, and burst intervals, are heavily affected by transport- and network-layer dynamics, including congestion, routing changes, and TCP control behavior. This suggests that resource loading sequences may provide a more stable basis for cross-environment identification than low-level traffic features.

![](images/6d5998a6d40affa1296b71693717a67d3f83b4bb14e6f3863ee134ccf6908d8d.jpg)

<details>
<summary>bar-line hybrid chart</summary>

| Task-Level Classification Robustness | Resource (%) | Traffic (%) |
| --- | --- | --- |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| **Resource** | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | **Resource** | **Resource** |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| *Resource* | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ***Resource* | ***Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource* |
| **Resource** | ****Resource* | ****Resource*. |
</details>

Figure 3: (a) CESM comparison between resource features $( F _ { \mathrm { c a t } } , F _ { \mathrm { s i z e } } )$ and traffic bursts $( F _ { \mathrm { b u r s t } } )$ under spatial and temporal drift; (b) classification F1-scores decay for a resource-only vs. traffic-only model.

To validate this hypothesis, we conduct an empirical analysis along two dimensions. First, we quantify the cross-environment drift and class separability of resource representations in feature space (Finding 1). Second, we evaluate whether this relative stability yields more robust classification performance under crossenvironment distribution shifts (Finding 2).

Finding 1: Compared with traffic features, resource-level features exhibit substantially stronger intra-class stability and inter-class separability across environments.

For each page load, we extract two resource sequences ordered by request initiation time. The first, $F _ { s i z e } ,$ , records the log-scaled payload size of each fetched resource. The second, $F _ { c a t } ,$ represents resource categories as one-hot vectors. As a traffic-side baseline, we derive $F _ { b u r s t }$ from encrypted traces by grouping contiguous packets traveling in the same direction and representing each burst by its signed log-scaled size.

We perform cross-regional and cross-temporal measurements on 100 monitored websites. Because these sequences have variable length and may exhibit local alignment shifts under crossenvironment loading conditions [22], we use Normalized Dynamic Time Warping (nDTW) [2] to measure distances between site prototypes. For a feature ?? , we define the same-site cross-environment drift $( \Delta _ { \mathrm { { s a m e } } } )$ and the different-site cross-environment distance $( \Delta _ { \mathrm { d i f f } } )$ between source environment ?? and target environment ?? as follows:

$$
\begin{array}{l} \Delta_ {\mathrm{same}} ^ {F} = \frac {1}{N} \sum_ {i = 1} ^ {N} d (p _ {i, s} ^ {F}, p _ {i, t} ^ {F}), \\ \Delta_ {\mathrm{diff}} ^ {F} = \frac {1}{N (N - 1)} \sum_ {i \neq j} d (p _ {i, s} ^ {F}, p _ {j, t} ^ {F}), \\ \end{array}
$$

To jointly evaluate whether features retain discriminative power while suppressing environmental noise, we introduce the Cross-Environment Stability Margin (CESM):

$$
\mathrm{CESM} _ {F} (s, t) = 1 - \Delta_ {\text { same }} ^ {F} / \Delta_ {\text { diff }} ^ {F}. \tag {2}
$$

A higher CESM indicates that cross-environment intra-site variation remains much smaller than inter-site discrepancy, and therefore reflects stronger robustness to environmental noise. As shown in Figure 3(a), both $F _ { s i z e }$ and $F _ { c a t }$ exhibit substantially stronger cross-environment stability than $F _ { b u r s t }$ . In cross-regional experiments spanning five geographic regions, $F _ { c a t }$ and $F _ { s i z e }$ achieve average CESM values of 0.675 and 0.577, respectively, compared with 0.218 for $F _ { b u r s t } ,$ , corresponding to gains of 3.09× and 2.65× over $F _ { b u r s t }$ . The same trend persists under temporal drift: after 150 days, $F _ { c a t } \ ( { \mathrm { C E S M } } = 0 . 5 9 2 )$ and $F _ { s i z e } \ ( \mathrm { C E S M } = 0 . 4 5 6 )$ remain well above $F _ { b u r s t } \left( \mathrm { C E S M } = 0 . 2 2 4 \right)$ , yielding 2.64× and 2.04× larger margins, respectively. These results show that resource-level features are inherently more robust to environmental variation and preserve stronger discriminative structure across diverse deployment conditions.

Finding 2: The stability advantage of resource-level features yields stronger task-level robustness. To examine whether the feature-space advantage carries over to downstream classification robustness, we control all other factors and compare two classifiers built on the same Deep Fingerprinting (DF) [39] architecture: a Resource-Only model, which takes $F _ { s i z e }$ and $F _ { c a t }$ as input, and a Traffic-Only model, which takes packet-level traffic sequences as input.

As shown in Figure 3(b), the Resource-Only model degrades much more slowly under environmental drift. Under temporal drift, both models initially achieve near-perfect source-domain F1-scores. However, after 150 days, the Traffic-Only model drops by 33.30 percentage points to 64.85%, whereas the Resource-Only model declines by only 14.22 points and still maintains 83.50%. In cross-regional evaluation, the Resource-Only model achieves an average F1-score of 91.49% across all target regions, outperforming the traffic-only model by 8.35 percentage points on average.

Takeaway. These empirical results show that resource-level features are substantially more stable and robust to environmental noise than low-level traffic features under cross-environment shifts. Yet such robust resource-side signals are unavailable to a passive eavesdropper at deployment time. This gap motivates the core design of ResAware: the key challenge is not to seek stronger features from online observations alone, but to transfer resource-side robustness to a traffic-only classifier through offline cross-modal supervision.

## 3.2 Can Resource-Side Robustness Be Transferred to Traffic-Only Models?

This leads to the central methodological question behind ResAware: can the stability available only through privileged supervision during training be transferred across modalities, and if so, how can it improve a classifier that must rely solely on low-level traffic at deployment time?

Our answer is yes, but not by assuming that resource sequences can be faithfully reconstructed from encrypted traffic. In modern web communications, concurrent browser scheduling, HTTP/2/3 multiplexing, transport-layer dynamics, and network latency variation collectively entangle multiple object-level requests within a continuous packet stream. Recovering precise object boundaries from encrypted traffic is therefore highly ill-posed in practice. Building stability transfer on such packet-to-object reconstruction would not only be impractical, but would also force the model to depend on fragile local alignment assumptions.

Instead, ResAware follows a more robust transfer pathway grounded in the Learning Using Privileged Information (LUPI) paradigm [23, 42] and generalized knowledge distillation. The resource view, available only during training, does not need to be reconstructed at inference time. As long as it provides a cleaner inductive signal than encrypted traffic alone, it can reshape the decision boundaries of a single-modality classifier through a teacher-student framework. In cross-environment WF, resource-side privileged supervision fits this paradigm particularly well.

Under standard hard-label supervision with Empirical Risk Minimization (ERM), a single-modality model can easily fall into shortcut learning, relying on spurious yet separable packet-level cues in the source environment and thus forming brittle decision boundaries that fail under distribution shift.

ResAware mitigates this problem by introducing a structural prior from the resource modality through soft-target supervision. This prior captures class-level similarity relationships at the application layer and guides the traffic-only model toward representations that better reflect intrinsic website identity, rather than transient environment-specific traffic patterns. What is transferred is not the raw resource sequence itself, but the class-level relational knowledge encoded in the resource modality. The appropriate role of the resource modality is therefore not as an auxiliary runtime input, but as a source of privileged supervision during training. How effectively this knowledge is inherited by the student, and how it affects decision-boundary calibration under long-term drift, are quantitatively analyzed in §5.7.

## 4 ResAware Overview and Design

ResAware is a training-time privileged knowledge distillation framework for cross-environment WF. Its core idea is straightforward: during the offline construction phase, a resource-only teacher model is trained on resource loading sequences collected under controlled conditions, and the resulting resource-side knowledge is transferred to a traffic-only student model through heterogeneous cross-modal distillation. In this way, ResAware introduces stable resource-side supervision into the student model without requiring resource access at inference time.

The framework is designed under three constraints:

• Privileged Information Isolation. High-fidelity resource features are available only during offline training and remain inaccessible during online inference.  
• Zero Online Overhead and Interface Compatibility. At deployment time, the framework must preserve the standard traffic-only observation interface of a passive WF attacker, without introducing additional online cost.  
• Plug-and-Play Integration. ResAware makes no assumptions about the underlying WF backbone. It can be instantiated on top of any existing WF model following a standard end-to-end classification pipeline.

![](images/6efaaea27af39a8066ffa7c320b49c604769df5c99ffa857451ae555c82ce91d.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
  A["Source Environment"] --> B["Resource"]
  B --> C{102, 12, 18, 802...}
  C --> D["Teacher Model"]
  D --> E["Category Embedding"]
  D --> F["Log(bytes)"]
  E --> G["Positional Encoding"]
  F --> G
  G --> H["Transformer Encoder"]
  H --> I["Layer 3"]
  H --> J["Layer 2"]
  H --> K["Layer 1"]
  I --> L["Feature Extraction"]
  J --> L
  K --> L
  L --> M["Teacher Classification Head"]
  M --> N["Cross-Entropy Loss"]
    
  O["Student Model Distillation"] --> P["Teacher Model"]
  P --> Q["zT"]
  Q --> R["Softmax(zT/τ)"]
  Q --> S["Softmax(zS/τ)"]
  R --> T["Joint Optimization"]
  S --> T
  T --> U["Knowledge Distillation Loss"]
  T --> V["Classification Loss"]
  U --> W["Total Loss"]
    
  X["Target Environment"] --> Y["Traffic"]
  Y --> Z["Traffic Feature Extraction"]
  Z --> AA["Backbone"]
  AA --> AB["Classification Head"]
  AB --> AC["zS"]
    
  AD["Testing on Traffic-only Samples"] --> AE["Student Model"]
  AE --> AF["Prediction"]
    
  AG["Gradient Flow Parameter Frozen"] --> AH["A.com B.com C.com"]
  AI["Resource Type Resource Size [CLS"] Token] --> AJ["Waterfall Graph"]
```
</details>

Figure 4: Overview of the ResAware framework. Offline training first trains a resource-only teacher, then distills its knowledge into a traffic-only student; all resource-side components are discarded before online deployment.

## 4.1 Design Principle: Privileged Resource Distillation

As illustrated in Figure 4, ResAware operates in two strictly separated phases: offline training and online inference. During offline training, the framework has access to paired samples $( x , x ^ { * } , y )$ , where ?? denotes the encrypted traffic trace of a single page load, $x ^ { * }$ denotes the corresponding resource loading sequence extracted under controlled conditions, and ?? is the ground-truth website label.

The distillation pipeline proceeds in three steps. First, a resourceonly teacher model is trained in the offline source environment to capture stable resource-side patterns that are less affected by network noise. Second, the teacher model is frozen, and its soft target outputs are used to supervise a traffic-only student model, transferring resource-side relational knowledge into the traffic feature space. Third, all resource-side components are discarded before deployment. The complete training and deployment procedure is summarized in Algorithm 1 (Appendix C).

## 4.2 Training the Resource-Only Teacher

In the controlled source environment, ResAware constructs pageload-level paired triplets $( x , x ^ { * } , y )$ , where ?? denotes the encrypted traffic trace, $x ^ { * }$ denotes the corresponding resource loading sequence, and ?? is the website label. This requires only page-load-level correspondence between ?? and $x ^ { * }$ , avoiding any need for fragile packet-to-object reconstruction.

To improve robustness under cross-environment extraction, we order resource events by request initiation time, as triggered by the browser engine, rather than by response completion order. Initiation order more directly reflects the parsing progress of the root document and the triggering logic of resource dependencies, whereas completion order is far more sensitive to network latency, congestion control, and HTTP multiplexing. Using initiation order therefore decouples the resource sequence from transport-side timing variation.

To convert a variable-length resource loading sequence into a fixed-size model input, we represent each page load as a sequence of ?? resource events:

$$
Z = \{(c _ {i}, \tilde {s} _ {i}) \} _ {i = 1} ^ {N} \tag {3}
$$

where ???? is the resource category ID and ??˜?? is the log-scaled payload size. Unless otherwise specified, we set ?? = 200 for truncation and padding. The sequence captures two feature channels:

• Categorical Channel. Based on the Content-Type field in HTTP response headers, each resource is mapped into one of nine categories: HTML, Tiny Image, Regular Image, CSS, JS, Font, JSON/API, Document, and Unknown. Image resources are further divided by payload size: those smaller than 5 KB are classified as Tiny Image, while those of 5 KB or larger are classified as Regular Image. This taxonomy captures the major resource types that commonly appear in modern web pages.

• Size Channel. We use the byte size of each resource as a continuous feature. To reduce the influence of large resources on optimization, the size of the ??-th resource is log-scaled to ??˜?? before being fed into the model.

We deliberately discard absolute request timestamps and preserve temporal structure only through event order, encoded by positional embeddings. This design prevents the teacher from overfitting to source-environment-specific latency patterns. The resulting fixed-length sequence is then used to train a teacher model ?? (·) based on a Transformer encoder [44], whose parameters are frozen after supervised training on source-domain hard labels.

## 4.3 Distilling Resource Knowledge into a Traffic-Only Student

During cross-modal knowledge distillation, the student model ?? (·) receives only encrypted traffic as input. ResAware is agnostic to the student’s input representation and can be instantiated on top of any compatible WF backbone. The original input format—whether packet length sequences, burst sequences, or Traffic Aggregation Matrices (TAM)—remains unchanged. At each forward pass, the frozen teacher model produces logits $z _ { T } = T ( x ^ { * } )$ , while the student model produces logits $z _ { S } = S ( x )$ . The student parameters $\theta _ { S }$ are optimized using two loss terms:

Classification Loss. To preserve the student’s discriminative accuracy on the traffic modality, we compute the cross-entropy loss against ground-truth labels:

$$
\mathcal {L} _ {c l s} = - \sum_ {c = 1} ^ {C} y _ {c} \log \left(\frac {\exp (z _ {S , c})}{\sum_ {j = 1} ^ {C} \exp (z _ {S , j})}\right) \tag {4}
$$

where ?? is the number of monitored websites.

Resource-Privileged Distillation Loss. To mitigate shortcut learning under ERM, we transfer the teacher’s soft knowledge via KL divergence with temperature ??:

$$
\mathcal {L} _ {k d} = \tau^ {2} \cdot \mathcal {D} _ {K L} \left(\sigma \left(\frac {z _ {T}}{\tau}\right) \| \sigma \left(\frac {z _ {S}}{\tau}\right)\right) \tag {5}
$$

where $\sigma ( \cdot )$ is the Softmax function. The temperature ?? flattens the posterior distribution, amplifying inter-class similarity signals beyond the target class. Minimizing this loss guides the student to internalize the inter-class relationships encoded by the resource modality, acting as a form of semantic regularization.

Joint Objective. The student’s total training objective is a weighted combination:

$$
\mathcal {L} _ {t o t a l} = (1 - \alpha) \mathcal {L} _ {c l s} + \alpha \mathcal {L} _ {k d} \tag {6}
$$

$\alpha \in [ 0 , 1 ]$ controls the trade-off between the classification objective and the privileged distillation objective. At the boundary $\alpha = 0 ;$ $\mathcal { L } _ { t o t a l }$ reduces to $\mathcal { L } _ { c l s }$ , and the student degenerates into a standard traffic-only classifier trained under ordinary ERM. In practice, the optimal ?? is primarily determined by the student backbone and exhibits relatively low sensitivity to the specific training and testing datasets; we analyze its effect in the ablation study (§F).

Mechanistically, $\mathcal { L } _ { c l s }$ preserves the student’s ability to discriminate ground-truth website labels, while $\mathcal { L } _ { k d }$ answers: “which websites share similar resource loading structures?” Together, they prevent the student from relying solely on one-hot supervision, effectively suppressing overfitting to transient, environment-specific traffic patterns.

## 4.4 Online Inference and Deployment

After distillation, ResAware retains only the student model ?? for deployment. All training-specific components, including the resource parser, the teacher model, and the distillation objective, are removed before deployment.

At inference time, the deployed model takes a single encrypted traffic trace as input, without expanding the online attack surface. All additional computation introduced by ResAware is confined to the offline training phase. As a result, the deployed model has the same inference latency and memory footprint as the underlying baseline, making ResAware a plug-and-play enhancement with zero additional online overhead.

## 5 Evaluation

This section evaluates the effectiveness, generality, and underlying mechanisms of ResAware under diverse cross-environment WF settings.

## 5.1 Experimental Setup

Datasets and Evaluation Protocols. Since existing public WF datasets lack application-layer resource events synchronized with traffic traces, we collect a large-scale evaluation dataset of paired traffic-resource samples. Each sample is represented as $( x , x ^ { * } , y )$ , where ?? is the encrypted traffic trace, $x ^ { * }$ is the privileged resource sequence (accessible only at training time), and ?? is the website label. Detailed resource sequence construction procedures are provided in Appendix D.1.

Data collection spanned November 2025 to April 2026 across six geographically distributed vantage points (US, Japan, Singapore, South Africa, Australia, and Germany). The monitored set comprises 100 stable websites randomly sampled from the Tranco Top 100K [29]. The unmonitored set consists of 83,645 reachable background websites excluding the monitored set. In total, we collected over 160,000 page-load traces (collection pipelines and distribution statistics are detailed in Appendix D.2). In the source domain, each monitored site comprises 150 traces used for model training; in each target-domain test set, each monitored site contributes 25–30 traces per snapshot. For open-world evaluation, the background split contains 1 trace per unmonitored site.

In all cross-environment experiments, target-domain samples are strictly excluded from model training, distillation hyperparameter selection, and threshold tuning. Distillation hyperparameters are tuned once on the source-domain validation set and fixed thereafter. All experiments are run five times with different random seeds; we report the mean performance. We design five evaluation scenarios to cover realistic deployment shifts:

• Temporal Drift. Models are trained on the source domain and tested on temporal snapshots collected at ∼30-day intervals to evaluate cross-time generalization.  
• Spatial Drift. The test set consists of samples from five geographic locations within the same time window, assessing

Table 1: Summary of backbone models, input feature representations, and the source-validated selected distillation weight ??

<table><tr><td>Backbone</td><td>Input Features</td><td>α</td></tr><tr><td>AWF [33]</td><td>Packet direction sequence</td><td>0.1</td></tr><tr><td>DF [39]</td><td>Packet direction sequence</td><td>0.5</td></tr><tr><td>RF [46]</td><td>Traffic aggregated features</td><td>0.5</td></tr><tr><td>Var-CNN [3]</td><td>Packet direction sequence</td><td>0.7</td></tr><tr><td>Tik-Tok [31]</td><td>Packet direction and timestamp sequence</td><td>0.5</td></tr><tr><td>CountMamba [10]</td><td>Packet direction, length, and timestamp sequence</td><td>0.7</td></tr></table>

generalization across diverse network paths and CDN deployments.

• Obfuscation proxy Drift. The test set covers six obfuscation proxy protocols (Shadowsocks [35], Trojan[41], VLESS-XTLS-Vision, VMess-WS-TLS, VMess-TLS and VMess[30]) to evaluate resilience against transport-layer obfuscation.  
• Browser Drift: By designating Chrome as the source domain for training and utilizing Edge and Firefox as target domains, we evaluate the robustness against variations in rendering engines and connection management.  
• Open-World Temporal Drift. Using temporal snapshots, we mix 100 monitored classes (8 samples each) with 80,000 unmonitored classes(1 samples each) at a 1:100 ratio. This scenario evaluates detection capability under strict falsepositive constraints (?? ????@1%??????).

Backbone Models. To cover diverse input representations and modeling paradigms, we select six representative WF architectures as student backbones. Table 1 lists the input features and validated ?? values for each model; the optimal ?? is coupled to the model architecture, a relationship we analyze in §F. For each baseline, we compare its native version against its ResAware-distilled counterpart.

Teacher Model and Reporting Role. Unless otherwise specified, “Teacher” refers exclusively to the resource-only teacher defined in §4.2. This Transformer-based model is trained on the same source-domain monitored websites as the student models, using only resource sequences. Because it relies on a privileged modality unavailable to the online attacker, its predictions are reported only as an oracle-style diagnostic reference for resource-side stability; they are neither a deployable baseline nor a formal upper bound for traffic-side student models.

Training Protocol and Hyperparameter Fairness. To ensure that performance gains are attributable to ResAware rather than additional hyperparameter tuning, we follow the architectures, optimizers, learning rate schedules, batch sizes, and training epochs from the original papers or official implementations for each backbone. For the native and ResAware-distilled versions of the same baseline, all training configurations are kept identical except for the distillation mechanism itself. ResAware-specific hyperparameters (temperature and distillation weight ??) are tuned once on the source-domain validation set and fixed for all subsequent experiments; they are never re-tuned for target environments.

Metrics. For closed-world tasks, we adopt the F1-score as the primary evaluation metric, supplemented by Precision and Recall. For open-world tasks, given the attacker’s sensitivity to false alarms, we prioritize True Positive Rate at a fixed False Positive Rate (?? ????@1%??????) as the primary metric.

Implementation Details. We implement ResAware in Python 3.12 with PyTorch 2.10.0. All training, distillation, and inference experiments run on a single workstation (Ubuntu 24.04 LTS) equipped with dual Intel Xeon Platinum 8352S CPUs, 128 GB RAM, and an NVIDIA RTX 4090 GPU (24 GB VRAM). Unless otherwise noted, all backbone implementations use the same random seeds to ensure reproducibility.

## 5.2 Zero-Shot Robustness under Cross-Environment Drift

We evaluate whether ResAware improves the zero-shot robustness of WF models under four cross-environment drift scenarios, where models are trained on the source domain with no access to targetdomain samples.

Overall Results. Table 2 summarizes the zero-shot closed-world F1-scores across six backbone models (see Appendix E for perenvironment breakdowns). ResAware yields positive gains in 21 of 24 backbone × drift combinations (87.5%).

Temporal Drift. Under a 150-day drift, ResAware improves Var-CNN from 72.77% to 81.49% (+8.72%), with additional gains of +4.40% for DF and +3.03% for Tik-Tok. The temporal decay curves in Figure 5 show that the performance gap generally widens over longer intervals for the stronger sequential backbones, indicating that ResAware slows degradation under long-horizon drift rather than merely improving source-domain fit. Table 3 further reports persnapshot Precision, Recall, and F1 for all six backbones; the ResAware student (Var-CNN backbone) remains close to the Teacher across all five snapshots, dropping only from 93.95% at Day 30 to 81.49% at Day 150, while the vanilla Var-CNN baseline falls to 72.77%. Notably, the Teacher model maintains high accuracy after 150 days, confirming that page-level resource organization is substantially more stable over time than packet morphology. ResAware exploits this asymmetry to regularize the student’s decision boundaries.

Spatial Drift. Across the five international vantage points, ResAware improves five of the six backbones on average. The largest gains appear for Var-CNN (+4.30%, 82.66%→86.96%), followed by CountMamba (+3.12%) and RF (+2.50%), while DF and Tik-Tok also improve by +1.93% and +2.25%, respectively. AWF is the only exception, showing a slight average drop (-0.47%), which indicates that spatial drift is generally mild enough for resource supervision to help, but low-capacity students may still fail to absorb the transferred topology consistently.

Obfuscated Proxy Drift. Obfuscation Proxy protocols heavily distort packet-level morphology while leaving page resource structure largely intact. The largest improvement is observed for Var-CNN, whose F1 score increases from 38.14% to 47.10% (+8.96 %), followed by RF (+3.88 %) and CountMamba (+1.29 %). AWF and Tik-Tok obtain only marginal gains (+0.50 and +0.36 %), while DF is the only backbone with a slight degradation (-1.04 %). This exception indicates that, under severe proxy-induced deformation, cross-modal distillation is not uniformly beneficial across architectures; its effectiveness still depends on the student’s ability to align traffic representations with the resource-level topology transferred by the teacher.

Table 2: Zero-shot closed-world F1-score with and without ResAware across four drift settings. Δ denotes the absolute gain in percentage points

<table><tr><td rowspan="2">Model</td><td colspan="3">Temporal Drift (Day 150)</td><td colspan="3">Spatial Drift (Avg.)</td><td colspan="3">Proxy Drift (Avg.)</td><td colspan="3">Browser Drift (Avg.)</td></tr><tr><td>w/o</td><td>w/</td><td>Δ</td><td>w/o</td><td>w/</td><td>Δ</td><td>w/o</td><td>w/</td><td>Δ</td><td>w/o</td><td>w/</td><td>Δ</td></tr><tr><td>AWF</td><td>33.25</td><td>32.25</td><td>-1.00</td><td>49.23</td><td>48.76</td><td>-0.47</td><td>17.53</td><td>18.03</td><td>+0.50</td><td>5.91</td><td>6.06</td><td>+0.15</td></tr><tr><td>CountMamba</td><td>28.94</td><td>29.16</td><td>+0.22</td><td>72.91</td><td>76.03</td><td>+3.12</td><td>61.21</td><td>62.50</td><td>+1.29</td><td>7.11</td><td>9.50</td><td>+2.39</td></tr><tr><td>RF</td><td>36.64</td><td>38.27</td><td>+1.63</td><td>76.11</td><td>78.61</td><td>+2.50</td><td>62.86</td><td>66.74</td><td>+3.88</td><td>18.15</td><td>22.83</td><td>+4.68</td></tr><tr><td>Tik-Tok</td><td>54.64</td><td>57.67</td><td>+3.03</td><td>82.85</td><td>85.10</td><td>+2.25</td><td>44.52</td><td>44.88</td><td>+0.36</td><td>4.79</td><td>6.05</td><td>+1.26</td></tr><tr><td>DF</td><td>61.39</td><td>65.79</td><td>+4.40</td><td>84.71</td><td>86.64</td><td>+1.93</td><td>48.32</td><td>47.28</td><td>-1.04</td><td>4.07</td><td>6.66</td><td>+2.59</td></tr><tr><td>Var-CNN</td><td>72.77</td><td>81.49</td><td>+8.72</td><td>82.66</td><td>86.96</td><td>+4.30</td><td>38.14</td><td>47.10</td><td>+8.96</td><td>17.24</td><td>21.45</td><td>+4.21</td></tr></table>

Table 3: Precision, Recall, and F1-score (%) under temporal drift for all six backbones and the resource-only teacher across five test snapshots (Day 30–150).

<table><tr><td rowspan="2"></td><td colspan="3">Day 30</td><td colspan="3">Day 60</td><td colspan="3">Day 90</td><td colspan="3">Day 120</td><td colspan="3">Day 150</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td><td>P</td><td>R</td><td>F1</td></tr><tr><td>Teacher</td><td>97.35</td><td>96.77</td><td>96.49</td><td>95.55</td><td>94.77</td><td>94.44</td><td>89.74</td><td>90.93</td><td>89.27</td><td>89.61</td><td>89.57</td><td>87.61</td><td>90.49</td><td>98.80</td><td>88.97</td></tr><tr><td>AWF</td><td>55.89</td><td>54.05</td><td>51.23</td><td>52.78</td><td>51.64</td><td>48.18</td><td>43.72</td><td>44.30</td><td>40.14</td><td>41.86</td><td>42.94</td><td>38.20</td><td>35.77</td><td>37.95</td><td>33.25</td></tr><tr><td>CountMamba</td><td>88.39</td><td>89.31</td><td>87.79</td><td>44.73</td><td>36.71</td><td>35.26</td><td>38.19</td><td>33.39</td><td>31.79</td><td>36.35</td><td>31.93</td><td>29.79</td><td>34.73</td><td>31.36</td><td>28.94</td></tr><tr><td>Tik-Tok</td><td>90.30</td><td>90.15</td><td>89.07</td><td>80.45</td><td>80.97</td><td>78.63</td><td>69.46</td><td>69.51</td><td>66.57</td><td>63.24</td><td>62.38</td><td>59.34</td><td>58.40</td><td>57.83</td><td>54.64</td></tr><tr><td>RF</td><td>91.25</td><td>91.52</td><td>90.46</td><td>61.96</td><td>47.12</td><td>45.88</td><td>52.24</td><td>41.82</td><td>39.84</td><td>49.83</td><td>38.84</td><td>36.53</td><td>47.84</td><td>39.47</td><td>36.64</td></tr><tr><td>DF</td><td>91.99</td><td>92.08</td><td>91.28</td><td>88.17</td><td>88.33</td><td>86.75</td><td>74.82</td><td>76.90</td><td>73.60</td><td>68.60</td><td>71.65</td><td>67.35</td><td>62.08</td><td>66.19</td><td>61.39</td></tr><tr><td>Var-CNN</td><td>92.90</td><td>92.52</td><td>91.68</td><td>90.30</td><td>89.56</td><td>88.63</td><td>83.57</td><td>82.03</td><td>80.37</td><td>82.33</td><td>81.62</td><td>79.44</td><td>74.51</td><td>76.22</td><td>72.77</td></tr><tr><td>ResAware</td><td>94.11</td><td>94.66</td><td>93.95</td><td>94.22</td><td>94.00</td><td>93.38</td><td>87.93</td><td>87.81</td><td>86.37</td><td>89.46</td><td>89.19</td><td>87.60</td><td>82.57</td><td>84.28</td><td>81.49</td></tr></table>

![](images/b4bce4151e9b82771a175b8238f4cefa034684017116201742e6aaab432d7cf7.jpg)

<details>
<summary>line chart</summary>

| Times(Days) | F1-Score (%) - Solid Line | F1-Score (%) - Dashed Line |
| ----------- | ------------------------- | -------------------------- |
| 30          | 92                        | 91                         |
| 60          | 88                        | 87                         |
| 90          | 77                        | 74                         |
| 120         | 72                        | 68                         |
| 150         | 67                        | 63                         |
</details>

(a) DF

![](images/1ccf8004b6fc0e4592e6153ab04d80c298c8b7c75027c1a8be8346ada16b7e8c.jpg)

<details>
<summary>line chart</summary>

| Times(Days) | w/o ResAware |
| ----------- | ------------ |
| 30          | 90           |
| 60          | 50           |
| 90          | 45           |
| 120         | 40           |
| 150         | 40           |
</details>

(b) TikTok

![](images/d8db0c8885d9f2ae368bce1c1a34bceb3111d6236c25a53fda54ba725f8590b6.jpg)

<details>
<summary>line chart</summary>

| Times(Days) | w/ ResAware |
| ----------- | ----------- |
| 30          | 90          |
| 60          | 82          |
| 90          | 70          |
| 120         | 62          |
| 150         | 58          |
</details>

(c) RF

![](images/5a54f277d152a077706c5cd6a3442257ff650ca3340fbe6f188206bfdf066d01.jpg)

<details>
<summary>line chart</summary>

| Times(Days) | Line 1 | Line 2 |
| ----------- | ------ | ------ |
| 30          | 94     | 92     |
| 60          | 94     | 89     |
| 90          | 87     | 81     |
| 120         | 88     | 80     |
| 150         | 82     | 75     |
</details>

(d) Var-CNN  
Figure 5: Closed-world F1-score (%) with and without ResAware over five temporal test snapshots (Day 30–150) for WF backbones.

Cross-Browser Drift. Browser drift is the most challenging of the four scenarios: under the vanilla setting, four of the six backbones remain below 10% average F1-score, with only RF (18.15%) and Var-CNN (17.24%) retaining limited discriminative power. ResAware still yields consistent gains for all six backbones, led by RF (+4.68%), Var-CNN (+4.21%), and DF (+2.59%), although the absolute performance remains far below that under temporal and spatial drift. This result suggests that browser switching perturbs how application resources are rendered, scheduled, and multiplexed into observable traffic, making cross-modal topology transfer substantially harder than in the other drift settings.

Takeaways. The zero-shot results support two conclusions: (1) Resource supervision during training improves most traffic-only WF models, with the clearest and most stable benefits under long-term temporal drift. (2) ResAware is not an unconditional enhancer: its effectiveness depends on whether resource sequences remain predictive of observable traffic morphology and whether the student has sufficient capacity to absorb the teacher’s inter-class topology; when browser execution or proxy encapsulation disrupts this correspondence, or when the student cannot accommodate the distillation constraint, gains may become limited or turn into negative transfer (§5.6).

## 5.3 Open-World Detection under Temporal Drift

Closed-world performance alone is insufficient to assess the practical threat of WF attacks; we therefore evaluate ResAware under the open-world temporal drift setting. We focus on the three strongest backbones in this regime, namely DF, Tik-Tok, and Var-CNN, and report TPR at a stringent operating point of 1% FPR under the 1:100 monitored-to-unmonitored imbalance.

Table 4: Open-world temporal drift results (?? ????@1%??????) for DF, Tik-Tok, and Var-CNN with and without ResAware across five temporal snapshots (100 monitored sites vs. 80K unmonitored, 1:100 ratio). Δ denotes the absolute gain in percentage points.

<table><tr><td>Model</td><td>Type</td><td>30</td><td>60</td><td>90</td><td>120</td><td>150</td></tr><tr><td rowspan="3">DF</td><td>w/o</td><td>50.68</td><td>39.52</td><td>28.45</td><td>24.87</td><td>20.40</td></tr><tr><td>w/</td><td>54.23</td><td>40.70</td><td>28.63</td><td>26.00</td><td>21.02</td></tr><tr><td>Δ</td><td>+3.55</td><td>+1.18</td><td>+0.18</td><td>+1.13</td><td>+0.62</td></tr><tr><td rowspan="3">Tik-Tok</td><td>w/o</td><td>27.50</td><td>8.60</td><td>6.73</td><td>5.50</td><td>4.52</td></tr><tr><td>w/</td><td>50.15</td><td>22.63</td><td>16.43</td><td>12.93</td><td>10.17</td></tr><tr><td>Δ</td><td>+22.65</td><td>+14.03</td><td>+9.70</td><td>+7.43</td><td>+5.65</td></tr><tr><td rowspan="3">Var-CNN</td><td>w/o</td><td>48.75</td><td>35.70</td><td>27.57</td><td>24.92</td><td>22.40</td></tr><tr><td>w/</td><td>55.07</td><td>41.05</td><td>30.43</td><td>28.85</td><td>27.20</td></tr><tr><td>Δ</td><td>+6.32</td><td>+5.35</td><td>+2.86</td><td>+3.93</td><td>+4.80</td></tr></table>

Table 4 shows that ResAware improves TPR@FPR=0.01 for all three backbones across the full 150-day window. The gains are most pronounced for Tik-Tok, where TPR rises by +22.65%, +14.03%, and +9.70% over the first three snapshots, and remains +5.65% higher even at Day 150. Var-CNN exhibits consistently positive improvements (+2.86% to +6.32%), while DF remains comparatively robust and still benefits from modest gains (+0.18% to +3.55%). Even when the baseline detector degrades substantially under long-term drift, resource supervision preserves meaningful monitored-site detection capability at a strict false-positive budget.

Takeaway. The closed-world robustness gains from ResAware carry over to the more operationally relevant open-world setting: training-time resource supervision improves low-FPR monitoredsite detection under temporal aging and severe class imbalance, with the largest benefits appearing in backbones whose traffic-side decision boundaries are otherwise most vulnerable to long-term drift.

## 5.4 Target-Domain Data Efficiency: Few-Shot and Zero-Label Adaptation

In practice, WF attackers may occasionally obtain limited targetdomain information after initial deployment. Such information takes two forms: a stronger but more costly variant in which the attacker acquires a small number of labeled target traces via controlled probing or repeated visits [4, 40], and a weaker but more scalable variant in which the attacker observes unlabeled target traffic for Test-Time Adaptation (TTA [21, 45]). Using Var-CNN as the backbone, we evaluate whether ResAware reduces the targetdomain data required to recover performance under distribution shift.

Few-Shot Adaptation with Labeled Target Samples. Following the standard few-shot evaluation protocol adopted in prior WF and domain adaptation works [4, 40], we freeze the backbone and update only the linear classifier with ?? labeled target-domain traces.

![](images/089ba25b30a0dc991d906750a8862ce4f7c1491d194c7825e5ccaf28153c00ab.jpg)  
Figure 6: Few-shot adaptation F1-score (%) of Var-CNN with and without ResAware under Shadowsocks, Trojan, VLESS-XTLS-Vision and VMess-WS-TLS proxy drifts.

Figure 6 shows that ResAware provides the largest benefits in the low-shot regime. Under the Trojan proxy, ResAware achieves 88.33% with just 1 shot, whereas vanilla Var-CNN reaches only 77.78%. Under the more disruptive VMess-WS-TLS setting, ResAware with 5 shots matches the performance of vanilla Var-CNN with 10 shots (94.50% vs. 94.11%), effectively halving the label requirement.

Unlabeled Target-Domain Adaptation. We further assess ResAware’s compatibility with Proteus [9], a state-of-the-art unlabeled adaptation framework, under six obfuscation proxy drift settings (Table 5). ResAware proves to be highly complementary to adaptation techniques. Proteus elevates vanilla Var-CNN accuracy from 38.79% to 54.89%, while ResAware + Proteus achieves a superior 69.14%. This complementarity reflects their distinct operational stages: ResAware focuses on environment-agnostic representation learning in the source domain, whereas Proteus facilitates targetdomain calibration. Consequently, ResAware serves as a stronger feature initializer rather than a substitute for test-time adaptation. Takeaways. ResAware improves the efficiency of both labeled and unlabeled target-domain adaptation: it reduces the labeled sample requirement for few-shot adaptation and provides a more robust feature initialization for unlabeled adaptation.

## 5.5 Ablation Analysis: What Makes ResAware Work?

Prior experiments establish that ResAware consistently improves the robustness of traffic-only WF models across diverse distribution shifts. We now investigate the sources of these gains through two ablation studies. First, we verify whether the improvements stem from correctly aligned privileged resource supervision or merely from the regularization effect of soft-label distillation. Second, we ablate individual resource channels—size, category, and order—to quantify each channel’s contribution. The sensitivity analysis of the distillation weight ?? is provided in Appendix F.

Privileged Resource KD vs. Generic KD. We design two control conditions to isolate the source of gains: Traffic KD replaces the teacher’s input with traffic burst features (retaining the distillation pipeline but removing the resource modality), and Class-Shuffled

Table 5: Closed-world F1-score (%) under Obfuscation proxy drift for Var-CNN across six obfuscation protocols, under four configurations of ResAware and Proteus [9]. ResAware operates at training time (source-side); Proteus operates at inference time (target-side); their combination consistently outperforms either component alone.

<table><tr><td>ResAwareProteus</td><td>w/o w/o</td><td>w/o w/</td><td>w/ w/o</td><td>w/ w/</td></tr><tr><td>Shadowsocks</td><td>40.87%</td><td>56.43%</td><td>49.83%</td><td>74.70%</td></tr><tr><td>Trojan</td><td>43.07%</td><td>60.72%</td><td>52.96%</td><td>82.32%</td></tr><tr><td>VLESS-XTLS-Vision</td><td>29.75%</td><td>34.47%</td><td>34.98%</td><td>39.86%</td></tr><tr><td>VMess</td><td>46.28%</td><td>64.87%</td><td>55.58%</td><td>85.04%</td></tr><tr><td>VMess-TLS</td><td>41.88%</td><td>62.96%</td><td>51.33%</td><td>75.25%</td></tr><tr><td>VMess-WS-TLS</td><td>30.90%</td><td>49.87%</td><td>34.35%</td><td>57.66%</td></tr><tr><td>AVG</td><td>38.79%</td><td>54.89%</td><td>46.51%</td><td>69.14%</td></tr></table>

Table 6: Ablation study verifying the necessity of correctly aligned privileged supervision under 150-day temporal drift (F1-score (%)). Three conditions are compared: ResAware with a resource teacher, KD with a traffic teacher, and KD with class-shuffled resource soft labels.

<table><tr><td>Model</td><td>w/ Resource KD (Ours)</td><td>Baseline</td><td>w/ Traffic KD</td><td>w/ Class-Shuffled Resource KD</td></tr><tr><td>Teacher</td><td>88.97%</td><td>-</td><td>77.15%</td><td>-</td></tr><tr><td>AWF</td><td>32.25%</td><td>33.25%</td><td>31.02%</td><td>29.44%</td></tr><tr><td>DF</td><td>65.79%</td><td>61.39%</td><td>55.31%</td><td>62.58%</td></tr><tr><td>RF</td><td>38.27%</td><td>36.64%</td><td>30.98%</td><td>37.71%</td></tr><tr><td>Tik-Tok</td><td>57.67%</td><td>54.64%</td><td>40.61%</td><td>54.52%</td></tr><tr><td>Var-CNN</td><td>81.49%</td><td>72.77%</td><td>51.48%</td><td>74.92%</td></tr><tr><td>CountMamba</td><td>29.16%</td><td>28.94%</td><td>24.36%</td><td>28.11%</td></tr></table>

Resource KD preserves the numerical distribution of the resource soft labels but randomly permutes the class assignments (to test whether gains arise solely from soft-label regularization).

As shown in Table 6, both control conditions perform substantially worse than ResAware and generally fall below the baseline. Traffic KD not only fails to improve robustness but exacerbates degradation, indicating that a same-modality teacher reinforces the student’s reliance on source-domain-specific spurious correlations. Class-Shuffled Resource KD performs at or below the baseline, ruling out soft-label regularization as the primary driver of gains. These results confirm that the student inherits the correct interclass topology from the resource teacher, not merely the numerical smoothing of its soft labels.

Contribution of Resource Channels. We evaluate the teacher and Var-CNN student under temporal drift by selectively ablating resource size (no size), type (no type), or request order (no order) to quantify each channel’s contribution.

As shown in Figure 7, resource size is the strongest discriminative signal: removing it drops the teacher’s 150-day F1-score from 88.97% to 16.16%, while the student drops from 81.49% to 77.34%. Resource type and order are nonetheless non-redundant: ablating type incurs a 6.65% F1-score drop for the teacher under 150-day drift, and shuffling order causes a 14.76% drop. Even when distilling from only partial resource channels (size and type), the student’s crossenvironment robustness remains above the traffic-only baseline. All resource channels thus encode transferable, stable structural information.

![](images/5f2b51346ee8a3eb9bda42f0d8e8ddae3f1a34a158e1ac0a35ead062163f33c6.jpg)  
Figure 7: Per-channel ablation F1-score (%) for the resourceonly teacher and ResAware Var-CNN student across temporal drift (Days 30–150).

Sensitivity of Distillation Weight ??. The weight $\alpha \in [ 0 , 1 ]$ balances hard-label classification and resource-topology supervision in $\mathcal { L } _ { t o t a l }$ . Across backbone and capacity sweeps (Figure 9 and Table 9), the near-optimal range is primarily capacity-dependent and stable across training and testing datasets; we therefore tune ?? once per backbone on the source-domain validation set and fix it for all target environments, with the full analysis deferred to Appendix F. Takeaways. The ablation studies confirm three points: (1) Gains stem from correctly aligned privileged resource knowledge, not from the distillation mechanism or soft-label regularization alone; (2) Resource size is the strongest single channel, while type and order provide complementary structural constraints; (3) ?? is a capacity-matching parameter for each student backbone, calibrated once on the source-domain validation set (full analysis in Appendix F).

## 5.6 Applicability Analysis: When Does ResAware Fail?

The preceding experiments show that ResAware is not an unconditional plug-in enhancer. Its effectiveness relies on two conditions. First, resource sequences must continue to encode stable website identity across the source and target domains. Second, the student must have sufficient capacity to compress the resource teacher’s inter-class topology into a traffic-only representation. When either condition is weakened, the distillation term may provide only limited benefit; when both are violated, it can induce negative transfer. Failure from Broken Traffic-Resource Correspondence. The first failure mode arises when the correspondence between resource structure and observable traffic morphology is substantially disrupted. ResAware is most suitable for temporal and spatial drift, where the perturbation mainly affects the network-observation layer while the resource set, category sequence, and size distribution remain comparatively stable. In contrast, browser drift changes page-load scheduling, connection reuse, preloading behavior, and script execution order. Obfuscation proxy drift can also systematically rewrite the projection from resource events to traffic packet sequences through tunnel multiplexing, fragmentation, outer TLS encapsulation, or WebSocket framing. As a result, ResAware still yields relative gains under browser drift, but the absolute macro-F1 remains low. Obfuscation proxy drift also exhibits clear model dependence: Var-CNN and RF benefit, whereas DF shows slight negative transfer. These results indicate that once the target shift enters the browser execution layer or the protocol encapsulation layer, the teacher’s resource-side soft labels may become a mismatched constraint rather than a stable prior.

![](images/f8fb50d760eb50d84ef8c2896bbfd2ac62b49ed63f343d6ed3effaea3123453f.jpg)

<details>
<summary>line chart</summary>

| Calibration curves comparing w/o and w/ ResAware | Mean Predicted Confidence | Dose/Ey |
| --- | --- | --- |
| w/o ResAware ECE | 0.138 | 0.034 |
| w/o ResAware ECE | 0.138 | 0.034 |
| w/o ResAware ECE | 0.138 | 0.034 |
| w/o ResAware ECE | 0.138 | 0.034 |
| w/o ResAware ECE | 0.138 | 0.034 |
| w/o ResAware ECE | 0.25 | 0.25 |
| w/o ResAware ECE | 0.25 | 0.25 |
| w/o ResAware ECE | 0.25 | 0.25 |
| w/o ResAware ECE | 0.25 | 0.25 |
| w/o ResAware ECE | 0.25 | 0.25 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/o ResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | 0.25 | 0.2 |
| w/oResAware ECE | -0.25 | -0.25 |
| w/oResAware ECE | -0.25 | -0.25 |
| w/oResAware ECE | -0.25 | -0.25 |
| w/oResAware ECE | -0.25 | -0.25 |
| w/oResAware ECE | -0.25 | -0.25 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/oResAware ECE | -0.25 | -0.2 |
| w/o ResAware ECE | -0.138 | -0.138 |
| w/o ResAware ECE | -0.138 | -0.138 |
| w/o ResAware ECE | -0.138 | -0.138 |
| w/o ResAware ECE | -0.138 | -0.138 |
| w/o ResAware ECE | -0.138 | -0.138 |
| w/o ResAware ECE | -0,138 | -0,138 |
| w/o ResAware ECE | -0,138 | -0,138 |
| w/o ResAware ECE | -0,138 | -0,138 |
| w/o ResAware ECE | -0,138 | -0,138 |
| w/o ResAware ECE | -0,138 | -0,138 |
| w/o ResAware ECE (ECE) | 1.138 | 1.138 |
| w/o ResAware ECE (ECE) | 1.138 | 1.138 |
| w/o ResAware ECE (ECE) | 1.138 | 1.138 |
| w/o ResAware ECE (ECE) | 1.138 | 1.138 |
| w/o ResAware ECE (ECE) | 1.136 | 1.136 |
| w/o ResAware ECE (ECE) | 1.136 | 1.136 |
| w/o ResAware ECE (ECE) | 1.136 | 1.136 |
| w/o ResAware ECE (ECE) | 1.136 | 1.136 |
| w/o ResAware ECE (ECE) | 1.136 | 977 |
| w/o ResAware ECE (ECE) | 1.136 | 977 |
| w/o ResAware ECE (ECE) | 1.136 | 977 |
| w/o ResAware ECE (ECE) | 1.136 | 977 |
| w/o ResAware ECE (ECE) | 1.136 | 977 |
| w/ ResAware ECE (ECE) | 1.136 | 977 |
| w/ ResAware ECE (ECE) | 1.136 | 977 |
| w/ ResAware ECE (ECE) | 1.136 | 977 |
| w/ ResAware ECE (ECE) | 1.136 | 977 |
</details>

Figure 8: Calibration and confidence distributions of Var-CNN at Day 150 with and without ResAware. The left panel shows the reliability diagram, while the middle and right panels show the confidence KDEs for correct and incorrect predictions, respectively.

Failure from Insufficient Student Capacity. The second failure mode comes from limited student capacity. ResAware does not expose resource features to the student at inference time; instead, it asks a traffic-only student to fit both hard-label decision boundaries and the resource teacher’s soft topology. The Var-CNN width-scaling experiment in Appendix F shows that smaller students have narrower best ?? ranges and lower gain ceilings. The full-width Var-CNN maintains 80.25%–82.22% macro-F1 within the best range of $\alpha = 0 . 1 – 0 . 7$ , reaching a maximum gain of 9.45 percentage points. In contrast, the 0.125× Var-CNN has a best range of only $\alpha = 0 . 1 { - 0 . 3 }$ , with a maximum gain of 4.60 percentage points. Thus, low-capacity students are not unable to benefit from resource supervision; they simply absorb a weaker teacher constraint. An overly large ?? turns the KD term from structural regularization into an optimization burden.

Deployment Guidelines. Based on the above analysis, we derive three practical guidelines. First, when drift mainly occurs below the resource layer, such as temporal aging, geographic relocation, CDN routing changes, or link-state variation, ResAware is a suitable default training enhancement. When the drift involves browser execution or complex proxy encapsulation, it should be validated per scenario, with the $\alpha = 0$ traffic-only baseline retained as a fallback. Second, ?? should be matched to student capacity and inductive bias: DF, Tik-Tok, and RF benefit most from moderate weights; Var-CNN and CountMamba benefit from medium-to-high weights; AWF should use smaller weights and be checked for negative transfer. Third, deployment should retain only the traffic-only student, with no resource parser or teacher model in the inference pipeline. If a small amount of target-domain traffic is available, ResAware is best used as a stronger source-domain initialization that can be combined with few-shot or unlabeled adaptation.

Table 7: Inter-class topology alignment between Var-CNN with and without ResAware and the resource teacher over 150 days. KL divergence (↓) measures the distributional distance between student and teacher soft outputs; Spearman ?? (↑) measures the rank correlation of per-class similarity orderings.

<table><tr><td rowspan="2">Days</td><td colspan="2">KL to Teacher (↓)</td><td colspan="2">Rel. Spearman ρ (↑)</td></tr><tr><td>w/o Res.</td><td>w/ Res.</td><td>w/o Res.</td><td>w/ Res.</td></tr><tr><td>30</td><td>2.5516</td><td>0.3838</td><td>0.0373</td><td>0.0806</td></tr><tr><td>60</td><td>2.4311</td><td>0.3522</td><td>0.0273</td><td>0.0775</td></tr><tr><td>90</td><td>2.2566</td><td>0.3261</td><td>0.0324</td><td>0.0860</td></tr><tr><td>120</td><td>2.1713</td><td>0.3140</td><td>0.0297</td><td>0.0962</td></tr><tr><td>150</td><td>2.1133</td><td>0.3029</td><td>0.0287</td><td>0.1022</td></tr></table>

## 5.7 Mechanism Analysis: What Does the Student Inherit?

This section investigates a core mechanistic question: what information does the resource teacher transfer to the traffic-only student through heterogeneous distillation? We find that the student inherits the resource-induced inter-class topology and acquires more stable decision boundaries.

ResAware Improves Model Robustness and Calibration. Figure 8 characterizes the effect of ResAware on Var-CNN’s output distribution at Day 150. The reliability diagram [24] shows that the baseline exhibits severe overconfidence (ECE = 0.138), whereas ResAware reduces ECE to 0.034—a nearly fourfold improvement. The confidence KDE reveals a complementary pattern: for correct predictions, ResAware produces a sharper, more concentrated peak near 1.0, indicating higher decisiveness; for incorrect predictions, the baseline clusters errors near high-confidence regions, whereas ResAware shifts the error mass toward lower confidence.

These results show that ResAware does not uniformly suppress confidence; instead, it achieves structural calibration—being more confident when correct and more conservative when wrong. The teacher thus imprints resource-side structural invariants onto the student, guiding it away from overfitting to transient traffic noise. The Student Aligns with the Teacher’s Soft Topology. To quantify how much of the teacher’s inter-class topology the student inherits, we track two metrics over the 150-day drift window. KL divergence measures the distributional distance between the student’s and teacher’s soft output distributions: a lower value indicates that the student assigns similar per-class probability mass as the teacher. Spearman ?? measures the rank correlation between the student’s and teacher’s per-class similarity orderings: a higher value indicates that the student preserves the teacher’s relative inter-class structure [18].

As shown in Table 7, Var-CNN without ResAware remains far from the teacher throughout the window, with KL divergence in the range of 2.1–2.6 and Spearman ?? near zero (0.027–0.037). In contrast, Var-CNN with ResAware maintains substantially closer alignment: KL divergence stays within 0.30–0.38, and Spearman ?? increases steadily from 0.081 at Day 30 to 0.102 at Day 150. These results confirm that the student inherits the resource teacher’s inter-class soft topology rather than simply mimicking hard-label predictions.

Takeaway. ResAware converts resource-side structural priors from the training phase into stable relational supervision signals. At inference, the student relies exclusively on encrypted traffic, yet its decision boundaries are regularized by the resource-induced topology—enabling both higher F1-score and better calibration under long-term drift.

## 6 Limitations and Future Work

ResAware assumes that resource structure retains adequate stability in the target environment. For highly personalized pages, sites under frequent A/B testing, heavily ad-injected platforms, or dynamically generated templates, resource sizes, categories, and loading sequences may fluctuate substantially, weakening the structural priors provided by the teacher. Future work could explore more abstract resource representations—such as dependency graphs, initiator graphs, or rendering-stage topologies—to reduce sensitivity to specific object sizes.

We do not evaluate strong anonymity networks such as Tor. Tor’s fixed-size cells, multiplexing, and congestion control further obscure the correspondence between application-layer resource sizes and observable packet sequences. Extending ResAware to such networks would likely require a resource teacher that de-emphasizes object sizes in favor of sequential or graph-based representations.

Finally, ResAware does not uniformly benefit all backbone–drift combinations. As shown in §5.2 and §5.6, severe browser or obfuscated proxy drift can break the traffic-resource correspondence, while low-capacity students may fail to absorb the teacher’s interclass topology, leading to diminished gains or negative transfer. Future work should develop capacity-aware weighting and driftaware criteria for falling back to traffic-only training when resource supervision becomes unreliable.

## 7 Related Work

Website Fingerprinting Attacks. Deep learning-based WF models, including DF [39], Var-CNN [3], Tik-Tok [31], and Count-Mamba [10], achieve high accuracy in closed-world IID settings by learning low-level packet statistics. However, packet-level signals are jointly shaped by website content structure and transport-layer dynamics: TCP congestion control, HTTP/2 multiplexing, CDN routing, and browser scheduling all modulate observable traffic independently of the page being loaded. Consequently, even modest changes in network path, obfuscated proxy protocol, or browser engine suffice to invalidate learned patterns [7, 8, 22, 34, 38], reflecting a fundamental mismatch between the stability of application-layer content structure and the volatility of its encrypted traffic projec tion [19].

Improving Robustness within the Traffic-Only Threat Model. Existing efforts fall into two categories. The first improves traffic feature representations: Shen et al. [36] use feature attribution and contrastive regularization to suppress defense-induced perturbations; Bahramali et al. [1] simulate network-condition variation via trace augmentation; and Shen et al. [37] pursue transfer-robust training objectives. While each reduces sensitivity to a specific perturbation type, all remain constrained by working within the encrypted traffic domain, since the instability of these signals stems from sources outside the traffic itself, limiting the reach of any representation-level fix.

The second category introduces post-deployment target-domain observations. Few-shot adaptation methods fine-tune the classifier with a small number of labeled target traces [4, 40, 51]; test-time adaptation methods operate on unlabeled target traffic via entropy minimization or distribution alignment [9, 50]. Both improve accuracy under drift but require post-deployment data collection and do not eliminate the root cause: the adapted model still anchors its decision boundaries to volatile traffic-domain signals. ResAware is orthogonally complementary to these methods (§5.4): by providing a more stable source-domain initialization, it amplifies the benefit of subsequent adaptation rather than replacing it.

Resource-Aware Website Fingerprinting. A separate research thread exploits application-layer resource structure as a more stable website identifier. Li et al. [20] show that resource loading sequences exhibit substantially greater cross-environment stability than packet features. HOLMES & WATSON [6] infers HTTP parallelism patterns directly from traffic as lightweight fingerprints; MRCGCN [12] constructs multi-level resource dependency graphs; and STAR [5] trains dual encoders to align traffic and resource representations for zero-shot cross-modal retrieval. These works confirm that resource-level signals offer a more stable encoding of website identity. However, their deployment assumptions differ: HOLMES infers structural signals from traffic alone and therefore needs no resource access at inference, but is bounded by what traffic can reveal about resource structure. MRCGCN and STAR directly incorporate resource graphs or embeddings that must be available at inference time, expanding the attacker’s observational requirement beyond standard passive eavesdropping. ResAware takes a different position: resource information is used exclusively as a privileged training-time supervision signal and fully discarded before deployment, leaving the online model with the same footprint as a conventional traffic-only classifier.

Learning Using Privileged Information and Knowledge Distillation. Vapnik and Izmailov [42, 43] formalize Learning Using Privileged Information (LUPI): auxiliary features available only at training time can substitute for larger datasets by providing richer concept supervision. Lopez-Paz et al. [23] establish a formal equivalence between LUPI and knowledge distillation, showing that teacher-student training on enriched data implements privileged supervision through soft-label transfer. Hinton et al. [14] demonstrate that temperature-scaled KL divergence provides a rich inter-class relational signal beyond one-hot labels. Industrial applications confirm this paradigm: at Taobao, post-click behavioral signals—privileged at training but unavailable at serving—are distilled into click-through-rate predictors with significant accuracy gains [49]. In the security domain, KD has been applied to traffic classification primarily for model compression [18, 26], not crossmodal generalization. To our knowledge, no prior WF work has formalized webpage resource structure as privileged information or exploited the training-rich / inference-poor asymmetry to provide environment-agnostic supervision. ResAware fills this gap by treating the resource modality as a privileged teacher that transfers inter-class topology to a traffic-only student without expanding the online attacker’s observational boundary.

## 8 Conclusion

This paper presents ResAware to address the performance degradation of WF models under environmental shift. By formalizing a training-rich / inference-poor asymmetric threat model, ResAware uses stable application-layer resource sequences as privileged supervision to regularize traffic-only student models. Our findings show that internalizing resource-induced class topology allows the student to move beyond the observational limitations of the traffic modality, anchoring on a website’s intrinsic identity rather than environment-specific traffic artifacts. Evaluated on a dataset spanning 5 months and 6 global vantage points, ResAware consistently improves the robustness of diverse WF architectures—including an 8.72% F1-score gain for Var-CNN under 150-day temporal drift. With zero inference overhead and orthogonal compatibility with existing adaptation methods, ResAware provides a practical foundation for robust website fingerprinting in real-world deployments.

## References

[1] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic Website Fingerprinting By Augmenting Network Traces. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security, CCS 2023, Copenhagen, Denmark, November 26-30, 2023, Weizhi Meng, Christian Damsgaard Jensen, Cas Cremers, and Engin Kirda (Eds.). ACM, New York, NY, USA, 1035– 1049. doi:10.1145/3576915.3616639  
[2] Donald J. Berndt and James Clifford. 1994. Using dynamic time warping to find patterns in time series. In Proceedings of the 3rd International Conference on Knowledge Discovery and Data Mining (Seattle, WA) (AAAIWS’94). AAAI Press, 359–370.  
[3] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2019. Var-CNN: A Data-Efficient Website Fingerprinting Attack Based on Deep Learning. Proc. Priv. Enhancing Technol. 2019, 4 (2019), 292–310. doi:10.2478/POPETS-2019-0070  
[4] Mantun Chen, Yongjun Wang, Hongzuo Xu, and Xiatian Zhu. 2021. Few-shot website fingerprinting attack. Comput. Netw. 198, C (Oct. 2021), 12 pages. doi:10. 1016/j.comnet.2021.108298  
[5] Yifei Cheng, Yujia Zhu, Baiyang Li, Xinhao Deng, Yitong Cai, Yaochen Ren, and Qingyun Liu. 2025. STAR: Semantic-Traffic Alignment and Retrieval for Zero-Shot HTTPS Website Fingerprinting. CoRR abs/2512.17667 (2025). arXiv:2512.17667 doi:10.48550/ARXIV.2512.17667  
[6] Yifei Cheng, Yujia Zhu, Baiyang Li, Peishuai Sun, Yong Ding, Xinhao Deng, and Qingyun Liu. 2025. HOLMES & WATSON: A Robust and Lightweight HTTPS Website Fingerprinting through HTTP Version Parallelism. In Proceedings of the ACM on Web Conference 2025, WWW 2025, Sydney, NSW, Australia, 28 April 2025- 2 May 2025, Guodong Long, Michale Blumestein, Yi Chang, Liane Lewin-Eytan, Zi Helen Huang, and Elad Yom-Tov (Eds.). ACM, 1078–1092. doi:10.1145/3696410. 3714578  
[7] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online Website Fingerprinting: Evaluating Website Fingerprinting Attacks on Tor in the Real World. In 31st USENIX Security Symposium, USENIX Security 2022, Boston, MA, USA, August 10-12, 2022, Kevin R. B. Butler and Kurt Thomas (Eds.). USENIX Association, 753–770. https://www.usenix.org/conference/usenixsecurity22/ presentation/cherubin  
[8] Xinhao Deng, Jingyou Chen, Linxiao Yu, Yixiang Zhang, Zhongyi Gu, Changhao Qiu, Xiyuan Zhao, Ke Xu, and Qi Li. 2025. Beyond a Single Perspective: Towards a Realistic Evaluation of Website Fingerprinting Attacks. CoRR abs/2510.14283 (2025). arXiv:2510.14283 doi:10.48550/ARXIV.2510.14283  
[9] Xinhao Deng, Yixiang Zhang, Qi Li, Zhuotao Liu, Yabo Wang, and Ke Xu. 2026. Enhancing Website Fingerprinting Attacks against Traffic Drift. In Network and Distributed System Security (NDSS) Symposium. Internet Society. https://www.ndss-symposium.org/ndss-paper/enhancing-websitefingerprinting-attacks-against-traffic-drift/  
[10] Xianwen Deng, Ruijie Zhao, Yanhao Wang, Mingwei Zhan, Zhi Xue, and Yijun Wang. 2025. Countmamba: A Generalized Website Fingerprinting Attack via Coarse-Grained Representation and Fine-Grained Prediction. In 2025 IEEE Symposium on Security and Privacy (SP). 1419–1437. doi:10.1109/SP61157.2025.00154  
[11] Roy T. Fielding, Mark Nottingham, and Julian Reschke. 2022. HTTP Semantics. RFC 9110. doi:10.17487/RFC9110  
[12] Bo Gao, Weiwei Liu, Guangjie Liu, Fengyuan Nie, and Jianan Huang. 2025. Multi-Level Resource-Coherented Graph Learning for Website Fingerprinting Attacks. IEEE Trans. Inf. Forensics Secur. 20 (2025), 693–708. doi:10.1109/TIFS.2024.3520014  
[13] Jamie Hayes and George Danezis. 2016. k-fingerprinting: A Robust Scalable Website Fingerprinting Technique. In 25th USENIX Security Symposium, USENIX  
Security 16, Austin, TX, USA, August 10-12, 2016, Thorsten Holz and Stefan Savage (Eds.). USENIX Association, 1187–1203. https://www.usenix.org/conference/ usenixsecurity16/technical-sessions/presentation/hayes  
[14] Geoffrey E. Hinton, Oriol Vinyals, and Jeffrey Dean. 2015. Distilling the Knowledge in a Neural Network. CoRR abs/1503.02531 (2015). arXiv:1503.02531 http://arxiv.org/abs/1503.02531  
[15] Andrew Hintz. 2002. Fingerprinting websites using traffic analysis. In Proceedings of the 2nd International Conference on Privacy Enhancing Technologies (San Francisco, CA, USA) (PET’02). Springer-Verlag, Berlin, Heidelberg, 171–178.  
[16] Paul E. Hoffman and Patrick McManus. 2018. DNS Queries over HTTPS (DoH). RFC 8484. doi:10.17487/RFC8484  
[17] Guodong Huang, Chuan Ma, Ming Ding, Yuwen Qian, Chunpeng Ge, Liming Fang, and Zhe Liu. 2023. Efficient and Low Overhead Website Fingerprinting Attacks and Defenses based on TCP/IP Traffic. In Proceedings of the ACM Web Conference 2023 (Austin, TX, USA) (WWW ’23). Association for Computing Machinery, New York, NY, USA, 1991–1999. doi:10.1145/3543507.3583200  
[18] Tao Huang, Shan You, Fei Wang, Chen Qian, and Chang Xu. 2022. Knowledge distillation from a stronger teacher. In Proceedings of the 36th International Conference on Neural Information Processing Systems (New Orleans, LA, USA) (NIPS ’22). Curran Associates Inc., Red Hook, NY, USA, Article 2443, 12 pages.  
[19] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Rachel Greenstadt. 2014. A Critical Evaluation of Website Fingerprinting Attacks. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security (Scottsdale, Arizona, USA) (CCS ’14). Association for Computing Machinery, New York, NY, USA, 263–274. doi:10.1145/2660267.2660368  
[20] Changzhi Li, Lihai Nie, Laiping Zhao, and Keqiu Li. 2023. Robust website fingerprinting through resource loading sequence. World Wide Web (WWW) 26, 5 (2023), 2329–2349. doi:10.1007/S11280-023-01138-2  
[21] Dongpu Li, Qifeng Yuan, Tan Li, Shuangwu Chen, and Jian Yang. 2020. Crossdomain Network Traffic Classification Using Unsupervised Domain Adaptation. In 2020 International Conference on Information Networking (ICOIN). 245–250. doi:10.1109/ICOIN48656.2020.9016470  
[22] Jianfeng Li, Dongliang Wang, Yixuan Liu, Yifei Gao, Xiaorong Zhang, Zheng Lin, Xiaobo Ma, Xiapu Luo, and Xiaohong Guan. 2025. Cross-Environmental Website Fingerprinting. In IEEE INFOCOM 2025 - IEEE Conference on Computer Communications, London, United Kingdom, May 19-22, 2025. IEEE, 1–10. doi:10. 1109/INFOCOM55648.2025.11044569  
[23] David Lopez-Paz, Léon Bottou, Bernhard Schölkopf, and Vladimir Vapnik. 2016. Unifying distillation and privileged information. In 4th International Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico, May 2-4, 2016, Conference Track Proceedings, Yoshua Bengio and Yann LeCun (Eds.). http: //arxiv.org/abs/1511.03643  
[24] Matthias Minderer, Josip Djolonga, Rob Romijnders, Frances Hubis, Xiaohua Zhai, Neil Houlsby, Dustin Tran, and Mario Lucic. 2021. Revisiting the Calibration of Modern Neural Networks. In Advances in Neural Information Processing Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual, Marc’Aurelio Ranzato, Alina Beygelzimer, Yann N. Dauphin, Percy Liang, and Jennifer Wortman Vaughan (Eds.). 15682–15694. https://proceedings.neurips.cc/paper/2021/hash/ 8420d359404024567b5aefda1231af24-Abstract.html  
[25] Ravi Netravali, Ameesh Goyal, James Mickens, and Hari Balakrishnan. 2016. Polaris: Faster Page Loads Using Fine-grained Dependency Tracking. In 13th USENIX Symposium on Networked Systems Design and Implementation, NSDI 2016, Santa Clara, CA, USA, March 16-18, 2016, Katerina J. Argyraki and Rebecca Isaacs (Eds.). USENIX Association, 123–136. https://www.usenix.org/conference/ nsdi16/technical-sessions/presentation/netravali  
[26] Quanbo Pan, Yang Yu, Hanbing Yan, Maoli Wang, and Bingzhi Qi. 2024. ETKD: A Semi-Supervised Learning-based Knowledge Distillation Model for Encrypted Traffic Classification. In 2024 IEEE International Conference on Systems, Man, and Cybernetics (SMC). 4528–4533. doi:10.1109/SMC54092.2024.10831035  
[27] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale. In 23rd Annual Network and Distributed System Security Symposium, NDSS 2016, San Diego, California, USA, February 21-24, 2016. The Internet Society. http://wp.internetsociety.org/ndss/wp-content/uploads/sites/25/2017/09/ website-fingerprinting-internet-scale.pdf  
[28] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale. In 23rd Annual Network and Distributed System Security Symposium, NDSS 2016, San Diego, California, USA, February 21-24, 2016. The Internet Society. http://wp.internetsociety.org/ndss/wp-content/uploads/sites/25/2017/09/ website-fingerprinting-internet-scale.pdf  
[29] Victor Le Pochat, Tom van Goethem, Samaneh Tajalizadehkhoob, Maciej Korczynski, and Wouter Joosen. 2019. Tranco: A Research-Oriented Top Sites Ranking Hardened Against Manipulation. In 26th Annual Network and Distributed System Security Symposium, NDSS 2019, San Diego, California, USA, February 24-27, 2019. The Internet Society. https://www.ndss-symposium.org/ndss-paper/tranco-aresearch-oriented-top-sites-ranking-hardened-against-manipulation/  
[30] Project X Community. 2020. Project X Xray-core. Accessed: 2026-04-28.  
[31] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gangadhara, and Matthew Wright. 2020. Tik-Tok: The Utility of Packet Timing in Website Fingerprinting Attacks. Proc. Priv. Enhancing Technol. 2020, 3 (2020), 5–24. doi:10.2478/POPETS-2020-0043  
[32] Eric Rescorla, Kazuho Oku, Nick Sullivan, and Christopher A. Wood. 2025. TLS Encrypted Client Hello. Internet-Draft draft-ietf-tls-esni-25. Internet Engineering Task Force. https://datatracker.ietf.org/doc/draft-ietf-tls-esni/25/ Work in Progress.  
[33] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom van Goethem, and Wouter Joosen. 2018. Automated Website Fingerprinting through Deep Learning. In 25th Annual Network and Distributed System Security Symposium, NDSS 2018, San Diego, California, USA, February 18-21, 2018. The Internet Society. https://www.ndss-symposium.org/wp-content/uploads/2018/02/ndss2018\_ 03A-1\_Rimmer\_paper.pdf  
[34] Mohammadhamed Shadbeh, Khashayar Khajavi, and Tao Wang. 2026. Reality Check for Tor Website Fingerprinting in the Open World. CoRR abs/2603.07412 (2026). arXiv:2603.07412 doi:10.48550/ARXIV.2603.07412  
[35] shadowsocks.org. 2016. Shadowsocks — A fast tunnel proxy that helps you bypass firewalls. https://shadowsocks.org/  
[36] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subverting Website Fingerprinting Defenses with Robust Traffic Representation. In 32nd USENIX Security Symposium (USENIX Security 23). USENIX Association, Anaheim, CA, 607–624. https://www.usenix.org/conference/usenixsecurity23/ presentation/shen-meng  
[37] Meng Shen, Jinhe Wu, Junyu Ai, Qi Li, Chenchen Ren, Ke Xu, and Liehuang Zhu. 2025. Swallow: A Transfer-Robust Website Fingerprinting Attack via Consistent Feature Learning. In Proceedings of the 2025 ACM SIGSAC Conference on Computer and Communications Security, CCS 2025, Taipei, Taiwan, October 13-17, 2025, Chun-Ying Huang, Jyh-Cheng Chen, Shiuh-Pyng Shieh, David Lie, and Véronique Cortier (Eds.). ACM, 1574–1588. doi:10.1145/3719027.3744795  
[38] Anatoly Shusterman, Roie David, and Yossi Oren. 2026. Understanding and addressing concept drift in website fingerprinting. Computer Networks 275 (1 Feb. 2026). doi:10.1016/j.comnet.2025.111811 Publisher Copyright: © 2025 The Author(s).  
[39] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep Fingerprinting: Undermining Website Fingerprinting Defenses with Deep Learning. In Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security, CCS 2018, Toronto, ON, Canada, October 15-19, 2018, David Lie, Mohammad Mannan, Michael Backes, and XiaoFeng Wang (Eds.). ACM, 1928–1943. doi:10.1145/3243734.3243768  
[40] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet Fingerprinting: More Practical and Portable Website Fingerprinting with N-shot Learning. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security, CCS 2019, London, UK, November 11-15, 2019, Lorenzo Cavallaro, Johannes Kinder, XiaoFeng Wang, and Jonathan Katz (Eds.). ACM, 1131–1148. doi:10.1145/3319535.3354217  
[41] trojan-gfw. 2023. Trojan Documentation — trojan-gfw.github.io. Accessed: 2026- 04-28.  
[42] Vladimir Vapnik and Rauf Izmailov. 2015. Learning using privileged information: similarity control and knowledge transfer. J. Mach. Learn. Res. 16 (2015), 2023– 2049. doi:10.5555/2789272.2886814  
[43] Vladimir Vapnik and Akshay Vashist. 2009. A new learning paradigm: Learning using privileged information. Neural Networks 22, 5-6 (2009), 544–557. doi:10. 1016/J.NEUNET.2009.06.042  
[44] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is all you need. In Proceedings of the 31st International Conference on Neural Information Processing Systems (Long Beach, California, USA) (NIPS’17). Curran Associates Inc., Red Hook, NY, USA, 6000–6010.  
[45] Dequan Wang, Evan Shelhamer, Shaoteng Liu, Bruno Olshausen, and Trevor Darrell. 2021. Tent: Fully Test-Time Adaptation by Entropy Minimization. In International Conference on Learning Representations. https://openreview.net/ forum?id=uXl3bZLkr3c  
[46] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Effective Attacks and Provable Defenses for Website Fingerprinting. In Proceedings of the 23rd USENIX Security Symposium, San Diego, CA, USA, August 20-22, 2014, Kevin Fu and Jaeyeon Jung (Eds.). USENIX Association, 143– 157. https://www.usenix.org/conference/usenixsecurity14/technical-sessions/ presentation/wang\_tao  
[47] Xiao Sophia Wang, Aruna Balasubramanian, Arvind Krishnamurthy, and David Wetherall. 2013. Demystifying Page Load Performance with WProf. In 10th USENIX Symposium on Networked Systems Design and Implementation (NSDI 13). USENIX Association, Lombard, IL, 473–485. https://www.usenix.org/conference/ nsdi13/technical-sessions/presentation/wang\_xiao  
[48] Yi Xie, Jiahao Feng, Wenju Huang, Yixi Zhang, Xueliang Sun, Xiaochou Chen, and Xiapu Luo. 2024. Contrastive Fingerprinting: A Novel Website Fingerprinting Attack over Few-shot Traces. In Proceedings of the ACM on Web Conference 2024,  
WWW 2024, Singapore, May 13-17, 2024, Tat-Seng Chua, Chong-Wah Ngo, Ravi Kumar, Hady W. Lauw, and Roy Ka-Wei Lee (Eds.). ACM, 1203–1214. doi:10. 1145/3589334.3645575  
[49] Chen Xu, Quan Li, Junfeng Ge, Jinyang Gao, Xiaoyong Yang, Changhua Pei, Fei Sun, Jian Wu, Hanxiao Sun, and Wenwu Ou. 2020. Privileged Features Distillation at Taobao Recommendations. In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining (Virtual Event, CA, USA) (KDD ’20). Association for Computing Machinery, New York, NY, USA, 2590–2598. doi:10.1145/3394486.3403309  
[50] Guoqiang Zhang, Jiahao Cao, Mingwei Xu, and Xinhao Deng. 2023. Unsupervised and Adaptive Tor Website Fingerprinting. In International Conference on Security and Privacy in Communication Systems. Springer, 209–229.  
[51] Hongcheng Zou, Jinshu Su, Ziling Wei, Shuhui Chen, and Baokang Zhao. 2022. An efficient cross-domain few-shot website fingerprinting attack with Brownian distance covariance. Comput. Networks 219 (2022), 109461. doi:10.1016/J. COMNET.2022.109461

## A Open Science

Research artifacts have been de-identified for double-blind review and are hosted at: https://github.com/aimafan123/ResAware. The repository includes the full training and evaluation code for the ResAware distillation framework and teacher model, along with implementations of six WF backbones—AWF, DF, Var-CNN, Tik-Tok, RF, and CountMamba—reproduced from their original papers or official codebases.

The artifact suite also includes scripts for zero-shot evaluation across four drift scenarios (temporal, spatial, obfuscated proxy, and browser), open-world temporal drift testing, and few-shot adaptation supporting both supervised and Proteus-based unsupervised modes. Due to storage constraints and privacy considerations, we provide featurized versions of our cross-environment datasets. Automated pipelines for data processing, training, and evaluation are included to facilitate efficient reproduction of the core experimental results.

## B Ethical Considerations

This research follows the established ethical guidelines of the security community for network measurement and privacy analysis. Our practices are as follows.

Data Collection and Privacy Protection. All network traffic was generated by automated headless browsers on vantage points controlled by our team. We accessed only publicly indexable websites (a subset of the Tranco Top 100K [29]). Data collection complied with each site’s robots.txt directives and terms of service. No real user browsing behavior, personally identifiable information (PII), or private communication content was involved at any stage. TLS session keys were extracted within our controlled client processes solely to reconstruct application-layer resource events and were neither retained beyond this purpose nor shared. Upon publication, we will release only featurized representations—packet direction and length sequences for traffic, and category and size sequences for resource loading. No raw payloads, URLs, IP addresses, or user-linked identifiers will be included, fully mitigating privacy risks while preserving research utility.

Selection of Monitored Sites. The 100 monitored sites were randomly sampled from the Tranco Top 100K list. To minimize exposure to politically sensitive content, we manually excluded sites identified by international human rights organizations as subject to mandatory censorship. The 83,645 unmonitored sites were also drawn from the Tranco rankings and do not target specific user groups or sensitive content.

Dual-Use and Responsible Disclosure. WF attack research is widely recognized as a prerequisite for improving privacy defenses: only by understanding and quantifying attacker capabilities can defenders design effective countermeasures. This paper focuses on the root causes of cross-environment WF failures rather than expanding online attacker capabilities. The core insight of ResAware—that unstable traffic-side supervision is the fundamental driver of generalization failure—provides direct guidance for defensive research. Defenders can introduce targeted perturbations at the resource-loading level—randomizing loading orders, injecting dummy requests, or diversifying resource type distributions—to undermine the stable resource-side inductive bias that ResAware exploits, complementing existing packet-level defenses. We will also release the large-scale paired traffic-resource dataset to lower the barrier for cross-environment WF research. Covering temporal, spatial, obfuscated proxy, and browser distribution shifts, this dataset represents one of the most comprehensive cross-environment WF benchmarks and will help the community evaluate attacks and defenses under unified protocols.

## C ResAware Training and Deployment Protocol

Algorithm 1 formalizes the three-stage training and deployment protocol of ResAware introduced in §4. Stage 1 extracts two-channel privileged resource features from raw resource records and trains the resource-only teacher under hard-label supervision. Stage 2 freezes the teacher and distills its soft-target distributions into the traffic-only student through a weighted combination of classifica tion loss and KL-divergence distillation loss. Stage 3 discards all resource-side components—the resource extractor, teacher model, cached soft labels, and distillation loss—before deployment, so that the deployed student operates on encrypted traffic alone with zero additional inference overhead.

## D Dataset Construction and Collection Details

## D.1 Methodology for Traffic-Resource Pairing

This section outlines the methodology for constructing trace-level traffic-resource pairs from a single controlled page visit. For each page load, we define a trace as the aggregate network activity triggered by a complete page visit. For each crawler visit, we simultaneously capture raw encrypted traffic and the corresponding TLS session keys. In the offline phase, we reconstruct application-layer resource sequences and align them with the captured traffic traces. The detailed procedure for resource sequence recovery is provided in Algorithm 2.

## D.2 Dataset Information

To evaluate cross-environment robustness, we construct a dataset suite we term the ResAware Dataset Suite. This suite is partitioned into multiple subsets, each isolating a distinct experimental factor: temporal evolution, spatial diversity, obfuscated proxy encapsulation, browser variation, and open-world background traffic.

Algorithm 1: Resource-Privileged Distillation for Traffic-Only WF  
Input: Source-domain paired training set $\mathcal{D}_{s}=\{(x_{i},R_{i},y_{i})\}_{i=1}^{n}$ , where $R_{i}$ denotes raw resource records; resource teacher $T_{\theta_{T}}$ ; traffic student $S_{\theta_{S}}$ ; truncation length N; temperature $\tau$ ; distillation weight $\alpha$ Output: Deployed traffic-only student $S_{\theta_{S}}$ // Stage 1: extract two-channel privileged resource features and train the teacher

1 foreach sample $(x_{i},R_{i},y_{i})\in\mathcal{D}_{s}$ do

2 $Z_{i}\leftarrow$ SortByRequestOrder( $R_{i}$ );

3 $c_{i}\leftarrow$ MapTypeToCategory( $Z_{i}$ ); // categorical channel

4 $\tilde{s}_{i}\leftarrow\log(1+\text{PayloadBytes}(Z_{i}))$ ; // size channel

5 $x_{i}^{*}\leftarrow\text{Pad/Truncate}_{N}\big([(c_{i,1},\tilde{s}_{i,1}),\ldots,(c_{i,|Z_{i}|},\tilde{s}_{i,|Z_{i}|})]\big)$ ;

6 end

7 Construct privileged set $D_{s}^{*}=\{(x_{i},x_{i}^{*},y_{i})\}_{i=1}^{n}$ ;

8 foreach mini-batch $B^{*}\subset\{(x_{i}^{*},y_{i})\mid(x_{i},x_{i}^{*},y_{i})\in\mathcal{D}_{s}^{*}\}$ do

9 $z_{T}\leftarrow T_{\theta_{T}}(x^{*})$ ;

10 $L_{T}\leftarrow\text{CE}(\sigma(z_{T}),y)$ ;

11 update $\theta_{T}$ by minimizing $L_{T}$ ;

12 end

13 Freeze $\theta_{T}$ ;

// Stage 2: distill resource knowledge into the traffic-only student

14 foreach mini-batch $B\subset D_{s}^{*}$ do

15 $z_{T}\leftarrow T_{\theta_{T}}(x^{*})$ ; // privileged branch; no gradient to T

16 $z_{S}\leftarrow S_{\theta_{S}}(x)$ ; // deployable branch

17 $L_{cls}\leftarrow\text{CE}(\sigma(z_{S}),y)$ ;

18 $L_{kd}\leftarrow\tau^{2}D_{KL}(\sigma(z_{T}/\tau)\parallel\sigma(z_{S}/\tau))$ ;

19 $L_{total}\leftarrow(1-\alpha)L_{cls}+\alphaL_{kd}$ ;

20 update $\theta_{S}$ by minimizing $L_{total}$ ;

21 end

// Stage 3: discard privileged components before deployment

22 Discard resource extractor, $T_{\theta_{T}}$ , cached soft labels, and distillation losses;

23 return $S_{\theta_{S}}$ for online inference on encrypted traffic x only;

To ensure environmental consistency across subsets, all vantage points run on Virtual Private Servers (VPS) hosted by Vultr1. Each VPS uses an identical base configuration: Debian 13 OS, 1 vCPU, 2 GB RAM, 64 GB NVMe storage, and 2 TB bandwidth. During collection, two isolated Docker containers ran concurrently on each VPS to execute crawling tasks, providing a clean and reproducible environment. Each access targeted the site’s homepage with a fixed 50-second capture window to cover initial page loads, asynchronous requests, and deferred resource loading. The automated browser scrolled the page three times at random intervals to trigger lazyloaded images, scripts, and advertisement resources. After each visit, a screenshot was saved and a quality control (QC) pipeline filtered out failed visits, error pages, blank pages, and incomplete loads.

Algorithm 2: Offline Privileged Resource Sequence Reconstruction  
Input: Encrypted packet sequence x, TLS session keys K
Output: Two-channel privileged resource sequence $x^{*}$ // Recover application-layer records offline

1 $x_{dec} \leftarrow \text{DecryptTraffic}(x, K)$ ;

2 $C \leftarrow \emptyset$ ; // Connection state map

3 $Z \leftarrow \emptyset$ ;

// Group decrypted application frames into resource streams

4 foreach application frame $a \in x_{dec}$ do

5 $f \leftarrow \text{FlowTuple}(a)$ ;

6 $sid \leftarrow \text{StreamID}(a)$ ;

7    if $sid \notin C[f]$ then

8 $C[f][sid] \leftarrow \text{NewStream}()$ ;

9    end

10 $S \leftarrow C[f][sid]$ ;

11    if $a \in RequestHeaders$ then

12 $S.t_{req} \leftarrow a.\text{time}$ ;

13    end

14    if $a \in ResponseHeaders$ then

15 $S.\text{type} \leftarrow \text{InferResourceType}(a)$ ;

16    end

17    if $a \in DataFrame$ then

18 $S.\text{size} \leftarrow S.\text{size} + a.\text{length}$ ;

19    end

20 end

// Keep complete streams and form a two-channel sequence

21 foreach stream $S \in C$ do

22    if S.type exists and S.size > 0 then

23 $Z \leftarrow Z \cup \{(S.t_{req}, S.\text{type}, S.\text{size})\}$ ;

24    end

25 end

26 $Z \leftarrow \text{SortByRequestTime}(Z)$ ;

27 $x^{*} \leftarrow [(type_{1}, size_{1}), \ldots, (type_{|Z|}, size_{|Z|})]$ ;

28 return $x^{*}$ ;

The collected subsets are described below:

• Train-Base: The source-domain training set for temporal and spatial drift experiments. Collected on November 21, 2025 from 6 VPS in New York, US, using Chrome with standard HTTPS/TLS. It covers 100 monitored sites at 150 traces per site (15,000 paired traces total).  
• Open-World: The unmonitored background pool for openworld evaluation, collected on November 21, 2025 from 6 VPS in New York, US with settings identical to Train-Base. Starting from 100,000 Tranco Top 100K [29] candidate sites, we retain 83,645 after excluding monitored-set overlap and filtering failed or anomalous visits. Each site contributes

one trace (83,645 total), used exclusively as the negative background pool.

• Geo-Drift: Used for spatial drift experiments. Collected on November 21, 2025 across five international vantage points—Japan (Tokyo), Singapore, South Africa (Johannesburg), Australia (Sydney), and Germany (Frankfurt)—using 10 VPS in total. All settings mirror Train-Base. It covers the same 100 monitored sites at 25-30 traces per site per location (14,087 paired traces across five locations).  
• Time-Drift: Used for temporal drift experiments, comprising five snapshots collected on December 21, 2025; January 20, 2026; February 19, 2026; March 21, 2026; and April 20, 2026—corresponding to 30, 60, 90, 120, and 150 days after Train-Base. Each snapshot uses 2 VPS in New York, US, with 30 traces per site for the 100 monitored sites (15,000 paired traces across five snapshots).  
• Train-Base-2: The source-domain training set for obfuscated proxy and browser drift experiments. Collected on March 21, 2026 from 6 VPS in New York, US with configurations identical to Train-Base, covering 100 monitored sites at 150 traces per site (15,000 paired traces). Its temporal alignment with the obfuscated proxy and browser test sets controls for long-term temporal drift, so that observed performance differences are attributable primarily to protocol or browser variation.  
Obfuscated-Proxy-Drift: Used for obfuscated proxy drift experiments. Collected on March 21, 2026 using 12 client VPS in New York, US; all traffic was forwarded through Xray proxies. Two additional VPS served as Xray proxy servers, each handling three obfuscation protocols, with two client VPS assigned per protocol. Both clients and servers run Xray-core v26.1.232. It covers 100 monitored sites at 30 traces per site per protocol (18,000 paired traces across six protocols).  
• Browser-Drift: Used for browser drift experiments. Collected on March 21, 2026 using 4 VPS in New York, US (2 per browser: Edge and Firefox); all other settings match Train-Base-2. It covers 100 monitored sites at 25-30 traces per browser per site (5,523 paired traces total).

## E Complete Per-Environment Zero-Shot Results Across All Drift Scenarios

Table 8 reports the complete per-environment closed-world F1- score for all six backbones evaluated in §5.2, complementing the aggregated results in Table 2. Across 108 backbone-environment combinations, ResAware yields positive gains in 84 cases (77.78%) and negative gains in 24 cases, indicating broad but not unconditional effectiveness. Negative cases mainly arise from low-capacity AWF under temporal/spatial/proxy/browser drift and from several protocol-induced proxy settings for DF/Tik-Tok, consistent with the applicability analysis in §5.6.

Table 8: Complete per-environment zero-shot closed-world F1-score for all six backbones with (w/) and without (w/o) ResAware across all drift scenarios. Values are Mean ± SD.

<table><tr><td rowspan="2">Scenario</td><td rowspan="2">Target Env.</td><td colspan="2">AWF</td><td colspan="2">DF</td><td colspan="2">RF</td><td colspan="2">Tik-Tok</td><td colspan="2">Var-CNN</td><td colspan="2">CountMamba</td></tr><tr><td>w/o</td><td>w/</td><td>w/o</td><td>w/</td><td>w/o</td><td>w/</td><td>w/o</td><td>w/</td><td>w/o</td><td>w/</td><td>w/o</td><td>w/</td></tr><tr><td rowspan="6">Temporal Drift</td><td>Day 30</td><td>51.26 ± 9.16</td><td>51.04 ± 3.70</td><td>91.28 ± 0.36</td><td>91.72 ± 0.69</td><td>90.46 ± 0.95</td><td>89.99 ± 0.82</td><td>89.07 ± 0.66</td><td>90.39 ± 0.30</td><td>91.68 ± 0.80</td><td>93.95 ± 0.65</td><td>87.79 ± 1.32</td><td>87.06 ± 0.67</td></tr><tr><td>Day 60</td><td>48.17 ± 8.36</td><td>49.00 ± 2.97</td><td>86.75 ± 1.24</td><td>87.25 ± 0.62</td><td>45.88 ± 1.94</td><td>47.71 ± 1.85</td><td>78.63 ± 1.89</td><td>81.45 ± 1.22</td><td>88.63 ± 1.78</td><td>93.38 ± 0.44</td><td>35.26 ± 3.31</td><td>36.09 ± 3.76</td></tr><tr><td>Day 90</td><td>40.15 ± 6.10</td><td>39.58 ± 2.00</td><td>73.60 ± 0.67</td><td>76.46 ± 0.89</td><td>39.84 ± 1.89</td><td>42.37 ± 1.46</td><td>66.57 ± 1.13</td><td>69.72 ± 0.56</td><td>80.37 ± 1.95</td><td>86.37 ± 0.73</td><td>31.79 ± 2.03</td><td>32.81 ± 1.03</td></tr><tr><td>Day 120</td><td>38.20 ± 5.35</td><td>37.89 ± 2.28</td><td>67.35 ± 0.92</td><td>71.38 ± 1.55</td><td>36.53 ± 2.04</td><td>38.73 ± 1.90</td><td>59.34 ± 1.14</td><td>62.67 ± 1.30</td><td>79.44 ± 1.99</td><td>87.60 ± 1.42</td><td>29.79 ± 2.89</td><td>29.38 ± 1.22</td></tr><tr><td>Day 150</td><td>33.25 ± 5.23</td><td>32.25 ± 3.41</td><td>61.39 ± 1.11</td><td>65.79 ± 1.49</td><td>36.64 ± 2.46</td><td>38.27 ± 1.06</td><td>54.64 ± 0.84</td><td>57.67 ± 0.65</td><td>72.77 ± 1.63</td><td>81.49 ± 1.61</td><td>28.94 ± 2.34</td><td>29.16 ± 2.21</td></tr><tr><td>AVG</td><td>42.21 ± 6.63</td><td>41.95 ± 2.76</td><td>76.07 ± 0.56</td><td>78.52 ± 0.93</td><td>49.87 ± 1.69</td><td>51.41 ± 1.30</td><td>69.65 ± 1.01</td><td>72.38 ± 0.50</td><td>82.58 ± 1.54</td><td>88.56 ± 0.84</td><td>42.71 ± 2.33</td><td>42.90 ± 1.70</td></tr><tr><td rowspan="6">Spatial Drift</td><td>AU</td><td>53.83 ± 8.71</td><td>53.33 ± 4.08</td><td>87.04 ± 0.26</td><td>88.13 ± 0.45</td><td>79.01 ± 0.73</td><td>79.65 ± 0.72</td><td>85.44 ± 0.25</td><td>86.98 ± 0.29</td><td>84.74 ± 0.73</td><td>87.44 ± 0.54</td><td>74.87 ± 1.25</td><td>79.31 ± 0.95</td></tr><tr><td>DE</td><td>40.80 ± 7.88</td><td>40.07 ± 3.16</td><td>81.99 ± 0.81</td><td>84.65 ± 1.11</td><td>77.21 ± 0.87</td><td>83.14 ± 0.62</td><td>80.87 ± 0.88</td><td>82.29 ± 0.31</td><td>81.99 ± 0.45</td><td>85.66 ± 1.07</td><td>77.05 ± 0.88</td><td>76.56 ± 0.18</td></tr><tr><td>JP</td><td>50.95 ± 8.56</td><td>50.73 ± 3.98</td><td>84.50 ± 0.41</td><td>86.38 ± 0.22</td><td>78.80 ± 0.42</td><td>80.69 ± 0.50</td><td>83.05 ± 0.39</td><td>84.92 ± 0.24</td><td>83.21 ± 1.06</td><td>88.11 ± 0.68</td><td>74.14 ± 1.64</td><td>76.84 ± 0.37</td></tr><tr><td>SG</td><td>51.64 ± 7.69</td><td>51.18 ± 2.84</td><td>86.84 ± 0.52</td><td>88.65 ± 0.33</td><td>79.79 ± 1.02</td><td>82.35 ± 0.34</td><td>83.97 ± 0.35</td><td>86.51 ± 0.58</td><td>84.71 ± 1.28</td><td>88.64 ± 0.21</td><td>75.44 ± 0.64</td><td>77.77 ± 0.21</td></tr><tr><td>ZA</td><td>48.93 ± 5.55</td><td>48.50 ± 2.94</td><td>83.16 ± 1.02</td><td>85.37 ± 0.40</td><td>65.76 ± 1.95</td><td>67.23 ± 1.37</td><td>80.93 ± 0.75</td><td>84.79 ± 0.28</td><td>78.67 ± 0.54</td><td>84.97 ± 0.53</td><td>63.05 ± 1.48</td><td>69.69 ± 1.61</td></tr><tr><td>AVG</td><td>49.23 ± 7.57</td><td>48.76 ± 3.36</td><td>84.71 ± 0.34</td><td>86.64 ± 0.28</td><td>76.11 ± 0.36</td><td>78.61 ± 0.38</td><td>82.85 ± 0.37</td><td>85.10 ± 0.22</td><td>82.66 ± 0.60</td><td>86.96 ± 0.40</td><td>72.91 ± 1.07</td><td>76.03 ± 0.59</td></tr><tr><td rowspan="7">Obfuscated Proxy Drift</td><td>Shadowsocks</td><td>12.09 ± 2.32</td><td>14.91 ± 2.16</td><td>43.94 ± 0.99</td><td>44.09 ± 0.91</td><td>59.32 ± 2.07</td><td>61.98 ± 3.23</td><td>45.90 ± 1.59</td><td>45.64 ± 1.20</td><td>40.21 ± 1.95</td><td>50.34 ± 2.88</td><td>60.84 ± 1.45</td><td>63.01 ± 0.16</td></tr><tr><td>Trojan</td><td>13.02 ± 2.49</td><td>15.13 ± 1.95</td><td>45.26 ± 1.47</td><td>45.37 ± 0.97</td><td>63.27 ± 2.80</td><td>66.46 ± 2.56</td><td>46.77 ± 1.63</td><td>46.66 ± 1.46</td><td>42.07 ± 1.36</td><td>53.25 ± 2.49</td><td>64.47 ± 2.05</td><td>64.58 ± 0.03</td></tr><tr><td>VLESS-XTLS-Vision</td><td>18.48 ± 0.88</td><td>16.77 ± 0.54</td><td>41.33 ± 1.14</td><td>40.05 ± 0.69</td><td>48.30 ± 1.97</td><td>51.58 ± 1.99</td><td>35.94 ± 1.84</td><td>37.12 ± 0.55</td><td>29.33 ± 2.65</td><td>36.25 ± 3.16</td><td>46.89 ± 1.88</td><td>47.72 ± 0.54</td></tr><tr><td>VMess-TLS</td><td>15.32 ± 2.82</td><td>18.09 ± 2.10</td><td>48.90 ± 1.38</td><td>47.38 ± 1.37</td><td>64.33 ± 2.17</td><td>67.53 ± 22.9</td><td>45.16 ± 3.11</td><td>45.47 ± 0.88</td><td>45.44 ± 1.82</td><td>55.73 ± 2.13</td><td>63.91 ± 0.46</td><td>65.41 ± 1.32</td></tr><tr><td>VMess</td><td>25.03 ± 0.74</td><td>22.94 ± 2.04</td><td>57.68 ± 1.28</td><td>55.11 ± 0.66</td><td>72.02 ± 2.21</td><td>76.90 ± 2.63</td><td>47.76 ± 4.18</td><td>48.69 ± 1.52</td><td>41.46 ± 3.07</td><td>52.21 ± 3.11</td><td>65.34 ± 0.62</td><td>66.37 ± 1.23</td></tr><tr><td>VMess-WS-TLS</td><td>21.25 ± 0.94</td><td>20.32 ± 1.73</td><td>52.82 ± 1.64</td><td>51.70 ± 0.49</td><td>69.94 ± 2.13</td><td>75.99 ± 2.29</td><td>45.57 ± 3.73</td><td>45.71 ± 1.60</td><td>30.30 ± 5.81</td><td>34.85 ± 3.15</td><td>65.82 ± 0.51</td><td>67.89 ± 0.83</td></tr><tr><td>AVG</td><td>17.53 ± 1.34</td><td>18.03 ± 1.45</td><td>48.32 ± 0.77</td><td>47.28 ± 0.73</td><td>62.86 ± 2.12</td><td>66.74 ± 2.36</td><td>44.52 ± 2.34</td><td>44.88 ± 0.35</td><td>38.14 ± 1.81</td><td>47.10 ± 2.46</td><td>61.21 ± 1.04</td><td>62.50 ± 0.44</td></tr><tr><td rowspan="3">Browser Drift</td><td>Edge</td><td>10.23 ± 1.88</td><td>09.98 ± 1.09</td><td>07.66 ± 0.69</td><td>12.18 ± 0.42</td><td>27.08 ± 1.57</td><td>32.60 ± 0.41</td><td>09.18 ± 0.52</td><td>11.80 ± 0.85</td><td>26.16 ± 2.11</td><td>33.64 ± 0.98</td><td>12.80 ± 1.22</td><td>16.37 ± 2.28</td></tr><tr><td>Firefox</td><td>01.60 ± 0.26</td><td>02.15 ± 0.29</td><td>00.49 ± 0.10</td><td>01.13 ± 0.22</td><td>09.22 ± 0.64</td><td>13.07 ± 1.37</td><td>00.40 ± 0.23</td><td>00.30 ± 0.18</td><td>08.31 ± 0.68</td><td>09.27 ± 1.59</td><td>01.42 ± 0.45</td><td>02.63 ± 0.24</td></tr><tr><td>AVG</td><td>05.91 ± 0.87</td><td>06.06 ± 0.69</td><td>04.07 ± 0.32</td><td>06.66 ± 0.21</td><td>18.15 ± 1.04</td><td>22.83 ± 0.82</td><td>04.79 ± 0.30</td><td>06.05 ± 0.47</td><td>17.24 ± 1.20</td><td>21.45 ± 0.72</td><td>07.11 ± 0.51</td><td>09.50 ± 1.02</td></tr></table>

base-1 temporal base-1 spatial base-2 temporal

![](images/281968e61f2b3bc3cb67268c4dafcacc29b105fb4d24be5f0128ba713343c0bd.jpg)

<details>
<summary>line chart</summary>

| α    | Δ mean F1-score (%) |
| ---- | ------------------- |
| 0.0  | 0.0                 |
| 0.3  | -5.0                |
| 0.6  | 0.0                 |
| 0.9  | -15.0               |
</details>

![](images/5934a2e36625e542ae348c15b2ad5cabe66d83b75bf68133bfaba690148b392c.jpg)

<details>
<summary>line chart</summary>

| α    | DF (Line 1) | DF (Line 2) | DF (Line 3) |
| ---- | ----------- | ----------- | ----------- |
| 0.0  | 0           | 0           | 0           |
| 0.3  | 4           | 3           | 1           |
| 0.6  | 5           | 4           | 2           |
| 0.9  | 3           | 3           | 1           |
</details>

![](images/5ff6f237e142d3070a9807a073332fb5d1a7269c0e8460ff7fdbea0a0ca16ce9.jpg)

<details>
<summary>line chart</summary>

| α    | Blue Line | Green Dashed Line | Orange Solid Line |
| ---- | --------- | ----------------- | ----------------- |
| 0.0  | 0         | 0                 | 0                 |
| 0.3  | ~0.5      | ~0.8              | ~-0.2             |
| 0.6  | ~0.4      | ~0.7              | ~-0.1             |
| 0.9  | ~0.6      | ~0.6              | ~-0.1             |
</details>

![](images/48eb6cd2fb489a47a7661afbc937e243d845b82dd59188df00c07654b7dbb028.jpg)

<details>
<summary>line chart</summary>

| α    | Line 1 | Line 2 | Line 3 |
| ---- | ------ | ------ | ------ |
| 0.0  | 0.0    | 0.0    | 0.0    |
| 0.3  | 4.0    | 3.5    | 2.0    |
| 0.6  | 3.5    | 4.0    | 2.5    |
| 0.9  | 2.0    | 3.0    | 1.5    |
</details>

![](images/ad90913232cb1a8223ff326e8fe3607611e7a13acf8a41fc2bbde477e0dcb3be.jpg)

<details>
<summary>line chart</summary>

| α    | Series 1 | Series 2 | Series 3 |
| ---- | -------- | -------- | -------- |
| 0.0  | 0.0      | 0.0      | 0.0      |
| 0.3  | 8.0      | 4.0      | 3.0      |
| 0.6  | 9.0      | 4.5      | 3.5      |
| 0.9  | 6.0      | 3.0      | 2.0      |
</details>

![](images/8c4adf8d12b5c253e3b1d6fd8309c4da017194f4bcfabfdb9a003a5666c314c4.jpg)

<details>
<summary>line chart</summary>

| α    | CountMamba |
| ---- | ---------- |
| 0.0  | 0          |
| 0.3  | 1          |
| 0.6  | 2          |
| 0.9  | 1          |
</details>

Figure 9: Performance gain Δ (%) over the $\alpha = 0$ baseline as a function of distillation weight ?? for six backbones. The bestperforming ?? range remains largely stable for each backbone, indicating that the distillation weight is mainly coupled to student capacity rather than to a particular source training window.

## F Sensitivity Analysis of ??

This appendix provides the complete sensitivity analysis of the distillation weight ??. Our goal is to understand how strongly resourceprivileged supervision should be injected into the traffic-only student, and whether this choice is tied to a particular target environment or instead reflects an intrinsic property of the student backbone.

In the joint objective

$$
\mathcal {L} _ {t o t a l} = (1 - \alpha) \mathcal {L} _ {c l s} + \alpha \mathcal {L} _ {k d}, \tag {7}
$$

the weight ?? ∈ [0, 1] controls how much optimization pressure is assigned to the resource-induced inter-class topology, relative to hard-label discrimination. When ?? is too small, the student receives little structural supervision from the resource teacher and largely degenerates to ordinary traffic-only ERM. When ?? is too large, the student may be forced to fit soft topological constraints that exceed the representational capacity of its traffic-side feature space.

To characterize this trade-off, we perform a full ?? scan over all six student backbones under temporal drift from two independent training datasets. We additionally verify the same trend under spatial drift from the source training dataset. Figure 9 reports the temporaldrift scan and shows that the best single ?? may shift slightly across training and testing datasets, but each backbone exhibits a stable best-performing range. This range is primarily governed by student capacity rather than the specific training window. DF, Tik-Tok, and RF benefit most from moderate distillation weights, whereas Var-CNN and CountMamba benefit from medium-to-high distillation weights; AWF is the most sensitive and can degrade when the distillation term dominates.

This pattern indicates that ?? should be interpreted as a capacitymatching parameter on the student side. The resource teacher’s inter-class topology must ultimately be compressed into a trafficonly representation space. A higher-capacity student can absorb this structural prior while preserving hard-label decision boundaries; a lower-capacity student has a smaller representation budget and is more prone to objective interference between $\mathcal { L } _ { c l s }$ and $\mathcal { L } _ { k d }$ .

Table 9: Capacity scaling analysis for Var-CNN under 150-day temporal drift. The best ?? range denotes distillation weights that remain close to the best result for each width and outperform the ?? = 0 baseline.

<table><tr><td>Var-CNN Width</td><td>α = 0</td><td>Best α Range</td><td>F1 in Best Range</td><td>Max Gain</td></tr><tr><td>1×</td><td>72.77</td><td>0.1–0.7</td><td>80.25–82.22</td><td>+9.45 pp</td></tr><tr><td>0.5×</td><td>74.36</td><td>0.1–0.6</td><td>80.31–80.94</td><td>+6.58 pp</td></tr><tr><td>0.25×</td><td>72.18</td><td>0.2–0.4</td><td>76.82–78.35</td><td>+6.17 pp</td></tr><tr><td>0.125×</td><td>70.35</td><td>0.1–0.3</td><td>73.14–74.95</td><td>+4.60 pp</td></tr></table>

Var-CNN Capacity Scaling. To further isolate the effect of model capacity, we keep the residual topology of Var-CNN fixed and scale only the channel width. We then repeat the ?? scan under 150-day temporal drift. This controlled experiment removes architectural differences and concentrates the comparison on student capacity itself. Table 9 summarizes the best ?? range for each width, where the best range denotes weights that remain close to the capacityspecific optimum and clearly outperform the ?? = 0 baseline.

Table 9 shows that capacity controls both the ceiling of distillation gains and the best-performing range of ??. The full-width Var-CNN has the widest best range: for $\alpha = 0 . 1 \mathrm { - } 0 . 7 ,$ it maintains 80.25%–82.22% macro-F1 and reaches a maximum gain of 9.45 percentage points. Reducing the width to 0.5× still preserves a broad best range of $\alpha = 0 . 1 \ – 0 . 6 ,$ but the maximum gain drops to 6.58 percentage points. Further reducing the width to 0.25× and 0.125× narrows the best ranges to 0.2–0.4 and 0.1–0.3, respectively, while the maximum gains decrease to 6.17 and 4.60 percentage points. Under the same teacher, training data, and residual topology, smaller students therefore convert less privileged resource supervision into peak robustness gains and exhibit narrower near-optimal ?? ranges.

This result does not imply that low-capacity students cannot benefit from resource supervision. Rather, they can absorb only a limited strength of teacher topology. For high-capacity students, the KD term mainly acts as a structural regularizer that reshapes decision boundaries without overwhelming hard-label discrimination. For low-capacity students, an overly large ?? allocates too much of the representation budget to matching the teacher distribution, turning the KD term from useful regularization into an optimization constraint beyond the student’s capacity.

Takeaways. The distillation weight ?? should be viewed as the strength of resource-privileged supervision matched to student capacity. Architectural differences affect the exact optimum, but the underlying mechanism is whether the student has sufficient representation budget to internalize the resource teacher’s inter-class topology. In practice, we tune ?? once per backbone on the sourcedomain validation set and keep it fixed across all target environments; the reported robustness gains do not rely on target-domain retuning. This analysis also clarifies the applicability boundary of ResAware: when the student has adequate capacity and the correspondence between resource structure and traffic observations remains stable, moderate or large ?? can substantially improve crossenvironment generalization; when student capacity is limited, ?? should be reduced to avoid over-distillation; when drift disrupts the cross-modal correspondence itself, ?? should be further reduced or the model should fall back to traffic-only training.
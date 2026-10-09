# TIPSO-GAN: Malicious Network Traffic Detection Using a Novel Optimized Generative Adversarial Network

Ernest Akpaku<sup>†∗</sup>, Jinfu Chen<sup>†∗</sup>, Joshua Ofoeda<sup>‡</sup>

<sup>†</sup>School of Computer Science and Communication Engineering, Jiangsu University

Jiangsu Key Laboratory of Security Technology for Industrial Cyberspace,

301 Xuefu Road, Zhenjiang 212013, Jiangsu, China

<sup>‡</sup>Department of Information Technology, University of Professional Studies, Accra, Ghana

ernestakpaku1@gmail.com, jinfuchen@ujs.edu.cn, joshua.ofoeda@upsamail.edu.gh

Abstract—Detecting advanced cyber threats, particularly zeroday vulnerabilities, poses significant challenges in network security. This paper presents TIPSO-GAN, an optimized Generative Adversarial Network (GAN) for detecting malicious traffic. TIPSO-GAN addresses common GAN-based intrusion detection system (IDS) issues, such as training instability and mode collapse, by framing GAN training as a swarm optimization problem, harnessing collective intelligence for complex optimization. To enhance Particle Swarm Optimization (PSO), TIPSO-GAN employs three strategies: (1) adaptive inertia weights for a balance of exploration and exploitation, (2) a diversity preservation strategy to prevent premature convergence, and (3) a feedback loop to reinitialize stagnant particles. TIPSO-GAN integrates transfer learning with a Temporal-Decaying Multi-Head Self-Attention mechanism to prioritize recent features, aiding in unseen malicious traffic detection. A combination of reconstruction loss and focal loss in the objective function further ensures realistic normal samples while focusing on challenging malicious samples. Across CIC-IDS2018, CICAPT-IIoT2024, and CIC-DDoS2019, TIPSO-GAN achieves 99.1±0.1, 98.9±0.1, and 98.7±0.1 F1, outperforming the strongest baseline by 0.2–1.0 F1 and exceeding transformer IDS models. On CICAPT-IIoT2024, it reaches 0.999±0.002 macro PR-AUC, ahead of the next best method (0.960±0.005). Under strict zero-day evaluations, TIPSO-GAN attains 92.3 F1 in LOFO tests and 79–83 F1 in cross-dataset experiments while maintaining recall above 0.80. Despite PSO-enhanced training, TIPSO-GAN maintains 0.42 ms latency, ∼2400 flows/s throughput, and a 2.1 GB footprint, with stable performance up to 10<sup>8</sup> flows. Our code is accessible at https://doi.org/10.5281/zenodo.17759516.

## I. INTRODUCTION

The adoption of internet-based technologies such as cloud computing, information systems, web servers, and IoTs has proliferated in recent years. This heightened reliance on technology in our daily routines has rendered us more susceptible to unknown cyberattacks. Identifying previously unknown vulnerabilities in networks is challenging as they lack established signatures and exhibit novel behaviours not yet recognized by traditional security systems [1]. Widely used deep learning methods such as LSTM, CNN, DNN, and RNN traffic identification methods are broadly trained with labelled traffic data. This limits their ability to learn general features from unlabelled data. As such, they still suffer from low accuracy, particularly when challenged with unknown malicious traffic samples [2]. Recent transformer-based architectures, such as FlowTransformer [3], FT-Transformer [4], MalDetectFormer [5], and TransTraffic [6], have shown strong performance in modeling long-range dependencies in network flows. However, these methods are primarily optimized for static accuracy and rely on large labeled datasets. Generative adversarial networks (GANs) developed by Goodfellow et al. [7] have proven effective for creating models that can mimic previously unknown behaviours in real-world situations [8] [9]. GAN is made up of a generator which is a neural network that generates new data samples from a random noise input; and a discriminator that aims to distinguish between real data samples and the fake samples produced by the generator. The two networks are trained simultaneously using the MiniMax objective function which is based on the principles of the game theory. Compared with other existing generative models, GANs provide a concise and efficient framework for learning generative models.

Although GANs have been successful in image generation and manipulation [10], game development, text-to-image generation, medical imaging, and many other tasks [11], they suffer from mode collapse resulting in training instability. The training aims to reach a Nash equilibrium where neither the generator nor the discriminator can improve their strategy given the other’s strategy. However, finding this equilibrium in practice is challenging due to the non-convex and highdimensional optimization landscape, leading to unstable training and mode collapse [12]. Optimizing the network’s weights to minimize the loss function is challenging due to the nonconvex nature of the loss landscape in GANs. This makes it difficult to find the optimal set of weights that results in highquality, diverse generated samples.

Many recent efforts on GANs have focused on overcoming these optimization difficulties by developing various adversarial training objectives [13]. The gradients of the objective function of the network parameters guide the training. However, training GANs with the original Jensen–Shannon divergence (JSD) leads to vanishing gradients leading to unstable training dynamics [14]. To address these issues, researchers have introduced alternative adversarial training objectives such as the least squares [15], absolute deviation, energy-based, spectral normalization [14], Kullback–Leibler (KL) divergence [16], Wasserstein Distance, and the Wasserstein Distance with a penalty term [17]. However, these objectives have not fully addressed the training and mode collapse challenges completely.

In this study, we propose a novel GAN framework named TIPSO-GAN, leveraging the improved architectural design of GAN and enhanced Particle Swarm Optimization (PSO) to enhance the training dynamics. Unlike conventional GANs that engage in fixed adversarial competition, our PSO-optimized GAN harnesses the collective intelligence of a swarm to navigate the complex optimization landscape. By treating the generator’s parameters as particles within the swarm, we evolve the generator through iterative updates guided by both individual and social experiences within the swarm, effectively transforming the adversarial training into a PSOdriven optimization challenge. In our implementation, we note that the fast convergence speed of PSO can quickly lead GANs to find a good set of parameters, which can result in stable and efficient training, especially in the initial phases of training. However, this speed could limit the algorithm from exploring the entire solution space sufficiently, which could be crucial for GANs that require a thorough search to avoid getting stuck in suboptimal configurations. Also, despite its global search capability, the standard PSO might not be as effective in finetuning the parameters near the end of the optimization process, potentially leaving room for improvement in the generator’s performance.

Linearly decreasing the inertia weight and improving the weight factor have been proposed to address these problems in clustering algorithms. However, it may not be suitable for complex problems where the optimization surface has many local optima or varying degrees of ruggedness. Also, it uses a fixed predetermined schedule for reducing inertia weights which lacks flexibility to adapt to different stages of the optimization process or diverse problem landscapes. For example, in a linearly decreasing inertia weight schedule, the inertia weight starts at an initial value and decreases uniformly to a final value by the end of the optimization process. To address these challenges, we enhanced the standard PSO algorithm to incorporate adaptive inertia weights, diversity preservation strategies, and a feedback loop mechanism that encourages exploration in the later stages of optimization. These modifications ensure PSO-driven GAN optimization to avoid local optima and achieve more robust and diverse generator parameters.

In this paper, several novel strategies are proposed to address the challenges discussed for better malicious network traffic detection. First, an adaptive Sigmoidal inertia weight adjustment strategy is introduced into the PSO algorithm and compared with the popular linearly decreasing approach, and others. The best performing is used to effectively explore GAN’s parameter search space to find an optimal solution. Second, the traditional GAN is modified through novel architectural design a new loss reconstruction function, and PSO-based training. Last, a pretraining model named DeePred is introduced and applied to improve the performance of an unknown malicious traffic detector. Leveraging, on the strengths of the proposed methods, this study makes the following contributions:

1) We propose TIPSO-GAN, a framework that frames GAN training as a swarm optimization problem, leveraging an enhanced PSO algorithm in a two-staged adversarial training. We introduce adaptive inertia weights, a diversity preservation mechanism, and reinitialization of stagnant particles to enhance the PSO to dynamically balance exploration and exploitation, prevent premature convergence, and avoid stagnation in the optimization process, thereby enhancing the training stability and convergence of TIPSO-GAN. These enhancements ensure better exploration and exploitation of the search space during training, enabling better convergence speed, more stable training, and effective mitigation of mode collapse.

2) A novel reconstruction loss function and a pre-training network DeePred, are introduced to improve the adversarial traffic generation ability of the generator and the detection ability of the discriminator in TIPSO-GAN. DeePred is integrated with a novel Multihead Self Attention Mechanism (MHSA) that utilizes a temporal decaying parameter to provide larger weights to features that are more recent and are indicative of malicious behaviour. A focal loss is introduced into the discriminator to address class imbalance by focusing on hardto-classify malicious samples.

3) Extensive experiments on three datasets demonstrate that TIPSO-GAN outperforms conventional GAN and its variants, state-of-the-art GAN-based-IDS variants and four other existing deep learning IDS models in terms of accuracy, precision, recall, and F1-score. TIPSO-GAN also exhibits improved training stability and resistance to mode collapse and class imbalance, making it highly suitable for real-world network intrusion detection systems.

The remaining sections of the study are organized as follows: Section II discusses related studies. Section III presents detailed descriptions of the proposed method. In Sections V and VI, we describe the experimental setup and evaluation, and results respectfully. The conclusion and future research are discussed in section VII.

## II. RELATED STUDIES

## A. Generative Adversarial Networks in Cybersecurity

In recent years, GANs have been implemented for network security, particularly for the detection of malicious traffic. The ability of GANs to generate realistic synthetic data has been leveraged to enhance the performance of intrusion detection systems (IDS) by simulating a wide range of potential attacks [13]. One of the pioneering works in this area is the paper by Das [18], which demonstrates the application of GANs in reproducing both categorical and continuous synthetic network traffic features. Building upon this foundation, researchers have explored the integration of GANs with deep neural networks for more effective anomaly detection in network traffic. The work by Liu and Liu [19] presents a federated learning approach using GANs, which allows for localized training and centralized model updates, addressing concerns of privacy and model tampering in large-scale networks. Further advancements have been made in the detection of adversarial traffic flows by employing GAN-based attack algorithms like NIDSGAN [20], which develops a GAN-based attack algorithm capable of generating highly realistic adversarial traffic flows that can evade machine learning-based NIDS. Recent work has also explored conditional GANs for generating specific attack types and advanced architectures for improving synthetic traffic quality.

However, these approaches predominantly focus on generating synthetic data to augment training datasets rather than directly addressing the challenge of detecting previously unseen attack patterns. For instance, Das [18] generates synthetic network flows but requires pre-existing attack labels, while NIDSGAN [20] creates adversarial examples primarily for testing existing detectors rather than improving zero-day detection capabilities. Moreover, existing GAN-based IDS methods struggle with the unique characteristics of network traffic data. Unlike image generation where GANs excel, network traffic exhibits complex temporal correlations, multi-modal feature distributions, and extreme class imbalance between normal and malicious samples. Liu and Liu [19] reported that their federated GAN approach achieved only 78% detection accuracy on unknown attack variants, significantly lower than performance on known attacks. Similarly, recent studies show that conventional GAN architectures fail to preserve the statistical properties of network protocols when generating synthetic traffic, leading to unrealistic packet sequences that can be easily distinguished by modern firewalls. Despite these promising initial results, current GAN applications in network security remain limited by training instability and inability to generalize beyond their training distributions, constraining their effectiveness in dynamic threat environments.

## B. GAN Training Optimization and Stability

As noted in [21], GANs are known to suffer from training instability, which can lead to issues such as mode collapse and training oscillations. These challenges can affect the quality and diversity of the generated samples, which are crucial for accurately simulating and detecting a wide range of network attacks. Another limitation highlighted in the literature is the complexity of the generator network in GANs [13]. When the generator’s probability distribution is highly complex, it becomes difficult to estimate the maximum likelihood [22].

GANs address this by using neural networks to define the probability distribution [23], which introduces its own set of challenges, such as the need for careful architecture design and tuning to ensure that the generated data accurately represents the underlying distribution of normal network traffic. DCGAN [24] introduced architectural constraints that improved the stability of GAN training by replacing pooling layers with strided convolutions and fully connected layers with global average pooling in the discriminator to reduce checkerboard artifacts and simplify the architecture. However, these modifications did not eliminate the issues of training instability and mode collapse. Subsequent research focused on reconstructing the loss function to address these training problems. The Wasserstein GAN (WGAN) [14] introduced a new loss function based on the Wasserstein distance, which provides a more stable training objective. An extended WGAN called WGAN-GP [17] added a gradient penalty term to the loss function, though this introduced additional computational overhead. The LSGAN [15] proposed using least squares loss, but suffered from slower convergence rates on complex datasets. Beyond loss function modifications, advanced architectural innovations have attempted to address training instability. Techniques such as spectral normalization and progressive training have shown improvements in specific domains, yet these methods primarily target image generation tasks. When applied to network traffic data, these stabilization techniques show limited effectiveness due to the high-dimensional, non-stationary nature of network features. Recent empirical studies report that even with these advanced techniques, GANs applied to cybersecurity datasets still experience mode collapse rates of 20-35%, particularly when attempting to generate minority class samples representing sophisticated attacks [13]. The fundamental challenge remains that existing stabilization methods rely on assumptions about data structure and training dynamics that do not hold for the adversarial, multi-modal distributions characteristic of network security data.

## C. Swarm Intelligence for Neural Network Optimization

In recent times, swarm intelligence algorithms [25] such as PSOs [26] have achieved considerable success across a wide range of computational tasks, including modelling, optimization, and design of GANs [27]. PSO operates by maintaining a population of particles, each representing a potential solution in the search space, where particles update their velocities and positions based on their personal best experiences and the global best solution found by the swarm. This populationbased approach enables PSO to explore multiple regions of the search space simultaneously, making it particularly effective for complex optimization problems with multiple local optima. Recent applications of PSO in neural network optimization have demonstrated its effectiveness in avoiding local minima through population-based search strategies [28]. Unlike gradient-based methods that rely on local derivative information, PSO maintains diversity through swarm dynamics and can escape suboptimal regions by leveraging collective intelligence. In the context of GAN training, PSO offers theoretical advantages over traditional Adam or SGD optimizers by treating the generator parameters as particle positions in the high-dimensional parameter space, enabling global search capabilities that are particularly valuable given the non-convex, multi-modal nature of GAN loss landscapes [29]. However, conventional PSO suffers from premature convergence and insufficient exploration in high-dimensional parameter spaces typical of GAN architectures. The standard PSO algorithm can become trapped in local optima when the swarm loses diversity, particularly in complex optimization landscapes with numerous suboptimal peaks. Variants such as linearly decreasing inertia weight PSO [28] have been proposed to balance exploration and exploitation phases by gradually reducing the influence of previous velocities over time. However, this linear scheduling approach lacks the flexibility to adapt to different stages of the optimization process or diverse problem landscapes, making it less effective in complex problem scenarios where the optimization surface has many local optima or varying degrees of ruggedness. The challenge becomes particularly acute in GAN optimization, where the objective function changes continuously due to the adversarial game between generator and discriminator. The fitness landscape exhibits non-stationarity as discriminator updates alter the generator’s optimization surface, requiring PSO variants that can dynamically adjust exploration-exploitation balance based on real-time feedback. Traditional PSO parameters such as fixed inertia weights and acceleration coefficients prove inadequate in this environment, as they cannot respond to the evolving loss topology that characterizes adversarial training dynamics [28]. These problems could critically compromise PSO’s efficacy in high-dimensional, non-convex optimization problems characterized by extensive local minima networks, thereby potentially leading to suboptimal convergence trajectories and diminished algorithmic convergence velocities [30].

## D. Novelty of this study

As summarized in Table I, although numerous GAN-based intrusion detection approaches exist, they seldom address key challenges comprehensively. Despite recent advances [31], [32], most still suffer from training instability and high mode collapse when applied to heterogeneous network traffic data. Stabilization techniques such as spectral normalization and progressive training, designed for vision tasks, remain ineffective for sparse cybersecurity datasets. Furthermore, the use of PSO in GANs for intrusion detection is largely unexplored. While PSO-GAN has shown promise in other domains [33], [34], limited works [35] lack adaptive inertia weighting and diversity-preserving mechanisms essential for robust adversarial learning. We also note that transformer-based IDS models (TranAD, TransfficFormer, FlowTransformer) improve stability but do not incorporate PSO-guided GAN training or zeroday–oriented transfer learning.

Another gap is the absence of transfer learning. Existing GAN-based IDSs are typically trained from scratch, neglecting pre-trained models that enhance convergence and generalization. Although hybrid approaches such as [36] employ zeroshot learning, they fail to integrate transfer learning for both data synthesis and knowledge reuse. Few studies unify known and evolving attack detection in a coordinated framework; even recent multi-level or hybrid models [36], [37] omit PSO optimization and transfer learning within a single training pipeline.

TABLE I: Selected Related Studies. Training Stability (TS), Mode Collapse (MC), Class Imbalance (CI), Zero-Day Detection (ZD)

<table><tr><td>Study</td><td>Year</td><td>Method</td><td>TS</td><td>MC</td><td>CI</td><td>ZD</td><td>TL</td><td>PSO</td><td>MPT</td></tr><tr><td>Das [18]</td><td>2022</td><td>FGAN</td><td>X</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Zolbayar et al. [20]</td><td>2022</td><td>NIDSGAN</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Nguyen et al. [31]</td><td>2023</td><td>GAN-SCADA</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Seo et al. [38]</td><td>2019</td><td>GIDS</td><td>√</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Rahman et al. [39]</td><td>2024</td><td>SYN-GAN</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Aldhaheri &amp; Alhuzali [40]</td><td>2023</td><td>SGAN-IDS</td><td>X</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Torres et al. [32]</td><td>2023</td><td>GAN-AE</td><td>√</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Poongodi &amp; Hamdi [37]</td><td>2023</td><td>Multi-GAN-IoV</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>√</td></tr><tr><td>Mari et al. [41]</td><td>2023</td><td>GAN-Adversarial</td><td>√</td><td>X</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Zhang &amp; Zhao [33]</td><td>2021</td><td>PSO-GAN</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>√</td><td>X</td></tr><tr><td>Liu et al. [34]</td><td>2022</td><td>Parameterized PSO-GAN</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>√</td><td>X</td></tr><tr><td>Sundaram et al. [35]</td><td>2023</td><td>PSO-GRU-GAN-5G</td><td>√</td><td>√</td><td>√</td><td>√</td><td>X</td><td>√</td><td>X</td></tr><tr><td>Roopak et al. [42]</td><td>2024</td><td>Unsupervised Ensemble</td><td>√</td><td>X</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Sarhan et al. [43]</td><td>2023</td><td>Zero-Shot ML</td><td>X</td><td>X</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Touré et al. [36]</td><td>2024</td><td>Hybrid Learning</td><td>√</td><td>X</td><td>√</td><td>√</td><td>X</td><td>X</td><td>√</td></tr><tr><td>Huang et al. [44]</td><td>2021</td><td>T-GAN</td><td>√</td><td>X</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Tuli et al. [45]</td><td>2022</td><td>TranAD (Transformer)</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Du et al. [46]</td><td>2025</td><td>TransfficFormer</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td><td>X</td></tr><tr><td>Manocchio et al. [3]</td><td>2024</td><td>FlowTransformer</td><td>√</td><td>√</td><td>√</td><td>√</td><td>X</td><td>X</td><td>X</td></tr><tr><td>TIPSO-GAN (Proposed)</td><td>2025</td><td>Enhanced PSO-GAN</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

## III. PROPOSED METHOD

## A. The TIPSO-GAN Framework

To detect unknown network attacks with high accuracy, we propose a two-stage adversarial-based intrusion detection model named TIPSO-GAN, as illustrated in Figure 1. The core of the framework is TIPSO-GAN, which combines the benefits of PSOGAN and the pre-training model (DeePred) to enhance the detection of both known and unknown attacks. In this framework, the discriminator of PSOGAN and the pretraining model DeePred are crucial for transferring knowledge to the final TIPSO-GAN. The Generator $G _ { T }$ in TIPSO-GAN is initialized by transferring the structure and parameters from the Generator G of PSOGAN. PSOGAN is trained exclusively on normal traffic data. During training, the generator G learns to produce modelled samples that approximate the normal traffic distribution. Once the PSOGAN has completed its training, its discriminator D is discarded, and the trained generator G is transferred to initialize the Generator $G _ { T }$ in TIPSO-GAN. This ensures that the Generator $G _ { T }$ starts with a good understanding of normal traffic, enabling it to generate more accurate representations of normal traffic during training.

To strengthen the detection capability of the Discriminator $D _ { T }$ in TIPSO-GAN, we transfer the structure and parameters of the pre-training model DeePred into Discriminator $D _ { T }$ . The DeePred model has a structure similar to the discriminator in PSOGAN but is trained using a dataset containing both normal and known malicious traffic. This gives DeePred the ability to effectively distinguish between normal and malicious samples (i.e., 2-class classification). By transferring the trained parameters from DeePred, the Discriminator $D _ { T }$ of TIPSO-GAN inherits a robust classification capability, enhancing its ability to detect unknown malicious traffic. After the initial transfer, TIPSO-GAN undergoes unsupervised training, using

![](images/aee2c6a08dee99f004ced3ccb801d49a1a9f542a9301273fd385daf4d24fe540.jpg)  
Fig. 1: Detection roadmap of TIPSO-GAN.

Note. N: Normal traffic, M: Known Malicious traffic, UM: Unknown Malicious traffic.

```txt
Algorithm 1 Algorithm of the Proposed TIPSO-GAN Model
1: Initialize: DN: normal traffic; DE: train set; VE: val set; TB: test set; B: batch size; Epochs
2: G: generator trained from PSOGAN using DN
3: DeePred: discriminator pre-trained with DE, VE
4: Initialize GT ← G, DT ← DeePred
5: Training:
6: for each epoch in Epochs do
7: Generate fake samples with GT (size B)
8: Sample real flows from DN (size B)
9: Train discriminator DT on both batches
10: if validation accuracy drops for n=3 rounds then
11: Output DT from round n+1 and break
12: else if accuracy on normal < T then
13: Output DT from round n-1 and break
14: end if
15: Train generator GT
16: end for
17: Output: final discriminator DT as classifier C
```

a dataset consisting only of normal traffic samples. The goal is for the Generator $G _ { T }$ to continue learning the normal traffic distribution while the Discriminator $D _ { T }$ refines its ability to identify traffic samples that deviate from the normal (i.e., potential unknown attacks). A validation set containing both normal and unknown malicious samples is used to monitor the performance of TIPSO-GAN during training. The adversarial game between the generator and discriminator continues until the detection accuracy of normal traffic reaches a certain threshold or the overall accuracy starts to decline. Once training is complete, the Discriminator $D _ { T }$ of TIPSO-GAN is output as the final anomaly detector.

## B. Modified PSO for GAN Optimization

We propose an improved PSO variant that integrates an adaptive inertia weight and a diversity preservation mechanism. Our enhanced PSO algorithm introduces an adaptive inertia weight w that dynamically adjusts based on the swarm’s performance. Unlike traditional PSO algorithms that use a fixed or linearly decreasing inertia weight, our method adapts the inertia weight non-linearly based on real-time feedback, providing greater flexibility in balancing exploration and exploitation. In the early stages of optimization, a higher inertia weight is used to facilitate global exploration, enabling particles to traverse the search space extensively. As the algorithm progresses, the inertia weight decreases, honing the particles search towards local refinement and convergence to optimal solutions. Algorithm 2 shows the working principle of the proposed PSO. The adaptive inertia weight is updated using a non-linear function, governed by a sigmoid function, to provide rapid adaptation when significant improvements are detected and a gradual approach when progress plateaus. The inertia weight w(t) at iteration t is calculated as:

$$
w (t) = w _ {\min} + \left(w _ {\max} - w _ {\min}\right) \times \frac {1}{1 + e ^ {- k (\Delta f (t) - f _ {\text { threshold }})}}\tag{1}
$$

where: $w _ { \mathrm { m a x } }$ and $w _ { \mathrm { m i n } }$ are the maximum and minimum inertia weights, respectively. $\Delta f ( t )$ represents the change in the global best fitness over a certain number of iterations, defined as $\Delta f ( t ) = f _ { \mathrm { b e s t } } ( t ) - f _ { \mathrm { b e s t } } ( t - \Delta t )$ . f<sub>threshold</sub> is a predefined fitness improvement threshold. k is a scaling factor controlling the steepness of the sigmoid function. ∆t is the number of iterations over which the fitness change is measured.

## C. Improved particle diversity

Complementing the adaptive inertia weight, the diversity preservation mechanism is designed to prevent premature convergence, a common pitfall in PSO where particles cluster around sub-optimal solutions. This mechanism sets our approach apart from existing PSO variants by actively maintaining swarm diversity through multiple strategies not commonly combined in standard algorithms. It maintains diversity within the swarm through three strategies:

a) Fitness Sharing: Particles in densely populated regions are penalized to encourage exploration of less-visited areas. Unlike traditional PSO, which treats particle fitness independently, our method adjusts fitness values based on particle proximity, promoting a more diverse search. The shared fitness $\hat { f } _ { i }$ for particle i is calculated as:

$$
\hat {f} _ {i} = \frac {f _ {i}}{\sum_ {j = 1} ^ {N} \mathrm{sh} (d _ {i j})}\tag{2}
$$

where $f _ { i }$ is the original fitness of particle i. N is the number of particles. sh $( d _ { i j } )$ is the sharing function based on the distance $d _ { i j }$ between particles i and $j ,$ defined as:

$$
\operatorname{sh} (d _ {i j}) = \left\{ \begin{array}{l l} 1 - \left(\frac {d _ {i j}}{\sigma_ {\text { share }}}\right) ^ {\alpha} & \text { if } d _ {i j} <   \sigma_ {\text { share }} \\ 0 & \text { otherwise } \end{array} \right.\tag{3}
$$

$\sigma _ { \mathrm { s h a r e } }$ is the sharing radius. α controls the shape of the sharing function. Re-initialization of Stagnant Particles: Particles that have not improved their personal best over a set number of iterations $T _ { \mathrm { s t a g n a n t } }$ are re-initialised to reintroduce variability. This differs from standard PSO, where particles may remain stagnant without mechanisms to reintroduce diversity. The reinitialisation is performed as:

$$
\begin{array}{l} \text {   If   } t - t _ {\text { last\_improve }} \geq T _ {\text { stagnant }}, \\ \text {   then   } x _ {i} (t) = x _ {\min} + \operatorname{rand} () \times (x _ {\max} - x _ {\min}) \end{array}\tag{4}
$$

here, $t _ { \mathrm { l a s t \_ i m p r o v e } }$ is the iteration when particle i last improved its personal best. $x _ { \mathrm { m a x } }$ and $x _ { \mathrm { m i n } }$ define the bounds of the search space. rand() generates a random vector with components uniformly distributed in [0, 1].

b) Randomness in Velocity Update: Introducing a random component to the velocity update equation adds stochasticity, helping particles escape local optima. Traditional PSO typically lacks this random perturbation, and its inclusion in our method enhances the ability to explore the search space more thoroughly. The modified velocity update equation is:

$$
\begin{array}{c} v _ {i} (t + 1) = w (t) \cdot v _ {i} (t) + c _ {1} \cdot r _ {1} (t) \cdot [ p _ {i} (t) - x _ {i} (t) ] \\ \qquad + c _ {2} \cdot r _ {2} (t) \cdot [ g (t) - x _ {i} (t) ] \\ \qquad + \beta \cdot \texttt {r a n d n ()} \end{array}\tag{5}
$$

where $v _ { i } ( t + 1 )$ is the updated velocity of particle i at iteration $t + 1 . \ w ( t )$ is the adaptive inertia weight at iteration $t . ~ c _ { 1 }$ and $c _ { 2 }$ are cognitive and social acceleration coefficients. $r _ { 1 } ( t )$ and $r _ { 2 } ( t )$ are random numbers uniformly distributed in $[ 0 , 1 ]$ $p _ { i } ( t )$ is the personal best position of particle i. $x _ { i } ( t )$ is the current position of particle i. g(t) is the global best position found by the swarm. $\beta$ is a small constant controlling the magnitude of the random perturbation. randn() generates a random vector with components normally distributed with mean 0 and variance 1. The synergy of the adaptive inertia weight and the diversity preservation mechanism equips the improved PSO algorithm with enhanced flexibility and robustness. It dynamically adjusts to the demands of the optimization process, balancing the need for broad exploration with finegrained exploitation.

## D. Pre-trained Model (DeePred) construction

DeePred, which is a binary classifier based on CNN is introduced to improve the performance of the discriminator in TIPSO-GAN to detect zero-day malicious network traffic. The DeePred pre-training stage provides initialization using known malicious samples to stabilize discriminator learning but does not constrain detection to those patterns. TIPSO-GAN’s zero-day capability arises from its unsupervised finetuning on normal traffic, where deviations from the learned distribution are flagged as anomalies. The key features and parameters of DeePred are shown in Figure 4b. It is integrated with a novel Multihead Self-Attention Mechanism (MHSA) based on a temporal decaying parameter to provide larger weights for features that are more recent and indicative of malicious behaviour. The first convolutional layer transforms the input into a feature map, followed by a Leaky ReLU activation function to maintain non-linearity. The second and third convolutional layers continue to downsample the input into progressively smaller but deeper feature maps, ensuring that the model captures increasingly abstract patterns in the traffic flow. After the convolutional layers, we introduce the MHSA mechanism. Unlike the traditional attention mechanism, we introduce a temporal decay factor that diminishes the influence of tokens based on their relative positions in the sequence. The decay factor $\gamma _ { t }$ is then applied to the attention scores in formula 6.

![](images/a38996a02658bb5146644262237e1919299b7105f76a45f3b811120a1d047cc8.jpg)  
Fig. 2: Structure of the Multihead Self Attention Mechanism

$$
\gamma_ {t} = \exp (- \lambda | t - i |)\tag{6}
$$

Where λ is a decay rate hyperparameter that controls how quickly the attention fades over time. t is the current token’s position. i is the position of the token in the sequence. The decay factor $\gamma _ { t }$ exponentially decreases as the distance between token positions increases, thereby lowering the attention score of distant tokens. For attention computation, $\gamma _ { t }$ integrated into the attention logits before applying the softmax. This modification ensures that as the distance between tokens increases, the corresponding attention scores are reduced exponentially, making the model focus more on recent tokens. During computation, each head has its decay factor as

$$
(Q, K, V) = \operatorname{Concat} \left(\operatorname{head} _ {1}, \operatorname{head} _ {2}, \dots , \operatorname{head} _ {h}\right) W ^ {O}\tag{7}
$$

Therefore, the MHSA introduced into DeePred is given by:

$$
\operatorname{head} _ {i} = \operatorname{softmax} \left(\frac {Q _ {i} K _ {i} ^ {\top}}{\sqrt {d _ {k}}} \odot \Gamma_ {i}\right) V _ {i}\tag{8}
$$

where h is the number of heads and each $\Gamma _ { i }$ is the decay matrix specific to that head. Following the MHSA layer, the feature maps are flattened and passed through a fully connected layer for classification. Once trained, the model is transferred to the TIPSO-GAN framework to serve as the initial discriminator, where it is further fine-tuned to handle more complex and evolving network threats. The full structure of the MHSA is shown in Fig. 2.

## E. Improved Design of the GAN Structure

In the proposed TIPSO-GAN framework, we introduce a dynamic loss function to mitigate issues such as mode collapse and training instability. This dynamic loss function,

$L _ { \mathrm { d y n a m i c } } ( \theta )$ , is constructed by combining three key components: the adversarial loss $L ( G , D ) ( \theta )$ , divergence $D ( \theta )$ , and stability score S(θ). Additionally, we apply label smoothing to further stabilize the training process.

Unlike the adversarial loss $L ( G , D ) ( \theta )$ , derived from the traditional DCGAN setup, we incorporate label smoothing in our approach to prevent the discriminator from becoming overconfident. Instead of hard labels (1 for real samples and 0 for generated samples), we use softened labels: 0.9 for real samples and 0.1 for generated samples. This encourages the discriminator to generalize better and avoid overfitting to the training data. The adversarial loss for the generator and discriminator is given by:

$$
\begin{array}{l} L (G, D) = \min _ {G} \left(- \frac {1}{m} \sum_ {i = 1} ^ {m} \log D (G (z _ {i}))\right) \\ \qquad + \max _ {D} \left(\frac {1}{m} \sum_ {i = 1} ^ {m} \log D (x _ {i})\right) \\ \qquad + \max _ {D} \left(\frac {1}{m} \sum_ {i = 1} ^ {m} \log \bigl (1 - D (G (z _ {i})) \bigr)\right) \end{array}\tag{9}
$$

Here, label smoothing is applied to adjust the discriminator’s output as follows:

$$
D (x) = \left\{ \begin{array}{l l} 0. 9 & \text { if } x \geq 0. 5 \\ 0. 1 & \text { if } x <   0. 5 \end{array} \right.
$$

This smooth label approach improves the discriminator’s performance on unseen data by reducing overfitting. To ensure more balanced training, we combine this adversarial loss with the divergence $D ( \theta )$ and stability score $S ( \theta )$ , forming the complete dynamic loss function:

$$
L _ {\text { dynamic }} (\theta) = \alpha \cdot L (G, D) (\theta) + \beta \cdot D (\theta) + \gamma \cdot S (\theta)\tag{10}
$$

Here, $\alpha , \beta ,$ and $\gamma$ are adaptive coefficients optimized through PSO, controlling the contributions of each term. We define the initial ranges of $\alpha , \beta ,$ , and $\gamma$ within [0, 1], ensuring their sum equals 1 to maintain balance across the three components. This dynamic formulation introduces label smoothing and adaptive weighting to promote more effective training and prevent mode collapse and vanishing gradients.

1) Reconstruction loss function: As described earlier, the generator in TIPSO-GAN is transferred from PSOGAN, which has demonstrated strong sample generation capabilities. However, during adversarial training in TIPSO-GAN, the generated pseudo-samples may become too similar to real samples, potentially increasing the false positive rate. To mitigate this, a reconstruction loss is introduced in TIPSO-GAN’s objective function. This not only enhances the generator’s ability to produce diverse, realistic samples but also improves the discriminator’s capacity to distinguish between real and generated samples. The structure and parameters of the proposed reconstruction loss function in shown in Fig. 5. The discriminator outputs a one-dimensional feature map in the flattened layer, which is utilised for reconstruction. The reconstruction loss function is defined as the expected value of the L1 norm of the difference between the original sample and the sample reconstructed by the generator, based on the features extracted by the discriminator. This can be expressed as:

$$
L _ {\phi , \theta} ^ {X} = \mathbb {E} _ {x \sim p _ {x}} \left[ \left\| G _ {\theta} (D _ {\phi} ^ {F} (x)) - x \right\| _ {1} \right]\tag{11}
$$

Where $G _ { \theta } ( D _ { \phi } ^ { F } ( x ) )$ denotes the generator’s reconstruction of the input sample x using the features extracted by the discriminator. The L1 norm ensures that the reconstructed sample closely resembles the original, which enhances the discriminator’s ability to recognise real (normal) samples, thereby reducing false positives.

a) Addressing Class Imbalance with Focal Loss: While the reconstruction loss improves the quality of the generated samples, TIPSO-GAN also incorporates a focal loss in the discriminator to tackle class imbalance between normal and malicious traffic. The focal loss emphasizes hard-to-classify samples—particularly under-represented malicious traffic. The focal loss is defined as:

$$
F L (p _ {t}) = - \alpha_ {t} (1 - p _ {t}) ^ {\gamma} \log (p _ {t})\tag{12}
$$

Where $p _ { t }$ is the model’s predicted probability for the true class. $\alpha _ { t }$ is a weighting factor that balances the importance of the minority class (malicious traffic). $\gamma$ is the focusing parameter that modulates the influence of easier examples, downweighting them while focusing on harder-to-classify malicious traffic. By using focal loss, the discriminator can focus more on detecting minority-class samples, such as rare and unknown malicious traffic, while avoiding being overwhelmed by the majority class (normal traffic). Both reconstruction loss and focal loss are integrated into the overall objective function to ensure that the generator and discriminator work in tandem to produce realistic, diverse samples while addressing the class imbalance problem.

b) Discriminator Loss: The discriminator’s objective function now combines the reconstruction loss and the focal loss, ensuring that the discriminator can: 1. Distinguish between real and generated samples based on the reconstruction of intricate features. 2. Detect minority-class malicious traffic more effectively. The overall discriminator loss is expressed as:

$$
L _ {\phi} ^ {D} = L _ {\phi} ^ {D} + \lambda \cdot L _ {\phi} ^ {X} + F L (p _ {t})\tag{13}
$$

Where $L _ { \phi } ^ { D }$ is the standard adversarial loss for the discriminator. $L _ { \phi } ^ { X }$ is the reconstruction loss that helps the discriminator distinguish real from generated samples. $F L ( p _ { t } )$ is the focal loss, which ensures that the discriminator focuses more on hard-to-classify examples, especially minority-class malicious traffic.

c) Generator Loss: Similarly, the generator’s loss function includes the reconstruction loss, guiding the generator to produce samples that closely resemble real network traffic. The generator’s loss is defined as:

$$
L _ {\theta} ^ {G} = L _ {\theta} ^ {G} + \lambda \cdot L _ {\theta} ^ {X}\tag{14}
$$

![](images/8e2f99985a06ae95e4e75fdf40ce765ce4da8d80c8eae0f9d6cb65c3ac4bceab.jpg)  
Fig. 3: The structure of DCGAN

Where $L _ { \theta } ^ { G }$ is the standard adversarial loss for the generator. $L _ { \theta } ^ { X }$ is the reconstruction loss, ensuring the generated samples align closely with normal traffic patterns. The reconstruction loss helps the discriminator extract intricate features from network traffic, reducing false positives and improving the identification of normal and malicious patterns. Focal loss ensures that the discriminator pays more attention to minorityclass samples, improving its ability to detect rare malicious traffic.

2) Structure and Parameters of PSOGAN: The structure of the proposed generator architecture (PSOGAN) is shown in Fig. 3. It is based on DCGAN but introduces key enhancements to improve its capacity for generating realistic network traffic data. Starting with a 100-dimensional noise vector, the input is passed through a fully connected layer and progressively upsampled via a series of deconvolutional layers. Key differences from the standard DCGAN include the incorporation of residual connections for stable training, and dilation in the second deconvolutional layer to capture multiscale features. The discriminator in our proposed architecture is shown in Fig. 4a. It is designed to distinguish between real and generated network traffic samples, following a modified DCGAN framework. The input to the discriminator passes through several convolutional layers that progressively reduce its spatial dimensions while increasing the depth of the feature maps.

## IV. THREAT MODEL

We assume adversaries aim to evade detection of malicious traffic, degrade IDS performance through poisoning, or exploit distribution shifts such as cross-domain or zeroday attacks. We consider white-box (full architecture and parameters), gray-box (architecture known, parameters hidden), and black-box (query-only) knowledge settings. The adversary can perturb flow features within protocol-valid bounds, generate adversarial traffic with generative models, inject mislabeled samples during training, or launch transfer attacks from substitute models; in real deployments they may also attempt resource exhaustion by overloading throughput. We assume the defender controls the training environment and preprocessing pipeline, which are trusted, while traffic inputs may be adversarial. Under these assumptions, TIPSO-GAN is evaluated against static perturbations, adaptive attacks, domain-constrained and mimicry attacks, poisoning, blackbox transfer, cross-domain generalization, and unseen zeroday (LOFO) scenarios, aligning the evaluation with the threat model.

## V. EXPERIMENTAL SETUP AND EVALUATION

## A. Implementation Details

Hardware and software setup details are presented in the Appendix A-B (see Table XIV). For the GAN framework, the generator and discriminator networks were configured with setup settings in Figs 3 and 4a. Detailed sensitivity analysis and hyperparameter settings information are presented in Table XV, and Figs. 11-14.

## B. Dataset

We evaluated our framework using the CIC-IDS2018, CIC-DDoS2019 [47], and CICAPT-IIoT2024 [48], each containing normal and various attack traffic types. We evaluate under leakage-robust settings. Details of the datasets are presented in Table II. For CIC-IDS2018 and CIC-DDoS2019, we use temporal splits that simulate deployment on future traffic. For CICAPT-IIoT2024, we use grouped splits by scenario and also leave-one-scenario-out folds. Before splitting, we remove exact and near-duplicate flows using hashing on normalized numeric features and an L2 tolerance of 1e-6. Where available, we split by flow/session keys and source hosts so that related flows do not cross partitions. All preprocessing models are fit on the training set only and applied to validation and test. The resulting transformation parameters are then applied unchanged to the validation and test partitions. No information from validation or test data is used during preprocessing, training, or model selection, ensuring strict isolation and preventing leakage. TIPSO-GAN operates at the flow level, aggregating packets within each TCP/UDP session to capture temporal and statistical dependencies.

TABLE II: Details of datasets used.

<table><tr><td>#</td><td>Dataset</td><td>Hosts</td><td>Flows</td><td>Normal (%)</td><td>Attack Types</td><td>Format</td></tr><tr><td>1</td><td>CICDDoS2019</td><td>130,079</td><td>888,825</td><td>0.93</td><td>12</td><td>CSV</td></tr><tr><td>2</td><td>CICAPT-IIoT2024</td><td>412,640</td><td>1,264,978</td><td>68.42</td><td>8</td><td>CSV</td></tr><tr><td>3</td><td>CIC-IDS2018</td><td>311,940</td><td>2,830,743</td><td>78.90</td><td>8</td><td>PCAP</td></tr></table>

## C. Baseline models

We compare TIPSO-GAN against thirteen baselines covering classical machine learning, transformer-based IDS, GAN variants, IDS-oriented GANs, and other deep learning methods. Classical models include Logistic Regression, XGBoost (weighted), and LightGBM (weighted). Transformer-based IDS baselines are TransfficFormer [46], FT-Transformer [4], and MalDetectFormer [5]. GAN variants include the standard GAN, WGAN, and WGAN-GP [49]. IDS-oriented GANs include IDSGAN [50], IGAN-IDS [51], SYN-GAN [52], SGAN-IDS [40], BigGan [53], and FenceGAN [54]. Additional deep learning baselines are IDS-INT [55], PSO-D-SEM [56], FR-APPSO-BiLSTM [57], and HAGRU [19]. This set spans classical, generative, and deep learning methods, providing a comprehensive basis for comparison.

## VI. RESULTS

Our study addresses the following five main questions:

1) Does TIPSO-GAN achieve stable GAN training and realistic flow generation? (Sections VI-A & VI-B)

![](images/bf53e4b716dd699a1824e2ffe26d98b8b2d914a31b681c478a31c675e0df05f3.jpg)  
Fig. 4: Network structure of pre-training model DeePreD (a) and Discriminator (b) of DCGAN

![](images/9fc8509babdeb4bca13d17af1bae2ce1a2b4694211f86b9a534af34b4f58a823.jpg)  
Fig. 5: Reconstruction of loss flow chart

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 Modified PSO for GAN Parameters Optimization
1: procedure PSO_GAN(N, max_iterations,  $W_{max}$ ,  $W_{min}$ ,  $C_{1}$ ,  $C_{2}$ )
2: Input: Population size N, Maximum iterations max_iterations, inertia bounds  $W_{max}$ ,  $W_{min}$ , learning rates  $C_{1}$ ,  $C_{2}$ 
3: Output: Best-performing configuration for GAN parameters
4: Initialize particles and velocity vectors
5: for iter = 1 to max_iterations do
6: for each particle do
7: Evaluate fitness
8: Update personal and global bests
9: Update velocity and position
10: Apply boundary check
11: end for
12: Adapt inertia weight linearly
13: end for
14: return Best-performing particle configuration
15: end procedure
</div>

2) Can TIPSO-GAN generalize to unseen attack families under LOFO and cross-dataset tests? (Section VI-F)

3) Is TIPSO-GAN robust to adaptive, domain-consistent, mimicry, poisoning, and transfer attacks? (Section VI-G)

4) How does TIPSO-GAN compare to transformer IDS models, non-GAN baselines, and stabilized GAN variants? (Section VI-D)

5) Is TIPSO-GAN efficient for real-time deployment in terms of latency, throughput, and resource usage? (Sections VI-H, VI-H1, and VI-I)

## A. Training stability and mode collapse

In this experiment, we assess the stability and resilience of TIPSO-GAN on the CICAPT-IIoT2024 dataset against mode collapse and compare its performance to DCGAN, WGAN, LSGAN, and the conventional GAN. Table III reports values at epochs $E ~ \in ~ 2 0 , 5 0 , 8 0 , 1 0 0$ . TIPSO-GAN consistently achieved the lowest MMD/KS/RMSE and highest entropy/coverage, converging as early as epoch 50 and plateauing thereafter. WGAN and SGAN-IDS were second-best in some cases, but TIPSO-GAN outperformed all baselines in the final epoch with MMD 0.063, KS 0.095, RMSE 0.081, entropy 0.91, and coverage 96%. The epoch-wise reporting demonstrates stability: baseline models improve gradually, while TIPSO-GAN converges rapidly and maintains flat curves with no oscillations. This rules out mode collapse, since entropy and coverage both increase monotonically rather than dropping at later epochs.

TABLE III: Stability and Mode Collapse.

<table><tr><td rowspan="2" colspan="2">Metric / Epoch</td><td colspan="8">Models</td></tr><tr><td>GAN</td><td>DCGAN</td><td>LSGAN</td><td>WGAN</td><td>WGAN-GP</td><td>BigGAN</td><td>SGAN-IDS</td><td>TIPSO-GAN</td></tr><tr><td rowspan="4">MMD ↓</td><td>20</td><td>0.310</td><td>0.280</td><td>0.260</td><td>0.200</td><td>0.185</td><td>0.150</td><td>0.170</td><td>0.095</td></tr><tr><td>50</td><td>0.240</td><td>0.210</td><td>0.190</td><td>0.160</td><td>0.148</td><td>0.120</td><td>0.140</td><td>0.070</td></tr><tr><td>80</td><td>0.210</td><td>0.190</td><td>0.170</td><td>0.135</td><td>0.130</td><td>0.110</td><td>0.120</td><td>0.065</td></tr><tr><td>100</td><td>0.189</td><td>0.174</td><td>0.161</td><td>0.128</td><td>0.125</td><td>0.105</td><td>0.110</td><td>0.063</td></tr><tr><td rowspan="4">KS ↓</td><td>20</td><td>0.360</td><td>0.330</td><td>0.305</td><td>0.270</td><td>0.250</td><td>0.210</td><td>0.240</td><td>0.160</td></tr><tr><td>50</td><td>0.300</td><td>0.270</td><td>0.250</td><td>0.220</td><td>0.200</td><td>0.170</td><td>0.200</td><td>0.120</td></tr><tr><td>80</td><td>0.280</td><td>0.250</td><td>0.230</td><td>0.200</td><td>0.190</td><td>0.160</td><td>0.185</td><td>0.100</td></tr><tr><td>100</td><td>0.247</td><td>0.228</td><td>0.211</td><td>0.182</td><td>0.178</td><td>0.150</td><td>0.169</td><td>0.095</td></tr><tr><td rowspan="4">RMSE ↓</td><td>20</td><td>0.240</td><td>0.210</td><td>0.198</td><td>0.178</td><td>0.165</td><td>0.145</td><td>0.162</td><td>0.120</td></tr><tr><td>50</td><td>0.190</td><td>0.170</td><td>0.160</td><td>0.150</td><td>0.140</td><td>0.118</td><td>0.138</td><td>0.095</td></tr><tr><td>80</td><td>0.170</td><td>0.160</td><td>0.150</td><td>0.130</td><td>0.128</td><td>0.108</td><td>0.120</td><td>0.085</td></tr><tr><td>100</td><td>0.152</td><td>0.141</td><td>0.136</td><td>0.122</td><td>0.120</td><td>0.102</td><td>0.114</td><td>0.081</td></tr><tr><td rowspan="4">Entropy ↑</td><td>20</td><td>0.42</td><td>0.48</td><td>0.50</td><td>0.55</td><td>0.57</td><td>0.60</td><td>0.58</td><td>0.72</td></tr><tr><td>50</td><td>0.53</td><td>0.56</td><td>0.59</td><td>0.66</td><td>0.68</td><td>0.71</td><td>0.69</td><td>0.85</td></tr><tr><td>80</td><td>0.58</td><td>0.60</td><td>0.63</td><td>0.70</td><td>0.72</td><td>0.75</td><td>0.73</td><td>0.89</td></tr><tr><td>100</td><td>0.62</td><td>0.66</td><td>0.69</td><td>0.74</td><td>0.76</td><td>0.78</td><td>0.77</td><td>0.91</td></tr><tr><td rowspan="4">Coverage ↑</td><td>20</td><td>41%</td><td>46%</td><td>49%</td><td>55%</td><td>58%</td><td>62%</td><td>60%</td><td>78%</td></tr><tr><td>50</td><td>55%</td><td>58%</td><td>63%</td><td>70%</td><td>72%</td><td>76%</td><td>74%</td><td>90%</td></tr><tr><td>80</td><td>60%</td><td>63%</td><td>68%</td><td>77%</td><td>79%</td><td>82%</td><td>80%</td><td>94%</td></tr><tr><td>100</td><td>68%</td><td>71%</td><td>74%</td><td>80%</td><td>82%</td><td>85%</td><td>83%</td><td>96%</td></tr></table>

## B. Synthetic Data Quality in Learned Embedding Space

To evaluate the fidelity and diversity of generated traffic beyond raw flow distributions, we compute metrics in a earned tabular embedding space. A 64-dimensional autoencoder was trained on real CICIDS-2018 traffic, and synthetic samples from each GAN variant were projected into this embedding. Following, we report squared Maximum Mean Discrepancy (MMD<sup>2</sup>) as a fidelity measure and precision, recall, and PR-F1 as diversity measures. All results are averaged over 5 random seeds with 95% confidence intervals. Table IV shows that TIPSO-GAN achieves the best overall quality, with the lowest MMD<sup>2</sup> (0.091 ± 0.006) and the highest precision (0.873 ± 0.009), recall (0.861 ± 0.009), and PR-F1 (0.867 ± 0.009). SGAN-IDS and WGAN are the closest competitors, but TIPSO-GAN consistently outperforms them across all metrics. These results indicate that TIPSO-GAN generates synthetic IIoT traffic that is both highly faithful to the real distribution and sufficiently diverse to avoid mode collapse, even under multiple training runs. This confirms the robustness of TIPSO-GAN when evaluated in a representation learned from the data, rather than relying only on raw flow statistics.

![](images/fdf02f7fcd4009b4e9d225f77189bba0ed27d821109379d7c08c4a6e3363bd52.jpg)  
(a) Collection

![](images/6ca4dcd63f5ab35e4857f1b22312b8e9850f002fbe5f2f9f9e9d47783c321d39.jpg)  
(b) Exfiltration

![](images/6c1824d2f1727844db044efc9f32b43829bbba5dd277ea0d9366c0052a7dd95a.jpg)

![](images/93e6e5acaa342b19b803b3b2161aef51cf26cb9188b1ab92a507a8420dcc899f.jpg)  
(c) Credential Access

(e) Discovery  
![](images/3adf681fc372e00e89397d4757db1a31a899dd5873ac1f92bc46c53d7b691fdc.jpg)

(d) Defence Evasion  
![](images/a89913f30244658082a1c0216fba447eaf6ff24d9e962c4e6ff41ee4835a1883.jpg)  
(f) Lateral Movement

![](images/19f2e584725fa52100f95c38adbe74926480e2b6170c65f27f362cacd8e4705d.jpg)  
(g) Persistence

![](images/e4e9e6257a56221350838c731f5a5c469f0cb39200c8370c708bc9c278f0dd67.jpg)  
(h) Command & Control  
Fig. 6: Per-class Precision–Recall curves on CICAPT-IIoT2024.

TABLE IV: Synthetic data quality in a learned tabular embedding (64-D autoencoder).

<table><tr><td>Model</td><td> $MMD^2$ (↓)</td><td>Precision (↑)</td><td>Recall (↑)</td><td>PR-F1 (↑)</td></tr><tr><td>GAN</td><td>0.355 ± 0.012</td><td>0.622 ± 0.011</td><td>0.611 ± 0.012</td><td>0.616 ± 0.011</td></tr><tr><td>DCGAN</td><td>0.291 ± 0.010</td><td>0.678 ± 0.012</td><td>0.664 ± 0.013</td><td>0.671 ± 0.012</td></tr><tr><td>LSGAN</td><td>0.248 ± 0.009</td><td>0.713 ± 0.013</td><td>0.701 ± 0.012</td><td>0.707 ± 0.012</td></tr><tr><td>WGAN</td><td>0.182 ± 0.008</td><td>0.782 ± 0.010</td><td>0.774 ± 0.011</td><td>0.778 ± 0.010</td></tr><tr><td>WGAN-GP</td><td>0.170 ± 0.008</td><td>0.795 ± 0.010</td><td>0.769 ± 0.010</td><td>0.782 ± 0.010</td></tr><tr><td>BigGAN</td><td>0.140 ± 0.007</td><td>0.821 ± 0.009</td><td>0.808 ± 0.009</td><td>0.814 ± 0.009</td></tr><tr><td>SGAN-IDS</td><td>0.152 ± 0.007</td><td>0.812 ± 0.010</td><td>0.801 ± 0.010</td><td>0.806 ± 0.010</td></tr><tr><td>TIPSO-GAN</td><td>0.091 ± 0.006</td><td>0.873 ± 0.009</td><td>0.861 ± 0.009</td><td>0.867 ± 0.009</td></tr></table>

## C. Multiclass detection results

We evaluate detection performance across all eight attack stages using per-class precision–recall (PR) curves and PR–AUC scores using the CICAPT-IIoT2024 dataset. Figure 6 shows the per-class PR-AUC curves with all models overlaid. TIPSO-GAN consistently dominates across classes, achieving higher PR–AUC than all baselines, particularly in minority classes such as Persistence and Lateral Movement. Exact per-class PR–AUC values, together with macro and micro averages, are reported in Table V, where TIPSO-GAN is marked as the best model in nearly every case.

To complement these threshold-free results, we also analyze performance at the operating point used for F1 optimization using the CICAPT-IIoT2024 dataset. Row-normalized confusion matrices for each model, computed at the macro-F1-optimal threshold on the validation set, are provided in Fig. 7. These matrices highlight where errors concentrate and illustrate that TIPSO-GAN not only achieves higher recall overall but also avoids the systematic misclassifications observed in GAN and DCGAN baselines. Together, the PR curves and PR–AUC scores in the main body, along with confusion matrices in Fig. 7, provide a comprehensive picture: TIPSO-GAN offers both superior ranking quality and robust thresholded classification across all APT attack stages.

## D. Detection performance

We evaluate all methods under rigorous, reproducible protocols. For CIC-IDS2018 and CIC-DDoS2019, we explicitly deduplicated flows, enforced flow/session and host isolation, and fit preprocessing only on training data to mitigate leakage. For CICAPT-IIoT2024, we assign entire scenarios to a single partition (grouped split) to prevent intra-scenario leakage. All results are averaged over five independent runs (mean±std) on the test sets.

On CIC-IDS2018, classical tabular learners and recent transformer models are competitive: LightGBM attains 96.9±0.3 F1 and MalDetectFormer 96.9±0.3 F1, with FT-Transformer and TransTraffic close behind (96.1±0.4 and 96.5±0.3 F1, respectively). Among GAN-based baselines, WGAN-GP reaches 94.2±0.4 F1 and SGAN-IDS/WGAN achieve 93.7±0.3 F1. The strongest non-ours baseline overall is PSO-D-SEM at 98.9±0.2 F1. TIPSO-GAN achieves $9 9 . 1 { \pm } 0 . 1 $ F1 (99.1±0.1 precision, 99.3±0.1 recall), improving over the strongest baseline by +0.2 F1 while maintaining low variance across seeds.

On CICAPT-IIoT2024, Transformer models remain strong (TransTraffic 95.0±0.3 F1; MalDetectFormer 94.7±0.3), and WGAN-GP is the best among standard GAN variants at 94.2±0.4 F1. PSO-D-SEM is the strongest non-ours method overall at 98.2±0.2 F1. TIPSO-GAN delivers 98.9±0.1 F1 (98.9±0.1 precision, 99.1±0.1 recall), exceeding the best baseline by +0.7 F1 under leakage-free scenario grouping.

On CIC-DDoS2019, temporal splits yield realistic difficulty: TransTraffic attains 94.6±0.4 F1 and MalDetectFormer

![](images/05ecfe59b591ecd3aa52d4da1cac6c990acddbb2eec88115f79e2cc4cad265a6.jpg)  
(a) GAN

![](images/1fab13270a62835345330a641660bfc30050093ba68a36872a68939e5b3e044a.jpg)

![](images/4e6b038a97b2e6f0d17ba7f4278f7f667cbf6bc5ba1ef122e3888ab26e3ef8c5.jpg)

![](images/ff5fdede74e46d27f2feb6e0a3c7782335afd7038220e9facfdac1b80b764eac.jpg)  
(d) WGAN-GP

(b) DCGAN  
(c) BigGAN  
![](images/5379508920189f06254a93a92a328f146fa0d2467709ca29905bd3fe089859c8.jpg)  
(e) SGAN-IDS

![](images/1d91c7ff9aed2363e2457230987cf4aec063059525ecbde88e55f137183099a4.jpg)  
(f) TIPSO-GAN  
Fig. 7: Row-normalized confusion matrices on CICAPT-IIoT2024 at the F1-optimal threshold.

TABLE V: Per-class PR-AUC on CICAPT-IIoT2024 (mean ± 95% CI over 5 seeds).

<table><tr><td>Class</td><td>GAN</td><td>DCGAN</td><td>LSGAN</td><td>WGAN</td><td>WGAN-GP</td><td>BigGAN</td><td>SGAN-IDS</td><td>TIPSO-GAN</td></tr><tr><td>Collection</td><td>0.788 ± 0.012</td><td>0.826 ± 0.011</td><td>0.862 ± 0.010</td><td>0.951 ± 0.007</td><td>0.960 ± 0.006</td><td>0.968 ± 0.005</td><td>0.972 ± 0.006</td><td>1.000 ± 0.003</td></tr><tr><td>Command &amp; Control</td><td>0.684 ± 0.015</td><td>0.736 ± 0.013</td><td>0.775 ± 0.012</td><td>0.903 ± 0.008</td><td>0.941 ± 0.006</td><td>0.950 ± 0.005</td><td>0.960 ± 0.006</td><td>0.999 ± 0.002</td></tr><tr><td>Credential Access</td><td>0.618 ± 0.014</td><td>0.712 ± 0.012</td><td>0.764 ± 0.011</td><td>0.895 ± 0.009</td><td>0.944 ± 0.006</td><td>0.949 ± 0.005</td><td>0.955 ± 0.006</td><td>0.999 ± 0.002</td></tr><tr><td>Defence Evasion</td><td>0.671 ± 0.014</td><td>0.751 ± 0.012</td><td>0.808 ± 0.011</td><td>0.921 ± 0.008</td><td>0.950 ± 0.006</td><td>0.955 ± 0.005</td><td>0.961 ± 0.005</td><td>0.998 ± 0.002</td></tr><tr><td>Discovery</td><td>0.720 ± 0.013</td><td>0.793 ± 0.012</td><td>0.829 ± 0.011</td><td>0.931 ± 0.008</td><td>0.954 ± 0.006</td><td>0.960 ± 0.005</td><td>0.967 ± 0.005</td><td>0.999 ± 0.002</td></tr><tr><td>Exfiltration</td><td>0.738 ± 0.012</td><td>0.751 ± 0.012</td><td>0.851 ± 0.010</td><td>0.939 ± 0.007</td><td>0.961 ± 0.005</td><td>0.968 ± 0.004</td><td>0.974 ± 0.004</td><td>0.999 ± 0.002</td></tr><tr><td>Lateral Movement</td><td>0.583 ± 0.016</td><td>0.646 ± 0.015</td><td>0.754 ± 0.012</td><td>0.888 ± 0.009</td><td>0.930 ± 0.006</td><td>0.938 ± 0.005</td><td>0.942 ± 0.005</td><td>0.999 ± 0.002</td></tr><tr><td>Persistence</td><td>0.653 ± 0.015</td><td>0.713 ± 0.013</td><td>0.747 ± 0.012</td><td>0.884 ± 0.009</td><td>0.940 ± 0.006</td><td>0.946 ± 0.005</td><td>0.952 ± 0.005</td><td>0.998 ± 0.002</td></tr><tr><td>Macro Avg</td><td>0.682 ± 0.014</td><td>0.741 ± 0.012</td><td>0.799 ± 0.011</td><td>0.914 ± 0.008</td><td>0.947 ± 0.006</td><td>0.954 ± 0.005</td><td>0.960 ± 0.005</td><td>0.999 ± 0.002</td></tr><tr><td>Micro Avg</td><td>0.690 ± 0.013</td><td>0.747 ± 0.012</td><td>0.805 ± 0.010</td><td>0.920 ± 0.007</td><td>0.950 ± 0.006</td><td>0.957 ± 0.005</td><td>0.962 ± 0.005</td><td>0.999 ± 0.002</td></tr></table>

94.3±0.4 F1; among vanilla GANs, WGAN-GP reaches 93.8±0.4 F1. The best non-ours baseline is PSO-D-SEM at $9 7 . 7 { \pm } 0 . 2 $ F1. TIPSO-GAN achieves 98.7±0.1 F1 with balanced precision/recall (98.8±0.1 / 99.0±0.1), improving over the strongest baseline by +1.0 F1. Across datasets, TIPSO-GAN consistently outperforms the strongest non-ours baseline by +0.2–1.0 F1 while preserving high precision and recall and low run-to-run variance.

## E. Calibration Analysis

We further evaluate model calibration, since overconfident but incorrect predictions pose serious risks in adversarial intrusion detection. This experiment was based on the CICAPT-IIoT2024 dataset. Calibration is assessed through reliability diagrams, which compare predicted confidence with empirical accuracy. The orange dashed line denotes perfect calibration, while the blue curve shows the model’s empirical reliability. The shaded area represents the miscalibration gap, quantitatively summarized by the Expected Calibration Error (ECE), which is displayed in each legend alongside the Brier Score. Lower values indicate better calibration.

Figure 9 shows that baseline models such as GAN, Big-GAN, and DCGAN tend to deviate from the diagonal, particularly at higher confidence levels, indicating overconfidence. TIPSO-GAN, in contrast, tracks the diagonal closely across all bins, with the lowest ECE and Brier scores. This demonstrates that TIPSO-GAN not only improves detection performance but also produces well-calibrated probability estimates, which are critical for operational decision-making in IIoT security.

TABLE VI: Robustness against adversarial attacks (mean ±95% CI over 5 seeds).

<table><tr><td>Category</td><td>Attack Type</td><td>Metric</td><td>GAN</td><td>DCGAN</td><td>LSGAN</td><td>WGAN</td><td>WGAN-GP</td><td>BigGAN</td><td>SGAN-IDS</td><td>TIPSO-GAN</td></tr><tr><td rowspan="10">Static</td><td rowspan="2">FGSM ( $\epsilon = 0.03$ )</td><td>FPR ↓</td><td>12.3</td><td>11.0</td><td>10.2</td><td>9.5</td><td>8.5</td><td>7.9</td><td>6.9</td><td>2.8</td></tr><tr><td>FNR ↓</td><td>15.7</td><td>14.4</td><td>13.5</td><td>12.6</td><td>11.2</td><td>10.5</td><td>9.1</td><td>3.5</td></tr><tr><td rowspan="2">BIM ( $\epsilon = 0.03$ )</td><td>FPR ↓</td><td>13.1</td><td>11.7</td><td>10.9</td><td>10.2</td><td>9.2</td><td>8.5</td><td>7.4</td><td>3.0</td></tr><tr><td>FNR ↓</td><td>17.2</td><td>15.8</td><td>14.6</td><td>13.6</td><td>12.6</td><td>11.7</td><td>9.8</td><td>4.1</td></tr><tr><td rowspan="2">PGD ( $\epsilon = 0.03$ )</td><td>FPR ↓</td><td>14.0</td><td>12.6</td><td>11.5</td><td>10.8</td><td>10.1</td><td>9.2</td><td>8.1</td><td>3.3</td></tr><tr><td>FNR ↓</td><td>18.5</td><td>16.9</td><td>15.6</td><td>14.4</td><td>13.4</td><td>12.5</td><td>10.6</td><td>4.5</td></tr><tr><td rowspan="2">C&amp;W ( $\ell_2$ )</td><td>FPR ↓</td><td>14.8</td><td>13.4</td><td>12.0</td><td>11.4</td><td>10.8</td><td>9.8</td><td>8.6</td><td>3.5</td></tr><tr><td>FNR ↓</td><td>19.3</td><td>17.7</td><td>16.2</td><td>15.2</td><td>14.1</td><td>13.0</td><td>11.0</td><td>4.8</td></tr><tr><td rowspan="2">DeepFool</td><td>FPR ↓</td><td>13.5</td><td>12.1</td><td>11.0</td><td>10.4</td><td>9.7</td><td>8.9</td><td>7.9</td><td>3.2</td></tr><tr><td>FNR ↓</td><td>17.0</td><td>15.6</td><td>14.4</td><td>13.4</td><td>12.2</td><td>11.3</td><td>9.5</td><td>4.0</td></tr><tr><td rowspan="4">Adaptive</td><td rowspan="2">Adaptive-PGD</td><td>FPR ↓</td><td>15.4</td><td>14.0</td><td>12.9</td><td>11.9</td><td>11.0</td><td>10.2</td><td>8.8</td><td>3.6</td></tr><tr><td>FNR ↓</td><td>20.1</td><td>18.6</td><td>17.3</td><td>16.1</td><td>14.8</td><td>13.8</td><td>11.9</td><td>5.1</td></tr><tr><td rowspan="2">AutoAttack [58]</td><td>FPR ↓</td><td>16.7</td><td>15.1</td><td>13.8</td><td>13.0</td><td>12.3</td><td>11.4</td><td>9.6</td><td>4.1</td></tr><tr><td>FNR ↓</td><td>21.5</td><td>19.9</td><td>18.4</td><td>17.2</td><td>15.7</td><td>14.5</td><td>12.7</td><td>5.6</td></tr><tr><td rowspan="4">Constrained</td><td rowspan="2">Constrained-PGD</td><td>FPR ↓</td><td>7.8</td><td>7.1</td><td>6.5</td><td>6.0</td><td>5.4</td><td>4.9</td><td>4.7</td><td>2.6</td></tr><tr><td>FNR ↓</td><td>14.9</td><td>13.8</td><td>12.6</td><td>11.7</td><td>10.8</td><td>9.9</td><td>8.3</td><td>4.9</td></tr><tr><td rowspan="2">Constrained-AA</td><td>FPR ↓</td><td>8.6</td><td>7.8</td><td>6.9</td><td>6.5</td><td>6.1</td><td>5.6</td><td>5.3</td><td>3.1</td></tr><tr><td>FNR ↓</td><td>16.5</td><td>15.2</td><td>13.9</td><td>13.0</td><td>12.2</td><td>11.1</td><td>9.6</td><td>5.8</td></tr><tr><td rowspan="6">Mimicry</td><td rowspan="2">EvadeML [59]</td><td>FPR ↓</td><td>15.8</td><td>14.2</td><td>13.1</td><td>12.3</td><td>11.6</td><td>10.7</td><td>9.1</td><td>4.2</td></tr><tr><td>FNR ↓</td><td>20.5</td><td>18.8</td><td>17.4</td><td>16.3</td><td>15.3</td><td>14.1</td><td>12.5</td><td>5.4</td></tr><tr><td rowspan="2">FENCE [60]</td><td>FPR ↓</td><td>14.9</td><td>13.5</td><td>12.4</td><td>11.7</td><td>10.9</td><td>10.0</td><td>8.6</td><td>3.7</td></tr><tr><td>FNR ↓</td><td>19.2</td><td>17.8</td><td>16.6</td><td>15.4</td><td>14.1</td><td>13.2</td><td>11.2</td><td>4.9</td></tr><tr><td rowspan="2">Mimicus [59]</td><td>FPR ↓</td><td>15.1</td><td>13.7</td><td>12.7</td><td>11.9</td><td>11.2</td><td>10.3</td><td>8.9</td><td>4.0</td></tr><tr><td>FNR ↓</td><td>19.9</td><td>18.3</td><td>17.0</td><td>15.8</td><td>14.6</td><td>13.4</td><td>11.8</td><td>5.2</td></tr><tr><td rowspan="6">Poisoning</td><td rowspan="2">1% label flip</td><td>FPR ↓</td><td>10.5</td><td>9.3</td><td>8.6</td><td>7.9</td><td>7.1</td><td>6.5</td><td>5.9</td><td>2.9</td></tr><tr><td>FNR ↓</td><td>12.8</td><td>11.6</td><td>10.6</td><td>10.0</td><td>9.4</td><td>8.8</td><td>7.7</td><td>3.8</td></tr><tr><td rowspan="2">3% label flip</td><td>FPR ↓</td><td>13.2</td><td>12.0</td><td>11.1</td><td>10.4</td><td>9.5</td><td>8.7</td><td>7.8</td><td>3.9</td></tr><tr><td>FNR ↓</td><td>18.1</td><td>16.7</td><td>15.6</td><td>14.3</td><td>13.0</td><td>12.0</td><td>10.4</td><td>5.0</td></tr><tr><td rowspan="2">5% label flip</td><td>FPR ↓</td><td>16.5</td><td>15.1</td><td>14.0</td><td>13.0</td><td>12.4</td><td>11.2</td><td>10.1</td><td>5.8</td></tr><tr><td>FNR ↓</td><td>22.7</td><td>21.1</td><td>19.9</td><td>18.5</td><td>17.1</td><td>15.6</td><td>13.9</td><td>7.1</td></tr><tr><td rowspan="4">Black-box</td><td rowspan="2">ResNet → TIPSO-GAN</td><td>FPR ↓</td><td>14.6</td><td>13.3</td><td>12.4</td><td>11.5</td><td>10.5</td><td>9.6</td><td>8.7</td><td>3.9</td></tr><tr><td>FNR ↓</td><td>19.8</td><td>18.4</td><td>17.0</td><td>15.8</td><td>14.4</td><td>13.2</td><td>11.6</td><td>5.3</td></tr><tr><td rowspan="2">Ensemble substitutes</td><td>FPR ↓</td><td>16.2</td><td>14.9</td><td>13.6</td><td>12.7</td><td>11.8</td><td>10.8</td><td>9.8</td><td>4.6</td></tr><tr><td>FNR ↓</td><td>22.1</td><td>20.6</td><td>19.2</td><td>17.8</td><td>16.3</td><td>15.1</td><td>13.4</td><td>6.2</td></tr></table>

## F. Robustness against unseen and cross-domain attacks

Table VIII highlights TIPSO-GAN’s robustness under two strict zero-day regimes using the CIC-IDS2018, CIC-DDoS2019, and CICAPT-IIoT2024 datasets. In the LOFO setting on CIC-IDS2018, performance decreases from 99.1 F1 (temporal split, Table VII) to an average of 92.3 F1, reflecting the difficulty of generalizing to entirely unseen attack families. The per-family breakdown shows variability: Web Attacks and Brute Force remain easier to detect (93.9 and 93.4 F1), while Infiltration is most challenging (90.4 F1), consistent with its low prevalence and stealthy traffic patterns. Second, a crossdataset protocol was used, training on one corpus and testing on another to assess domain transferability across different network environments and traffic distributions. The results show F1 scores ranging from 79–83 across train/test pairs. This ∼15–20 point drop shows the severe distribution shift across corpora collected under different environments. Despite this degradation, TIPSO-GAN consistently maintains recall above 80%, demonstrating non-trivial transferability to unseen domains. These results emphasize that while temporal splits are necessary, zero-day protocols such as LOFO and crossdataset evaluation provide a more realistic measure of IDS generalization.

## G. Adversarial Robustness

We evaluate robustness against static, adaptive, domainconstrained, mimicry, poisoning, and black-box transfer attacks on the CIC-IDS2018 dataset. Results are reported in terms of FPR and FNR, averaged over five runs with 95% confidence intervals (Table VI). Under FGSM, BIM, PGD, C&W, and DeepFool, TIPSO-GAN yields FPR around 3% and

FNR below 5%, while baselines range from 7–19%. Against Adaptive-PGD and AutoAttack, TIPSO-GAN maintains FNR under 6%, compared to 12–22% for prior models. With constrained PGD and AutoAttack that enforce numeric bounds, one-hot consistency, immutable masking, and cross-feature checks, TIPSO-GAN records FPR of 2.6–3.1% and FNR under 6%, outperforming baselines by large margins.

For EvadeML, FENCE, and Mimicus, TIPSO-GAN reduces FNR to 5–6%, while baselines show 12–20%. With label-flip poisoning, TIPSO-GAN rises gradually from 3.8% FNR at 1% flip to 7.1% at 5%, while baselines exceed 13–22%. Blackbox transfer. With ResNet and ensemble substitutes, TIPSO-GAN holds FNR under 6.2% versus 12–22% for baselines. TIPSO-GAN sustains lower FPR and FNR across all attack families, including domain-constrained and mimicry scenarios, demonstrating credible robustness under realistic IDS evasion settings.

## H. Runtime Performance, Scalability, and Deployment

We benchmark training cost, inference latency, throughput, and resource usage across representative IDS baselines (Table X) on the CICAPT-IIoT2024 dataset. All models were trained on an NVIDIA A100 with 32 CPU cores. Classical ML methods (Logistic Regression, XGBoost, LightGBM) achieve sub-millisecond inference and very high throughput but lack adversarial robustness. Deep IDS models such as IDS-INT, PSO-D-SEM, FR-APPSO-BiLSTM, and HAGRU require 6– 12 GPU hours to train and have latencies near 1 ms per flow, limiting scalability to under 1k flows/s. Transformer models (TransfficFormer, FT-Transformer, MalDetectFormer) show strong detection but incur higher training cost (18– 24 GPU hours), larger memory footprints (3–3.5 GB), and moderate throughput (1.3–1.6k flows/s). GAN-based IDS provide a better trade-off: GAN and WGAN achieve 2.6–2.8k flows/s, while SGAN-IDS and WGAN-GP trade higher training cost for robustness. TIPSO-GAN requires 14 GPU hours

TABLE VII: Detection performance of all evaluated IDS models across three datasets. Red = best; Blue = second best.

<table><tr><td>Dataset</td><td>Model</td><td>Acc.</td><td>Prec.</td><td>Rec.</td><td>F1</td><td>Train / Test (s)</td></tr><tr><td rowspan="24">CICIDS2018</td><td>Non-GAN Baselines</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>LightGBM (class weighted)</td><td>94.6 ± 0.4</td><td>94.3 ± 0.4</td><td>94.4 ± 0.4</td><td>94.4 ± 0.4</td><td>191 / 8</td></tr><tr><td>IDS-INT</td><td>87.4 ± 0.5</td><td>86.0 ± 0.5</td><td>84.5 ± 0.6</td><td>85.3 ± 0.5</td><td>25110 / 2481</td></tr><tr><td>PSO-D-SEM</td><td>97.7 ± 0.2</td><td>97.2 ± 0.2</td><td>98.2 ± 0.2</td><td>97.7 ± 0.2</td><td>42890 / 2410</td></tr><tr><td>FR-APPSO-BiLSTM</td><td>89.9 ± 0.4</td><td>89.2 ± 0.4</td><td>88.0 ± 0.5</td><td>88.6 ± 0.4</td><td>85400 / 4633</td></tr><tr><td>HAGRU</td><td>87.7 ± 0.5</td><td>86.9 ± 0.5</td><td>85.0 ± 0.6</td><td>85.9 ± 0.5</td><td>51402 / 5180</td></tr><tr><td>Transformer-based Models</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TransfficFormer</td><td>92.7 ± 0.6</td><td>92.3 ± 0.6</td><td>92.0 ± 0.7</td><td>92.2 ± 0.6</td><td>1085 / 51</td></tr><tr><td>FT-Transformer</td><td>94.0 ± 0.5</td><td>93.7 ± 0.5</td><td>93.8 ± 0.5</td><td>93.8 ± 0.5</td><td>1165 / 52</td></tr><tr><td>TransTraffic</td><td>94.8 ± 0.4</td><td>94.6 ± 0.4</td><td>94.7 ± 0.4</td><td>94.6 ± 0.4</td><td>1278 / 59</td></tr><tr><td>MalDetectFormer</td><td>94.5 ± 0.4</td><td>94.2 ± 0.4</td><td>94.3 ± 0.4</td><td>94.3 ± 0.4</td><td>1342 / 61</td></tr><tr><td>GAN-based IDS</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GAN</td><td>83.1 ± 0.5</td><td>81.5 ± 0.5</td><td>79.9 ± 0.5</td><td>80.7 ± 0.5</td><td>6984 / 1360</td></tr><tr><td>DCGAN</td><td>84.5 ± 0.5</td><td>83.1 ± 0.5</td><td>81.1 ± 0.5</td><td>82.1 ± 0.5</td><td>34011 / 4445</td></tr><tr><td>LSGAN</td><td>85.8 ± 0.4</td><td>84.5 ± 0.5</td><td>82.2 ± 0.5</td><td>83.3 ± 0.5</td><td>40955 / 2493</td></tr><tr><td>WGAN</td><td>91.7 ± 0.3</td><td>90.9 ± 0.3</td><td>90.0 ± 0.3</td><td>90.5 ± 0.3</td><td>43233 / 2609</td></tr><tr><td>SGAN-IDS</td><td>93.4 ± 0.3</td><td>92.5 ± 0.3</td><td>91.1 ± 0.4</td><td>91.8 ± 0.3</td><td>44730 / 3752</td></tr><tr><td>SYN-GAN</td><td>90.4 ± 0.4</td><td>89.3 ± 0.4</td><td>87.9 ± 0.5</td><td>88.6 ± 0.4</td><td>44500 / 5213</td></tr><tr><td>IGAN-IDS</td><td>89.2 ± 0.5</td><td>88.2 ± 0.5</td><td>86.4 ± 0.5</td><td>87.3 ± 0.5</td><td>32790 / 1693</td></tr><tr><td>IDSGAN</td><td>88.2 ± 0.5</td><td>87.0 ± 0.5</td><td>85.2 ± 0.6</td><td>86.1 ± 0.5</td><td>7105 / 870</td></tr><tr><td>FenceGAN</td><td>84.9 ± 0.4</td><td>84.0 ± 0.5</td><td>81.9 ± 0.5</td><td>83.0 ± 0.5</td><td>8381 / 1225</td></tr><tr><td>BigGAN</td><td>93.9 ± 0.4</td><td>93.4 ± 0.4</td><td>93.3 ± 0.4</td><td>93.4 ± 0.4</td><td>49650 / 3150</td></tr><tr><td>WGAN-GP</td><td>94.1 ± 0.4</td><td>93.7 ± 0.4</td><td>93.9 ± 0.4</td><td>93.8 ± 0.4</td><td>50500 / 2990</td></tr><tr><td>TIPSO-GAN (ours)</td><td>99.5 ± 0.1</td><td>98.8 ± 0.1</td><td>99.0 ± 0.1</td><td>98.7 ± 0.1</td><td>6611 / 410</td></tr><tr><td rowspan="26">CICAPT-IIoT2024</td><td>Non-GAN Baselines</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Logistic Regression (calibrated)</td><td>89.5 ± 0.6</td><td>88.9 ± 0.6</td><td>88.4 ± 0.7</td><td>88.6 ± 0.6</td><td>41 / 6</td></tr><tr><td>XGBoost (class weighted)</td><td>94.3 ± 0.4</td><td>94.0 ± 0.5</td><td>94.5 ± 0.4</td><td>94.2 ± 0.4</td><td>228 / 9</td></tr><tr><td>LightGBM (class weighted)</td><td>95.4 ± 0.4</td><td>95.2 ± 0.4</td><td>95.3 ± 0.5</td><td>95.3 ± 0.4</td><td>194 / 8</td></tr><tr><td>IDS-INT</td><td>88.7 ± 0.5</td><td>87.5 ± 0.5</td><td>85.4 ± 0.6</td><td>86.4 ± 0.5</td><td>26012 / 2635</td></tr><tr><td>PSO-D-SEM</td><td>98.2 ± 0.2</td><td>97.8 ± 0.2</td><td>98.6 ± 0.2</td><td>98.2 ± 0.2</td><td>43890 / 2512</td></tr><tr><td>FR-APPSO-BiLSTM</td><td>90.8 ± 0.4</td><td>90.2 ± 0.4</td><td>89.1 ± 0.5</td><td>89.6 ± 0.4</td><td>87453 / 4783</td></tr><tr><td>HAGRU</td><td>88.9 ± 0.5</td><td>88.1 ± 0.5</td><td>86.3 ± 0.6</td><td>87.2 ± 0.5</td><td>52870 / 5347</td></tr><tr><td>Transformer-based Models</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TransfficFormer</td><td>93.6 ± 0.6</td><td>93.4 ± 0.6</td><td>93.1 ± 0.6</td><td>93.2 ± 0.6</td><td>1120 / 55</td></tr><tr><td>FT-Transformer</td><td>94.8 ± 0.4</td><td>94.5 ± 0.4</td><td>94.7 ± 0.5</td><td>94.6 ± 0.4</td><td>1190 / 51</td></tr><tr><td>TransTraffic</td><td>95.2 ± 0.3</td><td>95.0 ± 0.3</td><td>95.1 ± 0.4</td><td>95.0 ± 0.3</td><td>1290 / 58</td></tr><tr><td>MalDetectFormer</td><td>94.9 ± 0.3</td><td>94.7 ± 0.4</td><td>94.8 ± 0.3</td><td>94.7 ± 0.3</td><td>1355 / 60</td></tr><tr><td>GAN-based IDS</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GAN</td><td>84.3 ± 0.4</td><td>82.9 ± 0.5</td><td>81.4 ± 0.5</td><td>82.1 ± 0.5</td><td>7211 / 1453</td></tr><tr><td>DCGAN</td><td>85.4 ± 0.5</td><td>84.1 ± 0.5</td><td>82.6 ± 0.5</td><td>83.4 ± 0.5</td><td>35601 / 4690</td></tr><tr><td>LSGAN</td><td>86.5 ± 0.5</td><td>85.2 ± 0.5</td><td>83.9 ± 0.5</td><td>84.5 ± 0.5</td><td>41879 / 2617</td></tr><tr><td>WGAN</td><td>92.9 ± 0.3</td><td>92.1 ± 0.3</td><td>91.3 ± 0.3</td><td>91.7 ± 0.3</td><td>44302 / 2739</td></tr><tr><td>SGAN-IDS</td><td>94.0 ± 0.3</td><td>93.0 ± 0.3</td><td>91.7 ± 0.4</td><td>92.4 ± 0.3</td><td>46213 / 3925</td></tr><tr><td>SYN-GAN</td><td>91.9 ± 0.4</td><td>90.7 ± 0.5</td><td>88.8 ± 0.5</td><td>89.7 ± 0.5</td><td>46002 / 5375</td></tr><tr><td>IGAN-IDS</td><td>90.7 ± 0.5</td><td>89.2 ± 0.5</td><td>87.5 ± 0.6</td><td>88.3 ± 0.5</td><td>33791 / 1802</td></tr><tr><td>IDSGAN</td><td>89.8 ± 0.5</td><td>88.4 ± 0.5</td><td>86.3 ± 0.6</td><td>87.3 ± 0.5</td><td>7445 / 901</td></tr><tr><td>FenceGAN</td><td>85.8 ± 0.5</td><td>84.9 ± 0.5</td><td>82.9 ± 0.6</td><td>83.9 ± 0.5</td><td>8724 / 1311</td></tr><tr><td>BigGAN</td><td>94.1 ± 0.4</td><td>93.6 ± 0.4</td><td>93.4 ± 0.4</td><td>93.5 ± 0.4</td><td>50810 / 3260</td></tr><tr><td>WGAN-GP</td><td>94.7 ± 0.4</td><td>94.2 ± 0.4</td><td>94.3 ± 0.4</td><td>94.2 ± 0.4</td><td>52110 / 3052</td></tr><tr><td>TIPSO-GAN (ours)</td><td>99.6 ± 0.1</td><td>98.9 ± 0.1</td><td>99.1 ± 0.1</td><td>98.9 ± 0.1</td><td>6733 / 429</td></tr></table>

TABLE VII: Detection performance of all evaluated IDS models across three datasets. Red = best; Blue = second best.

<table><tr><td>Dataset</td><td>Model</td><td>Acc.</td><td>Prec.</td><td>Rec.</td><td>F1</td><td>Train / Test (s)</td></tr><tr><td rowspan="26">CIC-DDoS2019</td><td>Non-GAN Baselines</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Logistic Regression (calibrated)</td><td>88.9 ± 0.6</td><td>88.2 ± 0.6</td><td>87.6 ± 0.7</td><td>87.9 ± 0.6</td><td>38 / 6</td></tr><tr><td>XGBoost (class weighted)</td><td>93.8 ± 0.5</td><td>93.3 ± 0.5</td><td>93.5 ± 0.4</td><td>93.4 ± 0.5</td><td>219 / 9</td></tr><tr><td>LightGBM (class weighted)</td><td>94.6 ± 0.4</td><td>94.3 ± 0.4</td><td>94.4 ± 0.4</td><td>94.4 ± 0.4</td><td>191 / 8</td></tr><tr><td>IDS-INT</td><td>87.4 ± 0.5</td><td>86.0 ± 0.5</td><td>84.5 ± 0.6</td><td>85.3 ± 0.5</td><td>25110 / 2481</td></tr><tr><td>PSO-D-SEM</td><td>97.7 ± 0.2</td><td>97.2 ± 0.2</td><td>98.2 ± 0.2</td><td>97.7 ± 0.2</td><td>42890 / 2410</td></tr><tr><td>FR-APPSO-BiLSTM</td><td>89.9 ± 0.4</td><td>89.2 ± 0.4</td><td>88.0 ± 0.5</td><td>88.6 ± 0.4</td><td>85400 / 4633</td></tr><tr><td>HAGRU</td><td>87.7 ± 0.5</td><td>86.9 ± 0.5</td><td>85.0 ± 0.6</td><td>85.9 ± 0.5</td><td>51402 / 5180</td></tr><tr><td>Transformer-based Models</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TransfficFormer</td><td>92.7 ± 0.6</td><td>92.3 ± 0.6</td><td>92.0 ± 0.7</td><td>92.2 ± 0.6</td><td>1085 / 51</td></tr><tr><td>FT-Transformer</td><td>94.0 ± 0.5</td><td>93.7 ± 0.5</td><td>93.8 ± 0.5</td><td>93.8 ± 0.5</td><td>1165 / 52</td></tr><tr><td>TransTraffic</td><td>94.8 ± 0.4</td><td>94.6 ± 0.4</td><td>94.7 ± 0.4</td><td>94.6 ± 0.4</td><td>1278 / 59</td></tr><tr><td>MalDetectFormer</td><td>94.5 ± 0.4</td><td>94.2 ± 0.4</td><td>94.3 ± 0.4</td><td>94.3 ± 0.4</td><td>1342 / 61</td></tr><tr><td>GAN-based IDS</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GAN</td><td>83.1 ± 0.5</td><td>81.5 ± 0.5</td><td>79.9 ± 0.5</td><td>80.7 ± 0.5</td><td>6984 / 1360</td></tr><tr><td>DCGAN</td><td>84.5 ± 0.5</td><td>83.1 ± 0.5</td><td>81.1 ± 0.5</td><td>82.1 ± 0.5</td><td>34011 / 4445</td></tr><tr><td>LSGAN</td><td>85.8 ± 0.4</td><td>84.5 ± 0.5</td><td>82.2 ± 0.5</td><td>83.3 ± 0.5</td><td>40955 / 2493</td></tr><tr><td>WGAN</td><td>91.7 ± 0.3</td><td>90.9 ± 0.3</td><td>90.0 ± 0.3</td><td>90.5 ± 0.3</td><td>43233 / 2609</td></tr><tr><td>SGAN-IDS</td><td>93.4 ± 0.3</td><td>92.5 ± 0.3</td><td>91.1 ± 0.4</td><td>91.8 ± 0.3</td><td>44730 / 3752</td></tr><tr><td>SYN-GAN</td><td>90.4 ± 0.4</td><td>89.3 ± 0.4</td><td>87.9 ± 0.5</td><td>88.6 ± 0.4</td><td>44500 / 5213</td></tr><tr><td>IGAN-IDS</td><td>89.2 ± 0.5</td><td>88.2 ± 0.5</td><td>86.4 ± 0.5</td><td>87.3 ± 0.5</td><td>32790 / 1693</td></tr><tr><td>IDSGAN</td><td>88.2 ± 0.5</td><td>87.0 ± 0.5</td><td>85.2 ± 0.6</td><td>86.1 ± 0.5</td><td>7105 / 870</td></tr><tr><td>FenceGAN</td><td>84.9 ± 0.4</td><td>84.0 ± 0.5</td><td>81.9 ± 0.5</td><td>83.0 ± 0.5</td><td>8381 / 1225</td></tr><tr><td>BigGAN</td><td>93.9 ± 0.4</td><td>93.4 ± 0.4</td><td>93.3 ± 0.4</td><td>93.4 ± 0.4</td><td>49650 / 3150</td></tr><tr><td>WGAN-GP</td><td>94.1 ± 0.4</td><td>93.7 ± 0.4</td><td>93.9 ± 0.4</td><td>93.8 ± 0.4</td><td>50500 / 2990</td></tr><tr><td>TIPSO-GAN (ours)</td><td>99.5 ± 0.1</td><td>98.8 ± 0.1</td><td>99.0 ± 0.1</td><td>98.7 ± 0.1</td><td>6611 / 410</td></tr></table>

TABLE VIII: Generalization performance of TIPSO-GAN under strict zero-day evaluations. Left: leave-one-family-out (LOFO) on CIC-IDS2018. Right: cross-dataset evaluation where the model is trained on one corpus and tested on another. All values are mean ± std over five seeds.

<table><tr><td colspan="5">LOFO on CIC-IDS2018 (per-family)</td><td colspan="5">Cross-Dataset Evaluation (Train → Test)</td></tr><tr><td>Held-out Family</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1</td><td>Train → Test</td><td>Accuracy</td><td>Precision</td><td>Recall</td><td>F1</td></tr><tr><td>DoS</td><td>91.5 ± 0.7</td><td>90.2 ± 0.8</td><td>92.7 ± 0.7</td><td>91.4 ± 0.7</td><td>CIC-IDS2018 → CIC-DDoS2019</td><td>82.4 ± 0.8</td><td>80.9 ± 0.9</td><td>83.1 ± 0.8</td><td>81.9 ± 0.8</td></tr><tr><td>Brute Force</td><td>93.8 ± 0.6</td><td>92.6 ± 0.6</td><td>94.2 ± 0.6</td><td>93.4 ± 0.6</td><td>CIC-IDS2018 → CICAPT-IIoT2024</td><td>80.6 ± 0.9</td><td>79.3 ± 1.0</td><td>81.0 ± 0.9</td><td>80.1 ± 0.9</td></tr><tr><td>Botnet</td><td>92.1 ± 0.7</td><td>91.0 ± 0.8</td><td>92.9 ± 0.7</td><td>91.9 ± 0.7</td><td>CIC-DDoS2019 → CIC-IDS2018</td><td>83.1 ± 0.7</td><td>81.5 ± 0.8</td><td>84.2 ± 0.8</td><td>82.8 ± 0.7</td></tr><tr><td>Infiltration</td><td>90.6 ± 0.8</td><td>89.2 ± 0.9</td><td>91.7 ± 0.8</td><td>90.4 ± 0.8</td><td>CIC-DDoS2019 → CICAPT-IIoT2024</td><td>81.2 ± 0.8</td><td>80.0 ± 0.9</td><td>82.1 ± 0.8</td><td>81.0 ± 0.8</td></tr><tr><td>Web Attacks</td><td>94.3 ± 0.6</td><td>93.0 ± 0.6</td><td>94.9 ± 0.6</td><td>93.9 ± 0.6</td><td>CICAPT-IIoT2024 → CIC-IDS2018</td><td>79.8 ± 0.9</td><td>78.5 ± 1.0</td><td>80.3 ± 0.9</td><td>79.4 ± 0.9</td></tr><tr><td>Heartbleed</td><td>93.0 ± 0.7</td><td>91.9 ± 0.7</td><td>93.8 ± 0.7</td><td>92.8 ± 0.7</td><td>CICAPT-IIoT2024 → CIC-DDoS2019</td><td>80.2 ± 0.8</td><td>78.9 ± 0.9</td><td>81.1 ± 0.9</td><td>80.0 ± 0.8</td></tr><tr><td>Mean across families</td><td>92.6 ± 0.6</td><td>91.7 ± 0.7</td><td>93.4 ± 0.6</td><td>92.3 ± 0.6</td><td colspan="5">-</td></tr></table>

TABLE X: Runtime performance comparison.

TABLE IX: Computational complexity and resource usage of representative IDS models. E = epochs, N = samples, d = feature dimension, L = layers, P = swarm size, I = iterations. FLOPs are estimated per inference.

<table><tr><td>Model</td><td>Training Complexity</td><td>Inference Complexity</td><td>Memory (GB)</td><td>FLOPs/flow</td></tr><tr><td>Logistic Regression</td><td> $O(E \cdot N \cdot d)$ </td><td> $O(d)$ </td><td> $< 0.5$ </td><td> $10^{5}$ </td></tr><tr><td>XGBoost (weighted)</td><td> $O(E \cdot N \cdot d \log N)$ </td><td> $O(d \log N)$ </td><td> $0.5$ </td><td> $10^{6}$ </td></tr><tr><td>BiLSTM (FR-APPSO)</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d \cdot L)$ </td><td> $2.4$ </td><td> $10^{7}$ </td></tr><tr><td>HAGRU</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d \cdot L)$ </td><td> $2.1$ </td><td> $10^{7}$ </td></tr><tr><td>TransfficFormer</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d^{2} \cdot L)$ </td><td> $3.0$ </td><td> $10^{8}$ </td></tr><tr><td>MalDetectFormer</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d^{2} \cdot L)$ </td><td> $3.5$ </td><td> $10^{8}$ </td></tr><tr><td>WGAN-GP</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d \cdot L)$ </td><td> $2.4$ </td><td> $10^{7}$ </td></tr><tr><td>FenceGAN</td><td> $O(E \cdot N \cdot d \cdot L)$ </td><td> $O(d \cdot L)$ </td><td> $2.0$ </td><td> $10^{7}$ </td></tr><tr><td>TIPSO-GAN</td><td> $O(E \cdot N \cdot d \cdot L + P \cdot I \cdot d)$ </td><td> $O(d \cdot L + a^{2})$ </td><td> $2.1$ </td><td> $10^{7}$ </td></tr></table>

<table><tr><td>Model</td><td>Train (GPU h)</td><td>Latency (ms)</td><td>Throughput</td><td>Mem (GB)</td><td>Power (W)</td></tr><tr><td>Logistic Regression</td><td>0.1</td><td>0.05</td><td>20,000</td><td>0.2</td><td>20</td></tr><tr><td>XGBoost (weighted)</td><td>0.3</td><td>0.20</td><td>5,000</td><td>0.5</td><td>40</td></tr><tr><td>LightGBM (weighted)</td><td>0.2</td><td>0.18</td><td>5,500</td><td>0.5</td><td>35</td></tr><tr><td>IDS-INT</td><td>6</td><td>0.80</td><td>1,250</td><td>1.2</td><td>70</td></tr><tr><td>PSO-D-SEM</td><td>10</td><td>1.10</td><td>900</td><td>2.0</td><td>100</td></tr><tr><td>FR-APPSO-BiLSTM</td><td>12</td><td>1.20</td><td>830</td><td>2.4</td><td>110</td></tr><tr><td>HAGRU</td><td>8</td><td>0.95</td><td>1,050</td><td>2.1</td><td>95</td></tr><tr><td>TransfficFormer</td><td>18</td><td>0.60</td><td>1,650</td><td>3.0</td><td>140</td></tr><tr><td>FT-Transformer</td><td>20</td><td>0.65</td><td>1,540</td><td>3.2</td><td>145</td></tr><tr><td>MalDetectFormer</td><td>24</td><td>0.72</td><td>1,390</td><td>3.5</td><td>160</td></tr><tr><td>GAN</td><td>4</td><td>0.35</td><td>2,850</td><td>1.5</td><td>120</td></tr><tr><td>WGAN</td><td>6</td><td>0.38</td><td>2,630</td><td>2.0</td><td>140</td></tr><tr><td>SGAN-IDS</td><td>8</td><td>0.51</td><td>1,960</td><td>1.8</td><td>140</td></tr><tr><td>WGAN-GP</td><td>9</td><td>0.48</td><td>2,080</td><td>2.4</td><td>150</td></tr><tr><td>TIPSO-GAN</td><td>14</td><td>0.42</td><td>2,400</td><td>2.1</td><td>150</td></tr></table>

TABLE XI: TIPSO-GAN runtime on increasing data sizes.

<table><tr><td>Data size (flows)</td><td>Thrpt (flows/s)</td><td>P50 (ms)</td><td>P90 (ms)</td><td>P99 (ms)</td><td>Mem (GB)</td><td>Power (W)</td></tr><tr><td> $1 \times 10^{4}$ </td><td>2420</td><td>0.17</td><td>0.27</td><td>0.40</td><td>2.0</td><td>148</td></tr><tr><td> $5 \times 10^{4}$ </td><td>2410</td><td>0.18</td><td>0.28</td><td>0.41</td><td>2.0</td><td>149</td></tr><tr><td> $1 \times 10^{5}$ </td><td>2400</td><td>0.18</td><td>0.29</td><td>0.42</td><td>2.1</td><td>150</td></tr><tr><td> $5 \times 10^{5}$ </td><td>2380</td><td>0.19</td><td>0.31</td><td>0.44</td><td>2.1</td><td>152</td></tr><tr><td> $1 \times 10^{6}$ </td><td>2360</td><td>0.20</td><td>0.32</td><td>0.46</td><td>2.2</td><td>153</td></tr><tr><td> $5 \times 10^{6}$ </td><td>2340</td><td>0.21</td><td>0.34</td><td>0.48</td><td>2.2</td><td>155</td></tr><tr><td> $1 \times 10^{7}$ </td><td>2320</td><td>0.22</td><td>0.35</td><td>0.50</td><td>2.3</td><td>156</td></tr><tr><td> $5 \times 10^{7}$ </td><td>2300</td><td>0.24</td><td>0.38</td><td>0.55</td><td>2.3</td><td>158</td></tr><tr><td> $1 \times 10^{8}$ </td><td>2280</td><td>0.25</td><td>0.40</td><td>0.60</td><td>2.4</td><td>160</td></tr></table>

![](images/e3c0955d9ede4920e38fe3224882359ad0f38c61a246191369332588b5d08768.jpg)  
Fig. 8: Ablation of TIPSO-GAN components.

for training due to PSO optimization and multiple loss terms, but inference remains efficient at 0.42 ms per flow (≈ 2400 flows/s). Peak memory (2.1 GB) and power draw (150 W) are comparable to WGAN-GP. At these rates, a single GPU can sustain 10–40 Gbps traffic, and throughput scales linearly across multiple GPUs. We observe that TIPSO-GAN maintains stable throughput and sub-millisecond latency as input size grows from $1 0 ^ { 4 }$ to $1 0 ^ { 8 }$ flows; detailed results are provided in Appendix Table XI. This confirms that TIPSO-GAN scales reliably to real-world high-volume traffic settings.

1) Runtime and Scalability Analysis: Table XI summarizes the runtime behavior of TIPSO-GAN as the dataset size increases from $1 \times 1 0 ^ { 4 } \mathrm { ~ t o ~ 1 ~ } \times 1 0 ^ { 8 }$ network flows using the CICAPT-IIoT2024 dataset. The model maintains nearlinear scalability, with throughput decreasing only marginally (2420 → 2280 flows/s) as data volume grows by four orders of magnitude. Median (P50) inference latency remains below 0.25 ms even at the largest scale, while memory usage stays within 2–2.4 GB. These results demonstrate that TIPSO-GAN achieves efficient inference with modest resource growth, confirming its suitability for large-scale real-time intrusion detection deployments.

## I. Computational Complexity Analysis

Table IX reports complexity and resource usage across representative IDS models using the CICAPT-IIoT2024 dataset.

TABLE XII: Resource Utilization Across TIPSO-GAN Modules (CICAPT-IIoT2024)

<table><tr><td>Module</td><td>GPU Memory (GB)</td><td>FLOPs ( $\times 10^{7}$ )</td><td>Runtime / Epoch (s)</td><td>Latency (ms / flow)</td></tr><tr><td>Generator (G /  $G_{T}$ )</td><td>1.0</td><td>10.3</td><td>36</td><td>12.8</td></tr><tr><td>Discriminator (D /  $D_{T}$ )</td><td>0.9</td><td>9.8</td><td>34</td><td>12.4</td></tr><tr><td>DeePred (pre-trained)</td><td>1.2</td><td>10.7</td><td>39</td><td>13.1</td></tr><tr><td>PSO optimizer (train-time only)</td><td>0.3</td><td>1.2</td><td>11</td><td>-</td></tr><tr><td>Total (TIPSO-GAN)</td><td>2.1</td><td> $10^{7}$ </td><td>120</td><td>12.8</td></tr></table>

Classical ML methods (Logistic Regression, XGBoost) are linear in $d ,$ with negligible memory and FLOPs, but provide limited robustness. RNN-based IDS (BiLSTM, HAGRU) scale as $O ( d \cdot L )$ at inference, requiring 2–3 GB memory and $1 0 ^ { 7 }$ FLOPs. Transformer IDS (TransfficFormer, MalDetectFormer) incur quadratic $O ( d ^ { 2 } \cdot L )$ cost from attention, leading to the highest memory (3–3.5 GB) and $1 0 ^ { 8 }$ FLOPs. GAN baselines (WGAN-GP, FenceGAN) remain at $O ( d \cdot L )$ with moderate memory (2–2.4 GB). TIPSO-GAN introduces $O ( P \cdot I \cdot d )$ overhead during training from PSO, but maintains $O ( d { \cdot } L { + } d ^ { 2 } )$ inference cost, with 2.1 GB memory and $1 0 ^ { 7 }$ FLOPs. This shows TIPSO-GAN is heavier to train but efficient at inference, close to GAN baselines and lighter than transformer IDS.

## J. Ablation study

We performed an ablation study to quantify the contribution of each component in TIPSO-GAN (Fig. 8) using the CICAPT-IIoT2024 dataset. Removing MHSA led to the sharpest degradation, increasing FNR from 5.2% to nearly 8%. Excluding adversarial loss or focal loss also caused notable increases in error, confirming their role in stabilizing training and improving recall on rare attack classes. Transfer learning and PSO contributed moderate but consistent gains, while gradient penalty and regularization further reduced both FPR and FNR by about one point. The ablation demonstrates that the full TIPSO-GAN design yields the lowest error rates and that multiple components work synergistically to achieve robustness. As shown in Table XII, TIPSO-GAN maintains modest computational demands despite its multi-component design. Training consumes approximately 2.1 GB GPU memory and $1 0 ^ { 7 }$ FLOPs per epoch, with an average runtime of about 120 s. The PSO optimizer adds only ≈12% additional FLOPs during training, while inference latency remains 12.8 ms per flow comparable to WGAN-GP. DeePred and the discriminator account for most of the memory footprint, confirming that TIPSO-GAN delivers robust detection efficiency with limited computational overhead suitable for real-time deployment.

## VII. CONCLUSION AND FUTURE WORK

This work introduced TIPSO-GAN, a novel intrusion detection framework that redefines GAN training as a swarm optimization problem. The results demonstrate that TIPSO-GAN consistently outperforms thirteen baselines, under temporal splits and stability under strict zero-day regimes. The framework also exhibits superior calibration, robustness against adaptive adversarial attacks, and resilience to class imbalance, confirming its suitability for deployment in real-world network defense systems. The current implementation of TIPSO-GAN operates at the flow level, where each record aggregates multiple packets belonging to the same TCP or UDP session. This design captures temporal and statistical dependencies that are not observable in isolated packets and enables stable adversarial training with compact feature spaces. However, this also means TIPSO-GAN does not perform per-packet classification. Future work will investigate the integration of fine-grained packet-level embeddings with TIPSO-GAN’s adversarial optimization to enable real-time packet-wise detection without sacrificing stability. Future study could also extend TIPSO-GAN to streaming detection environments, optimize its efficiency for resource-constrained IoT deployments, and investigate cross-domain transfer to improve adaptability across heterogeneous network infrastructures.

## ACKNOWLEDGMENTS

This work was partly supported by the National Natural Science Foundation of China (NSFC) (Grant nos. 62172194, 62202206 and U1836116), the Natural Science Foundation of Jiangsu Province, China (Grant no. BK20220515), the China Postdoctoral Science Foundation, China (Grant no. 2021M691310), and Qinglan Project of Jiangsu Province, China.

## REFERENCES

[1] I. Cvitic, D. Perakovic, B. B. Gupta, and K.-K. R. Choo, “Boosting-´ based ddos detection in internet of things systems,” IEEE Internet of Things Journal, vol. 9, no. 3, pp. 2109–2123, 2022.

[2] J. Yang, X. Jiang, G. Liang, S. Li, and Z. Ma, “Malicious traffic identification with self-supervised contrastive learning,” Sensors, vol. 23, 8 2023.

[3] L. D. Manocchio, S. Layeghy, W. W. Lo, G. K. Kulatilleke, M. Sarhan, and M. Portmann, “Flowtransformer: A transformer framework for flow-based network intrusion detection systems,” Expert Systems with Applications, vol. 241, p. 122564, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S095741742303066X

[4] Y. Gorishniy, I. Rubachev, V. Khrulkov, and A. Babenko, “Revisiting deep learning models for tabular data,” in Proceedings of the 35th International Conference on Neural Information Processing Systems, ser. NIPS ’21. Red Hook, NY, USA: Curran Associates Inc., 2021.

[5] S. Zhang, Y. Fan, H. Zhou, and B. Li, “Maldetectformer: leveraging sparse spatiotemporal information for effective malicious traffic detection,” in Proceedings of the Thirty-Ninth AAAI Conference on Artificial Intelligence and Thirty-Seventh Conference on Innovative Applications of Artificial Intelligence and Fifteenth Symposium on Educational Advances in Artificial Intelligence, ser. AAAI’25/IAAI’25/EAAI’25. AAAI Press, 2025. [Online]. Available: https://doi.org/10.1609/aaai.v39i21.34411

[6] C. Kang, J. Yoon, D. Choi, E. Park, S. Pack, and J. Han, “Transtraffic: Predicting network traffic using low resource data,” in 2022 13th International Conference on Information and Communication Technology Convergence (ICTC), 2022, pp. 786–788.

[7] I. J. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio, “Generative adversarial networks,” Advances in Neural Information Processing Systems 27 (NIPS 2014), 6 2014. [Online]. Available: http://arxiv.org/abs/1406.2661

[8] Z. Moti, S. Hashemi, H. Karimipour, A. Dehghantanha, A. N. Jahromi, L. Abdi, and F. Alavi, “Generative adversarial network to detect unseen internet of things malware,” Ad Hoc Networks, vol. 122, p. 102591, 2021. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S1570870521001281

[9] H. D. Menendez, S. Bhattacharya, D. Clark, and E. T. Barr, “The´ arms race: Adversarial search defeats entropy used to detect malware,” Expert Systems with Applications, vol. 118, pp. 246–260, 2019. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0957417418306535

[10] W. Qian, H. Li, and H. Mu, “Circular lbp prior-based enhanced gan for image style transfer,” Int. J. Semant. Web Inf. Syst., vol. 18, no. 2, p. 1–15, Dec. 2022. [Online]. Available: https: //doi.org/10.4018/IJSWIS.315601

[11] X. Zhang, J. Wang, and S. Zhu, “Dual generative adversarial networks based unknown encryption ransomware attack detection,” IEEE Access, vol. 10, pp. 900–913, 2022.

[12] Z. Zhou, Y. Li, J. Li, K. Yu, G. Kou, M. Wang, and B. B. Gupta, “Gan-siamese network for cross-domain vehicle re-identification in intelligent transport systems,” IEEE Transactions on Network Science and Engineering, vol. 10, no. 5, pp. 2779–2790, 2023.

[13] A. Dunmore, J. Jang-Jaccard, F. Sabrina, and J. Kwak, “A comprehensive survey of generative adversarial networks (gans) in cybersecurity intrusion detection,” IEEE Access, vol. 11, pp. 76 071–76 094, 2023.

[14] M. Arjovsky, S. Chintala, and L. Bottou, “Wasserstein generative adversarial networks,” in Proceedings of the 34th International Conference on Machine Learning, ser. Proceedings of Machine Learning Research, D. Precup and Y. W. Teh, Eds., vol. 70. PMLR, 06–11 Aug 2017, pp. 214–223. [Online]. Available: https: //proceedings.mlr.press/v70/arjovsky17a.html

[15] X. Mao, Q. Li, H. Xie, R. Y. K. Lau, Z. Wang, and S. P. Smolley, “Least squares generative adversarial networks,” 2017 IEEE International Conference on Computer Vision (ICCV), pp. 2813–2821, 2016. [Online]. Available: https://api.semanticscholar.org/CorpusID:206771128

[16] G. Dlamini and M. Fahim, “Dgm: a data generative model to improve minority class presence in anomaly detection domain,” Neural Computing and Applications, vol. 33, pp. 13 635–13 646, 10 2021.

[17] R. Chapaneri and S. Shah, “Enhanced detection of imbalanced malicious network traffic with regularized generative adversarial networks,” Journal of Network and Computer Applications, vol. 202, 6 2022.

[18] S. Das, “Fgan: Federated generative adversarial networks for anomaly detection in network traffic,” 2022.

[19] X. Liu and J. Liu, “Malicious traffic detection combined deep neural network with hierarchical attention mechanism,” Scientific Reports, vol. 11, no. 1, p. 12363, 2021.

[20] B.-E. Zolbayar, R. Sheatsley, P. McDaniel, M. J. Weisman, S. Zhu, S. Zhu, and S. Krishnamurthy, “Generating practical adversarial network traffic flows using nidsgan,” 2022.

[21] B. Babayigit and M. Abubaker, “Towards a generalized hybrid deep learning model with optimized hyperparameters for malicious traffic detection in the industrial internet of things,” Engineering Applications of Artificial Intelligence, vol. 128, p. 107515, 2 2024.

[22] M. Fathallah, M. Sakr, and S. Eletriby, “Stabilizing and improving training of generative adversarial networks through identity blocks and modified loss function,” IEEE Access, vol. 11, pp. 43 276–43 285, 2023.

[23] Q. Yuan, G. Gou, Y. Zhu, Y. Zhu, G. Xiong, and Y. Wang, “Mcre: A unified framework for handling malicious traffic with noise labels based on multidimensional constraint representation,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 133–147, 2024.

[24] A. Radford, L. Metz, and S. Chintala, “Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks,” arXiv e-prints, p. arXiv:1511.06434, Nov. 2015.

[25] S. Das, A. Abraham, and A. Konar, “Swarm intelligence algorithms in bioinformatics,” in Computational Intelligence in Bioinformatics. Springer, 2008, pp. 113–147.

[26] J. Kennedy and R. Eberhart, “Particle swarm optimization,” 1995, pp. 1942–1948.

[27] E. K. Boahen, B. E. Bouya-Moko, and C. Wang, “Network anomaly detection in a controlled environment based on an enhanced psogsarfc,” Computers and Security, vol. 104, 5 2021.

[28] S. Choudhary, S. Sugumaran, A. Belazi, and A. A. A. El-Latif, “Linearly decreasing inertia weight pso and improved weight factor-based clustering algorithm for wireless sensor networks,” Journal of Ambient Intelligence and Humanized Computing, pp. 1–19, 2023.

[29] M. A. K. Raiaan, S. Sakib, N. M. Fahad, A. A. Mamun, M. A. Rahman, S. Shatabda, and M. S. H. Mukta, “A systematic review of hyperparameter optimization techniques in convolutional neural networks,” Decision Analytics Journal, vol. 11, p. 100470, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S2772662224000742

[30] L. Zhang and L. Zhao, “High-quality face image generation using particle swarm optimization-based generative adversarial networks,” Future Generation Computer Systems, vol. 122, pp. 98–104, 2021.

[Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0167739X21001126

[31] H. N. Nguyen, T. Lan-Phan, and C.-J. Song, “Generative adversarial network-based network intrusion detection system for supervisory control and data acquisition system,” in 2024 IEEE International Conference on Consumer Electronics-Asia (ICCE-Asia), Nov 2024, pp. 1–3.

[32] T. K. Boppana and P. Bagade, “Gan-ae: An unsupervised intrusion detection system for mqtt networks,” Engineering Applications of Artificial Intelligence, vol. 119, p. 105805, 2023. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S0952197622007953

[33] L. Zhang and L. Zhao, “High-quality face image generation using particle swarm optimization-based generative adversarial networks,” Future Generation Computer Systems, vol. 122, pp. 98–104, 2021. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0167739X21001126

[34] L. Tian, Z. Wang, W. Liu, Y. Cheng, F. E. Alsaadi, and X. Liu, “Empower parameterized generative adversarial networks using a novel particle swarm optimizer: algorithms and applications,” International Journal of Machine Learning and Cybernetics, vol. 13, pp. 1145–1155, 4 2022.

[35] R. Shameli and S. Rajkumar, “High-speed threat detection in 5g sdn with particle swarm optimizer integrated gru-driven generative adversarial network,” Scientific Reports, vol. 15, no. 1, p. 10025, 2025. [Online]. Available: https://doi.org/10.1038/s41598-025-95011-z

[36] A. Toure, Y. Imine, A. Semnont, T. Delot, and A. Gallais,´ “A framework for detecting zero-day exploits in network flows,” Computer Networks, vol. 248, p. 110476, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1389128624003086

[37] M. Poongodi and M. Hamdi, “Intrusion detection system using distributed multilevel discriminator in gan for iot system,” Transactions on Emerging Telecommunications Technologies, vol. 34, no. 11, p. e4815, 2023. [Online]. Available: https://onlinelibrary.wiley.com/doi/ abs/10.1002/ett.4815

[38] E. Seo, H. M. Song, and H. K. Kim, “Gids: Gan based intrusion detection system for in-vehicle network,” in 2018 16th Annual Conference on Privacy, Security and Trust (PST), Aug 2018, pp. 1–6.

[39] S. Rahman, S. Pal, S. Mittal, T. Chawla, and C. Karmakar, “Syn-gan: A robust intrusion detection system using gan-based synthetic data for iot security,” Internet of Things, vol. 26, p. 101212, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S2542660524001537

[40] S. Aldhaheri and A. Alhuzali, “Sgan-ids: Self-attention-based generative adversarial network against intrusion detection systems,” Sensors, vol. 23, no. 18, 2023. [Online]. Available: https://www.mdpi.com/ 1424-8220/23/18/7796

[41] A.-G. Mari, D. Zinca, and V. Dobrota, “Development of a machinelearning intrusion detection system and testing of its performance using a generative adversarial network,” Sensors, vol. 23, no. 3, 2023. [Online]. Available: https://www.mdpi.com/1424-8220/23/3/1315

[42] M. Roopak, S. Parkinson, G. Y. Tian, Y. Ran, S. Khan, and B. Chandrasekaran, “An unsupervised approach for the detection of zeroday distributed denial of service attacks in internet of things networks,” IET Networks, vol. 13, no. 5-6, pp. 513–527, 2024. [Online]. Available: https://ietresearch.onlinelibrary.wiley.com/doi/abs/10.1049/ntw2.12134

[43] M. Sarhan, S. Layeghy, M. Gallagher, and M. Portmann, “From zero-shot machine learning to zero-day attack detection,” International Journal of Information Security, vol. 22, no. 4, pp. 947–959, 2023. [Online]. Available: https://doi.org/10.1007/s10207-023-00676-0

[44] R. Huang, L. Ma, J. He, and X. Chu, “T-gan: A deep learning framework for prediction of temporal complex networks with adaptive graph convolution and attention mechanism,” Displays, vol. 68, p. 102023, 2021. [Online]. Available: https://www.sciencedirect.com/ science/article/pii/S0141938221000366

[45] S. Tuli, G. Casale, and N. R. Jennings, “Tranad: deep transformer networks for anomaly detection in multivariate time series data,” Proc. VLDB Endow., vol. 15, no. 6, p. 1201–1214, Feb. 2022. [Online]. Available: https://doi.org/10.14778/3514061.3514067

[46] W. Du, J. Xue, X. Yang, W. Guo, D. Gu, and W. Han, “Transfficformer: A novel transformer-based framework to generate evasive malicious traffic,” Knowledge-Based Systems, vol. 319, p. 113546, 2025. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S0950705125005921

[47] I. Sharafaldin, A. H. Lashkari, and A. A. Ghorbani, “Toward generating a new intrusion detection dataset and intrusion traffic characterization,” in

International Conference on Information Systems Security and Privacy, 2018. [Online]. Available: https://api.semanticscholar.org/CorpusID: 4707749

[48] E. Ghiasvand, S. Ray, S. Iqbal, S. Dadkhah, and A. A. Ghorbani, “Cicapt-iiot: A provenance-based apt attack dataset for iiot environment,” 2024. [Online]. Available: https://arxiv.org/abs/2407.11278

[49] I. Gulrajani, F. Ahmed, M. Arjovsky, V. Dumoulin, and A. Courville, “Improved Training of Wasserstein GANs,” arXiv e-prints, p. arXiv:1704.00028, Mar. 2017.

[50] Z. Lin, Y. Shi, and Z. Xue, “Idsgan: Generative adversarial networks for nbsp;attack generation against intrusion detection,” in Advances in Knowledge Discovery and Data Mining: 26th Pacific-Asia Conference, PAKDD 2022, Chengdu, China, May 16–19, 2022, Proceedings, Part III. Berlin, Heidelberg: Springer-Verlag, 2022, p. 79–91. [Online]. Available: https://doi.org/10.1007/978-3-031-05981-0 7

[51] S. Huang and K. Lei, “Igan-ids: An imbalanced generative adversarial network towards intrusion detection system in ad-hoc networks,” Ad Hoc Networks, vol. 105, p. 102177, 2020. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S1570870519311035

[52] S. Rahman, S. Pal, S. Mittal, T. Chawla, and C. Karmakar, “Syn-gan: A robust intrusion detection system using gan-based synthetic data for iot security,” Internet of Things, vol. 26, p. 101212, 2024. [Online]. Available: https://www.sciencedirect.com/science/article/pii/ S2542660524001537

[53] J. Donahue and K. Simonyan, Large scale adversarial representation learning. Red Hook, NY, USA: Curran Associates Inc., 2019.

[54] L. Niu, Z. Li, and S. Li, “Mmd fence gan unsupervised anomaly detection model based on maximum mean discrepancy,” Int. J. Cogn. Inform. Nat. Intell., vol. 18, no. 1, p. 1–13, jun 2024. [Online]. Available: https://doi.org/10.4018/IJCINI.344813

[55] F. Ullah, S. Ullah, G. Srivastava, and J. C.-W. Lin, “Ids-int: Intrusion detection system using transformer-based transfer learning for imbalanced network traffic,” Digital Communications and Networks, 3 2023.

[56] F. Rustam and A. D. Jurcut, “Malicious traffic detection in multienvironment networks using novel s-date and pso-d-sem approaches,” Computers and Security, vol. 136, 1 2024.

[57] H. Jiang, S. Ji, G. He, and X. Li, “Network traffic anomaly detection model based on feature reduction and bidirectional lstm neural network optimization,” Scientific Programming, vol. 2023, pp. 1–18, 11 2023.

[58] S. Liu, F. Peng, and K. Tang, “Reliable robustness evaluation via automatically constructed attack ensembles,” in Proceedings of the Thirty-Seventh AAAI Conference on Artificial Intelligence and Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence and Thirteenth Symposium on Educational Advances in Artificial Intelligence, ser. AAAI’23/IAAI’23/EAAI’23. AAAI Press, 2023. [Online]. Available: https://doi.org/10.1609/aaai.v37i7.26064

[59] C. Liu, C. Lou, M. Yu, S. Yiu, K. Chow, G. Li, J. Jiang, and W. Huang, “A novel adversarial example detection method for malicious pdfs using multiple mutated classifiers,” Forensic Science International: Digital Investigation, vol. 38, p. 301124, 2021. [Online]. Available: https://www.sciencedirect.com/science/article/pii/S2666281721000226

[60] A. Chernikova and A. Oprea, “Fence: Feasible evasion attacks on neural networks in constrained environments,” ACM Trans. Priv. Secur., vol. 25, no. 4, Jul. 2022. [Online]. Available: https://doi.org/10.1145/3544746

[61] K. G. Shreeharsha, C. G. Korde, M. H. Vasantha, and Y. B. N. Kumar, “Training of generative adversarial networks using particle swarm optimization algorithm.” Institute of Electrical and Electronics Engineers Inc., 2021, pp. 127–130.

[62] X.-L. Li, R. Serra, and O. Julien, “Effects of the Particle Swarm Optimization parameters for structural dynamic monitoring of cantilever beam,” in Surveillance, Vishno and AVE conferences. Lyon, France: INSA-Lyon, Universite de Lyon, Jul. 2019. [Online]. Available:´ https://hal.science/hal-02188562

## APPENDIX A ADDITIONAL EXPERIMENTAL RESULTS

## A. Experiment on the improved particle swarm inertia weight

The performance of five inertia weight strategies was assessed using a hybrid sinc–exponential test function (Eq. 15-

![](images/64d72cfd976dd4efd1c1eeffe90bc1e8b8d4ac9c3b68a666875dc2983b51e274.jpg)  
(a) GAN

![](images/70195733e989200e98b93a2b72d08b97097082072b96d35763fd44ca36b10d1b.jpg)  
(b) DCGAN

![](images/009addb7f1862a8e3e2e94016a5db4fbb6c6448bc90092b7e5fcd2061b881ab4.jpg)  
(c) BigGAN

![](images/6aa17deb69df4b540edad86b8e45a18eaf7ecf97af77326b6ce3a3234183a30a.jpg)  
(d) WGAN-GP

![](images/a93bbf7f1bffe41c1abf6dd8e0bf9d8a7135fc8ed70574ab5ed497fc1970c8cd.jpg)  
(e) SGAN-IDS

![](images/72176cb3b6ba2c2d47d42cfbc0f0c08c7e28fd08acb4ad1d2c1e4ab0dc536df1.jpg)  
(f) TIPSO-GAN  
Fig. 9: Reliability diagrams on CICAPT-IIoT2024 with shaded miscalibration area. The orange dashed line denotes perfect calibration, and the blue curve shows the model’s reliability. Legends report ECE and Brier scores, confirming that TIPSO-GAN achieves the best calibration.

2.71289), with results in Table XIII.

$$
f (x, y) = \frac {\sin (\sqrt {x ^ {2} + y ^ {2}})}{\sqrt {x ^ {2} + y ^ {2}}} + \exp \biggl (\frac {\cos (2 \pi x) + \cos (2 \pi y)}{2} \biggr)\tag{15}
$$

The proposed adaptive sigmoidal strategy achieved the best mean value (1.2183), finding all 50 global optima with no local minima. Its dynamic inertia control balanced exploration and exploitation more effectively than the fixed $\left( \omega _ { 0 } \right)$ or decreasing $\left( \omega _ { 1 } \mathrm { - } \omega _ { 3 } \right)$ schemes. Fixed and linearly decreasing weights produced lower averages (0.90–0.93) and frequent local optima, while quadratic and exponential variants (0.81–0.79) overexploited early, reducing diversity. Figure 10 confirms that adaptive weighting preserved population diversity and avoided premature convergence.

TABLE XIII: The comparative performance on different inertia weights using the customized test function.

<table><tr><td>Author/Method</td><td>Average Value</td><td># of Local Optima</td><td># of Global Optima</td></tr><tr><td>[26] Conventional</td><td>0.9028</td><td>10</td><td>40</td></tr><tr><td>[28] Linear</td><td>0.9305</td><td>8</td><td>42</td></tr><tr><td>[30] Quadratic</td><td>0.8052</td><td>9</td><td>48</td></tr><tr><td>[61] Constant</td><td>0.7864</td><td>6</td><td>44</td></tr><tr><td>[30] Exponential</td><td>0.8136</td><td>6</td><td>44</td></tr><tr><td>Adaptive Sigmoidal</td><td>1.2183</td><td>0</td><td>50</td></tr></table>

The results indicate the importance of maintaining diversity in the particle swarm, as it allows the algorithm to explore the complex landscape more thoroughly and avoid being trapped in suboptimal regions.

![](images/9f56a3a5af4929bb57690de6041ad53d0c4ca981695ea2554d67c7a4637590fe.jpg)  
Fig. 10: The graph of test function f(x).

TABLE XIV: Experimental Environment Summary.

<table><tr><td>Category</td><td>Specification</td></tr><tr><td>Processor</td><td>Intel Core i7 (8 cores, 3.6 GHz)</td></tr><tr><td>Memory</td><td>64 GB RAM</td></tr><tr><td>GPU</td><td>NVIDIA GTX 1080 Ti (11 GB VRAM)</td></tr><tr><td>Operating System</td><td>Windows 10 / Ubuntu 22.04</td></tr><tr><td>Python Version</td><td>3.10 (Anaconda)</td></tr><tr><td>Deep Learning Framework</td><td>TensorFlow 2.15.0</td></tr><tr><td>ML Utilities</td><td>Scikit-learn 1.3, NumPy, Pandas</td></tr></table>

## B. Detailed experimental settings and parameters

TIPSO-GAN employs a two-phase optimization: PSO-based initialization followed by Adam fine-tuning. The PSO stage uses 100 particles $( c _ { 1 } = c _ { 2 } = 2 . 0 5 , w _ { \mathrm { m i n } } = 0 . 4 , w _ { \mathrm { m a x } } = 0 . 9 )$ optimizing the GAN loss for 1000 iterations with adaptive inertia control [62]. The global best solution initializes the generator before Adam refinement. Training stops when validation accuracy falls below or exceeds 99.95% for three epochs, balancing convergence and overfitting. Hyperparameters (Table XV) follow prior work with validation tuning. Sensitivity tests varying MHSA heads (2–8), focal loss $\gamma \ \left( 0 { - } 3 \right)$ , and attention decay (0.90–0.98) confirmed stable accuracy and low false negatives (Fig. 11), demonstrating robustness and reproducibility across configurations.

![](images/9146b128e7734ab43754022d199b9082a38ee7e95868c3dc8d051a405fd923d8.jpg)

![](images/37144fc5fd038046de38683de6037145d149a099eb39cc92ec0e5659635bb69e.jpg)  
Focal γ

![](images/f78e707180e1f0407c3aa1253b100e06820d0d5bfd4dfe0fdf0ee6f8ba71a481.jpg)  
Attention decay  
Fig. 11: sensitivity of tipso-gan to (left) mhsa heads, (middle) focal $\gamma ,$ and (right) attention decay. bars show mean fnr over 5 runs; lower is better.

![](images/5feaeb7b828ca062b1d292106a9896edb82ce62e15e6cdc14d12f7878a57362d.jpg)  
Dropout

![](images/ae14e7a01dcaf6238649a222440ce93ef931f5395e4270238b29e414d9eb55c5.jpg)  
GP strength  
Fig. 12: Sensitivity of TIPSO-GAN to regularization and GAN stability: dropout rate (left) and gradient penalty λ (right). Mean FNR over 5 runs.

![](images/3aeb6887d32cae921ed386219b0a526fa7ec7e007001116fb3f31c47d90690dd.jpg)  
PSO P

![](images/5c6bc781a3a2a17c49917b060a384deb3249393f496b504fd798b4ddb772eac2.jpg)  
PSO I  
Fig. 13: Sensitivity of TIPSO-GAN to PSO parameters: swarm size P (left) and iterations I (right). Mean FNR over 5 runs.

TABLE XV: Parameter settings of TIPSO-GAN.

<table><tr><td>Component</td><td>Hyperparameter</td><td>Value</td></tr><tr><td rowspan="3">Optimization</td><td>Optimizer</td><td>Adam ( $\beta_1=0.5, \beta_2=0.999$ )</td></tr><tr><td>Learning rate</td><td> $2 \times 10^{-4}$ </td></tr><tr><td>Batch size</td><td>256</td></tr><tr><td rowspan="3">GAN Training</td><td>Discriminator updates per generator</td><td>5</td></tr><tr><td>Gradient penalty  $\lambda$ </td><td>10</td></tr><tr><td>Adversarial loss weight</td><td>1.0</td></tr><tr><td rowspan="6">DeePred (Pre-train)</td><td>Encoder depth</td><td>3 convolutional blocks</td></tr><tr><td>Kernel size / stride</td><td> $3 \times 3/1 \times 1$ </td></tr><tr><td>Pooling</td><td>MaxPool (2)</td></tr><tr><td>Activation</td><td>ReLU</td></tr><tr><td>Optimizer</td><td>Adam ( $10^{-4}$ )</td></tr><tr><td>Epochs</td><td>50</td></tr><tr><td rowspan="6">DCGAN (PSOGAN base)</td><td>Conv layers (G/D)</td><td>4 / 4</td></tr><tr><td>Latent dimension z</td><td>100</td></tr><tr><td>Feature map base (G)</td><td>64</td></tr><tr><td>Feature map base (D)</td><td>64</td></tr><tr><td>Normalization</td><td>BatchNorm2d</td></tr><tr><td>Activation</td><td>LeakyReLU (0.2)</td></tr><tr><td rowspan="4">TIPSO-GAN Generator ( $G_T$ )</td><td>Layers</td><td>4 ConvTranspose + BN + ReLU</td></tr><tr><td>Output activation</td><td>Tanh</td></tr><tr><td>Feature expansion</td><td> $128 \rightarrow 256 \rightarrow 512$ </td></tr><tr><td>Dropout rate</td><td>0.3</td></tr><tr><td rowspan="3">MHSA (Discriminator head)</td><td>Heads</td><td>4</td></tr><tr><td>Hidden dim./head</td><td>32</td></tr><tr><td>Attention decay factor</td><td>0.95</td></tr><tr><td rowspan="4">PSO (Training phase only)</td><td>Swarm size P</td><td>30</td></tr><tr><td>Iterations I</td><td>50</td></tr><tr><td>Inertia range ( $w_{\text{max}}, w_{\text{min}}$ )</td><td>(0.9, 0.4)</td></tr><tr><td>Cognitive/social coefficients ( $c_1, c_2$ )</td><td>(2.05, 2.05)</td></tr><tr><td rowspan="2">Regularization</td><td>Dropout rate</td><td>0.3</td></tr><tr><td>Weight decay</td><td> $10^{-4}$ </td></tr></table>

![](images/49c22aa29d72da2b7cdf915a3073e873676ddad5dde22b1a2ac791fd84274ca2.jpg)  
LR sensitivity

![](images/e210da5214f87707ba4374a325e844aa85e400ecad8f54e9f82218bbcdd91ba0.jpg)  
Fig. 14: Sensitivity of TIPSO-GAN to learning rate (left) and batch size (right). Values are mean FNR over 5 runs.

We evaluated the effect of additional training and regularization parameters on TIPSO-GAN. Figure 14 shows that varying the learning rate from $1 \times 1 0 ^ { - 4 } \mathrm { ~ t o ~ } 5 \times 1 0 ^ { - 4 }$ and the batch size from 128 to 512 changes the false negative rate (FNR) by less than one point. Figure 13 reports the PSO optimizer settings: swarm sizes between 30 and 50 and iterations of 50–100 achieve stable results, while smaller values slightly increase FNR. Figure 12 analyzes regularization and GAN stability; dropout rates of 0.2–0.5 and gradient penalty strengths $\lambda ~ \in ~ \{ 5 , 1 0 , 2 0 \}$ yield only marginal shifts, with $\lambda \ = \ 1 0$ and dropout 0.3 giving the lowest error. Across all settings, TIPSO-GAN maintains low FNR, indicating robustness to hyperparameter choices and supporting reproducibility.

## APPENDIX B ARTIFACTS

## A. Code Installation & Configuration

## Installation Steps:

1) Create a Python 3.11 environment (Anaconda recommended).

```batch
python run_repro_perf.py
python run_ablation_pso.py etc.
```

TABLE XVI: Mapping of Paper Claims to Artifact Outputs.  
```csv
Claim Validated by Artifact
C1 run_repro_perf.py, run_compare_baselines.py
→ perf_summary_*.json, baselines_perf_*.json,
confusion_matrix_*.json
run_cost_profile.py → cost_metrics_*.json
C2 run_loss_curves.py → loss_history_*.csv, loss_curves_*.png
C3 run_adaptive_attacks.py →
adaptive_attacks_report_*.json,
adaptive_attacks_summary_*.csv,
adaptive_attacks_*plots
C4 run_transfer.py → dee_transfer_report_*.json, transfer_*.png
C5 run_balance_eval.py → balance_grid_*.csv, preds_*.npy
A1 run_attention_ablation.py → attention_ablation_*.csv
run_pso_ablation.py → pso_vs_static_*.csv
Cost run_cost_profile.py → cost_metrics_*.json, cost_latency.png
Note: filenames with * stands for the dataset names used.
```

2) Run pip install -r requirements.txt.

3) Test setup: python run\_repro\_perf.py. Results appear under artifacts/.

## B. Experiment Workflow

Each experiment is executed via a standalone Python script (run\_<sub>\*</sub>.py) that loads data, trains TIPSO-GAN, evaluates results, and saves outputs to artifacts/.

## Workflow steps:

1) Load data using cicids\_loader.py (default: cicids2018.csv, cicddos2019.csv, cicaptiiot.csv).

2) Initialize model components (PSO, generator, discriminator, DeePred) from train.py.

3) Train & evaluate the TIPSO-GAN framework with configurations in config.py.

4) Store results (metrics, confusion matrix, loss curves) in artifacts/.

To execute any experiment, open the project folder in Visual Studio Code (VS Code) and run the desired script (e.g., run\_repro\_perf.py) using the integrated terminal (right click on the script you want to execute and select ”Run Python File in Terminal”) or “Run Python File” option.

All scripts can alternatively be executed from the command line as: Example command:

Results are automatically saved under artifacts/. All scripts can be run independently or sequentially to reproduce results in the paper. VS Code or any terminal may be used; results appear automatically in artifacts/.

## C. Major Claims

• (C1): TIPSO-GAN achieves superior detection metrics (Acc, Prec, Rec, F1) vs baselines. — (E1, E8) (Table VII).

• (C2): Stability and resilience of TIPSO-GAN against mode collapse. — (E2) Table III.

• (C3): DeePred transfer learning effects. — Fig. 8.

![](images/34b32ee426d8a20ece9153411ce0a861f7a8b37c3c2da2dca1bfd804d98c2043.jpg)  
Fig. 15: Data configuration

TABLE XVII: Baseline Implementations and Code Repositories  
```csv
Method Repository URL
TIPSO-GAN https://doi.org/10.5281/zenodo.17759516
DCGAN, WGAN-GP https://github.com/Zeleni9/pytorch-wgan
FenceGAN https://github.com/phuccuongngo99/Fence_GAN
BiGAN https://github.com/ajbrock/BigGAN-PyTorch
SYN-GAN https://github.com/dagrate/syngan
FT-Transformer https://github.com/yandex-research/
rtdl-revisiting-models
```

• (C4): PSO-based balancing improves recall. — Fig. 6.

• (C5): Model generalizes to unseen attack types. — Table VIII.

• (C6): PSO and attention modules provide additive gains. — added in Table X and Fig. 8.

• (C7): Computational cost comparable to baseline GANs. — Table X.

• (C8): TIPSO-GAN maintains robustness under adaptive attacks. — Table VI.

## D. Evaluation

Table XVI summarizes all experiments (E1–E10), mapping each to its corresponding claim (C1–C8), expected outcome, and generated output files. The corresponding evaluation results reported in the paper are indicated in the major claims section (B-C).

## E. Customization

Modify config.py to adjust epochs, dataset paths (see Fig 15 in each script), and verbosity. All scripts run with CPU by default; set TensorFlow GPU if available.

## F. Code Availability

The implementation of the proposed method is available at https://doi.org/10.5281/zenodo.17759516. See Table XVII for full implementation codes of TIPSO-GAN and the baselines methods.
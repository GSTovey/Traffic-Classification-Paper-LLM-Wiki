USENIX

THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

# From Symmetry toward Weak Asymmetry: Secure Steganography under the Receiver’s Partial Channel Knowledge

Guorui Liao, Shuyu Gan, Jinshuai Yang, Yongfeng Huang, and Zhongyi Huang, Tsinghua University

https://www.usenix.org/conference/usenixsecurity26/presentation/liao

# This paper is included in the Proceedings of the 35th USENIX Security Symposium.

August 12–14, 2026 • Baltimore, MD, USA

ISBN 978-1-939133-58-8

Open access to the Proceedings of the 35th USENIX Security Symposium is sponsored by

AgleU

King Abdullah University of

Science and Technology

# From Symmetry toward Weak Asymmetry: Secure Steganography under the Receiver’s Partial Channel Knowledge

Guorui Liao Shuyu Gan Jinshuai Yang Yongfeng Huang Zhongyi Huang Tsinghua University

## Abstract

Provably secure steganography enables covert communication by disguising secret messages as normal communication content while guaranteeing computational indistinguishabil ity. Recent work typically assumes that the sender can construct stegotext based on explicit conditional distributions, while the receiver either has access to the same distributions for decoding or has no such access at all. In many realistic communication settings, however, the receiver’s access lies between these two extremes, a regime that is not captured by either assumption. We therefore introduce and study a new setting, called weakly asymmetric steganography, in which the sender has access to the full conditional distributions used for stegotext construction, while the receiver only has partial knowledge derived from them. We design provably secure steganography schemes under several representative forms of receiver-side knowledge. Specifically, we consider binary alphabets in which the receiver only knows whether a symbol’s probability exceeds a given threshold, as well as general alpha bets where the receiver only observes a possibly partial rank ing of symbols by probability. We evaluate our rank-based constructions in language-model-based text steganography under both limited receiver-side knowledge and precision induced distribution mismatch. The results show that weakly asymmetric steganography can achieve non-trivial embedding capacity, and further suggest the potential of this setting in distribution-mismatch scenarios.

## 1 Introduction

As surveillance and content censorship become increasingly prevalent, the right to free and private communication in cyberspace faces serious threats [12, 22]. In response, a wide range of privacy-enhancing technologies for communication have been studied and deployed. Among them, steganography circumvents censorship by concealing the very existence of secret communication.

Steganography disguises a secret message (i.e., hiddentext) as seemingly normal content. The resulting disguised content (i.e., stegotext) is designed to make it difficult for third-party observers to distinguish it from truly normal content (i.e., covertext). Through stegotext-based communication, the communicating parties can exchange hiddentext while external observers (censors or service providers), even with full access to all communication content, remain unable to determine whether any secret communication is taking place.

To make the above communication truly secure, researchers formally defined the security of steganography schemes as the computational indistinguishability between stegotext and covertext under the chosen hiddentext attack model (the steganographic version of the chosen plaintext attack model in cryptography). Schemes that satisfy this security definition and the correctness requirement (i.e., the ability to correctly recover the hiddentext) are referred to as provably secure steganography [15, 16]. Intuitively, this means that for any observer with practical computational capabilities, even if they know what the covertexts are expected to look like and even know or can choose the hiddentext to be embedded, they still cannot distinguish the stegotext constructed by the sender from genuine covertext.

For the construction of indistinguishable stegotext, recent mainstream steganography models, such as symmetric steganography [17], typically assume that the sender has access to an oracle which, given the current communication history, provides the explicit conditional distribution over the next covertext symbol. Based on this access, the sender can construct stegotext via a secret-driven sampling algorithm that iteratively selects symbols from the conditional distribution as a function of the hiddentext and updates the communication history until natural termination. The rapid development of AIGC (Artificial Intelligence Generated Content) further supports the practicality of this oracle assumption. In particular, autoregressive generative models [7, 13, 21, 25], such as large language models, explicitly output the conditional distribution over the next token given the current context. As a result, such models naturally instantiate the assumed oracle.

Under this common sender-side assumption, existing models of provably secure steganography can be classified by the receiver-side access they assume. In symmetric steganography, the receiver is assumed to have the same oracle access as the sender, enabling decoding based on the explicit condi tional distributions. In practice, this assumption is typically realized by having both parties deploy the same generative model. In contrast, undetectable steganography [26], also referred to as asymmetric steganography [2], assumes that the receiver has no access to such an oracle and performs decoding solely based on the received stegotext.

However, the two receiver-side assumptions above and their corresponding steganography schemes fail to capture many intermediate practical scenarios. In such scenarios, the receiver may not have access to the oracle described above and therefore cannot obtain the complete conditional distribu tions, yet may still possess some useful information related to these distributions. For instance, in language-model-based text steganography, such intermediate scenarios can arise from two common sources. First, the receiver may be unable to obtain the full conditional distribution due to limited device capability or restricted model access. Instead, it may only interact with the model through limited APIs, which expose partial observations of the distribution, such as top-k tokens or sampled outputs. Second, even if the receiver has access to the same generative model as the sender, it may still fail to reproduce the sender’s exact distributions. This can happen because of numerical precision, hardware differences, or in ference nondeterminism [14]. As a result, the receiver may obtain a perturbed version of the sender’s distribution rather than the exact distribution itself.

In these scenarios, symmetric steganography, which relies on precise distribution access at the receiver, may fail to de code. Asymmetric steganography avoids this requirement, but typically provides only very limited embedding capacity and ignores the partial information already available to the receiver.

To address this gap, we introduce the notion of weakly asymmetric steganography, which studies this intermediate regime through a clean and tractable abstraction: the receiver obtains only the information specified by a deterministic func tion of the sender’s conditional distribution, for example, the relative ordering of symbols under that distribution. We refer to such information as the receiver’s partial channel knowl edge. Figure 1 illustrates how our setting compares to existing steganography models. This abstraction captures a tractable core of the broader intermediate regime, while also provid ing a starting point for studying more approximate or noisy forms of receiver-side information. For example, information inferred from repeated samples, or statistical properties that may be preserved under distributional perturbations, can be viewed as natural extensions of this abstraction.

Weakly asymmetric steganography raises several funda mental questions that have not been studied before. One of the most basic questions is whether, given a fixed form of partial channel knowledge, there exist steganography schemes that decode using only this knowledge and effectively exploit it. To the best of our knowledge, existing work provides no clear evidence that such schemes exist for any concrete form of partial channel knowledge, beyond the trivial approach of ignoring such knowledge and falling back to fully asymmetric steganography schemes.

![](images/f7ec526e4f4ef01ac8419ae19f89810ea869ed9101b403d85712226cd4feef90.jpg)  
Figure 1: Comparison of symmetric, asymmetric, and weakly asymmetric steganography scenarios.

In this work, we take a first step toward answering this question by studying and constructing weakly asymmetric steganography schemes under two natural forms of receiver’s partial channel knowledge: threshold-based knowledge in binary alphabets and rank-based knowledge in general alphabets. The former tells the receiver whether a symbol’s probability exceeds a threshold, while the latter gives a full or partial ranking of symbols by probability. We further evaluate the proposed rank-based schemes in language-model-based text steganography under both limited receiver-side knowledge and precision-induced distribution mismatch.

Our main contributions are as follows:

1. We introduce a new formal setting, weakly asymmetric steganography, which captures scenarios where the sender has access to the full conditional distributions of the channel, while the receiver possesses only partial knowledge about these distributions.

2. We initiate the study of weakly asymmetric steganography by designing provably secure schemes under two representative forms of partial channel knowledge. In particular, we present schemes under threshold-based knowledge in binary alphabets and rank-based knowledge in general alphabets, demonstrating that partial channel knowledge can be explicitly exploited to achieve meaningful embedding capacity.

3. We empirically evaluate the proposed rank-based weakly asymmetric schemes in language-model-based text steganography. Our experiments show that weakly asymmetric steganography achieves non-trivial embedding capacity under limited receiver-side knowledge, and further suggest that this paradigm has potential in precisioninduced distribution-mismatch scenarios.

## Organization

The rest of this paper is organized as follows. Section 2 reviews the necessary background and related work on provably secure steganography. Section 3 introduces the formal model of weakly asymmetric steganography. Section 4 presents concrete constructions of weakly asymmetric steganography schemes under threshold and rank-based channel knowledge. Section 5 reports experimental evaluations of the proposed schemes in language-model-based text steganography, including studies under partial channel knowledge and distribution mismatch.

## 2 Background and Related Work

Provably Secure Steganography In 2002, Hopper et al. [16] introduced provably secure steganography, formalizing two fundamental requirements: correctness and secu rity. Correctness requires that the receiver’s decoding error be negligible, while security requires that no probabilistic polynomial-time (ppt.) adversary can distinguish stegotexts from covertexts with non-negligible advantage under chosen hiddentext attacks. This paradigm was initially studied in the universal steganography setting, where the sender has access to an oracle that samples from the channel distribution, whereas the receiver has no access to that distribution. Several schemes based on rejection sampling have been proposed in this setting [1, 3, 4, 10, 20, 23]. This setting minimizes oracle requirements, while existing schemes typically depend on strong and often unrealistic assumptions. For instance, they require the channel to exhibit a positive lower bound on the entropy of its conditional distributions, or assume the existence of suitable unbiased hash functions. Such conditions are rarely satisfied in practice [17]. In addition, these schemes generally provide only limited embedding capacity, which further restricts their practical applicability.

Symmetric Steganography with Generative Models Symmetric steganography, formalized by Kaptchuk et al. [17], assumes that both the sender and the receiver have access to an oracle that provides the channel distribution. This setting has become one of the most widely adopted paradigms [11, 17, 19, 24] in the study of provably secure steganography, partly because it naturally aligns with modern generative models [13, 21, 25] and enables practical and efficient stegosystems. Indeed, a generative model can be viewed as a function that maps a history (or prefix) to a conditional distribution over the next symbol, thereby instantiating the oracle assumed in symmetric steganography.

In practice, the most common application scenario of sym metric steganography is text steganography based on language models. Here, the sender transforms a secret message into fluent text by leveraging the shared language model and a symmetric steganography scheme. With provable security, the generated stegotext is computationally indistinguishable from normal language-model outputs. The receiver, equipped with the same language model, can reliably decode the embed ded message, while this shared-model setting also supports high embedding capacity. Recent symmetric steganography schemes [11,24] achieve embedding rates close to the channel entropy, which is the theoretical upper bound.

However, the correctness of symmetric steganography schemes relies on a fragile consistency requirement: at each step, the receiver must reconstruct the same conditional distribution used by the sender, even though the receiver itself does not generate stegotext. In language-model-based instantiations, this requires not only that both parties can run the same model (typically an open-source model), but also that their inference pipelines match closely, since even small differences in implementation details or numerical precision can change the induced conditional distribution.

Asymmetric Steganography (Undetectable Steganography) Undetectable watermarking, proposed by Christ et al. [9], was originally designed for watermarking the outputs of large language models. Its core assumption is that the sender (i.e., the model owner) controls the generation process, while the receiver (i.e., the detector), lacking access to the language model and the prompt, has no access to the conditional distributions underlying the generated text. The goal is to embed a detectable watermark while ensuring that watermarked outputs remain computationally indistinguishable from normal text, thereby preserving both linguistic quality and the statistical characteristics of model outputs. Building on this line of work, subsequent research generalized the embedded signal from a single watermark bit to richer information, leading to the notion of undetectable steganography [26], which is also referred to as asymmetric steganography in later work [2].

Existing schemes [2, 8, 26] typically encode information by biasing the sender’s symbol choice at each generation step based on the secret message. Although the receiver does not know the underlying channel distribution, given the secret key, each symbol has a small amount of mutual information with the secret message, allowing the receiver to recover the message by aggregating many observed symbols and performing hypothesis testing. This design is attractive because the receiver can decode solely from the observed symbols, without requiring access to the channel distribution or maintaining a synchronized channel history. Compared to symmetric steganography, the receiver does not need to run an identical and computationally expensive model as the sender, nor does it need to keep track of past context. Moreover, it is often robust to certain modifications of the generated stegotext.

However, these advantages come at a cost. In particular, the achievable embedding capacity is significantly constrained, making these schemes less suitable for covert communication scenarios that demand higher throughput. Moreover, these schemes still require careful balancing between the embed ding rate and decoding correctness, as decoding is based on hypothesis testing.

## 3 Definitions

## 3.1 Motivation

Symmetric and asymmetric steganography correspond to two extreme receiver-side assumptions. Many practical scenarios, however, lie between them: the receiver may be unable to obtain or exactly reproduce the conditional distributions, while still having useful information about them. This suggests an intermediate regime that is practically meaningful and theoretically worth studying.

Modeling such intermediate cases in full generality is difficult, since the receiver’s information is often approximate, noisy, and hard to characterize uniformly in practice. We therefore adopt a clean and tractable abstraction: the receiver obtains only the information specified by a deterministic func tion $f ( D )$ , where D is the sender’s conditional distribution. We call f the knowledge function, and refer to steganography under this abstraction as weakly asymmetric steganography. This abstraction directly captures settings where the receiver is given partial channel knowledge, while also providing a basis for studying broader settings. For example, such knowledge may be inferred from repeated samples. Moreover, when the receiver only has an approximate version of the sender’s distribution, coarse knowledge such as ordering may be more stable than exact probabilities, and may help make decoding more reliable in such cases.

In this section, we introduce the notation used throughout this work and formalize weakly asymmetric steganography in the symmetric-key setting.

## 3.2 Notations

Following the formulation of provably secure steganography [15, 17], we use the term covertext channel to refer to the normal communication channel in the steganographic setting. We write Σ for the alphabet of symbols that may appear in the communication, and denote $\Sigma = \{ \sigma _ { 0 } , \hdots , \sigma _ { | \Sigma | - 1 } \}$

We describe the behavior of a covertext channel by a probability distribution, referred to as the covertext channel distribution (or simply the channel distribution). Intuitively, the covertext channel distribution describes how normal commu nication typically continues after any given history. Formally, the covertext channel distribution D is a probability distribution over $\Sigma ^ { * }$ , where $\Sigma ^ { * }$ denotes the set of all finite sequences over Σ. For any history $\mathcal { H } = ( h _ { 0 } , \dotsc , h _ { n - 1 } ) \in \Sigma ^ { * }$ , D induces the conditional distribution over Σ of the next symbol in normal communication given ${ \mathcal { H } } .$ , which we denote by $\mathcal { D _ { H } }$ . When unambiguous, we will simply refer to $\mathcal { D } _ { \mathcal { H } }$ as the conditional distribution, and we will often use D to denote it.

## 3.3 Knowledge Function & Knowledge

We first formalize the notion of a knowledgefunction, which specifies what information about a distribution is available to a communication entity. Formally, a knowledge function is a mapping

$$
f: \mathcal {X} \to \mathcal {Y},
$$

where X denotes the set of probability distributions over the alphabet $\Sigma ,$ and $\mathcal { T }$ is the corresponding feature space. For a distribution $D \in { \mathcal { X } }$ , we refer to the value $f ( D ) \in \mathcal { Y }$ itself as the knowledge. Typical examples of knowledge functions include, for instance, the rank function rank(·), which maps a distribution D over Σ to the ordering of symbols by probability.

We say that a communication entity has knowledge f about the channel distribution D if, for every history H, it has access to the value $f ( \mathcal { D } _ { \mathcal { H } } )$ . For brevity, we refer to this access as having knowledge $f ( \mathcal D )$

The identity knowledge function $f _ { \mathrm { i d } } ( D ) = D$ corresponds to full channel knowledge. A constant knowledge function corresponds to no channel knowledge, since it reveals no nontrivial information about the conditional distribution. In this work, we focus on non-degenerate knowledge functions that lie strictly between these two extremes, and we refer to this regime as having partial channel knowledge.

## 3.4 Weakly Asymmetric Steganography

We follow the formal definition of symmetric steganography given by Kaptchuk et al. [17] and adapt it to define weakly asymmetric steganography, where the receiver has only partial channel knowledge. We state the definition as follows:

Definition 1 (Weakly Asymmetric Steganography). A weakly asymmetric steganography scheme $\Pi _ { \mathcal { D } , f } ,$ defined under a covertext channel distribution D and a knowledge function $f ,$ is a triple of possibly probabilistic algorithms,

$$
\Pi_ {\mathcal {D}, f} = \left(\operatorname{KeyGen} _ {\mathcal {D}}, \operatorname{Encode} _ {\mathcal {D}} ^ {f}, \operatorname{Decode} _ {f (\mathcal {D})}\right).
$$

$\mathsf { K e y G e n } _ { \mathcal { D } } ( 1 ^ { \lambda } )$ : generates the secret key sk.

• Encod $\mathsf { \Omega } _ { \mathcal { D } } ^ { f } ( \mathsf { s k } , m , \mathcal { H } )$ : takes as input a secret key sk, a secret bit string m (also called the hiddentext), and the channel history H . It outputs a stegotext $c \in \Sigma ^ { * }$

• Decode $\dot { \mathbf { \zeta } } _ { f ( \mathcal { D } ) } ( \mathbf { s k } , c , \mathcal { H } )$ : takes as input a secret key sk, a stegotext $^ { c , }$ and the channel history H. It outputs a bit string m on success, or the empty string ε on failure.

Here, the subscript D indicates that the algorithm has full channel knowledge, meaning that for any history ${ \mathcal { H } } ,$ it has access to the exact value of $\mathcal { D } _ { \mathcal { H } }$ . The superscript f indicates that the encoding algorithm also knows the public knowledge function $f .$ In contrast, the subscript $f ( \mathcal { D } )$ indicates that the algorithm has access only to the knowledge specified by $f ( \mathcal D )$ that is, for any history H, it knows only the value $f ( \mathcal { D } _ { \mathcal { H } } )$

Correctness. A scheme must ensure correctness, i.e., the Decode $f ( \mathcal D )$ algorithm can recover the embedded message from the stegotext except with negligible probability. For mally, for any secret key sk $ \mathsf { K e y G e n } _ { \mathcal { D } } ( 1 ^ { \lambda } )$

$$
\operatorname * {P r} \left[ \operatorname{Decode} _ {f (\mathcal {D})} (\mathrm{sk}, \operatorname{Encode} _ {\mathcal {D}} ^ {f} (\mathrm{sk}, m, \mathcal {H}), \mathcal {H}) = m \right] \geq 1 - \operatorname{negl} (\lambda).
$$

Security. Security requires that no ppt. adversary, given the full channel distribution $\mathcal { D } ,$ can distinguish oracle access to Encod $\mathsf { a } _ { \mathcal { D } } ^ { f } ( \mathsf { s k } , \cdot , \cdot )$ from oracle access to a random sampling oracle $O _ { \mathcal { D } } ( \cdot , \cdot )$ that returns a sample generated according to D with the appropriate length. Formally, a scheme is secure against chosen hiddentext attacks if, for all ppt. adversaries ${ \mathcal { A } } _ { { \mathcal { D } } } ,$ , with sk $ \mathsf { K e y G e n } _ { \mathcal { D } } ( 1 ^ { \lambda } )$ , the following inequality holds:

$$
\left| \operatorname * {P r} \left[ \mathcal {A} _ {\mathcal {D}} ^ {\text {Encode} _ {\mathcal {D}} ^ {f} (\mathrm{sk}, \cdot , \cdot)} = 1 \right] - \operatorname * {P r} \left[ \mathcal {A} _ {\mathcal {D}} ^ {O _ {\mathcal {D}} (\cdot , \cdot)} = 1 \right] \right| \leq \operatorname{negl} (\lambda).
$$

Informally, symmetric and asymmetric steganography can be viewed as two boundary cases of our formulation. In the symmetric setting, both the sender and the receiver have full channel knowledge. In contrast, the fully asymmetric setting can be roughly modeled by taking f to be a constant function $( \boldsymbol { \mathrm { e } } . \boldsymbol { \mathrm { g } } . , f \equiv 0 )$ , meaning that the receiver has no meaningful channel knowledge. Weakly asymmetric steganography, as studied in this work, captures the intermediate regime where f reveals some structured information about the channel distribution, while still falling short of full channel knowledge.

For any knowledge function $f ,$ every asymmetric steganography scheme is a valid weakly asymmetric steganography scheme, where the receiver can simply ignore $f ( \mathcal D )$ . Therefore, the central question is not existence, but non-triviality: whether there exist schemes that meaningfully exploit the receiver’s knowledge $f ( \mathcal D )$ to gain a strict advantage over simply ignoring it. We call such schemes non-trivial weakly asymmetric steganography schemes under knowledge $f .$ In this work, we focus on such non-trivial schemes.

## 4 Schemes under Threshold and Rank Knowledge

A natural question regarding weakly asymmetric steganog raphy is whether this setting has practical significance, or whether it amounts to a purely definitional generalization of symmetric and asymmetric steganography. More concretely, to the best of our knowledge, existing work has not established the existence of non-trivial weakly asymmetric steganography schemes under any form of partial channel knowledge.

This section provides an initial answer to this question by presenting constructions under two specific forms of partial channel knowledge. We consider threshold-based knowledge over binary alphabets, as well as rank-based knowledge over general alphabets, demonstrating the existence of non-trivial weakly asymmetric steganography schemes in both cases.

Throughout this section, all schemes are stateful [6]: the encoding and decoding algorithms maintain internal states that evolve with each invocation, following standard practice in symmetric steganography $[ 1 1 , 1 7 , 1 9 , { \bar { 2 } } 4 ] . ^ { 2 }$ They are also instantaneously decodable: each received symbol can be decoded immediately, without relying on future symbols, which helps limit error propagation in noisy cases.

Before introducing the constructions, we recall a standard technical component used in many symmetric steganography schemes [17, 19], namely a stateful pseudorandom generator.

## 4.1 Stateful Pseudorandom Generators

Following most classical constructions in symmetric steganography, particularly Meteor [17], our schemes utilize a stateful pseudorandom generator (PRG) [5]. We follow Meteor’s notation for stateful PRGs here. The stateful PRG consists of two algorithms:

## PRG.Setup,PRG.Next.

The setup algorithm generates the initial state material for the PRG and each invocation of PRG.Next outputs fresh pseudorandom bits of sufficiently long fixed length. We interpret this output as a real value in [0, 1) by normalizing the bit string in the natural way. We assume standard security: no ppt. adversary can distinguish oracle access to PRG.Next from oracle access to a truly uniform bit source with non-negligible advantage. Informally, sharing the same initial PRG state allows the sender and receiver to generate shared pseudorandomness.

## 4.2 Binary Alphabet under Threshold Knowledge

For a binary alphabet $\Sigma = \{ \sigma _ { 0 } , \sigma _ { 1 } \}$ , a distribution D is completely determined by the value $D ( \sigma _ { 0 } )$ . Thus, a natural form of partial knowledge is threshold information about this value.

We define a threshold knowledgefunction $\mathbf { 1 } _ { \theta } ( \cdot )$ , which indicates whether the probability of symbol $\sigma _ { 0 }$ in the distribution D is below a given threshold θ. Specifically, it outputs:

$$
\mathbf {1} _ {\theta} (D) := \mathbf {1} [ D (\sigma_ {0}) <   \theta ] = \left\{ \begin{array}{l l} 0, & \text { if } D (\sigma_ {0}) \geq \theta , \\ 1, & \text { if } D (\sigma_ {0}) <   \theta . \end{array} \right.
$$

This knowledge function reveals the comparison between $D ( \sigma _ { 0 } )$ and θ, and equivalently the comparison between $D ( \sigma _ { 1 } )$ and $1 - \theta .$ In this section, we consider weakly asymmetric steganography under the threshold knowledge function $\mathbf { 1 } _ { \theta } ( \cdot )$

A natural first attempt is to follow the randomness-recovery view of Meteor [17]: the (masked) hiddentext is interpreted as the randomness in [0,1) used for sampling, and each output symbol corresponds to a sampling interval. Thus, observing a symbol tells the receiver that the hiddentext lies in the corresponding interval, thereby reducing the uncertainty about the hiddentext and hence revealing information in the information-theoretic sense. This idea can also be applied here. For example, if the receiver observes $\sigma _ { 0 }$ and knows that $D ( \sigma _ { 0 } ) < \theta .$ , then it can localize the hiddentext to a known interval of length θ, and thus obtains some information about the hiddentext. However, Meteor recovers bits by extracting the common binary prefix of the inferred interval. Therefore, when $\Theta > 1 / 2$ , the inferred interval may have no nonempty common binary prefix, and this prefix-based recovery decodes no bit.

This observation suggests that threshold knowledge should be exploitable. The key is to focus on the symbol for which the receiver can certify a probability upper bound strictly smaller than 1. This intuition leads to our scheme below. We first present the special case $\Theta = 0 . 5 .$ and then extend it to handle an arbitrary threshold $\boldsymbol { \theta } \in ( 0 , 1 )$ .

## 4.2.1 The Special Case θ = 0.5

We begin with the case $\theta = 0 . 5$ , which captures the core ideas of our construction and provides a convenient starting point before extending to arbitrary thresholds. In this setting, the receiver only has access to the value ${ \bf 1 } _ { 0 . 5 } ( D )$ , rather than the full conditional distribution D.

Equivalently, this means that the receiver’s knowledge indicates which symbol is more likely under the binary distribution. Specifically, let $k = 1 _ { 0 . 5 } ( D )$ . By definition, we have

$$
D (\sigma_ {k}) \geq 0. 5 \geq D (\sigma_ {1 - k}),
$$

so $\sigma _ { k }$ is more likely, while $\sigma _ { 1 - k }$ is less likely.

Next, we describe the sender’s Sample algorithm and the receiver’s Recovery algorithm. The Sample algorithm specifies how the symbol is sampled based on the secret message for each conditional distribution $\mathcal { D } _ { \mathcal { H } }$ . The Recovery algorithm specifies how the receiver, given access to $f ( \mathcal { D } _ { \mathcal { H } } )$ , recovers the embedded bits from the received symbol. The full Encode and Decode algorithms are obtained by iterating these steps, as shown in Algorithm 4 and Algorithm 5.

(1) Sample algorithm. Given the current conditional distri bution $D = \mathcal { D } _ { \mathcal { H } }$ , the sender first computes $k = 1 _ { 0 . 5 } ( D )$ , so that $\sigma _ { k }$ is the more likely symbol and $\sigma _ { 1 - k }$ is the less likely one. The sender then draws a fresh pseudorandom value $r \in [ 0 , 1 )$ from the shared stateful PRG and lets b denote the first bit of the remaining secret message to be embedded. It then derives

$$
r ^ {\prime} = \left\{ \begin{array}{l l} r, & \text { if } b = 0 \\ 1 - r, & \text { if } b = 1 \end{array} \right.
$$

The value $r ^ { \prime }$ is used to sample a symbol. Specifically, the unit interval [0, 1) is partitioned according to the distribution D as follows:

$$
I _ {\sigma_ {1 - k}} = [ 0, D (\sigma_ {1 - k})), \qquad I _ {\sigma_ {k}} = [ D (\sigma_ {1 - k}), 1),
$$

Accordingly, the sender outputs $\sigma _ { 1 - k } \mathrm { i f } r ^ { \prime } < D ( \sigma _ { 1 - k } )$ , and $\sigma _ { k }$ otherwise.

In particular, when $b = 0 ,$ we have $r ^ { \prime } = r ,$ , and the above procedure reduces to sampling within the partition $\left( { { I _ { \alpha _ { 1 - k } } } , { I _ { \sigma _ { k } } } } \right)$ using r. When $b = 1$ , we have $r ^ { \prime } = 1 - r ,$ which is equivalent to sampling with r within the swapped partition $( I _ { \sigma _ { k } } ^ { \prime } , I _ { \sigma _ { 1 - k } } ^ { \prime } )$ where:

$$
I _ {\sigma_ {k}} ^ {\prime} = [ 0, D (\sigma_ {k}) ], \quad I _ {\sigma_ {1 - k}} ^ {\prime} = (D (\sigma_ {k}), 1).
$$

An illustrative overview is provided in Fig. 2.

If the sampled symbol is $\sigma _ { 1 - k } ,$ , the current secret bit b is considered successfully embedded, and the Encode algorithm proceeds to the next bit in the subsequent sampling step. Otherwise, the same secret bit is reused in the next sampling step. The formal description of the Sample algorithm is given in Algorithm 1. This procedure is feasible because the sender has full channel knowledge, in particular the exact values of $D ( \sigma _ { k } )$ and $D ( \sigma _ { 1 - k } )$

![](images/6385f694fbd51df047908ba5b570d5bbfd237b9ebe10414b0ad5a21aaa314b89.jpg)  
Figure 2: Illustration of the Sample algorithm under different bit b for a given pseudorandom value r. Here, $c _ { i }$ denotes the sampled symbol.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1: Sample $_{1_{0.5}}^{\Sigma=\{\sigma_{0},\sigma_{1}\}}(m',\mathrm{PRG}_{\mathrm{sk}},D)$

Input: Bits $m'$, Pseudorandom Generator PRG$_{sk}$, Distribution D

Output: Sampled Symbol $c_{i}$, Number of Embedded Bits $n_{i}$ $k \leftarrow 1_{0.5}(D), r \leftarrow \mathrm{PRG}_{\mathrm{sk}}.\mathrm{Next}(), b = m'[0]$;

$r' \leftarrow \begin{cases} r, &amp; \text{if } b = 0 \\ 1 - r, &amp; \text{if } b = 1 \end{cases}$

if $r' &lt; D(\sigma_{1-k})$ then

$\lfloor c_{i} \leftarrow \sigma_{1-k}, n_{i} \leftarrow 1;$

else

$\lfloor c_{i} \leftarrow \sigma_{k}, n_{i} \leftarrow 0;$

return $c_{i}, n_{i}$
</div>

(2) Recovery algorithm. Upon receiving the symbol and the knowledge $k = \mathbf { 1 } _ { 0 . 5 } ( D )$ , the receiver first checks whether the received symbol is $\sigma _ { 1 - k }$ . If not, then no bit has been embedded in the corresponding sampling step, and hence no further decoding is required at this step.

Once the symbol $\sigma _ { 1 - k }$ is observed, the decoded bit is determined by

$$
\mathbf {1} [ r \geq 0. 5 ],
$$

where r is the shared pseudorandom value generated by the stateful PRG. Specifically, if $r < 0 . 5 .$ , then the decoded bit is $0 ;$ otherwise, $\mathrm { i f } r \geq 0 . 5 ,$ , the decoded bit is 1. A formal description of the Recovery algorithm is given in Algorithm 2.

Notably, the receiver only needs to know the value of k (and hence the identity of $\sigma _ { 1 - k } )$ and the comparison between the shared randomness r and 0.5 to perform decoding, and does not require access to the exact value of $D ( \sigma _ { 1 - k } )$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Recovery $_{1_{0.5}}^{\Sigma=\{\sigma_{0},\sigma_{1}\}}(c_{i},PRG_{sk},k)$

Input: Symbol $c_{i}$, Pseudorandom Generator PRG$_{sk}$, Knowledge k

Output: Bit $x\in\{0,1,\varepsilon\}$ $r\leftarrow PRG_{sk}.Next();$

if $c_{i}=\sigma_{k}$ then

$|x\leftarrow\varepsilon;$

else

$if r&lt;0.5 then$ $|x\leftarrow0;$

else

$|x\leftarrow1;$

return x
</div>

By iterating the Sample and Recovery algorithms in Algorithm 1 and Algorithm 2, we obtain the corresponding encod ing and decoding algorithms Encod $\underline { { \mathsf { a } } } _ { \mathcal { D } } ^ { f }$ and Decode $f ( \mathcal { D } )$ , as formalized in Algorithm 4 and Algorithm 5. Together with the key generation algorithm $\mathsf { K e y G e n } _ { \mathcal { D } }$ in Algorithm 3, this yields the following theorem.

Theorem 1. For any covertext channel distribution D over the binary alphabet $\Sigma = \{ \sigma _ { 0 } , \sigma _ { 1 } \}$ , the scheme

$$
\Pi_ {\mathcal {D}, f} = (\mathrm{KeyGen} _ {\mathcal {D}}, \mathrm{Encode} _ {\mathcal {D}} ^ {f}, \mathrm{Decode} _ {f (\mathcal {D})})
$$

defined by Algorithm 3, Algorithm $^ { 4 , }$ and Algorithm ${ \mathfrak { H } } ,$ and induced by the Sample and Recovery in Algorithm 1 and Algorithm 2, is a weakly asymmetric steganography scheme under the knowledgefunction $f = \mathbf { 1 } _ { 0 . 5 } ( \cdot )$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: KeyGen$_{\mathcal{D}}(1^{\lambda})$

Input: Security Parameter $1^{\lambda}$
Output: Secret Key sk
sk $\leftarrow$ PRG.Setup($1^{\lambda}$);
return sk
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4: Encode$_{D}^{f}$(sk, m, H)

Input: Secret key sk, Hiddentext m, history H
Output: Stegotext c
n ← 0, c ← ε;
while n &lt; |m| and c has not ended do
    m' = m[n :];
    D ← D_H;
    ci, ni ← Sample$_{f}^{\Sigma}$(m', PRG$_{sk}$, D);
    c ← c ||ci, n ← n + ni;
    H ← H ||ci;
return c
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5: Decode $_{f(\mathcal{D})}$ (sk, c, H)

Input: Secret key sk, stegotext c, history H

Output: Bit string m

 $m \leftarrow \varepsilon$ ;

Let $c = (c_{0}, c_{1}, \ldots, c_{|c| - 1})$ ;

for $i \leftarrow 0$ to $|c| - 1$ do

 $k \leftarrow f(\mathcal{D}_{\mathcal{H}})$ ;

 $x \leftarrow Recovery_{f}^{\Sigma}(c_{i}, PRG_{sk}, k)$ ;

 $m \leftarrow m \|x, \mathcal{H} \leftarrow \mathcal{H} \|c_{i}$ 

return m
</div>

Proof sketch of Security. We first provide an informal intuitive proof, where we simplify by treating the random values r generated by the stateful PRG as independent and uniformly random.

For any given history H and fixed secret bit b, the Sample<sub>1</sub> Σ={σ<sub>0</sub>,σ<sub>1</sub>} algorithm samples according to the distribution $\mathcal { D } _ { \mathcal { H } }$ using the value $r ^ { \prime } .$ . Since $r ^ { \prime }$ is uniformly random regardless of whether $b = 0 \ \mathrm { o r } \ b = 1$ , the probability of sampling σ as the stego symbol $c _ { i }$ is

$$
\operatorname * {P r} _ {r \leftarrow \text {Unif} ([ 0, 1))} \bigl [ c _ {i} = \boldsymbol {\sigma} \mid \mathcal {H}, b \bigr ] = \mathcal {D} _ {\mathcal {H}} (\boldsymbol {\sigma}).
$$

Thus, conditioned on the current history ${ \mathcal { H } } ,$ each execution of Sampl $\begin{array} { l } { \Sigma { = } \{ \sigma _ { 0 } , \sigma _ { 1 } \} } \\ { { \overset { \gimel } { \cdot } } \mathbf { 1 } _ { 0 . 5 } } \end{array}$ has exactly the same output distribution as sampling directly from $\mathcal { D _ { H } }$

Furthermore, consider any two executions of $\mathsf { S a m p l e } _ { 1 _ { 0 . 5 } } ^ { \Sigma = \{ \sigma _ { 0 } , \sigma _ { 1 } \} }$ . Even if the corresponding secret bits are correlated, or even identical because the same bit is reused, the values $r _ { 0 } ^ { \prime }$ and $r _ { 1 } ^ { \prime }$ remain independent, since the underlying random values $r _ { 0 }$ and $r _ { 1 }$ are independent. Therefore, under this assumption (i.e., treating the values r as independent and uniformly random), for any fixed secret message m and secret key sk, the output of a single query to the encoding oracle Encode $\boldsymbol { \cdot } _ { \mathcal { D } } ^ { f }$ has the same distribution as the output of a single query to the oracle $O _ { \mathcal { D } }$

Finally, using the security of the underlying stateful PRG and the statefulness of the scheme, a standard hybrid argument

�. �

yields a formal proof of security.

Proof of Correctness. We show that the Recovery algorithm correctly recovers the bit embedded by the corresponding Sample algorithm.

First, consider the case where the sampled symbol is $\sigma _ { k }$ the more likely symbol. In this case, no bit is successfully embedded by the Sample algorithm, and hence no decoding is required. Accordingly, the Recovery algorithm outputs ε, which is correct.

We now consider the case where the sampled symbol is $\sigma _ { 1 - k } ,$ , in which exactly one bit is embedded. Fig. 3 depicts the sender’s sampling process from the receiver’s view and makes the correctness of the recovery rule intuitive. In the left half of the diagram, where $0 \leq r < 0 . 5$ , the symbol $\sigma _ { 1 - k }$ may be sampled when $b = 0 ;$ , but it cannot be sampled when $b = 1$ . Therefore, if the shared pseudorandom value $r < 0 . 5 .$ then sampling $\sigma _ { 1 - k }$ implies that the embedded bit must be 0. Equivalently,

$$
r <   0. 5 \land c _ {i} = \sigma_ {1 - k} \implies \text { embedded   bit } = 0.
$$

Indeed, if the embedded bit were 1, the Sample algorithm would output $\sigma _ { k }$ when $r < 0 . 5$ , since $D ( \sigma _ { k } ) \geq 0 . 5$ , contradicting the sampling of $\sigma _ { 1 - k }$ . Similarly, when $r \geq 0 . 5 .$ , sampling $\sigma _ { 1 - k }$ implies that the embedded bit must be 1. That is,

$$
r \geq 0. 5 \land c _ {i} = \sigma_ {1 - k} \implies \text { embedded   bit } = 1.
$$

Therefore, in this case the embedded bit can be expressed as

$$
\mathbf {1} [ r \geq 0. 5 ],
$$

which coincides exactly with the decoding rule used by the Recovery algorithm.

Therefore, in all cases, the Recovery algorithm correctly recovers the embedded bit. Since the Encode and Decode algorithms are obtained by iterating the corresponding Sample and Recovery procedures, the correctness of the scheme fol lows. If the stegotext naturally terminates before the entire hiddentext is embedded, correctness is understood with respect to the embedded prefix of the hiddentext.

<table><tr><td></td><td colspan="2">0≤r&lt;0.5</td><td colspan="2">0.5≤r&lt;1</td></tr><tr><td></td><td>0≤r&lt;**</td><td>**≤r&lt;0.5</td><td>0.5≤r&lt;1-**</td><td>1-**≤r&lt;1</td></tr><tr><td>b=‘0’</td><td>σ1-k</td><td></td><td colspan="2">σk</td></tr><tr><td>b=‘1’</td><td colspan="2">σk</td><td></td><td>σ1-k</td></tr></table>

From the view above, the Recovery knows

Figure 3: Illustration of the recovery procedure. The marker “\*\*” indicates that the exact value of $D ( \sigma _ { 1 - k } )$ is unknown to the receiver.

Capacity. We note that the Recovery algorithm can recover exactly 1 bit if and only if the sampled symbol is $\sigma _ { 1 - k }$ , which occurs with probability $D _ { \operatorname* { m i n } } = D ( \sigma _ { 1 - k } ) \leq 0 . 5$ . Therefore, the capacity (expectation) for this symbol is

$$
C _ {\mathbf {1} _ {0. 5}} = 1 \times D _ {\min} + 0 \times (1 - D _ {\min}) = D _ {\min}.
$$

## 4.2.2 General Case $\boldsymbol { \theta } \in ( 0 , 1 )$

To generalize the threshold from $\theta = 0 . 5$ to an arbitrary $\theta \in$ $( 0 , 1 )$ , we first reinterpret the Sample and Recovery for the case $\theta = 0 . 5$

The sender first applies a bit-controlled transformation to the shared random value r according to the current secret bit b (i.e., choosing to use either $r \ \mathrm { o r } \ 1 - r )$ , and then samples according to the distribution D. Moreover, a secret bit is considered successfully embedded and the sender proceeds to the next bit, if and only if the receiver is able to uniquely decode this bit. On the receiver side, decoding is attempted only upon receiving a symbol whose probability admits a known upper bound $( \mathrm { i } . \mathbf { e } . \sigma _ { 1 - k } )$ . Furthermore, decoding is performed only when the value r lies in a region that allows the secret bit to be uniquely determined. In the case $\theta = 0 . 5$ , as discussed above, this upper bound equals 0.5, and the corresponding decodable region covers the entire interval [0, 1). From this perspective, extending the construction to a general threshold θ reduces to identifying the range of random values for which the receiver can uniquely decode.

On the sender side, the sampling procedure remains unchanged: given the current secret bit b, the sender applies the same bit-controlled transformation to the shared random value, namely using $r ^ { \prime } = r { \mathrm { ~ i f ~ } } b = 0$ and $r ^ { \prime } = 1 - r \operatorname { i f } b = 1$ and then samples a symbol according to the distribution D. Consequently, for a general θ, the range of random values for which the receiver can uniquely decode is

$$
[ 0, \min (\theta , 1 - \theta) ] \cup (\max (\theta , 1 - \theta), 1)
$$

This is because, under the receiver’s knowledge $k = \mathbf { 1 } _ { \theta } ( D )$ we have

$$
D (\sigma_ {k}) \geq \min (\theta , 1 - \theta) \quad \text { and } \quad D (\sigma_ {1 - k}) \leq \max (\theta , 1 - \theta).
$$

Therefore, when $r \leq \operatorname* { m i n } ( \Theta , 1 - \Theta )$ , observing the symbol $\sigma _ { 1 - k }$ necessarily implies that it was sampled using $r ^ { \prime } = r ,$ and hence the embedded bit can be uniquely determined to be 0. Similarly, when $r > \operatorname* { m a x } ( \theta , 1 - \theta )$ , the embedded bit can only be 1.

A corresponding intuitive illustration is given in Figure 4. In the left region $0 \leq r \leq \operatorname* { m i n } ( \Theta , 1 - \Theta )$ ), the symbol $\sigma _ { 1 - k }$ may be sampled when $b = 0 ,$ , but cannot be sampled when $b = 1 ;$ hence observing $\sigma _ { 1 - k }$ uniquely determines the embedded bit as 0. Symmetrically, in the right region max $( \Theta , 1 - \Theta ) < r < 1$ the symbol $\sigma _ { 1 - k }$ may be sampled when $b = 1$ , but cannot be sampled when $b = 0 ;$ hence observing $\sigma _ { 1 - k }$ uniquely determines the embedded bit as 1. The middle region remains ambiguous from the receiver’s viewpoint and is therefore treated as non-decodable.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6: Sample $\Sigma=\{\sigma_{0},\sigma_{1}\}(m',PRG_{sk},D)$

Input: Bits $m'$, Pseudorandom Generator PRG$_{sk}$, Distribution D

Output: Symbol $c_{i}$, Number of Embedded Bits $n_{i}$ $k\leftarrow\mathbf{1}_{\theta}(D),r\leftarrow PRG_{sk}.Next(),b=m'[0];$ $r'\leftarrow\begin{cases}r,&amp;if b=0\\1-r,&amp;if b=1\end{cases}$

if $r'&lt;D(\sigma_{1-k})$ then

$c_{i}\leftarrow\sigma_{1-k};$

if $\min(1-\theta,\theta)&lt;r\leq\max(1-\theta,\theta)$ then

$|n_{i}\leftarrow0;$

else

$|n_{i}\leftarrow1;$

else

$c_{i}\leftarrow\sigma_{k},n_{i}\leftarrow0;$

return $c_{i},n_{i}$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 7: Recovery $_{1_{\theta}(D)}^{\Sigma=\{\sigma_{0},\sigma_{1}\}}(c_{i},\mathrm{PRG}_{\mathrm{sk}},k)$

Input: Symbol $c_{i}$, Pseudorandom Generator PRG$_{sk}$, Knowledge k

Output: Bit $x\in\{0,1,\varepsilon\}$ $r\leftarrow\mathrm{PRG}_{\mathrm{sk}}.\mathrm{Next}()$;

if $c_{i}=\sigma_{k}$ then

$|x\leftarrow\varepsilon;$

else

if $r\leq\min(1-\theta,\theta)$ then

$|x\leftarrow0;$

else

if $r&gt;\max(1-\theta,\theta)$ then

$|x\leftarrow1;$

else

$|x\leftarrow\varepsilon;$

return x
</div>

We now directly present the corresponding Sample and Recovery algorithms in Algorithms 6 and 7. Consistent with the above analysis, it is straightforward to verify that the resulting scheme is both secure and correct, and thus constitutes a weakly asymmetric steganography scheme under knowl edge function $f = { \bf 1 } _ { \boldsymbol { \theta } } ( \cdot )$ . The capacity of this scheme is given by

$$
C _ {\mathbf {1} _ {\theta}} = \min \left(D (\sigma_ {1 - k}), \theta , 1 - \theta\right).
$$

Since $D ( \sigma _ { k } ) \geq \operatorname* { m i n } ( \theta , 1 - \theta )$ , we have

$$
C _ {\mathbf {1} _ {\theta}} = \min \left(D (\sigma_ {1 - k}), D (\sigma_ {k}), \theta , 1 - \theta\right) = \min \left(D _ {\min}, \theta , 1 - \theta\right).
$$

where $D _ { \operatorname* { m i n } } : = \operatorname* { m i n } \{ D ( \sigma _ { 0 } ) , D ( \sigma _ { 1 } ) \}$

<table><tr><td></td><td colspan="2">0 ≤ r &lt; min(θ, 1 - θ)</td><td></td><td colspan="2">max(θ, 1 - θ)</td></tr><tr><td>b = &#x27;0&#x27;</td><td>σ1-k</td><td>?</td><td rowspan="2">?</td><td colspan="2">σk</td></tr><tr><td>b = &#x27;1&#x27;</td><td colspan="2">σk</td><td>?</td><td>σ1-k</td></tr><tr><td colspan="4">D(σk) ≥ min(θ, 1 - θ)</td><td colspan="2">1 - D(σk) ≤ max(θ, 1 - θ)</td></tr></table>

Figure 4: Illustration of the recovery procedure.

## 4.3 Scheme Design under Rank Knowledge

In this section, we study scheme design under rank-based knowledge over general alphabets $\Sigma = \{ \sigma _ { 0 } , \hdots , \sigma _ { | \Sigma | - 1 } \}$

In this setting, the receiver’s knowledge consists of an ordering of symbols induced by the conditional distribution. We begin with the case of full rank knowledge, where the receiver has knowledge of the complete ordering over the alphabet. Formally, this is represented by a knowledge function $f = \mathsf { r a n k } ( \cdot )$ which maps a distribution D over the alphabet Σ to a permutation

$$
\pi = \operatorname{rank} (D),
$$

such that

$$
D \left(\sigma_ {\pi (0)}\right) \geq D \left(\sigma_ {\pi (1)}\right) \geq \dots \geq D \left(\sigma_ {\pi (| \Sigma | - 1)}\right).
$$

We write $\Sigma ^ { \prime } = \pi ( \Sigma )$ to denote the list Σ ordered according to π, where $\Sigma ^ { \prime } [ i ] = \sigma _ { \pi ( i ) }$

We then extend the construction to partial rank knowledge, where the receiver only observes a restricted ordering over a subset of symbols. In this setting, the receiver’s knowledge is represented by

$$
\operatorname{PRank} (D) = (\hat {\pi}, \hat {\Sigma}),
$$

where ${ \hat { \Sigma } } \subseteq \Sigma$ denotes the subset of symbols whose relative order is known, and πˆ specifies the ordering over $\hat { \Sigma } .$

## 4.3.1 Full Rank Knowledge

Our basic idea is to recursively partition the alphabet Σ into two subsets whose total probability masses admit a relative ordering that can be inferred solely from rank knowledge, ensuring that at each recursive step the receiver can identify the higher-probability subset without accessing exact probability values. Consequently, we can recursively apply the sampling and recovery procedures for threshold knowledge with θ = 0.5, namely $\mathsf { S a m p l e } _ { 1 _ { 0 . 5 } }$ and $\mathsf { R e c o v e r y } _ { 1 _ { 0 . 5 } } ,$ to perform encoding and decoding over the two subsets. The recursion continues until a single symbol is selected on the sender side, or until all embedded bits have been recovered on the receiver side.

The partitioning rule is simple. For any list $\Sigma ^ { \prime }$ sorted in descending order of probability, we always have

$$
\sum_ {i \bmod 2 = 0} ^ {i <   | \Sigma^ {\prime} |} D (\Sigma^ {\prime} [ i ]) \geq \sum_ {i \bmod 2 = 1} ^ {i <   | \Sigma^ {\prime} |} D (\Sigma^ {\prime} [ i ]).
$$

Therefore, splitting $\Sigma ^ { \prime }$ by parity, as specified in Algorithm $^ { 8 , }$ induces two subsets whose total probability masses have a known ordering determined purely by rank information.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 8: ParitySplit( $\Sigma'$ )

Input: A sorted list  $\Sigma'$ 

Output: Two sublists ( $\sigma_{0}^{\prime}, \sigma_{1}^{\prime}$ )

 $\sigma_{0}^{\prime} \leftarrow \Sigma^{\prime}[0::2]$  // even-indexed elements;

 $\sigma_{1}^{\prime} \leftarrow \Sigma^{\prime}[1::2]$  // odd-indexed elements;

return ( $\sigma_{0}^{\prime}, \sigma_{1}^{\prime}$ )
</div>

The correctness of the scheme follows from the correct ness of the weakly asymmetric scheme under the knowledge function $f = { \bf 1 } _ { 0 . 5 }$ , which ensures correct bit recovery at each recursive step, while rank knowledge and the deterministic partitioning rule guarantee that the decoder’s recursion is fully synchronized with the sender’s. For security, an intuitive ex planation is as follows. At each recursive step, the probability that the $\mathsf { S a m p l e } _ { 1 _ { 0 . 5 } }$ selects a given subset is exactly equal to the total probability mass of that subset under the original distribution. As a result, the recursive procedure preserves the original distribution over symbols, and for any history H, secret bits m<sup>′</sup> and any symbol $\textstyle { \mathfrak {sigma } } \in \Sigma .$ , we still have

$$
\operatorname * {P r} _ {r _ {0}, r _ {1}, \ldots \leftarrow \text {Unif} [ 0, 1)} \bigl [ c _ {i} = \boldsymbol {\sigma} \mid \mathcal {H}, m ^ {\prime} \bigr ] = \mathcal {D} _ {\mathcal {H}} (\boldsymbol {\sigma}).
$$

The corresponding $\mathsf { S a m p l e } _ { \mathsf { r a n k } } ^ { \Sigma }$ and $\mathsf { R e c o v e r y } _ { \mathsf { r a n k } } ^ { \Sigma }$ are formalized in Algorithm 9 and Algorithm 10.

Capacity. At each recursive step, one bit is embedded if and only if the procedure descends into the lower-probability subset, as dictated by the behavior of the $\mathsf { S a m p l e } _ { 1 _ { 0 . 5 } }$ algorithm. Consequently, for any symbol $\sigma _ { \pi ( i ) }$ , the total number of embedded bits equals the number of times the lower-probability subset is selected along the recursion, which is exactly the number of ones in the binary representation of i.

Let $p _ { \pi ( i ) } = D ( \sigma _ { \pi ( i ) } )$ denote the probability of the i-th symbol in descending order. The expected embedding capacity is therefore

$$
C _ {\text { rank }} = \sum_ {i = 0} ^ {| \Sigma | - 1} p _ {\pi (i)} \cdot \operatorname{count} _ {1} (\operatorname{bin} (i)),
$$

where $\mathsf { c o u n t } _ { 1 } ( \mathsf { b i n } ( i ) )$ denotes the number of ones in the binary representation of i.

This capacity admits the following bounds:

$$
1 - p _ {\max} \leq C _ {\text { rank }} \leq H (D),
$$

where $p _ { \operatorname* { m a x } } = \operatorname* { m a x } _ { \sigma \in \Sigma } D ( \sigma )$ and $H ( D )$ denotes the entropy of D. The lower bound follows from the fact that every index $i \geq 1$ contains at least one one-bit. The upper bound holds since for all i,

$$
\operatorname{count} _ {1} (\operatorname{bin} (i)) \leq \log_ {2} (i + 1) \leq \log_ {2} \frac {1}{p _ {\pi (i)}},
$$

implying that the number of embedded bits per symbol does not exceed its information content.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 9: Sample $_{rank}^{\Sigma}(m', PRG_{sk}, D)$

Input: Bits $m'$, Pseudorandom Generator PRG$_{sk}$, Distribution $D$

Output: Symbol $c_i$, Number of Embedded Bits $n_i$ $n_i \leftarrow 0, \pi \leftarrow \text{rank}(D), \Sigma' \leftarrow \pi(\Sigma)$ // descending;
while $|\Sigma'| &gt; 1$ do

$(\sigma'_0, \sigma'_1) \leftarrow \text{ParitySplit}(\Sigma')$;
$D'(\sigma'_0) \leftarrow \frac{\sum_{x \in \sigma'_0} D(x)}{\sum_{x \in \Sigma'} D(x)}$;
$D'(\sigma'_1) \leftarrow \frac{\sum_{x \in \sigma'_1} D(x)}{\sum_{x \in \Sigma'} D(x)}$;
$\Sigma', b \leftarrow \text{Sample}_{\mathbf{1}_{0.5}}^{\Sigma = \{\sigma'_0, \sigma'_1\}} (m'[n_i:], PRG_{sk}, D')$;
$n_i \leftarrow n_i + b$;

$c_i \leftarrow \Sigma'[0]$;
return $c_i, n_i$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 10: Recovery $_{rank}^{\Sigma}(c_{i}, PRG_{sk}, \pi)$ 

Input: Symbol  $c_{i}$ , Pseudorandom Generator  $PRG_{sk}$ , Rank Knowledge  $\pi$ 

Output: Bits x

 $x \leftarrow \varepsilon, \Sigma' \leftarrow \pi(\Sigma)$  // descending;

while  $|\Sigma'| &gt; 1$  do

 $(\sigma_{0}', \sigma_{1}') \leftarrow \text{ParitySplit}(\Sigma');$ 

k = 0; //  $\Pr(\sigma_{0}') \geq \Pr(\sigma_{1}')$ $c_{i}' \leftarrow \begin{cases} \sigma_{0}', &amp; \text{if } c_{i} \in \sigma_{0}' \\ \sigma_{1}', &amp; \text{if } c_{i} \in \sigma_{1}' \end{cases}$ $x \leftarrow x \|Recovery_{1_{0.5}}^{\Sigma=\{\sigma_{0}',\sigma_{1}'\}}(c_{i}', PRG_{sk}, k), \Sigma' \leftarrow c_{i}';$ 

return x
</div>

## 4.3.2 Partial Rank Knowledge

We next consider partial rank knowledge PRank(·), where the receiver only observes an ordering πˆ over a subset of symbols ${ \hat { \Sigma } } \subseteq \Sigma$

Our key idea is simple: information is embedded only when the sampled symbol lies in $\hat { \Sigma } .$ . Otherwise, the sender samples a symbol outside Σ<sup>ˆ</sup> without embedding any bit. Concretely, the sender first draws a fresh random value $r \gets \mathrm { U n i f } [ 0 , 1 )$ (which is not shared with the receiver) and compares it with the total probability mass

$$
p _ {\hat {\Sigma}} := \sum_ {\sigma \in \hat {\Sigma}} D (\sigma).
$$

If $r > p _ { \hat { \Sigma } }$ , the sender outputs a symbol from $\Sigma \backslash \hat { \Sigma }$ according to the distribution D restricted to and renormalized on $\Sigma \backslash { \hat { \Sigma } } ,$ , and no bit is embedded. Otherwise, the sender renormalizes $D$ onto $\hat { \Sigma }$ to obtain $D _ { \hat { \Sigma } } ,$ and applies the full-rank scheme $\mathsf { S a m p l e } _ { \mathsf { r a n k } } ^ { \hat { \Sigma } }$ on the restricted alphabet $\hat { \Sigma }$ to embed bits and sample a symbol.

If the received symbol $c _ { i } \notin \hat { \Sigma } ,$ , the Recovery outputs $\varepsilon ;$ otherwise, it decodes using the full rank recovery $\mathsf { R e c o v e r y } _ { \mathsf { r a n k } }$ under knowledge πˆ. The corresponding sampling and recovery procedures are given in $\mathsf { S a m p l e } _ { \mathsf { P R a n k } }$ (Algorithm 11) and $\mathsf { R e c o v e r y } _ { \mathsf { P R a n k } }$ (Algorithm 12). Correctness and security of the resulting scheme follow directly from those of the fullrank construction. Top-k knowledge arises as a special case by restricting $\hat { \Sigma }$ to the top-k symbols.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 11: Sample $_{PRank}^{\Sigma}(m', PRG_{sk}, D)$

Input: Bits $m'$, Pseudorandom Generator PRG$_{sk}$, Distribution $D$

Output: Symbol $c_i$, Number of Embedded Bits $n_i$ ($\hat{\pi}, \hat{\Sigma}$) ← PRRank($D$);

$r \leftarrow$ Unif[0,1), $p_{\hat{\Sigma}} \leftarrow \sum_{\sigma \in \hat{\Sigma}} D(\sigma)$;

if $r &gt; p_{\hat{\Sigma}}$ then

    Sample $c_i \sim \text{Normalize}(D, \Sigma \setminus \hat{\Sigma})$;
    $n_i \leftarrow 0$

else

    $D_{\hat{\Sigma}} \leftarrow \text{Normalize}(D, \hat{\Sigma})$ $c_i, n_i \leftarrow \text{Sample}_{\text{rank}}^{\hat{\Sigma}}(m', PRG_{sk}, D_{\hat{\Sigma}})$

return $c_i, n_i$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 12: Recovery $_{PRank}^{\Sigma}(c_{i}, PRG_{sk}, (\hat{\pi}, \hat{\Sigma}))$ 

Input: Symbol  $c_{i}$ , Pseudorandom Generator  $PRG_{sk}$ , Partial Rank Knowledge ( $\hat{\pi}, \hat{\Sigma}$ )

Output: Bits x

if  $c_{i} \notin \hat{\Sigma}$  then

 $\lfloor$  return  $\varepsilon$ 

else

 $\lfloor x = Recovery_{rank}^{\hat{\Sigma}}(c_{i}, PRG_{sk}, \hat{\pi})$ 

return x
</div>

## 5 Experiments

In this section, we evaluate our rank-based weakly asymmetric steganography schemes in language-model-based text steganography.

We conduct two sets of experiments. First, we consider the setting directly captured by our model, where the receiver is given only rank-based knowledge. In particular, we evaluate both full-rank knowledge and partial-rank knowledge, where the receiver only observes the ordering of the top-k tokens.

Second, we study a distribution-mismatch setting in which the sender and the receiver run the same language model under different numerical precisions. This setting is outside the formal model, but is motivated by the approximate and noisy forms of receiver-side information discussed earlier, where decoding based on coarse knowledge such as ordering may be less sensitive to perturbations than decoding based on exact probability values.

## 5.1 Receiver with Partial Channel Knowledge

Setup For the channel distribution, we use two open-source language models: Meta-Llama-3-8B-Instruct<sup>3</sup> and Qwen2.5- 7B-Instruct<sup>4</sup>. The sender accesses the conditional distribution by running the language model directly. To simulate the receiver’s limited channel knowledge in the weakly asymmetric setting, we compute the full conditional distribution using the same language model, but provide the receiver only with the corresponding rank-based knowledge for decoding. We fix the prompt “Tell me something about steganography” as the history. Each stegotext is generated as a response to this prompt, and generation terminates when the language model produces an end-of-sequence token.

As baselines, we include asymmetric steganography and random sampling. Symmetric steganography schemes are not included as baselines, since they require full distribution access at the receiver and thus fall outside the weakly asymmetric setting. For asymmetric steganography, we use the Undetectable Steganography scheme [26], based on the official implementation<sup>5</sup>, with the default threshold parameter $t = 2$ . To avoid penalizing this baseline due to implementation inefficiencies, we apply minor implementation-level optimizations while preserving the original algorithmic behavior. These optimizations affect only runtime efficiency and do not change the reported non-runtime evaluation metrics. Random sampling is implemented using torch.multinomial.

We evaluate both the full-rank scheme and partial-rank schemes. For partial-rank knowledge, the receiver is restricted to the relative ordering of only the top-2, top-5, or top-10 tokens. The stateful PRG used in all rank-based weakly asymmetric schemes follows the same construction as in the classical Meteor scheme [17] and is implemented via HMAC-DRBG, with a precision of 52 bits.

All experiments are conducted on a single RTX 5880 Ada GPU with 48GB VRAM. For each experimental configuration, we generate 1,000 responses. The hiddentext and key are independently re-sampled for each response. The decoding is performed directly at the token level, without converting tokens back to text, in order to avoid ambiguities introduced by text-level representations.

Metrics. Capacity. We report the average number of embedded bits per response (Capacity), the average empirical entropy per response (Emp. Entropy), computed as the sum of token-wise entropies along the Encode process, and the utilization ratio (Util.), defined as Capacity divided by Emp. Entropy [11]. Time. We measure the average encoding and decoding time per response (Enc. Time and Dec. Time), which include both language model inference and steganographic operations. Other metrics. We also report the average length of the generated stegotext in number of tokens (Length) and the decoding correctness (Correct.), measured as the fraction of responses that are decoded correctly.

Results and Analysis. Table 1 summarizes the experimental results. A concrete example of generated stegotext under full-rank knowledge is provided in Appendix A. Rank-based weakly asymmetric steganography incurs only modest additional computational overhead compared to random sampling in our experiments. Across both language models, the generated text length and empirical entropy remain similar to those of random sampling, which is consistent with the proposed schemes preserving the natural generation behavior of the underlying language models.

The results also highlight a clear capacity gap between rank-based weakly asymmetric steganography and the fully asymmetric baseline. Undetectable steganography embeds only a few bits per response, whereas our rank-based schemes embed tens to hundreds of bits per response. In particular, even top-2 ordering information already brings a meaningful capacity gain, suggesting that intermediate receiver-side channel knowledge can be useful.<sup>6</sup>Overall, these results support the study of weakly asymmetric steganography as a meaningful setting between symmetric and fully asymmetric steganography.

## 5.2 Receiver under Distribution Mismatch

The previous subsection evaluates the setting where the receiver is explicitly given limited rank-based channel knowledge. We now consider a related but different scenario motivated by precision-induced distribution mismatch, where the receiver may obtain a perturbed version of the sender’s conditional distribution rather than the exact distribution itself.

In symmetric steganography, decoding correctness typi cally requires the receiver to reconstruct the same conditional distributions used by the sender at each generation step. Numerical discrepancies between the sender-side and receiverside distributions may therefore lead to decoding errors. In contrast, weakly asymmetric steganography decodes from coarse knowledge such as ordering, rather than exact probability values. As a result, as long as this knowledge remains consistent, decoding can remain reliable even when the underlying distribution changes. From this perspective, weakly asymmetric steganography can be viewed as a steganography model with improved numerical robustness.

Thus, we consider a language-model-based text steganography setting in which the sender and receiver run the same language model under different numerical precisions. Specif ically, the sender uses float32 precision, while the receiver performs inference and decoding under float16 precision, inducing a perturbation to the channel distribution. This setting is practically motivated, as float16 inference significantly reduces memory consumption and is commonly adopted under resource constraints.

Setup The experimental setup largely follows that of the previous subsection. We use the same language models, prompt, number of trials, and experimental hardware as before. Here, we focus only on the differences.

Unlike the standard setting where the sender and the receiver access identical channel distributions, we introduce a numerical asymmetry between the two parties. Specifically, the sender obtains the channel distribution by running the language model under float32 precision, while the receiver performs inference and decoding using the same model under float16 precision. For the asymmetric baseline, we reuse the results reported in Table 1, as its decoding does not depend on receiver-side channel distributions. In addition to asymmetric and random-sampling baselines, we include several symmetric steganography schemes for comparison, including Meteor (16-bit precision) [17], Discop (Huffman) [11], and SparSamp (32-bit) [24]. For fairness, all schemes use pseudorandomness generated via the same HMAC-DRBG construction.

To make token-level accuracy and edit distance more informative in the distribution-mismatch experiments, we use a simple fixed-budget PRG synchronization rule for our proposed schemes. In our rank-based schemes, different tokens may consume different numbers of PRG outputs. Under distribution mismatch, a local token-level error can therefore desynchronize the PRG states and cause cascading errors in later tokens.

To isolate such local errors, we fix the number of PRG outputs consumed per generated token: both sampling and recovery consume the same budget, discarding unused outputs when necessary. The budget is set to the maximum number of PRG outputs required to process one token in the corresponding implementation. This rule does not change the sampling or recovery decisions; it only fixes the PRG advancement schedule, so that token accuracy and edit distance better reflect local decoding errors. Response-level accuracy is largely unaffected, since exact response recovery already fails once any embedded-token error occurs.<sup>7</sup>

<table><tr><td rowspan="2">Model</td><td rowspan="2">Scheme</td><td colspan="3">Capacity Metrics</td><td colspan="2">Time Metrics</td><td rowspan="2">Length</td><td rowspan="2">Correct.↑</td></tr><tr><td>Capacity (bit/resp.)↑</td><td>Emp. Entropy (bit/resp.)</td><td>Util.↑</td><td>Enc. Time (s/resp.)↓</td><td>Dec. Time (s/resp.)↓</td></tr><tr><td rowspan="6">LLAMA 3 |Σ| ≈ 128k</td><td>Random Sampling</td><td>-</td><td>392.681</td><td>-</td><td>18.798</td><td>18.385</td><td>497.273</td><td>-</td></tr><tr><td>Undet. (t = 2) [26]</td><td>2.530</td><td>388.932</td><td>0.65%</td><td>21.507</td><td>0.143</td><td>494.819</td><td>61.8%</td></tr><tr><td>Rank (Full)</td><td>111.223</td><td>391.070</td><td>28.44%</td><td>20.662</td><td>19.115</td><td>497.441</td><td>100.0%</td></tr><tr><td>Rank (Top10)</td><td>95.067</td><td>386.317</td><td>24.61%</td><td>19.115</td><td>18.699</td><td>492.808</td><td>100.0%</td></tr><tr><td>Rank (Top5)</td><td>83.374</td><td>392.303</td><td>21.25%</td><td>19.215</td><td>18.884</td><td>498.172</td><td>100.0%</td></tr><tr><td>Rank (Top2)</td><td>49.855</td><td>390.106</td><td>12.78%</td><td>18.915</td><td>18.753</td><td>495.921</td><td>100.0%</td></tr><tr><td rowspan="6">QWEN 2.5 |Σ| ≈ 152k</td><td>Random Sampling</td><td>-</td><td>589.486</td><td>-</td><td>18.610</td><td>18.137</td><td>520.575</td><td>-</td></tr><tr><td>Undet. (t = 2)</td><td>2.305</td><td>590.922</td><td>0.39%</td><td>25.384</td><td>0.171</td><td>519.993</td><td>61.6%</td></tr><tr><td>Rank (Full)</td><td>170.589</td><td>588.066</td><td>29.01%</td><td>20.486</td><td>18.815</td><td>518.845</td><td>100.0%</td></tr><tr><td>Rank (Top10)</td><td>142.931</td><td>594.132</td><td>24.06%</td><td>19.132</td><td>18.702</td><td>522.571</td><td>100.0%</td></tr><tr><td>Rank (Top5)</td><td>118.122</td><td>597.423</td><td>19.77%</td><td>19.147</td><td>18.808</td><td>525.972</td><td>100.0%</td></tr><tr><td>Rank (Top2)</td><td>63.302</td><td>590.385</td><td>10.72%</td><td>18.748</td><td>18.580</td><td>521.248</td><td>100.0%</td></tr></table>

Table 1: Experimental results for rank-based weakly asymmetric steganography under partial channel knowledge in languagemodel-based text steganography.

Metrics. Unless otherwise specified, we use the same eval uation metrics as in the previous subsection. Here, we additionally report the following correctness metrics.

Correctness Metrics. Token Acc. measures the fraction of tokens for which the decoded bits match the embedded bits. Resp. Acc. measures the fraction of responses for which token-level decoding is correct at every generated token. ED reports the average edit distance between the decoded bitstring and the embedded bitstring, i.e., the minimum number of single-bit insertions, deletions, and substi tutions required to transform the decoded bitstring into the embedded bitstring. For each response, we compute ED using Levenshtein.distance from the Python Levenshtein package.

Results and Analysis. Table 2 reports the experimental results. This setting is designed to evaluate how different steganography schemes trade off embedding capacity and decoding robustness when the receiver cannot accurately recover the conditional distributions, and is particularly challenging for schemes that rely on precise numerical agreement at the receiver.

While symmetric schemes typically achieve high embedding capacity and entropy utilization, their correctness degrades substantially when precise numerical distributions are unavailable. In particular, several symmetric schemes exhibit lower token-level accuracy, larger edit distance, and nearzero response-level decoding success, indicating a strong dependence on accurate probability values. Non-instantaneous schemes, such as SparSamp, are especially sensitive to such distributional deviations, since decoding errors may accumulate across sampling steps.<sup>8</sup>

In contrast, rank-based weakly asymmetric steganography sacrifices part of the embedding capacity in exchange for significantly improved robustness. Weakly asymmetric schemes maintain token-level accuracy above 99% across all rank settings, together with substantially lower edit distance. Moreover, in our experiments, these schemes embed substantially more bits per response than the fully asymmetric baseline while retaining meaningful response-level decoding accuracy.<sup>9</sup> This robustness stems from the fact that decoding depends only on rank-based channel knowledge, which is generally more stable than exact probability values under numerical perturbations. The combination of high token-level accuracy and low edit distance further suggests that rankbased weakly asymmetric steganography has the potential to achieve stronger response-level reliability with lightweight

<table><tr><td rowspan="2">Model</td><td rowspan="2">Type</td><td rowspan="2">Scheme</td><td colspan="3">Capacity Metrics</td><td colspan="2">Time Metrics</td><td rowspan="2">Length</td><td colspan="3">Correct. Metrics</td></tr><tr><td>Embed.(bit/resp.)↑</td><td>Entropy(bit/resp.)</td><td>Util.↑</td><td>Enc. Time(s/resp.)↓</td><td>Dec. Time(s/resp.)↓</td><td>TokenAcc.↑</td><td>Resp.Acc.↑</td><td>ED↓</td></tr><tr><td rowspan="9">LLAMA 3|Σ| ≈ 128k</td><td>R.</td><td>Random.</td><td>-</td><td>391.773</td><td>-</td><td>19.007</td><td>9.979</td><td>499.007</td><td>-</td><td>-</td><td>-</td></tr><tr><td>S.</td><td>Meteor</td><td>207.9</td><td>385.581</td><td>53.9%</td><td>19.210</td><td>10.566</td><td>496.397</td><td>99.10%</td><td>1.8%</td><td>7.439</td></tr><tr><td>S.</td><td>Discop(Huff.)</td><td>304.6</td><td>387.701</td><td>78.6%</td><td>40.117</td><td>31.297</td><td>495.700</td><td>88.54%</td><td>0.9%</td><td>40.848</td></tr><tr><td>S.</td><td>Sparsamp</td><td>353.6</td><td>387.782</td><td>91.2%</td><td>18.942</td><td>10.361</td><td>496.045</td><td>-</td><td>0.1%</td><td>218.029</td></tr><tr><td>A.</td><td>Undet. (t=2)</td><td>2.5</td><td>388.932</td><td>0.65%</td><td>21.507</td><td>0.143</td><td>494.819</td><td>-</td><td>61.8%</td><td>-</td></tr><tr><td>W-A.</td><td>Rank (Full)</td><td>111.6</td><td>391.291</td><td>28.5%</td><td>20.576</td><td>10.518</td><td>498.091</td><td>99.69%</td><td>21.9%</td><td>1.888</td></tr><tr><td>W-A.</td><td>Rank (Top10)</td><td>96.0</td><td>389.432</td><td>24.7%</td><td>19.321</td><td>10.390</td><td>497.888</td><td>99.81%</td><td>39.3%</td><td>0.984</td></tr><tr><td>W-A.</td><td>Rank (Top5)</td><td>82.5</td><td>386.481</td><td>21.3%</td><td>19.191</td><td>10.348</td><td>496.653</td><td>99.85%</td><td>48.3%</td><td>0.775</td></tr><tr><td>W-A.</td><td>Rank (Top2)</td><td>49.6</td><td>389.758</td><td>12.7%</td><td>19.068</td><td>10.366</td><td>497.812</td><td>99.86%</td><td>50.6%</td><td>0.668</td></tr><tr><td rowspan="9">QWEN 2.5|Σ| ≈ 152k</td><td>R.</td><td>Random.</td><td>-</td><td>589.813</td><td>-</td><td>18.739</td><td>9.708</td><td>519.851</td><td>-</td><td>-</td><td>-</td></tr><tr><td>S.</td><td>Meteor</td><td>311.8</td><td>577.263</td><td>54.0%</td><td>18.683</td><td>10.206</td><td>512.867</td><td>98.72%</td><td>0.3%</td><td>10.535</td></tr><tr><td>S.</td><td>Discop(Huff.)</td><td>481.3</td><td>587.834</td><td>81.9%</td><td>46.471</td><td>36.788</td><td>518.430</td><td>79.04%</td><td>0.0%</td><td>83.220</td></tr><tr><td>S.</td><td>Sparsamp</td><td>550.1</td><td>598.026</td><td>92.0%</td><td>18.939</td><td>10.284</td><td>525.455</td><td>-</td><td>0.0%</td><td>399.092</td></tr><tr><td>A.</td><td>Undet. (t=2)</td><td>2.3</td><td>590.922</td><td>0.39%</td><td>25.384</td><td>0.171</td><td>519.993</td><td>-</td><td>61.6%</td><td>-</td></tr><tr><td>W-A.</td><td>Rank (Full)</td><td>171.7</td><td>588.504</td><td>29.2%</td><td>20.377</td><td>10.356</td><td>517.914</td><td>99.48%</td><td>9.2%</td><td>3.367</td></tr><tr><td>W-A.</td><td>Rank (Top10)</td><td>142.4</td><td>590.094</td><td>24.1%</td><td>18.980</td><td>10.216</td><td>519.504</td><td>99.68%</td><td>18.8%</td><td>1.826</td></tr><tr><td>W-A.</td><td>Rank (Top5)</td><td>117.2</td><td>593.762</td><td>19.7%</td><td>18.965</td><td>10.256</td><td>522.688</td><td>99.76%</td><td>28.8%</td><td>1.316</td></tr><tr><td>W-A.</td><td>Rank (Top2)</td><td>62.8</td><td>587.200</td><td>10.7%</td><td>18.652</td><td>10.158</td><td>518.992</td><td>99.83%</td><td>40.2%</td><td>0.875</td></tr></table>

Table 2: Experimental results under distribution mismatch (float32 sender vs. float16 receiver) for symmetric, asymmetric, and rank-based weakly asymmetric steganography in language-model-based text steganography.

error-correction mechanisms.

Overall, these results further support the potential of weakly asymmetric steganography in settings where the receiver cannot reliably recover the exact conditional distributions.

## 6 Discussion

Real-world applicability. Weakly asymmetric steganography targets the intermediate regime between symmetric and fully asymmetric steganography. Its most direct application is when the receiver’s capability is explicitly restricted to a given form of knowledge, for example when an interface exposes only limited features of the underlying distribution, such as top-k candidates together with their relative ordering. It may also apply when such knowledge is not directly provided but can be inferred from indirect access, such as by using repeated samples and statistical testing to recover coarse distributional properties with high probability. Finally, weakly asymmetric steganography provides a useful basis for settings where exact symmetry between the sender’s and receiver’s distributions is difficult to maintain, for example due to numerical precision, hardware, or implementation differences. In these cases, relying on partial knowledge can be more robust than requiring exact probability agreement, while still exploiting more information than fully asymmetric schemes. It may also serve as a starting point for more practical designs that further improve reliability under such imperfect conditions.

## 7 Conclusion

We introduced weakly asymmetric steganography, a new model that captures settings where the receiver possesses partial channel knowledge. We showed that such partial knowledge can be explicitly exploited by constructing provably secure steganography schemes under representative knowledge, including threshold-based knowledge in binary alphabets and rank-based knowledge in general alphabets. Our experimental results in language-model-based text steganography further suggest the potential of this approach under restricted receiver access and distribution mismatch.

## Acknowledgments

This work was supported by the National Natural Science Foundation of China under Grant Nos. U2336208 and 12025104.

## Ethical Considerations

This section outlines the ethical considerations of our research, following a stakeholder-based analysis.

Stakeholder Analysis and Process Impact Our stakeholders include the research team, future researchers, potential users of steganographic systems, security professionals, and the public. The research team benefits from a clearer formal ization of weakly asymmetric steganography, but also bears responsibility for communicating its assumptions, limita tions, and dual-use implications accurately. Future researchers may benefit from a more precise model for studying partialknowledge steganography, but this model could also inform the design of stronger covert channels. Potential users of steganographic systems, including benign users who rely on private communication, may benefit from better-understood security guarantees, but could be harmed if they overestimate the practical protection provided by theoretical schemes. Security professionals may benefit from a more accurate characterization of steganographic capabilities under partial knowledge, which can support defensive analysis and policy discussion, but may face increased challenges if such techniques are adapted faster than corresponding defenses. The public may benefit from improved scientific understanding and better informed security governance, but could be harmed if the resulting ideas are used for illicit, illegal, or harmful activities.

The research process itself posed limited direct risk. The work is primarily theoretical: we formalize a model, prove security/correctness properties, and evaluate controlled in stantiations using public models and synthetic generations. We did not collect personal data, involve human subjects, or interact with real users, production systems, or sensitive infrastructure.

Impact of the Publication The publication has both positive and negative implications. On the positive side, it gives the community a more realistic framework for reasoning about covert communication when receivers have partial, rather than full or zero, channel knowledge. This can improve both scientific understanding and defensive analysis by clarifying what kinds of partial access may already be enough to enable nontrivial steganography. On the negative side, like most steganography research, it could inform the design of more practical covert channels.

Mitigation To mitigate this risk, we frame the contribution as foundational analysis rather than a deployment recipe; we explicitly state the assumptions and limitations of the weakly asymmetric model so its practical utility is not overstated; and we evaluate only controlled, public-resource instantiations.

Justification for Research We believe conducting and publishing this work is justified because a precise understanding of the capabilities and limits of partial-knowledge steganography is necessary for both future defensive research and informed policy discussion. Any real-world deployment should undergo additional context-specific risk assessment and safeguards.

## Open Science

The artifact accompanying this paper is publicly available at: https://doi.org/10.5281/zenodo.20428322

The repository provides implementations of our rankbased weakly asymmetric steganography schemes, together with scripts for running the Section 5 experiments for these schemes.

## References

[1] Michael Backes and Christian Cachin. Public-key steganography with active attacks. In Theory of Cryp tography, Second Theory of Cryptography Conference, TCC 2005, Cambridge, MA, USA, February 10-12, 2005, Proceedings, Lecture Notes in Computer Science, pages 210–226. Springer, 2005.

[2] Minhao Bai, Jinshuai Yang, Kaiyi Pang, Xin Xu, Zhen Yang, and Yongfeng Huang. Provably robust and se cure steganography in asymmetric resource scenario. In IEEE Symposium on Security and Privacy, SP 2025, San Francisco, CA, USA, May 12-15, 2025, pages 1438– 1456. IEEE, 2025.

[3] Sebastian Berndt and Maciej Liskiewicz. Provable secure universal steganography of optimal rate: Provably secure steganography does not necessarily imply one-way functions. In Proceedings of the 4th ACM Workshop on Information Hiding and Multimedia Secu rity, IH&MMSec 2016, Vigo, Galicia, Spain, June 20-22, 2016, pages 81–92. ACM, 2016.

[4] Sebastian Berndt and Maciej Liskiewicz. On the gold standard for security of universal steganography. In Advances in Cryptology - EUROCRYPT 2018 - 37th Annual International Conference on the Theory and Applications of Cryptographic Techniques, Tel Aviv, Israel, April 29 - May 3, 2018 Proceedings, Part I, Lec ture Notes in Computer Science, pages 29–60. Springer, 2018.

[5] Manuel Blum and Silvio Micali. How to generate cryptographically strong sequences of pseudo random bits. In 23rd Annual Symposium on Foundations ofComputer Science, Chicago, Illinois, USA, 3-5 November 1982, pages 112–117. IEEE Computer Society, 1982.

[6] Dan Boneh and Victor Shoup. A Graduate Course in Applied Cryptography. 2023. Version 0.6, January 2023. URL: https://toc.cryptobook.us/.

[7] Mark Chen, Alec Radford, Rewon Child, Jeffrey Wu, Heewoo Jun, David Luan, and Ilya Sutskever. Genera tive pretraining from pixels. In Proceedings ofthe 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event, Proceedings of Machine Learning Research, pages 1691–1703. PMLR, 2020.

[8] Miranda Christ and Sam Gunn. Pseudorandom error correcting codes. In Advances in Cryptology - CRYPTO 2024 - 44th Annual International Cryptology Conference, Santa Barbara, CA, USA, August 18-22, 2024, Proceedings, Part VI, Lecture Notes in Computer Science, pages 325–347. Springer, 2024.

[9] Miranda Christ, Sam Gunn, and Or Zamir. Undetectable watermarks for language models. In The Thirty Seventh Annual Conference on Learning Theory, June 30 - July 3, 2024, Edmonton, Canada, Proceedings of Machine Learning Research, pages 1125–1139. PMLR, 2024.

[10] Nenad Dedic, Gene Itkis, Leonid Reyzin, and Scott Russell. Upper and lower bounds on black-box steganography. J. Cryptol., 22(3):365–394, 2009.

[11] Jinyang Ding, Kejiang Chen, Yaofei Wang, Na Zhao, Weiming Zhang, and Nenghai Yu. Discop: Provably secure steganography in practice based on "distribution copies". In 44th IEEE Symposium on Security and Privacy, SP 2023, San Francisco, CA, USA, May 21-25, 2023, pages 2238–2255. IEEE, 2023.

[12] Phillipa Gill, Masashi Crete-Nishihata, Jakub Dalek, Sharon Goldberg, Adam Senft, and Greg Wiseman. Characterizing web censorship worldwide: Another look at the opennet initiative data. ACM Trans. Web, 9(1):4:1– 4:29, 2015.

[13] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, et al. The llama 3 herd of models. CoRR, abs/2407.21783, 2024. arXiv:2407.21783.

[14] Horace He and Thinking Machines Lab. Defeating nondeterminism in llm inference. Thinking Machines Lab: Connectionism, 2025. URL: https://thinkingmachines.ai/blog/ defeating-nondeterminism-in-llm-inference/.

[15] Nicholas J. Hopper. Toward a Theory of Steganography. Ph.D. dissertation, technical report CMU-CS-04-157, Carnegie Mellon University, Pittsburgh, PA, USA, July 2004.

[16] Nicholas J. Hopper, John Langford, and Luis von Ahn. Provably secure steganography. In Advances in Cryptology - CRYPTO 2002, 22nd Annual International Cryptology Conference, Santa Barbara, California, USA, August 18-22, 2002, Proceedings, Lecture Notes in Computer Science, pages 77–92. Springer, 2002.

[17] Gabriel Kaptchuk, Tushar M. Jois, Matthew Green, and Aviel D. Rubin. Meteor: Cryptographically secure steganography for realistic distributions. In CCS ’21: 2021 ACM SIGSAC Conference on Computer and Communications Security, Virtual Event, Republic ofKorea, November 15 - 19, 2021, pages 1529–1548. ACM, 2021.

[18] Tri Van Le. Efficient provably secure public key steganography. IACR Cryptol. ePrint Arch., 2003:156, 2003.

[19] Guorui Liao, Jinshuai Yang, Weizhi Shao, and Yongfeng Huang. A framework for designing provably secure steganography. In 34th USENIX Security Symposium, USENIX Security 2025, Seattle, WA, USA, August 13-15, 2025, pages 6837–6856. USENIX Association, 2025.

[20] Anna Lysyanskaya and Mira Meyerovich. Provably secure steganography with imperfect sampling. In Public Key Cryptography - PKC 2006, 9th International Conference on Theory and Practice of Public-Key Cryptography, New York, NY, USA, April 24-26, 2006, Proceedings, Lecture Notes in Computer Science, pages 123–139. Springer, 2006.

[21] OpenAI. GPT-4 technical report. CoRR, abs/2303.08774, 2023. arXiv:2303.08774.

[22] Ram Sundara Raman, Prerana Shenoy, Katharina Kohls, and Roya Ensafi. Censored planet: An internet-wide, longitudinal censorship observatory. In CCS ’20: 2020 ACM SIGSAC Conference on Computer and Communications Security, Virtual Event, USA, November 9-13, 2020, pages 49–66. ACM, 2020.

[23] Luis von Ahn and Nicholas J. Hopper. Public-key steganography. In Advances in Cryptology - EURO-CRYPT 2004, International Conference on the Theory and Applications of Cryptographic Techniques, Interlaken, Switzerland, May 2-6, 2004, Proceedings, Lecture Notes in Computer Science, pages 323–341. Springer, 2004.

[24] Yaofei Wang, Gang Pei, Kejiang Chen, Jinyang Ding, Chao Pan, Weilong Pang, Donghui Hu, and Weiming Zhang. Sparsamp: Efficient provably secure steganography based on sparse sampling. In 34th USENIX Security Symposium, USENIX Security 2025, Seattle, WA, USA, August 13-15, 2025, pages 6817–6835. USENIX Association, 2025.

[25] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu. Qwen2.5 technical report. CoRR, abs/2412.15115, 2024. arXiv:2412.15115.

[26] Or Zamir. Undetectable steganography for language models. Trans. Mach. Learn. Res., 2024.

## A Examples of Generated Stegotexts

This appendix provides examples of stegotexts generated using Rank(Full). The original outputs were in Markdown format; for readability, we converted the Markdown syntax into standard LaTeX formatting without changing the textual con tent.

## Prompt

Tell me something about steganography

## Llama 3

Steganography! It’s an intriguing field that’s both fascinating and potentially mischievous.

Steganography is the art and science of hiding secret messages, images, audio, or video within plain sight, where the hidden content is not immediately detectable. The goal is to conceal the existence of the hidden message, making it impossible for unauthorized parties to detect or intercept it.

Steganography has a long history, dating back to ancient civilizations, where it was used to conceal secret messages and military communications. In modern times, steganography has become popular in various domains, including:

1. Digital watermarking: Watermarks are embedded in digital images, audio, or video to prove ownership, track usage, or detect tampering.

2. Data hiding: Files, documents, or messages are encoded within seemingly innocuous data, such as images, emails, or text files.

3. Image steganography: Hidden information is embedded within digital images, often using techniques like frequency domain analysis or spatial domain encoding.

4. Audio steganography: Secret messages are concealed within audio files, using techniques like echo hiding, frequency masking, or spreadspectrum coding.

Steganography can be used for various purposes, including:

1. Secure communication: Steganography can provide an additional layer of security for sensitive information.

2. Copyright protection: Watermarks can be used to prove ownership and track unauthorized use.

3. Forensic analysis: Steganographic techniques can help investigators detect and reconstruct hidden evidence in digital forensic cases.

4. Art and entertainment: Steganography can be used to create interactive and engaging multimedia experiences.

However, steganography also has its limitations and potential drawbacks:

1. Detectability: Steganographic methods can be detectable using advanced analysis techniques, such as machine learning-based tools.

2. Capacity limitations: The amount of information that can be embedded within a host media (e.g., image or audio) is limited.

3. Error correction: Since steganographic data is hidden, errors during transmission or storage can be difficult to correct.

4. Legal implications: The use of steganography for unauthorized purposes, such as hiding illegal content, can lead to legal consequences.

In conclusion, steganography is an exciting and rapidly evolving field that offers new possibilities for secure communication, creative expression, and data protection. However, it’s essential to recognize the ethical and legal implications of using steganographic techniques and to ensure that they are used responsibly.

## Qwen 2.5

Steganography is the practice of hiding secret data within an ordinary, non-secret file or message to avoid detection. The term “steganography” comes from the Greek words “stegano-” (meaning covered or concealed) and “-graphy” (meaning writing). Unlike cryptography, which encrypts data to make it unreadable to unauthorized parties, steganography aims to keep the secret information hidden in plain sight on the surface of a digital file, image, or message.

Here are some key aspects of steganography:

1. Types of Data Hidden: Steganography can hide various types of data, including text, images, video, audio, and network packets. Common examples include hidden text inside an image or a video frame, where the human eye can’t immediately spot the alteration.

2. Media Used: While the most common media used for steganography are images, other media such as audio files, video files, and even executable files can also be used to hide data.

## 3. Common Techniques:

• Least Significant Bit (LSB) Replacement: This is a common technique in digital steganography. It involves replacing the least significant bits of a pixel’s color value with the bits of the secret message, without noticeably altering the appearance of the image to the naked eye.

• Insertion in Metadata: Steganographic data can also be embedded in the metadata of a file, such as EXIF data in images or MP3 tags in audio files.

• Splicing Techniques: This involves splitting the cover material into parts and redistributing them to hide data. For example, a secret message can be embedded by altering the last bit of specific bytes or even entire blocks of data.

## 4. Masking and Watermarking:

• Masking: This technique involves obscuring the embedded data using another type of cover data to make the hidden information less detectable.

• Watermarking: Similar to steganography, watermarking involves embedding a signal into a cover medium, but the purpose of watermarking is usually to detect or identify the presence of the signal rather than keeping it a secret.

5. Detection and Analysis: There are tools and methods to detect steganography, such as statistical analysis and machine learning techniques. However, more advanced forms of steganography can be difficult to detect without specialized knowledge.

6. Legal and Ethical Considerations: The use of steganography can have legal and ethical implications. It is often used for benign purposes like data transfer, but it can also be used for malicious activities such as spreading malware or hiding illegal content.

Steganography plays a significant role in cybersecurity and digital forensics. As technology advances, so do the methods and techniques used in both steganography and its detection.
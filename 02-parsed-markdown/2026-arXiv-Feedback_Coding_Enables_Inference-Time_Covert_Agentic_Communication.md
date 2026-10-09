# Feedback Coding Enables Inference-Time Covert Agentic Communication

Sidong Guo<sup>1</sup>, Sajani Vithana<sup>2</sup>, Atefeh Gilani<sup>3</sup>, Lalitha Sankar<sup>3</sup>, Oliver Kosut<sup>3</sup>, and Flavio P. Calmon<sup>2</sup>

<sup>1</sup>Georgia Institute of Technology <sup>2</sup>Harvard University <sup>3</sup>Arizona State University

## Abstract

As large language models (LLMs) are increasingly used to automate digital interactions, users can leverage LLM-generated text as cover for covert communication within seemingly benign conversations. Existing LLM steganography, however, is predominantly white-box, requiring the sender and receiver to share the cover statistics, typically through access to the model weights and prompt. Black-box schemes remove this requirement by allowing the receiver to operate solely on the generated text, but current approaches rely on fixed-length, open-loop watermarking techniques that sufer from high decoding error rates under variable-length token generation. We recast black-box LLM steganography as a sequential communication problem with causal, noiseless feedback: every generated token is observed by both parties and can guide subsequent embedding. Based on this perspective, we introduce Burnashev Adaptive Posterior Matching (BAM), a feedback-coding scheme that combines posterior matching with a decode-and-confirm phase. The design is inspired by classical information-theoretic feedback coding principles, while its security is established through a cryptographic reduction proof. Across three open-weight language models, we demonstrate that BAM attains 0-0.1% empirical message error on an 8-bit payload in around 50 tokens, across 1000 trials, versus 10-17% for the strongest black-box baseline at comparable length. Building on the proposed steganography algorithm, we demonstrate the feasibility of an end-to-end communication protocol that achieves high communication rates across multiple conversational settings.

## 1 Introduction

Steganography is the practice of embedding a secret payload into an innocuous covertext such that only an intended receiver can reliably recover the hidden message while an adversary cannot distinguish the resulting stegotext from an ordinary cover. Steganographic communication has been studied extensively in both the information-theoretic literature [1] and the cryptography literature [12]. Its asymptotic embedding capacity, under a wide range of cover distributions and distortion constraints, has been well characterized [21, 11, 26].

The success of generative models, particularly large language models (LLMs), has renewed interest in text steganography, where secret messages are embedded directly into LLM-generated text. One emerging application of generative steganography is the establishment of covert communication channels mediated by LLM agents. Users can leverage LLM systems as a cover to exchange hidden messages beneath an overt conversation that remains fluent and task-consistent, efectively evading surface-level content policing. This threat model encompasses multiple configurations: two humans using agents as proxies in AI-mediated conversations or a human coordinating with a proxy agent [15, 24, 19]. In these settings, human actors may leverage local control over the agent’s sampling loop to apply logit-steering algorithms, embedding secret messages directly into covertext to evade surface-level monitoring. This capability is becoming increasingly realistic, as suitable models can sustain dialogues suficiently natural to pass a standard three-party Turing test [19].

Realizing this threat, however, requires operating under strict practical constraints. Existing steganog raphy approaches can be broadly divided according to the information available to the message decoder. The dominant paradigm is white-box steganography, in which both encoder and decoder have access to the language model’s conditional next-token distribution, which often entails sharing model parameters and prompts. Representative methods include coupling-based approaches that construct a minimumentropy coupling between the message and cover distributions [9], sampling schemes that mask the message with pseudorandom bits and embed it through inverse-transform sampling of the model distribution [20], and arithmetic-coding-based approaches [40]. Despite their algorithmic diferences, these techniques require the sender and receiver to share the same cover statistics, an assumption that rarely holds for independently deployed LLM agents.

Consequently, realistic covert communication requires a black-box approach [39][31], where the receiver observes only the generated text and has no access to the underlying language model weights, prompt, or token probabilities. Yet, existing black-box techniques remain ill-suited for conversational steganography. Most recent works in this domain take the form of inference-time multi-bit watermarking [13, 38, 10, 8]. Viewed as communication systems, these methods are largely fixed-length and open-loop: the encoder converts messages to a fixed set of codewords without using the realized outputs to adapt future transmissions, and the decoder commits after a preset token budget. Consequently, fixed-length protocols fail in dynamic conversational settings due to two main limitations:

• High Decoding Errors at High Embedding Rates: Existing schemes can only reliably recover payloads at very low embedding rates. Attempting higher transmission rates dramatically increases decoding error, falling well short of the error-rate trade-ofs achieved by white-box alternatives.

• Inflexibility to Variable Turn Lengths: Natural conversational turns vary unpredictably in length. Fixed-length protocols sufer decoding failures when a turn terminates prematurely, and their fixed codebooks cannot eficiently adapt when a turn naturally extends beyond its expected budget.

To address these limitations, we develop a provably secure black-box steganographic scheme based on sequential feedback communication. The use of feedback in black-box steganography was previously explored by Zamir [39], who combines repeated single-symbol embedding with a feedback-based error correction mechanism to enable reliable multi-bit transmission. We construct a fully operational scheme by instead take an information-theoretic feedback-coding approach in which feedback directly governs the evolution of the code itself. Since every generated token is observed identically by both commu nicating agents, the encoder can reproduce the decoder’s state and adapt future codeword symbols to the realized transcript. Specifically, we construct a variable-length protocol that combines adaptive posterior matching [32] with a Yamamoto-Itoh confirmation mechanism [37]. Rather than encoding and correcting individual payload symbols separately, the protocol maintains a belief over the entire message space, adaptively selects subsequent channel inputs from this belief, and verifies tentative decisions through an explicit confirmation phase. This enables the token budget to adapt to the realized channel while achieving high rate eficiency and near-zero decoding error without requiring the decoder to access the underlying language model. We further extend this point-to-point protocol to conversational settings and demonstrate the feasibility of covert agentic communication in terms of reliability, rate, and quality.

## Contributions.

• We demonstrate the feasibility of inference-time covert agentic communication by modeling the blackbox steganographic channel as a communication channel with causal, noiseless feedback, providing a formal system model and empirical frameworks for evaluating this emerging threat (Section 3).

• We introduce Burnashev Adaptive Posterior Matching (BAM), a variable-length feedback coding scheme explicitly designed for the black-box setting. BAM combines a sequential probabilitymatching step to localize messages with a confirmation phase to verify tentative decisions. This architecture substantially improves reliability over existing baseline methods (Section 4).

• We provide a cryptographic reduction proving computational indistinguishability of the proposed system under pseudo-random function (PRF) security (Section 5).

• We develop and implement a practical conversational protocol that integrates BAM with natural turn-taking, early-stopping generation, and multi-turn payload transmission (Section 6).

• We conduct extensive evaluations across multiple language models, moving beyond standard multibit watermarking primitives to test interactive conversational settings. Our results demonstrate substantial improvements in embedding eficiency and decoding reliability (Section 7).

Taken together, this work establishes that eficient inference-time covert communication is highly feasible for conversational settings, even under prompt and model agnostic settings.

## 2 Background and Related Work

Information-Theoretic and Cryptographic Security Measures In this work, we evaluate our steganographic framework under both information-theoretic security adapted from Cachin [4] and cryptographic security. Information-theoretic security traditionally relies on notions of weak and strong secrecy to guarantee that the information leakage of a message is either vanishing on average or can be made arbitrarily small for unnormalized mutual information [35, 2]. Information-theoretic covert ness [1], on the other hand, requires statistical indistinguishability between covertext and stegotext. Because these measures assume a uniform message prior, modern frameworks combine covertness and strong secrecy by requiring the Kullback-Leibler divergence between the cover and stego distributions to be arbitrarily small for every message [4]. While Cachin’s framework establishes theoretical secrecy against a passive eavesdropper, it does not guard against an active adversary with API access. Consequently, provably secure steganographic frameworks also require distinguishing security [28], which ensures computational indistinguishability against any probabilistic polynomial-time adversary.

Inference-Time Multi-Bit Watermarking As opposed to training-time steganography, which embeds information during the training process, inference-time steganography often induces a coupling between cover and stegotext to ensure indistinguishability [9]. The core of our distortion-free guar antee builds on the optimal transport (OT) coupling of ArcMark [13]. Conceptually, ArcMark is an inference-time multi-bit watermarking technique that embeds information by projecting both the language model’s vocabulary and the hidden message symbols onto a unit circle. To transmit a message, the encoder biases the next token distribution to favor the selection of tokens that are positioned angularly closer to the target message symbol on the circle. To ensure the quality of generation, ArcMark formulates the channel synthesis process as an OT problem with distortion-free constraint. Solving this optimization minimizes the expected circular distance between the sampled tokens and the target messages, subject to a marginal constraint.

Information-Theoretic Feedback Coding By recognizing that autoregressive token generation naturally forms a channel with instantaneous feedback, our scheme adapts classical feedback principle, combining posterior matching [32] with a Yamamoto-Itoh-style confirmation phase [37]. Classical information-theoretic results establish that noiseless feedback, while not increasing the capacity of a memoryless channel [7], can dramatically improve reliability function (the rate at which decoding error decreases) through adaptive coding. Foundational results include Burnashev’s optimal reliabil ity exponent [3], Yamamoto-Itoh’s two-phase achievability strategy [37] and modern variable-length feedback coding schemes [29]. In addition to optimal exponent, posterior matching [32] provides a capacity-achieving sequential coding strategy in which the encoder selects channel inputs according to the decoder’s current posterior belief.

Covert Agentic Communication Our work is orthogonal to existing literature that focuses on eliciting, detecting, or evaluating the impact of deceptive agentic behaviors [25, 36, 16]. We approach this threat as a sequential communication and cryptographic security problem at inference time. Covert Agentic Communication therefore refers to the ability of LLM agent (either independent or prompted by human actors) to hide messages in generated texts in inference-time. Covert communication has emerged as a significant security concern within LLM-based multi-agent systems and AI-mediated interactions [15, 24], where [34] showed that covert communication between agents are possible in the absence of shared secret via cryptographic key exchange.

## 3 System Framework and Threat Model

## 3.1 Notations and Problem Setup

We use the following notations throughout the paper:

• Variables. Random variables and their realizations are denoted by uppercase and lowercase letters, respectively $( \mathrm { e . g . , } X$ and x). Let X take values in a finite alphabet X. For $n \in \mathbb N$ we write $X ^ { n } \ \triangleq \ ( X _ { 1 } , \ldots , X _ { n } ) \in \ X ^ { n }$ , and for $1 \leq i \leq j \leq n$ , we denote the subsequence by $X _ { i : j } \triangleq ( X _ { i } , \ldots , X _ { j } )$

• Parameters. Let $\mathcal { X }$ denote the token vocabulary with cardinality $| { \mathcal { X } } | = V$ . We denote by $s \subseteq \Delta ^ { V }$ the set of possible next-token distributions, where $\Delta ^ { V }$ is the probability simplex over V tokens. At token position t, the language model induces a distribution $S _ { t } = s _ { t } \in \mathcal S , S _ { t } \triangleq$ $P _ { X _ { t } | X _ { 1 : t - 1 } , \rho } ,$ determined by the model parameters, prompt $\rho ,$ and previously generated tokens $x ^ { t - \mathrm { { i } } } \ ( \mathrm { { w h e n } }$ clear from context, we suppress the dependence on $\rho$ in notation). A binary message of length ℓ is denoted by $m \in \mathcal { M } \triangleq \{ 0 , 1 \} ^ { \ell }$ , we use $\operatorname { i d x } ( m )$ to denote the corresponding message index (decimal representation). Each message is encoded into a codeword $U ^ { n } ( m ) \in \mathcal { U } ^ { n }$ (may be stochastic), where n denotes the (possibly variable) codeword length. We use τ to denote the length of generated text, where we require $n \leq \tau .$ We also use κ to denote shared seed and $K = k \in \mathcal { K }$ as generated keys.

• Metrics. The Kullback–Leibler (KL) divergence between probability mass functions $P _ { 1 }$ and $P _ { 2 }$ on $\mathcal { X }$ is

$$
\mathbb {D} (P _ {1} \| P _ {2}) \triangleq \sum_ {x \in \mathcal {X}} P _ {1} (x) \log \frac {P _ {1} (x)}{P _ {2} (x)}.\tag{1}
$$

Logarithms are taken to base 2. We use λ to denote the security parameter and $1 ^ { \lambda }$ its unary representation. A function negl(λ) is negligible if it vanishes faster than the reciprocal of every polynomial in λ. The communicating parties share a uniform secret seed $\kappa \in \{ 0 , 1 \} ^ { \lambda }$ . An API adversary is denoted by A. The binary decision event $\mathcal { A } ( 1 ^ { \lambda } ) = 1$ indicates that the adversary classifies the output as stegotext, whereas $\mathcal { A } ( 1 ^ { \lambda } ) = 0$ indicates it is classified as benign covertext.

## 3.2 System Model

The overall framework of the covert communication setup is depicted in Fig. 1, which illustrates a single token generation at token position t. An encoder receives the prompt and the secret message, which together with the accumulated history so far, determine the next-token distribution and the codeword symbol $u _ { t } ,$ respectively. The system then samples a token $x _ { t }$ from either the biased distribution or the clean distribution, which is subsequently observed by both the legitimate decoder and an external observer (Eve). We define the core LLM communication channel as follows:

![](images/5b11e63d1f3e0b4130936c2af92a9e4b9f0ae4df1157924d19ddae4eabf30233.jpg)  
Figure 1: System model for a single generated token at position t.

Definition 1 (LLM channel). An $L L M$ channel Model is a probabilistic sampling rule that, on input prompt ρ and token history $x ^ { t - 1 } \in \mathcal { X } ^ { t - 1 }$ , induces the next-token distribution $s _ { t }$ . Without hidden message embedding, it samples

$$
s _ {t} \leftarrow \mathsf {M o d e l} (\rho , x ^ {t - 1}), \qquad x _ {t} \sim W _ {X | S} (\cdot | s _ {t}),\tag{2}
$$

where $W _ { X \mid S } ( x _ { t } | s _ { t } )$ is the unbiased base sampling rule $( e . g .$ . Top-k with temperature 1.0). Given an embedding symbol $u _ { t } \in \mathcal { U }$ and key $k _ { t } \in \mathcal { K }$ , the steganographic sampler instead generates

$$
x _ {t} \sim W _ {X | U, K, S} (\cdot | u _ {t}, k _ {t}, s _ {t}).\tag{3}
$$

Definition 2 (Black-box steganographic scheme). A black-box steganographic scheme for an LLM channel Model is a tuple of probabilistic algorithms

$$
\Pi_ {\text { Model }} = \left(\text { KeyGen }, \text { Enc } _ {\text { Model }, K}, \text { Dec } _ {K}\right).\tag{4}
$$

The algorithms are defined as follows.

• KeyGen(1<sup>λ</sup>) takes a shared seed $\kappa \in \{ 0 , 1 \} ^ { \lambda }$ and outputs the secret keying material K used by the encoder and decoder.

$\mathsf { E n c } _ { \mathsf { M o d e l } , K } ( m , \rho ) \to x ^ { \tau }$ takes a message m $\in \mathcal { M }$ and prompt ρ, and outputs a variable-length stegotext $x ^ { \tau }$ . It has inference-time access to Model and its next-token distribution.

$\mathsf { D e c } _ { K } ( x ^ { \tau } ) \to$ mˆ takes the stegotext and outputs a message estimate. It does not require access to Model, the prompt, or token probabilities.

Remark 1 (Noiseless feedback). In the absence of editing, the dependence on $X ^ { t - 1 }$ models perfect causal feedback: after each token is generated, both communicating parties observe the same transcript and can derive identical side information. This feedback is the source of the reliability gains achieved by our algorithm.

Remark 2 (System assumptions). Specifically, we refer to white-box steganography as schemes that require decoder access to cover statistics [23]. In LLM steganography, this means access to model weights and prompts. Unlike white-box steganographic schemes, in our setting the decoder is agnostic to the sender’s model weights, prompt, and token probabilities. Consequently, synchronization of side information is achieved entirely through deterministic hashing of the shared transcript [33, Appendix A].

However, based on the assumption of Definition 2, apart from the public algorithm, decoder knows the sender tokenizer and vocabulary X. The encoder, in contrast, has inference-time access to the underlying language model, the prompt used, and therefore its next-token distribution s<sub>t</sub>. An information access table for our proposed algorithm is provided in Appendix A.

## 3.3 Adversarial Model

As illustrated in Fig. 1, the system models potential adversary at two intervention points: the input side, where the prompt and message are chosen, and the observation side (Eve), where the public transcript is inspected. Based on these roles, we define two distinct adversarial settings:

1. Passive Eavesdropper: In this setting, legitimate party chooses the prompt and message, while Eve is an adversary. This models an entity such as a platform content moderator or an automated firewall passively analyzing the generated text in transit. The passive adversary’s primary objective is to detect whether the transcript contains a hidden payload (covertness). Alternatively, Eve may attempt to decode the payload if its existence is suspected (secrecy). Security against this adversary is evaluated using information-theoretic divergence strengthened from [4], which guarantees both covertness and secrecy.

2. Active API Adversary: In this setting, the adversary controls both the input side and the observation side. This models an auditor or malicious user who adaptively queries the deployed language model via its API, providing chosen prompts and message to elicit specific outputs. Operating under a probabilistic polynomial-time constraint, the adversary attempts to distinguish between generated stegotext and covertext. Security against this adversary is evaluated using cryptographic distinguishing advantage. In this paper, we consider a stronger version of the API adversary that can query both message and prompt.

Since our primary application is LLM steganography, where stegotext is often assumed to be shared, an adversary who edits, deletes, or paraphrases the transcript is outside the scope of our security assumptions.

## 3.4 Security and Performance Definitions

Definition 3 (δ-Reliability). A black-box steganographic scheme is δ-reliable if there exists $\delta \in [ 0 , 1 ]$ such that

$$
P _ {\mathrm{e}} = \frac {1}{| \mathcal {M} |} \sum_ {m = 1} ^ {| \mathcal {M} |} \operatorname * {P r} \left[ \operatorname{Dec} _ {K} (X ^ {\tau}) \neq m | M = m \right] \leq \delta .\tag{5}
$$

In addition, we define the finite-length reliability function as

$$
E \triangleq - \frac {1}{\mathbb {E} [ \tau ]} \log P _ {\mathrm{e}}.\tag{6}
$$

Definition 4 (Embedding rate). For a message set M and variable transcript length τ, the embedding rate is

$$
R \triangleq \frac {\log | \mathcal {M} |}{\mathbb {E} [ \tau ]}.\tag{7}
$$

Definition 5 (σ-secure on average (against passive adversary)). A black-box steganographic scheme is σ-secure on average if for any channel input u (Definition 1) and state s

$$
\sup _ {s, u} \mathbb {D} \bigg (W _ {X | S} (x | s) | | \sum_ {k \in \mathcal {K}} P _ {K} (k) W _ {X | U, K, S} (x | u, k, s) \bigg) \leq \sigma ,\tag{8}
$$

where $P _ { K } ( k )$ is the induced key distribution. When $\sigma = 0$ , the scheme is said to be perfectly secure on average.

Definition 6 (Cryptographic security (against polynomial-time adversaries)). A black-box steganographic scheme is cryptographically secure if, for any polynomial-time API adversary A making polynomially many adaptive queries, the following advantage is negligible:

$$
\left. \right.\left| \operatorname * {P r} \left[ \mathcal {A} ^ {\text { Real }} (1 ^ {\lambda}) = 1 \right] - \operatorname * {P r} \left[ \mathcal {A} ^ {\text { Clean }} (1 ^ {\lambda}) = 1 \right]\right| \leq \operatorname{negl} (\lambda).\tag{9}
$$

On query i, A adaptively chooses a prompt-message pair $( \rho _ { i } , m _ { i } )$ . In the Real experiment, the oracle returns stegotext generated by $\Pi _ { \mathsf { M o d e l } }$ from $( \rho _ { i } , m _ { i } )$ ; in the Clean experiment, the oracle returns covertext generated by the base channel $W _ { X \mid S }$ from the same prompt $\rho _ { i ; \ast }$ , independently of $m _ { i }$

## 4 Feedback Coding and the BAM Protocol

We present the covert communication protocol in two stages that together form a single variable-length feedback code. In the first stage, variable-length posterior matching (Section 4.2), progressively localizes the hidden message by steering the decoder’s posterior belief. Once the decoder’s confidence exceeds a prescribed threshold, a second confirmation phase (Section 4.3) verifies the tentative decision and amplifies decoding reliability. We refer to the resulting feedback code as Burnashev Adaptive Posterior Matching (BAM). The name reflects BAM’s architectural inspiration from the Yamamoto–Itoh strategy [37], which achieves the Burnashev reliability function for classical memoryless channels [3]. We do not claim the corresponding asymptotic optimality for the LLM channel studied here; instead, we empirically evaluate the finite-length gains contributed by variable-length stopping and confirmation.

## 4.1 Intuition

As discussed in Definition 1, LLM steganography naturally induces a communication channel with causal, noiseless feedback. From an information-theoretic perspective, feedback does not increase the asymptotic capacity of a memoryless channel [7]. Its principal benefit is instead to improve the reliability function(6), which characterizes the exponential decay of the decoding error probability with expected blocklength [3, 37, 29]. Consequently, we will show that embedding rate alone does not fully characterize the performance of a steganographic scheme; practical covert agentic communication equally depends on how reliably messages can be recovered within a finite number of tokens available.

Two distinct mechanisms underlie the reliability gain [27] (increase in reliability function). The first is sequentiality gain, whereby the transmitter communicates using a variable stopping time, spending additional channel uses when the decoder remains uncertain while terminating early once suficient confidence has been established. The second is adaptivity gain, whereby future channel inputs are selected according to past observations. To this end, our algorithm incorporates three core mechanism previously unexplored in black-box steganography:

• Posterior matching: An encoding technique by which encoder draws codeword symbols based on decoder’s message belief [32]. We adopted a mismatched-belief variation to enable eficient, higher-rate encoding, while eliminating the need to store an exponentially large pre-shared codebook.

• Threshold decoding: We achieve sequentiality gain by using a threshold decoder based on posterior belief, which enables variable-length stopping.

• Yamamoto-Itoh scheme: Yamamoto-Itoh’s classical result shows that adaptivity gain can be exploited by segment-based adaptation through a short confirmation phase, yielding the optimal reliability exponent (Burnashev exponent) for communication with feedback [37, 29].

An empirical evaluation of these performance gains is provided in Appendix D.

## 4.2 Feedback Coding via Posterior Matching

At a high level, this point-to-point communication method operates through four sequential components:

1. Codebook generation: The encoder dynamically maps the intended message to a channel input based on the decoder’s current posterior belief (Codeword in Fig. 1).

2. Key generation and optimal transport: Both parties derive synchronized cryptographic side information from the shared transcript to define a secure, distortion-free coupling using optimal transport (LLM sampler in Fig. 1).

3. Belief computation and encoding: The decoder (and the synchronized encoder) updates its posterior distribution over the message space using a robust likelihood model (Encoder in Fig. 1).

4. Decoding: The decoder applies a threshold-based rule to the posterior to commit to the transmitted message (Decoder in Fig. 1).

## 4.2.1 Codebook Generation

Let $m \in \mathcal { M }$ denote the true message, and let $\pi _ { t } ( m )$ denote the decoder’s posterior belief <sup>1</sup> on message m after observing the first t generated tokens. We initialize the decoder with the uniform prior $\pi _ { 0 } ( m ^ { \prime } ) =$ $\frac { 1 } { | \mathcal { M } | } , \ \forall m ^ { \prime } \in \mathcal { M }$

To select the next channel input, the encoder maps the discrete message space onto the continuous unit interval [0, 1] by partitioning it into sub-intervals proportional to each message’s current posterior probability. Given the posterior distribution $\{ \pi _ { t - 1 } ( m ^ { \prime } ) \} _ { m ^ { \prime } \in \mathcal { M } }$ , the encoder determines the input codeword symbol at token position t according to the posterior matching rule $u _ { t } = F _ { U } ^ { - 1 } ( V _ { t } ( m ) )$ ,

$$
V _ {t} (m) = \sum_ {m ^ {\prime}: \mathrm{idx} (m ^ {\prime}) <   \mathrm{idx} (m)} \pi_ {t - 1} (m ^ {\prime}) + R _ {t} \pi_ {t - 1} (m).\tag{10}
$$

$V _ { t } ( m )$ represents a continuous cumulative belief statistic for message m (the sum of belief of messages with message index lower than m). The summation term calculates the lower bound of message m’s probability interval. The term $R _ { t }$ , idealized as $R _ { t } \ \sim \ \mathrm { U n i f } [ 0 , 1 ]$ , is synchronized pseudorandomness derived from the shared seed, which we explain in subsequent sections. This randomized mapping ensures that $V _ { t }$ remains continuously distributed on [0, 1]. Finally, for the codeword random variable U with cardinality $| \mathcal { U } | = p , F _ { U } ^ { - 1 }$ denotes inverse-CDF sampling, which transforms this continuous belief statistic into a discrete codeword symbol. In the classical posterior matching framework, the input distribution $F _ { U }$ is chosen to maximize the achievable rate of the communication channel [32]. Since the efective LLM channel depends on the prompt and generally does not admit a tractable capacity characterization, we instead choose $F _ { U }$ to be uniform over $u ,$ yielding $u _ { t } = \lfloor p V _ { t } ( m ) \rfloor$ , where $p = | \mathcal { U } |$ is the cardinality of the codeword symbol set, public as part of the protocol.

Unlike conventional block codes, the codebook is generated online rather than fixed in advance. This does not prevent the decoder from reconstructing the message-to-codeword mapping, since the encoding policy is public and (10) depends only on the decoder’s current posterior, which both communicating parties can reproduce. We next describe how this posterior is updated.

## 4.2.2 Key Generation and Optimal Transport

This section instantiates the KeyGen algorithm of Definition 2. We adapt from the optimal transport (OT) coupling mechanism of ArcMark [13] together with a transcript-dependent key generation procedure. To transmit $u _ { t } ,$ the encoder samples token $x _ { t }$ from the biased channel $W _ { X | U , K , S } ( x _ { t } \mid u _ { t } , k _ { t } , s _ { t } )$ obtained by solving an OT problem subject to a distortion-free marginal constraint which we explain in detail in proceeding paragraphs.

Both encoder and decoder share a fixed secret λ-bit seed $\kappa ,$ sampled uniformly once using a cryptographically secure random number generator (we use $\lambda = 1 2 8$ by default). Each LLM generation session is assigned a fresh public nonce $\nu \sim \mathrm { U n i f } ( \{ 0 , 1 \} ^ { \lambda } )$ , which is included in the shared session metadata. At token position $t ,$ the key $k _ { t }$ and posterior-matching randomness $R _ { t }$ are generated by applying a keyed pseudorandom function to the nonce, the previous h token indices, and the current token position<sup>2</sup>

$$
\Lambda_ {t} = F _ {\kappa} \big (\nu \parallel x ^ {t - h: t - 1} \parallel t \big),\tag{11}
$$

where $F _ { \kappa } ( z )$ is a keyed pseudorandom function. The context window is zero-padded for $t \leq h$ (we use $h \ = \ 3$ by default) [22]. The nonce separates diferent generation sessions, while the position counter prevents repeated PRF inputs within a session. We split the resulting digest into three disjoint blocks $\hat { \Lambda _ { t } ^ { ( 1 ) } } , \hat { \Lambda _ { t } ^ { ( 2 ) } } , \hat { \Lambda _ { t } ^ { ( 3 ) } }$ . The first two blocks deterministically specify the channel index and the random permutation used by the OT coupling. The third block is mapped by a fixed public conversion function Rand : $\{ 0 , 1 \} ^ { * } \to ( 0 , 1 )$ to the synchronized posterior-matching randomness $R _ { t }$ . The complete side information is therefore $\left( ( k _ { t } ^ { ( 1 ) } , k _ { t } ^ { ( 2 ) } ) , R _ { t } \right)$

$$
\begin{array}{l} k _ {t} ^ {(1)} = \mathrm{int} \big (\Lambda_ {t} ^ {(1)} \big) \bmod r, \quad k _ {t} ^ {(2)} = \Psi \big (\mathcal {X}; \Lambda_ {t} ^ {(2)} \big), \\ R _ {t} = \mathsf {R a n d} \big (\Lambda_ {t} ^ {(3)} \big), \end{array}\tag{12}
$$

where $k _ { t } = ( k _ { t } ^ { ( 1 ) } , k _ { t } ^ { ( 2 ) } )$ is the key used to synthesize the biased channels and $r = | \mathcal { K } ^ { ( 1 ) } |$ denotes the cardinality of the first key component so that $k _ { t } ^ { ( 1 ) } \in \{ 0 , \ldots , r - 1 \}$ $R _ { t } \in ( 0 , 1 )$ is the dither used to generate codeword symbol. $\Psi ( \cdot ; \Lambda _ { t } ^ { ( 2 ) } )$ denotes a deterministic permutation of the vocabulary parameterized by ${ \Lambda } _ { t } ^ { ( 2 ) }$ . Equation (12) is precisely the KeyGen algorithm: given the shared seed $\kappa ,$ transcript history and public nonce $\nu ,$ it emits the per-token side information $( k _ { t } , R _ { t } )$ consumed by the encode and decoder.

Following [13], tokens and symbols are embedded on the unit circle: token x is assigned angle $2 \pi k _ { t } ^ { ( 2 ) } ( x ) / V$ (permutation $k _ { t } ^ { ( 2 ) }$ applied to the set $x )$ , while the symbol $u _ { t }$ and $k _ { t } ^ { ( 1 ) }$ determine the target angle $z _ { t } = \left( 2 \pi u _ { t } / p + 2 \pi k _ { t } ^ { ( 1 ) } / r + \phi \right)$ mod $2 \pi$ for some fixed angle $\phi .$ For realized $S _ { t } = s _ { t }$ , the biased sampling channel is obtained by solving the transport plan $P _ { X _ { t } , Z _ { t } } \in \mathbb { R } _ { + } ^ { V \times r }$

$$
\begin{array}{l} P _ {X _ {t}, Z _ {t}} ^ {*} = \arg \min _ {P \in \mathbb {R} _ {+} ^ {V \times r}} \sum_ {i = 0} ^ {V - 1} \sum_ {j = 0} ^ {r - 1} P _ {i, j} \Phi_ {i, j} \\ \text {s.t.} \quad \sum_ {j = 0} ^ {r - 1} P _ {i, j} = W _ {X _ {t} | S _ {t}} (i | s _ {t}), \quad \forall i \in [ 0, V - 1 ], \\ \text {s.t.} \quad \sum_ {i = 0} ^ {V - 1} P _ {i, j} = \frac {1}{r}, \quad \forall j \in [ 0, r - 1 ], \end{array}\tag{13}
$$

where the cost matrix $\Phi \in \mathbb { R } ^ { V \times r }$ is

$$
\Phi_ {i, j} = d \left(\frac {2 \pi k _ {t} ^ {(2)} (i)}{V}, \left(\frac {2 \pi u _ {t}}{p} + \frac {2 \pi j}{r} + \phi\right) \bmod 2 \pi\right)
$$

(14)

In practice we solve (13) using the Sinkhorn algorithm and recover the conditional distribution at the realized key via $W _ { X _ { t } | U _ { t } , K _ { t } , S _ { t } } \big ( \cdot | u _ { t } , k _ { t } , s _ { t } \big ) = r P _ { X _ { t } , Z _ { t } } ^ { * } \big ( \cdot , z _ { t } \big )$ , with $\operatorname* { P r } ( Z _ { t } = z _ { t } ) = 1 / r$ . Details for the algorithm setup are provided in Appendix C.

## 4.2.3 Belief Computation and Encoding

For each received token x, the decoder estimates the received symbol statistic $\hat { C } _ { t } = \bigl ( 2 \pi k _ { t } ^ { ( 2 ) } ( x ) / V -$ $2 \pi k _ { t } ^ { ( 1 ) } / r )$ mod $2 \pi$ and evaluates a robust Laplace-contaminated likelihood,

$$
\begin{array}{l} \ell_ {t} (u _ {t} (m)) = f \Big (d \Big (\hat {C} _ {t}, \frac {2 \pi u _ {t} (m)}{p} + \phi \Big) \Big) \\ = \frac {1 - \epsilon}{2 b (1 - e ^ {- \pi / b})} \exp \left(- \frac {d \Big (\hat {C} _ {t} , \frac {2 \pi u _ {t} (m)}{p} + \phi \Big)}{b}\right) + \frac {\epsilon}{2 \pi}, \end{array}\tag{15}
$$

with $b = \pi / ( p \sqrt { 2 } )$ and $\epsilon \in [ 0 , 1 ) \ [ 5 ]$ . The Laplace component models the received symbol as concentrated around the transmitted codeword symbol, while the uniform component accounts for outlier tokens whose decoded symbol statistic carries little information. The decoder then updates its posterior according to

$$
\pi_ {t} (m) = \frac {\pi_ {t - 1} (m) \ell_ {t} (u _ {t} (m))}{\sum_ {j} \pi_ {t - 1} (j) \ell_ {t} (u _ {t} (j))}.\tag{16}
$$

We note that for each message $m ,$ the mapping to codeword symbol $u _ { t } ( m )$ at position t is deterministic and available to both parties through (10).

## 4.2.4 Decoding

Because both communicating parties observe the same generated transcript, they maintain identical posterior beliefs throughout communication. Decoding therefore mirrors the encoding procedure. The decoder can declare a tentative message whenever there exists a message whose belief crosses threshold $\gamma , \exists m ^ { \prime } , \pi _ { t } ( m ^ { \prime } ) > \gamma .$ . In Algorithm 2 we augment the decoding with a two-phase threshold decoding.

A visual illustration of the posterior matching belief is shown in Appendix E. We also present the encoder and decoder as a single mirrored procedure in Appendix E.

## 4.3 The BAM Protocol

Posterior matching progressively concentrates the shared belief, but the leading candidate can still be incorrect. Once one candidate dominates, BAM treats verification as a binary ACK/NACK test and repeatedly transmits antipodal confirmation symbols. This design is inspired by the two-phase Yamamoto–Itoh strategy [37, 3]. We now describe the complete BAM protocol, using Algorithm 1 as its communication phase. The BAM protocol is parameterized by three thresholds, γ, γ<sub>ACK</sub>, and γ<sub>NACK</sub>, satisfying $0 . 5 \le \gamma , \gamma _ { \mathrm { A C K } } , \gamma _ { \mathrm { N A C K } } < 1$ . These parameters are part of the publicly known policy and therefore require no synchronization.

1. During the communication phase, the encoder generates codeword symbols and tracks the decoder’s posterior according to (10) and (16) using Algorithm 1.

2. Whenever the decoder’s posterior satisfies $\pi _ { t } ( m ^ { \prime } ) > \gamma$ for some $m ^ { \prime } \in \mathcal { M }$ , the protocol enters the confirmation phase and encoder transmits one of two confirmation symbols, $u _ { \mathrm { A C K } } = 0 { \mathrm { ~ i f ~ } } m ^ { \prime }$ is the true message or $u _ { \mathrm { N A C K } } = 1$ otherwise (corresponding to $\theta _ { \mathrm { A C K } } = 2 \pi u _ { \mathrm { A C K } } / p = 0$ and $\theta _ { \mathrm { N A C K } } ~ =$ $2 \pi u _ { \mathrm { N A C K } } / p = \pi$ with $p = 2 )$

3. During confirmation, the encoder tracks the decoder’s posterior over $\{ u _ { \mathrm { A C K } } , u _ { \mathrm { N A C K } } \}$ by applying belief update in (15), (16) with $p = 2$ and likelihood parameter $\epsilon _ { \mathrm { A C K } } \in [ 0 , 1 )$ . The confirmation phase terminates once either $\pi _ { t } { \left( u _ { \mathrm { A C K } } \right) } > \gamma _ { \mathrm { A C K } }$ , in which case the tentative message $m ^ { \prime }$ is accepted and the transmission terminates, or $\pi _ { t } { \big ( } u _ { \mathrm { N A C K } } { \big ) } > \gamma _ { \mathrm { N A C K } }$ , in which case the tentative message is rejected, the decoder reduces the posterior of the candidate message by a factor $( 1 - \gamma _ { \mathrm { N A C K } } ) / \gamma _ { \mathrm { N A C K } } .$ renormalizes the posterior, and protocol re-enters communication phase.

4. False Reject. If $\pi _ { t } { \left( u _ { \mathrm { N A C K } } \right) } > \gamma _ { \mathrm { N A C K } }$ even though $u _ { \mathrm { A C K } }$ was transmitted, the protocol re-enters the communication phase and continues to transmit the message via Algorithm 1.

5. False Accept. $\mathrm { I f } \ \pi _ { t } ( u _ { \mathrm { A C K } } ) > \gamma _ { \mathrm { A C K } }$ when u was transmitted, the protocol declares a decoding error event.

6. Timeout. If no message is accepted by token $T ^ { * }$ , the decoder outputs $\hat { m } = \arg \operatorname* { m a x } _ { m ^ { \prime } \in \mathcal { M } } \pi _ { T ^ { * } } ( m ^ { \prime } )$ The algorithm is therefore specified by the parameter tuple

$$
\operatorname{BAM} \left(\gamma , \gamma_ {\mathrm{ACK}}, \gamma_ {\mathrm{NACK}}, \left(\epsilon , \epsilon_ {\mathrm{ACK}}\right), T ^ {*}\right),\tag{17}
$$

where $( \epsilon , \epsilon _ { \mathrm { A C K } } )$ are the likelihood parameters in (15) used during the communication and confirmation phases, respectively. The complete procedure is summarized in Algorithm 2 in Appendix E.

The two branches of Algorithm 1 and 2 instantiate the remaining components of Definition 2. The encoder branch is $\mathsf { E n c } _ { \mathsf { M o d e l } , K } \colon$ given the message m, prompt $\rho ,$ and the side information $( k _ { t } , R _ { t } )$ from KeyGen, it forms the codeword symbol $u _ { t }$ by (10) and samples the token $x _ { t }$ from the biased channel (13), appending it to the stegotext $x ^ { \tau }$ . The decoder branch is Dec $. K \cdot$ observing only $x ^ { \tau }$ and the shared side information, it computes $u _ { t } ( \boldsymbol { m } ^ { \prime } )$ for every candidate $m ^ { \prime }$ , scores the likelihood (15), and updates the belief (16) to produce the estimate $\hat { m }$ . A complete, per-party account of the information available in the system is given in Appendix A.

Remark 3 (Confirmation phase as binary hypothesis testing). The confirmation phase is equivalent to a variable length repetition code over anti-podal symbols. The posterior over $\{ u _ { \mathrm { A C K } } , u _ { \mathrm { N A C K } } \}$ is updated using the contaminated-Laplacian likelihood in (15) with $p = 2$ and a separate contamination parameter $\epsilon _ { \mathrm { A C K } }$ . Since binary antipodal signaling experiences lower efective channel noise than the communication phase, the protocol does not require $\epsilon = \epsilon _ { \mathrm { A C K } }$ . Unlike Algorithm 1, in the confirmation phase, the posterior is used only in decoding, which is a binary hypothesis testing problem.

Remark 4 (Weights of type I and II error). A false reject incurs only an additional retransmission, whereas a false accept results in an unrecoverable decoding error. Consequently, we choose $\gamma _ { \mathrm { A C K } } >$ γ<sub>NACK</sub>, biasing the protocol toward retransmission rather than erroneous acceptance.

## 5 Security Analysis

We first establish the formal security guarantee for BAM through a computational indistinguishability proof against a polynomial-time adaptive API adversary. We then empirically validate marginal preservation under the implemented key generation.

## 5.1 Cryptographic Security

The formal guarantee targets the security definition of Definition 6. The adversary samples one fixed secret seed κ and keeps it hidden, while every API query receives a fresh public nonce. We assume that the adversary makes at most Q(λ) queries and observes at most $L ( \lambda )$ generated tokens. Note that in our algorithm, the decoder commits to a message decoding at an internal codeword length $n \leq \tau$ the token generation continues under the same marginal-preserving sampler until natural generation stop τ. Therefore, as will be shown, the length of generation does not enable adversary to distinguish covertext from stegotext.

Theorem 1. Let $F _ { \kappa }$ be the $P R F$ used to generate per-token side information. For every polynomialtime distinguishing adversary A making at most $Q ( \lambda )$ queries and observing at most $L ( \lambda )$ tokens, there exists a PRF distinguisher B such that

$$
\operatorname{Adv} _ {\mathcal {A}} ^ {\mathrm{BAM}} (\lambda) \leq \operatorname{Adv} _ {\mathcal {B}} ^ {\mathrm{PRF}} (\lambda) + \frac {Q (\lambda) (Q (\lambda) - 1)}{2 ^ {\lambda + 1}} + L (\lambda) \eta (\lambda),\tag{18}
$$

where $\mathrm { A d v } _ { B } ^ { \mathrm { P R F } }$ denotes the distinguishing advantage against the underlying $P R F$ and $\eta ( \lambda )$ is the pertoken deviation from the ideal $O T$ marginal constraint under a truly random function, complete definition provided in Appendix B.

Proof. Sketch. The proof follows a standard sequence-of-games argument. We first replace the PRF used to derive BAM side information with a truly random function. Any adversary capable of distinguishing these two games immediately yields a distinguisher against the underlying PRF, establishing the first term in (18). On the other hand, under an idealized key schedule, the OT marginal constraint guarantees that every generated token has the same distribution as under the unbiased language model. We then couple the BAM and unbiased generation processes token by token. A birthday bound yields the second term in (18), while deviations from the ideal OT marginal condition contribute to the third term $L ( \lambda ) \eta ( \lambda )$ . Combining the reduction with the coupling argument completes the proof. The full proof is provided in Appendix B. □

We stress that although BAM employs a variable internal decoding time n, this stopping time does not determine the observable generation length. Each conversational turn terminates only when EOS is sampled from the LLM. Moreover, since each query results in a finite-length token generation, both $Q ( \lambda )$ and $L ( \lambda )$ are polynomial in λ. Consequently, the distinguishing advantage in (18) is negligible whenever the underlying PRF is secure and $\eta ( \lambda )$ is negligible. For the ideal OT construction enforced in (13) and analyzed in Theorem 1, the base distribution is imposed as an exact marginal constraint, so $\eta ( \lambda ) =$ 0. The empirical study of Section 5.2 instead evaluates the realized finite-precision implementation, accounting for both the PRF-induced key distribution and numerical deviation of the OT solver.

## 5.2 Empirical Validation of Marginal Preservation

For every token position, the OT construction makes the biased channel $( W _ { X | U , K , S } ( \cdot \mid u , k , s ) )$ marginalize over key to $\textstyle ( W _ { X \mid S } ( \cdot \mid s ) )$ . This identity holds by construction for coupling-based schemes [9]. In practice, however, two sources of deviation may arise: the realized key distribution is induced by a PRF rather than sampled directly from a uniform key, and the OT coupling is computed numerically to finite precision. We therefore estimate the seed-marginalized per-token divergence

$$
\mathbb {D} \big (W _ {X | S} (x | s) \big | \big | \sum_ {k \in \mathcal {K}} P _ {K} (k) W _ {X | U, K, S} (x | u, k, s) \big),\tag{19}
$$

where $P _ { K }$ is the per-token key distribution induced by the realized PRF schedule under a uniform seed. We note that by Definition 5, we use a per-token KL constraint for every input symbol u and token history, which is stronger constraint than [4, Definition 2].

Fig 4 in Appendix estimates Definition 5 by Monte Carlo over an increasing number of seeds. At every token length, the estimate descends toward the sampling floor as the seed count grows, while the accumulated divergence grows roughly linearly in token length. $1 0 ^ { 5 }$ sampled seeds result in an empirical per-token KL smaller than $1 0 ^ { - 5 }$ . Therefore, the experiment found no local deviation resolvable at the reported Monte Carlo precision. The realized schedule is thus empirically σ-secure on average with small σ at the tested seed counts (Definition 5). Figure 4 should be viewed as an implementation diagnostic capturing both PRF-induced key non-uniformity and finite-precision OT solver.

## 6 Covert Agentic Conversation

Section 4 describes the BAM algorithm, which can be applied to any general LLM generated cover. However, conversational covertext in particular creates additional challenges not present in long, continuous generative text. In this section we explain several design considerations of the BAM algorithm specifically for conversational steganography.

A defining feature of covert agentic communication, compared with conventional covert communication over static covertexts [1, 6], is that the deployer controls the interaction but not the length of the covertext. The conversational setting, agent roles, and turn structure are chosen in advance, yet under the distortion-free constraint the language model cannot be forced to terminate at a prescribed token or continue once an EOS token is sampled. Consequently, we may resolve this mismatch by adapting BAM’s decoding decision to the realized generation rather than to a fixed belief threshold. This flexibility also makes the covertext itself a design variable: conversational settings with longer or higher-entropy turns naturally provide greater embedding opportunities (how to design suitable prompts for conversational steganography is outside the scope of this study). We first describe the agentic conversation setup considered in this work.

Agentic conversation setup. Both agents are first provided with a shared background description specifying the conversational setting, assigning each agent a role, and an opening. Each agent additionally receives a private instruction governing the content and style of its responses. For automation, we keep these instructions fixed throughout a conversation, although they may be customized on a turnby-turn basis according to user inputs. The efective context for each generation therefore consists of the shared background, the agent’s private instructions, and the public conversation history. Example conversation templates are provided in Appendix G.

Adaptive stopping. To improve token eficiency in conversational steganography, we consider the following modification to BAM, which adapts decoding to the realized conversational turn rather than enforcing a fixed decoding threshold.

1. Case I: $n \leq \tau$ . In this case, the codeword is completed at a token budget n shorter than natural generation length τ. The posterior belief exceeds the default decoding communication and confirmation thresholds $( \gamma , \gamma _ { \mathrm { A C K } } )$ before EOS is sampled, the encoder continues transmitting the message until EOS, while the decoder makes use of the additional tokens and chooses the highest belief message until the turn naturally terminates at EOS, thus creating better channel utilization.

2. Case II: $n > \tau .$ . In this case, the codeword cannot be completed before the natural generation τ of a conversation turn. If EOS is sampled before the confirmation phase completes, generation terminates normally instead of being artificially extended. Specifically, since the decoder’s belief in $u _ { \mathrm { A C K } }$ remains below $\gamma _ { \mathrm { A C K } }$ (including cases when confirmation phase is not reached), the opposing agent produces a genuine, unbiased response that carries no payload, allowing the overt conversation to proceed naturally. The transmitting agent then resumes embedding the remaining payload during its next turn.

Interactive composition and security By allowing the stopping time to follow the natural generation process, rather than a predetermined token budget, the modified algorithm can simultaneously achieve a higher throughput and better token utilization while preserving the distortion-freeness from point-to-point communication. Note that for multi-turn steganography under our construction, the security guarantee in Theorem 1 is local to each communication turn and is conditioned on the public conversation history. Alternating the point-to-point BAM transmissions therefore compose: if each communication turn is computationally indistinguishable from clean generation conditioned on every preceding public transcript, then a standard hybrid argument over any polynomial number of turns shows that the complete two-way conversation is computationally indistinguishable from the corresponding clean conversation.

## 7 Evaluation

## 7.1 Overview

We adopt a layered evaluation framework. The first layer evaluates BAM as a token-level stegano graphic embedding primitive on standardized continuous-text covers. These experiments measure its rate–reliability tradeof, text quality and computational cost against existing multi-bit watermarking baselines. The second layer evaluates the composition of this same primitive into an end-to-end covert agentic communication protocol. To the best of our knowledge, such evaluation benchmarks and corresponding baselines do not currently exist. Therefore, rather than repeating primitive-level measurements, we propose an evaluation framework for covert conversations that focuses on properties that arise only through multi-turn composition, including payload throughput, dialogue-level reliability, token utilization and conversational quality.

For continuous-text experiments, we use three base models: Llama-3.1-8B, Qwen-3.5-9B-Base, and Mistral-7B-v0.3. For covert agentic communication, we use Llama-3.1-8B-Instruct, Phi-4-14B-Instruct, Qwen3-A3B-30B-Instruct-2507. All models are accessed at inference time using temperature 1.0 and top-50 sampling. Experiments run with batch size 1 on a single NVIDIA A100-SXM4 GPU with 80 GB memory, 4 CPU cores, and 64 GB system memory on a SLURM cluster.

Throughout, $F _ { U } ^ { - 1 }$ is the inverse CDF of the uniform distribution, and posterior updates use the mixture-Laplace likelihood in (15). Codeword symbols are drawn from an alphabet of size $p = | \mathcal { U } | = 4$ with $\phi = 0$ , and the channel-key cardinality is $r = | \mathcal { K } ^ { ( 1 ) } | = 4$ . We use a 128-bit security parameter $\lambda = 1 2 8$ , context-window length $h = 3$ , and $F _ { \kappa } ( z ) = \mathrm { H M A C - S H A 2 5 6 } ( \kappa , z )$

## 7.2 Evaluation Metrics

## 7.2.1 Primitive-Level Metrics

The continuous-text experiments use the C4 Real News dataset and evaluate BAM against existing inference-time multi-bit watermarking schemes.

• Reliability and Rate. We evaluate the empirical counterpart of Definition 3 using the average message-decoding error probability over messages and prompts sampled uniformly across 1000 trials. Message error rate in Definition 3 is stricter than the bit-error rate reported by several baselines [10, 8]: a message is counted as incorrect whenever at least one payload bit is decoded incorrectly. This is the more operationally relevant metric for communication setting when no outer error-correction code is used. The efective embedding rate is defined in Definition 4.

• Text Quality. We evaluate fluency using perplexity and diversity using distinct-n. Perplexity is scored against full-softmax distribution and distinct-n measures the percentage of unique n-grams. Because BAM is variable-length, every stego generation is compared with a length-matched noembedding generation from the same base model. A smaller perplexity diference indicates better preservation of fluency, while a larger distinct-n value indicates less repetition.

• Generation Time. We report wall-clock generation time in seconds per token. Measurements are CUDA-synchronized and collected after untimed warm-up generations. Posterior-based decoding scales exponentially with the payload size; for BAM, the synchronized posterior afects both encoding and decoding. A detailed runtime breakdown and scaling analysis are provided in Appendix D.

## 7.2.2 Conversation-Level Metrics

As described in Section 6, for the conversational setting we simulate 100 dialogues of 10 rounds each, with each dialogue carrying up to 10 hidden payloads. The covert tasks are stateful in nature, therefore each round can carry only one payload. We focus on end-to-end properties introduced by variable turn lengths, alternating speakers, and multi-turn task dependence. Formal definitions are provided in Appendix G.1.

• Bits/token: The average number of successfully decoded payload bits per generated token. This measures the efective communication rate under the lower average entropy and variable turn lengths of conversational text.

![](images/a8ff7207c4e6eb1ce1ea470aff75d4e7c851bca5dccda8bb227bf83f55a7d200.jpg)  
Figure 2: BAM versus baseline schemes on the C4 News dataset with an 8-bit payload, across three base models (Llama-3.1-8B, Qwen-3.5-9B, Mistral-7B-v0.3). Each point trades message-decoding error against average token length; BAM (with SEM on length) attains significantly lower error at shorter average lengths than other baselines.

• Avg payload/dialogue: The average number of successfully transmitted payloads per conversation. This captures how much of the hidden task can be completed within the available dialogue.

• Message and dialogue error rate: Message error rate measures individual payload failures. Dialogue error rate is the fraction of ten-round conversations containing at least one incorrect payload, measuring the reliability required to complete an entire multi-message conversational session without communication error.

• Eficiency: The fraction of payload-carrying tokens. This measures utilization of the naturally available conversational cover.

• Conversational Quality: We use a blinded LLM judge to compare BAM and clean conversations with respect to naturalness, response relevance, multi-turn coherence, role adherence, repetition, and overt-task consistency. Transcripts are presented in randomized order, and we report the proportions of BAM wins, ties, and losses against length- and prompt-matched clean conversations.

## 7.3 Performance on Continuous Text

Setup We first demonstrate BAM’s steganography performance on the C4 Real News dataset. We compare against benchmark schemes under multi-bit watermarking ArcMark [13], MPAC [38], Bi-Mark [10] and StealthInk [18], the specific experimental setup details are provided in Appendix C<sup>3</sup>. For algorithm setting, we use $\mathrm { B A M } ( 0 . 5 , 1 - L ^ { - 1 } , 0 . 7 5 , ( 0 . 4 , 0 . 4 )$ , 1000) for (17) while sweeping the confirmation threshold $L \in \{ 2 , 2 ^ { 2 } , 2 ^ { 3 } , 2 ^ { 4 } , 2 ^ { 5 } , 2 ^ { 6 } , 2 ^ { 7 } , 2 ^ { 9 } , 2 ^ { 1 1 } , 2 ^ { 1 3 } , 2 ^ { 1 5 } , 2 ^ { 1 7 } \}$ . For each setting, we conduct 1000 trials. We embed an 8-bit payload across all settings. Because BAM’s length is variable, each watermarked scheme is compared against its own length-matched no-embedding baseline.

It is important to note that communication systems commonly employ sub-packetization to balance computational complexity and error performance. For example, a 64-bit message may be divided into eight 8-bit packets, substantially reducing the posterior-update complexity. We therefore focus on 8- bit payloads, while additional performance and runtime results for longer payloads are provided in Appendix D.

Table 1: Comparison of BAM scheme vs Baselines on C4 News Dataset. Reliability is reported as average generation length and message error rate (lower error is better). Values are mean ± SE over 1000 trials. Models: Llama: Llama-3.1-8B; Qwen: Qwen-3.5-9B-Base; Mistral: Mistral-7B-v0.3

<table><tr><td rowspan="2">Model</td><td rowspan="2">Scheme</td><td colspan="2">Reliability</td><td colspan="4">Text Quality</td><td>Time</td></tr><tr><td>Avg Len</td><td>Msg Err ↓</td><td>PPL ↓</td><td>Dist2</td><td>Dist3</td><td>Dist4</td><td>Sec/Token ↓</td></tr><tr><td rowspan="7">Llama</td><td>No Embedding</td><td>50.0</td><td>-</td><td>7.66 ± 0.11</td><td>0.969</td><td>0.986</td><td>0.992</td><td>0.0214</td></tr><tr><td>MPAC</td><td>50.0</td><td>0.797 ± 0.013</td><td>8.54 ± 0.11</td><td>0.963</td><td>0.982</td><td>0.989</td><td>0.0223</td></tr><tr><td>BiMark</td><td>50.0</td><td>0.569 ± 0.016</td><td>7.68 ± 0.11</td><td>0.959</td><td>0.977</td><td>0.984</td><td>0.0352</td></tr><tr><td>StealthInk</td><td>50.0</td><td>0.637 ± 0.015</td><td>7.66 ± 0.11</td><td>0.969</td><td>0.987</td><td>0.992</td><td>0.0231</td></tr><tr><td>ArcMark</td><td>50.0</td><td>0.106 ± 0.010</td><td>7.52 ± 0.11</td><td>0.972</td><td>0.988</td><td>0.994</td><td>0.0291</td></tr><tr><td>No Embedding</td><td>47.1 ± 1.5</td><td>-</td><td>7.71 ± 0.12</td><td>0.971</td><td>0.987</td><td>0.992</td><td>0.0224</td></tr><tr><td> $BAM(L=2^{15})$ </td><td>47.1 ± 1.5</td><td>0.001 ± 0.001</td><td>7.89 ± 0.12</td><td>0.970</td><td>0.984</td><td>0.989</td><td>0.0378</td></tr><tr><td rowspan="7">Qwen</td><td>No Embedding</td><td>50.0</td><td>-</td><td>7.83 ± 0.10</td><td>0.966</td><td>0.989</td><td>0.994</td><td>0.0420</td></tr><tr><td>MPAC</td><td>50.0</td><td>0.840 ± 0.012</td><td>9.03 ± 0.12</td><td>0.968</td><td>0.989</td><td>0.995</td><td>0.0420</td></tr><tr><td>BiMark</td><td>50.0</td><td>0.567 ± 0.016</td><td>8.23 ± 0.12</td><td>0.957</td><td>0.980</td><td>0.987</td><td>0.0558</td></tr><tr><td>StealthInk</td><td>50.0</td><td>0.659 ± 0.015</td><td>8.04 ± 0.11</td><td>0.965</td><td>0.989</td><td>0.995</td><td>0.0456</td></tr><tr><td>ArcMark</td><td>50.0</td><td>0.105 ± 0.010</td><td>7.76 ± 0.11</td><td>0.963</td><td>0.987</td><td>0.993</td><td>0.0510</td></tr><tr><td>No Embedding</td><td>45.8 ± 1.3</td><td>-</td><td>8.21 ± 0.13</td><td>0.970</td><td>0.989</td><td>0.995</td><td>0.0436</td></tr><tr><td> $BAM(L=2^{15})$ </td><td>45.8 ± 1.3</td><td>0.001 ± 0.001</td><td>8.24 ± 0.12</td><td>0.969</td><td>0.988</td><td>0.993</td><td>0.0541</td></tr><tr><td rowspan="7">Mistral</td><td>No Embedding</td><td>50.0</td><td>-</td><td>6.25 ± 0.09</td><td>0.962</td><td>0.985</td><td>0.992</td><td>0.0212</td></tr><tr><td>MPAC</td><td>50.0</td><td>0.872 ± 0.012</td><td>6.73 ± 0.09</td><td>0.959</td><td>0.981</td><td>0.989</td><td>0.0216</td></tr><tr><td>BiMark</td><td>50.0</td><td>0.674 ± 0.015</td><td>6.26 ± 0.08</td><td>0.958</td><td>0.980</td><td>0.988</td><td>0.0342</td></tr><tr><td>StealthInk</td><td>50.0</td><td>0.702 ± 0.014</td><td>6.16 ± 0.08</td><td>0.963</td><td>0.986</td><td>0.994</td><td>0.0217</td></tr><tr><td>ArcMark</td><td>50.0</td><td>0.168 ± 0.012</td><td>6.13 ± 0.09</td><td>0.959</td><td>0.982</td><td>0.991</td><td>0.0278</td></tr><tr><td>No Embedding</td><td>49.7 ± 1.2</td><td>-</td><td>6.22 ± 0.10</td><td>0.960</td><td>0.981</td><td>0.989</td><td>0.0222</td></tr><tr><td> $BAM(L=2^{11})$ </td><td>49.7 ± 1.2</td><td>0.000 ± 0.000</td><td>6.51 ± 0.09</td><td>0.963</td><td>0.984</td><td>0.991</td><td>0.0326</td></tr></table>

Evaluation The full reliability and average token length tradeof is reported in Fig. 2, and we expand the evaluation on other performance measures in Table 1.

• Reliability: BAM achieves significantly smaller error at shorter average length and the perfor mance gain is roughly two orders of magnitude better than the best baseline. Across all three models BAM achieves a substantially better reliability-length tradeof than the benchmark baselines. Concretely, BAM attains a message error rate of $\leq 0 . 1 \%$ over 1000 runs with an average token below 50 across all three LLM models, whereas the strongest baselines of comparable length incur 10–17% message error. The strong reliability guarantee is the cornerstone of ensuring covert communication. A detailed ablation for explaining the sources of performance gain is provided in Appendix D.

• Text Quality: In these trials, the stegotext generated by our method retains similar linguistic quality of texts generated from a clean model. The BAM outputs show only a modest perplexity diference across three models, compared to the base perplexity. Such diferences are on par with other distortion-free algorithms such as [18, 13, 10], while exhibiting better quality than distortionary [38].

• Time: The additional runtime of BAM comes mainly from channel synthesis (OT) and posterior update. As shown in Table 1, BAM runtime is the weakest part of the algorithm and exhibits a

30%, 6%, 17% increase compared to ArcMark over Llama, Qwen and Mistral, respectively. This is a result of posterior matching, which must be computed at both encoder and decoder. A detailed breakdown of runtime, as well as scalability concerns, are addressed in Appendix D.

## 7.4 Performance on Covert Agentic Communication

Setup We test the covert communication system in a two-way conversational setting. We use three specific turn-based covert tasks, which difer in the size of the hidden payload transmitted per message: a tic-tac-toe move (avg. 2.3 coded bits), a chess move (avg. 5.0 coded bits), and a move in 19 × 19 Go (go19, avg. 8.4 coded bits). We use uniform-prior source coding over the legal moves available in the current position <sup>4</sup>. We use two conversational covers: casual text-message chats and forum exchanges. In general, casual chats provide shorter conversation length, resulting in a lower overall embedding capacity. The shared background descriptions are generated by prompting GPT-5.5 to produce a pool of 50 distinct scenarios for each setting [14]. Each dialogue samples one background from its setting’s pool, so the covert channel is evaluated across a distribution of topics, while the side instructions are fixed for each setting. For each combination of covert task and overt conversation cover, we simulate 100 conversations of 10 rounds each, using the covert protocol with setting BAM(0.5, 0.75, 0.75, (0.7, 0.3), 1000). The default acknowledgment threshold γ is chosen to be lower than in the primitive test because we used the adaptive threshold rule designed for conversational cover discussed in Section 6, which improves channel eficiency at the cost of a marginal increase in decoding error.

Beyond reliability, the covert conversation must not induce quality degradation over unbiased conversations. Although we already demonstrated the quality in preceding sections, conversation setup may introduce multi-turn structure unaccounted for by primitive-level metrics. We generate 100 stegotext conversations with a clean conversation generated from the same topic, opener, and sampling seed, and ask an independent LLM judge (Gemini-3.1-Pro-Preview, Accessed Aug 10-24) which of the two is higher quality. This is intended to show that stegotext does not degrade the relative quality of multi turn generation compared to unbiased conversation. The judge sees the pair in blinded and randomized order and returns a win/tie/loss preference for the embedded transcript against its seed-matched clean counterpart. Additional experimental details provided in Appendix G.

Embedding Evaluation Table 2 reports the full simulation results using casual-chat covertext, with additional details provided in Appendix G. The results demonstrate that BAM supports reliable covert agentic communication when the conversational cover provides a suficient embedding throughput, determined jointly by its token length and average token entropy. For Llama-3.1 and Phi-4, message error remains below 3% across all three covert tasks, while Phi-4’s longer generations enable substan tially more payloads to be completed within each dialogue. In contrast, Qwen produces a considerably lower-entropy channel, which reduces the information available within each turn; as the payload size increases, transmissions therefore span more turns, decreasing the average number of completed payloads and eventually increasing decoding error. These results highlight a characteristic specific to conversa tional steganography: reliable communication depends not only on the embedding scheme, but also on matching the carrying capability of the overt conversation to the communication demand of the covert task.

Quality Evaluation As can be seen from Table 2, the judge shows no systematic preference for the clean conversations over their stego counterparts. The Llama-3.1-8B-Instruct split slightly favors stego conversation, but is not statistically significant, so we read it as no measurable quality gap rather than an advantage for embedding. This is expected: embedding adds no degradation of its own, and the weaker open-weight models tend to lose coherence over multi-turn generation in both conditions, and sampling variance can contribute to the result. This experiment concerns the efect of embedding, not absolute quality: dialogue naturalness is a property of the base model and prompt, and comparison to human conversation is beyond our scope.

Table 2: Turn-based covert channel on the casual chat covertext, across three open-weight instruct models and three embedding tasks. Values are mean $\pm \ \mathrm { S E }$ over 100 dialogues per cell.

<table><tr><td colspan="2">casual chat covertext</td><td colspan="3">Embedding task</td></tr><tr><td>Model</td><td>Metric</td><td>tictactoeavg. 2.3 bits</td><td>chessavg. 5.0 bits</td><td>go19avg. 8.4 bits</td></tr><tr><td rowspan="6">Llama-3.1-8B-Instructavg. entropy1.878 bits/tok,len 33.7 tok</td><td>Bits/token</td><td> $0.0607 \pm 0.0011$ </td><td> $0.0903 \pm 0.0023$ </td><td> $0.1030 \pm 0.0029$ </td></tr><tr><td>Avg payload/dialogue</td><td> $7.27 \pm 0.19$ </td><td> $5.20 \pm 0.17$ </td><td> $2.64 \pm 0.09$ </td></tr><tr><td>Dialogue error rate</td><td> $0.050 \pm 0.022$ </td><td> $0.020 \pm 0.014$ </td><td> $0.060 \pm 0.024$ </td></tr><tr><td>Message error rate</td><td> $0.0069 \pm 0.0029$ </td><td> $0.0038 \pm 0.0032$ </td><td> $0.0227 \pm 0.0106$ </td></tr><tr><td>Efficiency (%)</td><td> $88.64 \pm 0.99$ </td><td> $79.33 \pm 0.89$ </td><td> $65.25 \pm 0.62$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>58 / 0 / 42</td><td></td></tr><tr><td rowspan="6">Phi-4-14B-Instructavg. entropy2.049 bits/tok,len 62.3 tok</td><td>Bits/token</td><td> $0.0394 \pm 0.0008$ </td><td> $0.0666 \pm 0.0010$ </td><td> $0.1028 \pm 0.0022$ </td></tr><tr><td>Avg payload/dialogue</td><td> $9.33 \pm 0.12$ </td><td> $8.35 \pm 0.17$ </td><td> $5.54 \pm 0.21$ </td></tr><tr><td>Dialogue error rate</td><td> $0.020 \pm 0.014$ </td><td> $0.020 \pm 0.014$ </td><td> $0.070 \pm 0.026$ </td></tr><tr><td>Message error rate</td><td> $0.0021 \pm 0.0016$ </td><td> $0.0024 \pm 0.0017$ </td><td> $0.0126 \pm 0.0058$ </td></tr><tr><td>Efficiency (%)</td><td> $98.08 \pm 0.50$ </td><td> $95.25 \pm 0.65$ </td><td> $84.89 \pm 0.97$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>50 / 1 / 49</td><td></td></tr><tr><td rowspan="6">Qwen3-A3B-30B-Instructavg. entropy1.171 bits/tok,len 37 tok</td><td>Bits/token</td><td> $0.0434 \pm 0.0010$ </td><td> $0.0478 \pm 0.0017$ </td><td> $0.0470 \pm 0.0030$ </td></tr><tr><td>Avg payload/dialogue</td><td> $5.26 \pm 0.21$ </td><td> $3.25 \pm 0.14$ </td><td> $1.60 \pm 0.07$ </td></tr><tr><td>Dialogue error rate</td><td> $0.190 \pm 0.039$ </td><td> $0.200 \pm 0.040$ </td><td> $0.220 \pm 0.046$ </td></tr><tr><td>Message error rate</td><td> $0.0380 \pm 0.0091$ </td><td> $0.0708 \pm 0.0197$ </td><td> $0.0938 \pm 0.0406$ </td></tr><tr><td>Efficiency (%)</td><td> $79.53 \pm 1.07$ </td><td> $70.94 \pm 0.81$ </td><td> $62.56 \pm 0.34$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>46 / 0 / 54</td><td></td></tr></table>

## 8 Conclusion

We recast black-box LLM steganography as sequential communication over a channel with causal, noiseless feedback, and showed that this closes the reliability gap that had kept inference-time schemes impractical for covert agentic communication. Our protocol is inspired by information-theoretic feed back coding which combines posterior matching and Yamamoto–Itoh confirmation scheme. Over 1000 trials and three open-weight LLM models, BAM attains near error-free transmission on an 8-bit payload in an average of less than 50 tokens, orders of magnitude below the strongest black-box baseline at comparable length. Moreover, our algorithm is computationally indistinguishable against polynomial time adversary and remain empirically σ-secure against a passive observer. These results establish that reliable covert agentic communication is feasible even under prompt- and model-agnostic constraints, and that transcript-level monitoring carries a corresponding structural blind spot.

## References

[1] Matthieu R Bloch. Covert communication over noisy channels: A resolvability perspective. IEEE Transactions on Information Theory, 62(5):2334–2354, 2016.

[2] Matthieu R Bloch and J Nicholas Laneman. Strong secrecy from channel resolvability. IEEE Transactions on Information Theory, 59(12):8077–8098, 2013.

[3] Marat Valievich Burnashev. Data transmission over a discrete channel with feedback. random transmission time. Problemy peredachi informatsii, 12(4):10–30, 1976.

[4] Christian Cachin. An information-theoretic model for steganography. Information and computation, 192(1):41–56, 2004.

[5] Mengjie Chen, Chao Gao, and Zhao Ren. A general decision theory for Huber’s ϵ-contamination model. Electronic Journal of Statistics, 10(2):3752–3774, 2016.

[6] Xinying Chen, Jianping An, Zehui Xiong, Chengwen Xing, Nan Zhao, F Richard Yu, and Arumugam Nallanathan. Covert communications: A comprehensive survey. IEEE Communications Surveys & Tutorials, 25(2):1173–1198, 2023.

[7] Thomas M Cover and Joy A Thomas. Elements of information theory. John Wiley & Sons, 1999.

[8] Xuehao Cui, Ruibo Chen, Yihan Wu, and Heng Huang. MC<sup>2</sup>Mark : Distortion-free multi-bit watermarking for long messages. arXiv preprint arXiv:2602.14030, 2026.

[9] Christian Schroeder de Witt, Samuel Sokota, J Zico Kolter, Jakob Foerster, and Martin Strohmeier. Perfectly secure steganography using minimum entropy coupling. arXiv preprint arXiv:2210.14889, 2022.

[10] Xiaoyan Feng, He Zhang, Yanjun Zhang, Leo Yu Zhang, and Shirui Pan. Bimark: Unbiased multilayer watermarking for large language models. arXiv preprint arXiv:2506.21602, 2025.

[11] Tom´aˇs Filler, Andrew D Ker, and Jessica Fridrich. The square root law of steganographic capacity for markov covers. In Media forensics and security, volume 7254, pages 62–72. SPIE, 2009.

[12] Jessica Fridrich. Steganography in digital media: principles, algorithms, and applications. Cambridge university press, 2009.

[13] Atefeh Gilani, Sajani Vithana, Carol Xuan Long, Oliver Kosut, Lalitha Sankar, and Flavio P Calmon. Arcmark: Distortion-free multi-byte LLM watermark via optimal transport. arXiv preprint arXiv:2602.07235, 2026.

[14] Thilo Hagendorf. Deception abilities emerged in large language models. Proceedings of the National Academy of Sciences, 121(24):e2317967121, 2024.

[15] Jefrey T Hancock, Mor Naaman, and Karen Levy. AI-mediated communication: Definition, research agenda, and ethical considerations. Journal of Computer-Mediated Communication, 25(1):89–100, 2020.

[16] Kaibo Huang, Yukun Wei, WanSheng Wu, Tianhua Zhang, Zhongliang Yang, and Linna Zhou. Whispering agents: A event-driven covert communication protocol for the internet of agents. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 40, pages 31185–31192, 2026.

[17] Ya Jiang, Massieh Kordi Boroujeny, Surender Suresh Kumar, and Kai Zeng. Mirrormark: A distortion-free multi-bit watermark for large language models. arXiv preprint arXiv:2601.22246, 2026.

[18] Ya Jiang, Chuxiong Wu, Massieh Kordi Boroujeny, Brian Mark, and Kai Zeng. Stealthink: A multi-bit and stealthy watermark for large language models. arXiv preprint arXiv:2506.05502, 2025.

[19] Cameron R. Jones and Benjamin K. Bergen. Large language models pass a standard three-party Turing test. Proceedings of the National Academy of Sciences, 123(21):e2524472123, 2026.

[20] Gabriel Kaptchuk, Tushar M Jois, Matthew Green, and Aviel D Rubin. Meteor: Cryptographically secure steganography for realistic distributions. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, pages 1529–1548, 2021.

[21] Andrew D Ker, Tom´aˇs Pevn\`y, Jan Kodovsk\`y, and Jessica Fridrich. The square root law of steganographic capacity. In Proceedings of the 10th ACM workshop on Multimedia and security, pages 107–116, 2008.

[22] John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, and Tom Goldstein. A watermark for large language models. In International conference on machine learning, pages 17061–17084. PMLR, 2023.

[23] Guorui Liao, Jinshuai Yang, Weizhi Shao, and Yongfeng Huang. A framework for designing provably secure steganography. In 34th USENIX Security Symposium (USENIX Security 25), pages 6837–6856, 2025.

[24] Hannah Mieczkowski, Jefrey T Hancock, Mor Naaman, Malte Jung, and Jess Hohenstein. Ai-mediated communication: Language use and interpersonal efects in a referential communication task. Proceedings of the ACM on Human-Computer Interaction, 5(CSCW1):1–14, 2021.

[25] Sumeet R Motwani, Mikhail Baranchuk, Martin Strohmeier, Vijay Bolina, Philip H Torr, Lewis Hammond, and Christian S de Witt. Secret collusion among ai agents: Multi-agent deception via steganography. Advances in Neural Information Processing Systems, 37:73439–73486, 2024.

[26] Pierre Moulin and Joseph A O’Sullivan. Information-theoretic analysis of information hiding. IEEE Transactions on information theory, 49(3):563–593, 2003.

[27] Mohammad Naghshvar and Tara Javidi. Sequentiality and adaptivity gains in active hypothesis testing. arXiv preprint arXiv:1211.2291, 2012.

[28] Kaiyi Pang and Minhao Bai. Provable secure steganography based on adaptive dynamic sampling. arXiv preprint arXiv:2504.12579, 2025.

[29] Yury Polyanskiy, H Vincent Poor, and Sergio Verdu. Feedback in the non-asymptotic regime. IEEE Transactions on Information Theory, 57(8):4903–4925, 2011.

[30] Yury Polyanskiy and Yihong Wu. Information theory: From coding to learning. Cambridge university press, 2025.

[31] B Ya Ryabko and Daniil Borisovich Ryabko. Asymptotically optimal perfect steganographic systems. Problems of Information Transmission, 45(2):184–190, 2009.

[32] Ofer Shayevitz and Meir Feder. Optimal feedback communication via posterior matching. IEEE Transactions on Information Theory, 57(3):1186–1222, 2011.

[33] Dor Tsur, Carol Long, Claudio Mayrink Verdun, Sajani Vithana, Hsiang Hsu, Richard Chen, Flavio Calmon, et al. Heavywater and simplexwater: Distortion-free llm watermarks for low-entropy distributions. Advances in Neural Information Processing Systems, 38:107204–107256, 2026.

[34] Vinod Vaikuntanathan and Or Zamir. Undetectable conversations between ai agents via pseudorandom noise-resilient key exchange. arXiv preprint arXiv:2604.04757, 2026.

[35] Aaron D Wyner. The wire-tap channel. Bell system technical journal, 54(8):1355–1387, 1975.

[36] Shuhang Xu and Fangwei Zhong. Comet: Metaphor-driven covert communication for multi-agent language games. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics, pages 7892–7917, 2025.

[37] Hirosuke Yamamoto and Kohji Itoh. Asymptotic performance of a modified schalkwijk-barron scheme for channels with noiseless feedback (corresp.). IEEE Transactions on Information Theory, 25(6):729–733, 1979.

[38] KiYoon Yoo, Wonhyuk Ahn, and Nojun Kwak. Advancing beyond identification: Multi-bit watermark for large language models. arXiv preprint arXiv:2308.00221, 2023.

[39] Or Zamir. Undetectable steganography for language models. Transactions on Machine Learning Research, 2024.

[40] Zachary Ziegler, Yuntian Deng, and Alexander M Rush. Neural linguistic steganography. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 1210–1215, 2019.

## A Information Access to Parties

Table 3 enumerates, for the four parties considered in Fig. 1, the system information access, with $( \checkmark , \times )$ denoting availability. The only pre-shared secret between the legitimate parties is κ. All synchronized decoder-side information is either public or deterministically derived from the public transcript and $\kappa .$ The encoder additionally possesses local information, including the prompt, hidden payload and the model-dependent next-token distribution, that need not be available to the decoder.

Table details. The encoder has access to next-token distribution $s _ { t }$ and per-token control of the sampling loop to solve the OT program (13) and emit the biased token, so a hosted API exposing neither cannot host it. The decoder is receiver-black-box: it never instantiates the model or evaluates $s _ { t } ,$ needing only $\kappa ,$ the public policy, tokenizer and the nonce, from which it reconstructs side information. A passive Eve holds only the public policy, the transcript and cover distribution; lacking κ she can neither derive a key nor decode, and covertness against her is shown empirically in Appendix F. The API adversary additionally chooses $\rho$ and message $m ,$ and can approximate base distribution through repeated queries, but has no access to $\kappa ;$ its advantage is bounded by Theorem 1.

Key-derivation dataflow and deployment. At position t both legitimate parties compute

$$
(\underbrace {\kappa} _ {\text { secret }}; \underbrace {\nu ,   x _ {t - h : t - 1} ,   t} _ {\text { public   /   shared }}) \xrightarrow {F _ {\kappa}} \Lambda_ {t} \longrightarrow \big (k _ {t} ^ {(1)},   k _ {t} ^ {(2)},   R _ {t} \big),\tag{20}
$$

after which the encoder additionally uses $s _ { t }$ and $u _ { t } .$ , while the decoder uses only the emitted token identifier. Two system consequences follow: a text-only channel must assume public tokenization and token IDs, and ν must be freshly drawn.

<table><tr><td>Information item</td><td>Encoder</td><td>Decoder</td><td>Passive Eve</td><td>API adv.  $\mathcal{A}$ </td></tr><tr><td>Policy parameters ( $p, r, \phi, h, \epsilon, \epsilon_{ACK}, \gamma, \gamma_{ACK}, \gamma_{NACK}, T^{*}, F,$  etc.)</td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Tokenizer</td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Public session nonce  $\nu$ </td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Token IDs  $x^{t-1}$ </td><td>√</td><td>√</td><td>√</td><td>√</td></tr><tr><td>Shared seed  $\kappa$ </td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Per-token key  $k_{t}$ , dither  $R_{t}$ , permutation  $\Psi$ , derived (20)</td><td>√</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Model weights / Model</td><td>√</td><td>×</td><td>×</td><td>×</td></tr><tr><td>Prompt  $\rho$ </td><td>√</td><td>×</td><td>×</td><td>√</td></tr><tr><td>Next-token distribution  $s_{t}$ </td><td>√</td><td>×</td><td>√</td><td> $\checkmark^*$ </td></tr><tr><td>Secret message  $m$ </td><td>√</td><td>×</td><td>×</td><td>√</td></tr></table>

Table 3: Information available to each party in a BAM protocol $( { \check { \sqrt { : } } }$ available; ×: not available; $\checkmark \ast .$ available only in approximation).

## B Proof of Theorem 1

Let $F _ { \kappa }$ be the PRF with input shared seed κ. Suppose that the adversary makes $Q$ adaptive API queries (with Q polynomial in λ), choosing the prompt $\rho _ { i }$ and message $m _ { i }$ for each query as arbitrary functions of its previous observations, and observes $L ( \lambda )$ tokens in total. For each query $i \in \{ 1 , \ldots , Q \}$ the challenger samples a public nonce $\nu _ { i } \sim \mathrm { U n i f } ( \{ 0 , 1 \} ^ { \lambda } )$ . BAM’s decoding stopping rule is internal to the communication protocol and does not terminate token generation. The adversary observes only the length τ transcript, not n and therefore here $\begin{array} { r } { L ( \lambda ) = \sum _ { i } \tau _ { i } } \end{array}$ denotes the total number of generated tokens observed by the adversary. Index the observed tokens globally by $j \in \{ 1 , \dots , L ( \lambda ) \}$ , and let $q ( j ) , t _ { j } .$ and $c _ { j }$ denote the query index, within-query token position, and the hashing window associated with token j, respectively. Define

$$
Z _ {j} = \left(\nu_ {q (j)}, t _ {j}, c _ {j}\right), \quad \left(K _ {j}, R _ {j}\right) = \operatorname{Expand} \left(F _ {\kappa} \left(Z _ {j}\right)\right),\tag{21}
$$

where $K _ { j }$ denotes the keying material used by the OT coupling and $R _ { j }$ denotes the posterior-matching randomness. Under a truly random function, these are independent. We assume the following OT marginal constraint

$$
\sup _ {s, u} \left\| \sum_ {k} P _ {K} (k) W _ {X | U, K, S} (x \mid u, k, s) - W _ {X | S} (x | s) \right\| _ {\mathrm{TV}} \leq \eta (\lambda),\tag{22}
$$

where exact distortion-free OT corresponds to $\eta ( \lambda ) = 0$ , where $P _ { K } ( k )$ is the key distribution induced under truly random function.

Define the nonce-collision event $\mathsf { C o l } _ { Q } = \{ \exists i < i ^ { \prime } \leq Q$ such that $\nu _ { i } = \nu _ { i ^ { \prime } } \}$ . Conditioned on ${ \mathsf { C o l } } _ { Q } ^ { c }$ , all inputs $Z _ { j }$ are distinct: the nonce separates diferent API queries, while the strict monotonicity of $t _ { j }$ separates token positions within each query. Let $P _ { \mathrm { R e a l } }$ be the adversary transcript distribution when BAM uses the PRF $F _ { \kappa } { . }$ let $P _ { \mathrm { R F } }$ be the transcript distribution when $F _ { \kappa }$ is replaced by a truly random function $R ,$ and let $P _ { \mathrm { C l e a n } }$ be the transcript distribution under clean LLM generation. For an API adversary A, define the total steganography security advantage of BAM as

$$
\operatorname{Adv} _ {\mathcal {A}} ^ {\mathrm{BAM}} = \left| \operatorname * {P r} \left[ \mathcal {A} ^ {\text { Real }} (1 ^ {\lambda}) = 1 \right] - \operatorname * {P r} \left[ \mathcal {A} ^ {\text { Clean }} (1 ^ {\lambda}) = 1 \right] \right|,\tag{23}
$$

where $\mathcal { A } ^ { \sf R e a l }$ uses BAM generation $\Pi _ { \mathrm { m o d e l } }$ and $\mathcal { A } ^ { \mathsf { C l e a n } }$ uses base distribution $W _ { X \mid S } ( 9 )$ . The security advantage of the PRF against a distinguisher B is

$$
\mathrm{Adv} _ {\mathcal {B}} ^ {\mathrm{PRF}} = \left| \operatorname * {P r} _ {\kappa} \left[ \mathcal {B} ^ {F _ {\kappa}} (1 ^ {\lambda}) = 1 \right] - \operatorname * {P r} _ {R} \left[ \mathcal {B} ^ {R} (1 ^ {\lambda}) = 1 \right] \right|.\tag{24}
$$

We first compare real PRF BAM with random-function BAM using standard argument. The distinguisher B is given oracle access to a function O, which is either $\mathcal { O } = F _ { \kappa }$ or $\mathcal { O } = R$ . For each query, A supplies both the prompt $\rho _ { i }$ and the message $m _ { i }$ , which B uses directly in the simulated BAM generation. For each API query $i ,$ it samples and returns a fresh public nonce $\nu _ { i }$ . Whenever BAM needs side information at token position $j ,$ B computes $( K _ { j } , R _ { j } ) = \mathsf { E x p a n d } ( \mathcal { O } ( Z _ { j } ) )$ , samples the next token according to the BAM channel, and returns that token to A. When $\mathcal { A }$ outputs its final bit, B outputs the same bit. If $\mathcal { O } = F _ { \kappa }$ , then $\mathcal { A }$ sees the real BAM API. If $\mathcal { O } = R$ then $\mathcal { A }$ sees the random-function BAM API. Therefore,

$$
\left. \right.\left| \operatorname * {P r} \left[ \mathcal {A} ^ {\text { Real }} (1 ^ {\lambda}) = 1 \right] - \operatorname * {P r} \left[ \mathcal {A} ^ {\text { RF }} (1 ^ {\lambda}) = 1 \right]\right| \leq \operatorname{Adv} _ {\mathcal {B}} ^ {\text { PRF }}.\tag{25}
$$

It remains to compare $P _ { \mathrm { R F } }$ and $P _ { \mathrm { C l e a n } }$ , which we prove with a coupling argument. Couple the random-function BAM and clean generation processes token by token. Suppose that before position $j ,$ the two coupled transcripts are identical and that Col has not occurred. Then both processes have the same base LLM next-token distribution $W _ { X | S } ( x _ { j } | s _ { j } )$ . Since $Z _ { j }$ is a fresh input to the random function, its output is independent of all previous random-function outputs. Let $H _ { j } = h _ { j }$ denote the complete history prior to token $j ,$ , including all previous transcripts and the adversary’s adaptively chosen prompts and messages. For the query containing token $j ,$ , the channel input $U _ { j }$ may therefore depend arbitrarily on the chosen message $m _ { q ( j ) }$ , the history $h _ { j }$ and the posterior-matching randomness $R _ { j }$ . However, under true random-function, $K _ { j }$ is independent of $R _ { j }$ and of all prior information. Consequently,

$$
P _ {\mathrm{RF}} (K _ {j} = k \mid H _ {j} = h _ {j}, U _ {j} = u, \mathsf {C o l} _ {Q} ^ {c}) = P _ {K} (k).\tag{26}
$$

Hence the adversary-visible next-token law in the random-function BAM process is

$$
\begin{array}{c} P _ {\mathrm{RF}} (x _ {j} \mid h _ {j}, \mathsf {C o l} _ {Q} ^ {c}) = \sum_ {u} P _ {\mathrm{RF}} (u \mid h _ {j}, \mathsf {C o l} _ {Q} ^ {c}) \\ \times \sum_ {k} P _ {K} (k) W _ {X | U, K, S} (x _ {j} \mid u, k, s _ {j}). \end{array}\tag{27}
$$

By the OT marginal constraint, for every $u ,$

$$
\left\| \sum_ {k} P _ {K} (k) W _ {X | U, K, S} (\cdot \mid u, k, s _ {j}) - W _ {X | S} (\cdot \mid s _ {j}) \right\| _ {\mathrm{TV}} \leq \eta (\lambda).\tag{28}
$$

Therefore, by convexity of total variation distance,

$$
\begin{array}{l} \left\| P _ {\mathrm{RF}} (\cdot \mid h _ {j}, \mathsf {C o l} _ {Q} ^ {c}) - W _ {X | S} (\cdot \mid s _ {j}) \right\| _ {\mathrm{TV}} \\ \leq \sum_ {u} P _ {\mathrm{RF}} (u \mid h _ {j}, \mathsf {C o l} _ {Q} ^ {c}) \times \\ \left\| \sum_ {k} P _ {K} (k) W _ {X | U, K, S} (\cdot \mid u, k, s _ {j}) - W _ {X | S} (\cdot \mid s _ {j}) \right\| _ {\mathrm{TV}} \\ \leq \eta (\lambda). \end{array}\tag{29}
$$

Importantly, this bound holds for every $u ,$ and therefore for every message $m _ { q ( j ) } .$ , since the message afects the next-token law only through the induced channel input $U _ { j }$ . Therefore, as long as no nonce collision has occurred and the coupled transcripts have not difered, the two conditional next-token laws have TV at most $\eta ( \lambda )$ . By maximal coupling [30, Chapter 7.3], the two next tokens can be sampled to be equal with probability at least $1 - \eta ( \lambda )$ . A nonce collision contributes at most $\operatorname* { P r } ( \mathsf { C o l } _ { Q } )$ Thus, there exists a coupling of the two transcript distributions that fails with probability at most $\operatorname* { P r } ( \operatorname { C o l } _ { Q } ) + L ( \lambda ) \eta ( \lambda )$ ) apart, and hence

$$
\left\| P _ {\mathrm{RF}} - P _ {\text {Clean}} \right\| _ {\mathrm{TV}} \leq \operatorname * {P r} (\mathsf {C o l} _ {Q}) + L (\lambda) \eta (\lambda).\tag{30}
$$

Finally, by the triangle inequality,

$$
\begin{array}{c} \operatorname{Adv} _ {\mathcal {A}} ^ {\text {BAM}} \leq \operatorname{Adv} _ {\mathcal {B}} ^ {\text {PRF}} + \| P _ {\text {RF}} - P _ {\text {Clean}} \| _ {\text {TV}} \\ \leq \operatorname{Adv} _ {\mathcal {B}} ^ {\text {PRF}} + \operatorname * {P r} (\mathsf {C o l} _ {Q}) + L (\lambda) \eta (\lambda). \end{array}\tag{31}
$$

Since the nonces are sampled independently and uniformly from $\{ 0 , 1 \} ^ { \lambda }$ , we have

$$
\operatorname * {P r} (\mathsf {C o l} _ {Q}) \leq \frac {Q (Q - 1)}{2 ^ {\lambda + 1}}.\tag{32}
$$

Thus, for an adaptive adversary making Q(λ) API queries and observing L(λ) tokens,

$$
\mathrm{Adv} _ {\mathcal {A}} ^ {\mathrm{BAM}} (\lambda) \leq \mathrm{Adv} _ {\mathcal {B}} ^ {\mathrm{PRF}} (\lambda) + \frac {Q (\lambda) (Q (\lambda) - 1)}{2 ^ {\lambda + 1}} + L (\lambda) \eta (\lambda).\tag{33}
$$

Finally, since $F _ { \kappa }$ is a secure PRF, Q(λ) and $L ( \lambda )$ are polynomial in λ, and $\eta ( \lambda ) = 0$ by exact OT construction, we have

$$
\mathrm{Adv} _ {\mathcal {A}} ^ {\mathrm{BAM}} (\lambda) \leq \mathrm{negl} (\lambda) + \mathrm{negl} (\lambda).\tag{34}
$$

## C Experimental Setup Details for Section 7.3

Shared protocol. Over 1000 runs, 200 Prompts are drawn from C4 RealNews excerpts truncated to 32 tokens, with a fixed seed. Generation samples at top-50, temperature 1.0 with EOS disabled. Each baseline uses its authors’ oficial implementation and default configuration unless noted. For optimal transport coupling, we solve the entropic-regularized problem with the Sinkhorn matrix-scaling algorithm in the log domain: entropic regularization $\lambda _ { \mathrm { S } } = 0 . 2$ (Note that entropy regularization encourages non-deterministic solution with the potential cost of quality drop, but it does not afect the marginal constraint of the transport plan), capped at 4000 scaling iterations, with a tolerance of $1 0 ^ { - 4 }$ . For the C4 RealNews dataset tested, the likelihood parameters (0.4, 0.4) (where $0 \leq \epsilon , \epsilon _ { \mathrm { A C K } } < 1 )$ are chosen by a simple grid search with precision 0.2. In particular, contaminated Laplacian likelihood is used because it is a strong empirical noise model for our setting.

ArcMark. We choose $p = 4 , r = 4$ , 3-token hashed context; based on the paper, the payload is encoded by a rate-matched random linear code over $\mathbb { F } _ { 4 }$ of length n and decoded by maximum-likelihood scoring over the codebook.

MPAC. Main paper configuration: $\gamma = 0 . 2 5$ , radix r = 4 (4 message positions), left-hash seeding, position allocation via the default position PRF, bias δ = 1.5 (the MPAC(1.5) operating point); decoding and error accounting use MPAC’s own detector.

BiMark. Released defaults: base scaling factor 0.2, L = 20 vocabulary partitions (seeds fixed and shared with the decoder), 2-token window, internal top-50. Tied bit counts decode as unknown and score as errors under BiMark’s own hit accounting.

StealthInk. Chunk capacity of 1 bit per position (8 positions for our 8-bit payload), 3-gram seeding, following the released implementation.

## D Scalability and Ablation Study

We answer two questions in this appendix:

D.1 Scalability of BAM: How does runtime scale with exponentially large message size, and what design choices should be incorporated to reduce runtime?

D.2 Sources of gain: Which components of BAM lead to the performance gain compared to other state-of-the-art baselines?

## D.1 Scalability Study on BAM

We expand on the runtime experiment presented in Section 7. In practical communication systems, it is standard practice to subpacketize longer message payloads to enable more eficient decoding, albeit at the cost of a higher error rate. The decoding time of a message is exponential in its length, a cost that becomes even more prohibitive in adaptive settings, where the encoder must also compute the decoder’s posterior.

Setup All experiments are conducted using Llama-3.1-8B on C4 RealNews over N=1000 paired trials. We inherit all other experimental settings from Appendix C. For a 24-bit payload, we evaluate three subpacketization schemes:

$1 \times 2 4$ : Joint decoding over $2 ^ { 2 4 }$ possible messages.

$2 \times 1 2 \colon$ Two packets of $2 ^ { 1 2 }$ messages each.

$3 \times 8 \colon$ Three packets of $2 ^ { 8 }$ messages each.

Runtime is decomposed per sampled token into encoding (side information generation and OT channel synthesis), token generation (LLM forward pass and sampling), and decoding (posterior update and threshold decoding). We exclude the posterior update from the reported encoding runtime to isolate the time spent on side information generation and OT; in practice, total encoding runtime is approximately the sum of the encoding and decoding components in Table 4.

Evaluation As shown in Table 4, encoding and generation runtimes scale linearly with output length, with token generation accounting for the vast majority of total runtime. Joint decoding achieves the highest accuracy, attaining a transmission rate over 0.25 bits/token with less than a 2% message error rate. However, joint decoding leads to an exponential surge in decoding overhead, which is further compounded by the encoder’s need to compute the posterior. Nevertheless, a key advantage of BAM is that it requires no pre-stored, exponentially long codebooks across independently deployed agents, eliminating an otherwise impractical system assumption. It is also worth noting that tightening the Sinkhorn tolerance and increasing the iteration steps will marginally improve the performance at the cost of slower encoding time.

## D.2 Ablation Study on BAM

We use an ablation study to separate the three mechanisms introduced by BAM: online posteriormatching codebook generation, variable-length stopping, and ACK/NACK confirmation. We report error on both linear and semi-log scales; the latter makes it easier to compare how rapidly the empirical decoding error decreases as additional tokens are available. An important performance metric for this section is the reliability function (6).

Setup To isolate these individual sources of gain, we compare BAM against three ablation baselines:

1. BAM-one-phase: A single-phase variant of BAM.

2. BAM-fixed-length: A single-phase, fixed-length variant of BAM.

3. ArcMark: [13].

Table 4: Scalability study for a 24-bit payload under BAM, <sup>∗</sup> Encoding time excludes posterior computation.

<table><tr><td rowspan="2">L</td><td rowspan="2">Scheme</td><td rowspan="2">Error rate</td><td rowspan="2">Avg. tokens</td><td colspan="4">Runtime (ms/token)</td></tr><tr><td>Enc*.</td><td>Gen.</td><td>Dec.</td><td>Total</td></tr><tr><td rowspan="3">4</td><td>1 × 24</td><td>0.107 ± 0.010</td><td>75.2 ± 1.4</td><td>7.33 ± 0.02</td><td>19.733 ± 0.003</td><td>6.566 ± 0.010</td><td>33.63</td></tr><tr><td>2 × 12</td><td>0.159 ± 0.012</td><td>75.3 ± 0.9</td><td>7.32 ± 0.02</td><td>19.799 ± 0.003</td><td>0.2497 ± 0.0004</td><td>27.36</td></tr><tr><td>3 × 8</td><td>0.194 ± 0.013</td><td>75.5 ± 0.8</td><td>7.31 ± 0.03</td><td>19.628 ± 0.006</td><td>0.1393 ± 0.0002</td><td>27.08</td></tr><tr><td rowspan="3">64</td><td>1 × 24</td><td>0.017 ± 0.004</td><td>86.0 ± 1.9</td><td>7.35 ± 0.02</td><td>19.809 ± 0.003</td><td>6.04 ± 0.01</td><td>33.20</td></tr><tr><td>2 × 12</td><td>0.024 ± 0.005</td><td>96.9 ± 2.3</td><td>7.28 ± 0.02</td><td>19.814 ± 0.003</td><td>0.2240 ± 0.0005</td><td>27.32</td></tr><tr><td>3 × 8</td><td>0.035 ± 0.006</td><td>102.7 ± 2.3</td><td>7.16 ± 0.02</td><td>19.186 ± 0.010</td><td>0.1190 ± 0.0003</td><td>26.47</td></tr><tr><td rowspan="3">2048</td><td>1 × 24</td><td>0.011 ± 0.003</td><td>95.4 ± 2.6</td><td>7.16 ± 0.02</td><td>18.936 ± 0.002</td><td>5.58 ± 0.02</td><td>31.68</td></tr><tr><td>2 × 12</td><td>0.016 ± 0.004</td><td>111.9 ± 2.7</td><td>7.08 ± 0.02</td><td>18.953 ± 0.002</td><td>0.1921 ± 0.0006</td><td>26.22</td></tr><tr><td>3 × 8</td><td>0.020 ± 0.004</td><td>124.4 ± 2.6</td><td>7.15 ± 0.03</td><td>19.152 ± 0.004</td><td>0.1108 ± 0.0003</td><td>26.41</td></tr><tr><td rowspan="3">32768</td><td>1 × 24</td><td>0.007 ± 0.003</td><td>101.0 ± 2.6</td><td>7.70 ± 0.05</td><td>19.305 ± 0.007</td><td>5.29 ± 0.02</td><td>32.30</td></tr><tr><td>2 × 12</td><td>0.010 ± 0.003</td><td>117.8 ± 2.3</td><td>7.53 ± 0.04</td><td>19.429 ± 0.007</td><td>0.2073 ± 0.0006</td><td>27.17</td></tr><tr><td>3 × 8</td><td>0.021 ± 0.005</td><td>140.1 ± 2.7</td><td>7.49 ± 0.05</td><td>19.354 ± 0.009</td><td>0.1237 ± 0.0004</td><td>26.97</td></tr></table>

Specifically, BAM-one-phase utilizes Algorithm 1, where the decoder declares the estimated message mˆ at time t whenever

$$
\exists t > 0, \hat {m} \in \mathcal {M} \quad \mathrm{suchthat} \quad \pi_ {t} (\hat {m}) > 1 - L ^ {- 1},\tag{35}
$$

where L matches the belief threshold used in BAM’s confirmation phase. BAM-fixed-length further eliminates variable-length stopping from BAM-one-phase, instead committing to message ˆm at a fixed token length $t ^ { \prime }$ via maximum a posteriori (MAP) decoding:

$$
\hat {m} = \arg \max _ {m \in \mathcal {M}} \pi_ {t ^ {\prime}} (m).\tag{36}
$$

In this part, all experiments are conducted using Mistral-7B-v0.3 on C4 RealNews over $N { = } 2 0 0 0$ paired trials. We used a 8-bit payload with thresholds $L \in \{ 2 , 2 ^ { 2 } , 2 ^ { 3 } , 2 ^ { 4 } , 2 ^ { 5 } , 2 ^ { 6 } , 2 ^ { 7 } , 2 ^ { 9 } , 2 ^ { 1 1 } \}$ , with other simulation settings unchanged from Appendix C. The increase in iteration count and reduce in threshold are to guarantee a smoother curve on the semi-logy scale, when the error variance can be high.

Evaluation Fig. 3 presents the simulation result in both linear and semi-log scale. Compared to ArcMark [13], the empirical gain arises from three components. First, posterior matching improves the operating point (a horizontal shift in the semi-log scale) without changing the empirical slope, consistent with posterior-matching’s role as an eficient rate improvement rather than a reliability function improvement [32]. Second, variable-length stopping contributes a sequentiality gain (with slight abuse of terminology, we use sequentiality and adaptivity gains to describe an empirical finite length approximation of the gradient of decoding error, this is not a statement on asymptotic informationtheoretic guarantee). Third, the two-phase Yamamoto-Itoh confirmation contributes an adaptivity gain. Sequentiality and adaptivity gains manifest empirically as a steeper decay of decoding error (a larger reliability function (6)) in the semi-log scale.

## E Algorithm Pseudocode and Visualization

This appendix collects the pseudocode for the posterior-matching feedback code (Algorithm 1) and the complete BAM protocol (Algorithm 2) described in Section 4. In addition, Figure 5 illustrates the posterior matching procedure. At each token, the encoder maps the transmitted message to a channel input by inverse-CDF sampling with respect to the current posterior belief. After observing the generated token, the decoder updates its posterior according to (16), progressively concentrating probability mass on the transmitted message. Since the feedback is noiseless, the encoder performs the same update and therefore remains synchronized with the decoder throughout transmission.

![](images/aeab9231645aeb07f571dd91e0ea72a85c071a76053d5ce07864e31e1095fdb5.jpg)

(b)  
![](images/103376ce70688d6db043404c62be2edc46c4a28911a1cc002fabbdcd3254fc11.jpg)  
Figure 3: Ablation study of BAM; (a): Linear Scale ; (b): Semilogy Scale

![](images/c6fadb03518819579e29ff3fbaa1f86b51b9c750f496373e287699d3e26377a3.jpg)  
Figure 4: Seed-marginalized per-token KL divergence between the stego and cover distributions, averaged over the sequence, on Llama-3.1-8B and C4 News with $| \mathcal { K } ^ { ( 1 ) } | = 4$ , estimated by Monte Carlo over $1 \bar { 0 } ^ { 4 } , 5 \times 1 0 ^ { 4 }$ , and $1 0 ^ { 5 }$ uniformly random 128-bit seeds.

![](images/e4f3042bd17f53d2f114cace71636cbbeaeb23c561d6f4111e9722c2d9e1d764.jpg)  
Figure 5: Toy example of posterior-matching belief with $M = 1 6$ messages, true message index 11 and input alphabet size $p = 4$

## F Empirical KL Divergence per Token

The KL divergence in the sense of Cachin [4] measures the KL between cover and stego distributions seen by a passive observer without the shared seed. Under a uniform key, the ideal OT coupling reproduces the base marginal exactly, while a finite-precision implementation may introduce a small numerical residual. This experiment therefore probes the combined efect of the realized PRF schedule and numerical OT approximation after seed marginalization, using a stronger per-token version of [4] as defined in Definition 5.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 Posterior-Matching Feedback Coding.

Require: message set M, true message m (encoder only), alphabet size p, phase  $\phi$ , shared seed  $\kappa$ , public session nonce; decoder belief  $\pi_{0}(m') = 1/|\mathcal{M}|$ 

1:  $t \leftarrow 0$ 

2: while stopping rule  $\exists m', \pi_{t}(m') &gt; \gamma$  not met do

3:  $t \leftarrow t + 1$ 

4: both parties: derive  $(k_{t}, R_{t})$  via (12)

5: encoder: derive  $u_{t}$  from  $\pi_{t-1}$ , m,  $R_{t}$  via (10)

6: encoder: synthesize channel by solving the transport plan (13)

7: encoder: sample  $x_{t} \sim W_{X_{t}|U_{t}, K_{t}, S_{t}}^{*}$ 

8: decoder: observe  $x_{t}$ ; estimate  $\hat{C}_{t}$ 

9: both parties: compute  $u_{t}(m')$  for all  $m'$  from  $\pi_{t-1}$ ,  $R_{t}$ ; score  $\ell_{t}(u_{t}(m'))$  via (15)

10: both parties: update  $\pi_{t}$  via (16)

11: end while
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 BAM protocol. Public parameters ( $\gamma, \gamma_{ACK}, \gamma_{NACK}, (\epsilon, \epsilon_{ACK}), T^{*}$ )

Require: message set M, true message m (encoder only), alphabet size p, phase  $\phi$ , shared seed  $\kappa$ , public session nonce; decoder belief  $\pi_{0}(m') = 1/|\mathcal{M}|$ 

1:  $t \leftarrow 0$ 

2: while  $t &lt; T^{*}$  do

3: Communication: run Alg. 1 with current t, until  $\max_{m'} \pi_{t}(m') &gt; \gamma$  or  $t \geq T^{*}$ 

4: if  $\max_{m'} \pi_{t}(m') &gt; \gamma$  then

5:  $m' \leftarrow \arg\max_{m''} \pi_{t}(m'')$ 

6: Confirmation:  $u_{ACK}=0$ ,  $u_{NACK}=1$ .

7: encoder: Transmits  $u_{ACK}$  iff  $m'=m$ , until  $\pi(u_{ACK}) &gt; \gamma_{ACK}$ ,  $\pi(u_{NACK}) &gt; \gamma_{NACK}$ , or  $t \geq T^{*}$ 

8: both parties: score  $\ell_{t}(u_{ACK})$  and  $\ell_{t}(u_{NACK})$  via (15) with p = 2 and  $\epsilon_{ACK}$ 

9: if  $\pi(u_{ACK}) &gt; \gamma_{ACK}$  then

10: accept: commit  $m'$ ; if  $m' \neq m$  then declare a decoding error

11: return  $m'$ 

12: else if  $\pi(u_{NACK}) &gt; \gamma_{NACK}$  then

13: both parties: update belief

14:  $\pi_{t}(m') \leftarrow \frac{1 - \gamma_{NACK}}{\gamma_{NACK}} \pi_{t}(m')$ ; renormalize  $\pi_{t}$ 

15: end if

16: end if

17: end while

18: timeout: commit  $\hat{m} = \arg\max_{m'} \pi_{t}(m')$
</div>

We estimate the seed-marginalized divergence of Section 5.2: $W _ { X \mid S }$ is the unbiased distribution from the model, and the seed-marginal is approximated by averaging the biased channel over $1 0 ^ { 4 } , 5 \times 1 0 ^ { 4 }$ and $1 0 ^ { 5 }$ uniformly random sampled seeds (out of $2 ^ { 1 2 8 }$ possible seeds), each inducing its per-token key through the PRF. Here $r = | \mathcal { K } ^ { ( 1 ) } | = 4$ and the 128-bit seed enters only as PRF randomness. Same as Appendix C, we use entropic regularized $\lambda _ { \mathrm { S } } = 0 . 2$ Sinkhorn, capped at 4000 scaling iterations, with a tolerance of $1 0 ^ { - 4 }$ (a tighter tolerance results in a smaller empirical KL). As can be seen in Fig. 4, the Monte Carlo residual decreases with the seed count, while the accumulated divergence grows approximately linearly in n. Under an ideal uniform key and exact OT solution, the KL divergence σ is zero; the remaining deviation in the implemented system reflects finite-sample estimation and numerical OT precision.

## G Additional Experimental Details for Section 7.4

## G.1 Experimental Setup Details

Harness. Each cell fixes one covert task and one cover setting and runs N = 100 dialogues of $R =$ 10 rounds on one instruct model (one round is one instance of point-to-point conversation, not bidirectional). Generation uses temperature 1.0, top-50, OT coupling with $p = | \mathcal { U } | = 4 , r = | \mathcal { K } ^ { ( 1 ) } | = 4 ;$ $\phi = 0 , h = 3 , F _ { \kappa } = \mathrm { H M A C - S H A 2 5 6 , } \lambda = 1 2 8$ , and Sinkhorn (reg 0.2, ≤ 4000 iters, tol $1 0 ^ { - 4 } )$ . The protocol setting is BAM(0.5, 0.75, 0.75, (0.7, 0.3), 800). Under the Section 6 adaptive threshold rule, a payload whose confirmation belief π $( u _ { \mathrm { A C K } } )$ is below 0.75 at EOS spills to a later turn by opposing agent sending a clean response (up to 3 spills and $T ^ { * } { \mathrm { - t o k e n } }$ budget across turns). Role prompts are topic-agnostic; 50 GPT-5.5 (topic, opener) scenarios per setting are cycled so each seeds two dialogues, with a per-dialogue seed also fixing the topic-matched clean dialogue used for the quality comparison.

Source coding. At a position with n legal moves the payload is the index $m \in \{ 0 , \ldots , n - 1 \}$ of a uniformly chosen move, carrying $\log _ { 2 } n$ bits. For the scope of this work, we do not assume the distribution of moves or any human preference. Therefore, moves are enumerated in a fixed deterministic order (raster order for tic-tac-toe and 19×19 Go; python-chess order for chess); both parties replay the shared history to rebuild the same ordered list and invert the index. The alphabet is $\mathcal { M } = \{ 0 , \ldots , n - 1 \}$ so non-dyadic $| { \mathcal { M } } |$ needs no bit padding. Since n varies by position, the $2 . 3 / 5 . 0 / 8$ .4-bit task averages are empirical means of $\log _ { 2 }$ n over visited positions, not constants.

Error handling. Each dialogue contains ten message-transmission rounds. After an incorrect decode, we retain the sender’s task trajectory when generating subsequent payloads so that every dialogue contains the same number of transmission opportunities. This resynchronization is used only for evaluation bookkeeping and does not erase the decoding failure: the incorrectly decoded payload is counted toward message error, and the dialogue is counted as erroneous whenever at least one payload is decoded incorrectly. Thus, subsequent rounds measure additional channel transmissions rather than cascading task-state errors caused by an earlier failure.

Metrics. Index dialogues $d = 1 , \ldots , N$ . Let $\mathcal { C } _ { d }$ (each dialogue carries 10 rounds of message) be the completed, correctly received payloads, with $c _ { d } , e _ { d }$ correct and wrong decodes and $B _ { d }$ correctly delivered bits. Token counts are $W _ { d }$ (all payload-carrying tokens (stego tokens)) and $F _ { d }$ (filler-turn tokens (clean tokens)).

$\begin{array} { r } { B i t s / t o k e n = \frac { \sum _ { d } B _ { d } } { \sum _ { d } W _ { d } + F _ { d } } } \end{array}$

• Message $\begin{array} { r } { e r r o r = \frac { \sum _ { d } e _ { d } } { \sum _ { d } c _ { d } + e _ { d } } . } \end{array}$

• Dialogue error $\begin{array} { r } { = \frac { 1 } { N } \sum _ { d } \mathbf { 1 } [ e _ { d } > 0 ] } \end{array}$

• Avg. payload/dialogue $\begin{array} { r } { = \frac { 1 } { N } \sum _ { d } | { \mathcal { C } } _ { d } | . } \end{array}$

$\begin{array} { r } { E f f i c i e n c y = \frac { \sum _ { d } W _ { d } } { \sum _ { d } W _ { d } + F _ { d } } } \end{array}$

## G.2 Additional results using diferent covertext

Table 5 reports additional results using a forum-exchange covertext, whose longer token generation turns provide a larger embedding throughput than casual chat. Without changing the underlying BAM protocol, this increase in available covertext substantially improves both reliability and payload completion across all three models. Llama-3.1 achieves below 1% message error across all tasks, while Phi-4 nearly completes all ten payloads per dialogue with no decoding errors. For the lower-entropy Qwen model, message error decreases from $3 . 8 \% - 9 . 4 \%$ in Table 2 to $0 . 6 \% { - 2 . 6 \% }$ in Table 5. These results show that low model entropy does not preclude covert agentic communication, but places greater demands on the carrying opportunity provided by the covertext. More generally, the conversational setting can be optimized through prompt design to better match the available transmission budget to the covert payload demand; systematically optimizing this covertext-payload tradeof is beyond the scope of this work.

## G.3 Prompt to Judge the Quality of Conversational Text

We use the Gemini-3.1-Pro-Preview (Accessed Aug 10-24) as our LLM judge. Fig. 7 shows the prompt used to elicit a pairwise quality preference between a watermarked transcript and its seed-matched clean counterpart. Each pair is judged in an independent API call with temperature 0. To control for the position bias of LLM judges, we randomize all pairs.

## G.4 Example Agentic Conversation Setup

Table 6 shows one example instruction for the casual-chat setting used in Table 2 (the complete conversational profiles are provided in the code release), and Fig 6 shows the corresponding conversation from the casual-chat rollout.

![](images/53bec540341872448945714e226a06cfefb8f480b1e94caee03e85cff941d926.jpg)  
Figure 6: Example five-round covert conversation (casual-chat cover, Llama-3.1-8B-Instruct) in which the two agents secretly play tic-tac-toe. The notation a/b indicates that a payload-carrying tokens out of b total tokens are used in this round. All five payloads are decoded correctly.

![](images/074ec55238a92ffadd66a3a45b816868f7a6628215913020102441c96afa3618.jpg)  
Figure 7: The prompt for querying the LLM judge for pairwise quality evaluation.

Table 5: Turn-based covert channel on the forum exchange covertext, across three open-weight instruct models and three embedding tasks. Values are mean $\pm \ \mathrm { S E }$ over 100 dialogues per cell.

<table><tr><td colspan="2">Forum exchange covertext</td><td colspan="3">Embedding task</td></tr><tr><td>Model</td><td>Metric</td><td>tictactoeavg. 2.3 bits</td><td>chessavg. 5.0 bits</td><td>go19avg. 8.4 bits</td></tr><tr><td rowspan="6">Llama-3.1-8B-Instructavg. entropy1.743 bits/tok,len 101.6 tok</td><td>Bits/token</td><td> $0.0240 \pm 0.0004$ </td><td> $0.0434 \pm 0.0007$ </td><td> $0.0723 \pm 0.0013$ </td></tr><tr><td>Avg payload/dialogue</td><td> $9.84 \pm 0.05$ </td><td> $9.38 \pm 0.10$ </td><td> $7.57 \pm 0.18$ </td></tr><tr><td>Dialogue error rate</td><td> $0.010 \pm 0.010$ </td><td> $0.010 \pm 0.010$ </td><td> $0.050 \pm 0.022$ </td></tr><tr><td>Message error rate</td><td> $0.0010 \pm 0.0010$ </td><td> $0.0011 \pm 0.0011$ </td><td> $0.0066 \pm 0.0031$ </td></tr><tr><td>Efficiency (%)</td><td> $99.56 \pm 0.17$ </td><td> $98.33 \pm 0.35$ </td><td> $92.56 \pm 0.71$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>45 / 0 / 55</td><td></td></tr><tr><td rowspan="6">Phi-4-14B-Instructavg. entropy1.901 bits/tok,len 220.6 tok</td><td>Bits/token</td><td> $0.0111 \pm 0.0002$ </td><td> $0.0210 \pm 0.0004$ </td><td> $0.0389 \pm 0.0007$ </td></tr><tr><td>Avg payload/dialogue</td><td> $9.98 \pm 0.02$ </td><td> $10.00 \pm 0.00$ </td><td> $9.94 \pm 0.03$ </td></tr><tr><td>Dialogue error rate</td><td> $0.000 \pm 0.000$ </td><td> $0.000 \pm 0.000$ </td><td> $0.010 \pm 0.010$ </td></tr><tr><td>Message error rate</td><td> $0.0000 \pm 0.0000$ </td><td> $0.0000 \pm 0.0000$ </td><td> $0.0010 \pm 0.0010$ </td></tr><tr><td>Efficiency (%)</td><td> $99.97 \pm 0.04$ </td><td> $100.00 \pm 0.00$ </td><td> $99.91 \pm 0.07$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>52 / 10 / 38</td><td></td></tr><tr><td rowspan="6">Qwen3-A3B-30B-Instructavg. entropy1.128 bits/tok,len 122.6 tok</td><td>Bits/token</td><td> $0.0191 \pm 0.0003$ </td><td> $0.0321 \pm 0.0005$ </td><td> $0.0433 \pm 0.0011$ </td></tr><tr><td>Avg payload/dialogue</td><td> $9.26 \pm 0.12$ </td><td> $8.09 \pm 0.18$ </td><td> $4.50 \pm 0.19$ </td></tr><tr><td>Dialogue error rate</td><td> $0.060 \pm 0.024$ </td><td> $0.060 \pm 0.024$ </td><td> $0.120 \pm 0.033$ </td></tr><tr><td>Message error rate</td><td> $0.0065 \pm 0.0024$ </td><td> $0.0087 \pm 0.0036$ </td><td> $0.0267 \pm 0.0084$ </td></tr><tr><td>Efficiency (%)</td><td> $98.14 \pm 0.33$ </td><td> $95.14 \pm 0.57$ </td><td> $83.65 \pm 0.70$ </td></tr><tr><td>Quality (w/t/l)</td><td></td><td>52 / 2 / 46</td><td></td></tr></table>

<table><tr><td colspan="2">Conversational Profile (Casual Chat)</td></tr><tr><td>shared background</td><td>A casual text-message chat between two friends catching up about their weekend. Opener: yo how was your weekend? mine was pretty chill, mostly just stayed in and watched stuff lol</td></tr><tr><td>Agent A instruction</td><td>You are Friend A in a casual text chat. Reply naturally, like a real text message, lowercase and conversational. Reply should be within 50 words.</td></tr><tr><td>Agent B instruction</td><td>You are Friend B in a casual text chat. Reply naturally, like a real text message, lowercase and conversational. Reply should be within 50 words.</td></tr></table>

Table 6: Conversational profile example used for the covert agentic communication experiments.
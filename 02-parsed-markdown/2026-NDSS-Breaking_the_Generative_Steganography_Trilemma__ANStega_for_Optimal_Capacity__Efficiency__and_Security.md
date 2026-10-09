# Breaking the Generative Steganography Trilemma: ANStega for Optimal Capacity, Efficiency, and Security

![](images/72540d901edd0418564f112e482f0c056f0fa5078a104001042fd3989d6867f1.jpg)

Yaofei Wang<sup>∗</sup> Weilong Pang<sup>∗</sup> Kejiang Chen<sup>†</sup> Jinyang Ding<sup>†</sup>

Donghui Hu<sup>∗</sup> Weiming Zhang<sup>†</sup> Nenghai Yu<sup>†</sup>

<sup>∗</sup>Hefei University of Technology <sup>†</sup>University of Science and Technology of China Email: <sup>∗</sup>{wyf@,pangwl@mail.,hudh@}hfut.edu.cn <sup>†</sup>{chenkj@,source@mail.,zhangwm@,ynh@}ustc.edu.cn

Abstract—Generative steganography shows immense promise for covert communication, yet existing methods are often constrained by a trilemma of capacity, efficiency, and security. Methods based on Huffman Coding (HC) suffer from poor efficiency and security, while those based on Arithmetic Coding (AC), despite achieving optimal capacity, also pose security risks. Although recent provably secure methods have addressed the security issue, they often do so at the cost of elevated embedding complexity or diminished capacity—failing to match the high capacity exhibited by AC-based methods. To address this trilemma, we adapt Asymmetric Numeral Systems (ANS) for steganography. Our core insight is to repurpose the ANS state machine, using its decoding function for embedding and its encoding function for extraction. To translate this concept into a practical system, we introduce several key innovations. First, we incorporate a streaming architecture with state renormalization to enable the stable embedding of arbitrarily long messages. Second, we employ direct floating-point arithmetic, avoiding costly probability-to-frequency conversions to reduce complexity and precision loss. More critically, we introduce an innovative cryptographic mask mechanism that ensures the sampling process is driven by a cryptographically secure pseudo-random number generator, thereby achieving provable security. Finally, by optimizing core computations into highly efficient bitwise shift operations, ANStega achieves exceptional embedding and extraction speeds. Experimental results validate that ANStega simultaneously achieves optimal embedding capacity, optimal efficiency (embedding complexity with O(1)) and optimal security, successfully resolving the long-standing trilemma in generative steganography.

## I. INTRODUCTION

In today’s environment of increasing online surveillance and widespread traffic analysis [1], [2], the ability to share information without revealing that a conversation is taking place has become as important as protecting the content of the messages themselves. While encryption protects content, it exposes metadata [3]. This vulnerability can be exploited by adversaries to infer relationships between individuals or to enforce censorship. Steganography [4] addresses this by embedding secret data within innocuous media. This method ensures that the act of sending messages remains undetectable and appears indistinguishable from normal data exchange. Furthermore, these covert channels facilitate digital “dead drop” workflows [5], allowing a hidden message to be posted in a public forum and discreetly retrieved by the intended recipient without any traceable interaction. This approach extends privacy protections beyond what encryption alone can offer.

![](images/cd48c64833914c51fbc70f5cb7239644a4bc3d55276f9a4b09d8aba9fe328055.jpg)  
Fig. 1: Comparison of entropy-coding schemes for generative steganography. Top: Huffman coding maps bits to tokens via dynamic trees, causing distributional deviation. Middle: Arithmetic Coding (AC) operates on cumulative intervals but suffers from precision limitations and rescaling overhead. Bottom: ANStega (ours) utilizes constant-time state updates based on Asymmetric Numeral Systems, achieving near-entropy capacity with distributional indistinguishability.

Recently, the emergence of powerful generative models, particularly Large Language Models (LLMs), has catalyzed a significant shift in steganographic methodologies. Unlike traditional approaches that modify existing covers and risk detectable statistical anomalies [22], [23], generative steganography leverages powerful generative models to synthesize high-entropy, natural-looking media directly. Consequently, generative steganography has flourished across various modalities, including text [11], [12], images [9], and audio [10]. Researchers leverage these models’ rich, high-dimensional probability distributions to construct covert channels with high capacity and minimal statistical detectability

TABLE I: The Capacity-Efficiency-Security trilemma in generative steganography. • denotes that the method achieves the optimal goal for the corresponding property, whereas ◦ indicates a sub-optimal solution. Our work, ANStega, is the first to resolve this trilemma.

<table><tr><td>Method</td><td>Optimal Capacity (Near Entropy Limit)</td><td>Optimal Efficiency (O(1) Complexity)</td><td>Optimal Security ( $D_{\text{KL}} \leq \epsilon$ )</td><td>Modality</td></tr><tr><td>Huffman-based [6], [7]</td><td>●*</td><td>○</td><td>○</td><td>Text †</td></tr><tr><td>AC-based [8]-[11]</td><td>●*</td><td>○</td><td>○</td><td>Text / Audio †</td></tr><tr><td>ADG [12]</td><td>○</td><td>○</td><td>○</td><td>Text †</td></tr><tr><td>Meteor [13]</td><td>○</td><td>○</td><td>●</td><td>Text †</td></tr><tr><td>Discop [14]</td><td>○</td><td>○</td><td>●</td><td>Text / Image / Audio †</td></tr><tr><td>iMEC [15]</td><td>○</td><td>○</td><td>●</td><td>Text / Image / Audio †</td></tr><tr><td>SA-ANS [16]</td><td>○</td><td>○</td><td>○</td><td>Text †</td></tr><tr><td>FDPSS [17]</td><td>○</td><td>○</td><td>●</td><td>Text †</td></tr><tr><td>Shimmer [18]</td><td>○</td><td>●</td><td>●</td><td>Text †</td></tr><tr><td>SparSamp [19]</td><td>○</td><td>●</td><td>●</td><td>Text / Image / Audio †</td></tr><tr><td colspan="5">Image-based Methods:</td></tr><tr><td>Pulsar [20]</td><td>○</td><td>○</td><td>●</td><td>Image</td></tr><tr><td>StegaDDPM [21]</td><td>○</td><td>●</td><td>●</td><td>Image</td></tr><tr><td>ANStega (Ours)</td><td>●</td><td>●</td><td>●</td><td>Text / Image †</td></tr></table>

<sup>\*</sup>These methods achieve near-optimal capacity by altering the model’s original probability distribution.  
<sup>†</sup>Note that the coding algorithms are theoretically modality-agnostic; the listed modalities reflect the specific implementations in the cited works.

Historically, generative steganography is encoding-driven, adapting long-standing entropy coding techniques to steganographic use. Anderson and Petitcolas [24] first highlighted a critical insight—the duality between steganography and inverse compression. Early generative approaches adapted classical entropy coders, predominantly Huffman Coding (HC) and Arithmetic Coding (AC), to navigate generative model distributions. HC-based methods [6], [7], despite their conceptual simplicity, suffer from frequent tree reconstruction overhead and unavoidable distribution modifications, resulting in suboptimal efficiency and compromised security. Conversely, AC-based methods [9]–[11] achieve near-optimal capacity but incur significant computational overhead due to probability scaling, and also introduce precision-induced distortions, weakening security. As illustrated in Fig. 1, entropy-codingbased steganography navigates the model distribution to “decompress” a secret bitstream into tokens, thereby aligning embedding with generative sampling.

Recognizing these limitations, subsequent research emphasized provable security, as seen in schemes like Meteor [13], Discop [14], and iMEC [15]. Although these schemes guarantee robust security, they often impose substantial penalties on embedding capacity and computational performance, limiting their practicality. Even recent methods such as SparSamp [19], which achieve optimal security and efficiency, exhibit only a slight shortfall in embedding capacity—despite effectively reaching the entropy limit—due to constraints inherent to sparse sampling. Beyond the modality-agnostic coding algorithms, generative steganography has also been explored in image generation using diffusion models, yet similar trade-offs persist. For example, StegaDDPM [21] achieves high operational efficiency by integrating embedding into the diffusion sampling steps, but its capacity is low. On the other hand, Pulsar [20] prioritizes cryptographic security and extraction, however, this comes at the cost of computational overhead and reduced effective embedding rates.

Despite this promising direction, generative steganography remains fundamentally constrained by the Capacity-Efficiency-Security Trilemma, illustrated in Table I. An optimal steganographic method should simultaneously achieve three goals: (1) Optimal Capacity, approaching the Shannon entropy limit with a vanishing gap (near-entropy embedding); (2) Optimal Efficiency, characterized by constanttime complexity O(1); and (3) Optimal Security, ensuring statistical indistinguishability between the stego-content and the cover-content. However, existing methods have invariably compromised at least one of these crucial attributes.

This fragmented landscape highlights the need for a fundamentally novel coding paradigm to comprehensively resolve the trilemma. In this context, we identify Asymmetric Numeral Systems (ANS), introduced by Duda [25], as an overlooked yet promising entropy coder. ANS uniquely combines the computational simplicity reminiscent of Huffman Coding with the high compression efficiency characteristic of Arithmetic Coding. Its robust industrial adoption by major technology firms, including Meta [26], Apple [27], Google [28], and Microsoft [29], underscores its practical strengths. While recent studies have begun to explore ANS for steganography [16], fully harnessing its potential to simultaneously achieve optimal capacity, constant-time efficiency, and provable security remains an open challenge.

We present ANStega, a strictly provably secure steganographic encoder built on the ANS framework. Unlike concurrent approaches that focus primarily on sampling strategies [16], we do not merely transplant ANS: a na¨ıve port fails to provide long-message support, constant-time embedding, or rigorous distributional security. We therefore introduce a set of steganography-specific modifications: streaming rANS with bounded state to embed arbitrarily long messages without numerical blow-up; direct probability updates without global rescaling (no convert/renormalize over the full vocabulary), preserving the model distribution while maintaining O(1) perstep work; a per-step MASK (CSPRNG-based) that enforces sampling randomness and independence, yielding distributional indistinguishability; and a reimplementation of core arithmetic in bitwise primitives, further improving embedding throughput. Together, these changes make ANS fit for steganography: ANStega attains near-entropy capacity with constant-time embedding and provable security, while remaining practical for high-throughput LLM generation.

ANStega uniquely solves the generative steganography trilemma, achieving simultaneous optimal performance across embedding capacity, security, and efficiency. We experimentally validate that ANStega approaches the theoretical entropy limit, matches AC-based methods in capacity, and significantly exceeds them in computational efficiency and statistical security. Our theoretical proofs and extensive empirical evaluations confirm that ANStega preserves model distributions and achieves O(1) complexity by eliminating the scaling overhead typical in AC-based schemes.

Our main contributions are as follows:

• We propose ANStega, a generative steganographic scheme based on Asymmetric Numeral Systems. Rather than directly adopting ANS, we systematically redesign it for steganographic encoding by reversing its encodingdecoding roles, aligning seamlessly with LLM-based token generation.

• We introduce a tailored streaming rANS approach, allowing the stable embedding of arbitrarily long messages by maintaining bounded state intervals. This strategy effectively eliminates numerical overflow issues inherent in traditional ANS implementations.

• To enhance efficiency, we devise a direct floating-point update strategy that avoids global probability rescaling, and further accelerate embedding through bitwise arithmetic transformations, resulting in a constant-time embedding complexity (O(1)).

• We ensure provable steganographic security by integrating a cryptographic masking mechanism (MASK), which guarantees uniform randomness during token sampling.

![](images/7248e8b787b83e4995a66afcb588b55a8781f51a8b4ad85855eab94b79a08836.jpg)  
Fig. 2: A concrete example of LLM-based Steganography.

We prove that ANStega preserves the original model distribution, achieving optimal security.

• Extensive empirical evaluations validate that ANStega achieves optimal embedding performance across capacity, efficiency, and security metrics, successfully resolving the long-standing generative steganography trilemma.

## II. BACKGROUND AND RELATED WORK

## A. Steganographic Model

Steganography enables two communicating parties to exchange secret messages over a public channel without an adversary detecting the existence of communication. A classic formalization of this scenario is Simmons’ “Prisoners’ Problem” [30], in which two prisoners, Alice and Bob, wish to plan an escape by exchanging seemingly innocuous messages. A prison warden inspects all messages carefully, rejecting any communication that appears suspicious. This scenario captures two fundamental requirements of steganography:

1) Correctness: Bob must reliably recover the hidden message M from the received stego medium S without errors.

2) Undetectability: The warden’s ability to distinguish the stego medium S from a legitimate cover medium C should be no better than random guessing.

Steganographic models generally fall into two principal paradigms: modification-based and generation-based.

In modification-based steganography, given a cover medium $C \in { \mathcal { C } } ,$ a secret message $M \in { \mathcal { M } }$ , and a secret key K, the embedding process produces a stego medium $S \in S$ by minimally altering the cover medium:

$$
S = \mathcal {E} (C, M, K),\tag{1}
$$

where K is shared secretly between Alice and Bob. The embedding process ensures S is visually or statistically indistinguishable from C to unauthorized observers.

In contrast, generation-based steganography directly synthesizes a stego medium from the secret message without relying on a pre-existing cover. Formally, this generation process is represented as:

$$
S = \mathcal {G} (M, K),\tag{2}
$$

where G denotes a generative function parameterized by the secret key K. The principal advantage of generative steganography lies in eliminating explicit modification artifacts, potentially complicating detection.

To facilitate a better understanding of the generation-based steganographic model, we introduce a concrete running example based on LLM steganography, as illustrated in Figure 2.

Consider a scenario where a sender wishes to conceal a secret message, $m = \ ' 1 0 \ '$ , within a generated text stream. The process operates as follows:

1) Context and Distribution: The LLM receives a prompt (e.g., “I want to eat”) and computes a probability distribution $\mathcal { P } _ { i }$ for the next token. In our example, the tokens “later” (11), “now” (10), and “here” (0) are assigned probabilities of 0.25, 0.25, and 0.5, respectively.

2) Embedding (Encoding): Rather than sampling the next token purely at random—which is standard in normal generation—the sender utilizes a steganographic algorithm to map the message bits m to a specific token. Here, the message ’10’ maps directly to the token “now”.

3) Output: The token “now” is selected and appended to the text, resulting in “I want to eat now”. To an outside observer, this selection appears to be a natural continuation of the sentence, statistically consistent with the distribution $\mathcal { P } _ { i }$

## B. Generative Steganography

Early theoretical work on steganography established provably secure techniques for “cover-free” channels, yet these methods remained largely impractical due to the inability to sample realistic media distributions [31]. The advent of high-quality generative models—LLMs for text, diffusion or GAN/flow models for images and audio—has fundamentally changed the landscape by enabling realistic, high-entropy content synthesis that supports covert message embedding with minimal detectability.

In text, early LSTM-based schemes such as Fang et al. [32] encoded bits by selecting tokens from fixed vocabulary bins, but suffered from detectability issues. RNN-Stega [33] improved capacity by using Huffman coding over conditional token probabilities, though the required tree reconstruction and distribution distortion limited security and efficiency. The introduction of Arithmetic Coding (AC) with LLMs (e.g. Ziegler et al. [11]) allowed near-entropy embedding, but AC’s rescaling operations introduce precision loss and runtime overhead.

Subsequent work aimed to establish provably secure schemes. Meteor [34] mitigated randomness-reuse risks in AC-based embedding via recoverable-range sampling, improving cryptographic security at the cost of added complexity. Adaptive Dynamic Grouping (ADG) [35] dynamically partitions the token space to align with the LLM distribution, enhancing imperceptibility. Distribution-copy methods such as Discop [14] and minimum-entropy coupling like iMEC [15] further preserve statistical indistinguishability by constructing exact distributional copies or couplings—but both incur significant runtime cost. More recently, SparSamp [19] achieved O(1) embedding and perfect security in practice, but still exhibits a minor capacity gap due to its sparse-sampling design. Very recently, concurrent work SA-ANS [16] has begun to explore ANS for linguistic steganography. However, SA-ANS relies on direct state-dependent sampling without cryptographic masking, leaving statistical artifacts detectable by analysis. Furthermore, it lacks optimal complexity and employs fixed-rate consumption that limits capacity on lowentropy distributions.

Generative steganography has also developed beyond text: PixelCNN-based approaches for images [9], audio steganography via TTS models [10], and diffusion-based frameworks [20], [21] have all explored embedding messages during generation. Collectively, these advances demonstrate modalitywide applicability of generative steganography in AIGC, covering encoding-based designs and alternative mechanisms alike.

Despite this rich body of work, no existing approach simultaneously achieves (i) near-entropy embedding rate, (ii) constant-time efficiency (O(1)), and (iii) provable distributional indistinguishability. In particular, while ANS—a coding paradigm with Huffman-like efficiency and AC-level compression effectiveness—has attracted recent attention [16], its potential to fundamentally resolve this trilemma remains unrealized. Our work fills that gap by systematically adapting ANS to the steganographic setting, enabling efficient, provably secure, and high-capacity generative steganography.

## C. Asymmetric Numeral Systems

Asymmetric Numeral Systems (ANS) is a family of entropy coders introduced by Duda that combines AC–like compression effectiveness with Huffman-like efficiency [36]. Two widely used ANS variants are table-based ANS (tANS) and range-based ANS (rANS). tANS precomputes state transitions in lookup tables so that runtime encoding/decoding primarily performs bit-shifts, additions, and table reads; rANS maintains a single integer state and updates it with integer multiply–add and div/mod operations analogous to range (arithmetic) coding. ANS has seen broad industrial adoption: Zstandard [26], [37] and Apple’s LZFSE [27] employ Finite State Entropy, and the JPEG XL standard [38] supports ANS as one of its entropy coders. For steganographic use with generative models, we favor rANS because the target token distribution changes at every step, making tANS lookup tables impractical to precompute or maintain.

The core idea of ANS is to represent a sequence of symbols as a single natural number, effectively capturing the entire message’s information content. This is achieved by maintaining a state variable x, which is updated as each symbol is processed. Let $f _ { s }$ denote the frequency of symbol s, $\begin{array} { r } { C _ { s } = \sum _ { a < s } f _ { a } } \end{array}$ its cumulative frequency, and $\begin{array} { r } { \dot { M } = \dot { \sum } _ { a \in \Sigma } f _ { a } } \end{array}$ the total frequency. Each symbol s is encoded via:

$$
x \leftarrow \left\lfloor \frac {x}{f _ {s}} \right\rfloor \cdot M + C _ {s} + (x \bmod f _ {s}),\tag{3}
$$

after all symbols have been processed, the final state x and any residual bits are written out as the compressed output. During decoding the process is reversed, successively recovering symbols while restoring earlier states—thereby reproducing the original message exactly.

The decoding in rANS proceeds by inverting the encoding transformation to recover the original message from the final state x. At each step, the current symbol s is identified by the residue:

$$
s \leftarrow \mathsf {s y m b o l} (x \bmod M),\tag{4}
$$

the state is then updated as

$$
x \leftarrow f _ {s} \cdot \left\lfloor \frac {x}{M} \right\rfloor + (x \bmod M) - C _ {s},\tag{5}
$$

this process iterates until all symbols are decoded in order.

## III. MOTIVATION

The relationship between entropy coding and steganographic encoding provides a useful duality for modern generative steganography. In classical information theory, entropy coders such as Huffman Coding and Arithmetic Coding compress data by removing statistical redundancy, transforming a symbol sequence into a bitstream that is close to uniform [39]. Anderson and Petitcolas [24] noted a consequence for steganography: if one has a (near-)perfect generative model of the cover distribution and an invertible coder, then the inverse mapping can “decompress” a random bitstream (e.g., encrypted data) into plausible samples from that distribution. Informally, steganographic embedding can be viewed as the inverse of entropy coding: instead of compressing symbols into bits, we map a secret bitstream into symbols that follow the model’s target distribution.

This perspective naturally motivated adapting classical coders for steganography. However, direct use of HC/AC exposes a persistent capacity–efficiency–security tension:

• AC-based methods can approach the entropy limit and thus offer high embedding capacity [8]–[11]. In practice, each token step requires range updates and renormalization under finite precision, plus converting model probabilities to scaled integers. Although amortized time per step is constant, these operations introduce nontrivial overhead and sensitivity to precision/rounding, which complicates accurate sampling of low-probability tokens and can affect security if randomness management is not careful.

• HC-based methods, while fast in static compression, lose that advantage here: the model distribution changes at every step, implying frequent tree rebuilds or reweighting. Moreover, HC requires dyadic probabilities; quantization to dyadic weights induces a systematic mismatch to the target distribution, yielding suboptimal capacity and measurable KL divergence [6], [7].

In this paper, we hypothesize that the unique properties of ANS provide the ideal foundation for resolving the steganographic trilemma. Its near-optimal compression ratio suggests the potential to achieve maximum capacity; its low-complexity points toward O(1) efficiency; and its precise, scale-free arithmetic offers a way to avoid the distributional distortions that plague other methods. Therefore, this paper is dedicated to investigating this hypothesis. We present the adaptation of ANS for generative steganography, describing the necessary innovations to harness its theoretical strengths.

## IV. THREAT MODEL

We analyze ANStega against a passive adversary (the warden, Eve) whose goal is steganographic detection. Eve observes the public channel between the sender (Alice) and the receiver (Bob) and seeks to distinguish stego text S (carries a hidden message) from cover text C (does not). This is a binary hypothesis test; Eve’s success is measured by any distinguishing advantage over random guessing.

a) Kerckhoffs-aligned capabilities: We adopt a strong, standard model in which security relies only on secret keys, not on algorithm secrecy.

• System knowledge. Eve knows the generative model G (architecture, parameters, and sampling hyperparameters such as temperature) and the complete ANStega algorithm and its implementation details.

• Channel access. Eve intercepts the full token sequence and the prompt/context Φ for every message sent over the public channel. She may perform arbitrary statistical tests or train detectors using in-distribution corpora, and she may query G (black-box sampling) to draw matched reference samples.

• No access to secrets. Eve does not know the shared key $k _ { \mathrm { s e e d } }$ used to derive the per-step MASK via a CSPRNG. Internal ANS states and MASK values are never revealed on the public channel.

b) Passive Adversary: We focus on a passive adversary model, which is the standard setting for linguistic steganography aiming for high capacity [6]–[19]. In this model, Eve monitors the public channel to detect anomalies but does not modify traffic. We defer the discussion of active adversaries—who may inject or alter tokens to disrupt synchronization—to Section VIII, noting that resistance to such attacks typically requires sacrificing the near-entropy capacity that ANStega aims to achieve.

## V. PROPOSED METHOD

## A. Overview of Steganography System Based on ANS

The foundational principle of our system lies in mapping the ANS framework to the generative steganography task. Instead of merely using ANS as a black-box compressor, we repurpose its core state machine for message embedding and extraction. The key correspondences are established as follows (and illustrated in Figure 3):

• ANS Symbol Sequence ↔ StegoText S: The sequence of symbols produced by the state machine constitutes the final steganographic text.

• ANS Alphabet ↔ Model Vocabulary V: The set of all possible symbols corresponds to the vocabulary of the generative model G.

• ANS Frequency Table ↔ Model Probability Distribution $P ( s \mid \cdot \rangle ) { \mathrm { : } }$ The symbol frequencies are determined at each step by the next-token probability distribution predicted by the generative model.

![](images/448cdaf4f1b131ee8ab82e3d0d73a059fc077e199d1ed4a7decf548c92801bdb.jpg)  
Fig. 3: Mapping the core components of ANS to the generative steganography task.

• ANS Bitstream ↔ Secret Message m: The secret message provides the bits that drive the state machine’s evolution.

The central innovation of our approach lies in inverting the conventional roles of the ANS state transition functions, $\mathcal { C } ( s , x )$ (encode) and ${ \mathcal { D } } ( x )$ (decode). This inverse design is intuitive for generative tasks:

• Standard ANS decoding takes a state $x _ { t + 1 }$ and produces a symbol $s _ { t } .$ . This is precisely the functionality required for generative steganography, where we need to generate a token (symbol) based on the current state, which is derived from the secret message.

• Conversely, standard ANS encoding consumes a sequence of symbols to produce a final state. This mirrors our message extraction process, which consumes the sequence of received tokens to reconstruct the state and thereby reveal the original secret message.

Therefore, we formally define our embedding function Encode as the ANS decoding function $\mathcal { D } ,$ , and our extraction function ${ \mathsf { D e c o d e } } _ { \mathcal { G } }$ as the ANS encoding function C:

Embedding :

$$
\begin{array}{l} (x _ {t}, s _ {t}) = \mathcal {D} (x _ {t + 1}) \\ x _ {t + 1} = \mathcal {C} (s _ {t}, x _ {t}) \end{array}
$$

Extraction :

(6)

A critical consequence of this “decode-first, encode-later” architecture is the need to synchronize the extractor’s initial state with the embedder’s final state. To correctly reconstruct the message, the extractor must begin its computation from the exact state value, $x _ { \mathrm { f i n a l } }$ , where the embedder finished.

## B. Construction of the ANStega System

The previous section established the theoretical framework for using an ANS state machine for generative steganography. However, a direct implementation faces a significant practical challenge: the state value x can grow indefinitely when processing a long message, leading to numerical overflow. This section details how we engineer ANStega, an efficient system that overcomes this limitation through a streaming architecture and targeted optimizations.

1) Addressing State Overflow with Streaming rANS: To solve the problem of unbounded state growth, we adapt our system to use Streaming rANS. This approach constrains the state value x to a fixed operational range $[ L , H ]$ , ensuring numerical stability. Whenever an operation causes x to fall outside this range, a renormalization step is performed by streaming bits in or out. We adopt the standard configuration where $L = \alpha \cdot M$ and $H = 2 L - 1$ , for a hyperparameter α and $M = 2 ^ { \mathrm { p r e c i s i o n } }$

This is accomplished by integrating two core operations, Expand and Shrink, into our steganographic functions:

• Expand (during Embedding): During the embedding process $( \mathsf { E n c o d e } _ { \mathcal { G } } )$ , a state update can cause x to become too small $( \mathrm { i } . \mathrm { e } . , \ x < L )$ . To renormalize it, the Expand operation repeatedly shifts in bits from the secret message m into the low-order bits of the state until x is back within the $[ L , H ]$ range. This is the primary mechanism by which the secret message is consumed.

• Shrink (during Extraction): In the extraction process $( \mathsf { D e c o d e } _ { \mathcal { G } } )$ , to ensure that the state variable x consistently remains within the predefined valid interval $I =$ $[ L , H ]$ after each update, we introduce a preprocessing operation named Shrink. This operation is performed before each state update with ExtractStep (Equation 3). Its purpose is to pre-adjust x to guarantee that the new state value after the update will fall within I. A direct implementation would be to use a loop that speculatively calls ExtractStep to check if the next state is valid, but this is inefficient due to the repeated, costly function calls. As we prove in Appendix A-A, this complex check is equivalent to a much more efficient condition that only involves the current state x: while $( x \ge 2 \alpha f _ { s } )$ . Therefore, the optimized Shrink loop simply uses this fast condition. In each iteration, it outputs the least significant bit (LSB) of x and then performs a right-shift, continuing until x is small enough.

While Streaming rANS ensures stability, we introduce two further optimizations to maximize the performance and precision of ANStega.

2) Avoiding Rescale for Higher Fidelity: Traditionally, using generative models with entropy coders requires converting the model’s floating-point probabilities into integer frequencies for a range [0, M]. This rescaling process is computationally expensive and, more importantly, introduces quantization errors that distort the original probability distribution. To eliminate this, we perform all arithmetic directly in the floating-point domain. This is achieved by normalizing the state value on the fly (i.e., using ${ \frac { x \ ( \mathrm { m o d } \ M ) } { M } } )$ and adapting the state update function 5 accordingly:

$$
\begin{array}{l} f _ {s} ^ {\text { scaled }} \leftarrow \lceil P _ {s} \cdot M \rceil , \quad C _ {s} ^ {\text { scaled }} \leftarrow \lceil C _ {s} \cdot M \rceil \\ x \leftarrow f _ {s} ^ {\text { scaled }} \cdot \left\lfloor \frac {x}{M} \right\rfloor + (x \bmod M) - C _ {s} ^ {\text { scaled }} \end{array}\tag{7}
$$

![](images/43cdbd33d65b9d4ef906ab7b59c05970fd756281699671b803dd91d4ec0bbe8d.jpg)  
Fig. 4: An example of ANStega encoding process.

This approach preserves the model’s distribution while also reducing computational overhead.

3) Securing Randomness with a Cryptographic Mask: Although the Avoiding Rescale optimisation preserves the language-model distribution exactly, the residue $r \quad = \quad$ (x mod M)/M is uniform only if the least-significant bits of the ANS state x are themselves unbiased. Increasing the normalisation factor α mitigates—but cannot eliminate—bias, and it provides no formal guarantee.

To obtain unconditional uniformity we transform ANStega into a symmetric-key scheme that injects cryptographic randomness at every generation step:

1) Shared seed. Sender and receiver agree on a secret key $k _ { \mathrm { s e e d } }$ and seed an identical cryptographically secure pseudo-random number generator (CSPRNG).

2) Mask Generation: At each step t, the CSPRNG generates a precision-bit pseudo-random value, which serves as a cryptographic mask, $R _ { t }$

3) State Scrambling: The sampling variable r is then computed by first applying this mask to the low-order bits of the state via a bitwise XOR operation:

$$
r \leftarrow \frac {(x \bmod M) \oplus R _ {t}}{M}\tag{8}
$$

where ⊕ denotes the bitwise XOR operation.

Because $R _ { t }$ is computationally indistinguishable from uniform, the resulting r is provably uniform regardless of any latent structure in x or the choice of α. Steganographic security therefore reduces to the secrecy of $k _ { \mathrm { s e e d } }$ and the strength of the underlying CSPRNG, elevating ANStega’s indistinguishability guarantee from heuristic to cryptographic.

4) Computational Simplification with Bitwise Operations: The rANS state update formulas rely heavily on integer division and modulo operations. These can be computationally intensive. By setting our range parameter M to be a power of two (i.e., $M = 2 ^ { \mathrm { p r e c i s i o n } } )$ , all division and modulo operations with respect to M can be replaced with highly efficient bitwise shift and AND operations. This optimization dramatically reduces the computational load, making ANStega exceptionally fast and well-suited for deployment on resource-constrained devices.

5) Algorithmic Implementation: The mechanisms described above are implemented as a set of core algorithms. The Expand and Shrink algorithms handle the state renormalization for the streaming protocol. As shown in Algorithm 1, Expand normalizes a state $x < L$ by consuming bits from the message queue m and appends them to the state’s least significant bits. Algorithm 2 preemptively adjusts the state x to ensure that the subsequent state, after performing one extraction step, remains within the interval I.

The core inverse operations are realized in Algorithm 3 and Algorithm 4. Figure 4 provides a detailed, step-by-step walkthrough of this embedding process, illustrating the state transitions and token generation. The Sample function, detailed in Algorithm 3, performs the embedding step: it uses the state x to generate a uniform random value r, samples a token s according to the model’s distribution P, and computes the new, smaller state using the rANS decoding formula. The EncodeStep function performs the inverse extraction step: it takes the received token s and current state x to compute the new, larger state using the rANS encoding formula, ensuring perfect reversibility.

Finally, Algorithms 5 and 6 orchestrate the entire process. The main embedding loop, Encode<sub>G</sub>, iteratively calls Sample to generate a token and Expand to renormalize the state. The main extraction loop, Decode<sub>G</sub>, processes tokens in reverse, calling EncodeStep to update the state and Shrink to renormalize and extract the hidden message bits.

```typescript
Algorithm 1: Expand(x, m): Expand state x by consuming message bits
Input: State x, Message Queue m
Output: Expanded State x
while x < L do
    b ← m.pop_front() // Get next bit from message
    x ← (x ≪ 1) | b // Append bit to LSB, increasing state value
end
return x
```

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2: Shrink(x, s, P): Shrink state x and extract message bits

Input: State x, Symbol s, Probability Distribution P
Output: Shrink State x, Extracted Bits bits
Initialization: bits ← ∅
 $f_{s}^{scaled} \leftarrow \lceil P_{s} \cdot M \rceil$ $x_{max} \leftarrow 2 \cdot t \cdot f_{s}^{scaled}$ 
while  $x \geq x_{max}$  do
    b ← x mod 2
    bits.prepend(b) // Extract LSB and
    prepend to bits list
    x ← x ≫ 1 // Shrink state
end
return x, bits
</div>

## VI. SECURITY ANALYSIS

## A. Security Definition

Unlike information-theoretic steganography which assumes perfect randomness [15], we analyze ANStega under the standard cryptographic model of computational indistinguishability. The security of our system relies on the inability of a polynomial-time adversary (Eve) to distinguish the distribution of the stego-text $P _ { S }$ from the cover-text distribution $P _ { \mathcal { G } }$ (the language model).

Let $\mathcal { G } ( \Phi , s _ { < t } )$ denote the true next-token distribution of the language model. Previous methods, such as those based on HC or AC, inherently modify this distribution to fit dyadic intervals or integer frequencies, resulting in a non-zero

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3: Sample(x, P): Sample token and update state (Embedding Step)

Input: State x, Probability Distribution P
Output: New State x, Sampled Token s
Initialization: C ← Cumulative(P)
r ← (x mod M)/M
s ← InverseTransformSample(C, r) // Find token s where  $C_{s-1} \leq r &lt; C_s$ 
// This is the rANS decoding formula adapted for direct float probabilities
 $x \leftarrow \lfloor x/M \rfloor \times \lceil P_s \cdot M \rceil + (x (\text{mod } M)) - \lceil C_s \cdot M \rceil$ 
return x, s
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4: ExtractStep(x, P, s): Update state with token (ANS Encoding function)

Input: State x, Distribution P, Token s
Output: New State x
Initialization: C ← Cumulative(P)
 $f_{s}^{scaled} \leftarrow \lceil P_{s} \cdot M \rceil$ $C_{s}^{scaled} \leftarrow \lceil C_{s} \cdot M \rceil$ $x \leftarrow \lfloor x / f_{s}^{scaled} \rfloor \cdot M + C_{s}^{scaled} + (x \mod f_{s}^{scaled})$ 
return x
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5: Encode$_{\mathcal{G}}$: Main Loop of the ANStega Embedding

Input: Message $m$, Context $\Phi$, Generative Model $\mathcal{G}$, Seed $k_{\text{seed}}$

Output: Stegotext $S$, Final State $x$

Initialization:
$M \leftarrow 2^{\text{precision}}$, $L \leftarrow M \times \alpha$, $H \leftarrow 2L - 1$, $S \leftarrow \emptyset$ $x \leftarrow \text{bits2int}(m[: \lceil \log_2(H) \rceil])$ // Initialize state with first bits of m

CSPRNG.Setup($k_{\text{seed}}$)

while generation is not finished do
    mask $\leftarrow$ CSPRNG.next()
    $x_{\text{mask}} \leftarrow x \oplus \text{mask} // \text{XOR the lower bits}$
    of x with mask
    $P \leftarrow \mathcal{G}(\Phi)$ $(x, s) \leftarrow \text{Sample}(x_{\text{mask}}, P)$ $x \leftarrow \text{Expand}(x, m)$ $S \leftarrow S \parallel s$ $\Phi \leftarrow \Phi \parallel s$

end

return $S$, $x$
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6: Decode$_{\mathcal{G}}$: Main Loop of the ANStega Extraction

Input: Stegotext S, Context $\Phi$, Model $\mathcal{G}$, Final State $x_{\text{final}}$, Seed $k_{\text{seed}}$

Output: Decoded Message m

Initialization:
$M \leftarrow 2^{\text{precision}}$, $L \leftarrow M \times \alpha$, $H \leftarrow 2L - 1$, $m \leftarrow \emptyset$,
$x \leftarrow x_{\text{final}}$

CSPRNG.setup($k_{\text{seed}}$), mask_list = []

for each token s in S do
    mask $\leftarrow$ CSPRNG.next()
    mask_list.append(mask)

end

for each token s in reverse(S) do
    // 1. Get distribution for the PREVIOUS step
    $\Phi_{\text{context}} \leftarrow$ prefix of S before s
    $P \leftarrow \mathcal{G}(\Phi_{\text{context}})$
    // 2. pre-adjust state and extract message bits
    (x, out_bits) $\leftarrow$ Shrink(x)
    // 3. Update state using the token (ANS encoding)
    $x \leftarrow$ ExtractStep(x, P, s)
    // 4. Recover state x via XOR the same mask
    mask $\leftarrow$ mask_list.pop_back()
    $x \leftarrow x \oplus$ mask
    $m \leftarrow$ out_bits || m

end

Finalization:
out_bits $\leftarrow$ to_binary(x)    // The final state contains the message's first bits
m $\leftarrow$ out_bits || m

return m
</div>

Kullback-Leibler (KL) divergence $( D _ { \mathrm { K L } } ( P _ { \mathcal { G } } | | P _ { S } ) > 0 )$ even with perfect randomness.

In contrast, ANStega is designed such that the intended sampling distribution is identical to $P _ { \mathcal { G } }$ . Ideally, assuming access to a True Random Number Generator (TRNG), the residue $r _ { t }$ used for sampling is perfectly uniform, implying $D _ { \mathrm { K L } } ( P _ { \mathcal { G } } | | P _ { S } ) ~ = ~ 0$ . However, in practice, we rely on a CSPRNG. Therefore, we define security via the advantage of an adversary A in the steganographic distinguishing game:

$$
\mathbf {A d v} _ {\mathcal {A}} ^ {\text { stega }} = | \operatorname * {P r} [ \mathcal {A} (S) = 1 ] - \operatorname * {P r} [ \mathcal {A} (C) = 1 ] |\tag{9}
$$

where S is the stego-text sequence and $C$ is a cover-text sequence sampled natively from the model. We claim that for any probabilistic polynomial-time (PPT) adversary A, $\mathbf { A d v } _ { \mathcal { A } } ^ { \mathrm { s t e g a } }$ is negligible, provided the underlying CSPRNG is secure.

## B. Computational Security Analysis

The security proof proceeds by reduction. We show that distinguishing the stego-text from the cover-text is computationally equivalent to distinguishing the CSPRNG output from a truly random sequence.

1. Ideal Randomness Case (Information-Theoretic Baseline): Consider an idealized version of ANStega, denoted as $\Pi _ { i d e a l }$ , where the mask $R _ { t }$ is drawn from a uniform distribution $\mathcal { U } \{ 0 , M - 1 \}$ where $M = 2 ^ { p r e c i s i o n }$

As defined in Eq. (9), the sampling variable is derived via $r ~ \left. ~ \left[ \left( x ~ \mathrm { ( m o d ~ } M \right) \right) \oplus R _ { t } \right] / M$ . Since $R _ { t }$ is perfectly uniform and independent of the state x, the One-Time Pad property ensures that the resulting bits (x mod $M ) \oplus R _ { t }$ are perfectly uniform over $\{ 0 , \ldots , M - 1 \}$ . Consequently, the normalized residue r is uniform on [0, 1). Because the Sample algorithm uses Inverse Transform Sampling on the exact model distribution $P _ { \mathcal { G } }$ driven by this uniform $r ,$ the sampled token $s _ { t }$ follows $P _ { \mathcal { G } }$ exactly. Thus, in the ideal case:

$$
P _ {S} ^ {\mathrm{ideal}} (s _ {t} \mid s _ {<   t}) \equiv P _ {\mathcal {G}} (s _ {t} \mid s _ {<   t}) \implies D _ {\mathrm{KL}} \left(P _ {\mathcal {G}} \| P _ {S} ^ {\mathrm{ideal}}\right) = 0\tag{10}
$$

2. Real-World Case (Pseudo-Randomness): In the actual ANStega protocol $\Pi _ { \mathrm { r e a l } } , R _ { t }$ is generated by a CSPRNG seeded with key $k _ { \mathrm { s e e d } }$ . If there exists a PPT adversary A that can distinguish $P _ { S }$ from $P _ { \mathcal { G } }$ with non-negligible advantage ϵ, we can construct a distinguisher B for the CSPRNG. B receives a sequence of masks and runs the ANStega sampling procedure. If the masks are true random, the output follows $P _ { \mathcal { G } }$ (as proven in Case 1); if they are pseudo-random, the output follows $P _ { S } .$ Therefore, A’s ability to distinguish the text implies $\boldsymbol { B ^ { \prime } s }$ ability to distinguish the CSPRNG output from random noise.

$$
\mathbf {A d v} _ {\mathcal {A}} ^ {\text { stega }} \leq \mathbf {A d v} _ {\mathcal {B}} ^ {\text { PRNG }}\tag{11}
$$

Since $\mathbf { A d v } _ { B } ^ { \mathrm { P R N G } }$ is negligible for a secure CSPRNG, the resulting distribution $P _ { S }$ is computationally indistinguishable from $P _ { \mathcal { G } }$

## VII. EXPERIMENT

In this section, we empirically evaluate ANStega to address three key questions: (1) How does ANStega fundamentally perform against other entropy coding-based methods and what is the impact of hyperparameters? (2) How robust is its security under theoretical analysis and steganalysis? (3) How do its capacity and efficiency compare with the leading methods? By systematically addressing these questions, we aim to provide a holistic assessment of the superiority of ANStega as a wellbalanced steganographic solution.

## A. Experimental Setup

1) Models and Dataset: We evaluate ANStega on six representative generative models—GPT-2 (124M) [40], Llama 3 (8B) [41], Qwen2.5 (3B) [42], DeepSeek-R1-Distilled-Qwen (1.5B), SmolLm2(135M) [43] and Phi-2(2.7B) [44], using the IMDB [45] movie review dataset. The task involves contextual text completion, where 100 text samples are randomly selected, and the first three sentences of each are used as input context.

2) Baselines and Parameters: To ensure fair comparison, we adopt standardized settings across all methods. Two sampling strategies are used: top-k sampling [46], which selects from the k most probable tokens, and nucleus (top-p) sampling [47], which samples from the smallest set of tokens with cumulative probability above $p .$ For precision-sensitive baselines like AC [11], we use 32-bit precision $( \beta ~ = ~ 3 2 )$ while methods like iMEC [15], SparSamp [19] and SA-ANS [16] retain their standard configurations (block sizes of 10, 64 and 16, respectively).

3) Implementation Details: All experiments are conducted on a high-performance computing platform equipped with an Intel Xeon Gold 6330 CPU and an NVIDIA RTX 4090 GPU. The implementation is developed using PyTorch 2.0 with CUDA 11.8 to ensure efficient and reproducible results.

## B. Evaluation Metrics

To comprehensively assess ANStega and other baseline steganographic methods, we evaluate their performance on three key dimensions: capacity, efficiency, and security.

1) Capacity: We evaluate embedding capacity using two metrics. The Embedding Rate (ER) measures the average number of secret bits embedded per generated token:

$$
\mathrm{ER} = \frac {\text {   Encoded   bits   }}{\text {   Generated   tokens   }}\tag{12}
$$

The Utilized Entropy Rate (UR) normalizes capacity by comparing actual embedding to the model’s theoretical limit:

$$
\mathrm{UR} = \frac {\sum_ {t = 1} ^ {T} C _ {t}}{\sum_ {t = 1} ^ {T} E _ {t}}\tag{13}
$$

where $C _ { t }$ is the number of bits embedded at time step t, and $E _ { t }$ is the model’s Shannon entropy. Higher ER and UR indicate greater embedding capacity.

2) Efficiency: We assess computational efficiency through both throughput and overhead. Specifically, we use Embedding Speed (ES) and Generation Speed (GS) to measure bits and tokens processed per second:

$$
\mathrm{ES} = \frac {\text {   Encoded   bits   }}{\text {   Encoding   time   }}, \quad \mathrm{GS} = \frac {\text {   Generated   tokens   }}{\text {   Encoding   time   }}\tag{14}
$$

To quantify algorithmic overhead, we introduce the Samplingto-Inference Time Ratio (SITR), which captures the relative cost of steganographic sampling:

$$
\mathrm{SITR} = \frac {\text {Sampling time}}{\text {Inference time}}\tag{15}
$$

An efficient method should achieve high ES/GS and low SITR.

3) Security: We evaluate security from three complementary perspectives: randomness quality, statistical fidelity, and practical undetectability.

Since our method’s security relies on the indistinguishability of the cryptographic mask from uniform noise, we employ the NIST Statistical Test Suite (STS). We evaluate the bitstreams derived from the per-step sampling variates against this industry-standard battery of tests. Passing these tests confirms that the CSPRNG-driven sampling introduces no statistically detectable bias compared to a true random source.

TABLE II: Impact of α and the cryptographic mask on ANStega’s performance (Llama3, Top-p, $p = 1 . 0 ) $ .

<table><tr><td>α</td><td>Mask</td><td>ER(bits/token)</td><td>UR</td><td>ES(bits/s)</td><td>GS(tokens/s)</td><td>SITR</td></tr><tr><td rowspan="2">1</td><td>w/o</td><td>2.03</td><td>0.86</td><td>72.60</td><td>35.63</td><td>1.26E-02</td></tr><tr><td>w/</td><td>2.63</td><td>1.00</td><td>92.11</td><td>34.92</td><td>1.49E-02</td></tr><tr><td rowspan="2">4</td><td>w/o</td><td>2.44</td><td>0.97</td><td>87.92</td><td>35.94</td><td>1.26E-02</td></tr><tr><td>w/</td><td>2.54</td><td>0.99</td><td>88.44</td><td>34.79</td><td>1.46E-02</td></tr><tr><td rowspan="2">16</td><td>w/o</td><td>2.37</td><td>0.97</td><td>85.70</td><td>36.03</td><td>1.27E-02</td></tr><tr><td>w/</td><td>2.48</td><td>0.98</td><td>86.52</td><td>34.83</td><td>1.47E-02</td></tr><tr><td rowspan="2">64</td><td>w/o</td><td>2.65</td><td>1.02</td><td>95.22</td><td>35.87</td><td>1.28E-02</td></tr><tr><td>w/</td><td>2.70</td><td>1.01</td><td>94.38</td><td>34.84</td><td>1.46E-02</td></tr></table>

Standard steganographic methods often alter the generative distribution to embed information (e.g., via probability quantization or space partitioning). To quantify this inherent statistical distortion, we compute the algorithmic Kullback-Leibler (KL) divergence between the model’s original nexttoken probability distribution and the steganographic sampling distribution at each time step.

To assess real-world detectability, we measure steganalysis accuracy (Acc) by training classifiers to distinguish stego-text from cover-text:

$$
\mathrm{Acc} = \frac {\text { Correct   predictions }}{\text { Total   predictions }}\tag{16}
$$

An accuracy near 50% indicates strong resistance to detection.

## C. Hyperparameter Analysis of ANStega

To thoroughly evaluate the performance and security of ANStega and to determine its optimal configuration for subsequent experiments, we conduct an in-depth analysis of two key hyperparameters: the scale factor α and the cryptographic mask. The scale factor α defines the normalization range [L, H] (where $L \ = \ \alpha \cdot M )$ and thus directly impacts the frequency and efficiency of state updates. The mask is a CSPRNG-derived perturbation on the low-order state used to drive sampling randomness.

Our analysis targets two questions: (1) how α and the mask affect efficiency and capacity; and (2) how they affect the statistical randomness of the per-step sampling—which directly impacts security.

1) Capacity and Efficiency: We first measure capacity and efficiency under varying α and with/without the mask, using Llama 3 with Top-p sampling $( p = 1 . 0 )$ . The results (Table II) lead to following observations. Without the mask, ANStega attains near-entropy capacity only at larger α (e.g., UR = 0.90 at α = 1 vs. UR = 1.00 at α = 64), indicating that small normalization ranges distort the per-step sampling bits and depress capacity. With the mask enabled, capacity becomes essentially α-insensitive: ER and UR remain at the nearentropy frontier across settings (e.g., $\mathrm { U R } \approx 0 . 9 9 \mathrm { - } 1 . 0 1$ for $\alpha \in \{ 1 , 4 , 1 6 , 6 4 \} ;$ . Importantly, increasing α or enabling the mask does not introduce a computational burden: ES/GS and SITR stay nearly constant across all configurations.

TABLE III: NIST STS results on per-step sampling. (✓: pass, ✗: fail)

<table><tr><td>Test</td><td>Random/Vanilla</td><td colspan="4">ANStega</td></tr><tr><td>Mask</td><td>-</td><td colspan="3">w/o</td><td>w/</td></tr><tr><td> $\alpha$ </td><td>-</td><td>1</td><td>16</td><td>32</td><td>1–32</td></tr><tr><td>ApproximateEntropy</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>BlockFrequency</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>CumulativeSums</td><td>✓</td><td>✘</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>FFT</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>Frequency</td><td>✓</td><td>✘</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>LinearComplexity</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>LongestRun</td><td>✓</td><td>✘</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>NonOverlappingTemplate</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>OverlappingTemplate</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>Rank</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Runs</td><td>✓</td><td>✘</td><td>✓</td><td>✓</td><td>✓</td></tr><tr><td>Serial</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr><tr><td>Universal</td><td>✓</td><td>✘</td><td>✘</td><td>✘</td><td>✓</td></tr></table>

2) Security Analysis (NIST Statistical Randomness Test): We evaluated the per-step sampling randomness using the NIST STS battery on one million bits generated from a static distribution $\{ 0 . 1 , 0 . 2 , 0 . 3 , 0 . 4 \}$ . Table III highlights a critical distinction: the unmasked ANStega is sensitive to α, with lower values leading to increased test failures due to residual state structure. Conversely, the masked ANStega is robust to α variations, passing the full NIST suite across all configurations. These results mirror the random baseline, empirically confirming that the CSPRNG mask is essential for ensuring the generated variability is statistically indistinguishable from standard sampling.

Because security with mask is essentially α-insensitive while efficiency has already plateaued at small $\alpha ,$ we fix $\alpha = 4$ and enable the mask for all subsequent experiments.

## D. Performance Comparison against Traditional Coding Approaches

Tables IV and V contrast the four entropy coding-based steganographic methods on Llama 3 with top-k sampling.

The Huffman-based method suffers from significant computational overhead due to the frequent tree reconstruction required for the large vocabulary of Llama 3. Consequently, its embedding speed starts high (47.82 bits/s at $k = 8 )$ and collapses further to 6.93 bits/s at $k \ = \ 1 0 2 4$ as shown in Table IV. Although its entropy-utilization rate (UR) exceeds 1 due to forcing token probabilities onto dyadic weights, this approximation severely distorts the model distribution. As shown in Table V, the average / max KL divergence reaches $0 . 7 2 / 1 0 . 6 0$ at $k = 8 ,$ , signaling a clear statistical fingerprint. The AC-based method better balances capacity and speed: UR remains near entropy $( 0 . 9 8 \ \sim \ 1 . 0 2 )$ and ES increases with k. However, rescaling the range per-step still introduces algorithmic distortion, with KL divergence remaining in the $1 \bar { 0 } ^ { - 2 } \sim 1 0 ^ { - 4 }$ range. The concurrent work SA-ANS [16] adopts the ANS framework to improve capacity, achieving significantly lower KL divergence $( \sim 1 0 ^ { - 6 } )$ than AC. However, it still incurs noticeable sampling overhead $( \mathrm { S I T R } \approx 0 . 0 8 )$ due to its state adjustment mechanism, and its embedding capacity is slightly suboptimal at lower k values (e.g., $\mathrm { U R } = 0 . 8 9$ at $k { = } 8 )$

ANStega effectively overcomes these limitations. It achieves near-perfect entropy utilization $( \mathrm { U R } \approx 1 . 0 1 )$ across all settings, avoiding the dyadic approximation artifacts found in Huffman coding. Crucially, as detailed in Table V, ANStega yields zero algorithmic KL divergence because the probability distribution is not rescaled or quantized prior to sampling—surpassing both AC and SA-ANS in statistical fidelity. Leveraging constant-time rANS updates and bitwise optimizations, ANStega matches the high throughput of AC and SA-ANS while incurring the lowest sampling overhead (consistent $\mathrm { S I T R } = 0 . 0 1 )$ . This represents an 8× reduction in overhead compared to SA-ANS, securing optimal efficiency alongside provable security.

E. Comparative Analysis with Other Secure Steganographic Methods

To demonstrate that ANStega successfully solves the trilemma, we benchmarked its performance against a range of state-of-the-art, secure steganography methods. The evaluation focuses on the critical dimensions of embedding capacity and computational efficiency, where previous methods have been forced to make significant compromises. The cross-model comparison is presented in Table VI, while a detailed analysis of sampling hyperparameters (p) on Llama 3 is provided in Table VII.

The results clearly demonstrate the superiority of ANStega in terms of embedding capability. As an entropy-based encoding method, ANStega achieves nearly perfect entropy utilization $( \mathrm { U R } \approx 1 . 0 ) $ across all tested models and sampling configurations. This allows ANStega to attain a significantly higher embedding rate (ER) than competitors. For instance, on Llama 3 with $p = 1 . 0 0$ , ANStega’s ER of 1.93 bits/token is substantially higher than that of SparSamp (1.77), Meteorreorder (1.42), and iMEC (1.35). This high-capacity performance is robust across different model architectures (Table VI) and scalable with the entropy of the sampling space.

In terms of computational efficiency, ANStega demonstrates a decisive advantage. Its $O ( 1 )$ complexity translates to extremely high embedding speed (ES) and a minimal sampling-to-inference time ratio (SITR). As seen in Table VI, under the rigorous setting of $p = 1 . 0$ , ANStega’s throughput consistently surpasses all other methods. While SparSamp [19] also exhibits excellent O(1) efficiency with a low SITR, ANStega is unique in achieving this top-tier speed without sacrificing capacity. In stark contrast, methods like iMEC [15] and Meteor [13] incur a devastating computational cost on larger models or full sampling distributions, with SITR values orders of magnitude higher (e.g., SITR > 600 for iMEC on GPT-2), rendering them impractical for real-time applications. Thus, ANStega uniquely occupies the optimal position in the landscape of secure steganography.

TABLE IV: Capacity and efficiency comparison of entropy coding-based steganography on Llama 3.

<table><tr><td rowspan="2">Top-k</td><td colspan="4">ES (bits/s)</td><td colspan="4">UR</td><td colspan="4">SITR</td></tr><tr><td>Huffman</td><td>AC</td><td>SA-ANS $^{\dagger}$ [16]</td><td>ANStega</td><td>Huffman</td><td>AC</td><td>SA-ANS</td><td>ANStega</td><td>Huffman</td><td>AC</td><td>SA-ANS</td><td>ANStega</td></tr><tr><td>8</td><td>47.82</td><td>46.83</td><td>48.66</td><td>50.39</td><td>1.48</td><td>0.99</td><td>0.89</td><td>1.01</td><td>0.07</td><td>0.03</td><td>0.08</td><td>0.01</td></tr><tr><td>32</td><td>53.61</td><td>62.75</td><td>61.62</td><td>63.45</td><td>1.36</td><td>1.00</td><td>0.93</td><td>1.01</td><td>0.26</td><td>0.03</td><td>0.08</td><td>0.01</td></tr><tr><td>128</td><td>35.79</td><td>70.72</td><td>71.87</td><td>71.57</td><td>1.30</td><td>0.98</td><td>0.97</td><td>1.01</td><td>1.26</td><td>0.03</td><td>0.08</td><td>0.01</td></tr><tr><td>512</td><td>11.82</td><td>75.31</td><td>81.93</td><td>83.01</td><td>1.26</td><td>1.00</td><td>0.99</td><td>1.01</td><td>5.40</td><td>0.04</td><td>0.08</td><td>0.01</td></tr><tr><td>1024</td><td>6.93</td><td>84.62</td><td>81.61</td><td>86.43</td><td>1.25</td><td>1.02</td><td>0.99</td><td>1.02</td><td>13.91</td><td>0.04</td><td>0.08</td><td>0.01</td></tr></table>

<sup>†</sup> For SA-ANS, we calculate the effective embedding rate (per-token throughput) based on actual consumed bits rather than the theoretical parameter.

TABLE V: Comparison of algorithmic KL divergence (Ave / Max) across methods on Llama 3.

<table><tr><td>Top- $k$ </td><td>8</td><td>128</td><td>1024</td></tr><tr><td>Huffman</td><td>7.23E-01 / 10.60</td><td>5.60E-01 / 7.99</td><td>5.47E-01 / 8.60</td></tr><tr><td>AC</td><td>7.92E-02 / 2.41</td><td>9.44E-04 / 0.07</td><td>2.86E-05 / 0.003</td></tr><tr><td>SA-ANS</td><td>1.72E-06/8.68E-05</td><td>2.07E-06/9.46E-05</td><td>3.05E-06/1.08E-04</td></tr><tr><td>ANStega</td><td> $\mathbf{0} / \mathbf{0}$ </td><td> $\mathbf{0} / \mathbf{0}$ </td><td> $\mathbf{0} / \mathbf{0}$ </td></tr></table>

## F. Resistance to Steganalysis

To complement our theoretical security guaranties, we conducted empirical steganalysis experiments to assess ANStega’s practical undetectability. We constructed a balanced dataset of 20,000 samples generated under identical nucleus sampling settings $( p = 0 . 9 5 )$ . Specifically, we generated 10,000 benign cover texts using the base model and 10,000 corresponding stego texts using ANStega. The dataset was partitioned into an 80/20 train-test split. On this data, we trained and evaluated four widely-used steganalysis architectures: a Fully Connected Network (FCN) [48], a Convolutional Neural Network (CNN) [49], and two specialized Bi-LSTM with a classification layer R-BiLSTM-C [50] and BiLSTM-Dense [51].

The results, presented in Table VIII, demonstrate ANStega’s security. All four classifiers performed at a statistically equivalent level to random guessing, with accuracies hovering around the 50% mark. This indicates that even sophisticated, deep learning-based detectors were unable to find any reliable statistical artifacts in the stego-text generated by ANStega. These empirical findings provide strong practical evidence for our theoretical claim that ANStega-generated content is indistinguishable from model output.

## G. Qualitative Analysis and Cross-Modal Application

In addition to quantitative metrics, it is crucial to assess the qualitative nature of the generated stego-media. To this end, we present examples that demonstrate both the fluency of ANStega’s text outputs and its versatility for application in other modalities.

Table IX presents several text continuations generated by ANStega using the Llama 3 model. The examples confirm that the stego-text maintains high semantic coherence with the provided context and exhibits a natural, fluent style, rendering it qualitatively indistinguishable from benign model outputs.

To showcase ANStega’s flexibility, we also applied it to image generation. Following the integration methodology of Wang et al. [19], we embedded ANStega into the final sampling step of a Denoising Diffusion Probabilistic Model (DDPM) [52] pre-trained on the FFHQ dataset. As illustrated in Figure 5, the resulting 256 × 256 stego-images are highfidelity and visually coherent, demonstrating that the core principles of ANStega can be effectively adapted to different generative processes and data modalities.

## VIII. DISCUSSION AND LIMITATIONS

While ANStega achieves optimal capacity, efficiency, and provable security, we acknowledge limitations inherent to high-capacity steganography.

Robustness vs. Capacity. ANStega is fragile against active attacks (e.g., token insertion or reordering); unlike robust watermarking, it requires the stego-text to be received exactly as generated. However, this fragility is a necessary trade-off for bandwidth, allowing ANStega to achieve embedding rates over 200× higher than robust schemes [53]. It is best suited for reliable channels rather than copyright protection.

Passive Threat Model. We assume a passive adversary who monitors but does not modify traffic. While active interference can disrupt the channel, widespread traffic alteration imposes high operational costs on wardens. Consequently, the passive model remains the standard assumption for high-bandwidth covert communication.

Deployment Requirements. Successful decoding demands strict synchronization of models and sampling parameters; even minor floating-point non-determinism across hardware can cause errors. Standardization is required to mitigate these precision issues [5]. Additionally, as a symmetric system, ANStega requires secure initial seed exchange, though subsequent keys can be rotated via message embedding to minimize overhead.

## IX. CONCLUSION

In this work, we addressed the long-standing Capacity-Efficiency-Security Trilemma that has constrained the field of generative steganography. We identified the root of this problem in the inherent limitations of adapting classical entropy coders like Huffman and Arithmetic Coding. To break this impasse, we introduced ANStega, a steganographic system built upon the powerful paradigm of ANS.

Our main contribution lies not only in the application of ANS, but also in the systematic reconstruction of its core mechanisms to meet the unique requirements of steganography. Through innovative reverse application of state machines, customized streaming architecture, and key cryptographic masking mechanisms, we have designed a system that successfully balances the three competing goals. Our extensive theoretical analysis and empirical evaluation demonstrate that ANStega is the first method to simultaneously achieve the following three objectives: (1) near-optimal embedding capacity, (2) constant-time O(1) computational efficiency, and (3) provable security. Beyond raw metrics, ANStega preserves the stylistic fidelity of natural text and yields visually coherent diffusion images, demonstrating its applicability across modalities. These results position ANStega provides both a practical, high-performance tool for secure communication and a new, powerful paradigm for steganographic research. We hope that our work will provide valuable insights for the next generation of secure, efficient, and high-capacity covert communication systems.

TABLE VI: Capacity and efficiency comparison on different models (Top-p, p = 1.0).

<table><tr><td rowspan="2">Metrics</td><td rowspan="2">Models</td><td rowspan="2">ADG [12]</td><td rowspan="2">iMEC [15]</td><td colspan="2">Meteor [13]</td><td colspan="2">Discop [14]</td><td rowspan="2">SparSamp [19]</td><td rowspan="2">ANStega</td></tr><tr><td>base</td><td>reorder</td><td>base</td><td>huffman</td></tr><tr><td rowspan="6">ER(bits/token)</td><td>GPT-2</td><td>5.25</td><td>4.53</td><td>4.67</td><td>5.73</td><td>2.40</td><td>5.78</td><td>5.67</td><td>5.95</td></tr><tr><td>Qwen2.5</td><td>2.80</td><td>2.88</td><td>2.67</td><td>3.67</td><td>1.53</td><td>3.73</td><td>3.48</td><td>3.69</td></tr><tr><td>Llama 3</td><td>1.63</td><td>0.70</td><td>1.62</td><td>1.67</td><td>1.06</td><td>2.19</td><td>2.37</td><td>2.56</td></tr><tr><td>DeepSeek</td><td>2.57</td><td>2.33</td><td>2.57</td><td>3.20</td><td>1.48</td><td>3.41</td><td>3.50</td><td>3.59</td></tr><tr><td>SmolLm2</td><td>4.43</td><td>3.46</td><td>2.01</td><td>4.42</td><td>4.10</td><td>5.12</td><td>5.12</td><td>5.50</td></tr><tr><td>Phi-2</td><td>3.56</td><td>2.57</td><td>1.76</td><td>3.99</td><td>3.30</td><td>4.40</td><td>4.32</td><td>4.67</td></tr><tr><td rowspan="6">UR</td><td>GPT-2</td><td>0.85</td><td>0.70</td><td>0.77</td><td>0.89</td><td>0.38</td><td>0.95</td><td>0.93</td><td>1.00</td></tr><tr><td>Qwen2.5</td><td>0.73</td><td>0.68</td><td>0.70</td><td>0.83</td><td>0.40</td><td>0.93</td><td>0.97</td><td>1.01</td></tr><tr><td>Llama 3</td><td>0.63</td><td>0.73</td><td>0.66</td><td>0.72</td><td>0.42</td><td>0.90</td><td>0.97</td><td>1.00</td></tr><tr><td>DeepSeek</td><td>0.69</td><td>0.73</td><td>0.70</td><td>0.83</td><td>0.39</td><td>0.92</td><td>0.96</td><td>0.99</td></tr><tr><td>SmolLm2</td><td>0.81</td><td>0.68</td><td>0.38</td><td>0.84</td><td>0.75</td><td>0.94</td><td>0.94</td><td>1.01</td></tr><tr><td>Phi-2</td><td>0.76</td><td>0.68</td><td>0.38</td><td>0.86</td><td>0.73</td><td>0.95</td><td>0.93</td><td>1.01</td></tr><tr><td rowspan="6">ES(bits/s)</td><td>GPT-2</td><td>7.82</td><td>0.91</td><td>636.57</td><td>0.84</td><td>155.79</td><td>22.42</td><td>821.56</td><td>879.79</td></tr><tr><td>Qwen2.5</td><td>3.46</td><td>0.05</td><td>95.74</td><td>0.5</td><td>29.94</td><td>4.76</td><td>127.18</td><td>136.82</td></tr><tr><td>Llama 3</td><td>1.61</td><td>0.02</td><td>57.10</td><td>0.41</td><td>22.35</td><td>3.31</td><td>84.28</td><td>94.67</td></tr><tr><td>DeepSeek</td><td>1.82</td><td>0.04</td><td>115.88</td><td>0.31</td><td>32.97</td><td>4.62</td><td>157.14</td><td>169.51</td></tr><tr><td>SmolLm2</td><td>6.61</td><td>0.50</td><td>51.32</td><td>0.60</td><td>137.10</td><td>15.77</td><td>187.82</td><td>212.31</td></tr><tr><td>Phi-2</td><td>7.30</td><td>0.35</td><td>48.07</td><td>0.83</td><td>128.59</td><td>13.06</td><td>173.12</td><td>186.81</td></tr><tr><td rowspan="6">GS(tokens/s)</td><td>GPT-2</td><td>1.49</td><td>0.20</td><td>136.45</td><td>0.15</td><td>65.01</td><td>3.88</td><td>144.69</td><td>147.76</td></tr><tr><td>Qwen2.5</td><td>1.24</td><td>0.02</td><td>35.65</td><td>0.14</td><td>19.60</td><td>1.28</td><td>36.52</td><td>37.05</td></tr><tr><td>Llama 3</td><td>0.98</td><td>0.03</td><td>35.16</td><td>0.25</td><td>21.02</td><td>1.51</td><td>35.53</td><td>36.91</td></tr><tr><td>DeepSeek</td><td>0.71</td><td>0.02</td><td>45.09</td><td>0.10</td><td>22.29</td><td>1.32</td><td>46.06</td><td>47.17</td></tr><tr><td>SmolLm2</td><td>1.48</td><td>0.14</td><td>25.47</td><td>0.13</td><td>33.39</td><td>3.07</td><td>36.62</td><td>38.56</td></tr><tr><td>Phi-2</td><td>2.04</td><td>0.13</td><td>27.28</td><td>0.20</td><td>38.94</td><td>2.96</td><td>40.01</td><td>39.98</td></tr><tr><td rowspan="6">SITR</td><td>GPT-2</td><td>93.75</td><td>640.56</td><td>0.11</td><td>730.36</td><td>1.16</td><td>30.81</td><td>0.03</td><td>0.04</td></tr><tr><td>Qwen2.5</td><td>28.02</td><td>1891.82</td><td>0.03</td><td>245.61</td><td>0.77</td><td>24.67</td><td>0.01</td><td>0.01</td></tr><tr><td>Llama 3</td><td>35.51</td><td>1151.72</td><td>0.03</td><td>129.53</td><td>0.65</td><td>20.86</td><td>0.01</td><td>0.01</td></tr><tr><td>DeepSeek</td><td>59.77</td><td>1774.04</td><td>0.03</td><td>424.71</td><td>0.97</td><td>29.52</td><td>0.01</td><td>0.01</td></tr><tr><td>SmolLm2</td><td>22.77</td><td>187.50</td><td>0.33</td><td>162.29</td><td>0.03</td><td>10.27</td><td>0.01</td><td>0.01</td></tr><tr><td>Phi-2</td><td>18.07</td><td>261.24</td><td>0.40</td><td>182.69</td><td>0.03</td><td>11.94</td><td>0.01</td><td>0.01</td></tr></table>

TABLE VII: Capacity and efficiency comparison on Llama 3 (Top-p).

<table><tr><td rowspan="2">Metrics</td><td rowspan="2">p</td><td rowspan="2">ADG [12]</td><td rowspan="2">iMEC [15]</td><td colspan="2">Meteor [13]</td><td colspan="2">Discop [14]</td><td rowspan="2">SparSamp [19]</td><td rowspan="2">ANStega</td></tr><tr><td>base</td><td>reorder</td><td>base</td><td>huffman</td></tr><tr><td rowspan="3">ER(bits/token)</td><td>0.80</td><td>0.64</td><td>0.85</td><td>0.66</td><td>0.73</td><td>0.72</td><td>1.01</td><td>0.90</td><td>1.20</td></tr><tr><td>0.95</td><td>1.14</td><td>1.35</td><td>1.22</td><td>1.42</td><td>0.95</td><td>1.69</td><td>1.77</td><td>1.93</td></tr><tr><td>1.00</td><td>1.63</td><td>0.70</td><td>1.62</td><td>1.67</td><td>1.06</td><td>2.19</td><td>2.37</td><td>2.56</td></tr><tr><td rowspan="3">UR</td><td>0.80</td><td>0.52</td><td>0.86</td><td>0.55</td><td>0.61</td><td>0.58</td><td>0.85</td><td>0.99</td><td>1.00</td></tr><tr><td>0.95</td><td>0.60</td><td>0.79</td><td>0.64</td><td>0.73</td><td>0.48</td><td>0.87</td><td>0.99</td><td>1.01</td></tr><tr><td>1.00</td><td>0.63</td><td>0.73</td><td>0.66</td><td>0.72</td><td>0.42</td><td>0.90</td><td>0.97</td><td>1.00</td></tr><tr><td rowspan="3">ES(bits/s)</td><td>0.80</td><td>21.45</td><td>26.31</td><td>22.00</td><td>23.47</td><td>23.90</td><td>34.53</td><td>30.17</td><td>43.98</td></tr><tr><td>0.95</td><td>37.51</td><td>39.42</td><td>40.37</td><td>33.18</td><td>31.36</td><td>55.00</td><td>59.20</td><td>64.21</td></tr><tr><td>1.00</td><td>1.61</td><td>0.02</td><td>57.10</td><td>0.41</td><td>22.35</td><td>3.31</td><td>84.28</td><td>94.67</td></tr><tr><td rowspan="3">GS(tokens/s)</td><td>0.80</td><td>33.43</td><td>31.10</td><td>33.09</td><td>32.16</td><td>33.07</td><td>34.15</td><td>33.21</td><td>33.92</td></tr><tr><td>0.95</td><td>32.95</td><td>29.19</td><td>33.06</td><td>23.32</td><td>32.94</td><td>32.62</td><td>33.29</td><td>33.31</td></tr><tr><td>1.00</td><td>0.98</td><td>0.03</td><td>35.16</td><td>0.25</td><td>21.02</td><td>1.51</td><td>35.53</td><td>36.91</td></tr><tr><td rowspan="3">SITR</td><td>0.80</td><td>0.01</td><td>0.08</td><td>0.02</td><td>0.05</td><td>0.02</td><td>0.01</td><td>0.01</td><td>0.01</td></tr><tr><td>0.95</td><td>0.02</td><td>0.15</td><td>0.02</td><td>0.46</td><td>0.02</td><td>0.02</td><td>0.01</td><td>0.01</td></tr><tr><td>1.00</td><td>35.51</td><td>1151.72</td><td>0.03</td><td>129.53</td><td>0.65</td><td>20.86</td><td>0.01</td><td>0.01</td></tr></table>

![](images/3638d226fc9aaa5825657bb065aeec344600c643c4231a10935b692cca1cbbed.jpg)  
Fig. 5: Representative 256×256 stego-faces synthesized by a DDPM equipped with ANStega. Despite their natural appearance, each image conceals roughly 463 kbits of payload.

TABLE VIII: Steganalysis accuracy against ANStega.

<table><tr><td></td><td>FCN</td><td>CNN</td><td>R-BiLSTM-C</td><td>BiLSTM-Dense</td></tr><tr><td>Acc</td><td>49.92%</td><td>50.28%</td><td>49.35%</td><td>50.15%</td></tr></table>

TABLE IX: Context and generation examples.

<table><tr><td>Context</td><td>ANStega Generation</td></tr><tr><td>Beneath the quiet sky, dreams wander like fireflies, glowing softly in the silence of hope.</td><td>Yet, in the stillness of the night, what lies hidden, unseen by mortal eyes, is a dance of shadows, an art of darkness, an eternal sway of the pierced heart.</td></tr><tr><td>Even the darkest night cannot extinguish a heart that burns with purpose.</td><td>Every experience, no matter how difficult, is an opportunity to learn, grow, and rise above the challenges that we face. Courage and perseverance can help us overcome the impossible and lead us to new heights of success and fulfillment.</td></tr><tr><td>Titanic is not just a love story set against tragedy—it’s a cinematic elegy to fleeting beauty, human hubris, and the moments that define a lifetime.</td><td>James Cameron’s sweeping epic is a masterclass in filmmaking, a testament to the power of storytelling, and a reminder that even the most epic of tragedies can be told with a disparate array of miniatures, models, and digital wizardry.</td></tr></table>

## ACKNOWLEDGMENT

The authors thank the reviewers for their valuable comments. This work was supported in part by the Natural Science Foundation of China under Grant 62302146, 62472398, and U2336206.

## REFERENCES

[1] U. S. Congress, “Kids online safety act,” https://www.congress.gov/bill/ 118th-congress/house-bill/7891, April 2024.

[2] U. K. Parliament, “Online safety act 2023,” https://bills.parliament.uk/ bills/3137, 2023.

[3] D. Cole, “We kill people based on metadata,” https://www.nybooks.com/ online/2014/05/10/we-kill-people-based-metadata/, May 2014.

[4] G. J. Simmons, “The prisoners’ problem and the subliminal channel,” in Annual International Cryptology Conference, 1983. [Online]. Available: https://api.semanticscholar.org/CorpusID:2674577

[5] L. A. Bauer, J. K. Howes, S. A. Markelon, V. Bindschaedler, and T. Shrimpton, “Leveraging generative models for covert messaging: Challenges and tradeoffs for ”dead-drop” deployments,” in Proceedings of the Fourteenth ACM Conference on Data and Application Security and Privacy, ser. CODASPY ’24. New York, NY, USA: Association for Computing Machinery, 2024, p. 67–78. [Online]. Available: https://doi.org/10.1145/3626232.3653264

[6] Z.-L. Yang, X.-Q. Guo, Z.-M. Chen, Y.-F. Huang, and Y.-J. Zhang, “Rnnstega: Linguistic steganography based on recurrent neural networks,” IEEE Transactions on Information Forensics and Security, vol. 14, no. 5, pp. 1280–1295, 2019.

[7] F. Dai and Z. Cai, “Towards near-imperceptible steganographic text,” in Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, A. Korhonen, D. Traum, and L. Marquez,\` Eds. Florence, Italy: Association for Computational Linguistics, Jul. 2019, pp. 4303–4308. [Online]. Available: https://aclanthology.org/ P19-1422/

[8] T. Van Le and K. Kurosawa, “Bandwidth optimal steganography secure against adaptive chosen stegotext attacks,” in Information Hiding, J. L. Camenisch, C. S. Collberg, N. F. Johnson, and P. Sallee, Eds. Berlin, Heidelberg: Springer Berlin Heidelberg, 2007, pp. 297–313.

[9] K. Yang, K. Chen, W. Zhang, and N. Yu, “Provably secure generative steganography based on autoregressive model,” in International Workshop on Digital Watermarking, 2018. [Online]. Available: https://api.semanticscholar.org/CorpusID:59524394

[10] K. Chen, H. Zhou, H. Zhao, D. Chen, W. Zhang, and N. Yu, “When provably secure steganography meets generative models,” 2019. [Online]. Available: https://arxiv.org/abs/1811.03732v2

[11] Z. Ziegler, Y. Deng, and A. M. Rush, “Neural linguistic steganography,” in Proceedings ofthe 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), 2019, pp. 1210–1215.

[12] S. Zhang, Z. Yang, J. Yang, and Y. Huang, “Provably secure generative linguistic steganography,” in Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021, C. Zong, F. Xia, W. Li, and R. Navigli, Eds. Online: Association for Computational Linguistics, Aug. 2021, pp. 3046–3055. [Online]. Available: https: //aclanthology.org/2021.findings-acl.268

[13] G. Kaptchuk, T. M. Jois, M. Green, and A. D. Rubin, “Meteor: Cryptographically secure steganography for realistic distributions,” Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, 2021. [Online]. Available: https: //api.semanticscholar.org/CorpusID:235309313

[14] J. Ding, K. Chen, Y. Wang, N. Zhao, W. Zhang, and N. H. Yu, “Discop: Provably secure steganography in practice based on ”distribution copies”,” 2023 IEEE Symposium on Security and Privacy (SP), pp. 2238–2255, 2023. [Online]. Available: https://api.semanticscholar.org/CorpusID:260002610

[15] C. S. de Witt, S. Sokota, J. Z. Kolter, J. N. Foerster, and M. Strohmeier, “Perfectly secure steganography using minimum entropy coupling,” in The Eleventh International Conference on Learning Representations, 2023. [Online]. Available: https://openreview. net/forum?id=HQ67mj5rJdR

[16] Y. Liu, C. Xu, F. Yang, P. Zhang, and L. Wang, “Linguistic steganography via self-adjusting asymmetric number system,” Computational Linguistics, pp. 1–35, 09 2025. [Online]. Available: https://doi.org/10.1162/coli.a.22

[17] G. Liao, J. Yang, W. Shao, and Y. Huang, A framework for designing provably secure steganography. USA: USENIX Association, 2025.

[18] M. Bai, K. Pang, G. Liao, J. Yang, and Y. Huang, “Shimmer: a provably secure steganography based on entropy collecting mechanism,” in Proceedings of the 34th USENIX Conference on Security Symposium, ser. SEC ’25. USA: USENIX Association, 2025.

[19] Y. Wang, G. Pei, K. Chen, J. Ding, C. Pan, W. Pang, D. Hu, and W. Zhang, “SparSamp: Efficient provably secure steganography based on sparse sampling,” in 34th USENIX Security Symposium (USENIX Security ’25). USENIX Association, Aug. 2025.

[20] T. M. Jois, G. Beck, and G. Kaptchuk, “Pulsar: Secure steganography for diffusion models,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, ser. CCS ’24. New York, NY, USA: Association for Computing Machinery, 2024, p. 4703–4717. [Online]. Available: https://doi.org/10.1145/3658644. 3690218

[21] Y. Peng, D. Hu, Y. Wang, K. Chen, G. Pei, and W. Zhang, “Stegaddpm: Generative image steganography based on denoising diffusion probabilistic model,” in Proceedings of the 31st ACM International Conference on Multimedia, ser. MM ’23. New York, NY, USA: Association for Computing Machinery, 2023, p. 7143–7151. [Online]. Available: https://doi.org/10.1145/3581783.3612514

[22] A. D. Ker, “Improved detection of lsb steganography in grayscale images,” in International workshop on information hiding. Springer, 2004, pp. 97–115.

[23] M. Boroumand, M. Chen, and J. Fridrich, “Deep residual network for steganalysis of digital images,” IEEE Transactions on Information Forensics and Security, vol. 14, no. 5, pp. 1181–1193, 2019.

[24] R. Anderson and F. Petitcolas, “On the limits of steganography,” IEEE Journal on Selected Areas in Communications, vol. 16, no. 4, pp. 474– 481, 1998.

[25] J. Duda, “Asymmetric numeral systems,” 2009. [Online]. Available: https://arxiv.org/abs/0902.0271

[26] https://github.com/facebook/zstd.

[27] https://github.com/lzfse/lzfse.

[28] https://github.com/google/pik.

[29] D. E. Gladding, S. Gopalakrishnan, S. D. Kumbhani, and L. Hsu-Kuei, “Features of range asymmetric number system encoding and decoding,” Jan. 25 2022, uS Patent 11,234,023.

[30] G. J. Simmons, “The prisoners’ problem and the subliminal channel,” in Advances in Cryptology: Proceedings of Crypto 83. Springer, 1984, pp. 51–67.

[31] N. J. Hopper, J. Langford, and L. von Ahn, “Provably secure steganography,” in Advances in Cryptology — CRYPTO 2002, M. Yung, Ed. Berlin, Heidelberg: Springer Berlin Heidelberg, 2002, pp. 77–92.

[32] T. Fang, M. Jaggi, and K. Argyraki, “Generating steganographic text with lstms,” in Proceedings of ACL 2017, Student Research Workshop, 2017, pp. 100–106.

[33] Z.-L. Yang, X.-Q. Guo, Z.-M. Chen, Y.-F. Huang, and Y.-J. Zhang, “Rnnstega: Linguistic steganography based on recurrent neural networks,” IEEE Transactions on Information Forensics and Security, vol. 14, no. 5, pp. 1280–1295, 2019.

[34] G. Kaptchuk, T. M. Jois, M. Green, and A. D. Rubin, “Meteor: Cryptographically secure steganography for realistic distributions,” in Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security, 2021, pp. 1529–1548.

[35] S. Zhang, Z. Yang, J. Yang, and Y. Huang, “Provably secure generative linguistic steganography,” in Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021, 2021, pp. 3046–3055.

[36] J. Duda, “Asymmetric numeral systems: entropy coding combining speed of huffman coding with compression rate of arithmetic coding,” arXiv preprint arXiv:1311.2540, 2013.

[37] Y. Collet and M. Kucherawy, “Zstandard Compression and the application/zstd Media Type,” RFC 8478, Oct. 2018. [Online]. Available: https://www.rfc-editor.org/info/rfc8478

[38] J. Sneyers, J. Alakuijala, L. Versari, Z. Szabadka, S. Boukortt, A. Cohen-Tidhar, M. Firsching, E. Kliuchnikov, T. Lev-Ami, E. Portis, T. Richter, and O. Watanabe, “The jpeg xl image coding system: History, features, coding tools, design rationale, and future,” 2025. [Online]. Available: https://arxiv.org/abs/2506.05987

[39] T. Cover and J. Thomas, Elements of information theory. Wiley-Interscience, 2006.

[40] https://huggingface.co/openai-community/gpt2.

[41] https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct.

[42] https://huggingface.co/Qwen/Qwen2.5-3B-Instruct.

[43] https://huggingface.co/HuggingFaceTB/SmolLM2-135M.

[44] https://huggingface.co/microsoft/phi-2.

[45] https://ai.stanford.edu/<sup>∼</sup>amaas/data/sentiment/.

[46] A. Holtzman, J. Buys, M. Forbes, A. Bosselut, D. Golub, and Y. Choi, “Learning to write with cooperative discriminators,” in Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), I. Gurevych and Y. Miyao, Eds. Melbourne, Australia: Association for Computational Linguistics, Jul. 2018, pp. 1638–1649. [Online]. Available: https: //aclanthology.org/P18-1152

[47] A. Holtzman, J. Buys, L. Du, M. Forbes, and Y. Choi, “The curious case of neural text degeneration,” in International Conference on Learning Representations, 2020. [Online]. Available: https: //openreview.net/forum?id=rygGQyrFvH

[48] Z. Yang, Y. Huang, and Y.-J. Zhang, “A fast and efficient text steganalysis method,” IEEE Signal Processing Letters, vol. 26, no. 4, pp. 627–631, 2019.

[49] ——, “Ts-csw: text steganalysis and hidden capacity estimation based on convolutional sliding windows,” Multimedia Tools Appl., vol. 79, no. 25–26, p. 18293–18316, Jul. 2020. [Online]. Available: https://doi.org/10.1007/s11042-020-08716-w

[50] Y. Niu, J. Wen, P. Zhong, and Y. Xue, “A hybrid r-bilstm-c neural network based text steganalysis,” IEEE Signal Processing Letters, vol. 26, no. 12, pp. 1907–1911, 2019.

[51] H. Yang, Y. Bao, Z. Yang, S. Liu, Y. Huang, and S. Jiao, “Linguistic steganalysis via densely connected lstm with feature pyramid,” Proceedings of the 2020 ACM Workshop on Information Hiding and Multimedia Security, 2020. [Online]. Available: https: //api.semanticscholar.org/CorpusID:219980226

[52] J. Choi, S. Kim, Y. Jeong, Y. Gwon, and S. Yoon, “Ilvr: Conditioning method for denoising diffusion probabilistic models,” in 2021 IEEE/CVF International Conference on Computer Vision (ICCV), 2021, pp. 14 347– 14 356.

[53] M. Bai, J. Yang, K. Pang, X. Xu, Z. Yang, and Y. Huang, “Provably robust and secure steganography in asymmetric resource scenario,” in 2025 IEEE Symposium on Security and Privacy (SP), 2025, pp. 1438– 1456.

## APPENDIX A

NORMALIZATION MECHANISM OF THE STREAMING RANSENCODER

## A. Derivation of the Normalization Condition

A fundamental requirement of the rANS encoder is that after encoding any symbol s, the new state $\mathcal { C } ( s , x )$ must remain within the normalization interval I. This can be expressed as: $L \ \leq \ { \mathcal { C } } ( s , x ) \ < \ 2 L$ . To avoid a computationally expensive trial-and-error loop to enforce this condition, we derive an equivalent but far simpler direct condition on x. The derivation proceeds as follows. First, we substitute the definitions of $\mathcal { C } ( s , x )$ and $L = \alpha \times M$ into inequality (1):

$$
\alpha \times M \leq \left\lfloor \frac {x}{f _ {s}} \right\rfloor + C _ {s} + (x \bmod f _ {s}) <   2 \times \alpha \times M\tag{17}
$$

Dividing all parts of the inequality by M yields:

$$
\alpha \leq \left\lfloor \frac {x}{f _ {s}} \right\rfloor + \left[ C _ {s} + (x \bmod f _ {s}) \right] / M <   2 \alpha\tag{18}
$$

Let us analyze the fractional term $[ C _ { s } + ( x$ mod $f _ { s } ) ] / M$ By definition, $C _ { s } + f _ { s } \le M$ . Since $0 \leq$ (x mod $f _ { s } ) < f _ { s } ,$ , it follows that $0 \leq C _ { s } + ( x$ mod $f _ { s } ) < C _ { s } + f _ { s } \le M$ . Therefore, the value of the fractional term is bounded within the range [0, 1).

$$
0 \leq [ C _ {s} + (x \bmod f _ {s}) ] / M <   1\tag{19}
$$

Given that $\lfloor x / f _ { s } \rfloor$ is an integer and the fractional term is in [0, 1), the inequality18 can be simplified by considering only the integer parts:

$$
\alpha \leq \left\lfloor \frac {x}{f _ {s}} \right\rfloor <   2 \alpha\tag{20}
$$

Based on the properties of the floor function, inequality (5) is equivalent to:

$$
\alpha \leq \frac {x}{f _ {s}} <   2 \alpha\tag{21}
$$

Finally, multiplying all parts by $f _ { s }$ gives the direct constraint on the state x:

$$
\alpha f _ {s} \leq x <   2 \alpha f _ {s}\tag{22}
$$

## APPENDIX B ARTIFACT APPENDIX

This appendix provides a self-contained guide for evaluating the artifact for this paper.

## A. Description & Requirements

This section details the necessary components to set up the experimental environment and run the artifact.

1) How to access: The artifact is provided as a supplementary .zip file. A permanent, archived version is publicly accessible via the Zenodo repository at https://doi.org/10.5281/ zenodo.17943483.

2) Hardware dependencies:

• CPU: A modern multi-core CPU (e.g., Intel Xeon Gold 6330, as used in the paper).

• GPU: An NVIDIA GPU with sufficient VRAM is required for running the language models. An NVIDIA RTX 4090 (24GB) was used for the paper’s experiments. A GPU with at least 16GB of VRAM is recommended for the larger models (Llama 3 8B). The gpt2 model can be run on smaller-VRAM GPUs.

3) Software dependencies:

• Python ≥ 3.10

• PyTorch (CUDA 11.8 version is specified in requirements.txt)

• All other Python dependencies are listed in requirements.txt.

4) Benchmarks:

• Models: The artifact is designed to work with Hugging Face-compatible causal language models. The paper evaluates:

– GPT-2 (openai-community/gpt2)

– Llama 3 8B (meta-llama/Meta-Llama-3-8B -Instruct)

– Qwen2.5 3B (Qwen/Qwen2.5-3B-Instruct)

– DeepSeek-R1-Distilled-Qwen (deepseek-ai/DeepSeek-R1-Distill -Qwen-1.5B)

– SmolLm2 (HuggingFaceTB/SmolLM2-135M)

– Phi-2 (microsoft/phi-2)

The scripts will automatically download gpt2 if no local path is provided. Other models must be downloaded by the user from Hugging Face.

## • Datasets:

– imdb\_context.xlsx: (Provided) Contains 1,000 contexts from the IMDB movie review dataset. The batch script uses the first 100 entries for evaluation.

– message.txt: (Provided) A binary string used as the secret message payload.

## B. Artifact Installation & Configuration

[Estimated time: 10-15 minutes, plus model download time]

## 1) Unzip the artifact:

unzip anstega\_artifact.zip cd anstega\_artifact

2) Create a Python virtual environment: python3 -m venv venv source venv/bin/activate

3) Install dependencies: Install all required Python packages using the provided requirements.txt file. pip install -r requirements.txt

## 4) Model Preparation:

• Option 1 (Quick Test): No action needed. The scripts run\_single.py and run\_batch.py will default to loading openai-community/gpt2 from Hugging Face if the specified model\_name path is not found.

• Option 2 (Full Reproduction): To reproduce results for other models (e.g., Llama 3), manually download the model from Hugging Face and save it to a local directory. You will then need to update the model\_name variable in run\_single.py or run\_batch.py to point to this local path (e.g., model\_name = ’./LLaMA3\_8B/’).

## C. Experiment Workflow

The evaluation workflow is straightforward:

1) Installation: Set up the environment and dependencies as described in Section B.

2) Functional Test: Run run\_single.py to perform a single encoding and decoding pass. This verifies that the core ANStega algorithm is working correctly.

3) Performance Evaluation: Run run\_batch.py to execute the algorithm over 100 different contexts. This script computes and reports the average performance metrics (ER, UR, ES, GS, SITR) that directly correspond to the results presented in the paper.

## D. Major Claims

This artifact supports the following major claims from the paper:

• (C1) Optimal Capacity: ANStega achieves near-optimal embedding capacity, approaching the Shannon entropy limit (Utilization Rate, UR ≈ 1.0) and outperforming prior secure methods. This is proven by experiment (E2) and corresponds to the ’ER’ (bits/token) and ’UR’ metrics in Tables V and VI.

• (C2) Optimal Efficiency: ANStega has O(1) embedding complexity, resulting in high Embedding Speed (ES), Generation Speed (GS), and a minimal Sampling-to-Inference Time Ratio (SITR) that is competitive with AC-based methods and vastly superior to other provably secure methods. This is proven by experiment (E2) and corresponds to the ’ES’, ’GS’, and ’SITR’ metrics in Tables IV, V, and VI.

## E. Evaluation

This section provides the operational steps to validate the artifact and reproduce the paper’s key results.

Experiment (E1): Functional & Correctness Test: [∼5 human-minutes + <5 compute-minutes]

This experiment validates the correctness of the ANStega implementation by encoding a message and verifying that it can be perfectly decoded.

## • [Preparation]

1) Ensure the environment is set up (Section B).

2) No other preparation is needed. The script run\_single.py is configured to use gpt2 by default if no other model is found.

• [Execution] Run the single test script:

python run\_single.py

• [Results] The script will:

1) Print its configuration (token num, precision, etc.).

2) Print the auto-selected device (e.g., cuda).

3) Print the generated stego text.

4) Print a result\_dict with the performance metrics (ER, UR, ES, GS, SITR) for this single run.

5) Crucially, it will end by printing:

success!

This ”success!” message confirms that the outbits\_list from decoding perfectly matched the encoded\_message from encoding.

Experiment (E2): Performance & Capacity Evaluation (Batch): [∼5 human-minutes + 30-90 compute-minutes, depending on GPU/model]

This experiment reproduces the core performance metrics (ER, UR, ES, GS, SITR) presented in Tables IV, V, and VI by running a batch evaluation over 100 contexts.

## • [Preparation]

1) Ensure the environment is set up (Section B).

2) Ensure the imdb\_context.xlsx and message.txt files are in the same directory.

3) (Optional but recommended) To reproduce the paper’s main results for larger models, download the Qwen2.5-3B-Instruct model (or other models like Qwen) from Hugging Face... and edit run\_batch.py. Change the model name variable to point to its local path:

model\_name = ’/path/to/your/model/

## • [Execution] Run the batch test script:

python run\_batch.py

A tqdm progress bar will show the progress as it iterates through the 100 contexts.

• [Results] After the batch run is complete, the script will print a final result\_dict containing the average metrics over all 100 runs. Example (values will vary based on hardware and model): These values correspond to the metrics for Claims C1 and C2. The evaluator can compare these generated values directly with the rows for ANStega in Tables IV, V, and VI of the paper (for the corresponding model). Note: Exact speed metrics (ES, GS) will vary based on hardware, but the ER and UR values should be very close to the paper’s reported results.

## F. Customization

The experiments can be customized by modifying the parameters at the top of run\_single.py and run\_batch.py.

• model\_name: Path to the local Hugging Face model directory.

• seed: Random seed for reproducibility.

• precision: ANS precision parameter.

• ans\_t: ANS scale factor (referred to as α in the paper, Table II).

• top\_p: Nucleus sampling (top-p) value.

• token\_num: Number of tokens to generate.
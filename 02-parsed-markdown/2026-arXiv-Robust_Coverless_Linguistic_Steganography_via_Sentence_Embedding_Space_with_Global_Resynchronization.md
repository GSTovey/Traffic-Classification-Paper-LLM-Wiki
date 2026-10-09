# Robust Coverless Linguistic Steganography via Sentence Embedding Space with Global Resynchronization

Lizhi Xiong<sup>✉</sup> Nanjing University of Information Science and Technology Nanjing, China lzxiong16@163.com

Yuping Lu Nanjing University of Information Science and Technology Nanjing, China 202412200704@nuist.edu.cn

Ziqiang Li Nanjing University of Information Science and Technology Nanjing, China iceli@mail.ustc.edu.cn

Jun Li Nanjing University of Information Science and Technology Nanjing, China lijuun@yeah.net

Zhangjie Fu Nanjing University of Information Science and Technology Nanjing, China wwwfzj@126.com

## Abstract

Linguistic steganography enables covert communication through natural language. Existing methods heavily rely on token-level oper ations and struggle to maintain reliability under word- and sentencelevel textual perturbations. Moreover, variable-length coding-based schemes are highly susceptible to bit-slippage under minor distur bances, as perturbations cause desynchronization between embed ded and extracted bit sequences. To address these issues, we propose a robust coverless steganographic framework that operates in the sentence embedding space rather than the token space. Specifically, secret messages are encoded as hierarchical clustering paths in the sentence embedding space, which enhances decoding stability against word- and sentence-level textual perturbations. To tackle the bit-slippage problem, we introduce a Global Resynchroniza tion Mechanism (GRM) that reframes variable-length bitstreams as discrete symbols anchored to semantic subspaces, decoupling local embedding failures from global message recovery. Experi mental results demonstrate that under word- and sentence-level perturbations, our approach achieves substantial improvements in robustness, while maintaining efective embedding capacity and exhibiting strong resistance to statistical analysis.

## CCS Concepts

• Security and privacy → Human and societal aspects of se curity and privacy; • Computing methodologies → Lexical semantics.

## Keywords

Robust Linguistic Steganography; Sentence Embedding Space; Error Correction Code

## 1 Introduction

With the advancement and development of social networks, today’s social media platforms increasingly rely on automated systems for large-scale and strict information regulation to monitor, filter, and shape public opinion. Under the circumstances, users are turning to steganography as a covert means of conveying sensitive information, aiming to protect personal privacy. Steganography is a technique that embeds secret information into seemingly innocuous carriers to enable covert communication without arousing suspicion. In the age of digital steganography, people use texts, images [28], videos [2], and audios [29] as media to transmit secret messages. As the most fundamental medium of human communication, text is generated, transmitted, and consumed at massive scale across social media platforms every day, providing a natural and abundant cover for information hiding. Consequently, embedding secret information in text has become an important and active branch of steganography research.

Existing steganography methods are classified into modificationbased, retrieval-based and generative steganography. In the first two methods, secret messages are conveyed by altering or selecting words [36] or sentences [27] according to predefined coding rules. Such methods are inherently fragile due to the sensitivity of the characters. Even slight deletions or replacements may break the shared dictionary/codebook correspondence, leading to incorrect decoding or complete extraction failure once the edited content falls outside the shared dictionary. Subsequently, generative linguistic steganography [34, 42] based on Autoregressive Models (ARMs) [24] gained popularity due to fluent and natural generation. In these methods, secret information is embedded by sampling from context-conditioned token probability distributions; however, their strong sequential dependency makes them extremely fragile, as tampering with a single token can propagate errors to subsequent tokens and cause irreversible information loss, especially when attacks introduce error contents or segmentation ambiguity [18]. As shown in Figure 1, for methods that use characters or tokens as steganographic channels, even minor perturbations can cause decoding to fail. Therefore, existing text steganography methods generally sufer from insuficient robustness when facing realistic text attacks, fundamentally limiting their practical applicability.

![](images/e8014f868f0b74ef935fbb894d70d8a112af9c4c0d4ca8f6f2624df08e8b4262.jpg)  
Figure 1: An example of decoding error due to attacked token not in the vocabulary.

To address the problem, later robust steganographic methods [5, 16, 19] introduced some defense mechanisms at the token-level to enable partial recovery. Nevertheless, these defense mechanisms focus only on token-level perturbations while ignoring word- and sentence-level attacks. In practice, real-world adversaries are un aware of the steganographic system’s segmentation rules and tend to operate at the word- or sentence-level through deletion, inser tion anywhere or paraphrasing. Consequently, while token-level defenses can improve robustness against token-boundary-aligned perturbations, robustness under practical word- and sentence-level rewriting remains a fundamental and unresolved challenge for cur rent text steganography frameworks.

To address these challenges, we propose a robust coverless lin guistic steganography framework in the sentence embedding space. Specifically, a shared sentence encoder maps sentences into a uni fied semantic space, which is partitioned into multiple codable semantic subspaces for information hiding. We cluster the seman tic space in a hierarchical manner to reduce the computational overhead associated with the clustering required for high-capacity. Secret information is conveyed through subspace selection and sentence sampling within the selected subspace. To ensure the security ofsubspace selection, a provably secure coding-and-sampling strategy is adopted to selectively encode only a subset of seman tic subspaces, so that the resulting sampling distribution remains consistent with the underlying natural distribution. However, this strategy is inherently variable-length, and thus a subspace predic tion error at the receiver may lead to a local mismatch between the extracted and embedded message lengths, causing bit-slippage across subsequent bits. To address this issue, we organize the hid den information as discrete symbols aligned with the partitioning structure of the semantic space and integrate LT codes for global recovery, thereby localizing decoding errors and improving robust ness against text perturbations.

Our contributions can be summarized as follows:

• We propose a novel coverless linguistic steganography framework that shifts the embedding operation from fragile token sequences to a robust, high-dimensional sentence embedding space. By leveraging the approximate semantic invariance of sentence embeddings, our method inherently absorbs word and sentence-level textual perturbations.

• We propose a Hierarchical Clustering Mechanism (HCM) that cluster the semantic space into codable subspaces efficiently. By recursive pruning and hierarchical mapping, HCM achieves an optimal balance between embedding capacity and computational eficiency, reducing the complexity from exponential to linear.

• To resolve the critical issue of bit-slippage in variable-length provably secure encoding, we introduce a Global Resynchronization Mechanism (GRM). By reframing local desyn chronization as symbol erasures and integrating LT codes for global recovery, GRM decouples local embedding failures from global message integrity.

• Extensive experiments demonstrate that our method achieves strong robustness and efective embedding capacity under word- and sentence-level textual attacks.

## 2 Related Work

## 2.1 Retrieval Linguistic Steganography

Retrieval steganography requires the sender and receiver to share a large dataset and a set of coding rules, whose advantage is that the transmitted carrier remains natural without any modification. The sender selects a group of elements that can be mapped to the secret messages and sends them to the receiver to realize the transmission of secret information. For example, [37] established the mapping relationship through the word-frequency characteristics in the corpus; [9] encoded text according to the distance in semantic space; [25] built a search tree according to the character structure; [6] jointly realized information hiding through a database combining graphics and text. Retrieval linguistic steganography is a type of coverless steganography. Current retrieval-based text steganography methods have not systematically investigated steganographic robustness, which needs to be further explored. These methods rely on ARMs and hardly change the probability distribution of the generated words or semantics to ensure security when embedding secret information.

## 2.2 Provably Secure Linguistic Steganography

In recent years, researchers have proposed a variety of provably secure linguistic steganography methods based on generative language models. These methods are dedicated to designing messageembedding algorithms that are indistinguishable from the conventional text-generation process. ADG [40] adaptively and dynamically grouped tokens based on the probability generated by the pre-trained language model and recursively embeds secret information. Meteor [7] used the random prefix shared by the generation model to embed the message into the sampling random number and masked it at once, dynamically adapted to entropy changes, and takes both security and eficiency into account. Discop [4] proposed the “distributed copies” technique, which uses the index value of these “copies” to express secret information during the generation process and realizes practical steganography with provable security and high capacity. [15] made two major improvements to the prefix-encoding method—quantitative fine-tuning and distributed coupling—to repair security and capacity defects.

## 2.3 Robust Linguistic Steganography

In recent years, researchers began to pay attention to the problem of message loss caused by segmentation ambiguity, and designed corresponding countermeasures. SECC [5] overlaid an ECC layer similar to LT codes [10] on the conventional generative steganography pipeline to improve character-level erasure resistance; however, it didn’t mitigate the original extraction-error problem. To avoid al tering the probability distribution of candidate words, Syncpool [18] merged tokens that share a prefix into an “ambiguity pool” and used a shared encrypted pseudo-random generator to ensure con sistent selection, yet the secret information remained sensitive to vocabulary shifts.

Active textual attacks—such as deletion, insertion, and tampering—have also been studied. GTSD [30] employed a difusion model to generate candidate texts and embeds information via prompt-and batch mapping, achieving local robustness. Winstega [16] sacrificed capacity for anti-editing capability by using a sliding window and entropy-threshold-based discontinuous embedding during inference. STEAD [19] embedded duplicate codes in parallel at multiple locations within a single denoising step of a difusion model and co ordinated with neighborhood-search alignment to realize provably secure steganography resistant to insertion and deletion. These approaches achieved stable extraction under their respective tokenlevel active attacks.

## 2.4 Sentence Embedding Encoder

Sentence embeddings are obtained by encoding text sentences with a sentence embedding encoder. After suficient training, embed dings of semantically similar sentences exhibit higher similarity and smaller distance. Semantic similarity is computed by:

$$
\operatorname{Sim} (A, B) = \frac {A \cdot B}{\| A \| \| B \|} = \frac {\sum_ {i = 1} ^ {n} A _ {i} B _ {i}}{\sqrt {\sum_ {i = 1} ^ {n} A _ {i} ^ {2}} \sqrt {\sum_ {i = 1} ^ {n} B _ {i} ^ {2}}},\tag{1}
$$

where � and � denote the vector representations of the sentences, and $A _ { i }$ and $B _ { i }$ are their �-th components.

Owing to diferent training parameters and embedding dimen sions, each encoder exhibits distinct characteristics. For instance, the static encoder [12], trained with modest parameters, yields a relatively flat and uniform semantic space suitable for small models, but its advantage is speed. In contrast, encoders based on large models [1] produce a more comprehensive and high-dimensional semantic space at the cost of increased time and memory, yet ofer stronger text-processing capabilities. Due to the strong similarity matching ability, sentence embeddings are widely employed in downstream tasks such as retrieval [8], clustering [23], etc.

## 3 Proposed Method

## 3.1 Deployment Assumption and Threat Model

The proposed framework focuses on a symmetric key steganography system: the sender and receiver need to share the same dataset, sentence embedding encoder, LT Encoding Symbol Identifiers (ESI) and pseudo-random number key to ensure the construction of the same sentence-level semantic space and the success of extraction. The adversary can apply semantic-preserving perturbations but has no access to shared secrets, aiming to disrupt communication without altering meaning. Consider a Probabilistic Polynomial-Time (PPT) adversary operating in a highly regulated environment whose duty is to detect and eliminate covert communication that may be hidden in public texts. The adversary intercepts any text transmitted over public channels and possesses two capabilities: Detection capability. The adversary can apply steganalysis techniques to determine whether the suspicious texts may contain secret information. This corresponds to the security requirement.

Tampering capability. The adversary can tamper a text � into $s ^ { \prime } ,$ , but within limits: the semantic content of � remain unchanged. Let textual attack be a transformation operator: $\mathcal { A } : s  s ^ { \prime } .$ . This transformation satisfies approximate semantic invariance:

$$
\left\| \mathbf {v} (s ^ {\prime}) - \mathbf {v} (s) \right\| _ {2} \leq \epsilon ,\tag{2}
$$

where $\mathbf { v } ( s )$ denotes the semantic vector of � and � is the tampering threshold. This corresponds to the robustness requirement of steganography.

## 3.2 Overview

In this section, we introduce the proposed steganography framework. First of all, we introduce how to construct and partition semantic space and how to improve the eficiency. Then, we will describe the security application of SparSamp sampling method in this framework, and point out its limitations in robustness. On this basis, we employ a Global Resynchronization Mechanism (GRM) to improve it.

Figure 2 shows the proposed stegosystem. In the embedding phase, we cluster the sentence embedding spaces mapped by the dataset, and code and sample the divided semantic subspaces at multiple levels. At the same time, we encode the secret messages to be sent into symbol blocks, and embed them into each subspace layer in units of symbol blocks. After the iteration, we randomly select sentence samples in the selected subspaces and send them as steganography carriers. Text attacks may occur during transmission. In the extraction phase, we use the same sentence encoder as in the embedding phase to reconstruct the semantic space of the shared dataset, predict the semantic subspace of each sentence embedding in the steganography texts, reproduce the same hierarchical clustering results as the embedding phase, and decode the symbol blocks according to the sampling process. Finally, we use Belief Propagation (BP) decoder to accurately recover the original secret messages according to the collected symbol blocks.

## 3.3 Construction of Semantic Space

Robust Subspace Construction. The core of our robust framework lies in the structural stability inherent in the high-dimensional sentence manifold. High-quality sentence embeddings, generated by pre-trained encoders, exhibit a crucial property of semantic invariance: sentences with minor textual perturbations tend to cluster within a constrained neighborhood in the semantic space $V _ { S } .$ By applying clustering algorithms to partition $V _ { S }$ into a set of disjoint subspaces—rather than arbitrary partitioning—we capitalize on the natural distribution of the data to minimize intra-cluster variance. Due to the sparsity of high-dimensional spaces, most samples are distributed near the centroid. Consequently, we can establish a stable mapping between secret information and regional semantic characteristics. In this schema, we select the semantic subspaces as the fundamental steganographic units rather than individual tokens or specific sentence instances. Since the secret bits are tied to the subspace identity rather than the precise coordinates of a single vector, the system can tolerate significant word-level or sentence-level attacks. As long as the perturbed stego sentence $s ^ { \prime }$ satisfies the semantic proximity constraint Eq. 2 and remains within the original cluster boundary, the receiver can accurately identify the corresponding subspace and retrieve the secret message. This structure-level design efectively decouples the hidden information from fragile textual surface forms, thereby providing intrinsic robustness against various practical attacks.

![](images/ace8c0e6ca7236fafb48607d0f896faa02873e9b9e77794aebebe5bc46e82087.jpg)  
Figure 2: An overview of the proposed stegosystem. Embedding and extraction are mutually inverse processes.

We use k-means algorithm to cluster a semantic space $V _ { S } .$ . Given the number of clusters � and pseudo-random seed $r _ { c } ,$ k-means clustering can be formalized as the following optimization problem:

$$
\begin{array}{l} \{\boldsymbol {\mu} _ {1}, \ldots , \boldsymbol {\mu} _ {k} \} = \arg \min _ {\{\boldsymbol {\mu} _ {j} \} _ {j = 1} ^ {k}} \sum_ {i = 1} ^ {N} \min _ {1 \leq j \leq k} \left\| \mathbf {v} _ {i} - \boldsymbol {\mu} _ {j} \right\| _ {2} ^ {2}, \\ \text {s.t.} \quad \boldsymbol {\mu} _ {j} ^ {(0)} \sim \mathcal {P} (r _ {c}), \end{array}\tag{3}
$$

where $\mu _ { j }$ is the �-th cluster center, $\mu _ { j } ^ { ( 0 ) }$ is the initial centroid initial ized by the pseudo-random number $r _ { c } ,$ and $\mathcal { P } ( r _ { c } )$ is the initialization distribution determined by the random seed $r _ { c } .$

After clustering, the semantic space �<sub>�</sub> is divided into � disjoint semantic subspaces. To ensure that each semantic subspace has suficient stability, we test diferent values of � to determine the appropriate threshold. When the optimization convergence time is too long or the subspaces are too small to be robust after clustering, we consider � to be too large. When the value of � is set too small, although there is no concern about the stability of the subspace, the embedding capacity becomes too limited. Since both sides of the communication share the same $r _ { c } ,$ the clustering function is determined:

$$
\mathcal {C} _ {r _ {c}}: V _ {S} \to \{V _ {1}, V _ {2}, \dots , V _ {k} \},\tag{4}
$$

thereby ensuring that the sender and receiver obtain consistent semantic subspace partition results.

Hierarchical Clustering Mechanism. If a high steganography capacity is required, a large dataset must be used to construct a richer semantic space, thereby enabling the partitioning of more semantic subspaces. As shown in Eq. 3, the time complexity of the k-means algorithm for � samples is �(� · �). Assuming that a single sentence is to embed � secret bits, Shannon’s source-coding principle [22] dictates that � secret bits requires at least $2 ^ { b }$ distinguishable states. Consequently, the number of sub-clusters k must scale as:

$$
k \propto 2 ^ {b}.\tag{5}
$$

Then the time complexity of the algorithm is $O ( N \cdot 2 ^ { b } )$ . Therefore, when clustering large semantic spaces, increases in the number of samples � and in the number of secret bits � incur significant computational overhead.

To address this problem, we design a Hierarchical Clustering Mechanism (HCM) that embeds � secret bits across � layers, with each layer carrying <sup>¯</sup>� bits. In each layer �, the encoding process selects a specific cluster $V _ { h i t } ^ { ( i ) }$ as the $\mathrm { \hbar \hbar \mathrm { i t } } ^ { \mathfrak { s } }$ subspace based on the secret bits and designates it as the semantic space $V ^ { ( i + 1 ) }$ for the next layer. This cycle repeats � times.

The time complexity ofthis algorithm is $l { \cdot } O ( N { \cdot } 2 ^ { \bar { b } } )$ . Based on the actual clustering eficiency, we set <sup>¯</sup>� to 2 or 3. Then the complexity of each layer of clustering can be controlled and stable, and the overall time complexity can be regarded as linear complexity $O ( N \cdot l )$ . By concentrating computational overhead solely on the steganographic path, this method significantly improves the overall eficiency of the framework and efectively performs recursive pruning of irrelevant branches in the semantic space.

## 3.4 Global Resynchronization

Subspace Sampling. During clustering, the discrete distribution of samples makes it impossible to partition the semantic space perfectly evenly, so the number of samples in each subspace is usually diferent. If the subspaces $\{ V _ { 1 } , V _ { 2 } , . . . , V _ { k } \}$ are encoded in simple sequential order, the secret-driven selection will bias the semantic distribution of the output sentences away from the natural distribu tion, introducing security risks. To eliminate this bias, we adopt the SparSamp [26] approach—message-driven pseudo-random number—for subspace sampling.

![](images/afb6a874e30ade35f9f232916c8272db182b2bf1b7cf2cf5e9185505e7809a88.jpg)  
Figure 3: An example of bit-slippage. Due to a local decoding error, the subsequent extracted bit sequence is out of sync with the embedded bits.

The construction of the semantic space and the procedure of HCM remain unchanged. Let the subspaces obtained after the �-th layer partition driven by the pseudo-random number $r _ { c }$ be $C _ { r _ { c } } ( V ^ { ( t ) } ) \stackrel { - } { = } \{ V _ { 1 } ^ { ( t ) } , V _ { 2 } ^ { ( t ) } , . . . , V _ { k } ^ { ( t ) } \}$ , where $\begin{array} { r } { V ^ { ( t ) } = \sum _ { i = 1 } ^ { k } V _ { i } ^ { ( t ) } } \end{array}$ . The cumulative probability distribution of the samples is then:

$$
F ^ {(t)} (j) = \sum_ {i = 1} ^ {j} \frac {| V _ {i} ^ {(t)} |}{| V ^ {(t)} |},\tag{6}
$$

where $j \in \{ 0 , 1 , . . . , k \}$ . If � secret bits $m ( t ) \in \{ 0 , 1 \} ^ { b }$ are to be embedded in this layer, we partition the probability interval $[ 0 , 1 )$ uniformly with the minimum granularity $\delta = 1 / 2 ^ { b }$ , yielding $2 ^ { b }$ equally wide intervals whose starting positions are $x _ { i } = i \cdot \delta ,$ where $i \in \{ 0 , 1 , . . . , 2 ^ { b } - 1 \}$ . To simulate real random sampling and ensure reproducibility, we introduce a pseudo-random number $r _ { \Delta } \in [ 0 , 1 )$ derived from the shared key and construct the pseudo-random position:

$$
r (i) = \left(x _ {i} + r _ {\Delta}\right) \text {   mod   } 1,\tag{7}
$$

where $i \in \left\{ 0 , 1 , . . . , 2 ^ { b } - 1 \right\}$ . Let �<sup>∗</sup> = ���(�(�)) be the decimal value of the secret bits. The subspace selected for the next layer is given by the inverse CDF:

$$
V ^ {(t + 1)} = V _ {j ^ {*}} ^ {(t)},\tag{8}
$$

$$
j ^ {*} = \operatorname * {a r g m i n} _ {j} \left\{F ^ {(t)} (j) \geq r \left(i ^ {*}\right) \right\}.\tag{9}
$$

If there are two or more pseudo-random positions corresponding to the target subspace $V ^ { ( t + \bar { 1 } ) }$ , no message is embedded in this layer. This phenomenon is known as a message conflict.

Global Resynchronization Mechanism. After being subjected to a perturbation, there is a small probability that the receiver will incorrectly predict the cluster to which a sentence belongs, thereby extracting an incorrect secret message. More seriously, however, because the internal spatial structures of diferent clusters vary, the frequency of message conflicts also difers. This may cause the length of the bits extracted from that sentence to difer from the original bits, leading to misalignment in the subsequent bit sequence and significantly increasing the error rate. Figure 3 illustrates an example of bit-slippage.

![](images/80e42522e739e6aa604f54f16f3c2f507561e6a600c3c043c71931a41c8d4651.jpg)  
Figure 4: An example of GRM. The green arrow indicates that the clustering is correct, and the red arrow indicates that the clustering is wrong.

To address this issue, we propose a Global Resynchronization Mechanism (GRM) based on LT codes to dynamically align the extracted bit positions and decouple local extraction failures from global message recovery.

During embedding, we let the length of each symbol block of the LT codes be fixed to the single-layer embedding capacity � and standardize the number of layers for each sentence clustering to �. The LT encoder can generate an unbounded checksum stream $C =$ $\{ c _ { 1 } , c _ { 2 } , \ldots \}$ , where each symbol $c _ { i } \in \{ 0 , 1 \} ^ { b }$ represents a complete LT-encoded symbol block. Each layer carries exactly at most one symbol block. If the subspace sampling at layer $j$ of sentence � does not trigger a conflict, the corresponding symbol block $B _ { i b + j }$ is embedded into that layer. Otherwise, the layer is skipped and the symbol block $B _ { ( i - 1 ) l + j }$ is not embedded. For the �-th sentence, the symbol blocks are preassigned to the interval [(�−1)�+1, ��] globally, where missing symbol blocks are treated as natural erasures.

During extracting, the same decoding procedure is applied to the received sentence $s ^ { \prime } { : }$ If the subspace sampling at layer � of sentence � does not trigger a conflict, the corresponding symbol block $B _ { i b + j } ^ { \prime }$ is extracted; Otherwise, the layer is skipped and $B _ { i b + j } ^ { \prime }$ is none. Due to clustering errors or message conflicts, symbol blocks may not be successfully recovered from sentence $s ^ { \prime }$ that matches the one from the embedding stage. All extracted symbol blocks are subsequently reorganized into a global verification stream $C ^ { \prime }$ according to their predefined ESIs. Once the total number of collected symbols exceeds the LT decoding threshold, the original secret message can be reconstructed in a single decoding step. In this manner, local layer-level deviations are isolated at the sentence level, preventing error propagation across bits and significantly enhancing the robustness of the steganographic system.

Figure 4 illustrates an example of GRM when � = 3 and $l = 3$ After being attacked, the sentence $s _ { 2 } ^ { \prime }$ is unfortunately divided into the wrong subspace, and the involved symbol blocks is wrongly extracted. Because LT codes with a certain degree of redundancy possess inherent robustness, the correct message can still be recov ered even if some symbol blocks are missing.

## 4 Experiment

## 4.1 Implementation Details

Setup. We select the general text-embedding model Sentence-T5- Large [13] optimized by T5 model as the sentence-vector encoder. We retrieve and generate texts on PersonaChat [39] corpus. For HCM, we set the number of layers � to 3 and the number of clusters per layer � to 8. For decoding, we use the BP decoding algorithm. Baselines. We select AC [43], ADG [40], Discop [4], SECC [5], STEAD [19] and FSBTS [32] as the baseline methods. STEAD adopts Dream-7B [35] and the rest adopt GPT-2 [20]. FSBTS uses openCon cepts [38] as its dataset, while other methods randomly select texts from the PersonaChat corpus as inputs for text generation tasks.

## 4.2 Metrics

Robustness. In order to demonstrate the robustness, we test the extraction error rate $P _ { E }$ of stegos after five types of textual attacks. In the actual extraction process, the damage of secret information is mainly manifested in two physical forms: fragment loss and extrac tion error. According to information theory, the mutual information provided by the completely lost bits is 0, which is equivalent to the random guess of equal probability (i.e. the error rate is 0.5) at the receiver in the binary channel. Therefore, we use the full prob ability formula to convert the bit loss rate (BLR) of the extracted message and the bit error rate (BER) of the extracted message into the equivalent comprehensive bit error rate $P _ { E } \mathbf { ; }$

$$
P _ {E} = (1 - B L R) * B E R + 0. 5 * B L R.\tag{10}
$$

The types of text attacks we use include: deletion, replacement, insertion, swap and paraphrase. We use Parrot\_Paraphraser [3] model to implement the paraphrase operation. Among them, para phrase belongs to sentence-level attacks, and other attack types belong to word-level attacks. For word-level attacks, we set the ratio of the attacked words to the total number of words in a sample as �, which can be regarded as the attack intensity.

Quality of Stegos. We use Perplexity (PPL) of the model DialoGPTmedium [41] as the index to evaluate the quality of steganogra phy. PPL measures the instability of an LLM in predicting text sequences and represents the fluency of texts. The smaller the PPL, the smoother the stegos and the better the concealment. Since the dataset of FSBTS is fixed, it is not included in the evaluation.

Embedding Capacity. The ultimate transmission rate for reliable, error-free communication over a memoryless binary channel is bounded by the channel capacity [22]. The channel uncertainty induced by the composite error rate $P _ { E }$ is formulated by the binary entropy function $H _ { 2 } ( P _ { E } ) = - P _ { E } \log _ { 2 } ( P _ { E } ) - ( 1 - P _ { E } ) \log _ { 2 } ( 1 - P _ { E } )$ At the theoretical limit, $H _ { 2 } ( P _ { E } )$ represents the minimum propor tion of redundant parity bits inherently required to correct channel noise. Conversely, the term $\left[ 1 - H _ { 2 } ( P _ { E } ) \right]$ represents the capacity factor, which is the fraction genuinely available for carrying the useful payload after deducting the error-correction overhead. Consequently, the actual Efective Embedding Rate (EER) is computed as $\mathrm { E E R } = \left( 1 - H _ { 2 } ( P _ { E } ) \right) * \mathrm { E R }$ , where ER denotes the raw embedding capacity. $A s ~ P _ { E }$ approaches 50% and $\left[ 1 - H _ { 2 } ( P _ { E } ) \right]$ approaches 0, more redundant codes need to be introduced, resulting in less EER. We conducted tests with $\alpha = 5$ , as a representative value for moderate intensity. Under this condition, all methods functioned properly, and there were significant diferences in terms of robustness. Through numerous experiments, we have found that the relevant conclusions hold true for other values of � as well. Security. We use five steganalysis strategies—FCN [33], R-BiLSTM-C [14], LSTMATT [44], SANet [31] and HiDuNet [17]—to test security of stegos. The closer the accuracy of steganalysis to 50%, the better the concealment and the securer the stegos. Since there is no comparable cover text for FSBTS, it is not included in the evaluation.

Table 1: Robustness against paraphrase attack.

<table><tr><td>Method</td><td>AC</td><td>ADG</td><td>SECC</td><td>Discop</td><td>STEAD</td><td>FSBTS</td><td>Ours</td></tr><tr><td>BER</td><td>0.6145</td><td>0.3933</td><td>0.5500</td><td>-</td><td>-</td><td>0.1090</td><td>0.0038</td></tr><tr><td>BLR</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0.2681</td><td>0</td></tr><tr><td> $P_E$ </td><td>0.6145</td><td>0.3933</td><td>0.5500</td><td>0.5000</td><td>0.5000</td><td>0.2138</td><td>0.0038</td></tr></table>

Table 2: Comparison of PPL.

<table><tr><td rowspan="2">Method</td><td colspan="3">Dataset</td></tr><tr><td>PersonaChat</td><td>C4</td><td>IMDB</td></tr><tr><td>AC</td><td>112.70</td><td>157.78</td><td>213.95</td></tr><tr><td>ADG</td><td>127.24</td><td>398.31</td><td>394.51</td></tr><tr><td>ADG+SECC</td><td>125.16</td><td>390.18</td><td>431.72</td></tr><tr><td>Discop</td><td>109.34</td><td>193.18</td><td>176.15</td></tr><tr><td>STEAD</td><td>128.55</td><td>94.07</td><td>291.76</td></tr><tr><td>Ours</td><td>53.85</td><td>43.21</td><td>41.52</td></tr></table>

Table 3: Embedding capacity when $\alpha = 5 .$ The $\bf { \omega } ^ { \omega \alpha }$ (P/C/I)” column represents the result of the stegos of our method on PersonaChat/C4/IMDB.

<table><tr><td>Method</td><td>AC</td><td>ADG</td><td>ADG+SECC</td><td>Discop</td><td>STEAD</td><td>FSBTS</td><td>Ours (P/C/I)</td></tr><tr><td> $P_{E}$ </td><td>0.4001</td><td>0.3852</td><td>0.4938</td><td>0.2856</td><td>0.4204</td><td>0.0438</td><td>0.0038</td></tr><tr><td> $H_{2}$ </td><td>0.971</td><td>0.958</td><td>1</td><td>0.863</td><td>0.977</td><td>0.0259</td><td>0.036</td></tr><tr><td>ER (bit/token)</td><td>2.47</td><td>1.36</td><td>0.45</td><td>0.43</td><td>0.08</td><td>0.48</td><td>0.14/0.08/0.07</td></tr><tr><td>EER (bit/token)</td><td>0.07</td><td>0.06</td><td>0.00</td><td>0.06</td><td>0.00</td><td>0.36</td><td>0.13/0.08/0.07</td></tr></table>

## 4.3 Results

Robustness. Figure 6 shows the robust performance of diferent methods under diferent word-level attack types with diferent attack intensities. Our method sets the redundancy of LT code to three times. It can be seen that the baseline methods are quite vulnerable to word-level attacks, and their $P _ { E }$ increase as the attacks become stronger, tending to be 50% of random guess. In contrast, the $P _ { E }$ of our proposed method remains below 2.7%, achieved A significant improvement compared to the baseline methods.

Figure 5 illustrates the performance of various methods in terms of BER, BLR, and $P _ { E }$ under diferent types of attacks when � = 5. Based on the results, we can thoroughly analyze the primary factors contributing to the extraction errors for each method. First, the $P _ { E }$ of AC and ADG is dominated by BER, as assigning default values to undecodable tokens converts potential loss into extrac tion errors. Although ADG extracts suficient blocks for SECC to achieve a 0 BLR, its high inherent symbol error rate causes SECC’s error correction to fail, yielding a BER near 50%. Conversely, our method shares $\operatorname { S E C C } { \boldsymbol { s } }$ BLR mechanism but ensures highly accurate symbol extraction via resynchronization and semantic space stabil ity. This successfully averts SECC’s decoding failure, maintaining exceptionally low BER and $P _ { E }$ under various attacks. Second, the $P _ { E }$ of Discop and STEAD is predominantly driven by BLR, because they halt decoding at undecodable tokens, converting potential errors into message loss. Notably, Discop’s apparent error rate is artificially lowered by its zero-padding strategy, as these padded sequences are excluded from actual BLR calculations.

![](images/b869dbb7c3f9642e00af236d0d58887782d116ae63f4c5e33d647df661c61264.jpg)  
Figure 5: The specific robustness performance of diferent methods under diferent attack types when $\alpha { = } 5 .$

Table 4: Anti-steganalysis comparison. The ADG results are the same whether or not SECC error correction is added.

<table><tr><td>Method</td><td>FCN</td><td>R-BiLSTM-C</td><td>LSTMATT</td><td>SANet</td><td>HiDuNet</td></tr><tr><td>AC</td><td>65.10%</td><td>59.56%</td><td>59.75%</td><td>77.58%</td><td>74.00%</td></tr><tr><td>ADG(+SECC)</td><td>58.30%</td><td>56.93%</td><td>53.82%</td><td>90.67%</td><td>96.33%</td></tr><tr><td>Discop</td><td>52.70%</td><td>56.90%</td><td>53.92%</td><td>90.67%</td><td>92.71%</td></tr><tr><td>STEAD</td><td>55.56%</td><td>54.44%</td><td>52.22%</td><td>52.54%</td><td>93.33%</td></tr><tr><td>Ours</td><td>50.54%</td><td>49.60%</td><td>50.63%</td><td>53.43%</td><td>56.49%</td></tr></table>

Table 1 shows the robustness performance of diferent methods under paraphrase attack. It can be clearly seen that the baseline methods are also vulnerable to sentence-level attack, with Discop and STEAD completely unable to decode the attacked stegos, while our method still has strong robustness and significant advantages.

Among all attacks, the ER is slightly higher for replacement and deletion attacks on our system, as these operations may alter semantic keywords, causing the prediction to fail to be assigned to the correct cluster.

Quality of Stegos. Table 2 shows the PPL metrics of diferent meth ods on three datasets: PersonaChat [39], C4 [21], and IMDB [11]. By selecting natural sentences directly from the corpus, our method preserves the original linguistic distribution and fluency, achieving significantly lower PPL compared to generative methods.

Embedding Capacity. As shown in Table 3, we test the embedding capacity of diferent methods under mixed attacks (including all word-level attacks) when �=5. Our method sets the redundancy of

Table 5: The efect of the number of clusters � on robustness and capacity (� = 5).

<table><tr><td>k</td><td> $P_{ED}$ </td><td> $P_{ER}$ </td><td> $P_{EI}$ </td><td> $P_{ES}$ </td><td> $P_{EP}$ </td><td>ER</td></tr><tr><td>2</td><td>0.0038</td><td>0.0132</td><td>0</td><td>0</td><td>0</td><td>0.0299</td></tr><tr><td>4</td><td>0.0132</td><td>0.0225</td><td>0</td><td>0.0019</td><td>0</td><td>0.0667</td></tr><tr><td>8</td><td>0.0188</td><td>0.0263</td><td>0.0038</td><td>0.0038</td><td>0.0038</td><td>0.1295</td></tr><tr><td>16</td><td>0.2876</td><td>0.1147</td><td>0.3214</td><td>0.3195</td><td>0.3214</td><td>0.1338</td></tr></table>

Table 6: Ablation study of HCM. We test the eficiency under diferent numbers of clustering layers.

<table><tr><td>Number of Layers</td><td>Encoding Rate(s/bit)</td><td>Encoding Rate(s/layer)</td><td>Decoding Rate(s/bit)</td><td>Decoding Rate(s/layer)</td></tr><tr><td>1</td><td>20.96</td><td>167.71</td><td>10.75</td><td>85.96</td></tr><tr><td>2</td><td>1.37</td><td>5.48</td><td>1.17</td><td>4.67</td></tr><tr><td>3</td><td>1.52</td><td>4.61</td><td>1.49</td><td>4.47</td></tr><tr><td>4</td><td>2.18</td><td>1.09</td><td>2.11</td><td>1.06</td></tr></table>

Table 7: Capacity under diferent redundancy levels for deletion attack (� = 5).

<table><tr><td> $R_{LT}$ </td><td>1.5×</td><td>2×</td><td>2.5×</td><td>3×</td></tr><tr><td>ER(bit/token)</td><td>0.2552</td><td>0.1925</td><td>0.1598</td><td>0.1338</td></tr></table>

LT code to three times. Although our method ofers no advantage in ER under lossless transmission, its EER in the attack scenario outperforms that of other methods except FSBTS, which employs a larger dataset than ours. In addition to the comparison with the baseline methods, we test the embedding capacity of the proposed method on the same three datasets as mentioned above. It is clear that the ER of the stego texts in PersonaChat is higher, as the average length of its sentences is significantly shorter than that of the other two datasets.

Security. Table 4 shows that the detection accuracy of our proposed method is close to 50%, which shows that the performance of steganalysis methods is not better than random guess when detecting the stegos generated by our method, thus verifying the security of our method.

![](images/7963eaa3ae3ac398d80e09f3d36b2dc1499f67c61caddfc9d88c53ad0397faca.jpg)  
Figure 6: Robustness against word-level attacks. � represents the ratio of the attacked words to the total number of words in a sample.

![](images/5bdcd5544bc3e8742ae12c928fb1b5434e6455c733c0e1cfb4faeb68a53875c6.jpg)  
Figure 7: Ablation study of GRM. We test the BER of systems without GRM and systems with GRM combined with LT codes at diferent redundancy levels under various types of attacks of varying intensity.

## 4.4 Ablation Study

Number of Clusters. We test how the system’s robustness and embedding capacity vary with diferent cluster sizes �. Columns 2 through 6 represent the $P _ { E }$ values under deletion, replacement, insertion, swap, and paraphrase attacks, respectively. Table 5 shows that as � increases, $P _ { E }$ exhibits an upward trend, indicating that this reduces the size of the subspace, thereby making extraction errors more likely to occur. In addition, an increase in � also increases the codable entropy and improves the embedding rate (ER).

Hierarchical Clustering Mechanism (HCM). We test the time consumption with diferent number of levels. Table 6 shows that, compared with the single-layer flat structure, the introduction of HCM greatly reduces the single clustering time and achieves an order of huge improvement in eficiency. When the number is 2, the system reaches the eficiency inflection point; When the number continue to increase, time spent on each level falls, but the crosslayer scheduling overhead caused by multi-layer begins to exceed the benefit, resulting in a rebound in the overall time per bit.

Global Resynchronization Mechanism (GRM). As illustrated in Figure 7, the performance drops significantly without GRM module. The system with GRM achieves an extremely low BER, but the BER increases slightly when LT codes are added. This is because GRM converts error bits into lost bits, whereas LT’s redundancy coding converts them back into fewer error bits. This verifies the inherent robustness of semantic-space steganography and confirms that bitslippage, rather than semantic distortion, is the predominant factor behind decoding failure in the baseline system. In addition, the BER decreases consistently as the redundancy of LT codes increases. While 2× redundancy keeps the BER below 10%, it still exhibits an error floor. In contrast, the 3× configuration achieves near-perfect reconstruction across all attack types and intensities. The system maintains consistent robustness across four types of attacks.

Furthermore, as shown in Table 7, as the redundancy of the LT code increases, the amount of actual secret messages embedded decreases, and the ER shows a downward trend. This illustrates the trade-of between robustness and embedding capacity.

## 5 Conclusion

This paper proposes a robust coverless linguistic steganography framework that operates in the sentence embedding space rather than the fragile token space. By leveraging the semantic invariance of sentence representations, our method inherently absorbs wordand sentence-level textual perturbations. We introduce HCM to eficiently partition the semantic space and GRM to resolve the critical bit-slippage problem through LT codes. Experimental results demonstrate that our approach achieves substantial improvements in robustness, while maintaining efective embedding capacity, superior linguistic quality, and strong security against steganalysis.

## References

[1] Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. 2024. Bge m3-embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation. arXiv preprint arXiv:2402.03216 4, 5 (2024).

[2] Yanli Chen, Hongxia Wang, Hanzhou Wu, Zhiqiang Wu, Tao Li, and Asad Malik. 2019. Adaptive video data hiding through cost assignment and STCs. IEEE Transactions on Dependable and Secure Computing 18, 3 (2019), 1320–1335.

[3] Prithiviraj Damodaran. 2021. Parrot: Paraphrase generation for NLU.

[4] Jinyang Ding, Kejiang Chen, Yaofei Wang, Na Zhao, Weiming Zhang, and Neng hai Yu. 2023. Discop: Provably secure steganography in practice based on" distribution copies". In 2023 IEEE Symposium on Security and Privacy (SP). IEEE 2238–2255.

[5] Yuzhe Guo, Zhongliang Yang, Zhuang Wang, Zhili Zhou, and Linna Zhou. 2025. SECC-Stega: Generative Linguistic Steganographic Framework Based on Error Correcting Codes. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 1–5.

[6] Yuting Hu, Haoyun Li, Jianni Song, and Yongfeng Huang. 2020. MM-stega: multi modal steganography based on text-image matching. In International Conference on Artificial Intelligence and Security. Springer, 313–325.

[7] Gabriel Kaptchuk, Tushar M Jois, Matthew Green, and Aviel D Rubin. 2021. Meteor: Cryptographically secure steganography for realistic distributions. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. 1529–1548.

[8] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick SH Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. Dense Passage Retrieval for Open-Domain Question Answering.. In EMNLP (1). 6769–6781.

[9] Yi Long and Yuling Liu. 2018. Text coverless information hiding based on word2vec. In International Conference on Cloud Computing and Security. Springer, 463–472.

[10] Michael Luby. 2002. LT codes. In The 43rd Annual IEEE Symposium on Foundations ofComputer Science, 2002. Proceedings. IEEE Computer Society, 271–271.

[11] Andrew Maas, Raymond E Daly, Peter T Pham, Dan Huang, Andrew Y Ng, and Christopher Potts. 2011. Learning word vectors for sentiment analysis. In Proceedings of the 49th annual meeting of the association for computational linguistics: Human language technologies. 142–150.

[12] Tomas Mikolov, Kai Chen, Greg Corrado, and Jefrey Dean. 2013. Eficient estimation of word representations in vector space. arXiv preprint arXiv:1301.3781 (2013).

[13] Jianmo Ni, Gustavo Hernandez Abrego, Noah Constant, Ji Ma, Keith Hall, Daniel Cer, and Yinfei Yang. 2022. Sentence-t5: Scalable sentence encoders from pre trained text-to-text models. In Findings ofthe association for computational linguistics: ACL 2022. 1864–1874.

[14] Yan Niu, Juan Wen, Ping Zhong, and Yiming Xue. 2019. A hybrid R-BILSTM-C neural network based text steganalysis. IEEE Signal Processing Letters 26, 12 (2019), 1907–1911.

[15] Chao Pan, Donghui Hu, Yaofei Wang, Kejiang Chen, Yinyin Peng, Xianjin Rong, Chen Gu, and Meng Li. 2025. Rethinking Prefix-Based Steganography for En hanced Security and Eficiency. IEEE Transactions on Information Forensics and Security (2025).

[16] Kaiyi Pang, Minhao Bai, Jinshuai Yang, Wei-Qiang Zhang, Minghu Jiang, and Yongfeng Huang. 2025. WinStega: An Adaptive Robust Enhancement Framework for Generative Linguistic Steganography. In ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 1–5.

[17] Wanli Peng, Sheng Li, Zhenxing Qian, and Xinpeng Zhang. 2023. Text steganal ysis based on hierarchical supervised learning and dual attention mechanism. IEEE/ACM Transactions on Audio, Speech, and Language Processing 31 (2023), 3513–3526.

[18] Yuang Qi, Kejiang Chen, Kai Zeng, Weiming Zhang, and Nenghai Yu. 2024. Provably secure disambiguating neural linguistic steganography. IEEE Transactions on Dependable and Secure Computing (2024).

[19] Yuang Qi, Na Zhao, Qiyi Yao, Benlong Wu, Weiming Zhang, Nenghai Yu, and Kejiang Chen. 2025. STEAD: Robust Provably Secure Linguistic Steganography with Difusion Language Model. In The Thirty-ninth Annual Conference on Neural Information Processing Systems.

[20] Alec Radford, Jefrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language models are unsupervised multitask learners. OpenAI blog 1, 8 (2019), 9.

[21] Colin Rafel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2020. Exploring the limits of transfer learning with a unified text-to-text transformer. Journal ofmachine learning research 21, 140 (2020), 1–67.

[22] Claude E Shannon. 1948. A mathematical theory of communication. The Bell system technical journal 27, 3 (1948), 379–423.

[23] Jianlin Su, Jiarun Cao, Weijie Liu, and Yangyiwen Ou. 2021. Whitening sentence representations for better semantics and faster retrieval. arXiv preprint arXiv:2103.15316 (2021).

[24] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023. Llama: Open and eficient foundation language models. arXiv preprint arXiv:2302.13971 (2023).

[25] Kaixi Wang and Quansheng Gao. 2019. A coverless plain text steganography based on character features. IEEE Access 7 (2019), 95665–95676.

[26] Yaofei Wang, Gang Pei, Kejiang Chen, Jinyang Ding, Chao Pan, Weilong Pang, Donghui Hu, and Weiming Zhang. 2025. {SparSamp}: Eficient Provably Secure Steganography Based on Sparse Sampling. In 34th USENIX Security Symposium (USENIX Security 25). 6817–6835.

[27] Alex Wilson and Andrew D Ker. 2016. Avoiding detection on twitter: embedding strategies for linguistic steganography. Electronic Imaging 28 (2016), 1–9.

[28] Han-Zhou Wu, Yun-Qing Shi, Hong-Xia Wang, and Lin-Na Zhou. 2016. Separable reversible data hiding for encrypted palette images with color partitioning and flipping verification. IEEE transactions on circuits and systems for video technology 27, 8 (2016), 1620–1631.

[29] Junqi Wu, Bolin Chen, Weiqi Luo, and Yanmei Fang. 2020. Audio steganography based on iterative adversarial attacks against convolutional neural networks. IEEE transactions on information forensics and security 15 (2020), 2282–2294.

[30] Zhengxian Wu, Juan Wen, Yiming Xue, Ziwei Zhang, and Yinghan Zhou. 2024. GTSD: Generative Text Steganography Based on Difusion Model. In International Conference on Neural Information Processing. Springer, 168–183.

[31] Yiming Xue, Jiaxuan Wu, Ronghua Ji, Ping Zhong, Juan Wen, and Wanli Peng. 2023. Adaptive domain-invariant feature extraction for cross-domain linguistic steganalysis. IEEE Transactions on Information Forensics and Security 19 (2023), 920–933.

[32] Jinshuai Yang, Minghao Bai, Kaiyi Pang, Yue Gao, Jiajun Zou, and Yongfeng Huang. 2025. A Novel Framework of Semantic-Based Text Steganography. IEEE Transactions on Dependable and Secure Computing (2025).

[33] Zhongliang Yang, Yongfeng Huang, and Yu-Jin Zhang. 2019. A fast and eficient text steganalysis method. IEEE Signal Processing Letters 26, 4 (2019), 627–631.

[34] Zhong-Liang Yang, Xiao-Qing Guo, Zi-Ming Chen, Yong-Feng Huang, and Yu-Jin Zhang. 2018. RNN-stega: Linguistic steganography based on recurrent neural networks. IEEE Transactions on Information Forensics and Security 14, 5 (2018), 1280–1295.

[35] Jiacheng Ye, Zhihui Xie, Lin Zheng, Jiahui Gao, Zirui Wu, Xin Jiang, Zhenguo Li, and Lingpeng Kong. 2025. Dream 7b: Difusion large language models. arXiv preprint arXiv:2508.15487 (2025).

[36] Biao Yi, Hanzhou Wu, Guorui Feng, and Xinpeng Zhang. 2022. ALiSa: Acrostic linguistic steganography based on BERT and Gibbs sampling. IEEE Signal Processing Letters 29 (2022), 687–691.

[37] Jianjun Zhang, Yicheng Xie, Lucai Wang, and Haijun Lin. 2017. Coverless text information hiding method using the frequent words distance. In International Conference on Cloud Computing and Security. Springer, 121–132.

[38] Ningyu Zhang, Qianghuai Jia, Shumin Deng, Xiang Chen, Hongbin Ye, Hui Chen, Huaixiao Tou, Gang Huang, Zhao Wang, Nengwei Hua, et al. 2021. Alicg: Fine-grained and evolvable conceptual graph construction for semantic search at alibaba. In Proceedings of the 27th ACM SIGKDD conference on knowledge discovery & data mining. 3895–3905.

[39] Saizheng Zhang, Emily Dinan, Jack Urbanek, Arthur Szlam, Douwe Kiela, and Jason Weston. 2018. Personalizing dialogue agents: I have a dog, do you have pets too? arXiv preprint arXiv:1801.07243 (2018).

[40] Siyu Zhang, Zhongliang Yang, Jinshuai Yang, and Yongfeng Huang. 2021. Provably secure generative linguistic steganography. arXiv preprint arXiv:2106.02011 (2021).

[41] Yizhe Zhang, Siqi Sun, Michel Galley, Yen-Chun Chen, Chris Brockett, Xiang Gao, Jianfeng Gao, Jingjing Liu, and William B Dolan. 2020. Dialogpt: Large-scale generative pre-training for conversational response generation. In Proceedings of the 58th annual meeting of the association for computational linguistics: system demonstrations. 270–278.

[42] Xuejing Zhou, Wanli Peng, Boya Yang, Juan Wen, Yiming Xue, and Ping Zhong. 2021. Linguistic steganography based on adaptive probability distribution. IEEE Transactions on Dependable and Secure Computing 19, 5 (2021), 2982–2997.

[43] Zachary Ziegler, Yuntian Deng, and Alexander M Rush. 2019. Neural linguistic steganography. In Proceedings ofthe 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). 1210–1215.

[44] Jiajun Zou, Zhongliang Yang, Siyu Zhang, Sadaqat ur Rehman, and Yongfeng Huang. 2020. High-performance linguistic steganalysis, capacity estimation and steganographic positioning. In International Workshop on Digital Watermarking. Springer, 80–93.
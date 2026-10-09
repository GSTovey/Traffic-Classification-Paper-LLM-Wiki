# Exact Second-Order Asymptotics for Covert Communication over DMCs with Variational Distance Constraints

Qiaosheng Zhang, Lin Zhou, Member, IEEE, and Xuelong Li, Fellow, IEEE

## Abstract

We determine the exact second-order asymptotics of covert communication over binary-input discrete memoryless channels when covertness is measured by variational distance. Previous work by Tahmasbi and Bloch [IEEE Trans. Inf. Theory, Apr. 2019] characterized the first-order asymptotics and derived achievability and converse bounds on the second-order term, but these bounds do not match. The gap arises from an additional penalty of order $n ^ { 1 / 4 }$ in the achievability bound. We show that this penalty can be removed through a sharper analysis of the distribution of the warden’s output induced by pulse-position modulation. Specifically, we express the variational distance through the Bhattacharyya coefficient of two distributions and the expectation of a continuous function of the log-likelihood ratio. Because the resulting expectation involves a continuous function rather than the probability of a likelihoodratio event, an analysis of the characteristic function combined with a Gaussian smoothing argument reduces the approximation error from $O ( n ^ { - 1 / 4 } )$ (derived from the Berry–Esseen bound in prior work) to $O ( n ^ { - 1 / 2 } )$ . With this better controlled approximation error, we manage to derive a matching achievability result to the existing converse result, thus establishing the exact second-order asymptotics

## Index Terms

Covert communication, second-order asymptotics, variational distance, pulse-position modulation.

## I. INTRODUCTION

Covert communication considers the situation in which a transmitter communicates reliably with a legitimate receiver while concealing the presence of communication from a warden. Since the square-root law was formalized for additive white Gaussian noise channels in [1], the information-theoretic limits of covert communication have been progressively characterized for binary symmetric channels [2], [3], discrete memoryless channels (DMCs) [4], [5], classical-quantum channels [6], [7], multiple-access channels [8], [9], broadcast channels [10]–[12], channels with state [13], adversarial channels [14], MIMO AWGN channels [15], [16] and continuous-time channels subject to spectral constraints [17]. These studies show, under the usual non-degeneracy conditions, that only $O ( { \sqrt { n } } )$ information bits can be communicated reliably and covertly over n channel uses, and also identify the exact preconstant before ${ \sqrt { n } } ,$ which is commonly referred to as the covert capacity. For the binary-input DMC considered here, pulse-position modulation (PPM) provides a structured signaling mechanism that attains the optimal first-order scaling [18].

The finite blocklength behavior is less completely understood. For binary-input DMCs, Tahmasbi and Bloch [19] developed a unified second-order analysis under maximum probability of error for three covertness metrics: KL divergence, variational distance, and the probability of missed detection at a fixed probability of false alarm. Their achievability part, for all the three metrics, relies on a random coding argument with the PPM scheme [18]. When covertness is measured by KL divergence, their achievability and converse bounds match up to the second term in the order of $n ^ { 1 / 4 }$ , yielding exact second-order asymptotics. For the other two measures including variation distance, the authors of [19] identified the exact first-order term, of order $n ^ { 1 / 2 }$ , but the corresponding achievability and converse bounds differ for the second-order term scaling in the order of $n ^ { 1 / 4 }$ . Consequently, the exact second-order asymptotics remained open for these two covertness metrics.

In particular, variational distance has been widely adopted as a covertness metric in the literature, including in pioneering works such as [1], [2], because it has a direct operational interpretation in terms of the false-alarm and missed-detection probabilities of the warden’s hypothesis test. A standard binary hypothesis testing argument shows that, when the variational distance is small, the sum of the false-alarm and missed-detection probabilities remains close to one even when the warden Willie uses optimal detectors.

The objective of this work is to establish the exact second-order asymptotics for covert communication under the variational distance metric. We show that the achievable second-order term attained by pulse-position modulation (PPM) [18] coincides with the converse term established in [19], hence deriving the exact second-order asymptotics. The coding scheme remains unchanged from that work; the improvement lies entirely in a sharper analysis of the output distributions induced at the warden when the legitimate transmitter transmits or not. The proof of [19, Lemma 8] applies the Berry–Esseen theorem separately to two likelihood-ratio events, resulting in an approximation error of order $\ell ^ { - 1 / 2 }$ , where ℓ denotes the number of PPM pulses. Since $\ell = \Theta ( { \sqrt { n } } )$ , this error is of order $n ^ { - 1 / 4 }$ . To ensure that the covertness constraint is met despite an error of this scale, the number of pulses must be reduced by at least $\Theta ( n ^ { 1 / 4 } )$ . Since the leading term of the logarithm of the achievable message size is proportional to $\ell ,$ reducing $\Theta ( n ^ { 1 / 4 } )$ pulses reduces the logarithm of the message size by $\Theta ( n ^ { 1 / 4 } )$ , which is exactly the order of the second-order term. Therefore, the achievability bound fails to match the converse [19] at the second order.

Our analysis combines the two likelihood-ratio contributions at the level of their overlap before introducing a Gaussian approximation. We first use the elementary identity $\begin{array} { r } { 1 - \mathbb { V } ( P , Q ) = \sum } \end{array}$ min $\{ P ( z ) , Q ( z ) \}$ , and then rewrite the pointwise minimum in terms of the Bhattacharyya coefficient. This yields a midpoint representation of $1 - \mathbb { V } ( P , Q )$ as the product of the Bhattacharyya coefficient and the expectation of the continuous function $e ^ { - | x | / 2 }$ under a suitably defined midpoint distribution (see Lemma 1). The resulting expectation is analyzed through a characteristic-function analysis combined with Gaussian smoothing and an anti-concentration argument. These steps give an approximation error of order $O ( n ^ { - 1 / 2 } )$ . Since the Gaussian approximation depends on the normalized pulse count $\ell / { \sqrt { n } } ,$ an error of order $O ( n ^ { - 1 / 2 } )$ in the covertness expression can be compensated by changing $\ell / { \sqrt { n } }$ by $O ( n ^ { - 1 / 2 } )$ , which corresponds to an $O ( 1 )$ adjustment in ℓ. Such an adjustment does not affect the $n ^ { 1 / 4 }$ coefficient of the achievable message size. Consequently, the achievable second-order term coincides with the converse term.

The rest of this paper is organized as follows. Section II introduces the system model and states the main results. Section III establishes a sharp approximation, in variational distance, between the PPM-induced distribution of the warden’s output and the innocent output distribution. Section IV combines these approximations with the coding scheme of [19] to obtain the exact second-order asymptotics, and Section V concludes the paper.

![](images/323bbecc648cff26d8c21ba938ad35e2d1179db7baea0fca6615173970c3d931.jpg)  
Fig. 1: System model of covert communication over a binary-input DMC.

## II. MODEL AND MAIN RESULTS

## A. Notation

Random variables are denoted by upper-case letters, while their realizations are denoted by lower-case letters. Vectors are written in boldface. All logarithms and exponentials are natural. For integers $a \ \leq \ b ,$ let $[ [ a , b ] ] \triangleq$ $\{ a , a + 1 , \ldots , b \}$ . For real number $c \in \mathbb { R } .$ , let $[ c ] ^ { + } : = \operatorname* { m a x } \{ c , 0 \}$ . For probability mass functions P and Q on a finite alphabet X such that $P \ll Q$ , we define the KL divergence, variational distance, and chi-squared divergence, respectively, by

$$
\mathbb {D} (P \| Q) \triangleq \sum_ {x} P (x) \log \frac {P (x)}{Q (x)},
$$

$$
\mathbb {V} (P, Q) \triangleq \frac {1}{2} \sum_ {x} | P (x) - Q (x) |,
$$

$$
\chi_ {2} (P \| Q) \triangleq \sum_ {x} \frac {(P (x) - Q (x)) ^ {2}}{Q (x)}.
$$

## B. System Model

Let $\mathcal { X } = \{ 0 , 1 \}$ be the alphabet for channel input and $( { \mathcal { V } } , { \mathcal { Z } } )$ be two other finite alphabets. Let $W _ { Y | X } \in \mathcal { P } ( \mathcal { V } | \mathcal { X } )$ be a conditional distribution mapping from X to $\mathcal { V } ,$ and $W _ { Z | X } \in { \mathcal { P } } ( { \mathcal { Z } } | X )$ be a conditional distribution mapping from X to Z. We consider a transmitter communicating with a legitimate receiver over the binary-input DMC $( \mathcal { X } , W _ { Y | X } , \mathcal { Y } )$ , while a warden observes the channel input through a second DMC $( \mathcal { X } , W _ { Z | X } , \mathcal { Z } )$ . We refer to the tuple

$$
(\mathcal {X}, W _ {Y | X}, W _ {Z | X}, \mathcal {Y}, \mathcal {Z})
$$

as a binary-input covert communication channel (as illustrated in Fig. 1). The symbol 0 denotes the innocent symbol: when no communication happens, the transmitter sends the all-0 sequence. The symbol 1 denotes the non-innocent symbol used to convey information. The output distributions at the legitimate receiver and the warden induced by the two input symbols are denoted by

$$
P _ {0} (y) \triangleq W _ {Y | X} (y | 0), \qquad P _ {1} (y) \triangleq W _ {Y | X} (y | 1),
$$

and

$$
Q _ {0} (z) \triangleq W _ {Z | X} (z | 0), \quad Q _ {1} (z) \triangleq W _ {Z | X} (z | 1).
$$

Throughout the paper, we assume $Q _ { 1 } \ll Q _ { 0 } , Q _ { 1 } \neq Q _ { 0 }$ , and $P _ { 1 } \ll P _ { 0 }$ . The condition $Q _ { 1 } \ll Q _ { 0 }$ excludes symbols that reveal communication with positive probability after a single use, whereas $Q _ { 1 } \neq Q _ { 0 }$ excludes the degenerate case in which the warden obtains no statistical evidence of communication. The assumption $P _ { 1 } \ll P _ { 0 }$ rules out the regime in which the legitimate parties can achieve a throughput that breaks the square-root law [4], [5]. For simplicity, we write

$$
D _ {P} \triangleq \mathbb {D} (P _ {1} \| P _ {0}), \quad D _ {Q} \triangleq \mathbb {D} (Q _ {1} \| Q _ {0}), \quad V _ {P} \triangleq \operatorname{Var} _ {P _ {1}} \left[ \log \frac {P _ {1} (Y)}{P _ {0} (Y)} \right].
$$

We impose the usual non-degeneracy conditions $D _ { P } > 0$ and $V _ { P } > 0$

Definition 1. Let $M , K , n$ be three positive integers. An $( M , K , n )$ code contains an encoder and a decoder

$$
f: [   [ 1, K ]   ] \times [   [ 1, M ]   ] \longrightarrow \{0, 1 \} ^ {n}, \qquad \varphi : \mathcal {Y} ^ {n} \times [   [ 1, K ]   ] \longrightarrow [   [ 1, M ]   ].
$$

The message $W \in [ [ 1 , M ] ]$ and secret key $S \in [ [ 1 , K ]$ are independent and uniform on their respective sets. The induced distribution of the warden’s output, averaged over both message and key, satisfies that for each $\mathbf { z } \in \mathcal { Z } ^ { n }$

$$
\widehat {P} _ {Z ^ {n}} (\mathbf {z}) \triangleq \frac {1}{M K} \sum_ {s = 1} ^ {K} \sum_ {w = 1} ^ {M} W _ {Z | X} ^ {\otimes n} (\mathbf {z} | f (s, w)).
$$

The maximum probability of error is

$$
P _ {\text {err}} ^ {*} \triangleq \max _ {s \in [   [ 1, K ]   ], w \in [   [ 1, M ]   ]} \operatorname * {P r} \{\varphi (Y ^ {n}, s) \neq w \mid S = s, W = w \}.
$$

Definition 2. The code is ϵ-reliable if $P _ { \mathrm { e r r } } ^ { * } \leq \epsilon .$ . An ϵ-reliable code is an $( M , K , n , \epsilon , \delta ) _ { \mathbb { V } }$ code if

$$
\mathbb {V} (\widehat {P} _ {Z ^ {n}}, Q _ {0} ^ {\otimes n}) \leq \delta ,
$$

and is an $( M , K , n , \epsilon , \delta ) _ { \mathbb { D } }$ code if

$$
\mathbb {D} (\widehat {P} _ {Z ^ {n}} \| Q _ {0} ^ {\otimes n}) \leq \delta .
$$

Let $M _ { \mathbb { D } } ^ { * } ( n , \epsilon , \delta )$ and $M _ { \mathbb { V } } ^ { * } ( n , \epsilon , \delta )$ be the corresponding largest sizes of the message sets.

## C. Pulse-Position Modulation

Let m and ℓ be positive integers. A length-m, weight-one PPM block selects one coordinate uniformly over the m coordinates, transmits 1 in that coordinate, and transmits 0 elsewhere. The resulting distribution of the warden’s output is

$$
P _ {m} (\mathbf {z}) \triangleq \frac {1}{m} \sum_ {j = 1} ^ {m} Q _ {1} (z _ {j}) \prod_ {k \neq j} Q _ {0} (z _ {k}),
$$

Consider ℓ independent PPM blocks, and let the total blocklength $n = m \ell + r$ , where $0 \leq r < \ell .$ . Here, ℓ denotes the number of pulses (i.e., the number of ones in a codeword), and r denotes the number of trailing zeros appended after the ℓ blocks. We define the PPM-induced output distribution as

$$
P _ {Z, \mathrm{PPM}} ^ {n, \ell} \triangleq P _ {m} ^ {\otimes \ell} \otimes Q _ {0} ^ {\otimes r}.\tag{1}
$$

Let $c _ { 0 }$ and $c _ { 1 }$ be positive constants. The analysis in this work only considers the parameter regime

$$
0 <   c _ {0} \leq \frac {\ell}{m} \leq c _ {1} <   \infty ,\tag{2}
$$

since both ℓ and m scale as $\Theta ( { \sqrt { n } } )$ in the covert communication regime, as established in prior works [18], [19].

## D. Main Results And Discussions

For $x \in \mathbb { R }$ , let $\begin{array} { r } { Q ( x ) \triangleq \frac { 1 } { \sqrt { 2 \pi } } \int _ { x } ^ { \infty } e ^ { - u ^ { 2 } / 2 } d u } \end{array}$ denote the Gaussian Q-function. The following theorem provides the approximation of variational distance between the PPM-induced output distribution $P _ { Z , \mathrm { P P M } } ^ { n , \ell }$ and the innocent distributions $Q _ { 0 } ^ { \otimes n }$

Theorem 1 (Variational distance for the distribution induced by PPM). Suppose $n = m \ell + r$ such that $\begin{array} { r } { 0 < c _ { 0 } \le \frac { \ell } { m } \le c _ { 1 } < \infty } \end{array}$ and $0 \leq r < \ell .$ . Then, we have

$$
\mathbb {V} (P _ {Z, \mathrm{PPM}} ^ {n, \ell}, Q _ {0} ^ {\otimes n}) = 1 - 2 Q \left(\frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}}\right) + O (n ^ {- 1 / 2}).
$$

Remark 1. The approximation in Theorem 1 is sharper than the corresponding approximation in [19, Lemma 8, Eq. (136)], which has the same Gaussian leading term but contains the additional term $2 / { \sqrt { \ell } } ,$ together with an $O ( n ^ { - 1 / 2 } )$ error term. Since $\ell = \Theta ( { \sqrt { n } } )$ , the additional term is of order $n ^ { - 1 / 4 }$ . Theorem 1 removes this term by preserving the cancellation between the two likelihood-ratio contributions before applying the Gaussian approximation, and consequently yields a uniform error of order $O ( n ^ { - 1 / 2 } )$ . This allows us to obtain a tighter achievability bound that matches the converse bound of [19], as shown below.

After introducing Theorem 1, we are now ready to state the main result of this paper using the shorthand notation $\Gamma \triangleq Q ^ { - 1 } \left( \frac { 1 - \delta } { 2 } \right)$

Theorem 2 (Exact second-order asymptotics under variational distance). Fix $0 < \epsilon < 1$ . For every covertness parameter $0 < \delta < 1$

$$
\log M _ {\mathbb {V}} ^ {*} (n, \epsilon , \delta) = \frac {2 \Gamma D _ {P}}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}} n ^ {1 / 2} - \sqrt {\frac {2 \Gamma V _ {P}}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}} Q ^ {- 1} (\epsilon) n ^ {1 / 4} + O (\log n).\tag{3}
$$

Remark 2. Note that the right-hand side of (3) coincides with the converse bounds in [19, Eqs. (29)]. Therefore Theorem 2 completes the exact second-order characterization for the variational distance metric. Although the statement in Theorem 2 does not impose any constraint on the key size, the PPM random-coding construction in Section IV can be implemented with

$$
\log K = \frac {2 \Gamma}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}} [ D _ {Q} - D _ {P} ] ^ {+} n ^ {1 / 2} + o (n ^ {1 / 2}).
$$

In particular, no secret key is needed whenever $D _ { Q } < D _ { P }$ , i.e., whenever the warden’s channel is less informative than the legitimate parties’ channel.

Remark 3. The first- and second-order asymptotics under the KL-divergence metric were characterized in $I I 9 J$ as

$$
\log M _ {\mathbb {D}} ^ {*} (n, \epsilon , \delta) = \sqrt {\frac {2 \delta}{\chi_ {2} (Q _ {1} \| Q _ {0})}} D _ {P} n ^ {1 / 2} - \sqrt {\sqrt {\frac {2 \delta}{\chi_ {2} (Q _ {1} \| Q _ {0})}} V _ {P}} Q ^ {- 1} (\epsilon) n ^ {1 / 4} + O (\log n).
$$

This expression and (3) are both of the form $\ell D _ { P } - \sqrt { \ell V _ { P } } Q ^ { - 1 } ( \epsilon ) + { \cal O } ( \log n ) ,$ , where ℓ is the largest number of pulses imposed by the covertness constraint, that is, $\ell = \sqrt { 2 \delta n / \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) }$ under KL divergence and $\ell =$ $2 \Gamma \sqrt { n } / \sqrt { \chi _ { 2 } ( Q _ { 1 } \lVert Q _ { 0 } ) }$ under variational distance. The choice of covertness metric therefore affects only how the covertness parameter δ is converted into the largest number of pulses. Note that this differs qualitatively in the regime $\delta  0 ,$ where one has $\Gamma = \sqrt { \pi / 2 } \delta + O ( \delta ^ { 3 } )$ , so the number ofpulses grows linearly in δ under variational distance, but grows as $\sqrt { \delta }$ under KL divergence. This makes intuitive sense because variational distance behaves like the square root of KL divergence in this regime. Indeed, imposing $\mathbb { D } \le 2 \delta ^ { 2 }$ guarantees $\mathbb { V } \leq \delta$ by Pinsker’s inequality and allows $2 \delta \sqrt { n } / \sqrt { \chi _ { 2 } ( Q _ { 1 } \lVert Q _ { 0 } ) }$ pulses, whereas working directly with the variational distance allows $\sqrt { 2 \pi } \delta \sqrt { n } / \sqrt { \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) }$ pulses. The resulting gain in throughput, by a factor of $\sqrt { 2 \pi } / 2 \approx 1 . 2 5$ , is precisely the slack in Pinsker’s inequality.

## III. SHARP APPROXIMATION FOR VARIATIONAL DISTANCE (PROOF OF THEOREM 1)

Recall from (1) that the PPM-induced output distribution $P _ { Z , \mathrm { P P M } } ^ { n , \ell } = P _ { m } ^ { \otimes \ell } \otimes Q _ { 0 } ^ { \otimes r }$ , whereas the innocent output distribution can be written as $Q _ { 0 } ^ { \otimes n } = \left( Q _ { 0 } ^ { \otimes m } \right) ^ { \otimes \ell } \otimes Q _ { 0 } ^ { \otimes r }$ . Since tensoring two distributions with the same probability distribution does not change their variational distance, we have

$$
\mathbb {V} \left(P _ {Z, \mathrm{PPM}} ^ {n, \ell}, Q _ {0} ^ {\otimes n}\right) = \mathbb {V} \left(P _ {m} ^ {\otimes \ell}, \left(Q _ {0} ^ {\otimes m}\right) ^ {\otimes \ell}\right).
$$

## A. Midpoint Representation of Variational Distance

We first convert the variational distance $\mathbb { V } \left( P _ { m } ^ { \otimes \ell } , ( Q _ { 0 } ^ { \otimes m } ) ^ { \otimes \ell } \right)$ into two analytic quantities that can be estimated independently. For a length-m, weight one PPM block, we define the Bhattacharyya coefficient $\rho _ { m }$ and the geometric midpoint distribution $H _ { m } .$ respectively, by

$$
\rho_ {m} \triangleq \sum_ {\mathbf {z}} \sqrt {P _ {m} (\mathbf {z}) Q _ {0} ^ {\otimes m} (\mathbf {z})}, \quad \text { and } \quad H _ {m} (\mathbf {z}) \triangleq \frac {\sqrt {P _ {m} (\mathbf {z}) Q _ {0} ^ {\otimes m} (\mathbf {z})}}{\rho_ {m}}.\tag{4}
$$

Let $\mathbf { Z } _ { 1 } , \ldots , \mathbf { Z } _ { \ell }$ be i.i.d. according to $H _ { m } ,$ , and define the sum of log-likelihood ratio as

$$
L _ {m, \ell} \triangleq \sum_ {i = 1} ^ {\ell} \log \frac {P _ {m} (\mathbf {Z} _ {i})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {i})}.\tag{5}
$$

Lemma 1. By using the elementary identity

$$
\min \{a, b \} = \sqrt {a b} \exp \left(- \frac {1}{2} \left| \log \frac {a}{b} \right|\right), \quad \forall a, b > 0,
$$

the following expression holds:

$$
1 - \mathbb {V} (P _ {m} ^ {\otimes \ell}, (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell}) = \rho_ {m} ^ {\ell} \times \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} \left[ e ^ {- | L _ {m, \ell} | / 2} \right].\tag{6}
$$

The proof of Lemma 1 is provided in Appendix A. Therefore, to approximate the variational distance, it remains to evaluate the right-hand side of (6). Let

$$
h (x) \triangleq e ^ {- | x | / 2} \quad \text { and } \quad N _ {m, \ell} \sim N \left(0, \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}\right).\tag{7}
$$

In what follows, we will prove that the following two equations hold:

Equation (A):

Equation (B):

$$
\begin{array}{l} \rho_ {m} ^ {\ell} = \exp \left[ - \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} \right] \left(1 + O (m ^ {- 1})\right), \\ \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} (h (L _ {m, \ell})) = \mathbb {E} h (N _ {m, \ell}) + O (m ^ {- 1}). \end{array}
$$

Equation (A) provides the required approximation of the power of Bhattacharyya coefficient $\rho _ { m } ^ { \ell } .$ , whereas Equation (B) approximates the expectation of a function of $L _ { m , \ell }$ by its Gaussian counterpart. In the rest of this section, Subsection III-B proves that Equation (A) holds. Subsection III-C converts the main comparison in Equation (B) into the frequency domain and introduces an auxiliary Gaussian smoothing variable to prevent possible lattice peaks at high frequency. Subsection III-D divides the frequency domain into four ranges and controls the error term from each range. Subsection III-E removes the effect of the auxiliary Gaussian smoothing variable, thereby completing the proof of Equation (B). Finally, Subsection III-F combines Equations (A) and (B), evaluates the Gaussian expectation, and translates the result from the block parameter m to the original blocklength n.

B. Approximation of the Power of Bhattacharyya Coefficient $\rho _ { m } ^ { \ell }$

For brevity, we define

$$
B _ {m} \triangleq \frac {1}{m} \sum_ {j = 1} ^ {m} \left(\frac {Q _ {1} (Z _ {j})}{Q _ {0} (Z _ {j})} - 1\right),\tag{8}
$$

and Tahmasbi and Bloch [19] already calculated that when $( Z _ { 1 } , Z _ { 2 } , \ldots , Z _ { m } ) \sim Q _ { 0 } ^ { \otimes m }$

$$
\mathbb {E} [ B _ {m} ] = 0, \qquad \mathbb {E} [ B _ {m} ^ {2} ] = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}, \qquad \mathbb {E} [ B _ {m} ^ {3} ] = O (m ^ {- 2}), \qquad \mathbb {E} [ B _ {m} ^ {4} ] = O (m ^ {- 2}).
$$

Note that $Q _ { 1 } ( Z ) / Q _ { 0 } ( Z ) - 1$ is bounded on the finite support of $Q _ { 0 }$ , hence we define

$$
a _ {\min} \triangleq \min _ {z: Q _ {0} (z) > 0} \left\{\frac {Q _ {1} (z)}{Q _ {0} (z)} - 1 \right\}, \quad \text { and } \quad a _ {\max} \triangleq \max _ {z: Q _ {0} (z) > 0} \left\{\frac {Q _ {1} (z)}{Q _ {0} (z)} - 1 \right\}.
$$

Hoeffding’s inequality yields that

$$
Q _ {0} ^ {\otimes m} \left(| B _ {m} | > \frac {1}{2}\right) \leq 2 \exp \left(- \frac {m}{2 (a _ {\max} - a _ {\min}) ^ {2}}\right).\tag{9}
$$

Recalling that $\begin{array} { r } { P _ { m } ( \mathbf { z } ) = \frac { 1 } { m } \sum _ { j = 1 } ^ { m } Q _ { 1 } ( z _ { j } ) \prod _ { k \neq j } Q _ { 0 } ( z _ { k } ) } \end{array}$ , we have $P _ { m } / Q _ { 0 } ^ { \otimes m } = 1 + B _ { m }$ , and hence the Bhattacharyya coefficient can be written as $\rho _ { m } = \mathbb { E } _ { Q _ { \mathrm { n } } ^ { \otimes m } } [ \sqrt { 1 + B _ { m } } ]$ . To evaluate $\rho _ { m }$ through this expectation, we define the event $\mathcal { E } _ { m } \triangleq \left\{ | B _ { m } | \leq \frac { 1 } { 2 } \right\}$ , and then decompose

$$
\rho_ {m} = \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \sqrt {1 + B _ {m}} \mathbf {1} _ {\mathcal {E} _ {m}} \right] + \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \sqrt {1 + B _ {m}} \mathbf {1} _ {\mathcal {E} _ {m} ^ {\mathrm{c}}} \right].
$$

We first consider the expectation over $\mathcal { E } _ { m } .$ . Let $f ( x ) \triangleq { \sqrt { 1 + x } }$ for $x > - 1$ . Taylor’s theorem with the Lagrange remainder gives, for every $x \in [ - 1 / 2 , 1 / 2 ]$ , there exists a real number $\xi _ { x } \in [ 0 , x ]$ such that

$$
f (x) = \sqrt {1 + x} = 1 + \frac {x}{2} - \frac {x ^ {2}}{8} + \frac {x ^ {3}}{1 6} + R _ {4} (x), \quad \text { where } R _ {4} (x) = \frac {f ^ {(4)} (\xi_ {x})}{2 4} x ^ {4}.
$$

For $| x | \le 1 / 2$ , we have $\xi _ { x } \ge - 1 / 2$ , and hence $\begin{array} { r } { \left| f ^ { ( 4 ) } ( \xi _ { x } ) \right| \le \frac { 1 5 } { 1 6 } \left( \frac { 1 } { 2 } \right) ^ { - 7 / 2 } } \end{array}$ . Therefore, there exists a constant $c _ { 2 } > 0$ such that $| R _ { 4 } ( x ) | \leq c _ { 2 } | x | ^ { 4 }$ for $\left| x \right| \leq { \frac { 1 } { 2 } }$ . Applying this expansion with $x = B _ { m }$ on event ${ \mathcal { E } } _ { m }$ yields

$$
\begin{array}{c} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \sqrt {1 + B _ {m}} \mathbf {1} _ {\mathcal {E} _ {m}} \right] = Q _ {0} ^ {\otimes m} (\mathcal {E} _ {m}) + \frac {1}{2} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} \mathbf {1} _ {\mathcal {E} _ {m}} \right] - \frac {1}{8} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} ^ {2} \mathbf {1} _ {\mathcal {E} _ {m}} \right] \\ + \frac {1}{1 6} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} ^ {3} \mathbf {1} _ {\mathcal {E} _ {m}} \right] + O \left(\mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} ^ {4} \mathbf {1} _ {\mathcal {E} _ {m}} \right]\right). \end{array}
$$

It remains to remove the effect of the indicator $\mathbf { 1 } _ { \mathcal { E } _ { m } }$ in the above expression. Recalling the definitions of $a _ { \mathrm { m i n } }$ and $a _ { \mathrm { m a x } }$ , we have

$$
\left| B _ {m} \right| \leq \max \left\{\left| a _ {\min} \right|, \left| a _ {\max} \right| \right\} \quad Q _ {0} ^ {\otimes m} \text {-almost surely.}
$$

Therefore, for $k \in \{ 1 , 2 , 3 \}$ , the difference between $\mathbb { E } _ { Q _ { 0 } ^ { \otimes m } } \left[ B _ { m } ^ { k } \mathbf { 1 } _ { { \mathcal { E } } _ { m } } \right]$ and $\mathbb { E } _ { Q _ { 0 } ^ { \otimes m } } [ B _ { m } ^ { k } ]$ is exponentially small, since

$$
\begin{array}{r l} & {\left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} ^ {k} \mathbf {1} _ {\mathcal {E} _ {m}} \right] - \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {k} ] \right| = \left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ B _ {m} ^ {k} \mathbf {1} _ {\mathcal {E} _ {m} ^ {c}} \right] \right| \leq \max \{| a _ {\min} |, | a _ {\max} | \} ^ {k} \times Q _ {0} ^ {\otimes m} (\mathcal {E} _ {m} ^ {c})} \\ & {\qquad = O (e ^ {- (1 / (2 (a _ {\max} - a _ {\min}) ^ {2})) m}),} \end{array}
$$

where the last step follows from (9). Moreover, we also have $\mathbb { E } _ { Q _ { 0 } ^ { \otimes m } } \left[ B _ { m } ^ { 4 } \mathbf { 1 } _ { \mathcal { E } _ { m } } \right] \leq \mathbb { E } _ { Q _ { 0 } ^ { \otimes m } } [ B _ { m } ^ { 4 } ]$

We then consider the expectation over $\mathcal { E } _ { m } ^ { \mathrm { c } } .$ . Since $1 + B _ { m } = P _ { m } / Q _ { 0 } ^ { \otimes m } \geq 0$ and $B _ { m } \leq a _ { \mathrm { m a x } } .$ , we have $0 \leq$ $\sqrt { 1 + B _ { m } } \leq \sqrt { 1 + a _ { \operatorname* { m a x } } }$ . Therefore,

$$
\mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \sqrt {1 + B _ {m}} \mathbf {1} _ {\mathcal {E} _ {m} ^ {\mathrm{c}}} \right] \leq \sqrt {1 + a _ {\max}} Q _ {0} ^ {\otimes m} (\mathcal {E} _ {m} ^ {\mathrm{c}}) = O (e ^ {- (1 / (2 (a _ {\max} - a _ {\min}) ^ {2})) m}),
$$

where the last step again follows from (9). Combining the analyses above yields that

$$
\begin{array}{l} \rho_ {m} = 1 + \frac {1}{2} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ] - \frac {1}{8} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {2} ] + \frac {1}{1 6} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {3} ] + O \left(\mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {4} ]\right) + O (e ^ {- (1 / (2 (a _ {\max} - a _ {\min}) ^ {2})) m}) \\ = 1 - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + O (m ^ {- 2}), \end{array}
$$

and hence

$$
\log \rho_ {m} = \log \left(1 - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + O (m ^ {- 2})\right) = - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + O (m ^ {- 2}).
$$

Since $1 \leq \ell \leq c _ { 1 } m$ from the condition of Theorem 1, multiplying ℓ on both sides yields

$$
\ell \log \rho_ {m} = - \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + O (m ^ {- 1}).
$$

Exponentiating both sides yields

$$
\begin{array}{l} \rho_ {m} ^ {\ell} = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + O (m ^ {- 1})\right) \\ \qquad = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) \exp \left(O (m ^ {- 1})\right) \\ \qquad = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) \left(1 + O (m ^ {- 1})\right). \end{array}
$$

This completes the proof of Equation (A).

## C. Approximation of Equation (B) Via Fourier Representation In Characteristic Functions

Our next objective is to approximate $\mathbb { E } [ h ( L _ { m , \ell } ) ]$ . In particular, Subsections C–E below are organized to prove that

$$
\mathbb {E} [ h (L _ {m, \ell}) ] = \mathbb {E} [ h (N _ {m, \ell}) ] + O (m ^ {- 1}),\tag{10}
$$

where $L _ { m , \ell }$ is defined in (5) and $\begin{array} { r } { N _ { m , \ell } \sim N \left( 0 , \frac { \ell \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) } { m } \right) } \end{array}$ is defined in (7). To this end, we study the distributions of $L _ { m , \ell }$ and $N _ { m , \ell }$ through their characteristic function. Let i denote the imaginary unit. The characteristic function of $L _ { m , \ell }$ under $H _ { m } ^ { \otimes \ell }$ is defined as

$$
\varphi_ {L _ {m, \ell}} (t) \triangleq \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} \left[ e ^ {i t L _ {m, \ell}} \right], \qquad t \in \mathbb {R},
$$

whereas the characteristic function of $N _ { m , \ell }$ is defined as

$$
\varphi_ {N _ {m, \ell}} (t) \triangleq \mathbb {E} \left[ e ^ {i t N _ {m, \ell}} \right] = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} t ^ {2}\right), \quad t \in \mathbb {R}.
$$

This representation allows us to compare the distribution of $L _ { m , \ell }$ with an appropriate Gaussian distribution $N _ { m , \ell }$ by comparing their characteristic functions over different frequency ranges.

For $h ( x ) = e ^ { - | x | / 2 }$ , its Fourier transform is

$$
\widehat {h} (t) = \int_ {\mathbb {R}} e ^ {- | x | / 2} e ^ {- i t x} d x = \frac {1}{t ^ {2} + 1 / 4}, \qquad t \in \mathbb {R}.
$$

Since h is continuous and both h and $\widehat { h }$ are absolutely integrable, the Fourier inversion theorem yields

$$
h (x) = \frac {1}{2 \pi} \int_ {\mathbb {R}} \widehat {h} (t) e ^ {i t x} d t = \frac {1}{2 \pi} \int_ {\mathbb {R}} \frac {e ^ {i t x}}{t ^ {2} + 1 / 4} d t.
$$

Consequently, for every real-valued random variable X with characteristic function $\varphi _ { X } ( t )$ , Fubini’s theorem yields

$$
\mathbb {E} [ h (X) ] = \frac {1}{2 \pi} \int_ {\mathbb {R}} \frac {\mathbb {E} [ e ^ {i t X} ]}{t ^ {2} + 1 / 4} d t = \frac {1}{2 \pi} \int_ {\mathbb {R}} \frac {\varphi_ {X} (t)}{t ^ {2} + 1 / 4} d t,\tag{11}
$$

since E $\begin{array} { r } { \int _ { \mathbb { R } } \frac { | e ^ { i t X } | } { t ^ { 2 } + 1 / 4 } d t = \int _ { \mathbb { R } } \frac { d t } { t ^ { 2 } + 1 / 4 } < \infty . } \end{array}$

Directly applying (11) to compare $L _ { m , \ell }$ and $N _ { m , \ell }$ through their characteristic functions, $\mathrm { i . e . }$

$$
| \mathbb {E} [ h (L _ {m, \ell}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] | = \frac {1}{2 \pi} \left| \int_ {\mathbb {R}} \frac {\varphi_ {L _ {m , \ell}} (t) - \varphi_ {N _ {m , \ell}} (t)}{t ^ {2} + 1 / 4} d t \right|\tag{12}
$$

would require controlling the integrand at arbitrarily high frequencies. The Gaussian variable causes no difficulty, since $\varphi _ { N _ { m , \ell } } ( t )$ decays super-exponentially fast in |t|. However, as $L _ { m , \ell }$ is a sum of ℓ i.i.d. random variables taking finitely many values, its characteristic function $\varphi _ { L _ { m , \ell } } ( t )$ may not be small and may return close to one at high frequencies, whereas the weight $( t ^ { 2 } + 1 / 4 ) ^ { - 1 }$ decays only quadratically.

To circumvent this issue, we introduce a Gaussian smoothing variable $G _ { m } \sim N ( 0 , m ^ { - 1 } )$ , which is independent of $L _ { m , \ell }$ and $N _ { m , \ell } .$ . Its characteristic function is $\varphi _ { G _ { m } } ( t ) \triangleq \mathbb { E } \bigl [ e ^ { i t G _ { m } } \bigr ] = e ^ { - t ^ { 2 } / ( 2 m ) }$ . By independence,

$$
\varphi_ {L _ {m, \ell} + G _ {m}} (t) \triangleq \mathbb {E} \left[ e ^ {i t (L _ {m, \ell} + G _ {m})} \right] = \varphi_ {L _ {m, \ell}} (t) \times e ^ {- t ^ {2} / (2 m)},
$$

so that adding $G _ { m }$ multiplies $\varphi _ { L _ { m , \ell } }$ by a factor of $e ^ { - t ^ { 2 } / ( 2 m ) }$ , which is negligible once |t| exceeds the order of $\sqrt { m \log m }$ . This is precisely the range in which no useful bound on $\varphi _ { L _ { m , \ell } }$ is available.

After introducing $G _ { m }$ , we can then use the triangle inequality to decompose (12) as follows:

$$
\begin{array}{r l} & {| \mathbb {E} [ h (L _ {m, \ell}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] | \leq | \mathbb {E} [ h (L _ {m, \ell}) ] - \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] | + | \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] |} \\ & {\quad + | \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] |.} \end{array}\tag{13}
$$

In the following, we will analyze the smoothed Fourier error $\left| \mathbb { E } [ h ( L _ { m , \ell } + G _ { m } ) ] - \mathbb { E } [ h ( N _ { m , \ell } + G _ { m } ) ] \right|$ in Subsection $\mathrm { D } ;$ while the other two terms, corresponding to desmoothing errors, will be analyzed in Subsection E.

## D. Upper Bounds On the Smoothed Fourier Error

Applying the Fourier representation in (11), we bound the smoothed Fourier error as

$$
\begin{array}{l} | \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] | \\ = \frac {1}{2 \pi} \left| \int_ {\mathbb {R}} \frac {\varphi_ {L _ {m , \ell} + G _ {m}} (t) - \varphi_ {N _ {m , \ell} + G _ {m}} (t)}{t ^ {2} + 1 / 4} d t \right| \\ = \frac {1}{2 \pi} \left| \int_ {\mathbb {R}} \frac {e ^ {- t ^ {2} / (2 m)}}{t ^ {2} + 1 / 4} \left[ \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right] d t \right| \end{array}\tag{14}
$$

$$
\leq \frac {1}{2 \pi} \int_ {\mathbb {R}} \frac {e ^ {- t ^ {2} / (2 m)}}{t ^ {2} + 1 / 4} \left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right| d t,\tag{15}
$$

where (14) follows since $\varphi _ { N _ { m , \ell } + G _ { m } } ( t ) = \varphi _ { N _ { m , \ell } } ( t ) \times \varphi _ { G _ { m } } ( t ) = e ^ { - t ^ { 2 } / ( 2 m ) } \times e ^ { - \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) t ^ { 2 } / ( 2 m ) }$ . For simplicity, we define the nonnegative Fourier-error density as

$$
\mathcal {E} _ {m, \ell} (t) \triangleq \frac {e ^ {- t ^ {2} / (2 m)}}{t ^ {2} + 1 / 4} \left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right|.
$$

Fix $k \geq 1$ and $d \geq d _ { 0 }$ , where $d _ { 0 } > 0$ is the constant specified in Proposition 2 below, and let $u _ { 0 } > 0$ be a constant detailed in Appendix C. Below, we decompose the integral in (15) into four frequency bands:

$$
\begin{array}{r l} \int_ {\mathbb {R}} \mathcal {E} _ {m, \ell} (t) d t & = \int_ {| t | \leq d \sqrt {\log m}} \mathcal {E} _ {m, \ell} (t) d t \\ & + \int_ {d \sqrt {\log m} <   | t | \leq u _ {0} \sqrt {m}} \mathcal {E} _ {m, \ell} (t) d t \\ & + \int_ {u _ {0} \sqrt {m} <   | t | \leq \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t \end{array}
$$

$$
+ \int_ {| t | > \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t.\tag{16}
$$

The four frequency bands arise because different estimates of $\varphi _ { L _ { m , \ell } } ( t )$ are available at different frequencies, and each estimate is valid only up to a certain frequency.

• On $| t | \leq d { \sqrt { \log m } }$ , a refined expansion of $\varphi _ { L _ { m , \ell } } ( t )$ is accurate enough to control the difference $\varphi _ { L _ { m , \ell } } ( t ) \mathrm { ~ - ~ }$ $e ^ { - \ell \chi _ { 2 } ( Q _ { 1 } \parallel Q _ { 0 } ) t ^ { 2 } / ( 2 m ) }$ directly. This band is what determines the $O ( m ^ { - 1 } )$ rate in Equation (B); the other three bands are only required not to exceed it, and are in fact smaller once d and k are chosen large enough.

• On $d \sqrt { \log m } < | t | \leq u _ { 0 } \sqrt { m } .$ , this expansion is no longer accurate, so we bound $\varphi _ { L _ { m , \ell } } ( t )$ and $e ^ { - \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) t ^ { 2 } / ( 2 m ) }$ separately by the triangle inequality. Both decay as $e ^ { - \Theta ( t ^ { 2 } ) }$ on this band, and integrating this decay over $| t | > d \sqrt { \log m }$ leads to $m ^ { - \Theta ( d ^ { 2 } ) }$

• On $u _ { 0 } \sqrt { m } < | t | \leq \sqrt { k m }$ log m, even this quadratic decay is unavailable. What remains is that the characteristic function of a single summand of $L _ { m , \ell }$ in (5) stays bounded away from one, uniformly over this band; raised to the ℓ-th power, it becomes $e ^ { - \Theta ( m ) }$ . The Gaussian term is exponentially small here as well.

• On $\left| t \right| > \sqrt { k m \log m }$ , no estimate of $\varphi _ { L _ { m , \ell } }$ is used at all: the smoothing factor $e ^ { - t ^ { 2 } / ( 2 m ) }$ is at most $m ^ { - k / 2 }$ there, which already makes the integral negligible. This is precisely the band in which lattice effects could keep $\varphi _ { L _ { m , \ell } }$ from being small, and it is the reason for introducing $G _ { m }$

Propositions 1–4 below make these four estimates precise.

Proposition 1. For every fixed $d > 0$

$$
\int_ {| t | \leq d \sqrt {\log m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).
$$

Proposition 2. There exist $u _ { 0 } > 0$ and $d _ { 0 } > 0$ such that, for every fixed $d \geq d _ { 0 }$

$$
\int_ {d \sqrt {\log m} <   | t | \leq u _ {0} \sqrt {m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).
$$

Proposition 3. For every fixed $k > 0$ , there exists a constant $c _ { 3 , k } > 0$ such that

$$
\int_ {u _ {0} \sqrt {m} <   | t | \leq \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t = O (e ^ {- c _ {3, k} m}),\tag{17}
$$

where $u _ { 0 } > 0$ is the constant chosen in Proposition 2.

Proposition 4. For every fixed $k \geq 1$

$$
\int_ {| t | > \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).\tag{18}
$$

The proofs of Propositions 1-4 are provided in Appendices B-E, respectively. Combining (15), (16), and Propositions 1-4 together, it can be shown that the smoothed Fourier error satisfies

$$
| \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] | = O (m ^ {- 1}).
$$

## E. Removal of Gaussian Smoothing

To complete the decomposition in (13), it remains to show that removing $G _ { m }$ from each of the two expectations does not incur significant error.

Proposition 5 (Desmoothing error). The two desmoothing error terms satisfy

$$
| \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (L _ {m, \ell}) ] | = O (m ^ {- 1}), \qquad | \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] | = O (m ^ {- 1}).
$$

The proof of Proposition 5 is presented in Appendix F. Below, we briefly describe the high-level intuition for $L _ { m , \ell } .$ The argument for $N _ { m , \ell }$ is similar.

The key observation is the almost-sure perturbation bound

$$
| h (L _ {m, \ell} + G _ {m}) - h (L _ {m, \ell}) - G _ {m} h ^ {\prime} (L _ {m, \ell}) | \leq G _ {m} ^ {2} + | G _ {m} | \mathbf {1} _ {\{| L _ {m, \ell} | \leq | G _ {m} | \}}.\tag{19}
$$

The quadratic term $G _ { m } ^ { 2 }$ controls the usual second-order Taylor error when the interval between $L _ { m , \ell }$ and $L _ { m , \ell } + G _ { m }$ does not contain the origin. If this interval crosses the origin, then $h ( t ) = e ^ { - | t | / 2 }$ is not differentiable along the interval, and the error may instead be of order $\left| G _ { m } \right|$ . Such a crossing can occur only if $\begin{array} { r } { | L _ { m , \ell } | \leq | G _ { m } | } \end{array}$ , which accounts for the second term in the bound.

Because $G _ { m }$ is independent of $L _ { m , \ell }$ and has zero mean, the linear term $G _ { m } h ^ { \prime } ( L _ { m , \ell } )$ has zero expectation. It therefore remains to control the two terms on the right-hand side of (19). The first quadratic term contributes $\mathbb { E } [ G _ { m } ^ { 2 } ] = m ^ { - 1 }$ . For the second term, the anti-concentration estimate established in Appendix F gives $\mathrm { P r } \{ | L _ { m , \ell } | \leq$ $s \} \leq c ( s + m ^ { - 1 / 2 } )$ uniformly over $s \geq 0$ . Conditioning on $G _ { m }$ and taking $s = | G _ { m } |$ yields that the second term is bounded by $c \mathbb { E } [ | G _ { m } | ( | G _ { m } | + m ^ { - 1 / 2 } ) ]$ , which is $O ( m ^ { - 1 } )$ ) since $\mathbb { E } [ G _ { m } ^ { 2 } ] = m ^ { - 1 }$ and E $| G _ { m } | = O ( m ^ { - 1 / 2 } )$ . Hence adding and subsequently removing the smoothing variable changes the expectation by only $O ( m ^ { - 1 } )$ ).

Combining Subsections D and E together, we prove that $\mathbb { E } [ h ( L _ { m , \ell } ) ] = \mathbb { E } [ h ( N _ { m , \ell } ) ] + O ( m ^ { - 1 } )$ in (10).

## F. Completion of the Proof of Theorem 1

Substituting Equation (A) and (10) into Lemma 1 gives

$$
\begin{array}{l} 1 - \mathbb {V} \left(P _ {m} ^ {\otimes \ell}, (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell}\right) = \rho_ {m} ^ {\ell} \times \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} \left[ h (L _ {m, \ell}) \right] \\ \qquad = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) \left(1 + O (m ^ {- 1})\right) \left(\mathbb {E} [ h (N _ {m, \ell}) ] + O (m ^ {- 1})\right) \\ \qquad = \exp \left(- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) \mathbb {E} [ h (N _ {m, \ell}) ] + O (m ^ {- 1}), \end{array}\tag{20}
$$

where the last step uses $0 \leq h ( \cdot ) \leq 1$ and the fact that $\ell / m$ is bounded (as stated in (2)).

It remains to evaluate $\mathbb { E } [ h ( N _ { m , \ell } ) ]$ ] where $\begin{array} { r } { N _ { m , \ell } \sim N \left( 0 , \frac { \ell \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) } { m } \right) } \end{array}$ . By symmetry and the density of $N _ { m , \ell }$

$$
\begin{array}{l} \mathbb {E} [ h (N _ {m, \ell}) ] = \mathbb {E} e ^ {- | N _ {m, \ell} | / 2} = 2 \sqrt {\frac {m}{2 \pi \ell \chi_ {2} (Q _ {1} \| Q _ {0})}} \int_ {0} ^ {\infty} \exp \left(- \frac {x}{2} - \frac {m x ^ {2}}{2 \ell \chi_ {2} (Q _ {1} \| Q _ {0})}\right) d x \\ \qquad = 2 \exp \left(\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) \sqrt {\frac {m}{2 \pi \ell \chi_ {2} (Q _ {1} \| Q _ {0})}} \\ \qquad \times \int_ {0} ^ {\infty} \exp \left(- \frac {m}{2 \ell \chi_ {2} (Q _ {1} \| Q _ {0})} \left(x + \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{2 m}\right) ^ {2}\right) d x \\ \qquad = 2 \exp \left(\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{8 m}\right) Q \left(\frac {1}{2} \sqrt {\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}}\right), \end{array}\tag{21}
$$

where the last step follows from the change of variable $\begin{array} { r } { u = \sqrt { \frac { m } { \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } } \left( x + \frac { \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } { 2 m } \right) } \end{array}$ , under which the lower limit $x = 0$ is mapped to $\begin{array} { r } { u = \frac { 1 } { 2 } \sqrt { \frac { \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } { m } } } \end{array}$ . Substituting (21) into the expression in (20), the two exponential factors cancel, and hence

$$
1 - \mathbb {V} \left(P _ {m} ^ {\otimes \ell}, (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell}\right) = 2 Q \left(\frac {1}{2} \sqrt {\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}}\right) + O (m ^ {- 1}).
$$

It remains to replace the argument of $Q$ from $\begin{array} { r } { \frac { 1 } { 2 } \sqrt { \frac { \ell \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } { m } } \mathrm { ~ t o ~ } \frac { \ell } { 2 } \sqrt { \frac { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } { n } } } \end{array}$ that appeared in Theorem 1. Recall that $n = m \ell + r$ . The two arguments coincide exactly when $r = 0$ . When $r \neq 0$ , the following computation shows that the non-zero remainder r perturbs the argument by only $O ( m ^ { - 1 } )$ . Note that

$$
\left[ \frac {1}{2} \sqrt {\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}} \right] ^ {2} - \left[ \frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}} \right] ^ {2} = \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{4 m} \left(1 - \frac {m \ell}{n}\right) = \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{4 m} \frac {r}{n}.
$$

Because $r < \ell , n \geq m \ell ,$ , and $\ell / m \leq c _ { 1 }$ , we have

$$
0 \leq \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{4 m} \frac {r}{n} \leq \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{4 m} \frac {\ell}{m \ell} \leq \frac {c _ {1} \chi_ {2} (Q _ {1} \| Q _ {0})}{4 m} = O (m ^ {- 1}).
$$

Using the fact that $\begin{array} { r } { | x - y | = { \frac { | x ^ { 2 } - y ^ { 2 } | } { x + y } } } \end{array}$ for $x , y \geq 0$ , we have

$$
\left| \frac {1}{2} \sqrt {\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}} - \frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}} \right| = O (m ^ {- 1}).
$$

Since $\begin{array} { r } { | Q ^ { \prime } ( x ) | = \frac { 1 } { \sqrt { 2 \pi } } e ^ { - x ^ { 2 } / 2 } \leq \frac { 1 } { \sqrt { 2 \pi } } } \end{array}$ , the function Q is Lipschitz, and therefore

$$
Q \left(\frac {1}{2} \sqrt {\frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m}}\right) = Q \left(\frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}}\right) + O (m ^ {- 1}).
$$

Finally, combining the preceding calculations and noting that $m = \Theta ( { \sqrt { n } } )$ , we obtain

$$
\mathbb {V} \left(P _ {Z, \mathrm{PPM}} ^ {n, \ell}, Q _ {0} ^ {\otimes n}\right) = 1 - 2 Q \left(\frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}}\right) + O (n ^ {- 1 / 2}).
$$

This completes the proof of Theorem 1.

## IV. DERIVATION OF THE EXACT SECOND-ORDER CODING ASYMPTOTICS

This section links the approximation of variational distance in Section III to the covert communication problem.

## A. Random Coding With PPM Input Distribution

Recall that $n = m \ell + r$ , where $0 \leq r < \ell ,$ , and we partition the first mℓ coordinates into the blocks

$$
\mathcal {B} _ {i} \triangleq [   [ (i - 1) m + 1, i m ]   ], \qquad i \in [   [ 1, \ell ]   ].
$$

The length-n, weight-ℓ PPM input distribution is uniform on the set

$$
\mathcal {P} _ {n, \ell} \triangleq \left\{\mathbf {x} \in \{0, 1 \} ^ {n}: \sum_ {j \in \mathcal {B} _ {i}} x _ {j} = 1 \text {   for   every   } i, \quad \sum_ {j = m \ell + 1} ^ {n} x _ {j} = 0 \right\}.
$$

Thus every codeword has one non-innocent symbol in each of the ℓ blocks and only innocent symbols in the remaining r coordinates. There are $m ^ { \ell }$ such sequences, each having probability $m ^ { - \ell }$ . Passing this input distribution through the warden’s channel gives exactly the PPM-induced output distribution $P _ { Z , \mathrm { P P M } } ^ { n , \ell }$ in (1).

For message size $M _ { n }$ and key size $K _ { n }$ , we draw codewords $\left\{ \mathbf { X } _ { s w } : s \in \mathbb { I } ^ { 1 , K _ { n } } \mathbb { I } , w \in \mathbb { I } ^ { 1 , M _ { n } } \mathbb { I } \right\}$ independently from the PPM input distribution. For a fixed key s, the subcode $\{ \mathbf { X } _ { s w } : w \in \mathbb { [ 1 , M _ { n } ] ] } \}$ is used for reliable communication to the legitimate receiver. The decoding rule is the same as that in [19].

The reliability, resolvability, and expurgation arguments for this random codebook were established in [19, Theorem 5] and will not be repeated here. We only focus on the specialization of that result needed in the present paper. This specialization also makes explicit that the only new ingredient required below is a sufficiently accurate estimate of the covertness of the PPM-induced output distribution.

Proposition 6. Fix $0 < \epsilon < 1$ , and let $\ell = \Theta ( { \sqrt { n } } )$ . Suppose that the PPM-induced output distribution satisfies

$$
\mathbb {V} \big (P _ {Z, \mathrm{PPM}} ^ {n, \ell}, Q _ {0} ^ {\otimes n} \big) \leq \delta - n ^ {- 1 / 2}.
$$

Then, for all sufficiently large n, there exists a deterministic PPM code satisfying the corresponding covertness constraint and having maximum probability of error at most ϵ, with

$$
\log M _ {n} = \ell D _ {P} - \sqrt {\ell V _ {P}} Q ^ {- 1} (\epsilon) + O (\log n), \mathrm{and} \log K _ {n} = \ell [ D _ {Q} - D _ {P} ] ^ {+} + o (\sqrt {n}).
$$

The proof of Proposition 6 is provided in Appendix G, where we verify that the four conditions required for [19, Theorem 5] to hold are satisfied under the length-n, weight-ℓ PPM input distribution $\mathcal { P } _ { n , \ell }$

## B. Pulse Selection under the Variational Distance Metric

Fix $0 < \delta < 1$ , and recall that $\begin{array} { r } { \Gamma = Q ^ { - 1 } \left( \frac { 1 - \delta } { 2 } \right) } \end{array}$ . By Theorem 1, there exists a constant $c _ { 4 } > 0$ such that

$$
\mathbb {V} \big (P _ {Z, \mathrm{PPM}} ^ {n, \ell}, Q _ {0} ^ {\otimes n} \big) \leq 1 - 2 Q \left(\frac {\ell}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}}\right) + \frac {c _ {4}}{\sqrt {n}}
$$

for all sufficiently large n. Choose

$$
\ell_ {n} = \left\lfloor \frac {2 \Gamma}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}} \sqrt {n} - c _ {5} \right\rfloor ,
$$

where $c _ { 5 } > 0$ is a constant satisfying $\frac { c _ { 5 } \sqrt { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } } { \sqrt { 2 \pi } e ^ { \Gamma ^ { 2 } / 2 } } > c _ { 4 } + 1$ . By writing $\begin{array} { r } { \ell _ { n } = \frac { 2 \Gamma } { \sqrt { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } } \sqrt { n } - c _ { 5 } - \theta _ { n } } \end{array}$ for $0 \leq \theta _ { n } < 1$ , we have

$$
\frac {\ell_ {n}}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}} = \Gamma - \frac {(c _ {5} + \theta_ {n}) \sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}{2 \sqrt {n}}.
$$

Since $1 - 2 Q ( \Gamma ) = \delta .$ , Taylor expansion at $\Gamma$ yields

$$
\begin{array}{r l r} & & {1 - 2 Q \left(\frac {\ell_ {n}}{2} \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{n}}\right) = \delta - \frac {(c _ {5} + \theta_ {n}) \sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}{\sqrt {2 \pi n} e ^ {\Gamma^ {2} / 2}} + O (n ^ {- 1})} \\ & & {\leq \delta - \frac {c _ {5} \sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}{\sqrt {2 \pi n} e ^ {\Gamma^ {2} / 2}} + O (n ^ {- 1}).} \end{array}
$$

Consequently,

$$
\mathbb {V} \big (P _ {Z, \mathrm{PPM}} ^ {n, \ell_ {n}}, Q _ {0} ^ {\otimes n} \big) \leq \delta - \frac {1}{\sqrt {n}} \left(\frac {c _ {5} \sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}{\sqrt {2 \pi} e ^ {\Gamma^ {2} / 2}} - c _ {4} + o (1)\right).
$$

Since the constant $c _ { 5 }$ satisfies $\frac { c _ { 5 } \sqrt { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } } { \sqrt { 2 \pi } e ^ { \Gamma ^ { 2 } / 2 } } > c _ { 4 } + 1$ , we have that for all sufficiently large n,

$$
\mathbb {V} \big (P _ {Z, \mathrm{PPM}} ^ {n, \ell_ {n}}, Q _ {0} ^ {\otimes n} \big) \leq \delta - \frac {1}{\sqrt {n}},
$$

and hence the condition of Proposition 6 is satisfied.

Proposition 6 therefore gives a sequence of $( M _ { n } , K _ { n } , n , \epsilon , \delta )$ <sub>V</sub> codes satisfying

$$
\log M _ {n} = \ell_ {n} D _ {P} - \sqrt {\ell_ {n} V _ {P}} Q ^ {- 1} (\epsilon) + O (\log n).
$$

Substitution $\begin{array} { r } { \ell _ { n } = \frac { 2 \Gamma } { \sqrt { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } } \sqrt { n } + O ( 1 ) } \end{array}$ therefore yields

$$
\log M _ {n} = \frac {2 \Gamma D _ {P}}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}} n ^ {1 / 2} - \sqrt {\frac {2 \Gamma V _ {P}}{\sqrt {\chi_ {2} (Q _ {1} \| Q _ {0})}}} Q ^ {- 1} (\epsilon) n ^ {1 / 4} + O (\log n).
$$

The $n ^ { 1 / 4 }$ penalty appearing in [19, Eq. (30)] has therefore disappeared. Finally, by combining the converse result for variational distance in [19], we complete the proof of Theorem 2.

## V. CONCLUSION

This paper has established the exact second-order asymptotics for covert communication over the considered binary-input DMCs when covertness is measured by variational distance. The coding scheme is the PPM construction used in previous work, whereas the improvement mainly comes from a sharper analysis of the distribution induced at the warden. The resulting $O ( n ^ { - 1 / 2 } )$ approximation eliminates the $O ( n ^ { 1 / 4 } )$ backoff that appeared in the previous achievability analysis. Consequently, the achievable second-order term coincides with the converse second-order term developed in [19].

A promising direction for future work is to investigate whether the techniques developed here can be adapted to the setting in which covertness is measured by the probability of missed detection at a fixed probability of false alarm. The corresponding criterion is governed by a Neyman–Pearson tradeoff and has a different structure from variational distance, so it remains unclear whether the refinement established in this paper carries over without additional losses. A successful extension could lead to matching second-order asymptotics for this metric.

## ACKNOWLEDGEMENT

The proofs in this paper are provided jointly by the authors and GPT-5.6-Sol, with support from a math harness project at Shanghai AI Laboratory, developed by Dr. Shuyue Hu, Dr. Yang Chen, and Mr. Zhanhao Li. The authors performed a complete verification of the part of proofs that are generated by AI, including all intermediate calculations and logical steps, and assume full responsibility for the correctness of the mathematical content.

## APPENDIX A PROOF OF LEMMA 1

For arbitrary probability mass functions R and S,

$$
\begin{array}{c} 1 - \mathbb {V} (R, S) = \frac {1}{2} \sum_ {x} \{R (x) + S (x) - | R (x) - S (x) | \} \\ = \sum_ {x} \min \{R (x), S (x) \}. \end{array}
$$

Substituting $a = P _ { m } ^ { \otimes \ell } , b = ( Q _ { 0 } ^ { \otimes m } ) ^ { \otimes \ell }$ , and writing $\underline { { \mathbf { z } } } = ( \mathbf { z } _ { 1 } , \dots , \mathbf { z } _ { \ell } )$ , at every z for which both distributions $P _ { m } ^ { \otimes \ell } ( \underline { { \mathbf { z } } } )$ and $( Q _ { 0 } ^ { \otimes m } ) ^ { \otimes \ell } ( \underline { { \mathbf { z } } } )$ are positive, we have

$$
\min \left\{P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}), (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}}) \right\} = \sqrt {P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}) (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}})} \exp \left[ - \frac {1}{2} \left| \log \frac {P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}})}{(Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}})} \right| \right].
$$

By the definition of $H _ { m }$ , we have $\sqrt { P _ { m } ( \mathbf { z } _ { i } ) Q _ { 0 } ^ { \otimes m } ( \mathbf { z } _ { i } ) } = \rho _ { m } H _ { m } ( \mathbf { z } _ { i } )$ and thus

$$
\sqrt {P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}) (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}})} = \rho_ {m} ^ {\ell} \prod_ {i = 1} ^ {\ell} H _ {m} (\mathbf {z} _ {i}) = \rho_ {m} ^ {\ell} H _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}).
$$

Similarly, the logarithm of the product likelihood ratio can be expressed as

$$
\log \frac {P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}})}{(Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}})} = \sum_ {i = 1} ^ {\ell} \log \frac {P _ {m} (\mathbf {z} _ {i})}{Q _ {0} ^ {\otimes m} (\mathbf {z} _ {i})} = L _ {m, \ell} (\underline {{\mathbf {z}}}).
$$

If at z one of the product masses is zero, its contribution to min $\{ P _ { m } ^ { \otimes \ell } , ( Q _ { 0 } ^ { \otimes m } ) ^ { \otimes \ell } \}$ and $H _ { m } ^ { \otimes \ell }$ are both zero. Consequently,

$$
1 - \mathbb {V} (P _ {m} ^ {\otimes \ell}, (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell}) = \sum_ {\underline {{\mathbf {z}}}} \min \left\{P _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}), (Q _ {0} ^ {\otimes m}) ^ {\otimes \ell} (\underline {{\mathbf {z}}}) \right\}
$$

$$
= \sum_ {\underline {{\mathbf {z}}}: H _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}) > 0} \rho_ {m} ^ {\ell} H _ {m} ^ {\otimes \ell} (\underline {{\mathbf {z}}}) \exp \left(- \frac {1}{2} | L _ {m, \ell} (\underline {{\mathbf {z}}}) |\right) = \rho_ {m} ^ {\ell} \times \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} \left[ e ^ {- | L _ {m, \ell} | / 2} \right].
$$

This completes the proof of Lemma 1.

## APPENDIX B PROOF OF PROPOSITION 1

Proposition 1. For every fixed $d > 0$

$$
\int_ {| t | \leq d \sqrt {\log m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).
$$

Before introducing the proof of Proposition 1, we first introduce an auxiliary variable $M _ { m } ( s )$ that will be useful in later analyses:

$$
M _ {m} (s) \triangleq \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \left(1 + B _ {m}\right) ^ {s} \right], \quad s \in \mathbb {C} \text {   such   that   } \operatorname{Re} (s) > 0,
$$

where $\mathbb { C }$ represents the set of complex numbers, whereas $\operatorname { R e } ( s )$ denotes the real part of s. Note that $\rho _ { m }$ defined in (4) is a special case of $M _ { m } ( s )$ when $s = 1 / 2$

Lemma 2. For every fixed $d > 0$ , there exists a constant $c _ { B , 1 , d } > 0$ , depending only on d, $Q _ { 0 }$ , and $Q _ { 1 }$ , such that, for all sufficiently large m, uniformly over $s \in \mathbb { C }$ satisfying

$$
\frac {1}{4} \leq \operatorname{Re} (s) \leq \frac {3}{4}, \quad | \operatorname{Im} (s) | \leq d \sqrt {\log m},
$$

one has

$$
\log M _ {m} (s) = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + r _ {m} (s), \quad \text { where } | r _ {m} (s) | \leq \frac {c _ {B , 1 , d} (1 + | s |) ^ {4}}{m ^ {2}}.
$$

Below, we first provide a proof for Lemma 2, and then present the proof of Proposition 1 based on Lemma 2.

## A. Proof of Lemma 2

For convenience, we define $\begin{array} { r } { A ( Z ) \triangleq \frac { Q _ { 1 } ( Z ) } { Q _ { 0 } ( Z ) } - 1 } \end{array}$ . Then the random variable $B _ { m }$ defined in (8) can be written as $\begin{array} { r } { B _ { m } = \frac { 1 } { m } \sum _ { j = 1 } ^ { m } A ( Z _ { j } ) } \end{array}$ . Since $Q _ { 1 }$ and $Q _ { 0 }$ are probability mass functions, we have

$$
\mathbb {E} _ {Q _ {0}} [ A (Z) ] = 0, \quad \text { and } \quad \mathbb {E} _ {Q _ {0}} [ A (Z) ^ {2} ] = \chi_ {2} (Q _ {1} \| Q _ {0}).
$$

Moreover, $A ( Z )$ is bounded because the alphabet is finite and $Q _ { 1 } \ll Q _ { 0 }$

1) Calculating the Moments of $B _ { m } .$ : First, we note that [19, Eqns. (359)–(363)] has already shown that

$$
\mathbb {E} B _ {m} = 0, \quad \mathbb {E} B _ {m} ^ {2} = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}, \quad \mathbb {E} B _ {m} ^ {3} = \frac {\mathbb {E} _ {Q _ {0}} [ A (Z) ^ {3} ]}{m ^ {2}}.
$$

For the fourth moment, the only nonzero index patterns are four equal indices and two pairs. It follows that

$$
\begin{array}{r l} & {\mathbb {E} \left[ \left(\sum_ {j = 1} ^ {m} A (Z _ {j})\right) ^ {4} \right] = m \mathbb {E} _ {Q _ {0}} [ A (Z) ^ {4} ] + 6 \sum_ {1 \leq i <   j \leq m} \mathbb {E} _ {Q _ {0}} [ A (Z _ {i}) ^ {2} ] \mathbb {E} _ {Q _ {0}} [ A (Z _ {j}) ^ {2} ]} \\ & {\qquad = m \mathbb {E} _ {Q _ {0}} [ A (Z) ^ {4} ] + 3 m (m - 1) \chi_ {2} (Q _ {1} \| Q _ {0}) ^ {2}.} \end{array}
$$

Therefore,

$$
\mathbb {E} B _ {m} ^ {4} = \frac {3 \chi_ {2} (Q _ {1} \| Q _ {0}) ^ {2}}{m ^ {2}} + \frac {\mathbb {E} _ {Q _ {0}} [ A (Z) ^ {4} ] - 3 \chi_ {2} (Q _ {1} \| Q _ {0}) ^ {2}}{m ^ {3}} = O (m ^ {- 2}).
$$

The absolute third moment can be bounded using the fourth moment. By using the Lyapunov’s inequality $\left( \mathbb { E } | B _ { m } | ^ { 3 } \right) ^ { 1 / 3 } \leq \left( \mathbb { E } | B _ { m } | ^ { 4 } \right) ^ { 1 / 4 }$ , we have

$$
\mathbb {E} | B _ {m} | ^ {3} \leq \left(\mathbb {E} [ B _ {m} ^ {4} ]\right) ^ {3 / 4} = O (m ^ {- 3 / 2}).
$$

Note that although the absolute third moments $\mathbb { E } | B _ { m } | ^ { 3 } = O ( m ^ { - 3 / 2 } )$ , the signed third moment satisfies the sharper estimate $\mathbb { E } B _ { m } ^ { 3 } = O ( m ^ { - 2 } )$

2) A Uniform Expansion of $M _ { m } ( s )$ : The purpose of this step is to identify the term of order $m ^ { - 1 }$ in

$$
M _ {m} (s) = \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ (1 + B _ {m}) ^ {s} \right]
$$

and to bound the remaining terms uniformly by $c _ { B , 6 , d } ( 1 + | s | ) ^ { 4 } m ^ { - 2 }$ . To do so, we expand $( 1 + B _ { m } ) ^ { s }$ through the cubic term. The cubic contribution is of order $m ^ { - 2 }$ because $\mathbb { E } B _ { m } ^ { 3 } = O ( m ^ { - 2 } )$ , while the Taylor remainder is also of order $m ^ { - 2 }$ because it is controlled by $\mathbb { E } B _ { m } ^ { 4 } = O ( m ^ { - 2 } )$

The Taylor expansion cannot be applied uniformly when $B _ { m }$ is close to −1, because the derivatives of $x \mapsto$ $( 1 + x ) ^ { s }$ may become large. We therefore use the event $\mathcal { E } _ { m } = \left\{ | B _ { m } | \leq \frac { 1 } { 2 } \right\}$ introduced in Section III, on which $1 + B _ { m }$ is bounded away from zero. Thus, the Taylor expansion will only be used on ${ \mathcal { E } } _ { m }$ , whereas the contribution from $\mathcal { E } _ { m } ^ { \mathrm { c } }$ will be controlled directly using its exponentially small probability.

For fixed $s \in \mathbb { C } .$ , consider the complex-valued function of the real variable x

$$
f _ {s} (x) \triangleq (1 + x) ^ {s} = \exp \bigl (s \log (1 + x) \bigr), \qquad x > - 1.
$$

Denote its cubic Taylor polynomial at the origin by

$$
T _ {3} (s, x) \triangleq 1 + s x + \binom{s}{2} x ^ {2} + \binom{s}{3} x ^ {3}.
$$

and we also define the difference

$$
R _ {4} (s, x) \triangleq (1 + x) ^ {s} - T _ {3} (s, x).
$$

We now separate $M _ { m } ( s )$ into three terms. The first term is the expectation of the cubic Taylor polynomial and produces the leading term of the expansion. The second is the Taylor remainder on ${ \mathcal { E } } _ { m }$ , which will be controlled by $\mathbb { E } B _ { m } ^ { 4 }$ . The third is the correction from the exceptional event $\mathcal { E } _ { m } ^ { \mathrm { c } }$ , which will be exponentially small. More precisely,

$$
M _ {m} (s) = \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ T _ {3} (s, B _ {m}) \right] + \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ R _ {4} (s, B _ {m}) \mathbf {1} _ {\mathcal {E} _ {m}} \right] + \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \left((1 + B _ {m}) ^ {s} - T _ {3} (s, B _ {m})\right) \mathbf {1} _ {\mathcal {E} _ {m} ^ {c}} \right].
$$

We first evaluate the polynomial term, which determines the main part of $M _ { m } ( s )$ . Note that

$$
\begin{array}{r l} & {\mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ T _ {3} (s, B _ {m}) ] = 1 + s \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ] + \binom {s} {2} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {2} ] + \binom {s} {3} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {3} ]} \\ & {\qquad = 1 + \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + \binom {s} {3} \frac {\mathbb {E} _ {Q _ {0}} [ A (Z) ^ {3} ]}{m ^ {2}}.} \end{array}
$$

Since, for a numerical constant $c _ { B , 2 } > 0 , | { \binom { s } { 3 } } | \leq c _ { B , 2 } ( 1 + | s | ) ^ { 3 }$ , we have

$$
\left| \binom {s} {3} \frac {\mathbb {E} _ {Q _ {0}} [ A (Z) ^ {3} ]}{m ^ {2}} \right| \leq \frac {c _ {B , 2} (1 + | s |) ^ {3}}{m ^ {2}}.
$$

Thus,

$$
\mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ T _ {3} (s, B _ {m}) \right] = 1 + \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + O \left(\frac {(1 + | s |) ^ {3}}{m ^ {2}}\right).
$$

We next control the Taylor remainder on ${ \mathcal { E } } _ { m }$ . Note that Taylor’s theorem with an integral remainder gives

$$
R _ {4} (s, x) = \frac {x ^ {4}}{3 !} \int_ {0} ^ {1} (1 - t) ^ {3} f _ {s} ^ {(4)} (t x) d t, \quad \text { where } f _ {s} ^ {(4)} (x) = s (s - 1) (s - 2) (s - 3) (1 + x) ^ {s - 4}.
$$

Suppose that $\begin{array} { r } { \frac { 1 } { 4 } \leq \operatorname { R e } ( s ) \leq \frac { 3 } { 4 } } \end{array}$ and $\left| x \right| \leq { \frac { 1 } { 2 } }$ . For every $t \in [ 0 , 1 ]$ , we then have $\begin{array} { r } { \frac { 1 } { 2 } \leq 1 + t x \leq \frac { 3 } { 2 } } \end{array}$ . Since $1 + t x$ is positive, we have

$$
\left| (1 + t x) ^ {s - 4} \right| = (1 + t x) ^ {\operatorname{Re} (s) - 4} \leq 2 ^ {1 5 / 4}.
$$

Furthermore, for a numerical constant $c _ { B , 3 } > 0 , | s ( s - 1 ) ( s - 2 ) ( s - 3 ) | \leq c _ { B , 3 } ( 1 + | s | ) ^ { 4 }$ . Therefore, we have

$$
| R _ {4} (s, x) | \leq c _ {B, 3} (1 + | s |) ^ {4} | x | ^ {4}, \qquad | x | \leq \frac {1}{2}.
$$

The pointwise remainder bound and the fourth-moment estimate from Step 1 give

$$
\begin{array}{r l} \left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ R _ {4} (s, B _ {m}) \mathbf {1} _ {\mathcal {E} _ {m}} ] \right| & \leq c _ {B, 3} (1 + | s |) ^ {4} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {4} \mathbf {1} _ {\mathcal {E} _ {m}} ] \\ & \leq c _ {B, 3} (1 + | s |) ^ {4} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {4} ] \\ & \leq \frac {c _ {B , 3} (1 + | s |) ^ {4}}{m ^ {2}}. \end{array}
$$

Finally, it remains to control the exceptional event. By the definitions of $a _ { \mathrm { m i n } }$ and $a _ { \mathrm { m a x } }$

$$
a _ {\min} \leq B _ {m} \leq a _ {\max} \quad Q _ {0} ^ {\otimes m} \text {-almost surely.}
$$

Moreover, $\begin{array} { r } { 1 + B _ { m } = \frac { 1 } { m } \sum _ { j = 1 } ^ { m } \frac { Q _ { 1 } ( Z _ { j } ) } { Q _ { 0 } ( Z _ { j } ) } \ge 0 } \end{array}$ and $1 + B _ { m } \le 1 + a _ { \operatorname* { m a x } }$ . Hence, whenever $1 / 4 \le \mathrm { R e } ( s ) \le 3 / 4$ , there exists a constant $c _ { B , 4 } > 0$ such that

$$
| (1 + B _ {m}) ^ {s} | = (1 + B _ {m}) ^ {\mathrm{Re} (s)} \leq c _ {B, 4},
$$

where $0 ^ { s }$ is defined as zero because $\operatorname { R e } ( s ) > 0$ . The uniform boundedness of $B _ { m }$ also implies, for a constant $c _ { B , 5 } > 0$

$$
\left| T _ {3} (s, B _ {m}) \right| \leq c _ {B, 5} (1 + | s |) ^ {3}.
$$

Therefore,

$$
\begin{array}{l} \left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \big ((1 + B _ {m}) ^ {s} - T _ {3} (s, B _ {m}) \big) \mathbf {1} _ {\mathcal {E} _ {m} ^ {\mathrm{c}}} \right] \right| \\ \leq c _ {B, 5} (1 + | s |) ^ {3} Q _ {0} ^ {\otimes m} (\mathcal {E} _ {m} ^ {\mathrm{c}}) \\ \leq c _ {B, 5} (1 + | s |) ^ {3} \times e ^ {- (1 / (2 (a _ {\max} - a _ {\min}) ^ {2})) m}. \end{array}
$$

Since $e ^ { - ( 1 / ( 2 ( a _ { \mathrm { m a x } } - a _ { \mathrm { m i n } } ) ^ { 2 } ) ) m } \leq m ^ { - 2 }$ for all sufficiently large m, this term satisfies

$$
\left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ \big ((1 + B _ {m}) ^ {s} - T _ {3} (s, B _ {m}) \big) \mathbf {1} _ {\mathcal {E} _ {m} ^ {\mathrm{c}}} \right] \right| \leq \frac {c _ {B , 5} (1 + | s |) ^ {4}}{m ^ {2}}.
$$

Combining the three terms above yields

$$
M _ {m} (s) = 1 + \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + R _ {m} (s),\tag{22}
$$

where, for every fixed $d > 0 ;$ , there exists $c _ { B , 6 , d } > 0$ such that $\begin{array} { r } { | R _ { m } ( s ) | \leq \frac { c _ { B , 6 , d } ( 1 + | s | ) ^ { 4 } } { m ^ { 2 } } } \end{array}$ uniformly over all s such that ${ \begin{array} { l } { { \frac { 1 } { 4 } } \leq \mathrm { { R e } } ( s ) \leq { \frac { 3 } { 4 } } , | \operatorname { I m } ( s ) | \leq d { \sqrt { \log m } } } \end{array} }$

3) Passing From $M _ { m } ( s )$ To log $M _ { m } ( s ) { \mathrm { . } }$ : Applying the triangle inequality to the expansion in (22) yields

$$
\begin{array}{c} | M _ {m} (s) - 1 | \leq \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} | s (s - 1) | + | R _ {m} (s) | \\ \leq \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2} \frac {(1 + | s |) ^ {2}}{m} + c _ {B, 6, d} \frac {(1 + | s |) ^ {4}}{m ^ {2}}, \end{array}
$$

where the last inequality follows from $| s ( s - 1 ) | = | s | | s - 1 | \leq | s | ( | s | + 1 ) \leq ( 1 + | s | ) ^ { 2 } .$

On the range $\begin{array} { r } { \frac { 1 } { 4 } \leq \operatorname { R e } ( s ) \leq \frac { 3 } { 4 } } \end{array}$ and $| \operatorname { I m } ( s ) | \leq d { \sqrt { \log m } }$ , we have

$$
| s | \leq | \operatorname{Re} (s) | + | \operatorname{Im} (s) | \leq \frac {3}{4} + d \sqrt {\log m}.
$$

For $m \geq e ,$ , we have ${ \sqrt { \log m } } \geq 1$ and hence

$$
1 + | s | \leq \frac {7}{4} + d \sqrt {\log m} \leq \left(d + \frac {7}{4}\right) \sqrt {\log m}.
$$

Therefore,

$$
\left| M _ {m} (s) - 1 \right| \leq \frac {\chi_ {2} \left(Q _ {1} \| Q _ {0}\right)}{2} \left(d + \frac {7}{4}\right) ^ {2} \frac {\log m}{m} + c _ {B, 6, d} \left(d + \frac {7}{4}\right) ^ {4} \frac {(\log m) ^ {2}}{m ^ {2}}.
$$

Both terms converge to zero as $m  \infty ,$ which holds for all s satisfying the condition of Lemma 2. In particular, for all sufficiently large $m , \vert M _ { m } ( s ) - 1 \vert \leq { \frac { 1 } { 2 } }$ . We define log $M _ { m } ( s )$ by the absolutely convergent power series

$$
\log M _ {m} (s) = \sum_ {k = 1} ^ {\infty} \frac {(- 1) ^ {k + 1}}{k} \left(M _ {m} (s) - 1\right) ^ {k}.
$$

This series defines the unique analytic logarithm in a neighborhood of one whose value at one is zero. Thus, although $M _ { m } ( s )$ may be complex, the quantity log $M _ { m } ( s )$ is unambiguously defined.

Separating the first-order term in this series gives

$$
\log M _ {m} (s) = M _ {m} (s) - 1 + \sum_ {k = 2} ^ {\infty} \frac {(- 1) ^ {k + 1}}{k} \left(M _ {m} (s) - 1\right) ^ {k}.
$$

Since $| M _ { m } ( s ) - 1 | \leq 1 / 2$ , we have

$$
\left| \log M _ {m} (s) - \left(M _ {m} (s) - 1\right) \right| \leq \sum_ {k = 2} ^ {\infty} | M _ {m} (s) - 1 | ^ {k} = \frac {| M _ {m} (s) - 1 | ^ {2}}{1 - | M _ {m} (s) - 1 |} \leq 2 | M _ {m} (s) - 1 | ^ {2}.
$$

Substituting the expansion obtained in (22) now yields

$$
\begin{array}{l} \log M _ {m} (s) = M _ {m} (s) - 1 + \left[ \log M _ {m} (s) - \left(M _ {m} (s) - 1\right) \right] \\ \qquad = \frac {\chi_ {2} \left(Q _ {1} \| Q _ {0}\right)}{2 m} s (s - 1) + R _ {m} (s) + \left[ \log M _ {m} (s) - \left(M _ {m} (s) - 1\right) \right]. \end{array}
$$

Accordingly, define

$$
r _ {m} (s) \triangleq R _ {m} (s) + \left[ \log M _ {m} (s) - \left(M _ {m} (s) - 1\right) \right],
$$

which absorbs the Taylor-expansion remainder $R _ { m } ( s )$ and the imprecision caused by taking the logarithm. Hence,

$$
\begin{array}{l} | r _ {m} (s) | \leq | R _ {m} (s) | + \left| \log M _ {m} (s) - \left(M _ {m} (s) - 1\right) \right| \\ \leq \frac {c _ {B , 6 , d} (1 + | s |) ^ {4}}{m ^ {2}} + 2 | M _ {m} (s) - 1 | ^ {2} \\ \leq \frac {c _ {B , 1 , d} (1 + | s |) ^ {4}}{m ^ {2}} \end{array}
$$

for some constant $^ { c _ { B , 1 , d } }$ . We have therefore proved that

$$
\log M _ {m} (s) = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + r _ {m} (s), \qquad | r _ {m} (s) | \leq \frac {c _ {B , 1 , d} (1 + | s |) ^ {4}}{m ^ {2}}.
$$

This completes the proof of Lemma 2.

## B. Proof of Proposition 1

Recall that $\begin{array} { r } { L _ { m , \ell } = \sum _ { j = 1 } ^ { \ell } \log \frac { P _ { m } ( \mathbf { Z } _ { j } ) } { Q _ { 0 } ^ { \otimes m } ( \mathbf { Z } _ { j } ) } } \end{array}$ . By the definitions of $\rho _ { m }$ and $H _ { m }$ in (4), we have

$$
\rho_ {m} = M _ {m} (1 / 2) \quad \text { and } \quad H _ {m} (\mathbf {z}) = \frac {Q _ {0} ^ {\otimes m} (\mathbf {z})}{M _ {m} (1 / 2)} \left(\frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}\right) ^ {1 / 2}.
$$

Therefore, the characteristic function of the log-likelihood ratio of one PPM block under $H _ { m }$ is

$$
\mathbb {E} _ {H _ {m}} \left[ \exp \left(i t \log \frac {P _ {m} (\mathbf {Z} _ {1})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {1})}\right) \right] = \frac {1}{M _ {m} (1 / 2)} \sum_ {\mathbf {z}} Q _ {0} ^ {\otimes m} (\mathbf {z}) \left(\frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}\right) ^ {1 / 2 + i t} = \frac {M _ {m} (1 / 2 + i t)}{M _ {m} (1 / 2)}.
$$

Consequently, independence across the ℓ blocks yields

$$
\varphi_ {L _ {m, \ell}} (t) = \mathbb {E} _ {H _ {m} ^ {\otimes \ell}} \left[ e ^ {i t L _ {m, \ell}} \right] = \left[ \frac {M _ {m} (1 / 2 + i t)}{M _ {m} (1 / 2)} \right] ^ {\ell}.\tag{23}
$$

Note that

$$
\log M _ {m} (1 / 2 + i t) = - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} t ^ {2} + r _ {m} (1 / 2 + i t),
$$

$$
\log M _ {m} (1 / 2) = - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{8 m} + r _ {m} (1 / 2).
$$

Substitution into the expression for $\varphi _ { L _ { m , \ell } } ( t )$ in (23) yields

$$
\varphi_ {L _ {m, \ell}} (t) = \exp \left\{- \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} t ^ {2} + \ell \left[ r _ {m} (1 / 2 + i t) - r _ {m} (1 / 2) \right] \right\}.\tag{24}
$$

It then follows from (24) that

$$
\begin{array}{r l} & {\left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right|} \\ & {= e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \times | \exp \left\{\ell \left[ r _ {m} (1 / 2 + i t) - r _ {m} (1 / 2) \right] \right\} - 1 |} \\ & {\leq e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \times | \ell \left[ r _ {m} (1 / 2 + i t) - r _ {m} (1 / 2) \right] | \times \exp \left\{| \ell \left[ r _ {m} (1 / 2 + i t) - r _ {m} (1 / 2) \right] | \right\},} \end{array}
$$

where the last inequality follows from the fact that $| e ^ { w } - 1 | \leq | w | e ^ { | w | }$ for $w \in \mathbb { C }$

On the range $| t | \leq d \sqrt { \log m }$ , it follows from Lemma 2 that

$$
| \ell [ r _ {m} (1 / 2 + i t) - r _ {m} (1 / 2) ] | \leq \frac {c _ {B , 1 , d} (1 + | t | ^ {4})}{m} \leq \frac {c _ {B , 1 , d} [ 1 + d ^ {4} (\log m) ^ {2} ]}{m} = o (1),
$$

and hence the exponential of this term is also bounded by a constant for all sufficiently large $m$ . Moreover, since $\ell / m \geq c _ { 0 }$ due to the condition of Theorem 1, we have

$$
e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \leq e ^ {- c _ {B, 7} t ^ {2}}, \quad \text { where } c _ {B, 7} \triangleq \frac {c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0})}{2} > 0.
$$

Therefore,

$$
\left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right| \leq \frac {c _ {B , 1 , d}}{m} (1 + | t | ^ {4}) \times e ^ {- c _ {B, 7} t ^ {2}}.\tag{25}
$$

Since $e ^ { - t ^ { 2 } / ( 2 m ) } \leq 1$ , the bound on the difference between the two characteristic functions in (25) yields

$$
\begin{array}{r l} & {\int_ {| t | \leq d \sqrt {\log m}} \mathcal {E} _ {m, \ell} (t) d t \leq \frac {c _ {B , 1 , d}}{m} \int_ {| t | \leq d \sqrt {\log m}} \frac {(1 + | t | ^ {4}) e ^ {- c _ {B , 7} t ^ {2}}}{t ^ {2} + 1 / 4} d t} \\ & {\qquad \leq \frac {c _ {B , 1 , d}}{m} \int_ {\mathbb {R}} \frac {(1 + | t | ^ {4}) e ^ {- c _ {B , 7} t ^ {2}}}{t ^ {2} + 1 / 4} d t} \\ & {\qquad = O (m ^ {- 1}),} \end{array}
$$

where the last step follows from the fact that the integral over R is finite and independent of m. This completes the proof of Proposition 1.

## APPENDIX C PROOF OF PROPOSITION 2

Proposition 2. There exist $u _ { 0 } > 0$ and $d _ { 0 } > 0$ such that, for every fixed $d \geq d _ { 0 }$

$$
\int_ {d \sqrt {\log m} <   | t | \leq u _ {0} \sqrt {m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).
$$

## A. Proof of An Auxiliary Result

In this subsection, we first prove that there exist constants $u _ { 0 } > 0$ and $c _ { C , 1 } > 0$ such that

$$
\left| \mathbb {E} _ {H _ {m}} \exp \left(i u \sqrt {m} \log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) \right| \leq e ^ {- c _ {C, 1} u ^ {2}}, \quad | u | \leq u _ {0}.
$$

For simplicity, we define

$$
X _ {m} \triangleq \sqrt {m} \log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}, \quad \text { where } \mathbf {Z} \sim H _ {m}.\tag{26}
$$

Let $X _ { m } ^ { \prime }$ be an independent copy of $X _ { m }$ . By independence, we have

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} = \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \times \overline {{\mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}}}} = \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \times \mathbb {E} _ {H _ {m}} e ^ {- i u X _ {m} ^ {\prime}} = \mathbb {E} e ^ {i u (X _ {m} - X _ {m} ^ {\prime})}.
$$

Since $X _ { m }$ and $X _ { m } ^ { \prime }$ are independent and identically distributed, the pairs $( X _ { m } , X _ { m } ^ { \prime } )$ and $( X _ { m } ^ { \prime } , X _ { m } )$ have the same distribution. Consequently,

$$
X _ {m} - X _ {m} ^ {\prime} \stackrel {\mathrm{d}} {=} X _ {m} ^ {\prime} - X _ {m} = - (X _ {m} - X _ {m} ^ {\prime}).
$$

Thus the distribution of $X _ { m } - X _ { m } ^ { \prime }$ is symmetric about zero.

Since the sine function is odd, this symmetry implies E sin $\left( u ( X _ { m } - X _ { m } ^ { \prime } ) \right) = 0$ . Therefore,

$$
\mathbb {E} e ^ {i u (X _ {m} - X _ {m} ^ {\prime})} = \mathbb {E} \cos \bigl (u (X _ {m} - X _ {m} ^ {\prime}) \bigr) + i \mathbb {E} \sin \bigl (u (X _ {m} - X _ {m} ^ {\prime}) \bigr) = \mathbb {E} \cos \bigl (u (X _ {m} - X _ {m} ^ {\prime}) \bigr).
$$

It follows that

$$
1 - \left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} = \mathbb {E} \left[ 1 - \cos \bigl (u (X _ {m} - X _ {m} ^ {\prime}) \bigr) \right].
$$

This is useful because the elementary inequality $\begin{array} { r } { 1 - \cos y \ge \frac { y ^ { 2 } } { 2 } - \frac { | y | ^ { 3 } } { 6 } } \end{array}$ for $y \in$ R converts the problem of estimating characteristic function into estimating the second and third moments of $X _ { m } - X _ { m } ^ { \prime }$

We first evaluate these moments. In Appendix H, we show that

$$
\mathrm{Var} _ {H _ {m}} (X _ {m}) = \chi_ {2} (Q _ {1} \| Q _ {0}) + O (m ^ {- 1}), \qquad \mathbb {E} _ {H _ {m}} \left| X _ {m} - \mathbb {E} _ {H _ {m}} X _ {m} \right| ^ {3} = O (1).
$$

Therefore,

$$
\mathbb {E} (X _ {m} - X _ {m} ^ {\prime}) ^ {2} = 2 \operatorname{Var} _ {H _ {m}} (X _ {m}) = 2 \chi_ {2} (Q _ {1} \| Q _ {0}) + O (m ^ {- 1}).
$$

Consequently, for all sufficiently large $m ,$

$$
\mathbb {E} (X _ {m} - X _ {m} ^ {\prime}) ^ {2} \geq \chi_ {2} (Q _ {1} \| Q _ {0}).
$$

Furthermore, note that

$$
X _ {m} - X _ {m} ^ {\prime} = \left(X _ {m} - \mathbb {E} _ {H _ {m}} X _ {m}\right) - \left(X _ {m} ^ {\prime} - \mathbb {E} _ {H _ {m}} X _ {m} ^ {\prime}\right).
$$

Using $| x - y | ^ { 3 } \leq 4 ( | x | ^ { 3 } + | y | ^ { 3 } )$ , we obtain

$$
\mathbb {E} | X _ {m} - X _ {m} ^ {\prime} | ^ {3} \leq 4 \mathbb {E} | X _ {m} - \mathbb {E} _ {H _ {m}} X _ {m} | ^ {3} + 4 \mathbb {E} | X _ {m} ^ {\prime} - \mathbb {E} _ {H _ {m}} X _ {m} ^ {\prime} | ^ {3} = O (1).
$$

Thus there exists a constant $c _ { C , 2 } > 0$ such that for sufficiently large m,

$$
\mathbb {E} | X _ {m} - X _ {m} ^ {\prime} | ^ {3} \leq c _ {C, 2},
$$

We now apply the cosine inequality. For sufficiently large m

$$
\begin{array}{r l} & {1 - \left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} = \mathbb {E} \left[ 1 - \cos \bigl (u (X _ {m} - X _ {m} ^ {\prime}) \bigr) \right]} \\ & {\qquad \geq \frac {u ^ {2}}{2} \mathbb {E} (X _ {m} - X _ {m} ^ {\prime}) ^ {2} - \frac {| u | ^ {3}}{6} \mathbb {E} | X _ {m} - X _ {m} ^ {\prime} | ^ {3}} \\ & {\qquad \geq \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2} u ^ {2} - \frac {c _ {C , 2}}{6} | u | ^ {3}.} \end{array}
$$

To ensure that the quadratic term dominates this error, choose $u _ { 0 } > 0$ sufficiently small that $\begin{array} { r } { \frac { c _ { C , 2 } } { 6 } u _ { 0 } \leq \frac { \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) } { 4 } } \end{array}$ Then, for every $\begin{array} { r } { | u | \leq u _ { 0 } , \ \frac { c _ { C , 2 } } { 6 } | u | ^ { 3 } \leq \frac { \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) } { 4 } u ^ { 2 } } \end{array}$ , and therefore

$$
1 - \left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} \geq \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{4} u ^ {2}.
$$

Equivalently,

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} \leq 1 - \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{4} u ^ {2}.
$$

We can further choose $u _ { 0 }$ such that $\begin{array} { r } { 0 \leq \frac { \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } { 4 } u ^ { 2 } \leq 1 } \end{array}$ for all $| u | \leq u _ { 0 }$ . Using $1 - x \leq e ^ { - x }$ for $x \ge 0 .$ , we obtain

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| ^ {2} \leq \exp \left(- \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{4} u ^ {2}\right).
$$

Therefore, we obtain

$$
\left| \mathbb {E} _ {H _ {m}} \exp \left(i u \sqrt {m} \log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) \right| \leq \exp \left(- c _ {C, 1} u ^ {2}\right), \quad | u | \leq u _ {0}.
$$

where $\begin{array} { r } { c _ { C , 1 } = \frac { \chi _ { 2 } ( Q _ { 1 } | | Q _ { 0 } ) } { 8 } > 0 . } \end{array}$

## B. Proof of Proposition 2

For $\left| t \right| \leq u _ { 0 } \sqrt { m }$ , taking $u = t / \sqrt { m }$ yields

$$
\left| \mathbb {E} _ {H _ {m}} \exp \left(i t \log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) \right| \leq e ^ {- c _ {C, 1} t ^ {2} / m}.
$$

Since $\varphi _ { L _ { m , \ell } } ( t )$ is the ℓ-th power of this characteristic function, we have

$$
| \varphi_ {L _ {m, \ell}} (t) | \leq e ^ {- c _ {C, 1} \ell t ^ {2} / m} \leq e ^ {- c _ {C, 1} c _ {0} t ^ {2}},\tag{27}
$$

where the last inequality follows from $\ell / m \geq c _ { 0 }$ . The characteristic function of Gaussian variable $N _ { m , \ell }$ satisfies

$$
e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \leq e ^ {- c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / 2}.
$$

Define b <sup>≜</sup> min $\begin{array} { r } { \left\{ c _ { C , 1 } c _ { 0 } , \frac { c _ { 0 } \chi _ { 2 } \left( Q _ { 1 } \| Q _ { 0 } \right) } { 2 } \right\} > 0 } \end{array}$ . The triangle inequality and (27) then give

$$
\left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right| \leq | \varphi_ {L _ {m, \ell}} (t) | + e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \leq 2 e ^ {- b t ^ {2}}.
$$

Recalling the definition

$$
\mathcal {E} _ {m, \ell} (t) = \frac {e ^ {- t ^ {2} / (2 m)}}{t ^ {2} + 1 / 4} \left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right|,
$$

and using the facts $e ^ { - t ^ { 2 } / ( 2 m ) } \leq 1$ and $\frac { 1 } { t ^ { 2 } + 1 / 4 } \leq 4 $ , we obtain $\mathcal { E } _ { m , \ell } ( t ) \leq 8 e ^ { - b t ^ { 2 } }$ throughout the range considered in Proposition 2. Consequently,

$$
\int_ {d \sqrt {\log m} <   | t | \leq u _ {0} \sqrt {m}} \mathcal {E} _ {m, \ell} (t) d t \leq 8 \int_ {| t | > d \sqrt {\log m}} e ^ {- b t ^ {2}} d t.
$$

For every $x > 0 ,$

$$
\int_ {| t | > x} e ^ {- b t ^ {2}} d t \leq e ^ {- b x ^ {2} / 2} \int_ {\mathbb {R}} e ^ {- b t ^ {2} / 2} d t = \sqrt {\frac {2 \pi}{b}} e ^ {- b x ^ {2} / 2}.
$$

Taking $x = d \sqrt { \log m }$ therefore gives

$$
\int_ {d \sqrt {\log m} <   | t | \leq u _ {0} \sqrt {m}} \mathcal {E} _ {m, \ell} (t) d t \leq 8 \sqrt {\frac {2 \pi}{b}} e ^ {- b d ^ {2} \log m / 2} = 8 \sqrt {\frac {2 \pi}{b}} m ^ {- b d ^ {2} / 2}.
$$

Choose $d _ { 0 } > 0$ such that $\frac { b d _ { 0 } ^ { 2 } } { 2 } \geq 1$ . Then, for every $d \geq d _ { 0 }$ , we have $m ^ { - b d ^ { 2 } / 2 } \leq m ^ { - 1 }$ . This completes the proof of Proposition 2. □

## APPENDIX D

## PROOF OF PROPOSITION 3

Proposition 3. For every fixed $k > 0 .$ , there exists a constant $c _ { 3 , k } > 0$ such that

$$
\int_ {u _ {0} \sqrt {m} <   | t | \leq \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t = O (e ^ {- c _ {3, k} m}),
$$

where $u _ { 0 } > 0$ is the constant chosen in Proposition 2.

## A. Proof of An Auxiliary Result

In this subsection, we first prove that for every fixed $k > 0$ , there exists a constant $\eta _ { k } \in ( 0 , 1 )$ such that

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| = \left| \mathbb {E} _ {H _ {m}} \exp \left(i u \sqrt {m} \log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) \right| \leq \eta_ {k}
$$

uniformly over $u _ { 0 } \leq | u | \leq \sqrt { k \log m }$ , where the random variable $X _ { m }$ is introduced in Appendix C. Note that random variable $X _ { m }$ is not a sum of independent random variables under $H _ { m }$ . We therefore introduce

$$
Y _ {m} \triangleq \sqrt {m} B _ {m} = \frac {1}{\sqrt {m}} \sum_ {j = 1} ^ {m} A (Z _ {j}),
$$

where $A ( . )$ is the single-letter quantity introduced in Appendix B. Under $Q _ { 0 } ^ { \otimes m }$ , the characteristic function of $Y _ { m }$ factors into m single-letter characteristic functions. The proof will show that replacing $X _ { m }$ by $Y _ { m }$ , and then replacing $H _ { m }$ by $Q _ { 0 } ^ { \otimes m }$ , introduces only a vanishing error.

1) Replacing $X _ { m } \ B y \ Y _ { m }$ under $H _ { m } .$ On the event ${ \mathcal { E } } _ { m }$ introduced in Section III, the quantity $1 + B _ { m }$ is bounded below by $1 / 2 .$ . Using log $\begin{array} { r } { ( 1 + x ) - x = - \int _ { 0 } ^ { x } \frac { t } { 1 + t } } \end{array}$ dt for $x > - 1$ , we obtain that, for $| x | \leq 1 / 2$

$$
| \log (1 + x) - x | \leq \int_ {0} ^ {| x |} \frac {t}{1 - t} d t \leq \int_ {0} ^ {| x |} 2 t d t = | x | ^ {2}.
$$

Applying this inequality with $x = B _ { m }$ leads to

$$
| \log (1 + B _ {m}) - B _ {m} | \leq B _ {m} ^ {2}
$$

on ${ \mathcal { E } } _ { m }$ . Therefore, we have

$$
\left| X _ {m} - Y _ {m} \right| = \sqrt {m} \left| \log (1 + B _ {m}) - B _ {m} \right| \leq \sqrt {m} B _ {m} ^ {2}.
$$

We next take the expectation under $H _ { m }$ . First, one can verify that

$$
\frac {H _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})} = \frac {\sqrt {1 + B _ {m} (\mathbf {z})}}{\rho_ {m}}.
$$

Since $A ( Z )$ is bounded, $B _ { m }$ is bounded uniformly in $m ,$ and hence $\sqrt { 1 + B _ { m } }$ is also uniformly bounded. Moreover,

$$
| \rho_ {m} - 1 | = \left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \sqrt {1 + B _ {m}} - 1 \right| \leq \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left| \sqrt {1 + B _ {m}} - 1 \right| \leq \mathbb {E} _ {Q _ {0} ^ {\otimes m}} | B _ {m} | \leq \sqrt {\mathbb {E} _ {Q _ {0} ^ {\otimes m}} B _ {m} ^ {2}} = \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}}.
$$

Thus, for all sufficiently large m, we have $\rho _ { m } \ge 1 / 2$ , and hence there exists a constant $c _ { D , 1 } > 0$ such that for all z,

$$
H _ {m} (\mathbf {z}) \leq c _ {D, 1} Q _ {0} ^ {\otimes m} (\mathbf {z}).
$$

Therefore,

$$
\begin{array}{r l} & {\mathbb {E} _ {H _ {m}} \left[ | X _ {m} - Y _ {m} | \mathbf {1} _ {\{| B _ {m} | \leq 1 / 2 \}} \right] \leq \sqrt {m} \mathbb {E} _ {H _ {m}} \left[ B _ {m} ^ {2} \mathbf {1} _ {\{| B _ {m} | \leq 1 / 2 \}} \right]} \\ & {\qquad \leq c _ {D, 1} \sqrt {m} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} B _ {m} ^ {2}} \\ & {\qquad = c _ {D, 1} \sqrt {m} \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m} = O (m ^ {- 1 / 2}).} \end{array}
$$

It remains to control the event $\{ | B _ { m } | > 1 / 2 \}$ . Since (9) shows that $\begin{array} { r } { Q _ { 0 } ^ { \otimes m } \big ( | B _ { m } | > \frac { 1 } { 2 } \big ) \leq 2 \exp { \left( - \frac { m } { 2 ( a _ { \mathrm { m a x } } - a _ { \mathrm { m i n } } ) ^ { 2 } } \right) } } \end{array}$ we obtain

$$
H _ {m} \{| B _ {m} | > 1 / 2 \} \leq 2 c _ {D, 1} \exp \left(- \frac {m}{2 (a _ {\max} - a _ {\min}) ^ {2}}\right).
$$

By calculating that $\begin{array} { r } { \operatorname* { s u p } _ { \mathcal { E } _ { m } ^ { c } \cap \mathrm { s u p p } ( H _ { m } ) } | X _ { m } - Y _ { m } | = O ( \sqrt { m } \log m ) } \end{array}$ , we obtain

$$
\mathbb {E} _ {H _ {m}} \left[ | X _ {m} - Y _ {m} | \mathbf {1} _ {\{| B _ {m} | > 1 / 2 \}} \right] = O \big (e ^ {- (1 / 2 (a _ {\max} - a _ {\min}) ^ {2}) m} \big).
$$

Combining the two events together yields that

$$
\mathbb {E} _ {H _ {m}} | X _ {m} - Y _ {m} | = O (m ^ {- 1 / 2}).
$$

This further helps to control the change in the characteristic function caused by replacing $X _ { m }$ with $Y _ { m }$ . Since $| e ^ { i a } - e ^ { i b } | \leq | a - b |$ for $a , b \in \mathbb { R }$ , we have, for some constant $c _ { D , 2 } > 0$

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} - \mathbb {E} _ {H _ {m}} e ^ {i u Y _ {m}} \right| \leq \mathbb {E} _ {H _ {m}} \left| e ^ {i u X _ {m}} - e ^ {i u Y _ {m}} \right| \leq | u | \mathbb {E} _ {H _ {m}} | X _ {m} - Y _ {m} | \leq \frac {c _ {D , 2} | u |}{\sqrt {m}}.
$$

2) Replacing $H _ { m } \ B y \ Q _ { 0 } ^ { \otimes m }$ : We next show that the expectation of $e ^ { i u Y _ { m } }$ changes by only $O ( m ^ { - 1 / 2 } )$ when the underlying distribution is changed from $H _ { m }$ $Q _ { 0 } ^ { \otimes m }$ . By the definition of $H _ { m }$

$$
\sum_ {\mathbf {z}} \left| H _ {m} (\mathbf {z}) - Q _ {0} ^ {\otimes m} (\mathbf {z}) \right| = \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left| \frac {\sqrt {1 + B _ {m}}}{\rho_ {m}} - 1 \right| = \frac {1}{\rho_ {m}} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left| \sqrt {1 + B _ {m}} - \rho_ {m} \right|.
$$

Using the triangle inequality, we have

$$
\left| \sqrt {1 + B _ {m}} - \rho_ {m} \right| \leq \left| \sqrt {1 + B _ {m}} - 1 \right| + | 1 - \rho_ {m} |.
$$

Note that

$$
\mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left| \sqrt {1 + B _ {m}} - 1 \right| \leq \mathbb {E} _ {Q _ {0} ^ {\otimes m}} | B _ {m} | \leq \sqrt {\mathbb {E} _ {Q _ {0} ^ {\otimes m}} [ B _ {m} ^ {2} ]} = \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}}
$$

and

$$
\left| 1 - \rho_ {m} \right| = \left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ 1 - \sqrt {1 + B _ {m}} \right] \right| \leq \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left| 1 - \sqrt {1 + B _ {m}} \right| \leq \sqrt {\frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}}.
$$

Since $\rho _ { m } \ge 1 / 2$ for all sufficiently large $m ,$ there exists a constant $c _ { D , 3 } > 0$ such that

$$
\sum_ {\mathbf {z}} \left| H _ {m} (\mathbf {z}) - Q _ {0} ^ {\otimes m} (\mathbf {z}) \right| \leq \frac {c _ {D , 3}}{\sqrt {m}}.
$$

Because $| e ^ { i u Y _ { m } } | = 1$ , we have

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u Y _ {m}} - \mathbb {E} _ {Q _ {0} ^ {\otimes m}} e ^ {i u Y _ {m}} \right| \leq \sum_ {\mathbf {z}} \left| H _ {m} (\mathbf {z}) - Q _ {0} ^ {\otimes m} (\mathbf {z}) \right| | e ^ {i u Y _ {m} (\mathbf {z})} | \leq \frac {c _ {D , 3}}{\sqrt {m}}.
$$

Combining the above analyses, we obtain, for some constant $c _ { D , 4 } > 0$

$$
\begin{array}{r l} & {\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} - \mathbb {E} _ {Q _ {0} ^ {\otimes m}} e ^ {i u Y _ {m}} \right| \leq \left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} - \mathbb {E} _ {H _ {m}} e ^ {i u Y _ {m}} \right| + \left| \mathbb {E} _ {H _ {m}} e ^ {i u Y _ {m}} - \mathbb {E} _ {Q _ {0} ^ {\otimes m}} e ^ {i u Y _ {m}} \right|} \\ & {\qquad \leq \frac {c _ {D , 4} (1 + | u |)}{\sqrt {m}}.} \end{array}
$$

This allows us to replace the nonlinear midpoint variable $X _ { m }$ by the sum of i.i.d. random variables $Y _ { m }$

3) Calculating the Characteristic Function of $Y _ { m }$ : Define the single-letter characteristic function

$$
\varphi_ {A} (s) \triangleq \mathbb {E} _ {Q _ {0}} e ^ {i s A (Z)},
$$

and note that

$$
\mathbb {E} _ {Q _ {0} ^ {\otimes m}} \left[ e ^ {i u Y _ {m}} \right] = \mathbb {E} _ {Q _ {0} ^ {\otimes m}} \exp \left(\frac {i u}{\sqrt {m}} \sum_ {j = 1} ^ {m} A (Z _ {j})\right) = \varphi_ {A} (u / \sqrt {m}) ^ {m}.
$$

We next prove that $\left| \varphi _ { A } ( s ) \right|$ has a quadratic gap below one for sufficiently small s. Let $A ( Z ^ { \prime } )$ be an independent copy of $A ( Z )$ . Symmetrization implies

$$
| \varphi_ {A} (s) | ^ {2} = \mathbb {E} [ e ^ {i s (A (Z) - A (Z ^ {\prime}))} ] = \mathbb {E} [ \cos {(s (A (Z) - A (Z ^ {\prime})))} ],
$$

where the imaginary part vanishes because $A ( Z ) - A ( Z ^ { \prime } )$ has a symmetric distribution. Hence

$$
1 - | \varphi_ {A} (s) | ^ {2} = \mathbb {E} \left[ 1 - \cos \left(s (A (Z) - A (Z ^ {\prime}))\right) \right].
$$

Using 1 − cos x $\geq { \frac { x ^ { 2 } } { 2 } } - { \frac { | x | ^ { 3 } } { 6 } }$ for $x \in \mathbb { R }$ , we obtain

$$
1 - \left| \varphi_ {A} (s) \right| ^ {2} \geq \frac {s ^ {2}}{2} \mathbb {E} \left[ \left(A (Z) - A (Z ^ {\prime})\right) ^ {2} \right] - \frac {| s | ^ {3}}{6} \mathbb {E} \left[ \left| A (Z) - A (Z ^ {\prime}) \right| ^ {3} \right].
$$

Note that $\begin{array} { r } { \mathbb { E } \left[ ( A ( Z ) - A ( Z ^ { \prime } ) ) ^ { 2 } \right] = 2 \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) } \end{array}$ . The third absolute moment is finite because $A ( Z )$ is bounded. Therefore, there exists a constant $c _ { D , 5 } > 0$ such that

$$
1 - | \varphi_ {A} (s) | ^ {2} \geq \chi_ {2} (Q _ {1} \| Q _ {0}) s ^ {2} - c _ {D, 5} | s | ^ {3}.
$$

Choosing $s _ { 0 } > 0$ sufficiently small implies that for all $| s | \leq s _ { 0 }$ 2

$$
1 - | \varphi_ {A} (s) | ^ {2} \geq \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2} s ^ {2}.
$$

Let $c _ { D , 6 } \triangleq { \frac { \chi _ { 2 } ( Q _ { 1 } \Vert Q _ { 0 } ) } { 4 } }$ . Hence

$$
| \varphi_ {A} (s) | \leq \exp (- c _ {D, 6} s ^ {2}), \qquad | s | \leq s _ {0}.
$$

Fix $k > 0 . \mathrm { I f } \ | u | \le \sqrt { k \log m }$ , then $\begin{array} { r } { \frac { | u | } { \sqrt { m } } \leq \sqrt { \frac { k \log m } { m } } } \end{array}$ , which is smaller than $s _ { 0 }$ for all sufficiently large m. Therefore,

$$
\left| \mathbb {E} _ {Q _ {0} ^ {\otimes m}} e ^ {i u Y _ {m}} \right| = | \varphi_ {A} (u / \sqrt {m}) | ^ {m} \leq \left[ \exp \left(- c _ {D, 6} \frac {u ^ {2}}{m}\right) \right] ^ {m} = e ^ {- c _ {D, 6} u ^ {2}}.
$$

Combining this bound with the approximation obtained in Steps 1 and 2 gives

$$
\left| \mathbb {E} _ {H _ {m}} e ^ {i u X _ {m}} \right| \leq e ^ {- c _ {D, 6} u ^ {2}} + \frac {c _ {D , 4} (1 + | u |)}{\sqrt {m}}, \quad | u | \leq \sqrt {k \log m}.
$$

Finally, letting $\begin{array} { r } { \eta _ { k } \triangleq \frac { 1 + e ^ { - c _ { D , 6 } u _ { 0 } ^ { 2 } } } { 2 } \in ( 0 , 1 ) } \end{array}$ , one can check that for all $u _ { 0 } \leq | u | \leq \sqrt { k \log m } , \left| \mathbb { E } _ { H _ { m } } e ^ { i u X _ { m } } \right| \leq \eta _ { k }$

## B. Proof of Proposition 3

Consider the range $u _ { 0 } { \sqrt { m } } < | t | \leq { \sqrt { k m \log m } }$ . Taking $u = t / \sqrt { m }$ places u in the range $u _ { 0 } < | u | \leq \sqrt { k \log m }$ By independence across the ℓ blocks, we have

$$
| \varphi_ {L _ {m, \ell}} (t) | \leq \eta_ {k} ^ {\ell} = \exp (\ell \log \eta_ {k}) \leq \exp (c _ {0} m \log \eta_ {k}) = e ^ {- c _ {D, 7, k} m},
$$

where $c _ { D , 7 , k } \triangleq - c _ { 0 }$ log $\eta _ { k } > 0$

The characteristic function of Gaussian variable $N _ { m , \ell }$ is exponentially small on the same range. Indeed, using $\ell / m \geq c _ { 0 }$ and $\left| t \right| \geq u _ { 0 } \sqrt { m }$ , we obtain

$$
e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \leq e ^ {- c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / 2} \leq e ^ {- c _ {D, 8} m},
$$

where $c _ { D , 8 } \triangleq \frac { c _ { 0 } \chi _ { 2 } ( Q _ { 1 } \| Q _ { 0 } ) u _ { 0 } ^ { 2 } } { 2 } > 0$ . Let $c _ { D , 9 , k } \triangleq \operatorname* { m i n } \{ c _ { D , 7 , k } , c _ { D , 8 } \} > 0$ . It follows from the triangle inequality that

$$
\left| \varphi_ {L _ {m, \ell}} (t) - e ^ {- \ell \chi_ {2} (Q _ {1} \| Q _ {0}) t ^ {2} / (2 m)} \right| \leq 2 e ^ {- c _ {D, 9, k} m}.
$$

Since $e ^ { - t ^ { 2 } / ( 2 m ) } \ \leq \ 1$ and $\frac { 1 } { t ^ { 2 } + 1 / 4 } \ \leq \ 4$ , the definition of $\mathcal { E } _ { m , \ell } ( t )$ yields $\mathcal { E } _ { m , \ell } ( t ) \ \leq \ 8 e ^ { - c _ { D , 9 , k } m }$ throughout the uniform-contraction range. The total length of this range is at most $2 \sqrt { k m }$ log m. Therefore,

$$
\int_ {u _ {0} \sqrt {m} <   | t | \leq \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t \leq 1 6 \sqrt {k m \log m} e ^ {- c _ {D, 9, k} m}.
$$

Since a polynomial factor is dominated by any positive exponential, we obtain

$$
\int_ {u _ {0} \sqrt {m} <   | t | \leq \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t = O \left(e ^ {- c _ {D, 9, k} m / 2}\right),
$$

which completes the proof of Proposition 3 by setting $c _ { 3 , k } = c _ { D , 9 , k } / 2$

## APPENDIX E PROOF OF PROPOSITION 4

Proposition 4. For every fixed $k \geq 1$

$$
\int_ {| t | > \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t = O (m ^ {- 1}).
$$

Proof. By noting that both characteristic functions in (15) have modulus at most one, we obtain

$$
\begin{array}{r l} & {\int_ {| t | > \sqrt {k m \log m}} \mathcal {E} _ {m, \ell} (t) d t \leq 4 \int_ {\sqrt {k m \log m}} ^ {\infty} \frac {e ^ {- t ^ {2} / (2 m)}}{t ^ {2}} d t} \\ & {\qquad = \frac {4}{\sqrt {m}} \int_ {\sqrt {k \log m}} ^ {\infty} \frac {e ^ {- u ^ {2} / 2}}{u ^ {2}} d u} \\ & {\qquad = O \left(m ^ {- (k + 1) / 2} (\log m) ^ {- 3 / 2}\right),} \end{array}
$$

where the last step follows since

$$
\int_ {a} ^ {\infty} \frac {e ^ {- u ^ {2} / 2}}{u ^ {2}} d u \leq \frac {e ^ {- a ^ {2} / 2}}{a ^ {3}}.
$$

Therefore, (18) holds for every $k \geq 1$

## APPENDIX F PROOF OF PROPOSITION 5

Proposition 5 (Desmoothing error). The two desmoothing error terms satisfy

$$
| \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (L _ {m, \ell}) ] | = O (m ^ {- 1}), \qquad | \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] | = O (m ^ {- 1}).
$$

In Lemma 3 below, we provide an anti-concentration bound that controls the probability that $L _ { m , \ell }$ lies in any short interval. In particular, it will be applied to the random interval $[ - | G _ { m } | , | G _ { m } | ]$ to control the event on which adding $G _ { m }$ crosses the origin, where $h ( x ) = \exp ( - | x | / 2 )$ is not differentiable.

Lemma 3 (Uniform anti-concentration bound). There exists a constant $c _ { F , 1 } > 0$ such that, uniformly over $a \in \mathbb { R }$ and $s \geq 0 ,$

$$
\operatorname * {P r} \left\{a \leq L _ {m, \ell} \leq a + s \right\} \leq c _ {F, 1} \left(s + m ^ {- 1 / 2}\right).
$$

Proof of Lemma 3. For simplicity, we write

$$
\mu_ {m} \triangleq \mathbb {E} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right), \quad \sigma_ {m} ^ {2} \triangleq \operatorname{Var} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right).
$$

In Appendix H, we prove that

$$
\begin{array}{r l} & {\mu_ {m} = O (m ^ {- 2}), \quad \sigma_ {m} ^ {2} = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m} + O (m ^ {- 2}),} \\ & {\mathbb {E} _ {H _ {m}} \left| \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right) - \mathbb {E} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right) \right| ^ {3} = O (m ^ {- 3 / 2}).} \end{array}\tag{28}
$$

(29)

Let $G _ { 0 } \sim { \cal N } ( 0 , 1 )$ , and define the standardized version of $L _ { m , \ell }$ as

$$
S _ {m, \ell} \triangleq \frac {L _ {m , \ell} - \ell \mu_ {m}}{\sqrt {\ell} \sigma_ {m}}.
$$

By (28) and the assumption $c _ { 0 } \leq \ell / m \leq c _ { 1 }$ , we note that

$$
\ell \sigma_ {m} ^ {2} = \frac {\ell}{m} \chi_ {2} (Q _ {1} \| Q _ {0}) + O (m ^ {- 1})
$$

is bounded above and bounded away from zero. The Berry–Esseen theorem therefore yields

$$
\sup _ {x \in \mathbb {R}} | \operatorname * {P r} \{S _ {m, \ell} \leq x \} - \operatorname * {P r} \{G _ {0} \leq x \} | \leq c _ {F, 2} \frac {\ell \mathbb {E} _ {H _ {m}} \left| \log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})} - \mu_ {m} \right| ^ {3}}{(\ell \sigma_ {m} ^ {2}) ^ {3 / 2}} = O (m ^ {- 1 / 2}),
$$

where the last step follows from (28) and (29). Fix $a \in \mathbb { R } , s \geq 0$ , and $\eta > 0$ . Applying the Berry–Esseen bound twice yields

$$
\begin{array}{r l} & {\operatorname * {P r} \{a \leq L _ {m, \ell} \leq a + s \} \leq \operatorname * {P r} \{a - \eta <   L _ {m, \ell} \leq a + s \}} \\ & {\qquad = \operatorname * {P r} \left\{\frac {a - \eta - \ell \mu_ {m}}{\sqrt {\ell} \sigma_ {m}} <   S _ {m, \ell} \leq \frac {a + s - \ell \mu_ {m}}{\sqrt {\ell} \sigma_ {m}} \right\}} \\ & {\qquad \leq \operatorname * {P r} \left\{\frac {a - \eta - \ell \mu_ {m}}{\sqrt {\ell} \sigma_ {m}} <   G _ {0} \leq \frac {a + s - \ell \mu_ {m}}{\sqrt {\ell} \sigma_ {m}} \right\} + O (m ^ {- 1 / 2}).} \end{array}
$$

The distance between the two endpoints is $\begin{array} { r } { \frac { s + \eta } { \sqrt { \ell } \sigma _ { m } } \le c _ { F , 3 } ( s + \eta ) } \end{array}$ for some constant $_ { c _ { F , 3 } }$ , since $\sqrt { \ell } \sigma _ { m }$ is bounded away from zero. Since the density of standard Gaussian random variable $G _ { 0 }$ is bounded by $1 / { \sqrt { 2 \pi } }$ , we obtain

$$
\operatorname * {P r} \{a \leq L _ {m, \ell} \leq a + s \} \leq \frac {c _ {F , 3} (s + \eta)}{\sqrt {2 \pi}} + O (m ^ {- 1 / 2}).
$$

Letting $\eta \downarrow 0$ yields

$$
\operatorname * {P r} \{a \leq L _ {m, \ell} \leq a + s \} \leq \frac {c _ {F , 3} s}{\sqrt {2 \pi}} + O (m ^ {- 1 / 2}) \leq c _ {F, 1} \left(s + m ^ {- 1 / 2}\right).
$$

The enlargement of the interval at its lower endpoint ensures that the argument also covers a possible atom at a.

$$
G _ {m}
$$

Lemma 4 (Perturbation bound for h). Set $h ^ { \prime } ( 0 ) = 0$ . Then, for all $x , y \in \mathbb { R }$

$$
| h (x + y) - h (x) - y h ^ {\prime} (x) | \leq y ^ {2} + | y | \mathbf {1} _ {\{| x | \leq | y | \}}.\tag{30}
$$

Proof of Lemma 4. First, one can verify that for $\begin{array} { r } { u \neq 0 , | h ^ { \prime } ( u ) | \leq \frac { 1 } { 2 } } \end{array}$ and $\begin{array} { r } { | h ^ { \prime \prime } ( u ) | \leq \frac { 1 } { 4 } } \end{array}$ . Suppose that $x ( x + y ) > 0 .$ so that the segment between x and $x + y$ does not contain the origin. Taylor’s theorem implies, for some point ξ between x and $x + y$

$$
h (x + y) = h (x) + y h ^ {\prime} (x) + \frac {y ^ {2}}{2} h ^ {\prime \prime} (\xi).
$$

Therefore, we obtain

$$
| h (x + y) - h (x) - y h ^ {\prime} (x) | \leq \frac {y ^ {2}}{2} \sup _ {u \neq 0} | h ^ {\prime \prime} (u) | \leq \frac {y ^ {2}}{8}.
$$

It remains to consider $x ( x + y ) \leq 0 .$ , in which case the segment between x and $x + y$ crosses or touches the origin. This implies $| x | \le | y |$ , and hence $\mathbf { 1 } _ { \{ | x | \leq | y | \} } = 1$ . Moreover, note that h is $1 / 2 \AA \mathrm { - } 1$ Lipschitz because

$$
| h (v) - h (w) | \leq \frac {1}{2} | v - w |, \quad \forall v, w \in \mathbb {R}.
$$

Using this property and $| h ^ { \prime } ( x ) | \leq 1 / 2$ , with $h ^ { \prime } ( 0 ) = 0 .$ we obtain

$$
| h (x + y) - h (x) - y h ^ {\prime} (x) | \leq | h (x + y) - h (x) | + | y | | h ^ {\prime} (x) | \leq \frac {1}{2} | y | + \frac {1}{2} | y | = | y |.
$$

Combining the two cases completes the proof of Lemma 4.

Applying (30) pointwise with $x = L _ { m , \ell }$ and $y = G _ { m }$ yields

$$
\left| h \left(L _ {m, \ell} + G _ {m}\right) - h \left(L _ {m, \ell}\right) - G _ {m} h ^ {\prime} \left(L _ {m, \ell}\right) \right| \leq G _ {m} ^ {2} + \left| G _ {m} \right| \mathbf {1} _ {\{| L _ {m, \ell} | \leq | G _ {m} | \}}
$$

almost surely. Since $G _ { m } \sim N ( 0 , m ^ { - 1 } )$ is independent of $L _ { m , \ell }$ and $\mathbb { E } [ G _ { m } ] = 0$ , we have

$$
\mathbb {E} \left[ G _ {m} h ^ {\prime} (L _ {m, \ell}) \right] = 0.
$$

Taking expectations in the preceding pointwise inequality and using $| \mathbb { E } X | \leq \mathbb { E } | X |$ , we obtain

$$
\left. \right.\left| \mathbb {E} \left[ h \left(L _ {m, \ell} + G _ {m}\right)\right] - \mathbb {E} \left[ h \left(L _ {m, \ell}\right)\right]\right| \leq \mathbb {E} \left[ G _ {m} ^ {2} \right] + \mathbb {E} \left[ | G _ {m} | \mathbf {1} _ {\{| L _ {m, \ell} | \leq | G _ {m} | \}} \right].
$$

Condition on $G _ { m } = g$ . Since $G _ { m }$ is independent of $L _ { m , \ell } ,$ Lemma 3 applied to the interval $[ - | g | , | g | ]$ , whose length is $2 | g |$ , gives

$$
\operatorname * {P r} \left\{\left| L _ {m, \ell} \right| \leq \left| G _ {m} \right| \mid G _ {m} = g \right\} = \operatorname * {P r} \left\{- | g | \leq L _ {m, \ell} \leq | g | \right\} \leq 2 c _ {F, 1} \left(| g | + m ^ {- 1 / 2}\right).
$$

Hence, by the law of iterated expectations,

$$
\begin{array}{l} \mathbb {E} \left[ | G _ {m} | \mathbf {1} _ {\{| L _ {m, \ell} | \leq | G _ {m} | \}} \right] = \mathbb {E} \left[ \mathbb {E} \left[ | G _ {m} | \mathbf {1} _ {\{| L _ {m, \ell} | \leq | G _ {m} | \}} \big | G _ {m} \right] \right] \\ \qquad = \mathbb {E} \left[ | G _ {m} | \operatorname * {P r} \left\{| L _ {m, \ell} | \leq | G _ {m} |   | G _ {m} \right\} \right] \\ \qquad \leq 2 c _ {F, 1} \mathbb {E} \left[ | G _ {m} | \left(| G _ {m} | + m ^ {- 1 / 2}\right) \right] \\ \qquad = 2 c _ {F, 1} \mathbb {E} G _ {m} ^ {2} + 2 c _ {F, 1} m ^ {- 1 / 2} \mathbb {E} | G _ {m} |, \end{array}
$$

which scales as $O ( m ^ { - 1 } )$ since the Gaussian variable $G _ { m } \sim N ( 0 , m ^ { - 1 } )$ satisfies E $\begin{array} { r } { [ G _ { m } ^ { 2 } ] = \frac { 1 } { m } } \end{array}$ and $\begin{array} { r } { \mathbb { E } [ | G _ { m } | ] = \sqrt { \frac { 2 } { \pi m } } } \end{array}$ Therefore, we obtain

$$
| \mathbb {E} [ h (L _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (L _ {m, \ell}) ] | = O (m ^ {- 1}).
$$

Next, we bound the term $\lvert \mathbb { E } [ h ( N _ { m , \ell } + G _ { m } ) ] - \mathbb { E } [ h ( N _ { m , \ell } ) ] \rvert$ . Since

$$
\mathrm{Var} (N _ {m, \ell}) = \frac {\ell \chi_ {2} (Q _ {1} \| Q _ {0})}{m} \geq c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0}) > 0,
$$

the density of $N _ { m , \ell }$ satisfies

$$
f _ {N _ {m, \ell}} (x) = \sqrt {\frac {m}{2 \pi \ell \chi_ {2} (Q _ {1} \| Q _ {0})}} \exp \left(- \frac {m x ^ {2}}{2 \ell \chi_ {2} (Q _ {1} \| Q _ {0})}\right) \leq \frac {1}{\sqrt {2 \pi c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0})}}.
$$

Conditioning on $G _ { m } = g$ and using the independence of $G _ { m }$ and $N _ { m , \ell } ,$ we obtain

$$
\operatorname * {P r} \left\{| N _ {m, \ell} | \leq | G _ {m} | \mid G _ {m} = g \right\} = \operatorname * {P r} \left\{- | g | \leq N _ {m, \ell} \leq | g | \right\} = \int_ {- | g |} ^ {| g |} f _ {N _ {m, \ell}} (x) d x \leq \frac {2 | g |}{\sqrt {2 \pi c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0})}}.
$$

Consequently,

$$
\operatorname * {P r} \left\{\left| N _ {m, \ell} \right| \leq \left| G _ {m} \right| \mid G _ {m} \right\} \leq \frac {2 \left| G _ {m} \right|}{\sqrt {2 \pi c _ {0} \chi_ {2} (Q _ {1} \| Q _ {0})}}.
$$

Applying (30) with $x = N _ { m , \ell }$ and $y = G _ { m }$ yields, for some constant $c _ { F , 4 } > 0 ;$

$$
| \mathbb {E} [ h (N _ {m, \ell} + G _ {m}) ] - \mathbb {E} [ h (N _ {m, \ell}) ] | \leq c _ {F, 4} \mathbb {E} [ G _ {m} ^ {2} ] + c _ {F, 4} \mathbb {E} \left[ | G _ {m} | \Pr \{| N _ {m, \ell} | \leq | G _ {m} | | G _ {m} \} \right] \leq O (m ^ {- 1}).
$$

## APPENDIX GPROOF OF PROPOSITION 6

We apply [19, Theorem 5] with the length-n, weight-ℓ PPM input distribution $\mathcal { P } _ { n , \ell }$ . That theorem reduces the random-coding argument to four verifications: a reliability bound for each PPM codeword, an information-spectrum bound for channel resolvability, a positive-probability condition ensuring that the reliability and resolvability properties hold simultaneously, and a covertness guarantee for the PPM-induced output distribution. We verify the first conditions in this order, whereas the last one is exactly the assumption in Proposition 6.

1) Choice of the message and key sizes. We choose the message size $M _ { n }$ such that

$$
M _ {n} \triangleq \left\lfloor \exp \left\{\ell D _ {P} - \sqrt {\ell V _ {P}} Q ^ {- 1} \left(\epsilon - \frac {\kappa}{\sqrt {\ell}}\right) - 1 3 \log n \right\} \right\rfloor ,
$$

where $\kappa > 0$ is a sufficiently large constant. We choose $K _ { n }$ as the smallest positive integer satisfying

$$
\log (M _ {n} K _ {n}) \geq \max \left\{\log M _ {n}, \ell D _ {Q} + n ^ {3 / 8} \right\}.
$$

2) Verification of the reliability condition. Let $P _ { Y , \mathrm { P P M } } ^ { n , \ell } ( \mathbf { Y } )$ be the distribution induced by the PPM input distribution and the channel $W _ { Y \mid X }$ . For every PPM codeword x, we define its information density as $\imath ( { \bf x } ; { \bf Y } ) : = \imath$ $\begin{array} { r } { \sum _ { j : x _ { j } = 1 } \log \frac { P _ { 1 } ( Y _ { j } ) } { P _ { 0 } ( Y _ { j } ) } } \end{array}$ . We first verify that, for all sufficiently large $n ,$

$$
\max _ {\mathbf {x} \in \mathcal {P} _ {n, \ell}} \operatorname * {P r} \left\{\imath (\mathbf {x}; \mathbf {Y}) \leq \log (n ^ {1 3} M _ {n}) \right\} + \frac {1}{n} \mathbb {E} _ {P _ {Y, \mathrm{PPM}} ^ {n, \ell}} \left[ \frac {P _ {Y , \mathrm{PPM}} ^ {n , \ell} (\mathbf {Y})}{P _ {0} ^ {\otimes n} (\mathbf {Y})} \right] \leq \epsilon ,
$$

Applying [19, Lemma 5] yields

$$
\operatorname * {P r} \left\{\imath (\mathbf {x}; \mathbf {Y}) \leq \log (n ^ {1 3} M _ {n}) \right\} \leq Q \left(\frac {\ell D _ {P} - \log (n ^ {1 3} M _ {n})}{\sqrt {\ell V _ {P}}}\right) + \frac {c _ {G , 1}}{\sqrt {\ell}},
$$

where $c _ { G , 1 } > 0$ depends only on the channel. By the definition of $M _ { n }$ , we have

$$
\frac {\ell D _ {P} - \log (n ^ {1 3} M _ {n})}{\sqrt {\ell V _ {P}}} = Q ^ {- 1} \left(\epsilon - \frac {\kappa}{\sqrt {\ell}}\right) + o (\ell^ {- 1 / 2}).
$$

Since $Q$ is Lipschitz on bounded intervals, we have

$$
Q \left(\frac {\ell D _ {P} - \log (n ^ {1 3} M _ {n})}{\sqrt {\ell V _ {P}}}\right) = \epsilon - \frac {\kappa}{\sqrt {\ell}} + o (\ell^ {- 1 / 2}).
$$

The second term in the reliability condition is controlled by [19, Lemma 6]:

$$
\mathbb {E} _ {P _ {Y, \mathrm{PPM}} ^ {n, \ell}} \left[ \frac {P _ {Y , \mathrm{PPM}} ^ {n , \ell} (\mathbf {Y})}{P _ {0} ^ {\otimes n} (\mathbf {Y})} \right] \leq \exp \left(\frac {\ell (\ell + 1)}{n} \chi_ {2} (P _ {1} \| P _ {0})\right).
$$

Because $\ell = \Theta ( { \sqrt { n } } )$ , the exponent on the right-hand side is bounded, and therefore

$$
\frac {1}{n} \mathbb {E} _ {P _ {\mathrm{Y}, \mathrm{PPM}} ^ {n, \ell}} \left[ \frac {P _ {\mathrm{Y} , \mathrm{PPM}} ^ {n , \ell} (\mathbf {Y})}{P _ {0} ^ {\otimes n} (\mathbf {Y})} \right] = O (n ^ {- 1}) = o (\ell^ {- 1 / 2}).
$$

Choosing $\kappa > c _ { G , 1 }$ sufficiently large gives

$$
\max _ {\mathbf {x} \in \mathcal {P} _ {n, \ell}} \operatorname * {P r} \left\{\imath (\mathbf {x}; \mathbf {Y}) \leq \log (n ^ {1 3} M _ {n}) \right\} + \frac {1}{n} \mathbb {E} _ {P _ {Y, \mathrm{PPM}} ^ {n, \ell}} \left[ \frac {P _ {Y , \mathrm{PPM}} ^ {n , \ell} (\mathbf {Y})}{P _ {0} ^ {\otimes n} (\mathbf {Y})} \right] \leq \epsilon
$$

for all sufficiently large n. Thus the reliability condition of [19, Theorem 5] is satisfied.

3) Verification of the resolvability condition. By the choice of $K _ { n } .$ we have log $\begin{array} { r } { \frac { M _ { n } K _ { n } } { n ^ { 4 } } \ge \ell D _ { Q } + n ^ { 3 / 8 } - 4 } \end{array}$ log n. Applying the PPM information-spectrum bound in [19, Lemma 7], there exists a channel-dependent constant $c _ { G , 2 } >$ 0 such that

$$
\operatorname * {P r} \left\{\log \frac {W _ {Z | X} ^ {\otimes n} (\mathbf {Z} | \mathbf {X})}{P _ {Z , \mathrm{PPM}} ^ {n , \ell} (\mathbf {Z})} \geq \log \frac {M _ {n} K _ {n}}{n ^ {4}} \right\} \leq \exp \left[ - c _ {G, 2} \frac {(n ^ {3 / 8} - 4 \log n) ^ {2}}{\ell \log^ {2} m} \right],
$$

which is exponentially small since $\ell = \Theta ( n ^ { 1 / 2 } )$ . This verifies the information-spectrum condition for resolvability.

4) Verification of the positive-probability condition. The remaining condition in [19, Theorem 5] guarantees that the reliability and resolvability properties hold simultaneously for at least one realization of the random codebook.

Note that $M _ { n } = \exp ( \Theta ( { \sqrt { n } } ) )$ and log $( M _ { n } K _ { n } ) = O ( { \sqrt { n } } )$ . The remaining factors in the positive-probability condition depend on the finite output alphabet, the minimum positive output probability, and polynomial powers of $n .$ . Since the channel is fixed and the alphabet is finite, the corresponding logarithmic factors grow at most polynomially in $n .$ . Thus the quantity inside the exponential term in that condition is bounded below by a positive inverse polynomial in n, whereas $M _ { n } = \exp ( \Theta ( { \sqrt { n } } ) )$ . The exponential factor therefore converges to one, and the positive-probability condition holds for all sufficiently large n.

We have now verified all the conditions of [19, Theorem 5]. Consequently, for the covertness metric considered in the proposition, there exists a deterministic PPM code, with at least $M _ { n }$ messages, satisfying the required covertness constraint, having maximum probability of error at most ϵ.

Finally, we note that

$$
\begin{array}{c} \log M _ {n} = \ell D _ {P} - \sqrt {\ell V _ {P}} Q ^ {- 1} \left(\epsilon - \frac {\kappa}{\sqrt {\ell}}\right) - 1 3 \log n + o (1) \\ = \ell D _ {P} - \sqrt {\ell V _ {P}} Q ^ {- 1} (\epsilon) + O (\log n), \end{array}
$$

since $\begin{array} { r } { Q ^ { - 1 } \left( \epsilon - \frac { \kappa } { \sqrt { \ell } } \right) = Q ^ { - 1 } ( \epsilon ) + O ( \ell ^ { - 1 / 2 } ) } \end{array}$ , and

$$
\begin{array}{r l} & {\log K _ {n} = \left[ \ell D _ {Q} + n ^ {3 / 8} - \log M _ {n} \right] ^ {+} + O (1)} \\ & {\qquad = \left[ \ell (D _ {Q} - D _ {P}) + n ^ {3 / 8} + O (\sqrt {\ell} + \log n) \right] ^ {+} + O (1)} \\ & {\qquad = \ell [ D _ {Q} - D _ {P} ] ^ {+} + o (\sqrt {n}).} \end{array}
$$

This completes the proof of Proposition 6.

## APPENDIX H

## ESTIMATING THE MOMENT OF LOG-LIKELIHOOD RATIO

This appendix aims to derive the mean, variance, and third absolute centered moment of the one-block loglikelihood ratio under the midpoint distribution $H _ { m }$ :

$$
\mathbb {E} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) = O (m ^ {- 2}), \quad \operatorname{Var} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z})}{Q _ {0} ^ {\otimes m} (\mathbf {Z})}\right) = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m} + O (m ^ {- 2}),\tag{31}
$$

$$
\mathbb {E} _ {H _ {m}} \left| \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right) - \mathbb {E} _ {H _ {m}} \left(\log \frac {P _ {m} (\mathbf {Z} _ {j})}{Q _ {0} ^ {\otimes m} (\mathbf {Z} _ {j})}\right) \right| ^ {3} = O (m ^ {- 3 / 2}).\tag{32}
$$

As a result, we also have

$$
\operatorname{Var} _ {H _ {m}} (X _ {m}) = \chi_ {2} (Q _ {1} \| Q _ {0}) + O (m ^ {- 1}), \quad \text { and } \quad \mathbb {E} _ {H _ {m}} | X _ {m} - \mathbb {E} _ {H _ {m}} X _ {m} | ^ {3} = O (1),
$$

where $X _ { m }$ is defined in (26) in Appendix C.

## A. Mean And Variance

For simplicity, we abbreviate $C _ { m } \triangleq \log { \frac { P _ { m } ( \mathbf { Z } ) } { Q _ { 0 } ^ { \otimes m } ( \mathbf { Z } ) } }$ , where $\mathbf { Z } \sim H _ { m } . \mathrm { ~ I f ~ } P _ { m } ( \mathbf { z } ) = 0$ , then $H _ { m } ( \mathbf { z } ) = 0$ . Therefore, the value assigned to $C _ { m }$ at such points does not affect any expectation under $H _ { m }$

Recall that $\begin{array} { r } { M _ { m } ( s ) = \sum _ { \mathbf { z } } Q _ { 0 } ^ { \otimes m } ( \mathbf { z } ) \left( \frac { P _ { m } ( \mathbf { z } ) } { Q _ { 0 } ^ { \otimes m } ( \mathbf { z } ) } \right) ^ { s } } \end{array}$ for $\operatorname { R e } ( s ) > 0$ . Differentiating it with respect to s gives

$$
M _ {m} ^ {\prime} (s) = \sum_ {\mathbf {z}} Q _ {0} ^ {\otimes m} (\mathbf {z}) \left(\frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}\right) ^ {s} \log \frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}.
$$

At $s = 1 / 2$

$$
\begin{array}{r l} & M _ {m} ^ {\prime} (1 / 2) = \sum_ {\mathbf {z}} Q _ {0} ^ {\otimes m} (\mathbf {z}) \sqrt {\frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}} \log \frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})} \\ & \qquad = \sum_ {\mathbf {z}} \sqrt {P _ {m} (\mathbf {z}) Q _ {0} ^ {\otimes m} (\mathbf {z})} \log \frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})} = \rho_ {m} \mathbb {E} _ {H _ {m}} [ C _ {m} ], \end{array}
$$

Also note that $M _ { m } ( 1 / 2 ) = \rho _ { m }$ . Therefore, we have

$$
\frac {d}{d s} \log M _ {m} (s) \bigg | _ {s = 1 / 2} = \frac {M _ {m} ^ {\prime} (1 / 2)}{M _ {m} (1 / 2)} = \mathbb {E} _ {H _ {m}} [ C _ {m} ].
$$

Differentiating $M _ { m } ( s )$ with respect to s twice gives

$$
M _ {m} ^ {\prime \prime} (s) = \sum_ {\mathbf {z}} Q _ {0} ^ {\otimes m} (\mathbf {z}) \left(\frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}\right) ^ {s} \left(\log \frac {P _ {m} (\mathbf {z})}{Q _ {0} ^ {\otimes m} (\mathbf {z})}\right) ^ {2}.
$$

Evaluating at $s = 1 / 2$ and again using the definition of $H _ { m }$ , we obtain

$$
M _ {m} ^ {\prime \prime} (1 / 2) = \rho_ {m} \mathbb {E} _ {H _ {m}} [ C _ {m} ^ {2} ].
$$

Consequently, we have

$$
\left. \frac {d ^ {2}}{d s ^ {2}} \log M _ {m} (s) \right| _ {s = 1 / 2} = \frac {M _ {m} ^ {\prime \prime} (1 / 2)}{M _ {m} (1 / 2)} - \left(\frac {M _ {m} ^ {\prime} (1 / 2)}{M _ {m} (1 / 2)}\right) ^ {2} = \mathbb {E} _ {H _ {m}} [ C _ {m} ^ {2} ] - \left(\mathbb {E} _ {H _ {m}} C _ {m}\right) ^ {2} = \operatorname{Var} _ {H _ {m}} (C _ {m}).
$$

It remains to evaluate these derivatives using Lemma 2:

$$
\log M _ {m} (s) = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) + r _ {m} (s), \quad \text { where } | r _ {m} (s) | \leq \frac {c _ {B , 1 , d} (1 + | s |) ^ {4}}{m ^ {2}}.
$$

The derivative of the first term is

$$
\frac {d}{d s} \left[ \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) \right] = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} (2 s - 1),
$$

which equals zero when $s = 1 / 2$ . Its second derivative is

$$
\frac {d ^ {2}}{d s ^ {2}} \left[ \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{2 m} s (s - 1) \right] = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m}.
$$

We next differentiate the remainder term $r _ { m } ( s )$ . Choose the fixed disk $\begin{array} { r } { \mathcal { D } \triangleq \left\{ s \in \mathbb { C } : \left| s - \frac { 1 } { 2 } \right| \le \frac { 1 } { 8 } \right\} } \end{array}$ . Since $| s |$ is bounded on ${ \mathcal { D } } ,$ we have $\begin{array} { r } { \operatorname* { s u p } _ { s \in { \mathcal { D } } } | r _ { m } ( s ) | \leq \frac { c _ { H , 1 } } { m ^ { 2 } } } \end{array}$ for some constant $c _ { H , 1 } > 0$ . The function $r _ { m } ( s )$ is analytic on this disk. Cauchy’s derivative estimate therefore gives, for $k = 1 , \hat { z }$ ,

$$
\left| r _ {m} ^ {(k)} \left(\frac {1}{2}\right) \right| \leq \frac {k !}{(1 / 8) ^ {k}} \sup _ {s \in \mathcal {D}} | r _ {m} (s) | = O (m ^ {- 2}).
$$

It follows that

$$
\mathbb {E} _ {H _ {m}} [ C _ {m} ] = \left. \frac {d}{d s} \log M _ {m} (s) \right| _ {s = 1 / 2} = r _ {m} ^ {\prime} (1 / 2) = O (m ^ {- 2}),
$$

$$
\operatorname{Var} _ {H _ {m}} (C _ {m}) = \left. \frac {d ^ {2}}{d s ^ {2}} \log M _ {m} (s) \right| _ {s = 1 / 2} = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m} + r _ {m} ^ {\prime \prime} (1 / 2) = \frac {\chi_ {2} (Q _ {1} \| Q _ {0})}{m} + O (m ^ {- 2}).
$$

This completes the proof of (31).

## B. Third Absolute Centered Moment

The proof uses the event ${ \mathcal { E } } _ { m }$ introduced in Section III and its complement $\mathcal { E } _ { m } ^ { \mathrm { c } }$ . We first control the contribution from ${ \mathcal { E } } _ { m }$ . Note that

$$
\mathbb {E} _ {H _ {m}} \left[ | C _ {m} | ^ {3} \mathbf {1} _ {\mathcal {E} _ {m}} \right] = \sum_ {\mathbf {z} \in \mathcal {E} _ {m}} H _ {m} (\mathbf {z}) | C _ {m} (\mathbf {z}) | ^ {3}
$$

For $| x | \leq 1 / 2 ,$ , we have $| \log ( 1 + x ) | \leq 2 | x |$ |. Therefore, on the event ${ \mathcal { E } } _ { m }$ , we have $| C _ { m } | = | \log ( 1 + B _ { m } ) | \leq 2 | B _ { m } |$ The definition of $H _ { m }$ gives

$$
H _ {m} (\mathbf {z}) = Q _ {0} ^ {\otimes m} (\mathbf {z}) \frac {\sqrt {1 + B _ {m} (\mathbf {z})}}{\rho_ {m}}.
$$

On the event $\mathcal { E } _ { m } ,$ we have $\begin{array} { r } { \sqrt { 1 + B _ { m } ( \mathbf { z } ) } \le \sqrt { \frac { 3 } { 2 } } . } \end{array}$ Moreover, since $\rho _ { m } \to 1$ , we have $\rho _ { m } \ge 1 / 2$ for all sufficiently large $m .$ . Hence, on the event $\begin{array} { r } { \mathcal { E } _ { m } , H _ { m } ( \mathbf { z } ) \leq 2 \sqrt { \frac { 3 } { 2 } Q _ { 0 } ^ { \otimes m } ( \mathbf { z } ) } } \end{array}$ . Therefore,

$$
\mathbb {E} _ {H _ {m}} \left[ | C _ {m} | ^ {3} \mathbf {1} _ {\mathcal {E} _ {m}} \right] \leq 2 \sqrt {\frac {3}{2}} \sum_ {\mathbf {z} \in \mathcal {E} _ {m}} Q _ {0} ^ {\otimes m} (\mathbf {z}) \big (2 | B _ {m} (\mathbf {z}) | \big) ^ {3} \leq 1 6 \sqrt {\frac {3}{2}} \mathbb {E} _ {Q _ {0} ^ {\otimes m}} | B _ {m} | ^ {3} = O (m ^ {- 3 / 2}),
$$

where the last step follows from the fact that $\mathbb { E } | B _ { m } | ^ { 3 } = O ( m ^ { - 3 / 2 } )$ (calculated in Appendix B-A).

We next control the complement event $\mathcal { E } _ { m } ^ { \mathrm { c } }$ . Note that for all sufficiently large $m ,$

$$
H _ {m} (\mathbf {z}) = Q _ {0} ^ {\otimes m} (\mathbf {z}) \frac {\sqrt {1 + B _ {m} (\mathbf {z})}}{\rho_ {m}} \leq 2 \sqrt {a _ {\mathrm{max}} + 1} Q _ {0} ^ {\otimes m} (\mathbf {z}).
$$

Consequently,

$$
\mathbb {E} _ {H _ {m}} \left[ | C _ {m} | ^ {3} \mathbf {1} _ {\mathcal {E} _ {m} ^ {c}} \right] = \sum_ {\mathbf {z} \in \mathcal {E} _ {m} ^ {c}} H _ {m} (\mathbf {z}) | C _ {m} (\mathbf {z}) | ^ {3} \leq 2 \sqrt {a _ {\max} + 1} \times \max _ {\mathbf {z}: H _ {m} (\mathbf {z}) > 0} | \log (1 + B _ {m} (\mathbf {z})) | ^ {3} \times Q _ {0} ^ {\otimes m} (\mathcal {E} _ {m} ^ {c}).
$$

Using the concentration inequality in (9) and the fact that $| \operatorname* { m a x } _ { \mathbf { z } : H _ { m } ( \mathbf { z } ) > 0 } \log ( 1 + B _ { m } ( \mathbf { z } ) ) | = O ( \log m )$ , we obtain

$$
\mathbb {E} _ {H _ {m}} \left[ | C _ {m} | ^ {3} \mathbf {1} _ {\mathcal {E} _ {m} ^ {\mathrm{c}}} \right] = O (e ^ {- (1 / (2 (a _ {\max} - a _ {\min}) ^ {2})) m}).
$$

Combining the two events together yields that

$$
\mathbb {E} _ {H _ {m}} | C _ {m} | ^ {3} = O (m ^ {- 3 / 2}).
$$

Finally, one can check that

$$
\mathbb {E} _ {H _ {m}} \left| C _ {m} - \mathbb {E} _ {H _ {m}} C _ {m} \right| ^ {3} \leq 4 \mathbb {E} _ {H _ {m}} | C _ {m} | ^ {3} + 4 \left| \mathbb {E} _ {H _ {m}} C _ {m} \right| ^ {3} = O (m ^ {- 3 / 2}).
$$

This completes the proof of (32).

## REFERENCES

[1] B. A. Bash, D. Goeckel, and D. Towsley, “Limits of reliable communication with low probability of detection on AWGN channels,” IEEE J. Sel. Areas Commun., vol. 31, no. 9, pp. 1921–1930, Sep. 2013.

[2] P. H. Che, M. Bakshi, and S. Jaggi, “Reliable deniable communication: Hiding messages in noise,” in Proc. IEEE Int. Symp. Inf. Theory, 2013, pp. 2945–2949.

[3] Q. Zhang, M. Bakshi, and S. Jaggi, “Covert communication over adversarially jammed channels,” IEEE Trans. Inf. Theory, vol. 67, no. 9, pp. 6096–6121, Sep. 2021.

[4] M. R. Bloch, “Covert communication over noisy channels: A resolvability perspective,” IEEE Trans. Inf. Theory, vol. 62, no. 5, pp. 2334–2354, May 2016.

[5] L. Wang, G. W. Wornell, and L. Zheng, “Fundamental limits of communication with low probability of detection,” IEEE Trans. Inf. Theory, vol. 62, no. 6, pp. 3493–3503, Jun. 2016.

[6] L. Wang, “Optimal throughput for covert communication over a classical-quantum channel,” in Proc. IEEE Inf. Theory Workshop, Cambridge, U.K., Sep. 2016, pp. 364–368.

[7] A. Sheikholeslami, B. A. Bash, D. Towsley, D. Goeckel, and S. Guha, “Covert communication over classical-quantum channels,” in Proc. IEEE Int. Symp. Inf. Theory, Barcelona, Spain, Jul. 2016, pp. 2064–2068.

[8] K. S. K. Arumugam and M. R. Bloch, “Keyless covert communication over multiple-access channels,” in Proc. IEEE Int. Symp. Inf. Theory, Barcelona, Spain, Jul. 2016, pp. 2229–2233.

[9] K. S. K. Arumugam and M. R. Bloch, “Covert communication over a K-user multiple-access channel,” IEEE Trans. Inf. Theory, vol. 65, no. 11, pp. 7020–7044, Nov. 2019.

[10] K. S. K. Arumugam and M. R. Bloch, “Embedding covert information in broadcast communications,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 10, pp. 2787–2801, Oct. 2019.

[11] V. Y. F. Tan and S.-H. Lee, “Time-division is optimal for covert communication over some broadcast channels,” IEEE Trans. Inf. Forensics Security, vol. 14, no. 5, pp. 1377–1389, May 2019.

[12] Y. Steinberg and M. Wigger, “Covert capacity of degraded broadcast channels,” arXiv preprint arXiv:2605.09353, 2026.

[13] S.-H. Lee, L. Wang, A. Khisti, and G. W. Wornell, “Covert communication with channel-state information at the transmitter,” IEEE Trans. Inf. Forensics Security, vol. 13, no. 9, pp. 2310–2319, Sep. 2018.

[14] Q. Zhang, M. Bakshi, and S. Jaggi, “Covert communication with polynomial computational complexity,” IEEE Trans. Inf. Theory, vol. 66, no. 3, pp. 1354–1384, Mar. 2020.

[15] S.-Y. Wang and M. R. Bloch, “Covert MIMO communications under variational distance constraint,” IEEE Trans. Inf. Forensics Security, vol. 16, pp. 4605–4620, 2021.

[16] C. Liu, J. Wang, Q. Zhang, J. Xu, and L. Zhou, “Finite blocklength covert communication over quasi-static multiple-antenna fading channels,” arXiv preprint arXiv:2603.29645, 2026.

[17] Q. Zhang, M. R. Bloch, M. Bakshi, and S. Jaggi, “Undetectable radios: Covert communication under spectral mask constraints,” in Proc. IEEE Int. Symp. Inf. Theory, Paris, France, Jul. 2019, pp. 992–996.

[18] M. R. Bloch and S. Guha, “Optimal covert communications using pulse-position modulation,” in Proc. IEEE Int. Symp. Inf. Theory, Aachen, Germany, Jun. 2017, pp. 2825–2829.

[19] M. Tahmasbi and M. R. Bloch, “First- and second-order asymptotics in covert communication,” IEEE Trans. Inf. Theory, vol. 65, no. 4, pp. 2190–2212, Apr. 2019.
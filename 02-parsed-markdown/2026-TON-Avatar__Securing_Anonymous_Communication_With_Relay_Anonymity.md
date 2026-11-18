# Avatar: Securing Anonymous Communication With Relay Anonymity

Hao Zhu , Mei Wang , Zengpeng Li , and Jing Chen , Senior Member, IEEE

Abstract—Onion routing and mix networks are designed to provide users with anonymous Internet access and to prevent the disclosure of real IP addresses. In practice, anonymous networks serve various legitimate purposes, such as whistleblowing, circumventing censorship, and safeguarding personal online privacy and security. These systems typically achieve anonymity by introducing a series of relays between the sender and the receiver. An anonymous path, or circuit, is usually composed of multiple relays (commonly three), and onion routing systems such as Tor rely on these circuits to relay trafic and ensure anonymity. Although Tor employs hidden relays (known as bridges) to resist censorship and blocking, most relays are publicly listed, and their identities are visible to circuit initiators during circuit construction, making them susceptible to surveillance and targeted attacks. A malicious relay deviating from the protocol (e.g., injecting modified onions) poses serious threats to system security. An interesting question is how to preserve relay identity privacy while maintaining network functionality. In this paper, we introduce an innovative method for protecting relay privacy within circuits. This is achieved through the application of anonymous credentials, anonymous verifiable random functions (AVRFs), and signatures with key blinding. Additionally, if more than half of the directory authority servers within the current Tor network are compromised, the entire network could collapse. To mitigate this risk, our design distributes trust among more entities, enhancing the network’s resilience against potential adversaries. We have named this approach Avatar to enable users to navigate the online realm with the same freedom, privacy, and anonymity as an Avatar, allowing them to maintain full control over their digital identity. Furthermore, we provide a comprehensive analysis and evaluation of the Avatar framework. The findings indicate that, in comparison to the original Tor network’s onion routing protocol, our proposed protocol exhibits superior time eficiency in many network environments.

Index Terms—Anonymity, Tor, relay.

## I. INTRODUCTION

NONYMOUS networks aim to protect communication network is one of the largest low-latency anonymous networks globally [2], [3]. It ensures user privacy by using relays, which are volunteer-provided server nodes, to transmit messages securely. The operators of the Tor network have set up multiple servers, known as Directory Authority (DA) servers, to collect the topology information of all the relays in the network. Users can download relay information from DAs and select three relays to form anonymous circuits. Anonymous networks can be widely applied across various fields, such as virtual currency transactions, online whistleblowing platforms, and end-to-end encrypted communication, where robust privacy and security are paramount.

However, millions of Tor network users are currently confronted with significant security risks. The topology consensus of the Tor network is determined by 9 DAs following a majority rule. The unfortunate event of multiple DAs becoming corrupted can result in an inconsistent global consensus. Furthermore, adversaries may exploit these diferences in knowledge to diferentiate user behavior or to intercept user trafic [4]. Additionally, adversaries can corrupt some relay nodes, threatening the overall system security. Except for some bridges in the current Tor network [5], information about all other relays is publicly accessible via the oficial Tor website [6]. While attacking all relays is highly challenging, an adversary can inflict substantial damage at minimal cost by identifying and targeting high-value relays. This vulnerability arises because Tor clients display relay information when constructing circuits (see Fig. 1). Even if this information is hidden from the user, they can still infer the identity of the relay by analyzing the data packets. This is because the client needs to use the relay’s public key to verify its signature, thereby confirming the relay’s identity. An adversary can masquerade as a user or induce a user to continuously request the construction of circuits for path probing in order to gather statistical information about circuit composition and node selection patterns. For example, since the circuit selection in the Tor network is not entirely random and also considers factors such as the relay’s bandwidth, high-bandwidth relays will attract more users than low-bandwidth relays [7]. These factors make it easier for an adversary to identify targets for attack. An attack on a relay that operates across multiple circuits will result in more significant damage. Thus, a natural question is raised as follows:

![](images/522d4ede3c1fc460223b7acada744eb33c6a93a6207b61ae90309a9acf6789ff.jpg)  
Fig. 1. Relay privacy exposure. An adversary can gather extensive path information to analyze and pinpoint relays with higher message-forwarding frequencies.

## Can privacy-aware relays be integrated into eficient anonymous circuit construction without incurring additional deployment costs?

To address the above challenges, we propose an anonymous networking scheme, referred to as Avatar. The primary objective of Avatar is to enhance the privacy of relay nodes without incurring additional deployment costs, requiring only lightweight modifications to the existing Tor architecture. The key idea of Avatar is to incorporate anonymous credentials and anonymous verifiable random functions (AVRFs) into the circuit construction. This design preserves the functionality of the conventional onion routing protocol while providing strong privacy guarantees for relay nodes. Owing to its structural resemblance to a paperclip, the new circuit construction protocol is termed the Paperclip Anonymous Circuit (PAC). To enable the issuance of anonymous credentials and strengthen the system’s resilience against adversarial attacks, we further introduce a new role, referred to as group nodes, to replace the DAs in Tor. Similar to relays, group nodes are operated by volunteers, but they difer fundamentally from DAs that are directly maintained by the Tor network operators. The main responsibility of group nodes is to issue anonymous credentials to relays during circuit construction, thereby concealing their identities. To ensure fairness in credential issuance, we employ verifiable random functions (VRFs) to achieve randomized grouping. Moreover, the security of group nodes can be ensured through modern trusted hardware as demonstrated in [8].

Here, Table I presents a comparison between our scheme and several related anonymity schemes. In this comparison, we mainly focus on the core objectives that the Avatar protocol aims to achieve. Specifically, we consider anonymity schemes such as Tor, SGX-Tor, SmarTor, and Walking Onions, which, like our protocol, employ a circuit-based design. In addition, we include message-based anonymity systems such as Loopix and Nym, as well as the tunnel-based I2P system, in our comparison. It should be noted that Loopix, Nym, and I2P do not construct anonymous circuits, so scalability is not considered in their evaluation. Although message-based protocols are theoretically capable of resisting global passive adversaries, in practice, such attacks are extremely rare due to the high complexity and prohibitive cost of monitoring cross-national or intercontinental trafic at a global scale. Moreover, messagebased anonymous communication systems often sufer from severe performance degradation when transmitting large files or maintaining long-lived connections. In contrast, circuitbased anonymous communication protocols provide better performance in real-world use, which explains why systems such as Tor have become the largest and most widely deployed anonymity networks worldwide. As illustrated in Table I, Avatar uniquely introduces the concept of relay anonymity, which, to the best of our knowledge, has not been achieved by any existing anonymity protocol.

Contributions. Avatar’s contributions are summarized below:

• A secure anonymous network with paperclip anonymous circuits. We propose a secure privacy-aware anonymous network structure named Avatar. The crux of Avatar is to construct a PAC without compromising the privacy of relay nodes. Additionally, Avatar not only achieves better balance but also enhances resilience against adversarial attacks.

• Privacy-aware relay elections via anonymous VRF. To ensure relay privacy while maintaining the randomness of circuit construction and meeting other requirements such as network latency, we employ AVRF to select the anonymous group to which each relay in the PAC belongs.

• Anonymous relay authentication via anonymous credentials. Avatar introduces anonymous credentials to enable secure and eficient relay identity authentication within the circuit, achieving both relay anonymity and client verification. Furthermore, we extend the functionality of existing anonymous credentials to support the verification of the blinded public key used in both AVRF and signatures with key blinding.

• Prototype building with performance evaluation. Avatar provides a prototype system written in Python and provides a comparison with the Tor network to demonstrate the potential deployment in the real world. The results show that Avatar is generally more eficient than the existing Tor network.

Organization. We introduce the cryptographic notations and blocks related to Avatar in Section II. We present the system model and threat model in Section III and provide a brief overview of the design. Section IV provides a detailed description of our schemes. Section V presents a comprehensive security analysis of Avatar, accompanied by a performance evaluation. Finally, Section VI presents the related work as well as summarizes Avatar in Section VII.

## II. PRELIMINARIES

This section describes the common notations, assumptions, and cryptographic building blocks used in this paper.

## A. Notations and Definitions

Let λ denote the security parameter and q denote a prime. We denote by $\mathbb { Z } _ { q }$ the set $\{ 0 , 1 , . . . , q - 1 \}$ , and by $\mathbb { G } _ { 1 } , \mathbb { G } _ { 2 }$ , and ${ \mathbb G } _ { 3 }$ three bilinear cyclic groups of the same prime order $q ,$ with $g _ { 1 }$ and $g _ { 2 }$ as the generators of $\mathbb { G } _ { 1 }$ and $\mathbb { G } _ { 2 } .$ , respectively. The symbol $\underline { { \boldsymbol { \mathbb { S } } } }$ indicates uniform random sampling from a set. The symbol ← or → represents assignment operations (i.e., assigning the result of a computation), while = denotes equality. We use a standard symmetric encryption scheme satisfying Dec(k Enc(k m)) → m, where $k \in \mathcal { K } , m \in \mathcal { M } . \ H$ $H _ { \mathbb { G } _ { 1 } } , H _ { \mathbb { G } _ { 2 } }$ , and $H _ { \mathbb { Z } _ { q } }$ denote hash functions that map an arbitrarylength random input to the target domains $\{ 0 , 1 \} ^ { \lambda } , \mathbb { G } _ { 1 } , \mathbb { G } _ { 2 }$ , and $\mathbb { Z } _ { q } .$ , respectively.

TABLE I  
COMPARISON WITH RELATED ANONYMITY SCHEMES

<table><tr><td>Authors</td><td>Schemes</td><td>Resilience</td><td>Relay anonymity</td><td>Randomness</td><td>Scalability</td><td>Resisting GPA</td></tr><tr><td>Dingledine et al. [2]</td><td>Tor</td><td>○</td><td>○</td><td>○</td><td>○</td><td>○</td></tr><tr><td>Kim et al. [8]</td><td>SGX-Tor</td><td>●</td><td>○</td><td>○</td><td>○</td><td>○</td></tr><tr><td>Greubel el al. [9]</td><td>SmarTor</td><td>●</td><td>○</td><td>○</td><td>○</td><td>○</td></tr><tr><td>Komlo et al. [4]</td><td>Walking Onions</td><td>○</td><td>○</td><td>●</td><td>●</td><td>○</td></tr><tr><td>Piotrowska et al. [10]</td><td>Loopix</td><td>●</td><td>○</td><td>○</td><td>-</td><td>●</td></tr><tr><td>Diaz et al. [11]</td><td>Nym</td><td>●</td><td>○</td><td>○</td><td>-</td><td>●</td></tr><tr><td>Invisible Internet Project [12]</td><td>I2P</td><td>●</td><td>○</td><td>○</td><td>-</td><td>○</td></tr><tr><td>Ours</td><td>Avatar</td><td>●</td><td>●</td><td>●</td><td>●</td><td>○</td></tr></table>

GPA represents a global passive adversary.  represents the absence of this characteristic,  represents partial possession of this characteristic,  represents full possession of this characteristic, and – means the feature is not analyzed. It is important to clarify that in Avatar, when extending a circuit, the selection of the anonymity group to which the next-hop relay belongs is random. However, within the anonymity group, the specific relay chosen as the next hop is not selected randomly

Bilinear Pairings. Let e be a bilinear mapping relation $e ~ : \mathbb { G } _ { 1 } \times \mathbb { G } _ { 2 } \to \mathbb { G } _ { 3 }$ . A bilinear pairing has the following properties: (1) bilinearity, for all $g _ { 1 } \in \mathbb { G } _ { 1 } , g _ { 2 } \in \mathbb { G } _ { 2 }$ and $a , b$ ∈ $\mathrm { { \bar { Z } } } _ { q } , \mathrm { { \bar { \it { e } } } } ( g _ { 1 } ^ { a } , g _ { 2 } ^ { b } ) = { \it { e } } ( g _ { 1 } , g _ { 2 } ) ^ { \dot { a } b } ; ( 2 )$ non-degeneracy, $e ( g _ { 1 } , g _ { 2 } ) \neq 1$ ; (3) computability, e can be evaluated eficiently.

Non-Interactive Zero-knowledge. A non-interactive zeroknowledge (NIZK) argument consists of three algorithms $( \mathsf { S e t u p } _ { \mathsf { Z K } } , \mathsf { P r o v e } _ { \mathsf { Z K } } , \mathsf { V e r i f y } _ { \mathsf { Z K } } )$ [13]. The setup algorithm $\mathsf { S e t u p } _ { { \mathrm { Z K } } } ( { \mathcal { R } } ) \to$ crs generates the common reference string crs for the proof relationship R, where R is a polynomialtime relation consisting of pairs (w s). The proving algorithm $\mathsf { P r o v e } _ { \mathsf { Z K } } ( \mathcal { R } , c r s , s , w ) \to \pi$ produces a proof π demonstrating that the prover knows a witness w such that the input statement s satisfies the relation $\mathcal { R } ( w , s )$ . Finally, the verification algorithm $\mathsf { V e r i f y } _ { \mathsf { Z K } } ( \mathcal { R } , c r s , s , \pi ) \to 0 / 1$ determines the validity of the proof π for the given statement s. To simplify notation, we write: $\pi = { \cal P } K \{ ( w _ { 1 } , w _ { 2 } , \ldots ) : s _ { 1 } , s _ { 2 } , \ldots \}$ . Here, $w _ { 1 } , w _ { 2 } , \ldots$ represent secret values, and the prover claims knowledge of $s _ { 1 } , s _ { 2 } , \ldots$ that satisfy the specified statements.

## B. Cryptographic Building Blocks

Boneh-Lynn-Shacham Signature. Boneh-Lynn-Shacham (BLS) signature [14] consists of three algorithms $\begin{array} { r } { ( \mathsf { K e y G e n } _ { \mathsf { B L S } } , \quad \mathsf { S i g } _ { \mathsf { B L S } } , \quad \mathsf { V e r i f y } _ { \mathsf { B L S } } ) . } \end{array}$ The key generation algorithm ${ \mathsf { K e y G e n } } _ { \mathsf { B L S } } ( 1 ^ { \lambda } ) \to ( s k , p k )$ produces a secret key $s k \ = \ x$ and a corresponding public key $\begin{array} { r } { p k \ = \ g _ { 1 } ^ { x } } \end{array}$ where $x \overset { \mathbb { S } } { \longleftarrow } \mathbb { Z } _ { q } , g _ { 1 } \in \mathbb { G } _ { 1 }$ . The signing algorithm $\mathsf { S i g } _ { \mathsf { B L S } } ( s k , m ) \to \sigma$ generates a signature $\sigma ~ = ~ H _ { \mathbb { G } _ { 2 } } ( m ) ^ { s k }$ on a message m. The verification algorithm $\mathsf { V e r i f y } _ { \mathsf { B L S } } ( p k , \sigma , m ) \to 0 / 1$ checks the validity of the signature σ on the message m. It outputs 1 if $e ( g _ { 1 } , \sigma ) = e ( p k , H _ { \mathbb { G } _ { 2 } } ( m ) )$ holds; otherwise, it outputs 0.

Boneh-Boyen Signature. In this paper, we employ the main idea of Boneh-Boyen signature [15], [16] (abbreviated as BB or BBS) to provide anonymous credentials. BBS consists of three algorithms $( \mathsf { K e y G e n } _ { \mathsf { B B S } } , \mathsf { S i g } _ { \mathsf { B B S } } , \mathsf { V e r i f y } _ { \mathsf { B B S } } )$ . The key generation ${ \mathsf { K e y G e n } } _ { \mathsf { B B S } } ( 1 ^ { \lambda } ) \to ( s k , p k )$ generates a secret key $s k = x$ and a corresponding public key $p k = g _ { 2 } { ^ x }$ where x $\stackrel { \ S } {  } \mathbb { Z } _ { q } ,$ $g _ { 2 } \in \mathbb { G } _ { 2 }$ . The signing algorithm $\mathsf { S i g } _ { \mathsf { B B S } } ( s k , m ) \to \sigma$ generates a signature $\sigma = \overset { \overline { { } } } { g } _ { 1 } ^ { 1 / ( \overline { { x } } + m \overline { { ) } } } , \ g _ { 1 } \in \mathbb { G } _ { 1 }$ . The verification algorithm $\mathsf { V e r i f y } _ { \mathsf { B B S } } ( p k , \sigma , m ) \to 0 / 1$ checks the validity of σ. If e(σ pk· $g _ { 2 } ^ { m } ) \ = \ e ( g _ { 1 } , g _ { 2 } )$ holds, then $\sigma$ is valid, and the output is 1; otherwise, the output is 0.

Verifiable Random Function. A verifiable random function (VRF) [17] is a specialized pseudo-random function that additionally provides a verifiable proof, allowing the correctness of the function output to be ensured non-interactively. In this paper, we adapt the VRF scheme from [18]. The key generation algorithm ${ \mathsf { K e y G e n } } _ { \mathsf { V R F } } ( 1 ^ { \lambda } ) \to ( s k , p k )$ generates a secret key $s k = x$ and a public key $p k = g _ { 1 } ^ { x }$ , where $x \overset { \mathbb { S } } { \longleftarrow } \mathbb { Z } _ { q } , g _ { 1 } \in \mathbb { G } _ { 1 }$ The proving algorithm $\mathsf { P r o v e } _ { V R F } ( s k , p k , m ) \ \to \ \mathsf { \Gamma } ( F _ { s k } ( m ) , \pi )$ computes $u \ = \ H _ { G _ { 1 } } ( m ) ^ { x } , \ F _ { s k } ( m ) \ = \ H ( m , u )$ and generates a proof $\pi = P K \{ ( x ) : \log _ { H _ { G _ { 1 } } ( m ) } u = \log _ { g _ { 1 } } p k \}$ . The verification algorithm $\mathsf { V e r i f y } _ { \mathsf { V R F } } ( p k , m , F _ { s k } ( m ) , \pi ) \ \overset { ^ { \cdot } } { \to } \ 0 / 1$ checks whether both the function value $F _ { s k } ( m )$ and the proof π are correct. If $F _ { s k } ( m ) = H ( m , u )$ and π is verified successfully, this algorithm outputs 1; otherwise, it outputs 0.

Anonymous Verifiable Random Function. Anonymous VRF (AVRF) [19] introduces an innovative mechanism to protect the public key during the verification of the proof π. Roughly speaking, in AVRF, a secret key is associated with multiple diferent public keys, making it dificult for an attacker to link diferent verification instances under the same secret key to a public key (or identity). The key generation ${ \mathsf { K e y G e n } } _ { \mathsf { A V R F } } ( 1 ^ { \lambda } ) \to ( s k , p k )$ generates a $s k = x \stackrel { \ S } {  } \mathbb { Z } _ { q }$ and a $p k \ = \ ( p k _ { 1 } , p k _ { 2 } ) \ = \ ( g _ { 2 } , g _ { 2 } ^ { x } )$ where $g _ { 2 } \in \mathbb { G } _ { 2 }$ . The update algorithm $\mathsf { U p d a t e } _ { \mathsf { A V R F } } ( p k ) \to p k ^ { \prime }$ chooses a random $r \gets \mathbb { Z } _ { q }$ and outputs a blinded public key $p k ^ { \prime } = ( p k _ { 1 } ^ { \prime } , p k _ { 2 } ^ { \prime } ) = ( g _ { 2 } ^ { r } , g _ { 2 } ^ { x r } ) \qquad $ The proving algorithm Prove<sub>AVRF</sub>(sk $p k ^ { \prime } , m ) \ \to \ ( F _ { s k } ( m ) , \pi )$ computes $u \ = \ H _ { \mathbb { G } _ { 2 } } ( m ) ^ { x } , \ F _ { s k } ( m ) \ = \ H ( m , u )$ and generates a proof $\pi = P K \{ ( x ) : \log _ { H _ { \mathbb { G } } , ( m ) } u = l o g _ { p k _ { 1 } ^ { \prime } } p k _ { 2 } ^ { \prime } \}$ . The verification Veri $\mathsf { P } _ { \mathsf { A V R F } } ( p k ^ { \prime } , m , F _ { s k } ( m ) , \pi ) \to 0 / 1$ checks the correctness of $F _ { s k } ( m )$ and the proof π. If $F _ { s k } ( m ) = H ( m , u )$ and π is verified successfully, then outputs 1; otherwise, it outputs 0.

## III. PROBLEM STATEMENT AND MODELS

In this section, we compare the architectural designs of the original Tor network and Avatar, highlighting the existing issues within Tor and outlining the goals Avatar aims to achieve in addressing these challenges.

## A. System Model

The current Tor [2] architecture (as shown in Fig. 2(a)) exhibits three fundamental limitations that impact its security, privacy, and scalability. First, the relay information is collected and aggregated by only nine globally distributed DAs, which collaboratively generate the consensus directory. This centralized trust model lacks resilience [9]. For example, if a majority of the DAs are compromised, an adversary could manipulate relay bandwidth to steer trafic toward malicious nodes, thereby undermining the system’s security. Second, the identities of relay nodes in Tor are fully exposed to clients during circuit construction, ofering no privacy protection for relays. This exposure not only leaks relay metadata but also enables adversaries to conduct path-probing attacks, allowing them to infer significant portions of the network topology and identify high-value relay nodes for targeted attacks. Finally, Tor’s circuit construction protocol requires multiple rounds of communication between clients and relays, resulting in high latency and limited scalability for longer paths. To address these challenges, we propose Avatar, a novel architecture illustrated in Fig. 2(b), which enhances resilience, protects relay privacy, and improves circuit construction eficiency. Avatar is similar to Tor in that it consists of multiple network nodes under peer-to-peer secure channels (e.g., TLS [20]). Avatar is separated into five kinds of entities:

![](images/a62897851f413a47a5ef6ba17ae8b4c3401bf5965aeacdbf11e4ac4e2c8266c4.jpg)  
Fig. 2. Comparison of system models. Fig. 2(a) illustrates the components of the Tor network, while Fig. 2(b) presents the architecture of Avatar. Unlike Tor, Avatar removes the DA and replaces part of its functionality by converting some RNs into GNs. GN refers to group nodes, and RN refers to relay nodes. DA refers to directory authorities. CN refers to client nodes. SN refers to server nodes. BN refers to bulletin nodes.

Relay Node (RN). RNs are provided by volunteers, and their duty is to forward messages. Once a new server has been established by a volunteer, a minimum period must elapse before it can be transitioned into the role of an RN.

Group Node (GN). GNs assume roles similar to DAs in Tor, but are contributed by volunteers rather than centralized operators. Each GN manages a group of RNs, issues credentials to them, and publishes relevant information to the BN. GNs do not relay client messages.

Client Node (CN). CN is a user terminal that accesses anonymous network services via client software. For example, Tor provides open-source client software on GitHub that anyone can download.

Server Node (SN). SNs represent the destination servers with which CNs establish anonymous connections.

Bulletin Node (BN). The BN stores publicly verifiable data accessible to all nodes. It may be implemented via websites or blockchain to ensure immutability. To prevent protocol compromise, all data must be verifiable upon publication and validated upon retrieval, limiting the impact of potential malicious writes.

To mitigate the risks associated with centralized trust, Avatar decentralizes trust across a large number of GNs, each of which is assigned to maintain the information of a randomly selected subset of relay nodes. To further diferentiate system roles and enhance transparency, Avatar introduces BNs, which are responsible for disseminating verifiable data generated by GNs and RNs. To strengthen relay anonymity, Avatar’s circuit construction mechanism ensures that each relay’s identity is only visible to its neighboring nodes, while preserving path randomness and balancing network performance factors such as bandwidth. Finally, to address the scalability limitations of multi-round key exchange in circuit construction, Avatar adopts a one-round-trip design [4], enabling a more eficient and privacy-preserving anonymous circuit with significantly reduced communication overhead.

## B. Design Goal

Resilience. We aim to achieve a balanced system by distributing trust evenly and randomly among a larger number of entities, such that the system remains operational and functional even if some core nodes are compromised.

Relay Anonymity. Given an anonymous path $\{ C N , R N _ { 1 } , R N _ { 2 } , \dots , R N _ { n } , S N \}$ , each RN conceals its true identity from all nodes except its adjacent ones. Moreover, when an RN participates in two diferent anonymous paths, its identity must be unlinkable.

Randomness. Randomness is used to evaluate the composition of anonymous paths. To prevent attackers from easily predicting the relay nodes used in an anonymous path and conducting trafic analysis attacks, the composition of a path should be random and unpredictable, even to the path initiator.

Scalability. By reducing the time required for circuit construction, the system ensures that execution overhead grows slowly as the anonymous path lengthens, thereby significantly improving the scalability of circuits.

## C. Threat Model and Assumptions

We assume that GNs in Avatar follow the protocol, but may be curious about the information they process. The credential issuance process from GNs to RNs is conducted over secure channels. RNs are not fully trusted, and the adversary may compromise a subset of RNs and cause them to deviate arbitrarily from the protocol. The first-hop relay of the anonymous circuit and the BN are assumed to be trustworthy. Furthermore, the adversary’s goal is to disrupt the proper functioning of the anonymity network (including Tor and Avatar). Accordingly, we assume the adversary: (1) can compromise a subset of RNs; (2) can observe a fraction of the trafic within the anonymity network; (3) can generate, modify, delete, or delay network trafic. Notably, any entity can act as a CN, including adversarial entities that masquerade as CNs and repeatedly initiate circuit construction requests.

## D. Design Overview

The design of Avatar consists of three stages: the system setup stage, the distribution stage, and the PAC construction stage. The system setup stage involves generating public parameters accessible to all nodes within the system, which are then used by each node to generate corresponding keys. The distribution stage aims to achieve two main objectives: first, to randomly divide all relay nodes into diferent anonymous groups, thereby enhancing system resilience, and second, to enable the unique group node within each anonymous group to issue credentials to its managed relay nodes, ensuring the protection of relay node identities within the anonymous circuit. In the PAC construction stage, a user constructs an anonymous circuit to access the target server. This circuit is randomly generated and exhibits two critical privacy features: protection of the client’s identity (a common feature in most existing anonymous circuits) and protection of relay node identities (a novel feature introduced here for the first time, to the best of our knowledge). The following sections provide a brief overview of each stage of the protocol.

Definition 1 (Secure Anonymous Communication System with Relay Anonymity): A secure anonymous communication system with relay anonymity follows the syntax below.

\- System setup phase.

$p a r s \gets \mathsf { S e t u p } ( 1 ^ { \lambda } ) \mathsf { : }$ A setup algorithm that takes the security parameter $1 ^ { \lambda }$ as input and outputs public parameters pars. The public parameter pars is an invisible input to the following algorithm.

$( s k , p k ) \gets { \mathsf { K e y G e n } } ( \cdot ) \mathsf { : }$ A key generation algorithm that outputs a private/public key pair (sk pk).

\- Distribution phase.

$r e q _ { c r e d } \gets \mathsf { G r q G e n } ( s k , h ) \colon \mathsf { A }$ group request generation that takes as input the private key sk and the grouping basis h and outputs the grouping request $r e q _ { c r e d } .$

• {0 1} ← GrqVer(pk $r e q _ { c r e d } \mathrm { : }$ A group request verification algorithm, inputs the public key $p k$ and the grouping request $r e q _ { c r e d } .$ , and outputs the verification result: 1 if the verification is successful, and 0 otherwise.

• cred ← CredIss(sk e id): A credential issuance algorithm that takes as input a secret key $s k ,$ an epoch identifier e, and an identity identifier $i d ,$ and outputs a credential cred.

• {0 1} ← CredVer(pk cred): A credential verification algorithm that takes as input a public key $p k$ and a credential cred, and outputs a verification result: it returns 1 if the verification succeeds, and 0 otherwise.

\- Paperclip anonymous circuit construction phase.

$r e q _ { 1 } \gets \mathsf { C i r c l n i t } ( \cdot ) \colon \mathsf { A }$ circuit initialization algorithm that outputs a circuit construction request $r e q _ { 1 }$

$\{ r e q _ { i + 1 } , r e s _ { i } \} \gets$ CircFwd(data): A circuit forwarding algorithm that takes as input a message data (either a request or a response). If $\dot { } { } d a t a = r e q _ { i }$ and $i \in [ 1 , \ldots , n - 1 ]$ the algorithm outputs a forwarded request $r e q _ { i + 1 } ;$ if $d a t a \ = \ r e q _ { n } ,$ , it outputs a response $r e s _ { n } ;$ if data = res<sub>i</sub> and $i \in [ 2 , \ldots , n ]$ , the algorithm outputs $r e s _ { i - 1 }$

${ \vec { k } } \gets { \mathsf { C i r c V e r } } ( r e s _ { 1 } ) { : }$ A circuit verification algorithm that takes as input a circuit construction response $r e s _ { 1 } .$ . If the verification succeeds, it outputs the shared keys <sup>\~</sup>k on the circuit; otherwise, abort.

## IV. AVATAR: OUR MAGICAL ANONYMOUS COMMUNICATION

In this section, we provide a detailed description of the construction of Avatar, as illustrated in Fig. 3. The process consists of three phases: setup, distribution, and PAC.

## A. System Setup Phase

During the system setup phase, a bulletin board needs to be set up to store all foundational information, making it accessible to every node in the system. To allow a server provided by a volunteer to participate in the system as an RN or GN, the server must run a key generation algorithm KeyGen(·) to generate a pair of long-term keys. An identity identifier id $\in \ \mathbb { Z } _ { q }$ is then derived by hashing the generated long-term public key. The long-term key pair for the RN is $( p k _ { R } = g _ { 1 } ^ { x } \in \mathbb { G } _ { 1 } , s k _ { R } = x \in \mathbb { Z } _ { q } )$ . Its identifier is $i d _ { R } .$ The longterm key pair for the GN is $( p k _ { G } = g _ { 2 } ^ { x } \in \mathbb { G } _ { 2 } , s k _ { G } = x \in \mathbb { Z } _ { q } )$ . Its identifier is $i d _ { G }$ . Subsequently, the long-term public key and the identifier are posted on the bulletin board.

## B. Distribution Phase

The system runs in epochs, where e denotes the index of the current epoch. In each epoch, the system performs a distribution phase during which each RN runs a VRF and, based on its output, requests credentials from diferent GNs. Here, we guarantee the randomness of the RN request based on the randomness of the output of the VRF. Furthermore, this output can be verified by the GNs to prevent a malicious credential request from passing the verification. Only when an RN has the credential issued by the GN can it provide a forwarding service for the user’s messages. In this phase, we improve the resilience of the system against adversaries by distributing trust to more GNs. Since each GN issues credentials to only a subset of the total RNs, compromising a GN would afect only the RNs in its subset, leaving the remaining parts of the system unafected.

Anonymity Group. To distribute trust among more trusted entities, the system needs to group all RNs. After division, each group is also called an anonymous group, and each group has a group node. The RNs randomly request credentials from diferent group nodes based on the output $F _ { s k _ { R } } ( h )$ of the $\mathsf { P r o v e } _ { \mathsf { V R F } } ( \cdot )$ . The process of requesting credentials by RNs is shown in Alg. 1. The RNs obtain a grouping basis h from the bulletin board, where h is the hash value of the information published on the bulletin board in the previous epoch. h is used as input to the $\mathsf { P r o v e } _ { \mathsf { V R F } } ( \cdot )$ . The output $F _ { s k _ { R } } ( h )$ and the proof π<sub>VRF</sub> are generated with the participation of the $\mathrm { R N } \mathbf { \bar { s } } \ s \ k _ { R } .$ . The Gid(·) is a mapping function that returns the identifier of a GN.

(b) Avatar system  
![](images/8fe3b3d60801e5fb24c02131f06bbf5b9f42a4ed30dd2d906b0cb6524afccaec.jpg)  
(a) Partial structure of the system

![](images/0a70001ae07acbce0dc5de1e65091b867fa77b7e1493211d7b60a326737017aa.jpg)

Fig. 3. Phases of Avatar. Fig. 3(a) shows a part of the system, illustrating that the RNs are partitioned into diferent groups to request credentials from the GN by running the VRF. Fig 3(b) illustrates the Avatar algorithm, structured into three distinct phases. Notably, the curly braces in the figure indicate that $R N _ { 1 } , \bar { R } N _ { 2 } ,$ and $R N _ { 3 }$ are included within the set of all RNs.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 GrqGen(·)
Input:  $sk_{R}, h$ 
Output:  $req_{cred}$ 

1:  $(F_{sk_{R}}(h), \pi_{\mathrm{VRF}}) \leftarrow \mathrm{Prove}_{\mathrm{VRF}}(sk_{R}, h)$ 

2:  $id_{G} \leftarrow \mathrm{Gid}(F_{sk_{R}}(h) \mod \beta)$ 

3:  $\sigma \leftarrow \mathrm{Sig}_{\mathrm{BLS}}(sk_{R}, e \| F_{sk_{R}}(h) \| \pi_{\mathrm{VRF}} \| st)$ 

4: Return  $req_{cred} = (e, F_{sk_{R}}(h), \pi_{\mathrm{VRF}}, st, \sigma)$
</div>

The system assigns a range value to each GN. The upper bound $G N _ { i }$ is index and the lower bound is $i n d e x _ { i - 1 }$ . We assume there are M GNs in the system, and the total range assigned to them is $\beta .$ The assigned range values for $( G N _ { 1 } , G N _ { 2 } , . . . G N _ { M } )$ are {(index<sub>0</sub> index<sub>1</sub>) (index<sub>1</sub> index<sub>2</sub>) (index<sub>M−1</sub> index<sub>M</sub>)}. Gid(·) determines where $F _ { s k _ { R } } ( h )$ mod $\beta$ falls within the set {(index<sub>0</sub> index<sub>1</sub>) (index<sub>1</sub> index<sub>2</sub>)    (index<sub>M−1</sub> index<sub>M</sub>)} and then returns the identifier $i d _ { G }$ of the corresponding GN. Subsequently, RN generates a credential request $r e q _ { c r e d }$ and requests a credential from the GN with identifier $i d _ { G } .$ . The $r e q _ { c r e d }$ contains $\mathbf { R N } \mathbf { \bar { s } }$ state information $s t \ ( e . g .$ , bandwidth), a VRF proof π and output $F _ { s k _ { R } } ( h )$ , an epoch number $e ,$ and a signature $\sigma .$ Here we use the BLS to sign the information in $r e q _ { c r e d }$ to ensure the integrity of the information and the authenticity of the source. Other signature schemes can be used, but it is essential to ensure that all computations occur within the same cyclic group.

Request Validation. When the GN receives a credential request from the RN, it executes Alg. 2 to verify the legitimacy of the request $r e q _ { c r e d } .$ . If verification passes, it issues the credential. The GN records all RN’s information and sends it to the bulletin board. This operation serves two purposes: (1) informing other nodes about the group members managed by the GN, and (2) enabling other nodes to verify the legitimacy of the GN’s group members.

• Verify that the given signature is valid. Specifically, if Ver $\mathsf { f y } _ { \mathsf { B L S } } ( p k _ { R } , \sigma , e \| F _ { s k _ { R } } ( h ) \| \pi _ { \mathsf { V R F } } \| s t )$ evaluates to 1, proceed with the next step. Otherwise, reject.

• Verify whether the e matches the current execution epoch of the system. If it does, proceed; otherwise, reject.

• Verify whether the output $F _ { s k _ { R } } ( h )$ of $\mathsf { P r o v e } _ { \mathsf { V R F } } ( \cdot )$ is valid. Specifically, if Verif $\prime _ { \mathsf { V R F } } ( p k _ { R } , h , F _ { s k _ { R } } ( h ) , \pi _ { \mathsf { V R F } } )$ evaluates to 1, proceed with the next step; otherwise, reject.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 GrqVer(·)
Input: $pk_R, req_cred$
Output: 0 or 1
1: parse $req_cred = (e, F_{sk_R}(h), \pi_{VRF}, st, \sigma)$
2: if Verify$_{BLS}(pk_R, \sigma, e \| F_{sk_R}(h) \| \pi_{VRF} \| st)$ then
3:    if $e$ is correct then
4:    if Verify$_{VRF}(pk_R, h, F_{sk_R}(h), \pi_{VRF})$ then
5:    if Gid($F_{sk_R}(h) \mod \beta$) = $id_G$ then
6:    return 1
7:    end if
8:    end if
9:    end if
10: end if
11: return 0

• Compute $F_{sk_R}(h) \mod \beta$. If $F_{sk_R}(h) \mod \beta$ maps to its group identifier, the GN issues a credential to the RN.
</div>

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 3 Credlss(·)
Input: $sk_G, e, id_R$
Output: $cred$
1: $\varepsilon \leftarrow \mathbb{Z}_q^{\$}$
2: $\psi \leftarrow g_1^{1/(sk_G + \varepsilon + id_R + e)}$
3: $return$ $cred = (e, id_R, \varepsilon, \psi)$
</div>

Credential Issuance. Inspired by AAKA [21], we have GNs issue credentials to RNs to ensure the anonymity of RNs during the circuit construction process. However, AAKA’s validation of the credential’s validity period is independent of the credential itself. This can lead to the credential holder forging an arbitrary validity period of the credential. In this paper, we solve this problem. And, we transform this method to make it suitable for anonymous networks. Next, we introduce the process of issuing credentials (see Alg. 3) in anonymous networks.

ε is randomly selected by the GN for each credential issuance, secretly sent to the RN, and securely deleted by the GN afterward. The RN uses ε as an epoch secret key and generates the epoch public key $g _ { 2 } ^ { \varepsilon } .$ . The GN signs $i d _ { R } , e ,$ and ε using BBS to produce the credential $c r e d = ( e , i d _ { R } , \varepsilon , \psi )$ Notably, the credential must be securely transmitted to the RN over a secure channel.

Credential Validation. When the RN receives the issued credential cred from the GN, it validates the credential (see Alg. 4). If the validation passes, the RN securely stores the credential. In each epoch, the RN will use the credential to achieve anonymity during the circuit construction. It is important to note that in each epoch, an RN joins a new group and acquires a new credential to ensure continued anonymity.

• Verify the correctness of e and $i d _ { R } .$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 4 CredVer(·)
Input: $pk_G$, cred
Output: 0 or 1
1: parse $cred = (e, id_R, \varepsilon, \psi)$
2: if $id_R$ and e are correct then
3: if $e(\psi, pk_G \cdot g_2^{\varepsilon + id_R + e}) = e(g_1, g_2)$ then
4: return 1
5: end if
6: end if
7: return 0
</div>

• Verify that $\psi$ correctly signed the $\varepsilon , i d _ { R }$ and e. $\mathrm { I f } \ e ( \psi , p k _ { G } .$ $g _ { 2 } ^ { \varepsilon + i d _ { R } + e } ) = e ( g _ { 1 } , g _ { 2 } )$ , output 1 and accept the credential. Otherwise, reject the credential.

Discussion. In practical deployment, two critical factors must be considered during the distribution phase. First, a newly joined RN should not immediately participate in the ongoing grouping process. Allowing such participation would enable an adversary to repeatedly rejoin the system with diferent identities and private keys to manipulate the computation of $F _ { s k _ { R } } ( h )$ , thereby biasing the grouping outcome and undermining randomness. To mitigate this risk, a reasonable waiting period based on the system’s grouping epoch can be introduced before newly joined RNs are allowed to participate in the computation process.

Secondly, it is essential to guarantee the security of the GN and the process of issuing credentials from the GN to the RN. We consider the scenario in which the GN is compromised by an adversary. In such cases, the GN could issue credentials to malicious or unauthorized RNs, posing a serious threat to the system. To mitigate this, we propose using trusted hardware to protect the GN, specifically by storing the private key within a Trusted Execution Environment (TEE). While this enhances security, it introduces challenges such as deployment complexity. To ease deployment, we can utilize cloud platforms to deploy trusted components. The Tor network has already demonstrated the feasibility of this strategy by providing default VM images to run bridges on Amazon EC2 cloud [8].

For cases where trusted hardware is unavailable or untrusted, we propose a cryptographic alternative. During the circuit construction phase, each relay node $R N _ { i }$ verifies its successor $R N _ { i + 1 } \mathrm { { ' s } }$ legitimacy. This process involves two steps. First, $R N _ { i }$ verifies the VRF output and the corresponding proof submitted by $R N _ { i + 1 }$ to a public bulletin board to confirm that

![](images/88095c130ace1d2046c82bec4f79eb3761a1030a79bc0e683ab819698025f7c6.jpg)  
Fig. 4. Original onion-routing protocol.

$R N _ { i + 1 }$ has been correctly assigned to a specific group. Second, $R N _ { i }$ ensures that the credential presented by $R N _ { i + 1 }$ was issued by the GN associated with the group. If either verification fails, $R N _ { i }$ reports the error to the bulletin board. This shifts trust from hardware to cryptographic security. Additionally, Avatar can support full decentralization via a leader election algorithm, selecting a random subset of volunteer nodes as GNs each epoch, which is a direction for future work. This cryptographic approach can also complement trusted hardware to further enhance security.

## C. PAC Construction Phase

To guarantee the confidentiality and integrity of the data transmitted between CN and SN, the CN employs a multilayer encryption method. We will first briefly introduce the Onion Routing protocol and the Walking Onions protocol, and then elaborate on our circuit construction protocol.

Original Onion-Routing Protocol In the original Tor network’s onion-routing protocol [2], the CN downloads information about RNs from the DA to ensure the freshness of relay data. During the circuit construction phase, CN needs to select multiple relay nodes and then negotiate keys with each selected relay node individually. The key exchange protocol is illustrated in Fig. 4, and is simply described as follows.

• CN constructs an anonymous circuit by selecting three relays, $R N _ { 1 } , R N _ { 2 }$ , and $R N _ { 3 }$ , from the relay consensus directory downloaded from DA.

• CN generates a temporary key pair $( x _ { 1 } , g ^ { x _ { 1 } } )$ and encrypts $g ^ { x _ { 1 } }$ using $R N _ { 1 } { \mathrm { : } }$ ’s long-term public key before transmitting it to $R N _ { 1 } . ~ g$ is a generator of a group G with prime order $q .$

$R N _ { 1 }$ decrypts $E ( g ^ { x _ { 1 } } )$ with its long-term private key to obtain $g ^ { x _ { 1 } }$ . It generates a temporary key pair $( y _ { 1 } , g ^ { y _ { 1 } } )$ and computes the shared key $k _ { 1 } = ( g ^ { x _ { 1 } } ) ^ { y _ { 1 } }$ $R N _ { 1 }$ then securely stores $k _ { 1 }$ and responds to CN with $g ^ { y _ { 1 } }$ and $H ( k _ { 1 } )$

• CN receives $g ^ { y _ { 1 } }$ and $H ( k _ { 1 } )$ , computes the shared key $k _ { 1 } = ( g ^ { y _ { 1 } } ) ^ { x }$ <sup>1</sup>, and verifies the correctness of $H ( k _ { 1 } )$ . If the verification succeeds, CN securely stores $k _ { 1 }$ .

• CN again generates a temporary key pair $( x _ { 2 } , g ^ { x _ { 2 } } )$ and encrypts $g ^ { x _ { 2 } }$ with $R N _ { 2 } ^ { \prime } \mathrm { s }$ long-term public key. Then, CN encrypts the circuit expansion information using the shared key $k _ { 1 }$ and sends it to $R N _ { 1 }$

$R N _ { 1 }$ decrypts the ciphertext after receiving the encrypted circuit expansion information from CN, and then sends the decrypted information to RN .

$R N _ { 2 }$ decrypts $E ( g ^ { x _ { 2 } } )$ with its long-term private key to obtain $g ^ { x _ { 2 } }$ . It generates a temporary key pair $( y _ { 2 } , g ^ { y _ { 2 } } )$ and computes the shared key $k _ { 2 } = ( g ^ { x _ { 2 } } ) ^ { y _ { 2 } } . R N _ { 2 }$ then securely stores $k _ { 2 }$ and responds to $R N _ { 1 }$ with $g ^ { y _ { 2 } }$ and $H ( k _ { 2 } )$ .

![](images/e254fe4499fae416ac5b50e51b45e21fca6902c28c99e85e531f7a45f11827ed.jpg)  
Fig. 5. Single-pass walking onions protocol.

• After receiving the response message from $R N _ { 2 } , \ R N _ { 1 }$ encrypts the information using the shared key $k _ { 1 }$ and then sends the ciphertext to CN through the circuit $c _ { 1 }$

• After receiving the response from $R N _ { 1 } ,$ , CN decrypts the ciphertext using the shared key $k _ { 1 }$ . Then, CN computes the shared key $k _ { 2 } = ( g ^ { y _ { 2 } } ) ^ { x _ { 2 } }$ and verifies if the hash $H ( k _ { 2 } )$ is correct. If it is correct, CN stores $k _ { 1 }$

The process described above outlines how CN establishes shared keys with $R N _ { 1 }$ and $R N _ { 2 }$ . Key negotiation with subsequent relays follows a similar process. Ultimately, CN obtains shared keys with each relay, which are then used to encrypt the message in layers. As the ciphertext passes through each relay, one encryption layer is removed. Ultimately, when the message reaches the target server, it is exactly the original message that the CN intended to send.

Single-Pass Walking Onions Protocol. The Single-Pass Walking Onions protocol, introduced in [4], is a path selection and circuit construction protocol. In this protocol, a client constructs a circuit by sending and receiving only a single message each. For path selection, Walking Onions employs a verifiable random function to determine the next hop in the circuit. The key exchange protocol, depicted in Fig. $^ { 5 , }$ can be summarized as follows.

1) CN generates two temporary key pairs $( x , g ^ { x } )$ and $( d , g ^ { d } )$ and sets the circuit extension length $T = 2$ . It then sends $( X = g ^ { x } , D = g ^ { d } , T )$ to $R N _ { 1 }$

2) $R N _ { 1 }$ generates a temporary key pair $( y _ { 1 } , g ^ { y _ { 1 } } )$ and computes the shared key $k _ { 1 } ~ = ~ X ^ { y _ { 1 } }$ . It also generates a signature $A _ { 1 }$ for $g ^ { y _ { 1 } }$ . Next, RN computes $( \beta _ { 2 } , \pi _ { 2 } ) $ $\mathsf { P r o v e } _ { \mathsf { V R F } } ( c _ { 1 } , D ^ { b _ { 1 } } )$ using its path-selection private key $c _ { 1 }$ and long-term private key $b _ { 1 }$ . Two blinding factors are then derived: $r _ { 1 } \gets H _ { \mathbb { Z } _ { q } } ( k _ { 1 } )$ and $\nu _ { 1 } \gets H _ { \mathbb { Z } _ { a } } ( D ^ { b _ { 1 } } )$ , used to blind X and $D ,$ respectively. After completing these operations, $R N _ { 1 }$ determines the identity of RN based on $\beta _ { 2 }$ . It then securely transmits the information (X D T) to $R N _ { 2 }$

3) $R N _ { 2 }$ follows similar steps as $R N _ { 1 }$

4) $R N _ { 3 }$ generates a temporary key pair $( y _ { 3 } , g ^ { y _ { 3 } } )$ and computes the shared key $k _ { 3 } ~ = ~ X ^ { y _ { 3 } }$ . It also generates a signature $A _ { 3 }$ for $g ^ { y _ { 3 } }$ . Subsequently, $R N _ { 3 }$ sends the information $\rho _ { 3 }$ to $R N _ { 2 }$

5) After receiving the reply from $R N _ { 3 } , \ R N _ { 2 }$ performs a symmetric encryption operation $E _ { k _ { 2 } } [ \Sigma _ { 3 } , \beta _ { 3 } , \pi _ { 3 } , \rho _ { 3 } ]$ where $\Sigma _ { 3 }$ represents $R N _ { 3 } ^ { \mathbf { \Upsilon } } \mathbf { s }$ information signed by the DA. RN then replies with $\rho _ { 2 }$ to $R N _ { 1 }$

6) Upon receiving $\rho _ { 2 } , R N _ { 1 }$ executes similar steps as $R N _ { 2 }$

7) Upon receiving $\rho _ { 1 }$ , CN extracts $( g ^ { y _ { 1 } } , A _ { 1 } )$ , verifies $A _ { 1 }$ and computes the shared key $k _ { 1 } = ( g ^ { y _ { 1 } } ) ^ { x }$ . Using $k _ { 1 } ,$ CN decrypts the remaining portion of $\rho _ { 1 }$ . It then performs $\mathrm { V R F } _ { \mathrm { V e r i f y } } ( \cdot )$ to authenticate the next hop, $R N _ { 2 }$ . If the verification succeeds, CN continues with the next cyclic operation on $\rho _ { 2 }$ . After completing all iterations, CN successfully obtains $k _ { 1 } , k _ { 2 } , k _ { 3 }$

Our Protocol. In comparison with the Onion Routing and Walking Onions protocols, PAC adopts the following design. First, PAC builds circuits using the single-pass idea from Walking Onions. In this method, the client sends and receives only one message during circuit construction, which reduces the efect of network latency on eficiency. Similar to Onion Routing and Walking Onions, PAC ensures the trustworthiness of relays during the circuit construction, preventing man-in-themiddle attacks and related threats. To achieve relay anonymity with authentication, PAC uses an anonymous authentication scheme based on anonymous credentials [16], [21]. These credentials verify relay identities and also prove that a blinded key originates from the epoch public key. Once verified, this blinded key serves as the verification key for both the AVRF output and the signature.

Relay selection within the circuit is determined by the output of the AVRF. Unlike Walking Onions [4], which directly adopts VRFs, PAC employs AVRFs to preserve relay anonymity. By introducing AVRFs, PAC achieves both relay anonymity and randomness. To balance randomness with other performance requirements, such as latency, each relay node can independently select the next hop from the anonymous group according to predefined rules. Ganesh et al. [19] use complex zero-knowledge membership proofs to prove the reliability of the AVRF blinded public key, but these must be reconstructed whenever group membership changes. In contrast, PAC uses anonymous credentials to prove the trustworthiness of blinded public keys. This proof remains valid even when membership changes, making the method simpler and more eficient. Furthermore, PAC introduces a signature scheme with key blinding to ensure message integrity and authenticity during circuit construction. If attribute-based anonymous credentials were used to ensure message trustworthiness, a new credential would need to be generated for each message, resulting in significant time and resource overhead. By using anonymous credentials to prove the blinded public key for signatures, PAC avoids this overhead. Therefore, anonymous credentials in PAC serve as the link between the AVRF and the signature with key blinding, allowing us to construct circuits that simultaneously achieve randomness, anonymity, and eficiency.

To illustrate the PAC protocol, we use a circuit example involving $\{ C N , R N _ { 1 } , R N _ { 2 } , \ldots , R N _ { n } \}$ . Each relay node $R N _ { i }$ belongs to a group managed by a corresponding group node $G N _ { i }$ . This circuit is scalable, with the hop count T indicating the length of circuit extensions. With each expansion, the hop count decreases by 1, and the circuit stops expanding when $T$ reaches 0.

Initialization. As shown in Alg. 5, the CN executes the following operations when a circuit is constructed:

1) CN generates a temporary key pair $( u _ { 1 } , g ^ { u _ { 1 } } )$

2) Generate a random value $\tau _ { 1 }$ and send it to the next node. This ensures the next node cannot control the AVRF input, preventing it from obtaining an advantageous output.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 5 Circlnit(·)
Output: req1
1: $u_1 \leftarrow \mathbb{Z}_q, U_1 \leftarrow g_1^{u_1}$
2: $\tau_1 \leftarrow \mathbb{G}_1$
3: $y \leftarrow \mathcal{R}, id_{G_1} \leftarrow \text{Gid}(y \bmod \beta)$
4: $id_{R_1} \leftarrow \text{Group\_Member}(id_{G_1})$
5: $T = n - 1$
6: return req1 = (U1, τ1, T)
</div>

3) Generate a random value y, selected from the set R of real numbers. y is used as input into Gid(·) to obtain $i d _ { G _ { 1 } }$ about a $G N _ { 1 }$ . The purpose of the Group Member(·) function is to select the next node in the circuit. Here, we haven’t precisely defined the Group Member(·) function. After inputting the $i d _ { G _ { 1 } }$ , the Group Member(·) will choose a group member of $G N _ { 1 }$ as the next node based on pre-defined rules. These rules can include random selection, bandwidth-based selection, etc. Here, the CN will select a trusted node as the first hop.

4) $U _ { 1 } , \ \tau _ { 1 }$ , and T are sent together to the next node $R N _ { 1 }$ selected by the Group Member(·) according to predefined rules.

In practice, 3) can be omitted, and a bridge can be used as the first node of the circuit, similar to the current Tor network. When the bridge serves as the entry node, users no longer need to download relay information. Instead, the relay information is exchanged only between the group nodes and the relays, and users only need to know the bridge address and the identities of the group nodes to construct the anonymous circuit.

Forward. The function of the RN is message forwarding. It is responsible for forwarding two types of messages: request messages and response messages. Consequently, the CircFwd(·) process is divided into two parts: $\mathsf { C i r c F w d } _ { 1 } ( \cdot )$ (see Alg. 6), which handles the forwarding of request messages, and $\mathsf { C i r c F w d } _ { 2 } ( \cdot )$ (see $\mathrm { A l g . ~ } 7 )$ , which handles the forwarding of response messages. The detailed description of $\mathrm { A l g } .$ . 6 is as follows.

1) Generate a temporary key pair $( \nu _ { i } , g _ { 1 } ^ { \nu _ { i } } )$ and an epoch public key $r p k _ { i } = ( g _ { 2 } , g _ { 2 } ^ { \varepsilon _ { i } } )$ . Here, the epoch private key $r s k _ { i } = \varepsilon _ { i }$ was secretly sent to $R N _ { i }$ when the credential was previously issued by $G N _ { i }$

2) Compute $U _ { i } ^ { \nu _ { i } }$ . Here, an adversary hardly obtains $U _ { i } ^ { \nu _ { i } }$ under the Decisional Difie-Hellman (DDH) assumption.

3) $U _ { i } , V _ { i }$ and $U _ { i } ^ { \nu _ { i } }$ are input into the key derivation function $H _ { K }$ to obtain the shared key $k _ { i } \in \mathcal { K }$ , as well as additional random values $k _ { i } ^ { \prime } \in \mathbb { Z } _ { q }$ and $k _ { i } ^ { \prime \prime } \in \mathbb { Z } _ { q }$

4) Use the random value $k _ { i } ^ { \prime }$ to blind $U _ { i }$ , obtaining $U _ { i + 1 } \gets$ $U _ { i } ^ { k _ { i } ^ { \prime } }$ , and use $k _ { i } ^ { \prime \prime }$ to blind $\tau _ { i } ,$ obtaining $\tau _ { i + 1 } \gets \tau _ { i } ^ { \kappa _ { i } }$

5) Generate a blinding value $\gamma _ { i }$ . The value $\gamma _ { i }$ is used to blind $r p k _ { i } , p k _ { G _ { i } }$ , and the credentials issued by $G N _ { i }$

6) Use $\gamma _ { i }$ to blind rpk<sub>i</sub> to obtain $r p k _ { i } ^ { \prime } = ( g _ { 2 } ^ { \gamma _ { i } } , \hat { g } _ { 2 } ^ { \varepsilon _ { i } \gamma _ { i } } )$ . The blinded epoch public key $r p k _ { i } ^ { \prime }$ can verify the output of $\mathsf { P r o v e } _ { \mathsf { A V R F } } ( \cdot )$ and the signature on the $V _ { i } .$ However, $r p k _ { i } ^ { \prime }$ does not reveal the true identity of $R N _ { i }$ , and adversaries cannot link diferent $r p k ^ { \prime }$ together based on the DDH.

7) Execute $\mathsf { P r o v e } _ { \mathsf { A V R F } } ( \cdot )$ to generate an output $F _ { r s k _ { i } } ( \tau _ { i } )$ along with a corresponding proof $\pi _ { i } ^ { \prime } .$

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 6 CircFwd$_{1}$(·)
Input: req$_{i}$
Output: req$_{i+1}$
1: parse req$_{i}$ = (Ui, τ$_{i}$, T)
2: vi ← $\mathbb{Z}_{q}$, Vi ← g$_{1}^{vi}$, rpk$_{i}$ = (g$_{2}$, g$_{2}^{\varepsilon_{i}}$)
3: (k$_{i}$, k$_{i}'$, k$_{i}''$) ← H$_{K}$(Ui, Vi, U$_{i}^{vi}$)
4: U$_{i+1}$ ← U$_{i}^{k_{i}'}$, τ$_{i+1}$ ← τ$_{i}^{k_{i}''}$
5: γ$_{i}$ ← $\mathbb{Z}_{q}$, rpk$_{i}'$ ← Update$_{\text{AVRF}}$(rpk$_{i}$)
6: (Frsk$_{i}$(τ$_{i}$), π$_{i}'$) ← Prove$_{\text{AVRF}}$(rsk$_{i}$, rpk$_{i}'$, τ$_{i}$)
7: id$_{G_{i+1}}$ ← Gid(Frsk$_{i}$(τ$_{i}$) mod β)
8: id$_{R_{i+1}}$ ← Group_Member(id$_{G_{i+1}}$)
9: T = T - 1
10: return req$_{i+1}$ = (U$_{i+1}$, τ$_{i+1}$, T)
</div>

8) Process $F _ { r s k _ { i } } ( \tau _ { i } )$ to determine the identity $i d _ { R _ { i + } }$ of the next relay node $R N _ { i + 1 } ,$ , similar to how CN processes $y .$

$$
r e q _ {i + 1}
$$

9) Reduce the hop count by 1, then forward req<sub>i+1</sub> to the next node $R N _ { i + 1 }$ for further processing. After $R N _ { i \in [ 1 , \dots , n - 1 ] }$ completes Alg. 6, it waits for the response $r e s _ { i + 1 }$ from $R N _ { i + 1 }$ . Then, the process continues with the execution of Alg. 7. The following is a detailed description of Alg. 7.

10 Blind the credential issued by the $G N _ { i }$ using $\gamma _ { i }$ to obtain an anonymous credential.

• An anonymity credential $\psi _ { i } ^ { \prime } = \psi ^ { \gamma _ { i } }$ is generated.

• An auxiliary parameter, designated as $\bar { \psi } _ { i } = { \psi } _ { i } ^ { \prime - i d _ { R _ { i } } }$ $g _ { 1 } ^ { \gamma _ { i } } ,$ is generated. The form of $\bar { \psi } _ { i }$ difers from the schemes proposed by Camenisch et al. [16] and Yu et al. [21] due to the addition of two further attributes to the anonymous credential. The first attribute permits verification that the anonymous credential was issued in the current epoch of the system. The second attribute allows verifying the validity of $R N _ { i } { ' } \mathrm { s }$ blinded epoch public key via the credential.

11) Use $\gamma _ { i }$ to blind the public key $p k _ { G _ { i } }$ of the group node that issued the credential, obtaining $p k _ { G _ { i } } ^ { \prime }$

12) A zero-knowledge proof

$$
\pi_ {i} ^ {\prime \prime} = P K \{(i d _ {R _ {i}}, \gamma_ {i}): \bar {\psi} _ {i} = \psi_ {i} ^ {' - i d _ {R _ {i}}} \cdot g _ {1} ^ {\gamma_ {i}}, p k _ {G _ {i}} ^ {\prime} = p k _ {G _ {i}} ^ {\gamma_ {i}} \}\tag{1}
$$

should be constructed to prove ${ \bar { \psi } } _ { i }$ is the correct form and $p k _ { G _ { i } } ^ { \prime }$ is derived from $p k _ { G _ { i } }$ . To construct (1), the CN acts as the verifier, while the $R N _ { i }$ as the prover and performs the following operations:

• Randomly take $a , b \in \mathbb { Z } _ { q }$ and choose a challenge C.

• Compute $s _ { 1 } = a + C i d _ { R _ { i } }$ and $s _ { 2 } = b + C \gamma _ { i }$

• Generate two commitments $C o m _ { 1 } ( i d _ { R _ { i } } , \gamma _ { i } ) = { \psi _ { i } ^ { \prime - a } }$ $g _ { 1 } ^ { b }$ and $C o m _ { 2 } ( \gamma _ { i } ) = p k _ { G _ { i } } ^ { b }$

• Send $( \mathrm { C o m } _ { 1 } ( i d _ { R _ { i } } , \gamma _ { i } ) , \mathrm { C o m } _ { 2 } ( \gamma _ { i } ) , C , s _ { 1 } , s _ { 2 } )$ to verifier. Finally, the verifier checks $\psi _ { i } ^ { \prime - s _ { 1 } } \cdot g _ { 1 } ^ { s _ { 2 } } \stackrel { ? } { = } C o m _ { 1 } ( i d _ { R _ { i } } , \gamma _ { i } ) \cdot \bar { \psi } _ { i } ^ { C }$ and $p k _ { G _ { i } } ^ { s _ { 2 } } \overset { ? } { = } C o m _ { 2 } ( \gamma _ { i } ) { \cdot } p k _ { G _ { i } } ^ { \prime C }$ . Then, we define the challenge $C ~ = ~ { \cal H } _ { \mathrm { Z } _ { a } } ^ { ' } ( \mathrm { C o m } _ { 1 } ( i d _ { R _ { i } } , \gamma _ { i } ) | | \mathrm { C o m } _ { 2 } ( \gamma _ { i } ) | | \tau _ { i } )$ , which must be random and uniquely identify the commitment.

13) Generate a BLS signature $\sigma _ { i }$ on the temporary public key of $R N _ { i } .$ Unlike the original BLS signature, here we use the blinded epoch public key $r p k _ { i } ^ { \prime }$ to verify the signature. It is essential that the hash computation within the BLS signature here must be mapped to the group $\mathbb { G } _ { 1 } .$

```python
Algorithm 7 CircFwd₂(·)
Input: resi+1
Output: resi
1: ψ'i ← ψγi, ψ̅i ← ψ'i'−idRi · gγi
2: pk′G_i ← pkγi_Gi
3: π''i = PK{(idR_i, γi) : ψ̅i = ψ'i'−idR_i · gγi, pk′G_i = pkγi_Gi}
4: σi ← SigBLS(rsk_i · γi, V_i)
5: ci ← Enc(k_i, resi+1)
6: resi = (e, V_i, σi, rpk'i, pk′G_j, ψ'i, ψ̅i, Frsk_i(τ_i), π'i, π''i, ci)
7: return resi
```

14) Use $k _ { i }$ to encrypt $r e s _ { i + 1 }$ and then reply $r e s _ { i }$ to $R N _ { i - 1 }$ or CN. If the index of RN is 1, then reply $r e s _ { 1 }$ to CN.

When $R N _ { n }$ receives a circuit extension request, $R N _ { n }$ also executes Alg. 6. However, since $R N _ { n }$ no longer continues to expand the circuit, the steps related to circuit expansion can be skipped, and the corresponding return values can be set to null.

CN Verification. CN executes $\mathrm { A l g . }$ . 8 after receiving the information returned from $R N _ { 1 }$ . Alg. 8 is a loop function. So CN repeatedly executes the following operations:

1) Verify whether $\pi _ { i } ^ { \prime \prime }$ is valid. If valid, it indicates that $\bar { \psi } _ { i } =$ $\psi _ { i } ^ { \prime - i d _ { R _ { i } } } \cdot g _ { 1 } ^ { \gamma _ { i } }$ and $p k _ { G _ { i } } ^ { \prime } = p k _ { G _ { i } } ^ { \gamma _ { i } }$

2) Verify whether e is valid, and check whether:

$$
e (\bar {\psi} _ {i}, r p k _ {i} ^ {\prime} [ 0 ]) \stackrel {?} {=} e (\psi_ {i} ^ {\prime}, r p k _ {i} ^ {\prime} [ 0 ] ^ {e} \cdot r p k _ {i} ^ {\prime} [ 1 ] \cdot p k _ {G _ {i}} ^ {\prime}).
$$

If the verification is successful, it confirms that RN holds valid credentials issued by $G N _ { i } ,$ and that $r p k _ { i } ^ { \prime }$ originates from RN<sub>i</sub>’s epoch public key $r p k _ { i }$ for the current epoch.

3) Verify the blind BLS signature $\sigma _ { i } .$ If $\begin{array} { r l r } { e ( \sigma _ { i } , g _ { 2 } ) } & { { } = } & { e ( H _ { \mathbb { G } _ { 1 } } ( V _ { i } ) , r p k _ { i } ^ { \prime } [ 1 ] ) } \end{array}$ $\sigma _ { i }$ is valid. CN computes $( k _ { i } , k _ { i } ^ { \prime } , k _ { i } ^ { \prime \prime } ) \  H _ { K } ( \dot { U } _ { i } , V _ { i } , V _ { i } ^ { u _ { i } } )$ and decrypts $c _ { i }$ with $k _ { i }$ to obtain $r e s _ { i + 1 }$

4) Run ${ \mathsf { V e r i f y } } _ { \mathsf { A V R F } } ( \cdot )$ to determine whether $F _ { r s k _ { i } } ( \tau _ { i } )$ is correct and verify that $F _ { r s k _ { i } } ( \tau _ { i } )$ is indeed computed with the participation of $R N _ { i } ^ { \mathbf { \gamma } } \mathbf { s }$ epoch private key $\varepsilon _ { i } .$

5) Execute $\mathsf { G i d } ( F _ { r s k _ { i } } ( \tau _ { i } )$ mod $\beta )$ to obtain $i d _ { G _ { i + 1 } }$ , and the group node corresponding to $i d _ { G _ { i + 1 } }$ is denoted as $G N _ { i + 1 }$ Then CN can query to get the information about $G N _ { i + 1 } .$ 6) Use $k _ { i } ^ { \prime }$ and $k _ { i } ^ { \prime \prime }$ to blind $U _ { i }$ and $\tau _ { i } ,$ resulting in $U _ { i + 1 }$ and $\tau _ { i + 1 } .$ . To calculate $V _ { i + 1 } ^ { u _ { i + 1 } }$ in the next loop, $u _ { i + 1 } \ = \ u _ { i } k _ { i } ^ { \prime }$ needs to be calculated in the current loop.

After constructing an anonymous circuit, CN obtains shared keys $k _ { 1 } , k _ { 2 } , . . . , k _ { n }$ . Then, CN uses a multi-layer encryption, similar to the Tor network, to communicate with the $\mathbf { S N } .$

Quantify. We use entropy as a metric to quantify the anonymity of relays within an anonymous circuit. Higher entropy indicates greater uncertainty in path selection, making it more dificult for an adversary to determine the communication route. For an adversary capable of path probing, systems such as Tor, SGX-Tor, SmarTor, and Walking Onions all expose relay public keys during circuit construction, resulting in a deterministic and uniquely identifiable path. Consequently, their circuit entropy is efectively zero. In contrast, Avatar introduces uncertainty in path selection. Its circuit entropy depends on the number of hops T and the size of the relay anonymity set $\vec { A }$ at each hop. For the small-scale anonymous networks discussed in the next subsection, $\vec { A }$ is essentially equivalent to the total number of relays. If the anonymity entropy per hop is $\begin{array} { r } { H _ { j } = - \sum _ { i = 1 } ^ { | \vec { A } | } p _ { i } \log _ { 2 } { p _ { i } } } \end{array}$ , where $p _ { i }$ is the probability that relay RN ∈ A<sup>\~</sup> is selected. The total circuit entropy is $\begin{array} { r c l } { H _ { t o t a l } } & { = } & { \sum _ { j = 1 } ^ { T } H _ { j } , } \end{array}$ significantly increasing the uncertainty of the path from the adversary’s perspective.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 8 CircVer(·)

Input:  $res_{1}$ 

Output:  $\vec{k}$ 

1:  $\vec{k} \leftarrow \{\}$ 

2: for  $i \in \{1, \ldots, n\}$  do

3: parse  $res_{i} = (e, V_{i}, \sigma_{i}, rpk_{i}', pk_{G_{i}}', \psi_{i}', \bar{\psi}_{i}, F_{rsk_{i}}(\tau_{i}), \pi_{i}', \pi_{i}'', c_{i})$ 

4: if  $\pi_{i}''$  is valid then

5: if  $e(\bar{\psi}_{i}, rpk_{i}'[0]) \stackrel{?}{=} e(\psi_{i}', rpk_{i}'[0]^{e} \cdot rpk_{i}'[1] \cdot pk_{G_{i}}')$  then

6: if  $\text{Verify}_{\text{BLS}}(rpk_{i}'[1], \sigma_{i}, V_{i})$  then

7:  $(k_{i}, k_{i}', k_{i}') \leftarrow H_{K}(U_{i}, V_{i}, V_{i}^{u_{i}})$ 

8:  $\vec{k} \leftarrow \vec{k} \cup \{k_{i}\}$ 

9: if  $i \neq n$  then

10:  $res_{i+1} \leftarrow \text{Dec}(k_{i}, c_{i})$ 

11: if  $\text{Verify}_{\text{AVRF}}(rpk_{i}', \tau_{i}, F_{rsk_{i}}(\tau_{i}), \pi_{i}')$  then

12:  $id_{G_{i+1}} \leftarrow \text{Gid}(F_{rsk_{i}}(\tau_{i}) \mod \beta)$ 

13:  $U_{i+1} \leftarrow U_{i}'^{k_{i}}, \tau_{i+1} \leftarrow \tau_{i}'^{k_{i}''}$ 

14:  $u_{i+1} \leftarrow u_{i} k_{i}'$ 

15: end if

16: end if

17: end if

18: end if

19: end if

20: end for

21: return  $\vec{k}$
</div>

## D. Anonymity in A Small-Scale Anonymous Network

While our scheme provides enhanced relay anonymity in large-scale anonymous network scenarios, it is also imperative to consider the potential implications in the context of small-scale anonymous networks established by specific organizations or individuals. Let us consider the case where each GN issues credentials to m RNs. In this scenario, there are $m ^ { T }$ potential compositions for any T-hop circuit. However, in extreme cases where each GN only issues credentials to one RN, knowledge of the GN associated with each hop in the circuit would enable the determination of a specific circuit with certainty. In such a scenario, the anonymity of the relay would be compromised. A small-scale anonymous network where each GN issues an insuficient number of credentials would render it more susceptible to adversarial attacks, facilitating the identification of a unique circuit. Consequently, we have adapted the original scheme in Avatar to enhance its suitability for small-scale anonymity networks.

The supplementary scheme introduces only slight modifications in comparison to the previously described scheme. First, it enables credential verification without exposing the GN’s public key. Here, we only provide GN’s blinded public key $p k _ { G } ^ { \prime }$ and modify the corresponding zero-knowledge proof. We can ofer a membership proof to demonstrate that $p k _ { G } ^ { \prime }$ is a blinded version of one of the public keys from all group nodes. Second, regarding the proof that a random circuit was constructed, we adopt the following approach. After each distribution phase is completed, the RN is required to generate a relay list based on the information obtained from the BN. As illustrated in Tab. II, we have provided a list of the relays for RN. In the process of generating the relay list, the RN computes a shared value $( g _ { 2 } ^ { \varepsilon _ { j } } ) ^ { \varepsilon }$ by combining its epoch private key ε with the epoch public key $g _ { 2 } ^ { \varepsilon _ { j } }$ of $R N _ { j } ~ ( j \in \{ 1 , . . N \} , R N _ { j } \neq R N )$ . Each shared value is input into a hash function H, and the resulting hash value is modulo the range value θ to obtain $s _ { j } .$ The range value θ is set based on probability, and later we will provide a detailed explanation of this probability. The value $s _ { j }$ will be uniformly randomly distributed within the set $\left\{ 0 , \ldots , \bar { \theta } \right\}$ . Notably, the relay list must be generated before the anonymous credentials for the current epoch take efect.

TABLE II  
THE RELAY LIST

<table><tr><td>Relay</td><td>Epoch pk</td><td>Shared value</td><td>IP, etc.</td></tr><tr><td> $RN_{1}$ </td><td> $g_{2}^{\varepsilon_{1}}$ </td><td> $(g_{2}^{\varepsilon_{1}})^{\varepsilon},s_{1}$ </td><td>...</td></tr><tr><td> $RN_{2}$ </td><td> $g_{2}^{\varepsilon_{2}}$ </td><td> $(g_{2}^{\varepsilon_{2}})^{\varepsilon},s_{2}$ </td><td>...</td></tr><tr><td>...</td><td>...</td><td>...</td><td>...</td></tr><tr><td> $RN_{N-1}$ </td><td> $g_{2}^{\varepsilon_{N-1}}$ </td><td> $(g_{2}^{\varepsilon_{N-1}})^{\varepsilon},s_{N-1}$ </td><td>...</td></tr><tr><td> $RN_{N}$ </td><td> $g_{2}^{\varepsilon_{N}}$ </td><td> $(g_{2}^{\varepsilon_{N}})^{\varepsilon},s_{N}$ </td><td>...</td></tr></table>

Here, the subscript of RN only indicates its order in this table and is not related to its order in the circuit.

In the PAC, each relay selects the anonymous group to which the next-hop node belongs based on the output of the $\mathsf { P r o v e _ { A V R F } }$ . Subsequently, each relay selects a relay within the anonymity group chosen as its next hop, based on the pre-defined rules. The protocol demonstrates satisfactory randomness and relay anonymity in scenarios comprising numerous anonymity groups and members. In small-scale anonymity networks, the next relay is selected by comparing $F _ { r s k } ( \tau )$ mod θ with $s _ { j }$ from the relay list. A simple relation is defined between them, for example, $| F _ { r s k } ( \tau )$ mod $\theta - s _ { j } | \leq \lfloor \varpi \rfloor$ \$, similar to $\theta ,$ is defined based on probabilistic configurations. At this point, we enhance the anonymity of the relay by concealing it within the entire list of relays, thereby improving the anonymity of relays in small-scale anonymity networks. To verify whether each relay honestly selects the subsequent relay, the shared values $( g _ { 2 } ^ { \varepsilon _ { j } } ) ^ { \overline { \varepsilon } }$ can be employed for verification purposes. The protocol in IV-C will now be modified. Only a few of these steps are changed, and the original PAC protocol continues for those that are not specified.

## - Initialization.

3) CN directly selects a node with a high level of trust as the first hop in the circuit.

\- Forward.

8) RN<sub>i</sub> searches the relay list to identify the parameter $s _ { j }$ that matches $F _ { r s k _ { i } } ( \tau _ { i } )$ mod θ. If a matching $s _ { j }$ is found, the corresponding relay is therefore eligible to be chosen as the next hop in the circuit.

14) In comparison to the original $r e s _ { i }$ in the PAC protocol, we have added four new fields to res as required: $g _ { 2 } ^ { \varepsilon _ { i } \varepsilon _ { i + 1 } } , ( g _ { 2 } ^ { \varepsilon _ { i + 1 } \gamma _ { i + 1 } } ) ^ { \frac { 1 } { \gamma _ { i } } } , \left( g _ { 2 } ^ { \frac { \varepsilon _ { i } } { \gamma _ { i + 1 } } } \right) ^ { \gamma _ { i } } , g _ { 2 } ^ { \frac { \varepsilon _ { i - 1 } } { \gamma _ { i } } }$ . Next, we will explain these four fields.

${ g } _ { 2 } ^ { \varepsilon _ { i } \varepsilon _ { i + 1 } }$ is a shared value provided by $R N _ { i }$ to the CN, serving as proof that $R N _ { i + 1 }$ was randomly selected.

$( g _ { 2 } ^ { \varepsilon _ { i + 1 } \gamma _ { i + 1 } } ) ^ { \frac { 1 } { \gamma _ { i } } }$ is an auxiliary parameter, where $g _ { 2 } ^ { \varepsilon _ { i + 1 } \gamma _ { i + 1 } }$ can be obtained from $r e s _ { i + 1 }$ . It can be proven that $( g _ { 2 } ^ { \varepsilon _ { i + 1 } \gamma _ { i + 1 } } ) ^ { \frac { 1 } { \gamma _ { i } } }$ is derived from the blinded public key $g _ { 2 } ^ { \varepsilon _ { i + 1 } \gamma _ { i + 1 } }$ of $R N _ { i + 1 } .$

$\left( g _ { 2 } ^ { \frac { \varepsilon _ { i } } { \gamma _ { i + 1 } } } \right) ^ { \frac { 1 } { \gamma } }$ i is an auxiliary parameter, where $g _ { 2 } ^ { \frac { \varepsilon _ { i } } { \gamma _ { i + 1 } } }$ can be obtained from $r e s _ { i + 1 }$ . Once obtained, $g _ { 2 } ^ { \frac { \varepsilon _ { i } } { \gamma _ { i + 1 } } }$ is deleted from $r e s _ { i + 1 }$ by $R N _ { i } .$ It can be proven that $\left( g _ { 2 } ^ { \frac { \varepsilon _ { i } } { \gamma _ { i + 1 } } } \right) ^ { \gamma _ { i } }$ is derived from the blinded public key $g _ { ? } ^ { \varepsilon _ { i } \gamma _ { i } }$ of $\dot { R } N _ { i }$

$R N _ { i }$ queries the relay list based on the identity information of $R N _ { i - 1 }$ to obtain the epoch public key of $R N _ { i - 1 }$ , and <sup>ε</sup>i−1 ε then generates $g _ { 2 } ^ { \stackrel { . . . } { \gamma _ { i } } } . g _ { 2 } ^ { \stackrel { . . . } { \gamma _ { i } } }$ is transmitted only between $R N _ { i - 1 }$ and $R N _ { i }$ . Its role is to assist $R N _ { i - 1 }$ is generating the auxiliary parameter $\left( g _ { 2 } ^ { \frac { \varepsilon _ { i - 1 } } { \gamma _ { i } } } \right) ^ { \gamma _ { i - 1 } }$

## - CN Verification.

5) In the original PAC protocol, this step primarily involves obtaining the group to which the next hop by relay belongs to verify circuit randomness. Now, the CN verifies the randomness of the circuit construction through a shared value. If the CN needs to confirm whether $R N _ { i }$ has selected $R N _ { i + 1 }$ based on the $g _ { 2 } ^ { \varepsilon _ { i } \varepsilon _ { i + 1 } }$ <sup>1</sup>, it performs the following check.

• Verify whether $e \left( g _ { 2 } ^ { \frac { \varepsilon _ { i } \gamma _ { i } } { \gamma _ { i + 1 } } } , r p k _ { i + 1 } ^ { \prime } [ 0 ] \right) \overset { ? } { = } e ( g _ { 2 } , r p k _ { i } ^ { \prime } [ 1 ] )$ . If true, prove that $g _ { 2 } ^ { \gamma _ { i + 1 } }$ derived from $r p k _ { i } [ 1 ]$ and continue.

• Verify whether $e \left( g _ { 2 } ^ { \frac { \varepsilon _ { i + 1 } \gamma _ { i + 1 } } { \gamma _ { i } } } , r p k _ { i } ^ { \prime } [ 0 ] \right) \overset { ? } { = } e ( g _ { 2 } , r p k _ { i + 1 } ^ { \prime } [ 1 ] )$ . If <sup>ε</sup>i+1<sup>γ</sup>i+1 true, prove that $g _ { 2 } ^ { \gamma _ { i } }$ derived from the epoch public key $r p k _ { i + 1 } [ 1 ]$ of $R N _ { i + 1 } ,$ and continue.

• Verify whether $e \left( g _ { 2 } ^ { \frac { \varepsilon _ { i } \gamma _ { i } } { \gamma _ { i + 1 } } } , g _ { 2 } ^ { \frac { \varepsilon _ { i + 1 } \gamma _ { i + 1 } } { \gamma _ { i } } } \right) \stackrel { ? } { = } e ( g _ { 2 } , g _ { 2 } ^ { \varepsilon _ { i } \varepsilon _ { i + 1 } } )$ and $| F _ { r s k _ { i } } ( \tau _ { i } )$ mod $\theta - H ( g _ { 2 } ^ { \overline { { { \varepsilon _ { i } } } } \varepsilon _ { i + 1 } } )$ mod $\theta | \leq \lfloor \varpi \rfloor .$ If true, prove that $R N _ { i + 1 }$ was randomly selected by $R N _ { i } ,$ and continue.

Probability. In step 8) of the CN initial phase, there is a certain probability that RN may fail to match $s _ { j }$ from the relay list, which is an undesirable outcome. A matching failure indicates that the CN must initiate a request to rebuild the circuit. We aim to address this issue by maximizing the probability of matching success. The probability of a successful match in one attempt is given by $\begin{array} { r } { \stackrel { \cdot } { p r o b _ { 1 } } = \dot { 1 } - \left( 1 - \frac { 2 \lfloor \varpi \rfloor + 1 } { \theta } \right) ^ { N } } \end{array}$ where N represents the number of RNs in the relay list. Given that N is fixed, $p r o b _ { 1 }$ can be increased by increasing the ratio $\frac { 2 \lfloor \varpi \rfloor + 1 } { \theta }$ , where θ should still be kept significantly larger than \$. Additionally, another approach to enhance the matching probability is to allow RN to perform multiple matching attempts. If we assume m matching attempts, the success probability becomes $p r o b _ { 2 } = 1 - ( 1 - p r o b _ { 1 } ) ^ { m }$ . At this point, $p r o b _ { 1 }$ is fixed, and increasing prob can be achieved by raising m. However, θ, \$, and m are not arbitrarily set. We can optimize both strategies according to the network scale.

Discussion. Achieving relay anonymity in a small-scale anonymous network is a challenging task. Compared to largescale anonymous networks, we have expanded the set of relays to hide among to include all relays, but if the total number of relays remains small, the above approach still cannot achieve strong relay anonymity. Moreover, the current approach has two weaknesses: first, each RN needs to compute an additional relay list, which increases the system’s computational overhead; and second, there is a risk of matching failure when selecting relays, which raises the probability of circuit construction failure. A better approach would be to add fake RNs to the system. This method provides strong relay anonymity regardless of the network’s scale and is one of the directions for our future work.

## V. THEORETICAL ANALYSIS AND PERFORMANCE EVALUATION

## A. Theoretical Analysis

Resilience. To strengthen the system’s resilience against adversarial attacks, trust is distributed among many semihonest GNs. In the event of an attack on a GN, only the relays under that GN’s management will be afected. The distribution scheme of Avatar leverages the VRF, meaning that any adversary A attempting to disrupt the scheme must compromise the uniqueness, provability, or pseudorandomness properties of the VRF.

Theorem 1 (Resilience): If the uniqueness, pseudorandomness, and provability of the VRF hold, then Avatar satisfies resilience.

Sketched Proof. A function family ${ \cal F } . ( \cdot ) \ : \ : : \ : \{ 0 , 1 \} ^ { a ( \lambda ) } \ : \ :  \ :$ $\{ 0 , 1 \} ^ { b ( \lambda ) }$ is a family of VRFs, where a(λ) and $b ( \lambda )$ are computable in polynomial time. It must satisfy the following three properties. The uniqueness property requires that no value (pk<sub>,</sub> m<sub>,</sub> $F _ { s k } ^ { \prime } ( m ) , \bar { F } _ { s k } ^ { \prime \prime } ( m ) , \pi _ { \mathsf { V R F } } ^ { \prime } , \bar { \pi } _ { \mathsf { V R F } } ^ { \prime \prime } )$ can satisfy Verify<sub>VRF</sub> (pk<sub>,</sub> m<sub>,</sub> F<sup>0</sup> (m)<sub>,</sub> π<sup>0</sup> ) $\mathsf { V e r i f y } _ { \mathsf { V R F } } ( p k , m , F _ { s k } ^ { \prime \prime } ( m ) , \bar { \pi } _ { \mathsf { V R F } } ^ { \prime \prime } )$ when $F _ { s k } ^ { \prime } ( m ) \quad \mp \quad F _ { s k } ^ { \prime \prime } ( m )$ The provability property requires that if $( F _ { s k } ( m ) , \pi _ { \mathsf { V R F } } ) \ =$ Prove<sub>VRF</sub>(sk m),then $\begin{array} { r l r } { \mathsf { V e r i f y } _ { \mathsf { V R F } } ( p k , m , F _ { s k } ( m ) , \pi \mathsf { v R F } ) } & { { } = } & { 1 } \end{array}$ The pseudorandomness property requires that for any probabilistic polynomial time algorithm $\begin{array} { r l r } { \mathcal { A } } & { { } = } & { ( A _ { 1 } , A _ { 2 } ) . } \end{array}$ , that does not query its oracle on $( p k , s k ) \gets \mathsf { K e y G e n } _ { \mathsf { V R F } } ( \mathsf { i } ^ { \lambda } ) ;$ (m st) ← A<sup>ProveVRF(·)</sup>(pk); m,Pr b = b<sup>0</sup> y = F (m); y ← {0 1}<sup>b(λ)</sup> ≤ <sup>1</sup><sub>2</sub> + negl(λ). b ← {0 1}; b<sup>0</sup> ← A<sup>ProveVRF(·)</sup>(y<sub>b,</sub> st)

The safety of the $\scriptstyle \mathrm { V R F }$ [18] we use is based on the Computational Difie-Hellman (CDH) problem in the random oracle model. If an adversary can solve the CDH problem, the security of the VRF would be compromised, thereby undermining the resilience of our system. However, given that the probability of an adversary solving the CDH problem is negligible, the probability of compromising the system’s resilience is also negligible.

Relay Anonymity. The most notable diference between the PAC and other anonymous routing protocols is the protection of relay privacy. In the PAC, relay anonymity is achieved as the client verifies the identity of the RN and the validity of its blinded epoch public key through the use of anonymous credentials. When the validity of the blinded epoch public key is verified, the output of $\mathsf { P r o v e } _ { \mathsf { A V R F } } ( \cdot )$ being anonymously verified is also guaranteed. These credentials are unforgeable, unlinkable, and anonymous. Therefore, the security of relay anonymity depends on the security of the anonymous credentials. If an adversary A can compromise the security of the anonymous credentials, it would also compromise the relay anonymity properties. The security analysis of relay anonymity is equivalent to analyzing the security of anonymous credentials. Next, we present Theorem 2 and provide a sketched proof for it.

Theorem $\begin{array} { r l r l } { { 2 } } & { { } } & { ( R e l a y } \end{array}$ anonymity.): If anonymous credentials satisfy unforgeability, unlinkability, and anonymity, then Avatar achieves relay anonymity.

Sketched Proof. The anonymous credentials are constructed based on weak BB signatures, which are unforgeable against weak chosen message attacks under the q-SDH assumption. Here, we assume the existence of a challenger $\mathcal { C }$ and an adversary A. A sends C a list of n messages $\{ m _ { 1 } , \cdot \cdot \cdot , m _ { n } \} \quad \in \quad \{ 0 , 1 \} ^ { * }$ Then, C runs $\mathsf { K e y G e n } ( 1 ^ { \lambda } )$ to generate $\textbf { a } \ s k$ and a pk. Next, C generates credentals $c r e d _ { i } = ( \psi _ { i }  g _ { 1 } ^ { 1 / ( s k + m _ { i } ) } , m _ { i } )$ for $i = 1 , \ldots , n . \ { \mathcal { C } }$ then gives A the $p k$ and n credentials $\{ c r e d _ { 1 } , \cdot \cdot \cdot , c r e d _ { n } \}$ . If an adversary breaks the unforgeability of the weak BB signature under the q-SDH assumption, it wins the game by outputting a pair $( m , \psi )$ such that m $\notin \{ m _ { 1 } , \ldots , m _ { n } \}$ and $e ( \psi , p k \cdot g _ { 2 } ^ { m } ) = e ( g _ { 1 } , g _ { 2 } )$ According to the security analysis by Boneh and Boyen [15], it can be established that the probability of an adversary successfully forging a BB signature under a weak chosen message attack is negligible. Therefore, the likelihood of the adversary attempting to forge a credential under a weak chosen message attack can also be considered negligible.

The anonymous credentials generated by RN are based on a more eficient way of proving knowledge of a weak Boneh-Boyen signature, as proposed by Camenisch et al. [16]. Consequently, our anonymity and unlinkability are based on Camenisch’s original properties. We then modified part of the verification process to achieve our goal, but this did not alter its inherent properties. Here, we will briefly analyze the modified part. The information signed to the anonymous credentials is divided into two distinct categories: the hidden information, denoted $i d _ { R }$ and $\epsilon ,$ and the public information, e. The witness $i d _ { R }$ is verified satisfying the statement $\bar { \psi } = \psi ^ { ' - i d _ { R } } g _ { 1 } ^ { \gamma }$ by the underlying zero-knowledge proof, which is consistent with Camenisch’s approach. Then, $e ( \bar { \psi } , r p k ^ { \prime } [ 0 ] ) = e ( \psi ^ { \prime } , r p k ^ { \prime } [ 0 ] ^ { e }$ $r p k ^ { \prime } [ 1 ] \cdot p k _ { G } ^ { \prime } )$ verifies that  is the same as the epoch private key in $r p k ^ { \prime }$ , while e is verified directly by the plaintext, where $p k _ { G } ^ { \prime }$ is proven using a zero-knowledge proof. Here we show the details of the bilinear pairing computation below to demonstrate that we have not changed its intrinsic properties.

$$
\begin{array}{l} e (\bar {\psi}, r p k ^ {\prime} [ 0 ]) \\ = e \left(\left(g _ {1} ^ {\frac {1}{s k _ {G} + \varepsilon + i d _ {R} + e}}\right) ^ {- i d _ {R} \gamma} \cdot g _ {1} ^ {\gamma}, g _ {2} ^ {\gamma}\right) \\ = e \left(g _ {1} ^ {\frac {\gamma (s k _ {G} + \varepsilon + e)}{s k _ {G} + \varepsilon + i d _ {R} + e}}, g _ {2} ^ {\gamma}\right) \\ = e (g _ {1}, g _ {2}) ^ {\frac {\gamma^ {2} (s k _ {G} + \varepsilon + e)}{s k _ {G} + \varepsilon + i d _ {R} + e}} \\ e (\psi^ {\prime}, r p k ^ {\prime} [ 0 ] ^ {e} \cdot r p k ^ {\prime} [ 1 ] \cdot p k _ {G} ^ {\prime}) \\ = e \left(g _ {1} ^ {\frac {\gamma}{s k _ {G} + \varepsilon + i d _ {R} + e}}, (g _ {2} ^ {\gamma}) ^ {e} \cdot g _ {2} ^ {\varepsilon \gamma} \cdot g _ {2} ^ {s k _ {G} \gamma}\right) \\ = e \left(g _ {1} ^ {\frac {\gamma}{s k _ {G} + \varepsilon + i d _ {R} + e}}, g _ {2} ^ {\gamma (s k _ {G} + \varepsilon + e)}\right) \\ = e (g _ {1}, g _ {2}) ^ {\frac {\gamma^ {2} (s k _ {G} + \varepsilon + e)}{s k _ {G} + \varepsilon + i d _ {R} + e}} \end{array}
$$

Others. The properties of randomness, scalability, and forward security are satisfied by PAC. During circuit construction, the AVRF guarantees that each RN must randomly determine the anonymous group of the next hop based on its output. It is important to note that the RN itself is unable to determine the input to the AVRF. The input to the AVRF is determined by the previous node of the currently running AVRF relay. Furthermore, the epoch private key employed in the $\mathsf { P r o v e } _ { \mathsf { A V R F } } ( \cdot )$ is not determined by the RNs themselves. Instead, this epoch private key is securely distributed to the RN by the GN and is included in the signature of the credential issued to the RNs. In the event that an RN employs a forged private key to engage in the AVRF’s output computation, the CN’s verification process will inevitably fail. The protocol’s design incorporates the use of key pairs that are generated temporarily for the purpose of key exchange, thereby ensuring the forward security of the circuit construction process. Furthermore, in our design, the message can establish an anonymous circuit with just one round trip, thereby significantly reducing the circuit construction delay and enhancing its scalability. The specific time consumption for constructing the circuit will be presented in the experimental section.

## B. Performance Evaluation

Experiment Settings. To evaluate the efectiveness of the proposed scheme, we conducted a series of experimental tests. The results serve as a reference for assessing the feasibility of deploying the scheme in large-scale real-world environments. We established both simulated and real-world network environments. In the simulated environment, data transmission time was estimated based on actual bandwidth and network latency using the transmitted bit volume. In the real-world environment, the system was deployed on AWS EC2 instances distributed across Seoul, Tokyo, Singapore, Sydney, California, Frankfurt, the UAE, and Cape Town. All experiment results represent the average over multiple runs. Although the real-world measurements may be influenced by transient network congestion, packet loss, or routing variability, they provide valuable insights into the system’s deployment performance under realistic network conditions. Regarding the experimental devices, we primarily used AWS EC2 t2.micro (1 vCPU,1GiB) instances. However, since AWS does not provide t2.micro instances in the UAE and Cape Town regions, we used t3.micro instead, whose performance is comparable (difering only by one vCPU). To further examine algorithmic performance under varying computational capacities, additional experiments were performed on a high-performance workstation (Dell T3360, Intel Core i7-13700K, 3.4 GHz, 16 cores). Since the primary goal of this study is to achieve relay anonymity in anonymous circuits, the experiments focused on circuit construction and computational performance. Both the proposed scheme and the comparative schemes were implemented in Python, leveraging cryptographic libraries including MCL [22], [23], cryptography, pycryptodome, sphinxmix, and PyNaCl [24]. Data storage and management are handled by MySQL, and the entire system runs on Ubuntu Server 22.04 LTS.

Experimental Description and Results. The proposed algorithms were evaluated on t2.micro instances and the workstation T3360. The measurements focused solely on algorithm computation time, excluding network transmission and database I/O latency. The results are shown in Fig. 6(a). Although device performance has some impact on runtime, the algorithm consistently completed execution within 20 milliseconds across both high-performance and low-performance environments. Such performance is practically achievable on most real-world devices.

Since this study emphasized relay anonymity in anonymous circuits, we further evaluated the impact of the anonymity mechanism on circuit construction time. Specifically, circuits with 3 to 6 hops were constructed and measured. In the simulated network environment (see Fig. 6(b)–(c)), results indicate that network latency has a more significant efect on circuit construction time than bandwidth, with higher latency causing a more pronounced increase in construction time. To further demonstrate the performance of the proposed anonymous circuit construction scheme, it was compared with the Tor network and its optimized variant, Walking Onions. As shown in Fig. 6(d)–(g), under different simulated network conditions, the proposed Avatar exhibits superior construction eficiency. Tor’s construction time grows rapidly with an increasing number of hops, whereas Avatar and Walking Onions scale more gracefully. Although Avatar’s construction time is slightly higher than Walking Onions, this additional overhead is justified by the protocol’s support for relay anonymity. Real-world experiments were conducted using AWS EC2 instances. As shown in Fig. 6(h), circuit construction times are higher in realworld networks than in simulations, primarily because each hop spans diferent geographic regions, resulting in higher latency. Nevertheless, the conclusion from the simulated experiment remains valid. Avatar achieves substantial eficiency improvements over the standard Tor protocol and maintains comparable performance to Walking Onions. These results indicate that the proposed circuit construction protocol provides relay anonymity while maintaining high eficiency and scalability.

The previous evaluation focused on anonymous communication based on circuits. We next compared Avatar with other decentralized anonymous networks, including Loopix and I2P, which generally do not require circuit construction. Experiments were conducted on AWS EC2 instances, measuring the time required for clients to transmit identical data volumes to a server through each system. To ensure fairness, the data paths were kept as consistent as possible. Loopix is an anonymous network based on a mix network. In the experiments, the client splits data into units of the same size as in Avatar. Each unit is encrypted and transmitted along separate paths, with an average per-hop delay of 1 ms. In the experiments, trafic obfuscation was disabled. Enabling it would further increase Loopix’s transmission latency. I2P is an anonymous network based on dual tunnels. Both inbound and outbound tunnels were configured with two hops, each data unit carrying approximately 1 KB of payload. End-to-end encrypted transmission time was measured. As shown in Fig. 6(i), transmission times for Loopix and I2P increase significantly with data volume, exceeding those of Avatar. In Loopix, path selection and group operations are performed independently for each data unit, which results in a rapid increase in time cost when the data volume exceeds 1 MB. I2P introduces additional latency due to its bidirectional tunnel structure and the increased number of relay nodes. In contrast, Avatar constructs a bidirectional anonymous circuit and performs group operations only during setup, resulting in lower overall transmission latency.

![](images/6b0c3da5c0ea1453b8fac94f1e219e8b3bbf7a4b6fc9bb0f77f75a7a1693419a.jpg)  
(a) Avatar Algorithm Execution Time

![](images/341796ea84969507c53f25f614262dee5dc72ad8425b72d4a160de1b5e1b9f10.jpg)  
(b) Avatar Latency: 100ms

![](images/4d01d7936c79279c753b34d43c53171afcebc1fc2a65956ce53b1133dc0b4839.jpg)  
(c) Avatar Bandwidth: 100Mbps

![](images/fe8775f1d5ad012563ab67be1015c32d26b467220664f8747a17ca7dc8256f44.jpg)  
(d) Bandwidth: 10Mbps, Latency: 50ms

![](images/f36ad8f7acbc0378ed5790dc089f6f05d5e1c46d36ecda66babe904dc1a94572.jpg)  
(e) Bandwidth: 10Mbps, Latency: 100ms

![](images/875e336a875a7f84e463b306b3504745e3dde92f3d915ac725f3fea4a55e4bfa.jpg)  
(f) Bandwidth: 100Mbps, Latency: 50ms

![](images/fc8ec8f4af3f9dac35f561397e110fcb06d851c2d8f1ca6e47c6d65e8ae7aa3b.jpg)  
(g) Bandwidth: 100Mbps, Latency: 100ms

![](images/b10ebc1fb652adaca3e75d59dc3284c8f3f9cf77f5543f53cd774457edd2a151.jpg)  
(h) Real Network Environment

![](images/ca62c2187d856e63eb273c529837832b6277429313387d7bbb0e9eab1155f280.jpg)  
(i) Real Network Environment  
Fig. 6. Avatar evaluation and comparative experiments. Figures (b)–(g) were tested on the t2.micro instance. Figures (h) and (i) were mainly deployed on t2.micro and t3.micro instances.

TABLE III  
GENERATION TIME AND STORAGE OVERHEAD OF THE RELAY LIST

<table><tr><td>Number</td><td>50</td><td>100</td><td>200</td><td>400</td><td>800</td><td>1600</td></tr><tr><td>T3360 (ms)</td><td>4</td><td>8</td><td>15</td><td>30</td><td>60</td><td>122</td></tr><tr><td>t2.micro (ms)</td><td>18</td><td>36</td><td>72</td><td>144</td><td>289</td><td>578</td></tr><tr><td>Storage (KB)</td><td>20.4</td><td>40.8</td><td>81.7</td><td>163.6</td><td>327.2</td><td>327.2</td></tr></table>

Finally, we present in Table III the generation time of relay lists with diferent numbers of relays discussed in section IV-D, as well as the storage space occupied by the epoch public keys and shared values. As shown in the table, when the number of relays is relatively small, both the generation time and the storage overhead of the relay list remain at a very low level. It should be noted that the relay list can be generated locally by the relay nodes without being transmitted over the network. Therefore, its impact on the time cost of anonymous circuit construction is negligible. The main system overhead lies in the additional storage space, which is acceptable for most devices. For network operators, the choice of how to operate the anonymous network should be made based on practical requirements, such as the acceptable level of relay anonymity and the storage capacity of the devices. In future work, we will focus on exploring more eficient approaches to achieving relay anonymity in order to further enhance the anonymity and scalability of the system.

## VI. RELATED WORK

Tor. Anonymous networks are typically implemented in two ways. The first is message forwarding, where messages pass through multiple relays before reaching the recipient, as in Mix networks [25]. The second is logical broadcasting, where messages are broadcast, exemplified by DC networks [26]. Most modern anonymous network designs build on these two approaches. For example, Tor [2], I2P [12], Loopix [10], and Nym [11] follow the mix network model, while Herbivore and Dissent are based on the DC network model. Among them, Tor is one of the largest anonymous networks in the world, comprising thousands of relay nodes and serving millions of users. Numerous scholars have researched ways to enhance the Tor network. Kim et al. [8] design SGX-Tor to efectively enhance the security and privacy of Tor by utilizing Intel SGX [27], [28]. Greubel et al. [9] used TEE-equipped devices to achieve trusted bandwidth measurements. Komlo et al. [4] proposed a Single-Pass Walking Onions protocol, which utilizes a VRF [29] algorithm to randomly select relays for building a circuit. Meanwhile, the client exchanges a single message to negotiate multiple shared keys, reducing circuit construction time. Mani and Goldberg [30] present ZXAD, a zero-knowledge system that detects high-volume abuse at Tor exits while fully preserving user privacy, with proven security and low overhead. Despite continuous improvements to Tor, attack strategies [31], [32], [33], [34] targeting Tor are also constantly evolving. Therefore, this paper aims to enhance the overall security of anonymous networks from the perspective of protecting relay node privacy.

Anonymous Credentials. Chaum and Evertse [35] introduced the concept of anonymous credentials based on RSA cryptography. In 2001, Camenisch and Lysyanskaya [36] proposed an anonymous credentials protocol based on strong RSA assumptions, including registration, issuance, and presentation phases. In 2014, Chase et al. [37] proposed a Keyed-Verification Anonymous Credentials (KVAC) that is constructed using an algebraic message authentication code (MAC). In 2019, Camenisch et al. [38] proposed another novel Keyed-Verification Anonymous Credentials (KVAC) that contains Boneh-Boyen signatures. Benhamouda et al. [13] introduced a novel concept of anonymous tokens, known as Anonymous Counting Tokens (ACT), which ensure that no user can redeem multiple tokens for the same message. Mir et al. [39] proposed a new Issuer-Hiding Multi-Authority Anonymous Credentials (IhMA) system designed for decentralized environments. Karantaidou et al. [40], leveraging BLS, proposed a blind multi-signature scheme for the decentralized issuance of anonymous tokens. Then, Yu et al. [21] designed an anti-tracking cellular authentication scheme using Camenisch’s KVAC scheme. The mobile device presents anonymous credentials to the service’s website to confirm identity. However, instead of incorporating the expiration date of the anonymous credentials into the validation of the anonymous credentials, Yu performs a separate check of the plaintext expiration date. An adversary can use a correct plaintext date and an expired anonymous credential to pass the verification of the service network. In contrast to [21], we verify the validity period of the credential and employ anonymous credentials to achieve blind public key authentication.

## VII. CONCLUSION

We observe from the literature that existing anonymous network solutions cannot provide anonymity for relay nodes. Following the Walking Onions solution, we still use the VRF to elect the relay nodes, but we use an anonymous VRF and anonymity credentials to construct a new anonymous network solution named Avatar, which can preserve the relays privacy during circuit construction. Avatar can also distribute trust across more entities to improve the network’s resilience against adversaries. Next, we provided a prototype Avatar system written in Python, evaluated its performance, and compared it with the circuit construction protocol in the original Tor network. The results show that Avatar maintains high execution eficiency, even with the addition of a new property. The circuit construction protocol of Avatar ofers strong protection for relay privacy while achieving a well-balanced trade-of between circuit randomness and other properties like bandwidth. Notably, it not only maintains the same security guarantees as the existing onion routing protocol but also improves construction eficiency.

The level of relay anonymity in an anonymous circuit in Avatar is jointly determined by the number of hops in the circuit and the number of group members within each group. Indeed, Avatar has certain limitations: as described in IV-C, its anonymity performance is suboptimal in small, self-organized anonymous networks, and the supplementary scheme specifically designed for small-scale anonymous networks IV-D results in additional consumption of computational resources.

## REFERENCES

[1] J. Ren and J. Wu, “Survey on anonymous communications in computer networks,” Comput. Commun., vol. 33, no. 4, pp. 420–431, Mar. 2010.

[2] R. Dingledine, N. Mathewson, and P. F. Syverson, “Tor: The second-generation onion router,” in Proc. 13th USENIX Secur., 2004, pp. 303–320.

[3] Z. Ling, J. Luo, K. Wu, W. Yu, and X. Fu, “TorWard: Discovery, blocking, and traceback of malicious trafic over tor,” IEEE Trans. Inf. Forensics Security, vol. 10, no. 12, pp. 2515–2530, Dec. 2015.

[4] C. Komlo, N. Mathewson, and I. Goldberg, “Walking onions: Scaling anonymity networks while protecting users,” in Proc. USENIX, 2020, pp. 1003–1020.

[5] Tor Project. (2025). Bridges. [Online]. Available: https://tbmanual.torproject.org/bridges/

[6] Tor Project. (2025). Relay Search. [Online]. Available: https:// metrics.torproject.org/rs.html#simple

[7] Tor Project. (2025). Relay Flexible. [Online]. Available: https:// support.torproject.org/relay-operators/relay-flexible/

[8] S. Kim, J. Han, J. Ha, T. Kim, and D. Han, “Enhancing security and privacy of tor’s ecosystem by using trusted execution environments,” in Proc. USENIX, 2017, pp. 145–161.

[9] A. Greubel, A. Dmitrienko, and S. Kounev, “Smartor: Smarter tor with smart contracts: Improving resilience of topology distribution in the tor network,” in Proc. ACSAC ACM, 2018, pp. 677–691.

[10] A. M. Piotrowska, J. Hayes, T. Elahi, S. Meiser, and G. Danezis, “The loopix anonymity system,” in Proc. USENIX Secur., 2017, pp. 1199–1216.

[11] C. Diaz, H. Halpin, and A. Kiayias, “The nym network: The next generation of privacy infrastructure,” Nym Technol. SA, Switzerland, White Paper, 2021. [Online]. Available: https://nym.com/nym-whitepaper.pdf

[12] B. Zantout et al., “I2P data communication system,” in Proc. ICN, 2011, pp. 401–409.

[13] F. Benhamouda, M. Raykova, and K. Seth, “Anonymous counting tokens,” in Proc. ASIACRYPT, vol. 14439. Cham, Switzerland: Springer, 2023, pp. 245–278.

[14] D. Boneh, B. Lynn, and H. Shacham, “Short signatures from the Weil pairing,” in Proc. ASIACRYPT, vol. 2248. Cham, Switzerland: Springer, 2001, pp. 514–532.

[15] D. Boneh and X. Boyen, “Short signatures without random oracles,” in Proc. EUROCRYPT, vol. 3027. Cham, Switzerland: Springer, 2004, pp. 56–73.

[16] J. Camenisch, M. Drijvers, and J. Hajny, “Scalable revocation scheme for anonymous credentials based on n-times unlinkable proofs,” in Proc. ACM Workshop Privacy Electron. Soc., Vienna, Austria, 2016, pp. 123–133.

[17] S. Micali, M. O. Rabin, and S. P. Vadhan, “Verifiable random functions,” in Proc. FOCS, Jul. 1999, pp. 120–130.

[18] B. David, P. Gazi, A. Kiayias, and A. Russell, “Ouroboros praos: An adaptively-secure, semi-synchronous proof-of-stake blockchain,” in Proc. EUROCRYPT, vol. 10821. Cham, Switzerland: Springer, 2018, pp. 66–98.

[19] C. Ganesh, C. Orlandi, and D. Tschudi, “Proof-of-stake protocols for privacy-aware blockchains,” in Proc. EUROCRYPT, vol. 11476. Cham, Switzerland: Springer, 2019, pp. 690–719.

[20] E. Rescorla, “The transport layer security (TLS) protocol version 1.3,” in Proc. RFC, vol. 8446, 2018, pp. 1–160.

[21] H. Yu et al., “AAKA: An anti-tracking cellular authentication scheme leveraging anonymous credentials,” in Proc. Netw. Distrib. Syst. Secur. Symp., 2024.

[22] PYMCL. GitHub Repository. Accessed: Sep. 15, 2025. [Online]. Available: https://github.com/Jemtaly/pymcl

[23] MCL. GitHub Repository. Accessed: Sep. 15, 2025. [Online]. Available: https://github.com/herumi/mcl

[24] Python Software Foundation. (2025). Python Packaging Survey. [Online]. Available: https://pypi.org/search/?q=

[25] D. L. Chaum, “Untraceable electronic mail, return addresses, and digital pseudonyms,” Commun. ACM, vol. 24, no. 2, pp. 84–88, Feb. 1981.

[26] D. Chaum, “The dining cryptographers problem: Unconditional sender and recipient untraceability,” J. Cryptol., vol. 1, no. 1, pp. 65–75, Jan. 1988.

[27] P. Jain et al., “Opensgx: An open platform for SGX research,” in Proc. NDSS Internet Soc., 2016.

[28] I. Anati, S. Gueron, S. Johnson, and V. Scarlata, “Innovative technology for cpu based attestation and sealing,” in Proc. 2nd Int. Workshop Hardw. Architectural Support Secur. Privacy, vol. 13, no. 7, New York, NY, USA, 2013.

[29] S. Goldberg, L. Reyzin, D. Papadopoulos, and J. Vcelak, “Verifiable´ random functions (VRFS),” in Proc. RFC, vol. 9381, 2023, pp. 1–47.

[30] A. Mani and I. Goldberg, “ZXAD: high-volume attack mitigation for tor,” in Proc. 20th Workshop Workshop Privacy Electron. Soc., Nov. 2021, pp. 1–16.

[31] S. E. Oh et al., “Deepcofea: Improved flow correlation attacks on tor via metric learning and amplification,” in Proc. IEEE SP, May 2022, pp. 1915–1932.

[32] A. Panchenko et al., “Website fingerprinting at internet scale,” in Proc. NDSS, 2016.

[33] J. Juen, A. Johnson, A. Das, N. Borisov, and M. Caesar, “Defending tor from network adversaries: A case study of network path prediction,” Proc. Privacy Enhancing Technol., vol. 2015, no. 2, pp. 171–187, Jun. 2015.

[34] I. Karunanayake, N. Ahmed, R. A. Malaney, R. Islam, and S. K. Jha, “Deanonymisation attacks on tor: A survey,” IEEE Commun. Surv. Tut., vol. 23, no. 4, pp. 2324–2350, 4th Quart., 2021.

[35] D. Chaum and J. Evertse, “A secure and privacy-protecting protocol for transmitting personal information between organizations,” in Proc. CRYPTO, vol. 263. Cham, Switzerland: Springer, 1986, pp. 118–167.

[36] J. Camenisch and A. Lysyanskaya, “A signature scheme with eficient protocols,” in Proc. 3rd Int. Conf. Secur. Commun. Netw., vol. 2576. Amalfi, Italy. Cham, Switzerland: Springer, 2002, pp. 268–289.

[37] M. Chase, S. Meiklejohn, and G. Zaverucha, “Algebraic MACs and keyed-verification anonymous credentials,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2014, pp. 1205–1216.

[38] J. Camenisch, M. Drijvers, P. Dzurenda, and J. Hajny, “Fast keyedverification anonymous credentials on standard smart cards,” in Proc. IFIP SEC. Cham, Switzerland: Springer, 2019, pp. 286–298.

[39] O. Mir, B. Bauer, S. Grify, A. Lysyanskaya, and D. Slamanig, “Aggregate signatures with versatile randomization and issuer-hiding multi-authority anonymous credentials,” in Proc. ACM SIGSAC Conf. Comput. Commun. Secur., Nov. 2023, pp. 30–44.

[40] I. Karantaidou, O. Renawi, F. Baldimtsi, N. Kamarinakis, J. Katz, and J. Loss, “Blind multisignatures for anonymous tokens with decentralized issuance,” in Proc. CCS, 2024, pp. 1508–1522.

![](images/9820d34eaa46a22ab0937207a952d6ea719512e3542f26e6e3a86ad37c316bcb.jpg)  
Hao Zhu received the B.E. degree in software engineering from Shandong University of Technology, China, in 2019. He is currently pursuing the Ph.D. degree with the School of Cyber Science and Technology and the National Graduate School for Elite Engineers, Shandong University, Qingdao, China. He has published in international journals, including IEEE TRANSACTIONS ON CONSUMER ELECTRONICS. His research interests include applied cryptography and privacy protection.

![](images/09ede1d728f6506eb5f5b234f84fcae8d8190f871bc47ce0aa1ae88dc754cf4b.jpg)

Mei Wang received the Ph.D. degree in cyberspace security from Wuhan University, Wuhan, China, in 2022. During her Doctoral Program, she was a Research Assistant with Lancaster University, Lancaster, U.K. She is currently a Faculty Member with Shandong University, Qingdao, China. She has published research papers in international journals and conferences, such as IEEE/ACM TRANSAC-TIONS ON NETWORKING, IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS, Future Generation Computer Systems, and the ACM

CCS. Her research interests include applied cryptography, cloud computing, mobile computing, and privacy protection.

![](images/3e319156ec71e443ea9412e9db9173ae488afcaa57d7e663019757b1018c8765.jpg)

Zengpeng Li is currently an Associate Professor with Shandong University (SDU), China, supported by SDU Young Scholars’ Future Plan. Before joining SDU, he was a Post-Doctoral Research Fellow with Singapore University of Technology and Design and Lancaster University. His works appear in ACM CCS, ACSAC, NDSS, IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING and IEEE TRANSACTIONS ON SERVICES COMPUTING. His primary research interests include cryptographic protocols and secure distributed computing. He

served as a TPC Member for PoPETs, MSN, and KSEM. He served as the Program Chair for CIMSS2025 and CIMSS2023.

![](images/47c7a12cb4f654504d7acd19a12d978ccb4e29608a7c14d37c23fd4122706cb1.jpg)

Jing Chen (Senior Member, IEEE) received the Ph.D. degree in computer science from the Huazhong University of Science and Technology, Wuhan. He has been a Full Professor with Wuhan University since 2015. He has published more than 100 research papers in many international journals and conferences, such as IEEE TRANSACTIONS ON DEPENDABLE AND SECURE COMPUTING, IEEE TRANSACTIONS ON INFORMATION FOREN-SICS AND SECURITY, IEEE TRANSACTIONS ON MOBILE COMPUTING, IEEE TRANSACTIONS ON

COMPUTERS, IEEE TRANSACTIONS ON PARALLEL AND DISTRIBUTED SYSTEMS, USENIX Security, CCS, and INFOCOM. His research interests include computer science, network security, and cloud security.
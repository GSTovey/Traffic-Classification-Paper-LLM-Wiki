USENIX

THE ADVANCED COMPUTING SYSTEMS ASSOCIATION

# Remise: Authorized Anonymous Communication Systems

Rohan Ravi, Paritosh Shukla, and Adithya Vadapalli, IIT Kanpur https://www.usenix.org/conference/usenixsecurity26/presentation/ravi-rohan

# This paper is included in the Proceedings of the 35th USENIX Security Symposium.

August 12–14, 2026 • Baltimore, MD, USA

ISBN 978-1-939133-58-8

Open access to the Proceedings of the 35th USENIX Security Symposium is sponsored by

AgleU

King Abdullah University of

Science and Technology

# Remise: Authorized Anonymous Communication Systems

Rohan Ravi IIT Kanpur rohanra@cse.iitk.ac.in

Paritosh Shukla IIT Kanpur paritoshs24@cse.iitk.ac.in

Adithya Vadapalli IIT Kanpur avadapalli@cse.iitk.ac.in

## Abstract

We present Remise, a two-server authorized anonymous communication system built on Distributed Oblivious RAM (DORAM). Remise supports two modes of operation: (i) an anonymous bulletin board, where messages are publicly revealed at the end of each epoch without linking senders to messages, and (ii) anonymous commu nication channels, where messages remain secret-shared, and writers selectively grant and revoke read access to chosen readers. In both modes, the two servers execute read and write operations without learning which indices are accessed, which authorization tokens are used, or which relationships exist between writers and readers, assuming no collusion between the servers. A central con tribution of Remise is a lightweight and efficient accesscontrol mechanism. Authorization tokens are maintained in secret-shared form across the two servers, enabling oblivious verification and updates, while preventing leak age even under client–server collusion. Unlike prior DPF-based systems, Remise provides built-in auditing by having the semi-honest servers generate standard-basis vector shares internally, eliminating the need for server side DPF validity checks. We implement a prototype of Remise and evaluate it under realistic network conditions. Our experiments show an 80× improvement in online server time for request validity check when compared to PACL (IEEE S&P 2023) for large database size.

## 1 Introduction

The birth of the Internet was accompanied by great optimism. It was envisioned as a democratizing force—one that would enable free exchange of ideas, universal access to information, and participation independent of geography or social status. While this vision has been realized in many respects, the modern Internet also exposes users to pervasive surveillance, manipulation, and censorship [19, 23]. As a result, users increasingly feel compelled to self-censor and communicate with caution. In this context, anonymous communication systems offer a compelling response. By decoupling identities from messages, such systems protect users from surveillance and retaliation and play a critical role in preserving free expression. They are particularly valuable for journalists, whistleblowers, activists, and ordinary users operating in adversarial environments.

## 1.1 Anonymous Communication Systems

Sasy and Goldberg [27] classify anonymous communication systems into (i) sender-unlinkable broadcast systems (SUBS), (ii) sender-unlinkable messaging systems (SUMS), (iii) relationship-unobservable systems (RUS), and (iv) communication-unobservable systems (CUS). In this work, we focus on the first three categories. In a SUBS, users anonymously post messages to a public bulletin board that is typically secret-shared across multiple servers and reconstructed at fixed epochs. While the set of messages and the anonymity set of broadcasters are public, the link between a message and its author is hidden; cover traffic further prevents distinguishing real messages from dummy ones. Conceptually, SUBS resemble an anonymous microblogging platform. In a SUMS, receivers own mailboxes identified by secret mailbox IDs that are shared out of band with intended senders. Senders remain anonymous, only authorized senders can write to a mailbox, and receivers obtain only messages addressed to them, though receiver anonymity is not provided. This model is commonly used for confidential disclosures, such as journalist–source communication (e.g., SecureDrop [14]). RUS extend SUMS by additionally ensuring that even a global adversary cannot link senders to receivers.

Sender Anonymous Communication Channels: This work introduces a new type of RUS that has not been studied hitherto, namely, Sender Anonymous Communication

Channels. In this model, a set of senders posts messages on a secret message board shared by two parties. However, the parties never reconstruct the messages to post them to the public. Instead, writers give read access to readers of their choice. Furthermore, the writers can revoke the access whenever they wish to do so. We could also think about this as an anonymous Substack or blog. The subscribers (of the Substack or Blog) are the read ers who have been granted read access by the authors. The authors (the writers) are granted write access by the service provider (the Remise servers). The writers have “ownership” of that space in the sense that they can write messages of their choice in the space, allow only the people of their choice to read messages from that space, and can remove read access for any reader at any point.

## 1.2 Review of State-of-the-Art

Remise follows the lineage of Anonymous Communica tion Systems like Riposte, Express, Sabre, and Spectrum, which are based on the so-called Distributed Point Func tions (DPFs). We will not go into the details of DPFs, however, it suffices to regard a DPF as a functional, suc cinct representation of secret shares of a 1-hot vector. The servers use shares of a 1-hot vector produced by DPFs to perform read and write operations on a database with out revealing which element was accessed. Such systems typically need to perform two checks before allowing a write request to be executed: (i) the DPFs are valid, i.e., they will expand to the shares of a 1-hot vector (audit), and (ii) the user is allowed to access at the index at which they are attempting to do so (authorization).

Riposte: Corrigan-Gibbs, Boneh, and Mazières, presented Riposte [7], a sender-anonymous broadcasting system that works in the bulletin board model. In Riposte, the writers (or broadcasters) submit write requests, creating a DPF at a random location and sending it to the servers. The servers reconstruct and publish all the mes sages that were received during each epoch. A problem with users writing at random locations on the bulletin board is that a broadcaster could overwrite a message written by another broadcaster. To reduce the probability of such a write-collision to 5%, the size of the Riposte servers is 19.5 times the number of messages to be posted. Riposte runs an audit protocol to ascertain that the write requests submitted are well-formed DPFs. One major weakness of Riposte is that it uses $O ( { \sqrt { n } } )$ -sized DPFs, where n is the size of the database. This is because the structure of these DPFs make their auditing protocol effi cient.

Express: In Express [13], each receiver is assigned a mailbox together with a $\lambda = 1 2 8$ -bit mailbox ID by the servers. Receivers share this mailbox ID with intended senders, who write messages by generating DPFs tar geting the corresponding ID. Although senders generate DPFs over a domain of size $2 ^ { 1 2 8 }$ , the Express servers evaluate them only at registered mailbox IDs. Express improves upon Riposte by using logarithmic-sized DPFs together with SNIPs for auditing. However, auditing requires the servers to evaluate each submitted DPF at all registered mailbox IDs, incurring work linear in the number of mailboxes. As a result, Express is vulnerable to DoS attacks in which malicious clients submit malformed DPFs that force expensive evaluations before rejection. Moreover, Express is not secure against server–client collusion, since servers know all registered mailbox IDs and can thereby derive and leak write authorization for any mailbox.

Sabre: The work by Vadapalli, Storrier, and Henry, Sabre [31] extends the work by Express and prevents DoS attacks by presenting O(lgn) auditing. For authorization, Sabre uses a mailbox ID verification using pseudorandom functions. If a writer is authorized to write at the $\mathtt { i } ^ { * \mathrm { t h } }$ location, the writer should know $\mathrm { { P R F } ( k , i ^ { * } ) }$ while only the servers know the secret key, k. The writer submits the additive shares of PRF(k,i<sup>∗</sup>) along with the shares of $\dot { \mathrm { ~ \tt ~ 1 ~ } } ^ { * }$ to the Sabre servers. Then, the Sabre servers use secure multiparty computation(MPC) to compute PRF(k,i<sup>∗</sup>), and check for equality. However, the MPC computation requires the underlying cipher to have a low multiplicative depth. Like Express, Sabre is also not secure when a collusion between a server and a user occurs, as the servers know the authorization proof, PRF(k,i), for all index i, by virtue of knowing k.

Spectrum: Spectrum [22] is an anonymous broadcasting system introduced by Newman, Servan-Schreiber, and Devadas with a low number of broadcasters. Each broadcaster in Spectrum is allotted a “channel” where they are authorized to write. This prevents writecollisions. Spectrum presents a blind access control mechanism that allows the servers to perform auditing and authorization over the DPFs. In addition, Spectrum has a Blame-Game protocol that protects against malicious Spectrum servers from rejecting valid write requests. Unlike Express and Sabre, Spectrum is secure against server-writer collusion leading to leakage of authorization material under the discrete log hardness assumption.

PACL: Unlike prior work on anonymous communication, PACL [28] addresses access control for Function Secret Sharing, which can also be applied to DPFbased communication systems. It builds on the Spectrum method for blind access control and introduces more efficient techniques. In the basic setup, servers hold a vector of verification keys $\Lambda = \{ g ^ { \alpha _ { 1 } } , \ldots , g ^ { \alpha _ { n } } \}$ , where secret key ${ \alpha } _ { \mathrm { i } }$ authorizes access to index i (DPF generation at i). The DPF is used to locally select (multiplicative) secret shares of $g ^ { [ \alpha _ { \mathrm { i } } ] }$ ,enabling verification through additive shares of a proof $[ \Pi ] _ { k } \gets [ - { \bf { \alpha } } \mathbf { { \alpha } } _ { \mathrm { { i } } } ] _ { k }$ . The servers then check that $g ^ { [ \alpha _ { \mathrm { i } } ] _ { k } } \cdot g ^ { [ \Pi ] _ { k } }$ yields additive shares of 1. This essentially generalizes the Spectrum protocol to multiple channels, allowing simultaneous auditing and authorization. PACL improves efficiency by replacing exponentbased checks with a Schnorr proof over secret shares, which proves knowledge of the discrete logarithm of an additively shared element. A second construction, the inclusion predicate, supports multiple access keys per index. Here, servers store an $n \times \ell$ matrix of verification keys and use one DPF to select the $\mathrm { i } ^ { \mathrm { t h } }$ row and another to pick the correct column via correction terms, yielding the required shares for the audit.

Table 1: Comparison of Remise with prior systems. $N = { \mathrm { d a t a b a s e } }$ size, $L = { \mathrm { n u m b e r } }$ of registered writers, $\lambda { = } \operatorname { s e c u r i t y }$ parameter. “Auth Secret Hiding” indicates whether per-index authorization material is hidden from individual servers. “Auth Update Privacy” indicates whether authorization state can be updated without server visibility. For Riposte, $N > L ;$ for other systems $N = L$ . Riposte does not provide authorization. <sup>⋆</sup> Authorization overlaps with database write. <sup>†</sup> Audit and authorization are unified. <sup>‡</sup> Clients send secret shares of index instead of DPF keys, requiring logL bits.

<table><tr><td>System</td><td>ClientReq. Size</td><td>ServerAudit Work</td><td>ServerAuth Work</td><td>Auth SecretHiding</td><td>Auth UpdatePrivacy</td></tr><tr><td>Riposte</td><td> $O(\sqrt{N})$ </td><td> $O(N)$ </td><td>-</td><td>-</td><td>-</td></tr><tr><td>Express</td><td> $O(\lambda^2)$ </td><td> $O(L)$ </td><td> $O(L)^*$ </td><td>×</td><td>×</td></tr><tr><td>Sabre</td><td> $O(\log L)$ </td><td> $O(\log L)$ </td><td> $O(1)$ </td><td>×</td><td>×</td></tr><tr><td>Spectrum</td><td> $O(\log L)$ </td><td> $O(L)$ </td><td> $O(L)^†$ </td><td>√ (DL-Hard)</td><td>×</td></tr><tr><td>Spectrum + PACL</td><td> $O(\log L)$ </td><td> $O(L)$ </td><td> $O(L)^†$ </td><td>√ (DL-Hard)</td><td>×</td></tr><tr><td>Remise</td><td> $O(\log L)^‡$ </td><td>-</td><td> $O(L)$ </td><td>√ (Secret-shared)</td><td>√</td></tr></table>

We compare Remise and prior systems in Table 1. We only consider variants that use 2 main servers (for example, Spectrum can be instantiated with more than 2 servers).

## 1.3 System Overview

Remise<sup>1</sup> is a two-server anonymous communication system that enforces authorization for both read and write operations while providing anonymity. The servers verify authorization without learning the accessed index, the message or the authorization proof. The system supports two instantiations: a public bulletin board model (RemiseBB) and a communication channels model (RemiseCC). In RemiseBB, authorized writers anony mously post messages to pre-assigned slots in the bulletin board. This bulletin board is periodically reconstructed and published. All write requests made by writers (actual or cover traffic), look indistinguishable to the servers or an adversary observing the network. As a result, the link between the writers and the published messages is severed. In RemiseCC, the messages are posted by writers similarly to RemiseBB, except that they are not published. Instead, writers can selectively grant and revoke read access to chosen readers and only an authorized reader can read from a given index. RemiseCC allows writers to update (grant or revoke) read permissions. The RemiseCC servers remain oblivious to both the identities of authorized readers and any changes in the authorization state. Here, all read and write requests (actual and cover traffic) are indistinguishable to the servers and the network, which hides writer-reader link.

Figure 1 gives a brief overview of RemiseBB and RemiseCC and its interaction with users.

Contributions We make the following contributions: (i) We introduce a DORAM-based authorization mechanism for message boards that provides built-in auditability, (ii) We design communication channels in which writers can grant read permissions to readers without servers learning which reader received access, and (iii) We support revocation of access privileges while hiding from the servers whose permissions were modified.

## 1.3.1 Main ideas in realizing Remise

Distributed ORAM for hidden accesses: Remise is a Distributed Oblivious Random Access Memory (DORAM) based Anonymous Communication System. While we defer the detailed discussion of DORAMs to Section 2.3, it suffices for now to know that DORAMs enable multiple parties, each holding secret shares of a memory and secret shares of an index, to perform an oblivious (write or read) access to the memory at the index. Remise servers act like DORAM parties and perform operations on the secret shared database and secret shared inputs.

Built-in Auditing: In previous systems that use DPFs [7, 13, 22, 31] to perform an access on the secret shared databases held by the servers, the client provides the DPF keys for the servers to evaluate. Consequently, the servers have to perform an audit check to ensure that the DPF keys evaluate to valid shares of a 1-hot vector, otherwise malformed DPFs could corrupt the entire database. A consequence of using DORAMs (like Flo ram [11] and Duoram [30], which Remise does) is that the shares of the standard-basis vector are generated by the servers themselves, thereby offloading this computation from potentially malicious clients to the servers.

![](images/2db27619a6163604b6359b0662d53fff39b8a938b2235b4ab7bbfed4000eace7.jpg)  
(a) RemiseBB: Remise instantiated in the anonymous bulletin board model. Requests from writers and cover traffic are indistinguishable to servers and any adversary. Writers write to allocated locations, which the servers reconstruct and publish at the end of each epoch.  
(b) RemiseCC: Remise instantiated in the anonymous communication channels model. Authorized writers post messages accessible only to authorized readers with message content hidden from all other entities. Write requests (including cover traffic) are indistinguishable from one another, and so are read requests, while writer-reader links remain hidden.  
Figure 1: Remise system overview

Resistance to Client–Server Collusion: In Remise, authorization tokens are stored as secret shares across servers, ensuring that authorization secrets remain hidden under client–server collusion, as long as at least one server is semi-honest. In contrast, Express and Sabre store authorization material in the clear, allowing a collud ing server to leak authorization secrets. While Spectrum (and PACL) prevent this leakage under computational assumptions, Remise provides information-theoretic security.

Authorization Revocability Remise (as RemiseCC) supports authorization revocability by allowing writers to obliviously update read authorization tokens (proofs) as sociated with messages they authored. This functionality is essential in anonymous communication settings where a writer controls read access for a dynamic set of read ers. Writers may grant access to new readers or revoke access from previously authorized readers, while preserv ing unlinkability between writers, readers, and database indices. As a consequence of authorization tokens being maintained in secret-shared form, Remise enables these updates to be performed via oblivious DORAM update operations, without exposing which authorization state was modified. In contrast, while Spectrum (and PACL) hide the secret key used for authorization, any modification to the vector of verification keys is directly visible to the servers, precluding oblivious authorization updates.

## 2 Background

## 2.1 Secret Shares

Secret sharing is a cryptographic mechanism for distributing a secret among multiple parties such that any subset of fewer than t parties learns no information about the secret, while any subset of t or more parties can reconstruct it. The parameter t is called the threshold of the secret-sharing scheme. Secret-sharing schemes come in many flavors. We denote additive secret sharing of a value x modulo 2<sup>r</sup> by $x ^ { \mathrm { A S } }$ . When using (k, k) additive sharing among k parties, the individual shares are denoted by $x _ { 0 } ^ { \mathrm { A S } } , \ldots , x _ { k - 1 } ^ { \mathrm { A S } }$ , and satisfy $\textstyle \sum _ { i = 0 } ^ { k - 1 } x _ { i } ^ { \mathrm { A S } } \equiv x$ (mod 2<sup>r</sup>). We use $b ^ { \mathrm { B S } }$ to denote a Boolean share, and $x ^ { \mathrm { G S } }$ to denote a generic (secret) sharing of x. An alternative way to secret-share an index $\dot { \textbf { 1 } } ^ { * }$ is via shares of a one-hot vector, i.e., a vector that is zero everywhere ex cept at the position $\dot { \mathbf { 1 } } ^ { * }$ . Such shares are particularly useful in sender-anonymous communication. Distributed Point Functions (DPFs) [4] provide a succinct mechanism for secret-sharing standard-basis vectors. In particular, (2, 2)- DPFs allow two parties to share a standard-basis vector and serve as a core building block of the Distributed ORAM constructions used in Remise.

## 2.2 Secure Multiparty Computation

Secure Multiparty Computation (MPC) is a cryptographic technique where parties ${ \sf S } _ { 1 } , \ldots , { \sf S } _ { n }$ holding private inputs $x _ { 1 } , \ldots , x _ { n }$ jointly compute a function $f ( x _ { 1 } , \ldots , x _ { n } )$ such that no party learns anything beyond what can be learned from the output. There are three main metrics to evaluate the performance of an MPC protocol, namely, (i) local computation, the computational work performed by each party, (ii) bandwidth, the total communication exchanged between parties during the protocol, and (iii) round complexity, the number of communication rounds (network latencies) required.

In the following we will present some of the MPC protocols that will be used in the paper.

Multiplication: We denote the multiplication operation as $\overline { { z } } ^ { \mathrm { G S } } \gets \mathbf { M U L T } ( x ^ { \mathrm { G S } } , y ^ { \mathrm { G S } } )$ ). Du-Atallah [12] is a variant of the classic Beaver’s method [3] to do multi plication on secret shares, which we use in this paper. While Du-Atallah is a (2 + 1)-Party protocol, it can be easily converted to a 2P-Protocol by using OT (Oblivious Transfer) to produce correlated randomness. We model the protocol using the ideal functionality $\mathcal { F } _ { \sf M U L T }$

EQZ Protocol. The Equal-to-Zero protocol checks whether a secret-shared value is equal to zero. We denote the operation by $b ^ { \mathsf { A S } } \gets \mathsf { E Q Z } ( x ^ { \bar { \mathsf { A S } } } )$ , where the parties holding additive shares of x obtain shares of a bit b such that b = 1 iff $x = 0$ , and $b = 0$ otherwise. We model the protocol using the ideal functionality F<sub>EQZ</sub>.

## 2.3 Oblivious Memory Access

Distributed Oblivious Read-Only Memory (DOROM) supports oblivious reads from a database that is fixed after setup. Let $\mathbf { D } \in \mathbb { F } ^ { n }$ be a database and let $\mathbf { i } ^ { * } \in [ n ]$ denote an index. The two servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold an encrypted representation of the database such that for every $\mathbf { i } \in [ n ] , \mathbf { D } [ \mathbf { i } ] + \mathtt { P R F } \big ( \mathrm { k } _ { 0 } , \mathbf { i } \big ) + \mathtt { P R F } \big ( \mathrm { k } _ { 1 } , \mathbf { i } \big )$ is stored by the servers, while $\mathsf { S } _ { b }$ knows only $\mathrm { k } _ { b } .$ . An oblivious read at a secret-shared index $\mathbf { i } ^ { * \mathbf { A S } }$ is denoted by $\mathrm { D } ^ { \mathrm { R O } } [ \mathrm { i } ^ { * \mathrm { A S } } ]$ which outputs additive shares of $\mathbf { D } [ \mathbf { i } ^ { * } ]$ while leaking only invocation metadata. A read operation is implemented using PIR over the encrypted database, followed by a lightweight MPC step to remove the PRF masks. We model the protocol using the ideal functionality F<sub>DOROM</sub>.

Distributed Oblivious Write-Only Memory (DOWOM) supports oblivious updates to a secret-shared database. The two servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold additive shares $\mathrm { D } _ { 0 } ^ { \mathrm { A S } } , \mathrm { D } _ { 1 } ^ { \mathrm { A S } }$ of the database. An oblivious update at a secret-shared index $\mathrm { i ^ { * A S } }$ by a secret-shared value $\mathsf { M } ^ { \mathrm { A S } }$ is denoted by: $\mathrm { D ^ { A S } [ i ^ { * A S } ]  D ^ { A S } [ i ^ { * A S } ] + M ^ { A S } }$ . The update modifies only the target location while hiding both the accessed index and updated value. Operationally, the servers locally add additive shares of $\mathbf { e } _ { \mathrm { i } ^ { * } } \cdot \mathbb { M }$ to their database shares, where $\mathbf { e _ { i ^ { * } } }$ is standard basis-vector at $\dot { \mathrm { ~ \tt ~ 1 ~ } } ^ { * }$ The protocol leaks only invocation metadata. We model the protocol using the ideal functionality F<sub>DOWOM</sub>.

Distributed Oblivious RAM (DORAM) supports both oblivious reads and oblivious writes. Formally, given additive shares of a database $\mathrm { D ^ { A S } }$ , an index $\mathrm { i ^ { * A \bar { S } } }$ and an update value $\mathsf { M } ^ { \mathrm { A S } }$ , a DORAM supports: (i) oblivious reads producing shares of $\mathbf { D } [ \mathbf { i } ^ { * } ]$ , and (ii) oblivious writes producing updated database shares $\mathrm { { D ^ { \prime } } ^ { \mathrm { { A S } } } }$ such that $\mathbf { D } ^ { \prime } [ \mathbf { i } ] = \mathbf { D } [ \mathbf { i } ]$ for all $\dot { \bf 1 } \neq \dot { \bf 1 } ^ { * }$ , and $\mathrm { D ^ { \prime } } [ \mathrm { i ^ { * } } ] = \mathrm { D } [ \mathrm { i ^ { * } } ] + \tt M$ . The protocol leaks only invocation metadata. We model the protocol using the ideal functionality F<sub>DORAM</sub>.

Supporting both operations simultaneously is more expensive than specialized DOROM or DOWOM constructions. This is because the protocol must either switch between distinct memory layouts, as in Floram [11], or maintain additional auxiliary state such as blinds and blind shares, as in Duoram [30]. In this work, we instantiate DOROM and DOWOM using Floram [11], and instantiate full DORAM using 2P-Duoram [30].

Preprocessing in DORAMs All the standard-basis vector shares needed in DORAMs (including read only and write only) are produced using DPFs. It is important to note that Remise servers produce the DPFs in a preprocessing phase (before the client obliviously informs where to write and what to write) and adjust them to the correct index and value in the online phase with constant communication. For more details, we refer the reader to the Duoram paper [30], beginning with §4.1 which describes the underlying (2 + 1)-party protocol. The twoparty variant, as further discussed in the paper, is obtained by using Oblivious Transfer to generate multiplicative triples.

## 3 Authorized Messaging

Remise operates with two non-colluding servers, $\mathtt { S } _ { 0 }$ and $\mathrm { S } _ { 1 }$ , and can be instantiated in two models: (i) the Anonymous Bulletin Board model, denoted as RemiseBB, and (ii) the Anonymous Communication Channels model, denoted as RemiseCC. Two main types of users interact with Remise, namely, (i) writers, and (ii) read ers. A subset of users may also generate cover traffic by issuing dummy read or write requests. For writes, cover traffic consists of zero-message updates, while for reads, it consists of valid read requests to a reserved dummy index. For the Remise servers, such requests are information-theoretically indistinguishable from real access requests and serve the purpose of increasing the size of the anonymity set.

Setup Phase The functioning of Remise (both RemiseBB and RemiseCC) begins with a setup phase, during which writers obtain authorization to write at specific indices, while the servers remain oblivious to which index was assigned to which writer. In particu lar, the setup ensures that none of the Remise servers learns (i) which users (from the superset of users includ ing cover traffic and actual writers) are authorized to write messages, (ii) which indices are assigned to which writers, or (iii) the value of the write authorization token associated with an assigned index, which is issued to the authorized writer.

RemiseBB In RemiseBB, writers post messages on a shared bulletin board held by the servers which are reconstructed and published after every epoch. A writer submits a write request by sending shares of the message, shares of the index, and shares of the write authorization token. The servers accept the request if the token corre sponds to the index (of course, without learning either the token or the index). Authorized indices in RemiseBB allow for preventing write-collisions as writers are only allowed to write at their assigned index. It also capitalizes on the asymmetry of real-world broadcasting, similar to what Spectrum [22] does, where there are fewer writers than total users in a system. Thus, while keeping the server computation only influenced by the number of real writers, we can still derive anonymity from all users without reserving extra space.

RemiseCC In contrast, in RemiseCC, while writers post messages similar to RemiseBB, the two servers never reconstruct the message database. Instead, the writ ers grant reading rights to specific readers of their choice, and this information is conveyed to the RemiseCC servers obliviously. Similar to write authorization tokens, the servers in RemiseCC also hold shares of read authorization tokens and the writer has control over the values of the read authorization tokens for the index they own. Readers submit read requests by sending shares of the index and shares of the read authorization tokens to the servers in order to retrieve a message. Upon receiving a read request, the RemiseCC servers verify (obliviously) whether the reader has permission to read from that index. If the permission is not granted, the read request is dropped.

Notation Throughout, for any value, array, or database D, we denote its additive sharing between servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ by $\mathrm { { D = D _ { 0 } ^ { A S } + D _ { 1 } ^ { A S } } }$ , where $\mathsf { S } _ { b }$ holds $\mathrm { D } _ { b } ^ { \mathrm { A S } }$ for $b \in \{ 0 , 1 \}$ If D is an additively shared array or database, then for every index $\mathrm { i } , \mathrm { D [ i ] } \stackrel { \bullet } { = } \mathrm { D } _ { 0 } ^ { \mathrm { A S } } [ \dot { \bf i } ] + \mathrm { D } _ { 1 } ^ { \dot { \mathrm { A S } } } [ \dot { \bf i } ]$ . We use D to denote both the bulletin board in RemiseBB and the message board in RemiseCC. The size of D is N. Servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold additive shares of $\mathbf { D } ,$ as well as PRF-encrypted versions of the write-authorization token database, denoted by WRTOK. For each index i, the entry WRTOK[i] encodes the write-authorization tokens required to write to the $\mathrm { i } ^ { \mathrm { t h } }$ location of D. The database WRTOK is readonly. In RemiseCC, the servers additionally hold additive shares of the read-authorization tokens database, denoted by RDTOK. Each entry RDTOK[i] consists of a list of m tokens, where possession of any one token suffices to prove authorization to read the contents of D[i]. During the setup phase, servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold additive shares of the setup database SETUPDB, to which writers post their public keys. At the end of setup, each writer learns its assigned indices via a published database denoted by ACCESSDB.

Threat Model The Remise clients (writers, readers and cover traffic) are completely untrusted. They may deviate arbitrarily from the protocol, form collusion with other clients or with a malicious server. Authorization tokens are treated as bearer credentials. Any entity possessing a valid read or write token for an index may exercise the corresponding capability. For privacy, Remise requires that the servers do not collude with each other. For integrity, Remise requires both servers must follow the protocol. We assume a global network adversary that observes all communication between clients and servers. We assume the existence of pseudorandom generators and pseudorandom functions for any randomness and key generation used in the protocols. We assume the existence of secure channels between each client and each server, providing confidentiality, integrity and replay protection for communicated messages.

## 3.1 Remise APIs

Remise exposes a set of APIs that the users use to interact with the system in both RemiseBB and RemiseCC. We model the system using the ideal functionality $\mathcal { F } _ { \mathsf { R e m i s e } } .$ $\mathcal { F } _ { \sf R e m i s e }$ starts with invoking the SetupPhase containing a registration window during which the users may register as writers. Once the registration window closes, the functionality processes all the requests and assigns indices to registered writers. Once the setup phase ends, $\mathcal { F } _ { \sf R e m i s e }$ allows for writing, reading, and updating authorization any polynomial number of times and in arbitrary order.

Corrupted clients interact with the functionality through the adversary.

More specifically, $\mathcal { F } _ { R e m i s e }$ exposes four interfaces to the users: (i) Setup.Reg, (ii) Write, (iii) UpdateAuth, and (iv) Read. The functionality maintains the following state: (i) WriteAuth : $[ N ]  \{ 0 , 1 \} ^ { \lambda } \cup \{ \perp \}$ , mapping each logical index to its write-authorization token, (ii) ReadAuth : $[ N ]  2 ^ { \{ 0 , 1 \} ^ { \lambda } }$ , mapping each logical index to its set of valid read-authorization tokens, and (iii) $\mathbf { D } : [ N ] \to \mathcal { M }$ , storing the database contents at each logical index. Initially, all entries are set to ⊥ (or the empty set where appropriate). It also maintains a clock $T _ { c l o c k } .$ , boolean variables, namely, setup\_done and win dow\_open.

Corruption. A PPT adversary A statically corrupts at most one server $\mathbf { S } _ { b } \left( b \in \{ 0 , 1 \} \right)$ and an arbitrary strict subset of clients $W _ { C } \subsetneq W$ , where W is the set of registered writers. We assume the existence of cover traffic, and that this cover traffic is not corrupted, since corrupting such a participant is equivalent to them not providing cover.

Real view. The real-world view of ${ \mathcal { A } } ,$ denoted $\mathrm { V i e w } _ { \mathcal A } ^ { \mathrm { R e a l } }$ , contains: (i) the inputs and random coins of every corrupted party, (ii) every protocol message sent or received by a corrupted party including its interaction with any ideal functionality invoked in the hybrid model, and (iii) the public transcript, i.e. every value published by the protocol.

Ideal world. In the ideal world, honest parties do not run the protocol; instead they forward their inputs to the trusted functionality $\mathcal { F } _ { \mathsf { R e m i s e } }$ through its interfaces. On each invocation $\mathcal { F } _ { \sf R e m i s e }$ updates its internal state, returns outputs to the parties over secure channels, and appends the corresponding entry to the leakage log LeakLog.

The Simulator. The simulator S interacts with F<sub>Remise</sub> on behalf of the corrupted parties. The simulator does not know honest parties’ inputs. It is given exactly: (i) the inputs and outputs of the corrupted parties (the corrupt server $\mathsf { S } _ { b }$ and the clients in $W _ { C } )$ , forwarded to and from $\mathcal { F } _ { \sf R e m i s e }$ on their behalf, and (ii) the leakage LeakLog produced by $\mathcal { F } _ { \sf R e m i s e }$ over the whole execution. From these alone $\mathcal { S }$ must produce a transcript $\mathrm { V i e w } _ { \mathcal { S } } ^ { \mathsf { l d e a l } }$ that is indistinguishable from the adversary’s real-world view. Security means $\mathrm { V i e w } _ { \mathcal { A } } ^ { \mathrm { R e a l } } \approx _ { c } \mathrm { V i e w } _ { \mathcal { S } } ^ { | | \mathrm { d e a l } }$ for every PPT A.

Setup Phase Remise (both RemiseBB and RemiseCC) provides a registration API that writers invoke during a one-time setup phase to obtain authorization to write to the database D. Each registered writer is assigned a database index together with a corresponding write authorization token, which will allow them to make authorized write requests to the database index. The setup phase hides from the servers both the set of registered writers and the indices assigned to them: while the servers may observe a superset of users submitting requests (including cover traffic), they cannot distinguish registered writers from non-writers. Additionally, the servers do not learn the value of any write authorization token.

F begins by invoking the functionality SetupPhase (described in Phase 1). At the start of the setup phase, a registration window is open which is controlled by $\mathcal { F } _ { \mathsf { R e m i s e } } \mathrm { ^ { * } s }$ internal clock $T _ { c l o c k }$ . The end of the registration window, $T _ { e n d }$ is fixed in $\mathcal { F } _ { \mathsf { R e m i s e } }$ During the registration window, writers and cover-traffic participants may interact only with the $\mathsf { S e t u p . R e g ( \cdot , \cdot ) }$ interface (Interface 1). Registration requests submitted outside the active registration window are rejected and ignored by the functionality. The functionality accumulates all registration requests received during the window, and processes it accordingly when the window ends. The adversary learns the set of all participants but cannot distinguish registered writers (mode = register) from cover traffic $( { \mathsf { m o d e } } = { \mathsf { c o v e r } } )$ . The adversary additionally learns the unordered set of assigned indices, but does not learn which participant received which index.

Definition 1 formalizes the anonymity achieved during the setup phase. The adversary learns the entire set of participants which includes at least one cover traffic provider and one honest writer but does not learn the set of registered writers.

Definition 1 (Setup anonymity). Let W be the set of registered writers in the setup phase and let $W _ { C } \subsetneq W$ be the corrupted participants. The setup phase satisfies setup anonymity if, in the experiment ofthe Security Model,for every PPT adversary A corrupting one server and the participants in $W _ { C } ,$ there exists a PPT simulator S such that $\begin{array} { r } { \mathrm { V i e w } _ { \mathcal { A } } ^ { \mathrm { R e a l } } \approx _ { c } \ S \big ( 1 ^ { \lambda } , W _ { C } , \mathtt { L e a k L o g } \big ) } \end{array}$

Write Operation in Remise In both RemiseBB and RemiseCC, registered writers are allowed to submit messages at their assigned locations. The system checks each submission and, if permitted, stores it in the message database. Users willing to provide cover traffic may also send write requests by sending zero messages. In the RemiseBB variant the bulletin board is published at the end of each epoch, whereas in RemiseCC, the message board is not published.

${ \sf W i t e } ( \cdot , \cdot , \cdot )$ denotes the interface for writes; the formal definition appears in Interface 2. A client submits a write request by sending $( \mathbf { i } ^ { * } , \Delta \mathbb { M } , \omega )$ , which are the target index, the value update, and the corresponding write authorization token. Here, $\Delta \mathbb { M } = \mathbb { M } ^ { \prime } - \mathbb { M }$ , where $\mathsf { M } ^ { \prime }$ is the new value and M is the current value stored at $\mathbf { D } [ \mathbf { i } ^ { * } ]$ . Since the authorized writer controls the value of $\mathbf { D } [ \mathbf { i } ^ { * } ]$ , we assume that the writer knows the current value M at all times. ${ \sf W r i t e A u t h } [ \dot { \bf 1 } ^ { * } ] = \mathfrak { O }$ means that ω is the correct write authorization token for writing at $\dot { \mathbf { 1 } } ^ { * }$ , while $\Delta \mathbb { M } = 0$ means this is a zero message. In either case, ∆M is added to the $\mathrm { i ^ { * } t h }$ index of D.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\mathcal{F}_{\text{Remise}}: \text{Phase 1 SetupPhase. Functionality of } \mathcal{F}_{\text{Remise}}.$

1: $P \leftarrow \emptyset, Q \leftarrow \emptyset, R \leftarrow \emptyset$
2: setup_done ← false
3: window_open ← true
4: while $T_{clock} \leq T_{end}$ do
    // $T_{clock}$ keeps ticking
    // users use Setup.Reg to make requests
5: end while
6: window_open ← false
7: for each ($w_j, mode_j$) ∈ P do
8:    if $mode_j = register$ then
9:    pick fresh unused index $i^*j \in [N]$
10:    $\omega_j \stackrel{\$}{\leftarrow} \{0, 1\}^\lambda$
11:    WriteAuth[$i^*j$] ← $\omega_j$
12:    $R \leftarrow R \cup \{i^*j\}$
13:    $Q \leftarrow Q \cup \{(w_j, mode_j, i^*j, \omega_j)\}$
14:    end if
15: end for
    // Leak unordered assigned-index set
16: LeakLog ← LeakLog || (assigned : R)
17: A learns LeakLog
18: for each ($w_j, mode_j, i^*j, \omega_j$) ∈ Q with $mode_j = register$ do
19:    $w_j$ learns ($i^*j, \omega_j$) over a secure channel
20: end for
21: setup_done ← true
</div>

Updating Read Authorization in RemiseCC Unlike in RemiseBB, the message board in RemiseCC is not re constructed and published. Instead, readers issue requests using read authorization tokens to read from the message board. The writers can decide who can read the messages they write. They do this by controlling the values of the read authorization tokens for the locations they are assigned to write at. Writers can then communicate values of the tokens to new readers, using some out-of-band method. Writers can also change the value of an exist ing read authorization token, thereby revoking access to all readers who were previously given that token. This step ensures that message access remains controlled and private.

UpdAuth(·, ·, ·) denotes the interface for updating read authorization tokens for an index; the formal definition appears in Interface 3. The writer sends the element-wise difference of the new list of read authorization tokens with the current list. Since a writer authorized to write at index i<sup>∗</sup>, controls the value of ReadAuth[i<sup>∗</sup>], we assume that it knows the current value at all times.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\mathcal{F}_{\text{Remise}}: \text{Interface 1 Setup.Reg}(w, mode): w \text{ is a user, bit mode } \in \{\text{register, cover}\} \text{ tells if } w \text{ wants to register or is providing cover traffic}$

1: if window_open = false then
2:    return ⊥ to w // window closed
3: end if
4: LeakLog ← LeakLog || (Participant : w)
5: P ← P ∪ {(w, mode)}
6: A learns LeakLog

$\mathcal{F}_{\text{Remise}}: \text{Interface 2 Write}(i^*, \Delta M, \omega) \text{ from client } c$

1: if setup_done = false then
2:    return ⊥
3: end if
    // Either it is cover traffic or authorized write
4: if ($\Delta M = 0$) ∨ (ω = WriteAuth[i*]) then
5:    out ← acc
6: else
7:    out ← rej
8: end if
    // Leak public sender identity and decision
9: LeakLog ← LeakLog || (write : c, out)
10: A learns LeakLog
11: if out = acc then
12:    D[i*] ← D[i*] + $\Delta M$
13: end if
    // Return final decision to the servers
14: Servers and c learn out
</div>

Read Operation in RemiseCC Readers who have been granted read access can request to retrieve messages using the read authorization tokens provided by the writer. The servers checks their authorization, and if valid, they provide the reader with the message content.

Read(·,·) denotes the interface for reads; the formal definition appears in Interface 4. A reader submits a read request by sending (i<sup>∗</sup>, t), which are the target index and a read-authorization token. If the token and the index submitted have the correct correspondence, i.e., t ∈ ReadAuth[i<sup>∗</sup>], then the read succeeds and the reader learns D[i<sup>∗</sup>]. The functionality leaks only the identity of the requesting reader and the accept/reject outcome through LeakLog.

Leakage profile. Recall that during setup phase, LeakLog contains entries of the form (Participant : w) and (assigned : R), where R denotes the unordered set of assigned indices. After the setup phase, arbitrary interleavings of Write, UpdAuth, and Read invocations append entries of the form (write : c, out), (updauth : c, out), and (read : c, out). The interface-specific leakage is captured entirely through the entries of LeakLog.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
$\mathcal{F}_{\text{Remise}}: \text{Interface 3 UpdAuth}(i^*, \Delta R, \omega) \text{ from client } c$

1: if setup_done = false then
2:    return ⊥
3: end if
    // ΔR ← R' - R is element-wise diff of new token list with current list
    // Determine whether the update is accepted
4: if ω = WriteAuth[i*] then
5:    out ← acc
6: else
7:    out ← rej
8: end if
    // Leak public sender identity and decision
9: LeakLog ← LeakLog||(updauth : c, out)
10: if out = acc then
11:    ReadAuth[i*] ← ReadAuth[i*] + ΔR
12: end if
13: A learns LeakLog
    // Return final decision to the servers
14: Servers and c learn out

$\mathcal{F}_{\text{Remise}}: \text{Interface 4 Read}(i^*, t) \text{ from client } c$

1: if setup_done = false then
2:    return ⊥
3: end if
    // Determine whether the read is accepted
4: if t ∈ ReadAuth[i*] then
5:    out ← acc // t is a valid token at i*
6: else
7:    out ← rej
8: end if
    // Leak public reader identity and decision
9: LeakLog ← LeakLog||(read : c, out)
10: A learns LeakLog
11: if out = acc then
12:    c learns D[i*]
13: else
14:    c learns ⊥
15: end if
    // Return final decision to the servers
16: Servers and c learn out
</div>

## 4 Remise: The Details

Protocols 5 to 8 realize the interfaces and the authorization states of the ideal functionality $\mathcal { F } _ { \mathrm { R e m i s e } }$ described in Section 3.1. WriteAuth is realized by WRTOK, which is a DOROM held by $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ . ReadAuth is realized by RDTOK, a DORAM database held by $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 } ,$ storing a list of m tokens per index. In the remainder of this section, we describe these protocols in detail and present their corresponding security theorems.

Setup Phase in Remise The setup phase of Remise (both RemiseBB and RemiseCC) consists of three stages. It begins with a writer registration stage, which fol lows a bootstrapping mechanism similar to that of Spectrum [22] and relies on an anonymous broadcast system such as Riposte [7]. The servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold additive shares of an anonymous bulletin board SETUPDB. Writers anonymously submit public keys to random locations in SETUPDB using a Riposte-style anonymous broad cast, modeled by the ideal functionality $\mathcal { F } _ { A B }$ . Anonymous broadcast hides the link between the public key pk and the broadcasting writer w. Writes to SETUPDB are ac cepted only during a fixed registration window.

Remise inherits a non-zero probability of failed reg istrations due to write collisions in Riposte. However, since the registration occurs only once during setup, this allows for us to make the failure probability negligible by over-provisioning the database relative to the maximum number of writer registrations allowed in Remise. We can also use collision recovery methods, as suggested in Riposte [7]. For example, a table of size 2.7N achieves roughly 95% successful registrations while tolerating two-way collisions, where N is the maximum number of registrations.

Once the writer registration phase ends, the servers reconstruct SETUPDB and recover the set of public keys written at random locations. For each such pk, the servers assign a unique database index $\dot { \mathbf { 1 } } ^ { * }$ using an agreed-upon ordering between $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ . The servers hold the additive shares of the write authorization token database WRTOK. To generate a write authorization token for $\dot { \mathtt { 1 } } ^ { * }$ without revealing it to either servers, $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ independently sample random strings $\ell _ { 0 }$ and $\ell _ { 1 }$ respectively, without learning each other’s shares. $\ell _ { 0 } + \ell _ { 1 } = \ell$ becomes the write authorization token for $\dot { \textbf { 1 } } ^ { * }$ . They locally update their respective shares of WRTOK by setting $\mathrm { W R T O K } _ { 0 } [ \mathbf { i } ^ { * } ] \longleftarrow$ $\ell _ { 0 }$ and $\mathbf { W } \mathbf { R } \mathbf { T } 0 \mathbf { K } _ { 1 } [ \mathbf { i } ^ { * } ]  \ell _ { 1 }$ . After assigning an index and token for all submitted requests, the servers convert their additive shares of WRTOK into doubly encrypted readonly database denoted by WRTOK<sup>RO</sup>.

Finally, for each writer with public key pk, each server encrypts its share of the authorization token together with the assigned index $\dot { \mathbf { 1 } } ^ { * }$ under $\mathtt { p k } .$ . These ciphertexts are written to a separate database ACCESSDB at the same position from which pk was read in SETUPDB. The published database ACCESSDB concludes the setup phase, enabling each writer to decrypt and learn its assigned index and corresponding write authorization token. Figure 2 illustrates the setup phase in Remise.

Protocol 5 describes the setup phase in detail. Although the protocol shows w registering for a single index, any writer can reserve multiple indices by making more than one request. The servers may enforce a limit on the number of requests made by each user during the setup phase, to prevent a user from exhausting server resources. In line 5, the servers jointly assign each posted public key to a unique database index by evaluating a randomized function ASSIGN, agreed upon by servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 } .$ . This function picks a uniformly random index and discards a sampling if the index is already assigned.

![](images/21fc93d6c4bd9dd9854db962bfa180eaf3bf9d5d05ca59910ab426fd9cc9f93a.jpg)  
Figure 2: Remise setup phase: In Stage 1: writers post their public keys using an anonymous broadcast system like Riposte. In Stage 2: servers get the value of public key and assign an index $\dot { \mathrm { ~ \tt ~ 1 ~ } } ^ { * }$ . They also sample their respective shares of the write authorization token (L0 and L1), so that no single server knows the actual value of the token. In Stage 3: the servers combine their respective encrypted shares and publish it. They also convert WRTOK into DOROM copies.

Note that during Stage 1, every writer interacts with the anonymous-broadcast functionality ${ \mathcal { F } } _ { \mathsf { A B } } { \mathrm { : } }$ : a registering writer broadcasts a public key, while a cover-traffic par ticipant broadcasts a zero message over the same channel. By the anonymity of $\mathcal { F } _ { \mathsf { A B } }$ , a corrupt server cannot distinguish a public-key broadcast from a zero broadcast, and hence cannot tell a registrant from a cover participant; this indistinguishability is inherited from $\mathcal { F } _ { \mathsf { A B } }$ and is not a property of $\mathcal { F } _ { \sf R e m i s e }$ itself. What $\mathcal { F } _ { \sf R e m i s e }$ additionally guarantees is that the set of assigned indices is revealed without any link to the writers who received them (Def inition 1): even an adversary corrupting one server and the writers in $W _ { C }$ learns the assigned-index set and its own assignments, but no correspondence for any honest writer(s).

Theorem 1 (Setup anonymity). Assume PRF is a secure pseudorandom function, the encryption scheme is IND-CPA secure, and $\mathcal { F } _ { A B }$ is the idealfunctionalityfor anonymous broadcast. Then Protocol 5 securely realizes SetupPhase (Phase 1) of $\mathcal { F } _ { R e m i s e }$ with respect to Defini tion 1, against any PPT adversary corrupting at most one server and any strict subset $W _ { C } \subsetneq W$ of writers.

Proofsketch. WLOG assume $\mathrm { S } _ { 0 }$ is corrupt. Given the leakage from SetupPhase as LeakLog and the corrupted writer set $W _ { C }$ , the simulator S constructs the adversary’s view as follows.

(i) Simulating identities and assignment. S processes LeakLog sequentially. For each leakage entry of the form (Participant : w), S records that participant w participated in the registration. When S encounters an entry (assigned : $R ) _ { : }$ , it interprets R as the unordered set of assigned indices. S now simulates a mapping between public keys and assigned indices for the setup phase as follows: for corrupted writers $w \in W _ { C } ,$ , S uses the adversary-provided public keys and assigned indices. For the remaining assigned indices (corresponding to honest registrants), S samples independent uniformly random public keys, and defines $\{ \mathtt { p k } _ { w } \mapsto \mathbf { i } ^ { * } { } _ { w } \} _ { \mathtt { i } ^ { * } { } _ { w } \in R } ,$ , (ii) Simulating SETUPDB. S populates SETUPDB with public keys for all $w \in W _ { C }$ . The remaining public keys simulated for the honest writers are given to the simulator for $\mathcal { F } _ { \mathsf { A B } }$ , which generates a transcript where the keys appear at uniformly random locations (other than the ones previously populated) in the corrupt server’s view of SETUPDB, leaking only the information allowed by $\mathcal { F } _ { \mathsf { A B } }$ . By anonymity of $\mathcal { F } _ { \mathsf { A B } }$ , the simulated SETUPDB is computationally indistinguishable from the real execution, (iii) Simulating ACCESSDB and local state. Using the mapping $\{ \mathtt { p k } _ { w } \mapsto \mathtt { i } ^ { * } { } _ { w } \} _ { \mathtt { i } ^ { * } { } _ { w } \in R } , \mathtt { S }$ constructs the corresponding entries of ACCESSDB: For all assigned indices, S knows $\ell _ { 0 }$ corresponding to $\dot { \mathbf { 1 } } ^ { * } { } _ { w } \left( \mathrm { i } . \mathrm { e } . \right.$ ., the value in $\mathrm { W R T O K } _ { 0 } \bigl [ \mathbf { i } ^ { * } { } _ { w } \bigr ] \bigr )$ . For indices belonging to honest writers, it samples a uniformly random string to simulate $\ell _ { 1 }$ (the value in $\operatorname { W R T O K } _ { 1 } \left[ \mathbf { i } ^ { * } { } _ { w } \right] )$ , while for writers in $W _ { C } ,$ , it uses adversary known values The simulator writes the encryption of $\left( \mathbf { i } ^ { * } \| \boldsymbol { \ell } _ { 0 } \right)$ and $\left( \mathbf { i } ^ { * } \lVert \boldsymbol { \ell } _ { 1 } \right)$ , using $\mathtt { p k } _ { w } .$ , and (iv) Simu-

Protocol 5 SETUP PHASE IN REMISE: A writer w re quests write authorization to an index in D. Servers S and $\mathsf { S } _ { 1 }$ hold secret shares of a setup bulletin board, SETUPDB. A write authorization token database, WRTOK, is also secret shared between the two servers. WRTOK is empty at the start of the protocol.

```txt
STAGE 1: Writer Registration
1: w generates key pair (pk, sk)
2: w writes pk to a random location i in SETUPDB, i.e. SETUPDB[i] ← pk, using a Riposte-styled write

STAGE 2: Server-Side Assignment
// After the writer-registration window ends
3: S₀ and S₁ reconstruct SETUPDB
4: for all i ∈ [|SETUPDB|] such that SETUPDB[i] is valid public key pk do
// Servers agree on assignment of fresh index
5: S₀ and S₁ compute i* ← ASSIGN()
6: for b ∈ {0,1} do
7: S_b samples a random string ℓ_b ← {0,1}^λ
8: S_b stores WRTOK_b[i*] ← ℓ_b
9: S_b computes c_b ← ENC_pk(i* || ℓ_b)
10: end for
11: S₀ and S₁ write (c₀ || c₁) to ACCESSDB[i]
12: end for
13: S₀ and S₁ publish ACCESSDB
// servers convert WRTOK shares into encrypted copies
14: For each b ∈ {0,1}, S_b samples key k_b
15: S_b, constructs vector R_b, where R_b[i'] = PRF(k_b, i') for all index i' ∈ [N]
16: S_b sends (WRTOK_b + R_b) to S_{1-b}
// S₀, S₁ hold (WRTOK₀ + R₀), (WRTOK₁ + R₁)
17: Servers calculate and store WRTOK^RO ← WRTOK₀ + R₀ + WRTOK₁ + R₁

STAGE 3: Writer Key Retrieval
18: w retrieves ACCESSDB[i]
19: w decrypts using sk to obtain (i*,ℓ₀,ℓ₁)
20: w reconstructs ℓ ← ℓ₀ + ℓ₁ // ℓ is the write authorization token for i*
```

lating $\mathbf { W } \mathbf { R } \mathbf { T O K } ^ { \mathbf { R O } }$ . Finally, it simulates the PRF-masked read-only memory, by simulating the masked share of $\mathsf { S } _ { 1 }$ $( \mathbf { W } \mathbf { R } \mathbf { T } \mathbf { O } \mathbf { K } _ { 1 } + R _ { 1 } )$ by replacing PRF values $( R _ { 1 } )$ with uniformly random values. Finally, $\mathcal { S }$ outputs the simulated SETUPDB, ACCESSDB, WRTOK<sup>RO</sup>, and the local state of $\mathtt { S } _ { 0 }$

The simulated view is computationally indistinguishable from the real execution by: (i) anonymity of $\mathcal { F } _ { \mathsf { A B } }$ (ii) pseudorandomness of PRF, and (iii) IND-CPA security of the encryption scheme. All remaining components are perfectly distributed. □

Writing in Remise A writer submits a write request to servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ by sending $( \mathbf { i } ^ { * \mathrm { A S } } , \Delta \mathbb { M } ^ { \mathrm { A S } } , \mathbf { \omega } ^ { \mathrm { A S } } )$ , which are additive shares of the target index, the value update, and the corresponding write authorization token. $\mathbf { D } [ \mathbf { i } ^ { * } ]$ is updated with value ∆M if either ω is the valid write authorization token for $\dot { \mathtt { 1 } } ^ { * }$ , or if $\Delta \mathbb { M } = 0 ,$ , corresponding to cover traffic.

Protocol 6 describes the process of writing in Remise. w has full control over the value $\mathbf { D } [ \mathbf { \lambda i } ^ { * } ]$ and thus we assume it knows the value M before making write request. Before any write is made $\mathbf { D } [ \mathbf { i } ] = 0$ for all index i. Line 3 checks if the payload value (∆M), is zero. If ∆M is zero, $z ^ { \mathrm { A S } }  1 ^ { \mathrm { A S } }$ , otherwise $z ^ { \mathrm { A S } }  0 ^ { \mathrm { A S } }$ . Line 4 does a DOROM read into the token database to get shares of the actual token of write authorization. Line 6 computes an MPC OR of two check values, z and auth, to ensure either a zero message is provided or the authorization passed. In RemiseBB, Line 9 is a write-only memory access, while in RemiseCC, it is a DORAM write.

Providing Read Authorization Granting read access to an index $\dot { \mathbf { 1 } } ^ { * }$ in RemiseCC consists of two steps: (i) distributing a read-authorization token to the reader, and (ii) obliviously updating the token database so that possession of the token grants read access to $\dot { \mathbf { 1 } } ^ { * }$ . A writer may distribute the token either through an initial in-person exchange or via a dialing protocol such as Express $[ 1 3 ] . ^ { 2 }$ After distributing the token, the writer must inform the servers that possession of the token authorizes reading from an index (say i<sup>∗</sup>) of the message board. Servers $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ hold additive shares of a read authorization token database RDTOK. Each entry RDTOK[i] consists of a list of m tokens, where possession of any one token suffices to read D[i]. Before updating RDTOK, the servers verify that the requester is authorized to write to index $\dot { \textbf { 1 } } ^ { * }$ by checking the supplied write-authorization proof, exactly as in the write operation (Protocol 6). If the check succeeds, $\mathtt { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ update their shares of RDTOK via a DORAM write. The writer can revoke read authorization for readers holding a token, by removing it from the list RDTOK[i<sup>∗</sup>] during the update. To support cover $\mathrm { t r a f f i c } ^ { 3 }$ RemiseCC designates a public-update index $\dot { \bf 1 } _ { \mathrm { u p d } }$ whose write-authorization token is public. Any user willing to provide cover traffic can make updates to $\mathrm { \mathbf { R D T O K } } \big [ \mathrm { i } _ { \mathrm { u p d } } \big ]$ using the same protocol for update (Protocol 7). The servers do not assign $\mathrm { \dot { \bar { 1 } } _ { u p d } }$ in the setup phase.

```txt
Protocol 6 WRITE IN REMISE: Writer w wants to write M' at i*th index of the database D. w knows the current value of D[ i* ] as M and holds ω as write authorization proof. S0 and S1 hold shares of D and WRTOK. At the end of the protocol, if the write authorization passes, S0 and S1 will end up with new shares of D, such that D[ i* ] ← M'

1: w calculates ΔM ← M' - M // new val. - curr. val.
2: For each b ∈ {0,1}, w sends (i*ASb, ΔMASb, ωASb) to Sb.
// Servers obliviously check for zero message
3: zAS ← EQZ(ΔMAS)
// Servers do DOROM read on the write token database
4: FAS ← WRTOKRO[i*AS]
5: authAS ← EQZ(FAS - ωAS)
// MPC OR operation
6: auditAS ← authAS ∨ zAS
// Servers reconstruct audit
7: audit ← REC(auditAS)
8: if audit = 1 then
9: DAS[i*AS] ← DAS[i*AS] + ΔMAS // D[ i* ] = M
10: else
11: return // Reject the request and perform no write
12: end if
```

Protocol 7 describes the protocol that allows a writer to update the values of read authorization tokens for an index. The RemiseCC servers have to first ascertain that the writer updating the tokens for an index, is indeed the author of the messages at that index (say i<sup>∗</sup>). Lines 4 to 6 authenticate the writer. Once the writer is authenticated, in Line 8 RDTOK is updated via a DORAM update operation, such that the list of tokens at index $\dot { \textbf { 1 } } ^ { * }$ holds new token values that the writer wants.

Reading in RemiseCC Recall that in RemiseCC, the servers do not reconstruct the message board. Instead, readers read from D, held as additive shares by $\mathrm { S } _ { 0 }$ and $\mathsf { S } _ { 1 }$ A reader submits a read request by sending $\mathbf { \bar { \Phi } } _ { \mathbf { ( i ^ { * } A S , t ^ { A S } ) } }$ which are shares of the index they wish to read from and the shares of the read authorization token they received from the writer. Protocol 8 describes the protocol to read in RemiseCC. We first remark that the notion of reading in RemiseBB does not exist since that is a broadcasting system, where the messages are published. Lines 2 to 11 authenticate the reader. To authenticate, the servers obliviously check that the reader knows at least one of the read tokens associated with the index they are trying to access. Readers providing cover traffic simply send read requests to a special index $\dot { \bf 1 } _ { \mathrm { r e a d } }$ . Similar $\mathrm { \ t o \ i _ { \mathrm { u p d } } }$ , this index is not assigned to a writer during the setup phase. The read authorization tokens $\dot { \bf 1 } _ { \mathrm { r e a d } }$ $( \mathrm { R D T O K } \big [ \mathbf { i } _ { \mathrm { r e a d } } \big ] )$ , are made public and are used to make read requests to it. The write authorization token for $\dot { \bf 1 } _ { \mathrm { r e a d } }$ $( \mathbf { W } \mathbf { R } \mathbf { T } \mathbf { O } \mathbf { K } \big [ \mathbf { i } _ { \mathrm { r e a d } } \big ] )$ however, must be hidden by the servers. This is to prevent any malicious user from updating RDTOK[i<sub>read</sub>] using Protocol 7.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Protocol 7 UPDATE READ AUTHORIZATION IN REMISECC: Writer w has write authorization to index i* and knows the current list of m tokens at RDTOK[i*] denoted by  $R_{i*}$ .  $S_{0}$  and  $S_{1}$  hold shares of a token database RDTOK. w wants to write new list  $R'_{i*}$  at RDTOK[i*].
// w prepares new tokens for i*.
1: w constructs  $R'_{i*} = \{t_{1}, \ldots, t_{m}\}$ .
// w computes the element-wise difference
2:  $\Delta R_{i*} \leftarrow R'_{i*} - R_{i*}$ .
3: For each  $b \in \{0, 1\}$ , w sends ( $i^{AS}, \Delta R_{i*}^{AS}, \omega^{AS}$ )
// Servers check writer's authorization.
4:  $F^{AS} \leftarrow WRTOK^{AS}[i^{AS}]$ 
5: check $^{AS} \leftarrow EQZ(\mathcal{F}^{\mathrm{AS}} - \omega^{\mathrm{AS}})$ 
6: check  $\leftarrow REC(check^{AS})$ 
7: if check = 1 then
// Authorized: update token list at i*.
8:  $RDTOK^{AS}[i*] \leftarrow RDTOK^{AS}[i*] + \Delta R_{i*}^{AS}$ 
9: else
10: return // Reject the request
11: end if
// Cover traffic: any user may run the same protocol with  $i^{*} = i_{upd}$ , using the public write-token for  $i_{upd}$ .
</div>

Theorem 2 (Write/UpdAuth/Read privacy). In the (F<sub>DOROM</sub>,F<sub>DOWOM</sub>,F<sub>DORAM</sub>,F<sub>EQZ</sub>,F<sub>MULT</sub>)-hybrid model, Protocols 6, 7, and 8 securely realize the Write, UpdAuth, and Read interfaces, respectively, of F<sub>Remise</sub> against any semi-honest adversary corrupting one server and any subset of clients.

Proofsketch. WLOG assume $\mathtt { S } _ { 0 }$ is corrupt. The simulator $\mathcal { S }$ processes LeakLog sequentially. For each leakage entry of the form (write : c, out), (updauth : c, out), or (read : ${ \mathrm { : } } c , \mathsf { o u t } { \mathrm { ) } }$ , S invokes the corresponding simulation procedure described below to simulate the adversary’s view using the underlying hybrid simulators.

Write. Let $\mathbf { \left( i ^ { * } , \right)} \Delta M , \omega $ be the honest writer’s input. The simulator samples additive shares $\mathbf { i } _ { \mathrm { ~ 0 ~ } } ^ { * \mathrm { A S } } , \Delta \mathrm { M } _ { 0 } ^ { \mathrm { A S } }$ , and $\mathfrak { w } _ { 0 } ^ { \mathrm { A S } }$ uniformly and delivers them to $\mathtt { S } _ { 0 }$ . It then: (i) invokes the $\mathcal { F } _ { \mathrm { E Q Z } }$ simulator to simulate the zero-check on $\Delta \mathsf { M } ^ { \mathrm { A S } }$ , (ii) invokes the F<sub>DOROM</sub> simulator on $( 1 ^ { \lambda } , \dot { \bf 1 } ^ { * \mathrm { A S } } )$ to simulate retrieval of the proof share, (iii) invokes the F<sub>EQZ</sub> simulator again for the proof equality test, (iv) invokes the $\mathcal { F } _ { \mathrm { M U L T } }$ simulator for the OR-combination step;, and (v) if $\mathsf { o u t } = \mathsf { a c c }$ , invokes the write simulator for ei ther F (RemiseBB) or $\mathcal { F } _ { \mathrm { D O R A M } }$ (RemiseCC) on $( 1 ^ { \lambda } , \dot { \bf 1 } _ { ~ 0 } ^ { * \mathrm { A S } } , \Delta { \sf M } _ { 0 } ^ { \mathrm { A S } } )$ ). If $\mathsf { o u t } = \mathsf { r e j }$ , the simulator halts.

```txt
Protocol 8 READ IN REMISECC: A reader r wants to read content D[ i* ] using read authorization token t. Servers hold shares of D and RDTOK. At the end of the protocol, r reads D[i*] if t ∈ RDTOK[i*].

// Reader sends shares of index and its read authorization token to the servers
// Readers providing cover traffic would send same request for the reserved index i_read

1: For each b ∈ {0,1}, r sends (i *AS_b, t^AS_b) to S_b
// Servers do a DORAM read to get shares of the list of tokens for i*

2: T^AS ← RDTOK^AS[i*AS]

3: Parse T^AS = {t_1^AS, ..., t_m^AS}

// Servers calculate additive shares of the check value for each of the token in the list

4: for all t_i ∈ T do

5: check_i^AS ← t_i^AS - t^AS

6: end for
// Servers check if any token matches

7: for i = 1 to m do

8: z_i^AS ← EQZ(check_i^AS)

9: end for

10: auth^AS ← ∨_{i=1}^m z_i^AS

11: auth ← REC(auth^AS) // servers reconstruct

12: if auth = 1 then
// Allow read operation

13: read^AS ← D^AS[i*AS]

14: S_0 and S_1 send read^AS_0 and read^AS_1 to the reader.
// Reconstruction of the shares

15: The reader computes: read ← read^AS_0 + read^AS_1

16: else
// Drop the read request

17: return

18: end if
```

UpdAuth. Let $\left( \mathbf { i } ^ { * } , \Delta R _ { \mathrm { i } ^ { * } } , \omega \right)$ be the honest writer $\mathrm { \nabla ^ { \cdot } s }$ input. The simulator samples $\mathbf { i } _ { 0 } ^ { * \mathrm { A S } } , \mathbf { \omega } _ { 0 } ^ { \mathrm { A S } }$ , and $\Delta R _ { \mathrm { i ^ { * } 0 } } ^ { \mathrm { \Delta A S } }$ uniformly and delivers them to $\mathrm { S } _ { 0 } .$ . It then: (i) invokes the F<sub>DOROM</sub> simulator on $( 1 ^ { \lambda } , \mathrm { i } ^ { * \mathrm { A S } } )$ to simulate retrieval of the proof share, (ii) invokes the $\mathcal { F } _ { \mathrm { E Q Z } }$ simulator to simu late the equality test, and (iii) if out = acc, invokes the $\mathcal { F } _ { \mathrm { D O R A M } }$ simulator on $( 1 ^ { \lambda } , \dot { \bf 1 } _ { ~ 0 } ^ { * \mathrm { A S } } , \Delta R _ { \mathrm { i } ^ { * } 0 } ^ { \mathrm { ~ A S } } )$ to simulate the token-database update. If $\mathsf { o u t } = \mathsf { r e j }$ , the simulator halts.

Read. Let $( \mathtt { i } ^ { * } , \mathtt { t } )$ be the honest reader’s input. The simulator samples $\mathbf { i } _ { \mathrm { ~ 0 ~ } } ^ { * \mathrm { A S } }$ and $\mathrm { t } _ { 0 } ^ { \mathrm { A S } }$ uniformly and delivers them to $\mathrm { S } _ { 0 } .$ . It then: (i) invokes the F<sub>DORAM</sub> simulator on $( \mathbf { i } _ { 0 } ^ { * \mathrm { { A S } } } , \mathbf { i } _ { 0 } ^ { \mathrm { { A S } } } )$ to simulate retrieval of token shares, (ii) invokes the $\mathcal { F } _ { \mathrm { E Q Z } }$ simulator for the m equality checks, (iii) invokes the $\mathcal { F } _ { \mathrm { M U L T } }$ simulator for the m-way-OR-combination step, and (iv) if $\mathsf { o u t } = \mathsf { a c c } .$ , invokes the $\mathcal { F } _ { \mathrm { D O R A M } }$ simulator on $( 1 ^ { \lambda } , \dot { \bf 1 } ^ { * \mathrm { A S } } )$ to simulate the DORAM read. If out $= { \mathsf { r e j } }$ , the simulator halts.

In all three cases, the simulated shares are uniformly distributed and computationally indistinguishable from the real protocol execution by the security of the underlying hybrid functionalities. Hence, the simulated transcript is indistinguishable from the corrupt server’s real view. □ We end this section by remarking that Dynamic broadcast encryption schemes such as that of Delerablée et al. [10] also achieve authorized reading by restricting decryption to authorized readers, but typically reveal authorization or revocation structure through ciphertext or key updates. In contrast, RemiseCC stores authorization state separately in the oblivious token database RDTOK. Revocation requires only an oblivious DORAM update to RDTOK, without re-encrypting stored messages or revealing which authorization state changed.

## 4.1 RemiseBB (Sabre): Authorization w/o DORAMs

If we relax our threat model to disallow collusion between a RemiseBB server and a user, we can achieve authorization without relying on DORAMs by borrowing Sabre’s authorization check [31]. Let $F : \{ 0 , 1 \} ^ { \lambda } \times I \to$ $\{ 0 , 1 \} ^ { \lambda }$ be a PRF. The authorization token for an index i is defined as $\tau _ { i } = F _ { \mathrm { k } } ( i )$ , where the PRF key k is known to the two servers. A client authorized to access index $\dot { \textbf { 1 } } ^ { * }$ is given the token $\tau _ { \mathrm { i ^ { * } } } = F _ { \mathrm { k } } ( \mathrm { i ^ { * } } )$ during setup. To make an access, the client submits additive shares of the target index $\mathbf { i } _ { \mathrm { ~ 0 ~ } } ^ { * \mathrm { A S } } , \mathbf { i } _ { \mathrm { ~ 1 ~ } } ^ { * \mathrm { A S } }$ , along with additive shares of the token $\tau _ { 0 } ^ { \mathrm { A S } } , \tau _ { 1 } ^ { \mathrm { A S } }$ . Using their shares of $\dot { \mathbf { 1 } } ^ { * }$ , the servers jointly evaluate the PRF under MPC to compute $\tau ^ { \star } = F _ { \kappa } ( \mathfrak { i } ^ { * } )$ , and then perform an MPC equality check to verify that $\pmb { \tau } ^ { \star } = \pmb { \tau } .$ If the check succeeds, the access is authorized. The authorization check has constant computational complexity and communication complexity. As in Sabre, collusion between a server and a client is out of scope: since the servers know the PRF key, they can compute valid authorization tokens for any index, and therefore such collusion trivially enables unauthorized access. Unlike Sabre, RemiseBB (Sabre) does not need to perform an audit to check the validity of the DPFs. We remark that combining RemiseCC with Sabre does not yield an efficient construction that also preserves writer-reader unlinkability.

## 4.2 Limitations

Concurrent Reads and Writes. RemiseCC does not guarantee linearizable consistency under concurrent reads and writes to the same location. If a read and write overlap, the two servers may observe different operation orders, causing the reader to reconstruct one old share and one updated share, yielding an inconsistent value. This affects only read consistency; it does not compromise write correctness, authorization, or privacy. Once both servers process the write, the database con verges to the correct state. This limitation is common in asynchronous secret-shared storage systems without coordination, including Express and Sabre. Systems such as Riposte and Spectrum avoid this issue by restricting reads to completed epochs. Locking or versioning could provide stronger consistency, but would increase latency and potentially leak additional access-pattern informa tion. We leave stronger consistency guarantees to future work.

Out-of-Band Token Distribution. When granting read access, a writer in RemiseCC must distribute a fresh authorization token through an out-of-band channel. This assumption is also present in systems such as Sabre, Ex press, and Spectrum, where readers must initially obtain shared secrets or authorization material externally. De signing scalable and privacy-preserving authorization distribution mechanisms without trusted setup channels remains an open problem.

Malicious Servers. Unlike in Spectrum, Remise does not provide any Blame-Game protocol. Therefore, a ma licious server could potentially drop write request from an honest client. We assume semi-honest behavior from Remise servers.

## 5 Implementation and Evaluation

Table 2 describes the asymptotic costs in realizing Remise. DPF evaluation in MPC accounts for the preprocessing cost. Notice that the costs in RemiseCC have factor of m, the number of read tokens per database index.

We implemented a proof-of-concept prototype in C++. All experiments were conducted on a server equipped with two Intel<sup>®</sup> Xeon<sup>®</sup> Gold 6430 processors, 251 GiB of RAM, and running a 64-bit Linux operating system. Network latency and bandwidth were emulated using tc netem, and all experiments were run on an otherwise idle system. Spectrum (PACL) and Express (PACL) mean Spectrum and Express integrated with PACL access control mechanism, respectively. We compare RemiseBB with Spectrum (PACL), and RemiseBB (Sabre) with Express (PACL), since each pair operates under the same threat model. In particular, in both RemiseBB and Spec trum (PACL), server-client collusion does not allow the server to unilaterally issue a write token to an arbitrary writer. While in RemiseBB (Sabre) and Express (PACL), server-client collusion can enable a single server to issue write tokens to arbitrary writers.

In the following, we compare Remise with the various anonymous communication systems in PACL’s codebase<sup>4</sup>, namely Spectrum and Express.

Bandwidth Comparisons Table 3 compares the bandwidth consumption for write operations of Remise and PACL systems. First observe that the client request size for write operations in Remise (RemiseBB, RemiseCC and RemiseBB (Sabre)) is smaller. This is because, in Remise the client does not send the DPF keys, rather the servers construct the DPF from the index and the message shares. We observe that the validity check bandwidth(auditing + authorization) is independent of the message size for all systems. In Remise, the messages shares are only used once the authorization passes and they go to the access phase.

Request Validity Check Comparisons Figure 3a compares the wall-clock time for servers to check the validity of a single write request (includes DPF audit (if any), and authorization checks) in RemiseBB and Spectrum (PACL) under three network latencies: 10 ms, 30 ms, and 60 ms. We do not include a comparison with plain Spectrum, since integrating PACL improves its performance by more than an order of magnitude. For smaller database sizes, Spectrum (PACL) outperforms the total cost (preprocessing plus online) of RemiseBB. This behavior is expected. The preprocessing phase of RemiseBB —specifically, the MPC-based generation of shares of a standard-basis vector—requires O(log n) rounds of communication. In contrast, Spectrum (PACL) relies on the evaluation of a verifiable DPF, which, while computationally more expensive than a standard DPF, avoids this additional round complexity. As the database size increases, computational overhead begins to dominate latency-induced costs. This trend is reflected in our results: at lower latencies, the crossover point at which RemiseBB outperforms Spectrum (PACL) occurs at smaller database sizes. We were unable to execute the Spectrum (PACL) implementation beyond 2<sup>26</sup>; however, extrapolating from existing measurements, the performance gap is expected to further favor RemiseBB at larger scales. Finally, when considering only the online phase, the gains are an order of magnitude larger. For example, at a database size of 2<sup>26</sup>, RemiseBB provides nearly an 80× speedup over Spectrum (PACL).

Figure 3b compares the time required to validate a request in RemiseBB (Sabre) against the time required to validate a single request in Express (PACL). Since RemiseBB (Sabre)’s implementation amortizes latency across a large batch of requests, while Express(PACL) is dominated by per request local computation, comparing these operating points makes the performance differ ences more apparent in the plots. We first point out that in RemiseBB (Sabre) there is no preprocessing phase for the authorization. Observe that since the authorization check in RemiseBB (Sabre) is PRF-based it is independent of the database size. In Express (PACL), however, since the authorization involves evaluating the DPF, the authorization time grows linearly with the database size. The upshot of this will be visible in the following paragraph in Figure 4b, where we will observe that the through put for RemiseBB (Sabre) will be much higher than the throughput of Express (PACL).

Table 2: Server-Side Cost Comparison of Remise Variants. Cost mentioned in gray is the preprocessing cost.

<table><tr><td>Operation</td><td>Local Computation</td><td>Bandwidth</td><td>Rounds</td></tr><tr><td>Remise Write</td><td> $O(n) + O(n)$ </td><td> $O(\lg n) + O(1)$ </td><td> $O(\lg n) + O(1)$ </td></tr><tr><td>RemiseCC Read</td><td> $O(n) + O(n \cdot m)$ </td><td> $O(\lg n) + O(m)$ </td><td> $O(\lg n) + O(1)$ </td></tr><tr><td>RemiseCC Update Authorization</td><td> $O(n) + O(n \cdot m)$ </td><td> $O(\lg n) + O(m)$ </td><td> $O(\lg n) + O(1)$ </td></tr></table>

Table 3: Bandwidth (in bytes) decomposition across different systems during the write operation. We fix the database size at $2 ^ { 2 0 }$ . In the table, n denotes the number of write requests, k out-of-n requests are authorized, m denotes the size of the payload. The number of LowMC rounds in RemiseBB (Sabre) is denoted as rnds. The DOROM operation in Remise uses LowMC cipher, thus it appears in the Req. validity Check bandwidth. The gray values represents the preprocessing phase communication. Spectrum and Express communications were calculated from their source code.

<table><tr><td>System</td><td>Client Req. Size writer → Sb</td><td>Req. Validity Check Sb → S1-b</td><td>Access Sb → S1-b</td></tr><tr><td>Remise</td><td>(m+24)·n</td><td>960·n+16·(2·rnds+3)·n</td><td>m·k</td></tr><tr><td>RemiseBB (Sabre)</td><td>(m+24)·n</td><td>16·(rnds+3)n</td><td>m·k</td></tr><tr><td>Spectrum (PACL)</td><td>(m+3120)·n</td><td>65·n</td><td>0</td></tr><tr><td>Express (PACL)</td><td>(m+376)·n</td><td>16·n</td><td>0</td></tr></table>

Throughput and Goodput Comparisons Figure 4 compares the throughput and goodput achieved by the different systems under varying fractions of unauthorized traffic. For RemiseBB (and RemiseBB (Sabre)), we eval uate two configurations: (i) using offline-preprocessed DPFs, and (ii) generating (on-the-fly) DPFs online during request processing.

Observe in Figure 4a that online DPF generation signif icantly reduces both throughput and goodput compared to the offline-preprocessed setting. In contrast, when DPFs are preprocessed offline, increasing the fraction of unauthorized traffic improves throughput and goodput. This is because unauthorized requests terminate after the lightweight authorization phase and avoid the more expensive access phase.

Finally, Figure 4b shows that as the fraction of unauthorized traffic increases, RemiseBB (Sabre) with on the-fly DPF generation, surpasses Express (PACL) at progressively smaller database sizes. This is because the authorization cost of RemiseBB (Sabre) is O(1), since it avoids DPF expansion during authorization.

Cost Breakdown and Effect of Message Size Figure 5 shows the breakdown of the total wall-clock time into preprocessing, online validity check, and access costs for different message sizes. We fix the size of the database to $2 ^ { 2 0 }$ and network latency to 30 ms. We observe that the online validity check contributes only a small fraction of the total execution time in Remise. The preprocessing cost appears for RemiseBB and RemiseBB (Sabre), while the remaining systems do not perform any preprocessing. Furthermore, the access cost dominates the overall runtime and increases significantly with the message size. Observe that, the access costs for all systems are identical, as they rely on the same underlying DPFbased access mechanism. The upshot of this is that, as the message size increases, the throughput and goodput are similarly affected across systems. For all systems, the validity check cost remains nearly constant across different message sizes, since the validity of a request is independent of the transferred payload size. The figure also illustrates that unauthorized requests avoid the expensive memory-access phase entirely; consequently, the large “green” access component would be absent for such requests, reducing both wall-clock time and bandwidth consumption.

RemiseCC vs. PACL-Inclusion Predicate In Figure 6, we benchmark the time taken by the servers to perform authorization checks on read requests in RemiseCC. We compare against PACL’s inclusion predicate access control, as it provides the same functionality of having multiple read authorization tokens per index. The experiment is done on a database of size $2 ^ { 2 4 }$ while varying the number access tokens per index. We do not plot the online time for RemiseCC as it is close to the total time because we use 2P-Duoram, which uses a Computationally symmetric PIR (CSPIR) [30].

![](images/e612ae978e0e64d25999d7a8b1f3d7a378005fe55d2b9b54e067f33a8b67fa5e.jpg)

![](images/725bebd66f61c3b441c395f3d922de1c7713e9bbb8a42cdf7831dee0daba79b0.jpg)

![](images/d586fc499a70536e759a1272a6f02b78bab76d4e2a074d395dcb8e2b5b011a62.jpg)

![](images/07840fff3a3261546ef12b3686d2fdf0f7428ffa6b2177fe4de91e1bbceae08e.jpg)  
(a) RemiseBB vs. Spectrum (PACL); experiments for Spectrum (PACL) were limited to input size $2 ^ { 2 6 }$ due to infrastructure constraints. The corresponding error bars are small; for example, for RemiseBB at 30 ms latency and input size $2 ^ { 2 4 }$ , the observed variation is ±14.597 ms for total time and ±8.8908 ms for online time.  
(b) RemiseBB (Sabre) vs. Express (PACL); experiments for Express (PACL) were limited to size $2 ^ { 2 6 }$ due to infrastructure constraints. The variance is too small, thus the error bars are not visible.  
Figure 3: Wall-clock time comparison of request validity check during write operations in RemiseBB with PACL systems for different latencies while varying the database size.

## 6 Related Work

DC-nets based Systems: Anonymous communication systems often use dining cryptographer networks (DC nets) to achieve sender-recipient unobservability, where one participant sends a real message while others send cover traffic. However, DC-nets suffer from high commu nication overhead, poor scalability, and disruption attacks, where a malicious participant can corrupt a broadcast using an invalid share. Dissent [8] introduces a costly blame protocol to identify disruptors but cannot prevent disruptions. Verdict [9] improves this using proofs of correctness, enabling verifiable DC-nets that prevent malformed contributions.

PIR-based Systems: Pynchon Gate [26] uses private information retrieval (PIR) for pseudonymous mail retrieval. Pung [1] extends this with a PIR-based key-value store where clients privately retrieve encrypted messages indexed by keys derived from shared secrets. Talek [6] supports private group messaging via a private log indexed using blocked cuckoo hashing [24], with clients using a PRF on a secret log handle to derive pseudorandom locations. Distributed-PIR [29] reduces server computation by offloading work to clients, increasing client overhead.

Mix-Net Based Systems: Mix-net systems obfuscate message sources through relays and shuffling. Riffle [17] uses verifiable shuffles and relies on the anytrust model, where anonymity holds if one server is honest. Cmix [5] and Trellis [20] improve efficiency using precomputation. Atom [16] iteratively shuffles messages across server groups, requiring one honest server per group. XRD [18] assigns clients mailboxes and uses loopback messages and shared chains to hide communication patterns.

Differential Privacy based Systems: Vuvuzela [32] pioneered differential privacy based anonymous messaging using shared drop locations derived from shared keys. Karaoke [21] improves Vuvuzela with efficient noise verification. Groove [2] further improves flexibility by allowing users to pre-submit messages, go offline without privacy loss, and communicate concurrently with multiple users.

ORAM-based Systems: Myco [15] introduces an ORAM-based metadata-private messaging system using an asymmetric two-server model, where servers emulate the ORAM client and server. Myco achieves polylogarithmic per-access server work, outperforming PIR and DPF-based systems. However, Myco does not provide server-enforced access control: any client can read any location and must trial-decrypt entries. While Remise presents a Distributed-ORAM based communication system, it focuses on improving access control in DPF-based systems by enabling servers to enforce authorized read and write locations and reject unauthorized accesses.

![](images/35a00696fdadb3476e44c3583f7fb81b3e09467ba482371c4222325547299dae.jpg)  
(a) RemiseBB vs. Spectrum (PACL); experiments for Spectrum (PACL) were limited to database size $2 ^ { 2 6 }$ due to infrastructure constraints. The corresponding error bars are small.  
RemiseBB(Sabre) (w/ preproc DPFs) Thrput 1 RemiseBB(Sabre) (w/ on-the-fly DPFs) Thrput Express(PACL) Thrput RemiseBB(Sabre) (w/ preproc DPFs) Goodput RemiseBB(Sabre) (w/ on-the-fly DPFs) Goodput Express(PACL) Goodpu

![](images/cb70e0187439e4aa3d5f67f0b2d16e497eecf76b098c8a77742ea2b24ec49be6.jpg)  
(b) RemiseBB (Sabre) vs. Express (PACL); All values for RemiseBB (Sabre) uses on-the-fly DPFs. Experiments for Express (PACL) were limited to database size $2 ^ { 2 6 }$ due to infrastructure constraints. The corresponding error bars are small.

Figure 4: Throughput and Goodput Performance: We vary the database size and keep the latency fixed at 30ms. The message size in these experiments is 32 bytes  
![](images/d2515fd005812f199e06c61cceb52a714781857f5743b13ecd459483f746a2b8.jpg)  
Figure 5: Breakdown of total cost for different message sizes for database size $2 ^ { 2 0 }$ and 30 ms network latency. In the plot we cannot see the Validity Check (online) time for RemiseBB, since it is very small (around 15 ms).

## 7 Conclusion

Remise enforces that only authorized clients can read from or write to the database. Importantly, the Remise servers perform access control checks without learning (i) the content of the messages written, (ii) which messages are being read, or (iii) any linkage between reads and writes.

![](images/802a6593609d4eb83b268d9210f36e47d2aacf71b6618c5727965155074c65ee.jpg)  
Figure 6: Comparing RemiseCC and PACL’s read authorization. In these experiments we do not have a latency set between the servers since the local computation dominates the cost.

## Ethical Considerations

Stakeholder Identification and Impacts. We structure this section as a stakeholder-based analysis, distinguishing between direct stakeholders—those who design, implement, or deploy Remise —and indirect stakeholders—those affected by systems built using Remise. Di rect stakeholders include the research team and organi zations that deploy anonymous communication services based on Remise. Indirect stakeholders include end users who rely on such systems for private and anonymous communication, journalists and whistleblowers who may depend on strong sender anonymity, regulators and auditors responsible for oversight, people who may be targeted by hateful rhetoric or online harassment by malicious actors, and adversaries who may attempt to disrupt or misuse anonymous communication infrastructures.

Research Team. This work involves no human sub jects, no physical experiments, and no collection of realworld private data. All evaluation is conducted using synthetic workloads and controlled experimental settings. We explicitly acknowledge and respect the intellectual contributions of all authors.

Service Providers and System Deployers. Organizations deploying Remise (e.g., operators of anonymous bulletin boards or private communication platforms) may benefit from improved efficiency, fast auditing, and strong authorization privacy. However, deployment requires careful engineering and cryptographic review. Miscon figuration or implementation errors could lead to service disruption, denial of access for honest users, or weakened anonymity guarantees. To mitigate these risks, we document system assumptions, protocol tradeoffs, and performance characteristics in detail.

End Users and Society. Beneficence. Remise is designed to strengthen privacy and freedom of expression by enabling authorized anonymous communication without revealing access patterns, sender–receiver rela tionships, or authorization state. The system is partic ularly relevant for high-risk users such as journalists, whistleblowers, activists, and individuals operating under surveillance. Respectfor Persons. We carefully cite prior work in anonymous communication, DPF-based systems, and DORAMs to ensure accurate attribution and to avoid misrepresentation of related techniques. The design of Remise explicitly avoids requiring users to reveal identities, long-term metadata, or sensitive per sonal information to the servers. Justice. The protocols underlying Remise rely only on standard cryptographic primitives and do not require specialized hardware or proprietary infrastructure. Our goal is to keep the core techniques accessible to researchers and system design ers worldwide, reducing barriers to entry and enabling independent verification and reuse.

Respect for Law and Public Interest. We recog nize that anonymous communication systems may raise concerns for regulators and law-enforcement agencies. Remise is designed to operate within the bounds of applicable law, assuming lawful deployment and governance by service providers. The system provides authorization controls that restrict which locations clients may read or write, balancing anonymous communication with serverenforced access control without requiring surveillance of honest users. Sometimes, malicious actors may conduct targeted harassment or spread hateful rhetoric. While these campaigns are not strictly unlawful they are nevertheless harmful, and a system like Remise could enable such abuse. Minority / non-normative populations are particularly at risk of this sort of abuse in online spaces.

Publication and Research Impact. This work contributes new techniques for combining DORAMs, authorization, and anonymous communication, and may influence future research on privacy-preserving systems. To reduce misuse or misinterpretation, we document key design decisions and tradeoffs, including the efficiency benefits of read-only and write-only memory instantiations, the assumption of at least one honest server, and the limitations of the threat model.

Potential Harms and Dual-Use Risks. We acknowledge that anonymous communication systems can be misused by malicious actors, including for spreading false or harmful information anonymously. Additionally, immature or unreviewed deployments of Remise could harm honest users by causing loss of availability or weakened anonymity guarantees. We therefore encourage responsible deployment, thorough security auditing, and appropriate legal and organizational oversight. We emphasize that Remise is a research prototype and that production deployments should be preceded by careful review.

Decision to Conduct and Publish. This research was initiated to improve the efficiency, robustness, and accountability of anonymous communication systems. We considered the dual-use nature of such systems and concluded that the benefits to privacy, free expression, and secure communication outweigh the potential risks when the system is deployed responsibly. The decision to publish followed internal review, correctness validation, and performance evaluation.

## Open Science

Our code is available via permanent link here: https: //zenodo.org/records/20438384. We provide all artifacts necessary to reproduce the evaluation, available at: Source Code: (i) Code to benchmark Remise, (ii) Distributed Point Function (DPF) primitives, (iii) Secret-sharing abstractions and MPC building blocks, and (iv) Asynchronous networking framework used for protocol execution. Benchmarking Infrastructure: (i) Scripts (and commands) used to reproduce numbers reported in Figures 3–6, (ii) Configuration file examples, so that anyone can write their config file and run any custom experiment, and (iii) Network-latency configuration scripts used to emulate the evaluation settings reported in the paper. Reported Metrics: (i) Through put and goodput, (ii) Evaluation, audit, and write latency, (iii) Communication bandwidth, and (iv) 95% confidence intervals.

## Acknowledgments

The authors used generative AI-based tools to revise the text, improve flow and correct any typos, grammatical errors, and awkward phrasing. The authors thank Anu sandhan National Research Foundation (ANRF) for their support. This research work was partially supported by a travel grant from Satish and Kamlesh Agarwal, Houston, TX, USA.

## References

[1] Sebastian Angel and Srinath Setty. Unobservable Communication over Fully Untrusted Infrastructure. In 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16), 2016.

[2] Ludovic Barman, Moshe Kol, David Lazar, Yossi Gilad, and Nickolai Zeldovich. Groove: Flexible Metadata-Private Messaging. In 16th USENIX Symposium on Operating Systems Design and Imple mentation (OSDI 22), 2022.

[3] Donald Beaver. Efficient Multiparty Protocols Using Circuit Randomization. In CRYPTO, pages 420–432, 1991.

[4] Elette Boyle, Niv Gilboa, and Yuval Ishai. Function Secret Sharing: Improvements and Extensions. In Proceedings of the 23rd ACM Conference on Computer and Communications Security (CCS), pages 1292–1303. ACM, 2016.

[5] David Chaum, Debajyoti Das, Farid Javani, Aniket Kate, Anna Krasnova, Joeri de Ruiter, and Alan T. Sherman. cMix: Mixing with Minimal Real-Time Asymmetric Cryptographic Operations. Cryptology ePrint Archive, Paper 2016/008, 2016.

[6] Raymond Cheng, William Scott, Elisaweta Masserova, Irene Zhang, Vipul Goyal, Thomas Anderson, Arvind Krishnamurthy, and Bryan Parno. Talek: Private Group Messaging with Hidden Access Patterns. In Proceedings of the 36th Annual Computer Security Applications Conference, ACSAC ’20, pages 84–99, 2020.

[7] Henry Corrigan-Gibbs, Dan Boneh, and David Maz ières. Riposte: An Anonymous Messaging System

Handling Millions of Users. In 2015 IEEE Symposium on Security and Privacy, SP 2015, San Jose, CA, USA, May 17-21, 2015, pages 321–338. IEEE Computer Society, 2015.

[8] Henry Corrigan-Gibbs and Bryan Ford. Dissent: accountable anonymous group messaging. In Ehab Al-Shaer, Angelos D. Keromytis, and Vitaly Shmatikov, editors, Proceedings ofthe 17th ACM Conference on Computer and Communications Security, CCS 2010, Chicago, Illinois, USA, October 4-8, 2010, pages 340–350. ACM, 2010.

[9] Henry Corrigan-Gibbs, David Isaac Wolinsky, and Bryan Ford. Proactively Accountable Anonymous Messaging in Verdict. In Samuel T. King, editor, Proceedings ofthe 22th USENIX Security Symposium, Washington, DC, USA, August 14-16, 2013, pages 147–162. USENIX Association, 2013.

[10] Cécile Delerablée, Pascal Paillier, and David Pointcheval. Fully Collusion Secure Dynamic Broadcast Encryption with Constant-Size Ciphertexts or Decryption Keys. In Pairing-Based Cryptography – Pairing 2007, volume 4575 of Lecture Notes in Computer Science, pages 39–59. Springer, 2007.

[11] Jack Doerner and Abhi Shelat. Scaling ORAM for Secure Computation. In CCS, pages 523–535. ACM, 2017.

[12] Wenliang Du and Mikhail J. Atallah. Protocols for Secure Remote Database Access with Approximate Matching. In E-Commerce Security and Privacy (Part II), Advances in Information Security, February 2001.

[13] Saba Eskandarian, Henry Corrigan-Gibbs, Matei Zaharia, and Dan Boneh. Express: Lowering the Cost of Metadata-hiding Communication with Cryptographic Privacy. In 30th USENIX Security Symposium, USENIX Security 2021, August 11- 13, 2021, pages 1775–1792. USENIX Association, 2021.

[14] Freedom of the Press Foundation. SecureDrop, 2025. Open-source whistleblower submission system. Latest release: 2.12.8 (May 8, 2025).

[15] Darya Kaviani, Deevashwer Rathee, Bhargav Annem, and Raluca Ada Popa. Myco: Unlocking Polylogarithmic Accesses in Metadata-Private Messaging. In 2025 IEEE Symposium on Security and Privacy (SP), pages 4419–4437, 2025.

[16] Albert Kwon, Henry Corrigan-Gibbs, Srinivas Devadas, and Bryan Ford. Atom: Horizontally Scaling Strong Anonymity. In Proceedings of the 33rd ACM Symposium on Operating Systems Principles (SOSP), pages 463–480. ACM, 2017.

[17] Albert Kwon, David Lazar, Srinivas Devadas, and Bryan Ford. Riffle: An Efficient Communication System With Strong Anonymity. Proc. Priv. Enhancing Technol., 2016(2), 2016.

[18] Albert Kwon, David Lu, and Srinivas Devadas. XRD: Scalable Messaging System with Cryptographic Privacy. In Ranjita Bhagwan and George Porter, editors, 17th USENIX Symposium on Networked Systems Design and Implementation, NSDI 2020, Santa Clara, CA, USA, February 25-27, 2020, pages 759–776. USENIX Association, 2020.

[19] Emily B. Laidlaw. Regulating Speech in Cyberspace: Gatekeepers, Human Rights and Corporate Responsibility. Cambridge University Press, 2015.

[20] Simon Langowski, Sacha Servan-Schreiber, and Srinivas Devadas. Trellis: Robust and Scalable Metadata-private Anonymous Broadcast. Cryptology ePrint Archive, Paper 2022/1548, 2022.

[21] David Lazar, Yossi Gilad, and Nickolai Zeldovich. Karaoke: Distributed Private Messaging Immune to Passive Traffic Analysis. In 13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18), pages 711–725, Carlsbad, CA, October 2018. USENIX Association.

[22] Zachary Newman, Sacha Servan-Schreiber, and Srinivas Devadas. Spectrum: High-bandwidth Anonymous Broadcast. In 19th USENIX Symposium on Networked Systems Design and Implementation (NSDI 22), 2022.

[23] Jason R. C. Nurse. Cybercrime and You: How Criminals Attack and the Human Factors That They Seek to Exploit. The Oxford Handbook of Cyberpsychology, pages 662–690, October 2018.

[24] Rasmus Pagh and Flemming Friche Rodler. Cuckoo hashing. Journal of Algorithms, 51(2):122–144, 2004.

[25] Rohan Ravi, Paritosh Shukla, and Adithya Vadapalli. Remise: Authorized anonymous communication systems. Cryptology ePrint Archive, Paper 2026/481, 2026.

[26] Len Sassaman, Bram Cohen, and Nick Mathewson. The pynchon gate: a secure method of pseudonymous mail retrieval. In Proceedings of the 2005 ACM Workshop on Privacy in the Electronic Society, WPES ’05, pages 1–9, New York, NY, USA, 2005. Association for Computing Machinery.

[27] Sajin Sasy and Ian Goldberg. SoK: Metadata-Protecting Communication Systems. Proc. Priv. Enhancing Technol., 2024(1):509–524, 2024.

[28] Sacha Servan-Schreiber, Simon Beyzerov, Eli Yablon, and Hyojae Park. Private Access Control for Function Secret Sharing. In 2023 IEEE Symposium on Security and Privacy (SP), 2023.

[29] Elkana Tovey, Jonathan Weiss, and Yossi Gilad. Distributed PIR: Scaling Private Messaging via the Users’ Machines. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, CCS ’24, pages 1967–1981, New York, NY, USA, 2024. Association for Computing Machinery.

[30] Adithya Vadapalli, Ryan Henry, and Ian Goldberg. Duoram: A Bandwidth-Efficient Distributed ORAM for 2- and 3-Party Computation. Cryptology ePrint Archive, Paper 2022/1747, 2022. https: //eprint.iacr.org/2022/1747.

[31] Adithya Vadapalli, Kyle Storrier, and Ryan Henry. Sabre: Sender-Anonymous Messaging with Fast Audits. In IEEE Symposium on Security and Privacy (SP), pages 1953–1970, 2022.

[32] Jelle van den Hooff, David Lazar, Matei Zaharia, and Nickolai Zeldovich. Vuvuzela: scalable private messaging resistant to traffic analysis. In Ethan L. Miller and Steven Hand, editors, Proceedings ofthe 25th Symposium on Operating Systems Principles, SOSP 2015, Monterey, CA, USA, October 4-7, 2015, pages 137–152. ACM, 2015.
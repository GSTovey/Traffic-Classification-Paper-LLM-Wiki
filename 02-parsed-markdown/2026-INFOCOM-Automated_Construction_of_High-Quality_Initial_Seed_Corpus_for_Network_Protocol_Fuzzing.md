# Automated Construction of High-Quality Initial Seed Corpus for Network Protocol Fuzzing

Weicheng Lin<sup>1,2</sup>, Laile Xi<sup>1,2</sup>, Yaowen Zheng<sup>1,2</sup>, Shenghao Lin<sup>1,2</sup>, Jiaxing Cheng<sup>1,2</sup>, Zhen Wang<sup>1,2</sup>, Shizhao Tian<sup>1,2</sup>, Yubo Li<sup>1,2</sup>, Tianheng Qu<sup>1,2</sup>, Hongsong Zhu<sup>1,2</sup> <sup>1</sup> Institute of Information Engineering, CAS, Beijing, China

<sup>2</sup> School of Cyber Security, University of Chinese Academy of Sciences, Beijing, China

{linweicheng, xilaile1998, zhengyaowen, linshenghao, chengjiaxing, wangzhen2022, tianshizhao, liyubo, qutianheng, zhuhongsong}@iie.ac.cn

Abstract—Network protocols are foundational to modern communication systems, making vulnerability discovery critical. Stateful protocol fuzzers have been widely adopted due to their high efficiency and low false positives. However, they heavily depend on the quality of the initial seed corpus. Unfortunately, these seeds are typically handcrafted, limited in quantity, and often exercise only shallow protocol behaviors.

In this paper, we present AutoSeeder, the first automated framework for constructing high-quality initial seed corpus tailored to stateful protocol fuzzing. Its core idea is to combine lightweight analysis of protocol source code with large language models to get state-handling logic and guide the generation of syntactically valid initial seeds that can reach deeper protocol states. Evaluation on twelve widely-used protocols shows that AutoSeeder can quickly construct a high-quality initial seed corpus, compared with four baselines, resulting in average improvements of 51.95% in state coverage, 152.6% in state transition coverage and 42.51% in code coverage. In addition, AutoSeeder is compatible with three state representation schemes to enhance the performance of the base fuzzers, including AFLNET, StateAFL, and NSFuzz. When integrated with AFLNET, AutoSeeder also discovers seven previously unknown bugs.

Index Terms—Network protocol, fuzzing, large language model, vulnerability discovery.

## I. INTRODUCTION

Network protocols define message formats and procedures that can be exchanged between network devices, ensuring coordination in communication systems. However, protocol implementations are often imperfect. Any flaw in protocol implementation can pose significant threats, particularly when exploited in publicly accessible servers, as exemplified by WannaCry [1] and Heartbleed [2]. The number of vulnerabilities in network servers continues to increase [3]. Therefore, identifying flaws in protocol implementations is essential to ensuring security and reliability of communication systems.

Fuzzing is a widely recognized technique for discovering vulnerabilities. It operates by automatically supplying numerous unexpected inputs to the system under test (SUT) to reveal abnormal behavior [4]. However, fuzzing network servers remains challenging due to their statefulness. The relationships between protocol states are intricate, where packets in a particular state not only define the internal state of protocol but also affects the processing of subsequent packets. State-ofthe-art state-aware fuzzers, whether generation-based [5] [6]or mutation-based [7] [8] [9] [10], address it by state models.

Compared to generation-based fuzzing, which relies on protocol specifications to generate inputs, mutation-based fuzzing operates directly on real network traffic without requiring protocol specifications. It introduces structural perturbations and boundary violations into the input space, making it more effective at producing unexpected inputs that trigger abnormal execution paths. Moreover, mutation-based fuzzing is compatible with coverage-guided feedback, enabling greybox fuzzing and increasing the likelihood of discovering vulnerabilities.

However, mutation-based fuzzing heavily relies on the quality of initial seed corpus, which directly determines the breadth and depth of exploration, especially for stateful protocols [4] [11] [12]. The lack of initial seed corpus, or the use of low-quality seeds, often results in wasted fuzzing effort and even failure. Existing fuzzers typically obtain initial seeds by manually collecting real-world network traffic [7] [8] [9] [10]. However, such seeds are often limited in both quantity and semantic depth, covering only shallow protocol states, and subsequent mutation struggles to generate inputs that trigger complex interactions or deep transitions, severely limiting fuzzing effectiveness. CHATAFL [10] attempts to mitigate this challenge by leveraging large language models (LLMs) to enrich initial seed corpus. Nevertheless, it still relies on the existence of initial seeds and performs poorly when initial seed quality is low. Moreover, its generality is limited to text-based protocols. In summary, automatically constructing high-quality initial seed corpus for protocol servers remains a fundamental challenge in stateful protocol greybox fuzzing [4] [8] [10] [13].

The successful application of LLMs to fuzzing has provided new insight into overcoming the persistent challenge of initial seed corpus construction [10] [14] [15]. These works demonstrate the potential of LLMs to understand protocol semantics and assist fuzzing, offering a viable path toward reducing reliance on human expertise. Although integrating LLMs with fuzzing represents a state-of-the-art approach, significant challenges persist in enabling LLMs to automatically generate high-quality initial seed corpus:

(C1) Insufficient knowledge of protocol implementations: Although LLMs are generally assumed to possess protocol-related knowledge by learning from a wide range of public specifications (e.g., RFCs), such knowledge remains insufficient to construct a high-quality initial seed corpus for fuzzing network protocols with strict format constraints and may even be misleading. This is because specifications are written in natural language, which often contains ambiguities and underspecified behaviors. These issues result in significant gaps between specifications and actual implementations, as well as between different implementations, particularly in the implementation of protocol state machines [16] [17] [18].

(C2) Lack of methodological support for initial seed corpus construction: The initial seed corpus construction for protocol fuzzing still relies heavily on tester protocol expertise and lacks systematic methodological guidance. We leverage LLMs to learn protocol state relationships from source code to guide seed generation. However, it remains challenging, as LLMs often assign inconsistent names to semantically equivalent states extracted from different code fragments. Moreover, when directly generating initial seeds, LLMs may violate syntactic integrity, especially for binary formats. Developing principled approaches that ensure syntactic integrity and enable deep protocol exploration remains an open problem.

(C3) Limited diversity in initial seed corpus: The effectiveness of mutation-based fuzzing is highly influenced by the quality of initial seed corpus, particularly their diversity. Techniques like AFL’s minset strategy, which selects a minimal yet diverse subset of seeds, have been shown to significantly improve mutation efficiency [19]. In contrast, manually constructed initial seed corpus tends to overrepresent typical interaction patterns, leading to high redundancy and low diversity, which constrain mutation to similar execution paths, weaken early feedback loops, and ultimately hinder both coverage growth and vulnerability discovery.

We propose AutoSeeder, the first automated framework designed to construct high-quality initial seed corpus tailored for stateful protocol fuzzing. AutoSeeder is broadly applicable across various protocol types, including both text-based and binary protocols, and can enhance a variety of stateful fuzzers based on response codes [7] [20], memory states [8], and state variables [9]. To address C1, AutoSeeder introduces retrieval-based relevant code extraction (Section III-A) to identify protocol state-related fragments from protocol source code. This allows LLMs to focus on state–related code, which is often scattered across the codebase, thereby capturing implementation details absent in specifications, improving analysis accuracy, and reducing token overhead. To address C2, AutoSeeder introduces lightweight LLM-driven state transition analysis (Section III-B), which extracts protocol states, methods, and transitions from the relevant code and instantiates them to guide initial seed construction. To improve the consistency and reliability of the extraction, we propose a unified namespace to standardize the output of LLMs. To ensure syntactic integrity, especially for binary formats, we use field-level templates to guide instantiation. This design ensures syntactic validity and effective coverage of deep protocol states while avoiding inefficient and error-prone manual efforts. To address C3, AutoSeeder introduces state-aware initial seed generation (Section III-C), which combines field-level instantiation with three complementary strategies for stepwise initial seed construction. It effectively overcomes the limitations of LLMs in directly generating initial seeds, especially for binary formats, and ensures the constructed initial seed corpus is highly diverse, minimally redundant, and mutation-effective.

We evaluate AutoSeeder on twelve widely-used open-source protocols across three state representation schemes and four baselines. Experimental results show that AutoSeeder constructs initial seed corpus significantly more efficiently than existing methods. When used for fuzzing, these seeds lead to an average improvement of 51.95%, 51.69% and 80.19% in state coverage, 152.6%, 62.04% and 186.11% in state transition coverage and 42.51%, 24.4% and 22.28% in code coverage over the base fuzzers (AFLNet, StateAFL and NSFuzz), demonstrating both effectiveness and generality. Furthermore, when integrated with AFLNet, AutoSeeder discovers seven new bugs, compared to only two found without AutoSeeder.

Our contributions are summarized as follows:

• We propose the first automated framework designed to construct high-quality initial seed corpus for stateful protocol fuzzing. It is broadly applicable to diverse protocol types and supports multiple state representation schemes.

• We present a method for guiding initial seed corpus construction based on lightweight source code analysis. Our approach extracts protocol implementation knowledge from source code and leverages LLMs to perform lightweight analysis of state transitions.

• We introduce three synergistic strategies to promote high diversity, low redundancy, and strong mutation potential in the constructed initial seed corpus.

• Evaluated on twelve real-world protocols across three state representation schemes and four baselines, AutoSeeder rapidly constructs a high-quality initial seed corpus and significantly enhances state coverage, state transition coverage, and code coverage, demonstrating both effectiveness and generality. Additionally, AutoSeeder discovered seven previously unknown bugs.

## II. BACKGROUND AND RELATED WORK

## A. Stateful network protocol fuzzing

The statefulness of network protocol servers poses unique challenges for fuzzing. To effectively fuzz servers, researchers construct state model to capture the structure of the protocol state space and guide the fuzzing. State model is typically represented as a graph consisting of a finite set of states and transitions, which concisely describe the key states of the protocol and the conditions under which transitions occur.

Early research on constructing state models relied heavily on domain-specific knowledge and extensive manual effort, requiring researchers to extract state transitions directly from protocol specifications. This labor-intensive process significantly constrained the scalability and effectiveness of fuzzing. Recent studies have introduced automated techniques to infer state models and systematically guide the fuzzing. These approaches require a well-defined representation of protocol states. Common strategies include modeling states based on server response codes [7], [20], memory states [8], or state variables [9] [21]. Such automation reduces manual overhead and, to some extent, enhances the effectiveness of fuzzing.

![](images/cbce111ee7bdda127c6caa6becbde949c0d0dc96d2441cd890cce11e29b33b0b.jpg)  
Fig. 1: Overview of AutoSeeder.

By leveraging the state model and monitoring the SUT’s responses, stateful fuzzers can infer the current protocol state and generate inputs that conform to the expected message format. These messages may be generated fully at random [22], via mutation of existing inputs [7] [23], or through generation based on predefined data models [5] [24]. Among these, mutation-based protocol fuzzers typically use a set of pre-recorded message sequences as initial seed corpus and achieve coverage by perturbing their structure and order. This approach underpins recent state-of-the-art fuzzers, including AFLNet [7], StateAFL [8], NSFuzz [9], and CHATAFL [10].

However, mutation-based protocol fuzzers remain heavily dependent on the quality of the initial seed corpus [4] [11] [12]. Existing corpus construction methods primarily rely on manually collecting network traffic, extracting client requests, and converting them into the default format expected by the fuzzer to serve as initial seeds [7] [8] [9] [10]. However, these seeds typically cover only simple interactive scenarios, making it difficult for subsequent mutations to generate highquality inputs. To improve seed quality, some studies have introduced expert-curated initial seed corpus to enhance the fuzzing of stateful protocols [25]. However, crafting them requires a deep understanding of the protocol and the ability to design inputs that trigger multiple state transitions—a costly and highly specialized task, particularly as new protocols continue to emerge. SVRM constructs a communication model by extracting representative messages from network traffic and generates the initial seed corpus accordingly [26]. However, it assumes that the traffic covers all request types of the protocol, which is difficult to achieve in practice. LLMs offer a new opportunity for seed corpus construction. Fuzz4All uses LLMs as an input generation engine, enabling the production of inputs for practically any language [14]. However, most seeds generated by Fuzz4All tend to be invalid due to neglecting the stateful nature of protocols. By contrast, CHATAFL attempts to utilize LLMs to enrich the initial seeds [10], but it remains reliant on initial seeds and performs badly when they are of poor quality. Moreover, limited by the ability of LLMs to directly generate initial seeds, particularly in binary formats, CHATAFL is only applicable to text-based protocols. In summary, existing approaches fall short in automating and ensuring the quality of initial seed corpus construction. A dedicated method for automatically constructing a high-quality initial seed corpus remains lacking, posing a key bottleneck to further improving stateful protocol fuzzing effectiveness.

## B. Large language models

LLMs have exhibited remarkable capabilities across a diverse set of tasks, including text generation [27], code synthesis [28], and conversations [29]. Trained on massive corpora, these models can perform task-specific reasoning without requiring additional hard-coded heuristics.

LLMs typically perform specific tasks either through finetuning [30] or prompting [31]. Compared to fine-tuning, prompting does not require updates to model parameters. The effectiveness of LLMs in understanding and completing a task largely depends on the richness of the information in the prompt [32]. Prompting enables the convenient incorporation of external knowledge via the context window, significantly improving performance on previously unseen tasks.

Pre-trained on billions of internet-scale samples, including a wide range of publicly available network protocol documentation, LLMs are considered to be able to understand protocol state machines and message sequences, making them wellsuited to improve protocol fuzzing. This potential has already been demonstrated by recent work [10]. Given the remarkable capabilities exhibited by LLMs, leveraging them to address the challenge of constructing high-quality initial seed corpus for protocol fuzzing represents a worthwhile research direction.

## III. FRAMEWORK AND KEY COMPONENTS

Fig. 1 presents the overview of AutoSeeder. AutoSeeder comprises three components: retrieval-based relevant code extraction, LLM-driven state transition analysis, and stateaware initial seed generation. AutoSeeder takes the source code of a network protocol implementation as input and performs relevant code extraction (Section III-A) to identify code fragments closely associated with the state processing of protocol. Next, AutoSeeder applies an LLM-driven state transition analysis (Section III-B) to obtain and instantiate protocol states, message methods, and their transitions from the extracted code fragments, guiding initial seed corpus construction. Based on the analysis results, AutoSeeder conducts state-aware initial seed generation (Section III-C), which combines three synergistic strategies: 1) Depth-guided layered seed generation ensures diversity and broad coverage of state transitions, 2) Method-aware redundancy suppression reduces redundancy within the initial seed corpus, and 3) LLM-guided semantic refinement enhances the semantic completeness and mutation potential of individual initial seeds. Together, these strategies produce a high-quality initial seed corpus that significantly improves the effectiveness of subsequent fuzzing.

(b) State extraction.  
![](images/99c9f6cfbfca580dead5d9cbef386e8ec506ca44ece4b58788d11c77db06f7de.jpg)  
Fig. 2: Multidimensional Query Set for Protocol State-relevant Fragments Retrieval.

![](images/83aa02ed54c618285cb1a0116dee7188dbaa3742e2cff3232795042e45617f64.jpg)  
(c) Method extraction. (d) Transition instantiation. (e) Transition completion.  
Fig. 3: Prompt templates for LLM-driven protocol state transition analysis.

## A. Retrieval-based Relevant Code Extraction.

Protocol implementations typically contain a wide range of complex components, including protocol parsing, network communication, security management, configuration, and interfaces. However, not all modules are closely related to protocol state processing. AutoSeeder employs the relevant code extraction to automatically locate code fragments that are tightly coupled with state processing, such as state variable definitions and handlers, state transition, and network event loops. These code fragments accurately reflect the protocol’s implementation details and runtime behaviors, helping to bridge the gap left by approaches that rely solely on documentation or traffic capture. Focusing on relevant code fragments rather than the entire codebase significantly improves the precision of the analysis and reduces processing overhead.

Code Slicing and Vectorization. AutoSeeder first uses TextLoader and LanguageAwareSplitter from LangChain [33] to automatically load and slice all source code, while preserving syntactic and structural integrity, including data structure and function. Subsequently, AutoSeeder uses the embedding model microsoft/unixcoder-base-nine [34] to encode code fragments into vectors, which are then stored for retrieval.

Vector-based Code Retrieval. Protocol implementation is typically large and structurally fragmented, with staterelated logic dispersed across multiple components. Simple approaches based on keyword or filename matching are often inadequate for capturing the multifaceted nature of state processing, including state definitions, transitions, and eventdriven behaviors, which often result in incomplete or biased retrieval results. Inspired by best practices in semantic retrieval [35] [36], we use vector-based code retrieval. Through iterative experimentation and comparative analysis, we design a set of systematic queries (Fig. 2) covering multiple aspects of protocol state to enable efficient retrieval of relevant codes.

Each query is encoded into a vector using the same embedding model. The cosine similarity is then computed between query and code fragment vectors to retrieve the top-k most relevant matches. This enables efficient extraction of code fragments that are semantically aligned with the target queries.

Post-processing. Post-processing mainly involves merging results from multiple queries and reorganizing the fragments for contextual coherence, to facilitate downstream analysis by the LLMs. Specifically, we first deduplicate identical fragments using hash-based comparison to avoid overlaps across queries. Then, to recover the original code context often disrupted by similarity-based ranking, we reorder fragments based on their source filenames and in-file positions. Finally, we reorganize the reordered fragments into blocks according to the LLM’s token limitations.

## B. LLM-driven State Transition Analysis

The goal of state transition analysis is to extract fine-grained knowledge and uncover undocumented behaviors from protocol implementations through code block–level analysis, and to construct abstract state transitions and instances for guiding initial seed generation. However, semantically equivalent variables with different names across code fragments introduce redundancy and hinder accurate transition extraction. To address this, we propose an LLM-driven code block analysis that constructs a unified namespace for state and method types, enabling iterative discovery of valid protocol state transitions along with their instances, as shown in Algorithm 1.

Algorithm 1 takes $S _ { \mathrm { c b } }$ as input and outputs $S _ { S } , \ S _ { M }$ and $S _ { S T }$ . It initializes $S _ { S }$ and $S _ { M }$ via prompt-based queries to the LLM to obtain common state and method names in the protocol, and specifies the initial state (line 1), using the prompt in Fig. 3a. These two sets form a unified namespace, which will be gradually expanded and refined during analysis to standardize the naming of states and methods. Next, the algorithm iteratively processes each code block (lines 2-16). In each iteration, it first extracts state names from the current block using the prompt in Fig. 3b (line 4). For any new state, the algorithm queries the LLM to check if its semantics align with an existing state in $S _ { S } .$ If so, it unifies the name; otherwise, it is added to $S _ { S }$ (lines 5-7). Method extraction follows the same procedure (lines 8-11) using the prompt in Fig. 3c. When analyzing state transitions, the algorithm not only follows the above procedure but also generates message instances that can trigger each identified transition (lines 12- 15), using the prompt in Fig. 3d. During instantiation, a fieldlevel template is extracted and the LLM is instructed to strictly follow it when generating message instances, ensuring semantic and syntactic validity, especially for binary protocols. After processing all blocks, the algorithm performs a final LLMbased review to validate the consistency and completeness of the discovered transitions, and attempts to complete missing potential transitions (line 17), using the prompt in Fig. 3e.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 1 State Transition Analysis
Input: $S_{cb}$: Set of related code blocks
Output: $S_S$: Set of protocol states
Output: $S_M$: Set of protocol methods
Output: $S_{ST}$: Set of protocol state transitions
1: $S_S$, $S_M \leftarrow$ INITIALIZATION()
2: for i from 0 to $S_{cb}$.number do
3: $S'_S \leftarrow \emptyset$; $S'_M \leftarrow \emptyset$; $S'_{ST} \leftarrow \emptyset$
4: $S'_S \leftarrow$ STATEEXTRACT($S_{cb}[i]$, $S_S$)
5: if $S'_S$ is not in $S_S$ then
6: STATEUPDATE($S_S$, $S'_S$)
7: end if
8: $S'_M \leftarrow$ METHODEXTRACT($S_{cb}[i]$, $S_M$)
9: if $S'_M$ is not in $S_M$ then
10: METHODUPDATE($S_M$, $S'_M$)
11: end if
12: $S'_{ST} \leftarrow$ TRANSITIONEXTRACTINSTANTIATE($S_{cb}[i]$, $S'_S$, $S'_M$)
13: if $S'_{ST}$ is not in $S_{ST}$ then
14: STATETRANSITIONUPDATE($S_{ST}$, $S'_{ST}$)
15: end if
16: end for
17: STATETRANSITIONCOMPLETION($S_S$, $S_M$, $S_{ST}$)
18: return $S_S$, $S_M$, $S_{ST}$
</div>

## C. State-aware Initial Seed Generation

We aim to construct a high-quality initial seed corpus that captures complex state transitions based on the extracted transition relations. While traversing all state transitions can theoretically produce a complete set of seeds, this naive approach often results in an overwhelming number of highly redundant initial seeds due to the presence of loops and deep transition paths, which offers little benefit to fuzzing. To ensure the overall quality and effectiveness of the initial seed corpus, we design three strategies that collectively enhance the diversity of the initial seed corpus, reduce redundancy, and improve the mutation potential of individual initial seeds.

<div class="mineru-algorithm" style="white-space: pre-wrap; font-family:monospace;">
Algorithm 2 State-Aware Initial Seed Generation
Input: $S_S$: State set obtained in the previous step
Input: $S_M$: Method set obtained in the previous step
Input: $S_{ST}$: State transition set obtained in the previous step
Output: Corpus: Initial seed corpus
1: global SHALLOW_DEPTH, MIDDLE_DEPTH, MAX_DEPTH
2: Corpus ← ∅
3: $S_I$ ← EXTRACTINITIALSTATE($S_S$, $S_{ST}$)
4: for i from 0 to $S_I$.number do
5: msgs ← ∅; depth ← 0; flag_ret ← false
6: CONSTRUCTION(Corpus, $S_{ST}$, $S_M$, $S_I[i]$, msgs, depth, flag_ret)
7: end for
8: return Corpus
Function CONSTRUCTION(Corpus, $S_{ST}$, $S_M$, current, msgs, depth, flag_ret):
9: $S_{st}$ ← SORTVALIDTRANSITIONS($S_{ST}$, current)
10: if depth ≥ MAX_DEPTH or $S_{st}$ = ∅ then
11: if REDUNDANCYSUPPRESSION(msgs, $S_M$, Corpus) then
12: seed ← SEMANTICREFINEMENT(msgs, $S_M$)
13: Corpus ← Corpus ∪ {seed}
14: end if
15: if depth ≥ MAX_DEPTH then
16: flag_ret ← true
17: end if
18: return
19: end if
20: number ← DEPTHGUIDE(depth)
21: for i from 0 to number do
22: APPEND(msgs, $S_{st}[i]$.instance)
23: RECORDUPDATE($S_{st}[i]$)
24: CONSTRUCTION(Corpus, $S_{ST}$, $S_M$, $S_{st}[i]$.next_state, msgs, depth + 1, flag_ret)
25: RECORDCLEAN($S_{st}[i]$)
26: if flag_ret and depth ≥ SHALLOW_DEPTH then
27: break
28: end if
29: end for
30: if flag_ret and depth &lt; SHALLOW_DEPTH then
31: flag_ret ← false
32: end if
33: return
</div>

Algorithm 2 shows the entire workflow. It takes $S _ { S } , S _ { M }$ and $S _ { S T }$ as input and output Corpus. The algorithm first identifies the initial states (line 3), and then recursively generates initial seeds that cover rich state transitions from each initial state (lines 4-7). The details are implemented in the construction function, which mainly applies the following three strategies.

Depth-Guided Layered Seed Generation: It is used to enhance the diversity of corpus. We use SHALLOW DEPTH and MIDDLE DEPTH to distinguish three layers (line 1), and design differentiated traversal strategies across layers to achieve diverse initial seed generation. Specifically, we first filter the valid transitions of the current state by limiting the number of times each transition can be visited. Then, we compute the frequency of each transition’s corresponding method in the request message sequence msgs, and sort transitions in ascending order of frequency to obtain the $S _ { s t }$ (line 9). The algorithm recursively explores all valid transitions for shallow states, the top-3 for intermediate states, and only the first for deep states (line 20). When a transition is visited, its instance is appended to the msgs, and its visit record will be incremented by one (lines 22-23). The traversal then proceeds recursively (line 24), and cleans up the visit records when backtracking (line 25). A maximum recursion depth MAX DEPTH is defined (line 1). When a leaf node is reached or the depth exceeds MAX DEPTH, the msgs is recorded as a candidate initial seed (line 10). If the depth exceeds MAX DEPTH, the algorithm backtracks to the nearest shallow state and resumes traversal (lines 15-17), skipping intermediate unvisited paths (lines 26-32). This design avoids generating excessive, structurally redundant, and overly long seed candidates.

Method-Aware Redundancy Suppression: It aims to reduce redundancy within the initial seed corpus. Although diversity is already considered during candidate generation, further filtering is needed to select more representative candidates. We apply two heuristic rules (line 11):

• Method Diversity. We compute the ratio of method types contained in each candidate to the total number of method types in $S _ { M }$ . Candidates below the predefined richness threshold (e.g., 30%) are all removed.

• Method Sequence Similarity. We measure similarity between method sequences of candidates using the longest common subsequence algorithm. For any pair exceeding a similarity threshold (e.g., 80%), only one is retained.

LLM-Guided Semantic Refinement: To further enhance the mutation potential of the candidate, we leverage LLMs to understand message sequences to fine-tune the local structure of candidate to maximize the overall quality of the corpus. Specifically, for each candidate, we identify the missing methods by comparing $S _ { M }$ and guide the LLM to try to reasonably insert them into the candidates. The LLM will decide whether to insert, the number and location of insertions based on deep reasoning. The prompt is shown in Fig. 4. If the candidate is already sufficiently complete, LLM may choose not to modify it. Moreover, each candidate is refined at most once to preserve the overall size of the initial seed corpus.

![](images/97fbf54b6ada962bebbf7b574654ac1d20ea45573644c6455fd95241dc26c686.jpg)  
Fig. 4: Prompt used in LLM-guided semantic refinement.

## IV. EVALUATION

We have implemented a prototype of AutoSeeder, which consists of approximately 4500 lines of C/C++ code and about 400 lines of Python code. We use ChatGPT-4o-mini [37] in Section III-B and III-C, as well as across all baselines in the evaluation. Following best practices [38] [39] [10], we set the temperature to 0.5 to ensure precise and fact-based responses. All LLMs used in AutoSeeder can be replaced with similar models without modifying the overall architecture. To evaluate AutoSeeder, we conducted a set of experiments designed to answer the following questions:

RQ1 Efficiency: Can AutoSeeder, based on the designed construction guidance mechanism, improve the efficiency of initial seed corpus construction for fuzzing?

RQ2 Effectiveness: Can AutoSeeder improve the coverage performance of the base fuzzers?

RQ3 Generality: Can AutoSeeder effectively generalize to different protocol types and state representation schemes?

RQ4 Ablation: How does each strategy designed in the section III-C impact overall performance?

RQ5 Real-World Bugs Finding: Can AutoSeeder enhance the base fuzzer to discover bugs in real-world protocols?

## A. Experimental setup

Table I presents the information of twelve subjects used for the evaluation. Our benchmark consists of ten protocol implementations from the ProFuzzBench [25] that are widely adopted in previous studies and two emerging protocol implementations that lack expert-curated initial seeds, reflecting more realistic fuzzing scenarios. These targets cover a diverse set of protocol types, including both text and binary protocols, and span a wide range of real-world applications such as media streaming, messaging, and file transfer. To ensure the reliability of fuzzing evaluation, we applied necessary patches (e.g., derandomization) to each protocol implementation.

TABLE I: Detailed information about our subjects.

<table><tr><td>Subject</td><td>Protocol</td><td>#LOC</td><td>Type</td><td>Version</td></tr><tr><td>LightFTP</td><td>FTP</td><td>4.4k</td><td>Text</td><td>5980ea1</td></tr><tr><td>Bftpd</td><td>FTP</td><td>4.7k</td><td>Text</td><td>5.7</td></tr><tr><td>PureFTPD</td><td>FTP</td><td>29k</td><td>Text</td><td>c21b45f</td></tr><tr><td>ProFTPD</td><td>FTP</td><td>242k</td><td>Text</td><td>4017eff8</td></tr><tr><td>Forked-daapd</td><td>DAAP</td><td>109k</td><td>Text</td><td>2ca10d9</td></tr><tr><td>Live555</td><td>RTSP</td><td>57k</td><td>Text</td><td>a0eb8f9</td></tr><tr><td>Kamailio</td><td>SIP</td><td>939k</td><td>Text</td><td>2648eb3</td></tr><tr><td>Exim</td><td>SMTP</td><td>118k</td><td>Text</td><td>38903fb</td></tr><tr><td>Dcmtk</td><td>DICOM</td><td>576k</td><td>Binary</td><td>7f8564c</td></tr><tr><td>TinyDTLS</td><td>DTLS</td><td>10.8k</td><td>Binary</td><td>06995d4</td></tr><tr><td>Ngtcp2</td><td>QUIC</td><td>186.3k</td><td>Binary</td><td>e2372a8</td></tr><tr><td>Google quiche</td><td>QUIC</td><td>33k</td><td>Binary</td><td>149b7e62</td></tr></table>

TABLE II: Efficiency of AutoSeeder and baselines in constructing the initial seed corpus.

<table><tr><td rowspan="2">Subject</td><td colspan="4">Manual construction</td><td colspan="4">CHATAFL*</td><td colspan="4">Fuzz4All</td><td colspan="4">AutoSeeder</td></tr><tr><td>Time (m)</td><td>#Tokens</td><td> $R_v$ </td><td> $V_{eff}$ </td><td>Time (m)</td><td>#Tokens</td><td> $R_v$ </td><td> $V_{eff}$ </td><td>Time (m)</td><td>#Tokens</td><td> $R_v$ </td><td> $V_{eff}$ </td><td>Time (m)</td><td>#Tokens</td><td> $R_v$ </td><td> $V_{eff}$ </td></tr><tr><td>LightFTP</td><td>&gt;480</td><td>0</td><td>4/4</td><td>&lt;0.008</td><td>31.7</td><td>148,314</td><td>181/184</td><td>5.7</td><td>54.5</td><td>13,011,210</td><td>169/601</td><td>3.1</td><td>54.5</td><td>1,289,545</td><td>393/393</td><td>7.2</td></tr><tr><td>Bftpd</td><td>&gt;480</td><td>0</td><td>4/4</td><td>&lt;0.008</td><td>33.5</td><td>148,861</td><td>181/184</td><td>5.4</td><td>61.1</td><td>13,969,421</td><td>182/387</td><td>3</td><td>61.1</td><td>1,649,452</td><td>420/420</td><td>6.9</td></tr><tr><td>Pure-FTPD</td><td>&gt;480</td><td>0</td><td>4/4</td><td>&lt;0.008</td><td>28.3</td><td>132,489</td><td>166/166</td><td>5.9</td><td>25.2</td><td>5,870,295</td><td>29/74</td><td>1.2</td><td>25.2</td><td>4,349,325</td><td>446/447</td><td>17.7</td></tr><tr><td>ProFTPD</td><td>&gt;480</td><td>0</td><td>4/4</td><td>&lt;0.008</td><td>31.3</td><td>148,550</td><td>184/184</td><td>5.9</td><td>79.4</td><td>18,686,823</td><td>153/561</td><td>1.9</td><td>79.4</td><td>7,508,672</td><td>589/602</td><td>7.4</td></tr><tr><td>Forked-daapd</td><td>&gt;600</td><td>0</td><td>2/2</td><td>&lt;0.004</td><td>37.2</td><td>662,556</td><td>53/92</td><td>1.4</td><td>23.3</td><td>5,788,431</td><td>27/104</td><td>1.2</td><td>23.3</td><td>4,317,375</td><td>57/59</td><td>2.4</td></tr><tr><td>Live555</td><td>&gt;480</td><td>0</td><td>6/6</td><td>&lt;0.0125</td><td>32.6</td><td>431,526</td><td>109/124</td><td>3.3</td><td>148.3</td><td>35,906,612</td><td>54/1073</td><td>0.4</td><td>148.3</td><td>7,866,581</td><td>576/594</td><td>3.9</td></tr><tr><td>Kamailio</td><td>&gt;600</td><td>0</td><td>2/2</td><td>&lt;0.004</td><td>26.3</td><td>218,409</td><td>112/158</td><td>4.3</td><td>180.3</td><td>36,958,006</td><td>63/481</td><td>0.3</td><td>180.3</td><td>6,849,729</td><td>517/527</td><td>2.9</td></tr><tr><td>Exim</td><td>&gt;600</td><td>0</td><td>2/2</td><td>&lt;0.004</td><td>40.3</td><td>329,041</td><td>233/242</td><td>5.8</td><td>48.1</td><td>9,853,532</td><td>28/176</td><td>0.6</td><td>48.1</td><td>11,648,248</td><td>520/520</td><td>10.8</td></tr><tr><td>Dcmtk</td><td>&gt;600</td><td>0</td><td>2/2</td><td>&lt;0.004</td><td>×</td><td>×</td><td>×</td><td>×</td><td>262.9</td><td>56,076,923</td><td>16/1080</td><td>0.06</td><td>262.9</td><td>34,834,843</td><td>581/606</td><td>2.2</td></tr><tr><td>TinyDTLS</td><td>&gt;600</td><td>0</td><td>2/2</td><td>&lt;0.004</td><td>×</td><td>×</td><td>×</td><td>×</td><td>11.0</td><td>22,532,212</td><td>3/31</td><td>0.3</td><td>11.0</td><td>1,981,663</td><td>15/15</td><td>1.4</td></tr><tr><td>Ngtcp2</td><td>&gt;600</td><td>0</td><td>1/1</td><td>&lt;0.002</td><td>×</td><td>×</td><td>×</td><td>×</td><td>224.5</td><td>46,018,679</td><td>12/983</td><td>0.05</td><td>224.5</td><td>11,517,653</td><td>511/525</td><td>2.3</td></tr><tr><td>Google quiche</td><td>&gt;600</td><td>0</td><td>1/1</td><td>&lt;0.002</td><td>×</td><td>×</td><td>×</td><td>×</td><td>165.6</td><td>34,270,081</td><td>69/871</td><td>0.4</td><td>165.6</td><td>10,275,611</td><td>355/357</td><td>2.1</td></tr></table>

To enable a fair comparison, we selected four representative initial seed corpus construction approaches as baselines:

• Manual construction: Existing mutation-based fuzzers typically assume manually construct seeds as the default input. It involves capturing network traffic between clients and servers, and extracting client-side requests in the format expected by the fuzzer to serve as initial seeds.

• Seed Reuse from ProFuzzBench [25]: These seeds have been empirically validated, and thus often yield better mutation effectiveness compared to manually construct seeds. However, their generality is limited to a small set of well-studied protocols, as the majority of protocols still lack such high-quality, publicly available seeds.

• Fuzz4All: Fuzz4All leverages LLMs as an engine for input generation, allowing it to produce diverse and realistic inputs for any practically relevant language.

• CHATAFL<sup>∗</sup>: Although CHATAFL still relies on the existence of initial seeds, it provides a novel approach to enrich initial seed corpus. To comprehensively evaluate AutoSeeder, we combine it with seed reuse as a baseline.

To evaluate the generality of AutoSeeder across different state representation schemes, we selected three fuzzers as the base fuzzers, each corresponding to a representative state representation scheme, including response-code based (AFLNet [7]), memory-state based (StateAFL [8]), and statevariable based (NSFuzz [9]), which cover the main methods.

All experiments were conducted on the same host machine running Ubuntu 18.04 (64-bit), equipped with an Intel(R) Xeon(R) Gold 5120 CPU @ 2.20GHz, 125 GB RAM, a NVIDIA Tesla V100 GPU, and a 1 TB HDD. We set up each target service with each fuzzer in separate docker containers and used the same resource for evaluation. Each fuzzing run lasted 24 hours, with results collected both at the end of initial seed execution (P1) and after the full 24-hour period (P2). To mitigate randomness, each experiment was repeated 10 times, resulting in a total of 31,200 CPU hours of fuzzing evaluation.

## B. RQ1: Efficiency of AutoSeeder

We evaluate efficiency using four metrics:

• T ime : Time spent on constructing the initial seed corpus.

• Tokens : Tokens used by LLMs in corpus construction.

$R _ { v }$ : Ratio of valid initial seeds to the total. A valid seed

$V _ { e f f }$ : The number of valid seeds generated per minute.

To evaluate the efficiency of manual construction, we conducted a small-scale study with ten cybersecurity Ph.D. students, measuring their average performance in conducting initial seeds. The recorded Time covers key steps including protocol comprehension, client configuration, payload preparation, traffic capture, and seed crafting, excluding server-side configuration shared across all methods.

Since seed reuse accumulates over an unknown time span, which inevitably takes longer than manual construction and has already been extensively optimized through prior fuzzing, we do not evaluate its efficiency.

Although CHATAFL<sup>∗</sup> relies on initial seeds, we report Time only for the seed enrichment, excluding human effort.

Table II presents the efficiency comparison between AutoSeeder and the baselines. Compared to manual construction, AutoSeeder shows clear advantages in Time and $V _ { e f f } .$ Compared to CHATAFL<sup>∗</sup>, AutoSeeder eliminates the reliance on manual efforts, supports more protocol types, and improves $V _ { e f f }$ by 57.6% on average. Compared to Fuzz4All, AutoSeeder achieves over 5× higher $V _ { e f f }$ while using 65.2% fewer T okens under the same time. Overall, manual approaches and documentation-driven LLM methods often struggle due to limited protocol understanding, whereas AutoSeeder’s source-code-centric design delivers significantly better performance.

## C. RQ2: Effectiveness of AutoSeeder

We evaluate effectiveness using state space coverage and code coverage. Using AFLNET as the base fuzzer, we report percentage improvements over baselines in both P1 and P2.

State space coverage. We use the number of discovered states and transitions as metrics to evaluate state space coverage. Table III compares AutoSeeder with the baselines. Across all subjects in both phases (P1 and P2), AutoSeeder achieves the highest state space coverage. On average, in P1, AutoSeeder discovers 197.78% more states and 1316.54% more transitions than manual construction, 129.63% / 826.41% more than seed reuse, 22.58% / 47.51% more than CHATAFL<sup>∗</sup>, and 152.83% / 608.27% more than Fuzz4All. In P2, AutoSeeder discovers 56.16% more states and 172.69% more transitions than manual construction, 22.73% / 80.85% more than seed reuse, 11.31% / 25.32% more than CHATAFL<sup>∗</sup>, and 117.61% / 331.55% more than Fuzz4All.

TABLE III: Average number of states and state transitions for AutoSeeder and the baselines Manual Collection, Seed Reuse, CHATAFL<sup>∗</sup> and Fuzz4All in 10 runs on AFLNet of 24 hours.

<table><tr><td rowspan="3">Subject</td><td colspan="4">Manual construction</td><td colspan="4">Seed Reuse</td><td colspan="4">CHATAFL*</td><td colspan="4">Fuzz4All</td><td colspan="4">AutoSeeder</td></tr><tr><td colspan="2">state</td><td colspan="2">tran.</td><td colspan="2">state</td><td colspan="2">tran.</td><td colspan="2">state</td><td colspan="2">tran.</td><td colspan="2">state</td><td colspan="2">tran.</td><td colspan="2">state</td><td colspan="2">tran.</td></tr><tr><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td></tr><tr><td>LightFTP</td><td>6.00</td><td>12.00</td><td>6.00</td><td>46.80</td><td>7.00</td><td>24.30</td><td>7.00</td><td>154.10</td><td>18.00</td><td>24.10</td><td>97.00</td><td>203.90</td><td>7.00</td><td>13.00</td><td>20.00</td><td>44.40</td><td>20.00</td><td>24.50</td><td>107.00</td><td>215.60</td></tr><tr><td>Bftpd</td><td>10.00</td><td>21.60</td><td>13.00</td><td>106.10</td><td>13.00</td><td>24.60</td><td>20.00</td><td>174.80</td><td>20.00</td><td>24.30</td><td>132.00</td><td>214.20</td><td>11.00</td><td>24.00</td><td>27.00</td><td>160.30</td><td>21.00</td><td>24.40</td><td>158.00</td><td>237.70</td></tr><tr><td>Pure-FTPD</td><td>3.00</td><td>16.90</td><td>3.00</td><td>70.50</td><td>3.00</td><td>23.30</td><td>3.00</td><td>104.30</td><td>18.00</td><td>30.10</td><td>100.00</td><td>306.10</td><td>7.00</td><td>13.00</td><td>13.00</td><td>47.90</td><td>25.00</td><td>31.30</td><td>212.00</td><td>449.00</td></tr><tr><td>ProFTPD</td><td>6.00</td><td>20.70</td><td>6.00</td><td>125.80</td><td>12.00</td><td>22.70</td><td>21.00</td><td>160.10</td><td>18.00</td><td>25.30</td><td>108.00</td><td>235.60</td><td>10.00</td><td>15.00</td><td>27.00</td><td>59.10</td><td>23.00</td><td>30.60</td><td>167.00</td><td>335.70</td></tr><tr><td>forked-daap</td><td>2.00</td><td>8.00</td><td>2.00</td><td>15.00</td><td>3.00</td><td>8.00</td><td>4.00</td><td>21.60</td><td>4.00</td><td>8.00</td><td>8.00</td><td>21.90</td><td>2.00</td><td>2.00</td><td>1.00</td><td>1.00</td><td>4.00</td><td>13.00</td><td>10.00</td><td>29.30</td></tr><tr><td>Live555</td><td>2.00</td><td>11.00</td><td>2.00</td><td>56.40</td><td>5.00</td><td>11.00</td><td>4.00</td><td>76.30</td><td>7.00</td><td>12.00</td><td>13.00</td><td>87.40</td><td>4.00</td><td>6.00</td><td>5.00</td><td>27.30</td><td>8.00</td><td>13.00</td><td>15.00</td><td>95.30</td></tr><tr><td>Kamailio</td><td>4.00</td><td>11.00</td><td>9.00</td><td>97.30</td><td>5.00</td><td>13.00</td><td>11.00</td><td>104.20</td><td>5.00</td><td>15.00</td><td>16.00</td><td>109.70</td><td>2.00</td><td>2.00</td><td>3.00</td><td>3.00</td><td>7.00</td><td>16.10</td><td>29.00</td><td>124.50</td></tr><tr><td>Exim</td><td>2.00</td><td>9.00</td><td>2.00</td><td>31.40</td><td>2.00</td><td>12.00</td><td>4.00</td><td>56.10</td><td>3.00</td><td>15.00</td><td>8.00</td><td>64.70</td><td>2.00</td><td>6.00</td><td>2.00</td><td>21.70</td><td>6.00</td><td>18.30</td><td>13.00</td><td>71.20</td></tr><tr><td>Dcmtk</td><td>1.00</td><td>3.00</td><td>1.00</td><td>3.00</td><td>2.00</td><td>4.00</td><td>1.00</td><td>3.00</td><td>×</td><td>×</td><td>×</td><td>×</td><td>2.00</td><td>4.00</td><td>1.00</td><td>3.00</td><td>3.00</td><td>4.00</td><td>2.00</td><td>3.00</td></tr><tr><td>TinyDTLS</td><td>2.00</td><td>7.00</td><td>2.00</td><td>19.10</td><td>2.00</td><td>8.00</td><td>3.00</td><td>22.30</td><td>×</td><td>×</td><td>×</td><td>×</td><td>2.00</td><td>2.00</td><td>2.00</td><td>2.00</td><td>7.00</td><td>10.00</td><td>9.60</td><td>24.40</td></tr><tr><td>Ngtcp2</td><td>3.00</td><td>4.00</td><td>2.00</td><td>10.00</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>2.00</td><td>2.00</td><td>2.00</td><td>2.00</td><td>5.00</td><td>7.00</td><td>6.00</td><td>13.00</td></tr><tr><td>Google_quiche</td><td>4.00</td><td>4.00</td><td>4.00</td><td>10.00</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>2.00</td><td>3.00</td><td>1.00</td><td>2.00</td><td>5.00</td><td>8.00</td><td>8.00</td><td>14.00</td></tr></table>

TABLE IV: Average code branch coverage of AutoSeeder and the baselines in 10 runs on AFLNet of 24 hours.

<table><tr><td>Subject</td><td>Manual construction</td><td>Seed Reuse</td><td>CHATAFL*</td><td>Fuzz4All</td><td>AutoSeeder</td></tr><tr><td>LightFTP</td><td>162.50</td><td>387.10</td><td>391.70</td><td>162.70</td><td>410.90</td></tr><tr><td>Bftpd</td><td>465.30</td><td>476.60</td><td>472.40</td><td>471.90</td><td>494.80</td></tr><tr><td>Pure-FTPD</td><td>812.10</td><td>1056.80</td><td>1091.90</td><td>332.30</td><td>1149.70</td></tr><tr><td>ProFTPD</td><td>4846.90</td><td>5039.40</td><td>5067.60</td><td>3234.70</td><td>5498.80</td></tr><tr><td>forked-daap</td><td>1797.10</td><td>2410.50</td><td>2479.60</td><td>707.40</td><td>2577.10</td></tr><tr><td>Live555</td><td>1735.80</td><td>2861.90</td><td>2886.40</td><td>1047.90</td><td>2931.60</td></tr><tr><td>Kamailio</td><td>9207.80</td><td>9404.30</td><td>9634.60</td><td>5126.10</td><td>10604.70</td></tr><tr><td>Exim</td><td>2919.10</td><td>3579.20</td><td>3675.10</td><td>1054.60</td><td>3711.30</td></tr><tr><td>Dcmtk</td><td>2087.90</td><td>2492.50</td><td> $\times$ </td><td>2063.60</td><td>3058.10</td></tr><tr><td>TinyDTLS</td><td>413.70</td><td>470.10</td><td> $\times$ </td><td>345.80</td><td>577.40</td></tr><tr><td>Ngtcp2</td><td>2731.90</td><td> $\times$ </td><td> $\times$ </td><td>1751.30</td><td>3545.20</td></tr><tr><td>Google quiche</td><td>7044.50</td><td> $\times$ </td><td> $\times$ </td><td>2973.10</td><td>9017.90</td></tr></table>

Code coverage. We use branch coverage as a metric to evaluate code coverage. Table IV reports the coverage results after 24 hours, comparing AutoSeeder with the baseline methods. AutoSeeder improves code coverage by 27.33% over the manual construction, 10.06% over seed reuse, 6.54% over CHATAFL<sup>∗</sup>, and 126.13% over Fuzz4All.

Overall, AutoSeeder consistently outperforms all baselines across all evaluation metrics, demonstrating its effectiveness. The results of P1 show that the initial seeds generated by AutoSeeder capture diverse state transitions, significantly enhancing the early feedback loop of fuzzing and improving fuzzing efficiency. The P2 results further indicate that these seeds not only increase early-stage performance but also guide fuzzing to explore a broader test space over time. These findings suggest that AutoSeeder, while maintaining a high level of automation, leverages its source code analysis-driven initial seed corpus generation mechanism to uncover protocol implementation details and produce high-quality initial seeds with strong mutation potential.

## D. RQ3: Generality of AutoSeeder

We use the number of supported protocol types and the number of compatible state representation schemes as metrics to assess generality.

Protocol type. To evaluate protocol generality, we evaluated AutoSeeder on 12 protocols (as listed in Table I), covering both text-based and binary protocols. The results of the above experiments demonstrate that AutoSeeder generalizes well across diverse protocol types.

State representation. To evaluate compatibility with state representation, we evaluate three representation schemes mentioned above. As shown in Table V, compared to manual construction, AutoSeeder significantly enhances the base fuzzers in both P1 and P2. On average, during P2, AutoSeeder enables StateAFL to discover 51.69% more states, 62.04% more transitions, and achieves 24.40% higher code coverage. For NSFuzz, the improvements are 80.19%, 186.11%, and 22.28%, respectively.

Overall, AutoSeeder exhibits strong performance across diverse protocol types and multiple state representation schemes. These results indicate that AutoSeeder effectively captures the concrete semantics of protocol state machines from implementation by relevant code extraction, which avoids costly manual analysis. Furthermore, combined with its guided construction mechanism and generation strategy, AutoSeeder enhances the LLM’s capacity to manipulate message sequences, which enables the embedding of the actual semantics of protocol implementation into seed structure.

## E. RQ4: Ablation Study

AutoSeeder employs three generation strategies to construct high-quality initial seed corpus.

• S1: Depth-Guided Layered Seed Generation

• S2: Method-Aware Redundancy Suppression

• S3: LLM-Guided Semantic Refinement

To evaluate the contribution of each strategy, we conducted an ablation study by incrementally disabling each component.

• AutoSeeder: All three strategies are enabled.

• AutoSeeder-v2: Strategy S3 is disabled.

• AutoSeeder-v1: Both strategies S2 and S3 are disabled.

• AutoSeeder-v0: All strategies S1, S2, and S3 are disabled, directly use depth-first traversal.

Table VI presents the number of initial seeds generated by the above four tools and the corresponding 24-hour fuzzing results with AFLNet as the base fuzzer. Overall, all strategies contribute to improving the quality of the initial seed corpus.

Strategy S1. Overall, S1 significantly reduces the number of generated initial seeds. An excessive number of initial seeds can cause the fuzzer to spend substantial time in the dry run, severely slowing down the fuzzing. This is particularly evident in protocols like LightFTP, where the initial seed corpus exceeds five million and results in reduced coverage. For this situation, S1 proves especially effective, reducing the corpus size by more than 50× compared to AutoSeeder-v0, and does not harm fuzzing effectiveness—in fact, both state space and code coverage are improved in most cases.

TABLE V: Average number of states, state transitions, and code branches covered by StateAFL and NSFuzz using initial seed corpus constructed by AutoSeeder and manual construction.

<table><tr><td rowspan="3">Subject</td><td colspan="5">StateAFL: Manual construction</td><td colspan="5">StateAFL: AutoSeeder</td><td colspan="5">NSFuzz: Manual construction</td><td colspan="5">NSFuzz: AutoSeeder</td></tr><tr><td colspan="2">State</td><td colspan="2">Tran.</td><td>Code</td><td colspan="2">State</td><td colspan="2">Tran.</td><td>Code</td><td colspan="2">State</td><td colspan="2">Tran.</td><td>Code</td><td colspan="2">State</td><td colspan="2">Tran.</td><td>Code</td></tr><tr><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P2</td><td>P1</td><td>P2</td><td>P1</td><td>P2</td><td>P2</td></tr><tr><td>LightFTP</td><td>17.00</td><td>42.30</td><td>9.00</td><td>239.70</td><td>159.20</td><td>33.00</td><td>65.20</td><td>189.00</td><td>397.10</td><td>354.60</td><td>2.00</td><td>2.00</td><td>3.00</td><td>3.00</td><td>164.00</td><td>3.00</td><td>5.00</td><td>6.00</td><td>13.90</td><td>391.10</td></tr><tr><td>Bftpd</td><td>2.00</td><td>3.00</td><td>3.00</td><td>6.00</td><td>443.10</td><td>3.00</td><td>4.00</td><td>6.00</td><td>10.50</td><td>472.70</td><td>4.00</td><td>13.00</td><td>6.00</td><td>51.50</td><td>471.40</td><td>13.00</td><td>15.00</td><td>38.00</td><td>91.10</td><td>513.80</td></tr><tr><td>Pure-FTPD</td><td>2.00</td><td>3.00</td><td>2.00</td><td>4.00</td><td>786.00</td><td>2.00</td><td>4.00</td><td>3.00</td><td>5.00</td><td>925.00</td><td>2.00</td><td>5.00</td><td>3.00</td><td>9.10</td><td>820.10</td><td>5.00</td><td>6.25</td><td>14.00</td><td>20.80</td><td>1207.30</td></tr><tr><td>ProFTPD</td><td>6.00</td><td>12.00</td><td>7.00</td><td>83.50</td><td>3864.80</td><td>14.00</td><td>23.00</td><td>82.00</td><td>151.40</td><td>4599.90</td><td>5.00</td><td>14.30</td><td>8.00</td><td>60.20</td><td>4827.70</td><td>26.00</td><td>40.50</td><td>106.00</td><td>263.20</td><td>5380.60</td></tr><tr><td>forked-daap</td><td>2.00</td><td>4.00</td><td>2.00</td><td>5.00</td><td>1673.70</td><td>4.00</td><td>6.00</td><td>6.00</td><td>9.00</td><td>2808.90</td><td>2.00</td><td>2.00</td><td>2.00</td><td>2.00</td><td>1738.50</td><td>4.00</td><td>10.00</td><td>7.00</td><td>36.00</td><td>2770.40</td></tr><tr><td>Live555</td><td>5.00</td><td>16.00</td><td>9.00</td><td>129.60</td><td>1739.60</td><td>43.00</td><td>24.40</td><td>92.00</td><td>181.50</td><td>2891.00</td><td>2.00</td><td>11.60</td><td>2.00</td><td>24.10</td><td>2054.70</td><td>5.00</td><td>13.00</td><td>11.00</td><td>55.00</td><td>3044.00</td></tr><tr><td>Kamailio</td><td>2.00</td><td>2.00</td><td>3.00</td><td>3.00</td><td>8831.00</td><td>3.00</td><td>3.00</td><td>4.00</td><td>4.00</td><td>9608.20</td><td>2.00</td><td>4.00</td><td>3.00</td><td>12.00</td><td>9014.90</td><td>4.00</td><td>5.00</td><td>6.00</td><td>15.00</td><td>10731.60</td></tr><tr><td>Exim</td><td>4.00</td><td>6.00</td><td>7.00</td><td>26.00</td><td>3409.40</td><td>6.00</td><td>9.80</td><td>17.00</td><td>35.30</td><td>3972.70</td><td>2.00</td><td>4.00</td><td>2.00</td><td>10.00</td><td>3772.20</td><td>3.00</td><td>5.00</td><td>4.00</td><td>14.00</td><td>4037.10</td></tr><tr><td>Dcmtk</td><td>2.00</td><td>9.00</td><td>2.00</td><td>7.00</td><td>2139.80</td><td>9.00</td><td>13.00</td><td>9.00</td><td>16.40</td><td>2969.90</td><td>3.00</td><td>4.00</td><td>3.00</td><td>7.00</td><td>2668.00</td><td>4.00</td><td>12.30</td><td>6.00</td><td>34.20</td><td>3065.70</td></tr><tr><td>TinyDTLS</td><td>7.00</td><td>23.80</td><td>25.00</td><td>51.50</td><td>372.50</td><td>13.00</td><td>31.30</td><td>37.00</td><td>89.60</td><td>531.00</td><td>1.00</td><td>7.00</td><td>1.00</td><td>22.00</td><td>417.30</td><td>1.00</td><td>8.50</td><td>1.00</td><td>31.60</td><td>588.00</td></tr></table>

TABLE VI: Results of the ablation study.

<table><tr><td rowspan="2">Subject</td><td colspan="4">AutoSeeder-v0</td><td colspan="4">AutoSeeder-v1</td><td colspan="4">AutoSeeder-v2</td><td colspan="4">AutoSeeder</td></tr><tr><td>Number</td><td>State</td><td>Tran.</td><td>Code</td><td>Number</td><td>State</td><td>Tran.</td><td>Code</td><td>Number</td><td>State</td><td>Tran.</td><td>Code</td><td>Number</td><td>State</td><td>Tran.</td><td>Code</td></tr><tr><td>LightFTP</td><td>&gt;5M</td><td>22.00</td><td>154.20</td><td>325.70</td><td>1704</td><td>24.00</td><td>199.70</td><td>392.60</td><td>393</td><td>24.00</td><td>201.10</td><td>399.70</td><td>393</td><td>24.50</td><td>215.60</td><td>410.90</td></tr><tr><td>Bftpd</td><td>&gt;5M</td><td>21.00</td><td>188.50</td><td>431.20</td><td>14485</td><td>24.00</td><td>234.90</td><td>492.10</td><td>420</td><td>24.00</td><td>233.10</td><td>489.90</td><td>420</td><td>24.40</td><td>237.70</td><td>494.80</td></tr><tr><td>Pure-FTPD</td><td>&gt;5M</td><td>27.00</td><td>312.50</td><td>981.90</td><td>10448</td><td>27.00</td><td>327.40</td><td>1071.20</td><td>447</td><td>28.00</td><td>343.30</td><td>1057.30</td><td>447</td><td>31.30</td><td>449.00</td><td>1149.70</td></tr><tr><td>ProFTPD</td><td>&gt;5M</td><td>26.00</td><td>246.40</td><td>4957.10</td><td>1474</td><td>27.00</td><td>262.10</td><td>5289.30</td><td>602</td><td>27.00</td><td>270.70</td><td>5349.40</td><td>602</td><td>30.60</td><td>335.70</td><td>5498.80</td></tr><tr><td>Forked-daap</td><td>2196</td><td>5.00</td><td>10.00</td><td>1967.80</td><td>80</td><td>5.00</td><td>11.00</td><td>1975.40</td><td>59</td><td>5.00</td><td>11.00</td><td>1975.60</td><td>59</td><td>13.00</td><td>29.30</td><td>2577.10</td></tr><tr><td>Live555</td><td>&gt;1M</td><td>8.00</td><td>48.30</td><td>1637.90</td><td>7757</td><td>8.00</td><td>50.90</td><td>1901.60</td><td>594</td><td>8.00</td><td>51.10</td><td>1913.80</td><td>594</td><td>13.00</td><td>95.30</td><td>2931.60</td></tr><tr><td>Kamailio</td><td>&gt;1M</td><td>15.00</td><td>101.60</td><td>9031.70</td><td>13577</td><td>16.00</td><td>115.70</td><td>9731.20</td><td>527</td><td>16.00</td><td>119.80</td><td>9789.90</td><td>527</td><td>16.10</td><td>124.50</td><td>10604.70</td></tr><tr><td>Exim</td><td>&gt;1M</td><td>16.00</td><td>59.80</td><td>2973.80</td><td>8035</td><td>18.00</td><td>71.40</td><td>3643.90</td><td>520</td><td>18.00</td><td>71.30</td><td>3613.50</td><td>520</td><td>18.30</td><td>71.20</td><td>3711.30</td></tr><tr><td>Dcmtk</td><td>&gt;5M</td><td>3.00</td><td>2.00</td><td>2534.80</td><td>15214</td><td>3.00</td><td>2.00</td><td>2894.60</td><td>606</td><td>3.00</td><td>2.00</td><td>2981.70</td><td>606</td><td>4.00</td><td>3.00</td><td>3058.10</td></tr><tr><td>TinyDTLS</td><td>19</td><td>9.00</td><td>19.00</td><td>503.60</td><td>15</td><td>9.00</td><td>18.00</td><td>503.80</td><td>15</td><td>9.00</td><td>19.00</td><td>503.60</td><td>15</td><td>10.00</td><td>24.40</td><td>577.40</td></tr><tr><td>Ngtcp2</td><td>&gt;5M</td><td>7.00</td><td>12.00</td><td>2887.90</td><td>2373772</td><td>7.00</td><td>12.00</td><td>3128.80</td><td>525</td><td>7.00</td><td>12.00</td><td>3257.90</td><td>525</td><td>7.00</td><td>13.00</td><td>3545.20</td></tr><tr><td>Google quiche</td><td>&gt;1M</td><td>8.00</td><td>10.00</td><td>8092.30</td><td>33299</td><td>8.00</td><td>10.00</td><td>8719.20</td><td>357</td><td>8.00</td><td>10.00</td><td>8731.40</td><td>357</td><td>8.00</td><td>14.00</td><td>9017.90</td></tr></table>

Strategy S2. Across most protocols, S2 effectively eliminates approximately 99.8% of redundant seeds compared to AutoSeeder-v1, without causing any noticeable degradation in state space or code coverage.

Strategy S3. For protocols with complex seed structures and semantics, such as Forked-daapd, Live555, and Dcmtk, S3 achieves notably better results, with an average code coverage improvement of 8.77% over AutoSeeder-v2. In contrast, for protocols with highly regularized seed formats, such as FTP, the previous strategies already produce high-quality initial seeds, making the additional benefit of S3 relatively limited.

## F. RQ5: Real-World Bugs Finding of AutoSeeder

We evaluate the effectiveness of AutoSeeder in discovering real-world bugs by integrating it with AFLNet. To this end, we conduct long-term fuzzing on all targets.

Table VII presents the bugs discovered by AFLNet under the same setup across initial seed corpus generated by AutoSeeder and each baseline. AutoSeeder triggered a total of seven bugs, covering a variety of vulnerability types including useafter-return, buffer overflow, and memory leaks, which could lead to serious security consequences, including remote code execution and resource exhaustion. In contrast, the comparison method can discover only two of these bugs (ID 3 and ID 6). All crashes were reported to developers; four have been confirmed, while the remaining are under investigation. We are also actively applying for CVE IDs for the confirmed bugs. These results show that AutoSeeder significantly enhances the capability of existing fuzzers to continuously discover previously unknown vulnerabilities in real-world network services.

TABLE VII: Details of 7 bugs discovered by AutoSeeder.

<table><tr><td>ID</td><td>Protocol</td><td>Influence</td><td>Vulnerability Type</td><td>Status</td><td>AutoSeeder</td><td>Others</td></tr><tr><td>1</td><td>Live555</td><td>testOnDemandRTSPServer</td><td>SEGV</td><td>Reported</td><td>√</td><td></td></tr><tr><td>2</td><td>Live555</td><td>testOnDemandRTSPServer</td><td>use after return</td><td>Reported</td><td>√</td><td></td></tr><tr><td>3</td><td>Dcmtk</td><td>createAssociationKey</td><td>memory leaks</td><td>Confirmed</td><td>√</td><td>√</td></tr><tr><td>4</td><td>Dcmtk</td><td>DcmTransportLayer</td><td>memory leaks</td><td>Confirmed</td><td>√</td><td></td></tr><tr><td>5</td><td>TinyDTLS</td><td>server.c</td><td>buffer-overflow</td><td>Confirmed</td><td>√</td><td></td></tr><tr><td>6</td><td>LightFTP</td><td>cfgparse.c</td><td>memory leak</td><td>Reported</td><td>√</td><td>√</td></tr><tr><td>7</td><td>LightFTP</td><td>/ftpserv.c</td><td>memory leak</td><td>Confirmed</td><td>√</td><td></td></tr></table>

## V. CONCLUSION AND DISCUSSION

In this paper, we present AutoSeeder, the first automated framework designed to construct high-quality initial seed corpus for stateful protocol fuzzing. AutoSeeder comprises three key components: retrieval-based relevant code extraction, LLM-driven state transition analysis, and state-aware initial seed generation. By leveraging LLMs to analyze statehandling logic embedded in implementations, AutoSeeder automatically generates high-quality initial seeds that are syntactically valid and capable of reaching deep protocol states, thereby significantly reducing the reliance of existing fuzzers on manual effort. Evaluation on twelve real-world protocols across three state representation schemes and four baselines demonstrates the effectiveness and generality of AutoSeeder.

Limitations. Although the full state machine logic is implicitly embedded in protocol implementations, fully extracting relevant knowledge remains highly challenging, often leading to false negatives and false positives in both relevant code extraction and state transition analysis. Therefore, AutoSeeder is designed to complement mutation-based fuzzing rather than function as a purely generative method. Experimental results confirm the practical effectiveness of this hybrid strategy.

[1] S. Mohurle and M. Patil, “A brief study of wannacry threat: Ransomware attack 2017,” International journal of advanced research in computer science, vol. 8, no. 5, pp. 1938–1940, 2017.

[2] Codenomicon and Google Security Team, “The Heartbleed Bug,” https: //heartbleed.com/, 2020, [Online; accessed 10-April-2023].

[3] B. Hawkes, “0day in the wild,” https://googleprojectzero.blogspot.com/ p/0day.html, 2019, [Online; accessed 01-10-2021].

[4] V. J. Manes, H. Han, C. Han, S. K. Cha, M. Egele, E. J. Schwartz, and\` M. Woo, “The art, science, and engineering of fuzzing: A survey,” IEEE Transactions on Software Engineering, vol. 47, no. 11, pp. 2312–2331, 2019.

[5] PeachTech, “Peach fuzzing platform,” Website. https://www.peach.tech.

[6] J. Pereyda, “boofuzz: A fork and successor of the sulley fuzzing framework,” 2015.

[7] V.-T. Pham, M. Bohme, and A. Roychoudhury, “Aflnet: a greybox fuzzer ¨ for network protocols,” in 2020 IEEE 13th International Conference on Software Testing, Validation and Verification (ICST). IEEE, 2020, pp. 460–465.

[8] R. Natella, “Stateafl: Greybox fuzzing for stateful network servers,” Empirical Software Engineering, vol. 27, no. 7, p. 191, 2022.

[9] S. Qin, F. Hu, Z. Ma, B. Zhao, T. Yin, and C. Zhang, “Nsfuzz: Towards efficient and state-aware network service fuzzing,” ACM Transactions on Software Engineering and Methodology, vol. 32, no. 6, pp. 1–26, 2023.

[10] R. Meng, M. Mirchev, M. Bohme, and A. Roychoudhury, “Large¨ language model guided protocol fuzzing,” in Proceedings of the 31st Annual Network and Distributed System Security Symposium (NDSS), vol. 2024, 2024.

[11] L. Hayes, H. Gunadi, A. Herrera, J. Milford, S. Magrath, M. Sebastian, M. Norrish, and A. L. Hosking, “Moonlight: Effective fuzzing with nearoptimal corpus distillation,” arXiv preprint arXiv:1905.13055, 2019.

[12] A. Herrera, H. Gunadi, L. Hayes, S. Magrath, F. Friedlander, M. Sebastian, M. Norrish, and A. L. Hosking, “Corpus distillation for effective fuzzing: A comparative evaluation,” arXiv preprint arXiv:1905.13055, 2019.

[13] S. Jiang, Y. Zhang, J. Li, H. Yu, L. Luo, and G. Sun, “A survey of network protocol fuzzing: Model, techniques and directions,” arXiv preprint arXiv:2402.17394, 2024.

[14] C. S. Xia, M. Paltenghi, J. Le Tian, M. Pradel, and L. Zhang, “Fuzz4all: Universal fuzzing with large language models,” in Proceedings of the IEEE/ACM 46th International Conference on Software Engineering, 2024, pp. 1–13.

[15] Z. Yang, H. Peng, Y. Jiang, X. Li, H. Du, S. Wang, and J. Liu, “Chathttpfuzz: large language model-assisted iot http fuzzing,” International Journal of Machine Learning and Cybernetics, pp. 1–22, 2025.

[16] M. Zheng, D. Xie, Q. Shi, C. Wang, and X. Zhang, “Validating network protocol parsers with traceable rfc document interpretation,” arXiv preprint arXiv:2504.18050, 2025.

[17] J. Yen, T. Levai, Q. Ye, X. Ren, R. Govindan, and B. Raghavan, “Semi-´ automated protocol disambiguation and code generation,” in Proceedings of the 2021 ACM SIGCOMM 2021 Conference, 2021, pp. 272–286.

[18] S. Bishop, M. Fairbairn, M. Norrish, P. Sewell, M. Smith, and K. Wansbrough, “Rigorous specification and conformance testing techniques for network protocols, as applied to tcp, udp, and sockets,” in Proceedings of the 2005 conference on Applications, technologies, architectures, and protocols for computer communications, 2005, pp. 265–276.

[19] Z. M., “American fuzzy lop,” in http://lcamtuf. coredump. cx/afl, 2022.

[20] L. Xi, H. Zhang, S. Lin, W. Zhang, Y. Sun, H. Zhu, and L. Sun, “Enhancing coverage in stateful protocol fuzzing via value-based selection,” in 2024 IEEE Symposium on Computers and Communications (ISCC). IEEE, 2024, pp. 1–6.

[21] J. Ba, M. Bohme, Z. Mirzamomen, and A. Roychoudhury, “Stateful¨ greybox fuzzing,” in 31st USENIX Security Symposium (USENIX Security 22), 2022, pp. 3255–3272.

[22] K. K. Ang and D. C. Ranasinghe, “Quic-fuzz: An effective greybox fuzzer for the quic protocol,” arXiv preprint arXiv:2503.19402, 2025.

[23] J. Li, S. Li, G. Sun, T. Chen, and H. Yu, “Snpsfuzzer: A fast greybox fuzzer for stateful network protocols using snapshots,” IEEE Transactions on Information Forensics and Security, vol. 17, pp. 2673–2687, 2022.

[24] S. M. M. Rashid, T. Wu, K. Tu, A. A. Ishtiaq, R. H. Tanvir, Y. Dong, O. Chowdhury, and S. R. Hussain, “State machine mutation-based testing framework for wireless communication protocols,” in Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security, 2024, pp. 2102–2116.

[25] R. Natella and V.-T. Pham, “Profuzzbench: A benchmark for stateful protocol fuzzing,” in Proceedings of the 30th ACM SIGSOFT international symposium on software testing and analysis, 2021, pp. 662–665.

[26] W. Lin, Z. Jiang, F. Xu, Y. Su, Z. Li, L. Mao, and C. Tang, “Svrm: Composing various network service fuzzing corpus with one single model,” in ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2025, pp. 1–5.

[27] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell et al., “Language models are few-shot learners,” Advances in neural information processing systems, vol. 33, pp. 1877–1901, 2020.

[28] Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan, “Automated repair of programs from large language models,” in 2023 IEEE/ACM 45th International Conference on Software Engineering (ICSE). IEEE, 2023, pp. 1469–1481.

[29] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat et al., “Gpt-4 technical report,” arXiv preprint arXiv:2303.08774, 2023.

[30] A. Radford, K. Narasimhan, T. Salimans, I. Sutskever et al., “Improving language understanding by generative pre-training,” 2018.

[31] P. Liu, W. Yuan, J. Fu, Z. Jiang, H. Hayashi, and G. Neubig, “Pretrain, prompt, and predict: A systematic survey of prompting methods in natural language processing,” ACM computing surveys, vol. 55, no. 9, pp. 1–35, 2023.

[32] M. M. Mohajer, R. Aleithan, N. S. Harzevili, M. Wei, A. B. Belle, H. V. Pham, and S. Wang, “Skipanalyzer: An embodied agent for code analysis with large language models,” CoRR, 2023.

[33] O. Topsakal and T. C. Akinci, “Creating large language model applications utilizing langchain: A primer on developing llm apps fast,” in International Conference on Applied Engineering and Natural Sciences, vol. 1, no. 1, 2023, pp. 1050–1056.

[34] D. Guo, S. Lu, N. Duan, Y. Wang, M. Zhou, and J. Yin, “Unixcoder: Unified cross-modal pre-training for code representation,” arXiv preprint arXiv:2203.03850, 2022.

[35] S. S. Monir, I. Lau, S. Yang, and D. Zhao, “Vectorsearch: Enhancing document retrieval with semantic embeddings and optimized search,” arXiv preprint arXiv:2409.17383, 2024.

[36] K. Fang, L. Zhao, Z. Shen, R. Wang, R. Zhour, and L. Fan, “Beyond lexical: A semantic retrieval framework for textual searchengine,” arXiv preprint arXiv:2008.03917, 2020.

[37] P. Welsby and B. M. Cheung, “Chatgpt,” pp. 1047–1048, 2023.

[38] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever et al., “Language models are unsupervised multitask learners,” OpenAI blog, vol. 1, no. 8, p. 9, 2019.

[39] X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, S. Narang, A. Chowdhery, and D. Zhou, “Self-consistency improves chain of thought reasoning in language models,” arXiv preprint arXiv:2203.11171, 2022.
# Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic

Van Tran University of Chicago Chicago, United States

Tian Li University of Chicago Chicago, United States

Shinan Liu University of Hong Kong Hong Kong, China

Nick Feamster University of Chicago Chicago, United States

## Abstract

To address the scarcity and privacy concerns of network trafic data, various generative models have been developed to produce synthetic trafic. However, synthetic trafic is not inherently privacy-preserving, and the extent to which it leaks sensitive information, and how to measure such leakage, remain largely unexplored. This challenge is further compounded by the diversity of model architectures, which shape how trafic is represented and synthesized. We introduce a comprehensive set of privacy metrics for synthetic network trafic, combining standard approaches like membership inference attacks (MIA) and data extraction attacks with network-specific identifiers and attributes. Using these metrics, we systematically evaluate the vulnerability of diferent representative generative models and examine the factors that influence attack success. Our results reveal substantial variability in privacy risks across models and datasets. MIA success ranges from 0% to 88%, and up to 100% of network identifiers can be recovered from generated trafic, highlighting serious privacy vulnerabilities. We further identify key factors that significantly afect attack outcomes, including dataset diversity and how well the generative model fits the training data. These findings provide actionable guidance for designing and deploying generative models that minimize privacy leakage, establishing a foundation for safer synthetic network trafic generation. We release our code and evaluation framework to support reproducibility and facilitate future research.

## CCS Concepts

• Security and privacy → Network security.

Keywords Synthetic network trafic; Privacy leakage

ACM Reference Format: Van Tran, Shinan Liu, Tian Li, and Nick Feamster. 2026. Quantifying the Privacy Implications of High-Fidelity Synthetic Network Trafic. In Proceedings ofthe 2026 ACM Internet Measurement Conference (IMC ’26), October 12–16, 2026, Karlsruhe, Germany. ACM, New York, NY, USA, 18 pages. https://doi.org/10.1145/3777912.3839833

## 1 Introduction

Network trafic generators have gained significant traction in both academia and industry due to their versatility [1–4]. They can augment training data for underrepresented scenarios (such as network attacks), enabling more robust anomalydetection models [5, 6]. They also provide a practical way to generate diverse, realistic trafic for analysis, algorithm testing, and performance benchmarking—allowing users to work with high-fidelity data without needing access to raw trafic traces [1, 5, 7].

However, generative modeling does not automatically come with privacy [8–10]. While prior work has focused largely on fidelity [3, 4, 11], i.e., how realistic the generated trafic appears, much less attention has been paid to the privacy implications of synthetic trafic generation. In practice, many generative models either overlook privacy risks entirely [11, 12] or ofer only minimal protection against them. Compounding this issue, systematic evaluation of privacy risks in synthetic network trafic remains scarce. A few existing eforts primarily rely on existing membership inference attacks (MIA) [3, 13, 14] as the sole measure of privacy leakage, even though network trafic contains highly sensitive information beyond data membership [1, 15–17].

To bridge the gap between real-world privacy risks in network trafic and the limited metrics currently used to evaluate them, we introduce a comprehensive suite of privacy metrics spanning three complementary attack types: (1) membership inference attacks (MIA), (2) data extraction attacks, and (3) network-specific privacy attacks. MIA and data extraction are standard privacy attacks against generative models [18–20]. MIA determines whether a trafic sample was included in the model’s training data, while data extrac tion measures whether the model memorizes and reproduces training data. However, neither attack reveals what informa tion is exposed, whether it is sensitive, or the extent of the leakage, limiting their interpretability for network privacy.

Leveraging insights from real-world privacy attacks on network trafic, including fingerprinting [21, 22], attribute inference [17, 23], and topology reconstruction [24, 25], we introduce network-specific metrics that capture three key risks: (i) network identifier memorization (e.g., IP and MAC addresses), which can directly expose users and devices; (ii) sensitive property leakage, which can reveal user behaviors, visited websites, and application usage patterns; and (iii) topology extraction, which exposes structural relationships between network entities and can compromise organizational security. Together, these metrics capture the practical privacy risks of synthetic trafic generation and inform deployment decisions.

We evaluate our metrics across four state-of-the-art gen erative models, each representing a distinct generation paradigm (GAN, difusion, transformer, SSM), and five datasets collected under diverse network conditions and tasks. Here is the summary of our research questions:

• RQ1: How successful can each privacy attack be under the most challenging conditions for an attacker? (§5) We evaluate MIA, data extraction, and network-specific privacy attacks across network generative models under the most challenging conditions for an attacker: attackers only have black-box access and each generative model only undergoes minimal training (i.e., less likely to overfit to or memorize training data). We find that even under these constrained conditions, MIA attacks, particularly against NetSSM and NetShare, can achieve true positive rate (TPR) exceeding 0.8 on some datasets. Additionally, up to 100% of network identifiers in training data can be correctly recovered from the outputs of NetSSM and TraficLLM.

• RQ2: Which factors impact the success of privacy attacks? (§6) We evaluate the factors that could influence each privacy attack type. These include attacker capabilities (black-box vs. white-box access), model overfitting, and data properties (training data diversity). Our findings reveal that for MIA, white-box access can increase the TPR by nearly 0.2 on average for NetDifusion and NetSSM. For data extraction and network-specific attacks, models with greater overfitting increase extractable rate and network identifiers’ precision and recall scores.

• RQ3: What is the privacy-utility tradeof when ap plying privacy risks mitigation techniques? (§6) We explore whether mitigation strategies such as identifier anonymization and noise addition can reduce privacy risks, and examine the privacy-utility tradeofs of these approaches. Our findings show that no single mitigation strategy can address all privacy risks and applying these techniques can reduce data utility.

The remainder of this paper is organized as follows. Section 2 covers related work. Section 3 describes privacy attack and mitigation methodology. Section 4 presents experimental setup. Section 5, 6, and 7 each covers results for a research question. Section 8 discusses implications of our findings and we conclude our work in Section 9.

## 2 Related Work

## 2.1 Network Trafic Generation

Synthetic trace generation has long been an important topic in network research, and consequently, a substantial body of work has been dedicated to advancing this area.

Non-generative models: Early network trafic generation relied on simulation tools [26–31] or statistical methods [32, 33]. However, simulation tools fail to capture the complexity of real-world trafic, while statistical methods generate only limited network features and lack the fine-grained granularity required for many network analysis tasks.

GAN-based models: Generative Adversarial Networks (GANs) are a class of generative models that train a generator and a discriminator in an adversarial manner until generated outputs become statistically indistinguishable from real data. GAN-based trafic generators include NetShare [3], Doppel-GANger [34] and PacketCGAN [35]. NetShare first merges trafic collected from diferent measurement epochs into a single large trace and then splits the trace into flows based on five-tuples. Next, each header field is encoded using datasetdependent encoding schemes. A time-series GAN is then trained on the encoded data to capture temporal dependencies within each flow. Generated outputs include flow-level statistics and selected packet header fields, including IP addresses, ports, TTL values, packet sizes, and inter-arrival times.

Difusion-based models: Difusion models are a class of generative AI models that generate high-quality data by learning to reverse a gradual noise-addition process. Difusionbased network trafic generators [4, 36–38] often represent network trafic as images and fine-tune difusion models to synthesize realistic trafic samples. NetDifusion [4], for example, represents packet headers as 2D images by first converting header fields into bitmaps and then applying a three-value color encoding scheme to represent bit values of 0, 1, and missing or undefined fields. The resulting images are used to fine-tune a pre-trained Stable Difusion model conditioned on trafic class labels. During generation, the model conditions on both a text prompt and a structural edge map extracted using ControlNet to better preserve structural patterns, followed by a post-generation correcting process to ensure generated trafic follow network protocols.

<table><tr><td>Model</td><td>Base Model</td><td>Granularity</td><td>Unit</td><td>Generated Data</td></tr><tr><td>NetDiffusion</td><td>Diffusion</td><td>Packet</td><td>Bit</td><td>Network layer (except IP addresses), transport layer for the first 1024 packets.</td></tr><tr><td>NetSSM</td><td>State-space model</td><td>Packet</td><td>Byte</td><td>Ethernet layer, network layer and transport layer for the entire PCAP file.</td></tr><tr><td>TrafficLLM</td><td>Transformer</td><td>Packet</td><td>Hex digits</td><td>Ethernet layer, network layer, and transport layer for the first packet.</td></tr><tr><td>NetShare</td><td>GANs</td><td>Flow</td><td>Tabular values</td><td>5-tuples and header fields including packet length, type of service, identification, control flag, data offset, time to live, and inter-arrival time.</td></tr></table>

Table 1: Overview of network trafic generative models and their output representations.

Transformer-based models: Transformer-based models are neural networks that process sequential data by using a mechanism called self-attention, which allows the model to look at all elements in a sequence at once and learn how they relate to each other. Transformer-based trafic generators [12, 39, 40] typically tokenize network trafic into hexadec imal values or byte-level representations and then train or fine-tune transformer models to learn trafic patterns and representations. TraficLLM [12] fine-tunes GPT-2 on tokenized network trafic using a two-stage pipeline. The first stage improves the model’s instruction-following capability, while the second stage focuses on learning network trafic patterns and representations.

State-space models: State-space models (SSMs) [11] are mathematical frameworks for modeling sequential dynamic systems through hidden states that evolve over time. NetSSM [11] applies this framework to network trafic generation through a structured tokenization and pretraining pipeline. First, it tokenizes packet headers at the byte level, mapping each byte to an integer in the range [0, 255]. These token sequences are further augmented with control tokens, such as label tokens to indicate trafic type and boundary tokens to delimit individual packets. The resulting sequences are used to pretrain an SSM architecture that predicts the next token autoregressively given the preceding context.

In this study, we examine privacy leakage across four models - NetShare, NetDifusion, TraficLLM, and NetSSM — selected for two reasons. First, each model represents the state of the art within its respective generative paradigm: GANs, difusion models, transformers, and state-space models. Second, this diversity of paradigms enables a comprehensive assessment of privacy risks across fundamentally diferent architectural approaches, facilitating a rigorous evaluation of the privacy-utility trade-ofs inherent to each approach. Table 1 summarizes key diferences between each model.

## 2.2 Privacy Risks of Generative Models

Membership inference attacks: Under MIA, an adver sary can leverage generative models’ tendency to overfit to their training data to diferentiate between training versus non-training samples based on how the model behaves on them. In a typical MIA setting, attackers first extract observ able signals and then apply a threshold or classifier to infer membership. In a white-box MIA where an attacker has access to the model’s internal parameters and gradients, an attacker can use a wider variety of signals such as model loss [41, 42] and gradient on input samples [8, 43]. In contrast, in a black-box setting, membership signals observed by an attacker are often limited to the model’s outputs and output token probabilities [44–46]. To overcome this limitation, an attacker can train shadow models on some shadow train set [46, 47], enabling them to learn membership inference patterns without direct access to the model’s internals. MIA can be successful on a variety of models, including difusion models [18, 43, 48, 49], transformer-based models [50–54] and GAN-based models [8, 46].

Data extraction attacks: Extraction attacks concern with whether an attacker can reconstruct training data, be it text sequences [44, 55] or images [56], from the model. Various models including difusion [56, 57], transformers [44, 55, 58], and GANs [59–61] are vulnerable to this attack. For example, since memorized samples tend to appear with disproportionately high frequency and confidence scores, attackers can prompt the model to generate a large number of outputs, rank them based on these metrics, and then examine them for memorization. Extracted text sequences can contain sensitive information such as names, phone numbers, and email addresses [44, 55], while extractable images contain identifiable faces and company logos [56].

Other privacy attacks: Generative models are also vulnerable to additional privacy risks, including attribute inference and linkability attacks. Attribute inference attacks [10, 20, 62–64] aim to uncover a specific sensitive attribute of the model’s training data such as its composition. In contrast, a linkability attack [65, 66] concerns with whether an adversary can determine if two records originate from the same underlying entity.

## 2.3 Privacy Risks of Network Trafic

Fingerprinting attacks are among the most widely studied and prevalent for network trafic. Leveraging packet sizes, timing patterns, TTL values, and window sizes, adversaries can infer device types [15, 16], operating systems [21, 22], and services being used [67, 68]. Under attribute inference attacks [17, 23], attackers can infer sensitive attributes about training data such as demographic of its users, their age group and career stage. Additionally, some attacks [1, 24, 25] attempt to deanonymize networks and reconstruct network topologies from anonymized trafic data.

Despite various privacy attacks on network trafic, privacy risks in synthetic network trafic remain largely unexplored. Jin et al. [14] provide early evidence that MIA at the traficsource level is feasible. However, their work focuses solely on MIA, leaving other threats, such as fingerprinting and attribute inference, unexplored. This leaves a critical gap in understanding the privacy risks of synthetic network trafic and how to mitigate them.

## 2.4 Privacy Risks Mitigation

Various privacy risks mitigation techniques have been de veloped to protect network trafic privacy. Anonymization methods [69–71], such as prefix-preserving and reversible pseudonymization, mask identifiers like IP and MAC addresses to prevent recovery of original values. Other ap proaches protect sensitive fields, including port numbers, flow sizes, and packet inter-arrival times, by reducing meta data granularity [72], adding noise [73, 74], or modifying packet traces through trafic shaping [75–77].

Despite extensive work on privacy protection for real network trafic, synthetic network trafic remains largely un protected. Existing generators either lack privacy safeguards [11, 12] or apply limited protections, such as removing IP addresses [4] or adding diferential privacy noise to protect against MIA [3, 13]. Moreover, none evaluate or mitigate network trafic–specific privacy attacks. This lack of comprehensive privacy evaluation and mitigation poses significant security challenges for synthetic network trafic generation.

## 3 Methods to Evaluate Privacy & Utilities

Section 3.1 describes our methods for evaluating privacy risks through MIA, data extraction, and network-specific privacy attacks, along with the rationale for these attacks. Section 3.2 presents the mitigation techniques we evaluate and the downstream utility assessments used to measure their privacy–utility tradeofs.

Not all privacy attacks apply to every generative model due to diferences in model architectures and outputs. For example, NetDifusion removes all network identifiers from the training data, preventing identifier-based attacks. Similarly, TraficLLM generates only the first packet of each flow rather than complete flows, making attribute-based network specific attacks infeasible. Accordingly, we evaluate only the privacy attacks applicable to each model. Table 2 summarizes the attacks conducted for each model.

## 3.1 Privacy Attack Methods

3.1.1 Membership Inference Atack (MIA)We conduct MIA at the PCAP level, the common generation unit for network trafic models. To launch MIA, we curate signals (features)

<table><tr><td></td><td>MIA</td><td>Data extraction</td><td colspan="3">Network-specific Identifiers Attributes Topology</td></tr><tr><td>NetShare</td><td>√</td><td>✗</td><td>√</td><td>√</td><td>√</td></tr><tr><td>NetDiffusion</td><td>√</td><td>√</td><td>✗</td><td>√</td><td>✗</td></tr><tr><td>TrafficLLM</td><td>√</td><td>√</td><td>√</td><td>✗</td><td>✗</td></tr><tr><td>NetSSM</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

Table 2: Privacy attacks conducted for each generative model. ✓ indicates an attack was conducted; ✗ indicates “not conducted” because of diferent data encodings and model design choices.

for training binary classifiers that predict whether a sample belongs to the training set. Under black-box MIA, we assume the adversary has no access to model internals, such as parameters or gradients, and does not train shadow models. However, the adversary can observe model outputs and token log probabilities [44]. For NetDifusion, we use the pixel-wise $L _ { 2 }$ reconstruction error between the input and generated images. For NetSSM and TraficLLM, we compute perplexity using token log probabilities from the first packet of the input PCAP. For NetShare, which generates tabular flow records, we extract features from generated outputs, including the total number of packets, counts of unique source and destination IPs and ports, and the mean and standard deviation of continuous fields such as packet length and TTL.

Under white-box MIA, where the attacker can access model parameters and gradients, we use the average gradient norm of model parameters on the input image for NetDifusion. For TraficLLM and NetSSM, we use the average gradient norm computed on tokens generated from the first packet of the input PCAP. We do not conduct white-box MIA on NetShare because its generator and discriminator operate on preprocessed encoded representations rather than raw trafic data. Since the encoded input dimensionality depends on the dataset-specific encoding process, models trained on one PCAP trace are incompatible with others, preventing direct reuse of model internals for membership inference.

After extracting signals from the target holdout set (nonmembers) and shadow training set (members), we train classifiers to predict membership status. We evaluate several classifiers, including neural networks, support vector machines (SVMs), and XGBoost, and report results from the best-performing model. Following standard MIA evaluation practice [78–80], we report the true positive rate at a false positive rate of 0.01 (TPR at FPR≤0.01). Figure 1 illustrates the construction of the train, shadow train, and target holdout sets, while Figure 2 shows the overall MIA pipeline.

3.1.2 Data Extraction AtackInspired by Nasr et al. [55], who define a successful extraction as one where the model outputs text containing a substring of at least 50 tokens that appears verbatim in the training set, we adapt this approach to the networking context as follows. First, we define the "generation prompt" as the input required by each model to produce synthetic trafic. For NetDifusion, this is a combination of a training image and a descriptive text prompt specifying the trafic type. For NetSSM and TraficLLM, it is the trafic type label present in the training data. For NetShare, it is the raw network trafic PCAPs.

![](images/0f467b52bf00d415db2ba47357d8931afcb33cb3871bc11346716da4c6bd8041.jpg)  
Figure 1: Pipeline of splitting each dataset into train set, shadow train set and target holdout.

![](images/142cbedf9f67d3d2d8fb6ab2cd0c9575b509052c88e58963eb9b023b8f336e57.jpg)  
Figure 2: Pipeline of Membership Inference Attacks (MIA). (1) The data owner trains the generative model on the train set and makes it available as a service to everyone. (2) An attacker queries the generative model to extract signals and trains a binary attacker model to predict membership. (3) To predict membership of a target sample, an attacker first queries the generative model to extract signals, then predicts membership using the trained attacker model.

Second, we compare each generated sequence against the training data to identify verbatim matches. We define a generated sequence as extractable if it contains a contiguous sequence ofat least 10 tokens that appears verbatim in the training data (we identify contiguous matches at the token level, rather than in the parsed header fields). Because diferent generative models operate over diferent representation units, we define a “token” as the native unit used by each model to learn and generate synthetic trafic. For example, in NetDifusion, a token corresponds to a bit, so extractabil ity requires memorization of a contiguous sequence of 10 bits (1.25 bytes). In NetSSM, a token corresponds to a byte, yielding a threshold of 10 bytes, while in TraficLLM, a token corresponds to a hexadecimal digit, corresponding to 10 hex digits (5 bytes).

To measure the success of a data extraction attack on a model, we introduce the metric extractable rate, defined as the percentage ofgenerated outputs that constitute a successful extraction.

3.1.3 Network-Specific AtackNetwork trafic contains di verse information that varies in sensitivity. Network identifiers such as MAC addresses and IP addresses are highly sensitive, as they can reveal the location, device type, and even the identity of users. Other features, such as Time To Live (TTL) and Type of Service (ToS), while less sensitive than network identifiers, can be used to generate fingerprints that infer the operating system or application type. Furthermore, overall trafic patterns can be collectively analyzed to reconstruct network topology, exposing critical network infrastructure. To address these diverse privacy concerns, we categorize this sensitive information into three types: network identifiers, network properties, and network topology, and we evaluate each separately.

Network Identifiers: While network identifiers are considered "personal information" under major privacy frameworks, including GDPR and CCPA, and may be subject to anonymization requirements, certain entities such as network operators, ISPs, and organizations exempt under specific jurisdictions, may lawfully retain this information for legitimate operational purposes, including security monitoring, network management, and attack detection. Therefore, identifier leakage in synthetic trafic therefore remains a significant practical concern. Inspired by the privacy metrics of Lukas et al. [81] for measuring PII leakage, we adopt two complementary metrics, Precision and Recall, to quantify identifier leakage. Recall measures how much of the training dataset’s network identifiers are at risk of extraction. Precision measures an attacker’s confidence that a generated network identifier appears in the training dataset.

$$
\begin{array}{l} R e c a l l = \frac {| \{i \mid i \in \mathcal {G} \cap \mathcal {T} \} |}{| \{i \mid i \in \mathcal {T} \} |} \\ P r e c i s i o n = P (i \in \mathcal {T} \mid i \in \mathcal {G}) \end{array}
$$

where G denotes the set of identifiers generated, and T denotes the set of identifiers present in the training data.

Network properties: Based on features used in fingerprinting and attribute inference attacks [17, 21–23], we consider the following non-identifiers as sensitive network properties: Time To Live (TTL), IP Identification (IP ID), Type of Service (ToS), Window Size, Control Flags, TCP Data Ofset, flow size, and packet size. Since ground truth for fingerprinting attacks is unavailable, we evaluate leakage by comparing the distributions of these features between training and generated data using Earth Mover’s Distance (EMD) [82] <sup>1</sup>. A smaller distance indicates higher leakage risk.

Network topology: Network topology refers to the structure of how devices are connected and communicate in a network, including link-level connections (using MAC addresses) and network-level routing (using IP addresses). This information can expose relationships among devices and network segments [83], allowing attackers to identify critical nodes and potential attack paths [84, 85]. To measure topol ogy leakage, we employ a graph-based comparison between training and generated data. We define a communication flow as an exchange of network trafic (unidirectional or bidirectional) between a pair of addresses (IP or MAC).

To evaluate topology leakage, we select the top 100 communication flows ranked by total bytes transferred and constructs non-directed graphs where nodes represent IP or MAC addresses and edges encode observed communication relationships. Since the flows in this setting are large, persistent transfers that dominate network by volume despite constituting a negligible fraction of total flow count, they likely encode inter-node dependency relationships, bottleneck locations, and routing hierarchies, making their leakage a disclosure of the load-bearing skeleton of the underlying network topology [86]. Additionally, we also evaluate under a setting where the topology comprises of both large and small flows. Refer to Appendix C for the setup and results.

Topology similarity is evaluated using three metrics: (1) node overlap—the proportion of addresses common to both graphs, (2) edge overlap—the proportion of shared communications, and (3) node connectivity distribution—the similarity in the number of connections per node across both topologies (measured using EMD). Note that cross-flow correlation at tacks, while outside our current threat model, could amplify topology leakage by exploiting relationships across flows and are an important direction for future work.

3.1.4 Why do These Atacks Mater?We focus on membership inference, data extraction, and network-specific privacy attacks because they correspond to the main questions that network operators and data owners are concerned about when releasing synthetic trafic. Industry frameworks such as the OWASP ML Security Top 10 [87] and NIST AI guidance [88] recognise MIA and data extraction as AI privacy risks that can lead to confidentiality breaches, regulatory exposure, and reputational harms.

First, MIA captures participation privacy and is widely adopted as a standard way to quantify privacy risk in ma chine learning [46]. In the networking context, MIA reveals whether trafic from a specific user, device, service, or organization was used for training, allowing attackers to infer sensitive network activity or the presence of specific services or devices.

Second, data extraction attacks measure content memorization. Prior work has shown that generative models can regurgitate individual training records [44, 55]. In network trafic, these attacks test whether a model reproduces training packet sequences when queried. For example, extracting packets from an internal service could reveal its port, protocol, and communication pattern, enabling attackers to identify and target hidden services.

Third, our network-specific attacks target semantic leakage unique to network trafic. By separately measuring leakage of network identifiers (such as IP and MAC addresses), fingerprinting-relevant fields (such as TTL, window size, or flags), and communication topology, these attacks capture concrete harms such as re-identifying a host from its IP address, inferring its OS or software stack from fingerprinting fields, or identifying otherwise hidden internal services from communication patterns.

Together, these three attack families capture complementary privacy risks in synthetic network trafic: training-set participation (MIA), trace memorization (data extraction), and network-semantic leakage (network-specific attacks). We therefore argue that they provide a meaningful core for evaluating privacy risks in trafic generative models.

In this study, we focus on privacy risks in multi-flow network trafic, where packet captures (PCAPs) contain multiple concurrent flows, as this better reflects real-world network conditions and often introduces additional privacy risks compared to single-flow trafic. Further motivation for this design choice is provided in Section 4.1.

## 3.2 Privacy Risks Mitigation Methods

Inspired by privacy risks mitigation techniques for real network trafic [69–71, 73, 74], we explore several mitigation strategies and evaluate their privacy-utility tradeofs on synthetic trafic. For each strategy, we apply mitigation on the trafic generators’ training data.

3.2.1 Anonymization-Based StrategiesTo protect network identifiers and network topology, we investigate three anonymization strategies with varying levels of restrictiveness.

• Complete Anonymization (CA): In this most restrictive anonymization approach, each network identifier (IP addresses and MAC addresses) is replaced with a single constant value. This approach efectively eliminates all identifier-based privacy attacks, including network topology reconstruction.

• Pseudonymization (PS): A less restrictive alternative is pseudonymization where each unique network identifier in the training data is consistently replaced with a distinct randomly generated synthetic identifier. This one-to-one mapping preserves network structure and communication patterns while obscuring the original identifiers.

• Prefix-preserving (PP): For this approach, the last k bits of each network identifier are set to zero (k=8 bits for IP addresses, k=12 bits for MAC addresses), while the rest remain intact, allowing the hierarchical prefix informa tion to be preserved. For IP addresses, subnet structure is retained while host identities is obscured. For MAC ad dresses, the organization unique identifier that identifies the manufacturer is preserved while device-specific bits are removed.

3.2.2 Noise-Based StrategiesDiferential Privacy (DP) noise is a privacy risk mitigation technique where calibrated ran dom noise is deliberately injected into data, queries, or model updates, ensuring that it is statistically impossible for an adversary to detect whether any single data point was included or excluded in the dataset. Since most network trafic gen erative models do not currently support adding DP noise directly to the model (e.g., via DP-SGD), we apply DP-noise to the training data, as in previous works [13]. Rather than perturbing every header field, we specifically target the sensitive network properties including TTL, IP ID, ToS, Window Size, IP packet length. We do not add noise to fields such as IP addresses or MAC addresses. We allocate an equal privacy budget across all targeted properties and add noise simultaneously for all selected properties. We then apply clipping and rounding operations to ensure the perturbed values re main within valid ranges and conform to the appropriate data types.

3.2.3 Privacy-Utility Tradeofs EvaluationWe measure utility using two metrics: fidelity and downstream task performance. To assess privacy implications, we select key metrics from Section 3.1 covering all three attack types.

Fidelity metrics. Fidelity measures how well synthetic trafic resembles real-world trafic. Following the fidelity metrics used in NetShare [3], we measure distributional dis tance between training and generated datasets using Earth Mover’s Distance (EMD) across five key distributions. An increase in EMD indicates a decrease in fidelity since the gen erated data diverges further from the training distribution, while a decrease in EMD indicates an increase in fidelity. The five evaluated distributions are:

• SA/DA: Relative frequency ranking of source and destination IP addresses (from most to least frequent)

• SP/DP: Distribution of source and destination port numbers

• PR: Relative frequency of IP protocols (e.g., TCP, UDP, ICMP)

<table><tr><td>Traffic Dataset</td><td>#Pcaps</td><td>#Flows</td><td>#Packets</td><td>#IPs</td><td>#MACs</td><td>#Labels</td></tr><tr><td>Service recognition (SR)</td><td>660</td><td>2,363</td><td>1,313,372</td><td>207</td><td>21</td><td>11</td></tr><tr><td>IoT (IoT)</td><td>521</td><td>9,023</td><td>1,007,501</td><td>1324</td><td>48</td><td>9</td></tr><tr><td>USTC TFC 2016 (USTC)</td><td>501</td><td>183,570</td><td>994,174</td><td>116620</td><td>15</td><td>13</td></tr><tr><td>CIC DoHBrw 2020 (CIC)</td><td>480</td><td>10,758</td><td>838,140</td><td>2330</td><td>7582</td><td>8</td></tr><tr><td>VNAT (VNAT)</td><td>1103</td><td>14,646</td><td>2,118,603</td><td>52</td><td>51362</td><td>19</td></tr></table>

Table 3: Overview of five network trafic datasets.

Downstream task performance. Downstream task utility of synthetic trafic is measured using downstream classification accuracy. In the multi-flow setting, we classify PCAPs using PCAP-level labels. In the single-flow setting, we split each PCAP into flows and classify individual flows using flow-level labels. Since flow-level labels are available only for the IoT and SR datasets, to ensure fair comparison between multi-flow and single-flow settings, we evaluate downstream performance only on these two datasets.

For the IoT dataset, the multi-flow task is device activity classification (e.g., Alexa playing music), while the singleflow task is device-type classification, which is important for anomaly detection and security monitoring [89, 90]. For the SR dataset, both multi-flow and single-flow tasks classify service types (e.g., video conferencing or streaming), which are important for QoS provisioning and network resource allocation [91].

Similar to Jiang et al. [4] and Chu et al. [11], we also use packet header-level features (excluding identifier-based features such as IP addresses) determined via nPrintML [92], as features to classify each PCAP. <sup>2</sup> We train two XGBoost classifiers: one on synthetic trafic generated when the generator’s training data is unmitigated and one on synthetic trafic generated when training data is mitigated. We evaluate these two classifiers on the same real-world held-out test set (shadow train set). The classification accuracy diference of these two models quantifies the utility cost of applying mitigation techniques.

Privacy metrics. Privacy impact of mitigation techniques is measured using the follow metrics. To measure changes in MIA success, we measure changes in TPR at FPR ≤ 0.01 (Δ TPR at FPR ≤ 0.01). For data extraction attack, we use changes in extractable rate (Δ extractable rate). Lastly, for networkspecific attacks, we use (1) changes in precision score and (2) changes in recall score for source IP and (3) changes in Earth Mover’s Distance (Δ EMD) between training and generated data averaged across all sensitive network properties (refer to Section 3.1.3). Since lower EMD indicates more successful attacks (closer distributional match enables easier property inference), while higher EMD indicates improved privacy protection, to maintain consistency with other metrics where positive changes indicate improved privacy, we report the change in network-specific attack efectiveness as the negative of the change in EMD (i.e., -ΔEMD).

We investigate privacy–utility tradeofs for both multiflow and single-flow generation to understand how mitigation techniques afect diferent trafic generation tasks. Privacy is evaluated across all five datasets, while utility, including both fidelity and downstream task performance, is assessed only on the IoT and SR datasets.

## 4 Experimental Setup

This section describes the target to be generated in our experiments, the dataset preparation process, and the details of synthetic trafic generation.

## 4.1 Generation Target

In this work, our main target for generation for privacy evaluation is multi-flow PCAPs. Unlike single-flow PCAPs that capture communication between two entities, multiflow PCAPs contain multiple concurrent flows, each defined by a 5-tuple (source IP, destination IP, source port, destination port, protocol). Multi-flow trafic generation is valuable for practical applications including network trafic analytics, monitoring, and simulating realistic environments to test network algorithms and protocols. However, it presents unique technical and privacy challenges that make it particularly important to study.

From a technical perspective, multi-flow generation is more complex than single-flow generation. While singleflow generation only needs to model the temporal dynamics within one communication session (intra-flow patterns), multi-flow generation must additionally capture the relation ships and dependencies between diferent flows (inter-flow patterns), such as timing correlations and bandwidth sharing across concurrent connections.

From a privacy perspective, multi-flow trafic exposes more sensitive information than single-flow trafic. Beyond individual communication details, multi-flow data reveals network-wide communication patterns, entity relationships, and network topology—information that is highly sensitive and valuable to adversaries. For example, flow co-occurrence patterns can serve as efective signals for membership inference and topology reconstruction attacks, and can further enable the construction of user, service, or device trafic fingerprints. These elevated privacy risks make multi-flow trafic generation a critical area for privacy evaluation.

Given both the practical importance and heightened privacy concerns of multi-flow trafic generation, we focus primarily on this scenario throughout our evaluation.

## 4.2 Dataset Preparation

We use five datasets collected from diferent networks and application domains. The IoT dataset [93] contains trafic from various IoT device activities. The Service Recognition (SR) [4] and VNAT [94] datasets capture trafic from diferent service types, including streaming, conferencing, and social media. The USTC TFC 2016 (USTC) [95] and CIC DoHBrw 2020 (CIC) [96] datasets provide network trafic from various attack scenarios. <sup>3</sup> Refer to Table 3 for the final dataset size.

Furthermore, since packet captures (PCAPs) vary widely in length — with some exceeding 100,000 packets — we split each PCAP into smaller segments of up to 2,000 packets and randomly select at most 20 segments from each original PCAP. Additionally, since some labels contain significantly more PCAPs than others, we limit each label to a maximum of 60 PCAPs to ensure balanced representation across labels. Table 3 provides details about each dataset after this curation process.

For each dataset, we first group PCAPs by label. We then randomly select two labels and set aside all PCAPs from those labels as target holdout (non-member). The PCAPs associated with the remaining labels are split evenly (50/50) into two parts: one part is used to train the generative models (train set), and the other serves as the shadow train set (mimic members). Refer to Figure 1 for how each dataset is split.

## 4.3 Synthetic Trafic Generation

We train NetDifusion by fine-tuning Stable Difusion v1.5 using LoRA (Low-Rank Adaptation) with a batch size of 4. We train until the average loss over the most recent 100 epochs falls below 0.02 (an epoch is one complete pass over the training set). This empirically chosen threshold indicates a clear loss plateau across most datasets. For NetSSM, we use a batch size of 1 and train until the loss stabilizes over the most recent 4 epochs. Similarly, TraficLLM is fine-tuned from ChatGLM2-6B with a batch size of 1 and trained until the loss plateaus over the most recent 4 epochs. For NetShare, we adopt the default training configuration without Diferential Privacy (DP). Since GAN training involves adversarial optimization between a generator and a discriminator, both losses tend to oscillate rather than converge monotonically; therefore, we train until the losses stabilize and fluctuate around a consistent level.

After training trafic generative models, we generate synthetic trafic as follows. For NetDifusion, we generate 20 output images for each input image (where each image represents a multi-flow PCAP file). We select the output closest to the input based on pixel-wise L2 distance and apply the post-generation correction process to the selected image. For NetSSM and TraficLLM, we generate 30 output sequences per trafic label. This matches the approximate number of PCAPs per label in the training data, ensuring balanced sample representation across labels. For NetShare, we use the default setting where the number of flows generated is approximately equal to the number of flows in the input PCAP.

![](images/979eaed9ca23a83e621b8250c8fc4e8d44acf6a3b988fa1a74a1636672b650b4.jpg)

![](images/e6349bb94dd91a34b63b877dbbfa6bbf5f347f3ba0170a4cbd8aa3e5a4cf8a00.jpg)  
(a) MIA success  
(b) Data extraction success  
Figure 3: MIA and data extraction success across models and datasets.

## 5 How successful can each privacy attack be under the most challenging conditions for an attacker?

To address RQ1, we begin with a conservative setting in which the attacker is restricted to black-box access, and all generative models are trained for a single epoch. Under this setting, we observe that all models are under-trained. Refer to Section 6 for results when models are trained for extended epochs.

## 5.1 MIA Success Rate

Finding 1: MIA can be highly successful against NetSSM and NetShare on certain datasets.

Even under the setting where attacker only has black-box access and the model is under-trained, MIA is highly efec tive against NetSSM and NetShare on certain datasets. For NetSSM, TPR at $\mathrm { F P R } \leq 0 . 0 1$ can be as high as 0.88 on IoT dataset and for NetShare, TPR at $\mathrm { F P R } \leq 0 . 0 1$ reaches over 0.9 on USTC dataset. MIA is moderately efective against TraficLLM, but considerably less efective against NetDifu sion (Figure 3a). We hypothesize that these diferences arise from diferences in data encoding and model architecture. Compared to bit-level encoding in NetDifusion, byte-level or hexadecimal representations in NetSSM and TraficLLM may provide more informative representations of network trafic. Their language-based architectures may also better capture the sequential structure of network trafic than Net-Difusion. As such, MIA attacks tend to be more successful against NetSSM and TraficLLM than NetDifusion. How ever, the signals available to the MIA attacker also difer across models due to their diferent input/output representations. Thus, cross-model diferences in MIA success should be interpreted cautiously, as they do not isolate the efect of architecture alone.

Furthermore, the efectiveness of MIA varies substantially across datasets. For example, MIA achieves high success rates against NetShare on the USTC dataset, but performs poorly on other datasets. Similarly, MIA is highly successful against NetSSM on the IoT and SR datasets, while showing limited efectiveness on the remaining datasets. One possible explanation is the distribution diference between the train and holdout set for the features used by MIA attack. For instance, if the first packets of PCAPs from the train set closely resemble those from the holdout set, TraficLLM and NetSSM may struggle to distinguish between the train and holdout samples. Likewise, if flow-level features, such as the number of source IPs or packet counts, is highly similar, NetShare may fail to efectively diferentiate between them. Additional evidence supporting this explanation is provided in the Appendix Figure 12 and 13.

![](images/ff636e97f6f922d009e41d90150e894d6bccf1523e3b915fa21d8387277276aa.jpg)  
(a) NetSSM

![](images/662481ff844e603c3ab3f3226c7ec56e72a4ff47fd13acdb4dbc6889857c0e5c.jpg)  
(b) TraficLLM  
Figure 4: Extractable rate across diferent byte positions for NetSSM & TraficLLM. Higher extractable rate is observed at byte positions 1-9 and 26-33 for NetSSM.

## 5.2 Data Extraction Attack Success Rate

Finding 2: Data extraction attack is more successful against autoregressive models than difusion models. Categorical/identifier data are more likely to be memorized than continuous data.

Among the three packet-level generative models, NetDifusion is not vulnerable to data extraction attacks. This aligns with the design choice in NetDifusion: representing trafic as images at bit granularity removes explicit sequence structure, which likely makes verbatim packet-level memorization harder to sustain. In contrast, the extractable rate is notably high (≥ 0.4) for both NetSSM and TraficLLM which are autoregressive models. Refer to Figure 3b for more details about data extraction attack success. It is important to note that our extraction analysis uses each generator’s native output representation and token granularity, rather than a common unit. Thus, extraction rates are not directly comparable across generators.

We next analyze which byte positions in packet headers are most vulnerable to extraction. A position is defined as extractable if the next 10 contiguous tokens starting at that location appear identically in the training data at the same ofset (Figure 4). For NetSSM, extractable rates are consistently high at byte positions 1–9 and 26–33 across datasets, indicating these regions are more predictable and susceptible to memorization. These positions correspond primarily to identifier fields: bytes 1–9 map to Ethernet headers (source/destination MAC addresses and EtherType), while 26–33 map to network-layer fields such as source/destination IP addresses and related padding. In contrast, mid-range positions (e.g., 14–25), which include more continuous-valued fields such as packet size and TTL, show lower extractability due to higher variability and lower repetition. Overall, ex traction success is concentrated in categorical header fields, while continuous fields are substantially less vulnerable.

![](images/e5fc906388e76ddc1f0a9f60f2dda2b88a553236f27a43c61d154e0b8f670174.jpg)

![](images/2c3467fa87fb9586dab33d5954c279cf71308eb2bc95e650300979b8f0dd0807.jpg)  
(b) Recall

(a) Precision  
Figure 5: Precision and recall scores for source IP addresses across diferent models and datasets.  
![](images/4ca63f25db5db1fbe3e4366601cef8fb0b2530d70239147d3c7920f43c7815af.jpg)  
Figure 6: Distribution of memorized and non-memorized source IPs as a function of their frequency in the training data for dataset SR (Total number ofIPs = 227). Source IPs that appear more frequently in the training set are more likely to be memorized and reproduced in the generated output.

We also observe that TraficLLM exhibits a similar extractability pattern to NetSSM, with consistently high ex tractable rates at byte positions 1–15 (corresponding to bytes 1–20 in TraficLLM, since each token represents a hexadecimal digit). However, unlike NetSSM, it does not show simi larly high extractability at positions 26–33. This diference could be due to tokenization granularity: NetSSM operates at the byte level, whereas TraficLLM uses hexadecimal digit to kens, resulting in longer sequences for the same information and making exact memorization more dificult.

5.2.1 Network identifiers leakageSource and destination IP addresses show substantial leakage in both precision and recall metrics (Figure 5 for source IPs; Figure 14 in the Ap pendix for destination IPs). This leakage is most severe for NetSSM, followed by TraficLLM while not significant for NetShare. We hypothesize that precision and recall scores is low for Netshare because identifiers like source IP are encoded into vector embedding of lower precision, which reduce the risk of exact memorization of such fields. For NetSSM, precision scores on source IP exceed 0.8 on three of five datasets, indicating a high likelihood that any generated identifier appears in the training set. We also observe that recall scores is particular high for the SR and VNAT datasets (>0.3). We hypothesize that, since these datasets contain relatively fewer IP addresses than the other datasets, achieving high recall on these datasets is more tractable compared to datasets like USTC which contain thousands of unique IPs. Refer to Table 3 for number of identifiers in each dataset.

<table><tr><td>Feature</td><td>NetDiffusion</td><td>NetSSM</td><td>TrafficLLM</td><td>NetShare</td></tr><tr><td>Time to Live (TTL)</td><td>0.36</td><td>0.10</td><td>0.22</td><td>0.32</td></tr><tr><td>Identification (ID)</td><td>0.26</td><td>0.08</td><td>0.18</td><td>0.27</td></tr><tr><td>Type of Service (ToS)</td><td>0.17</td><td>0.06</td><td>0.11</td><td>0.27</td></tr><tr><td>TCP Window Size</td><td>0.14</td><td>0.12</td><td>0.25</td><td>-</td></tr><tr><td>TCP Control Flags</td><td>0.15</td><td>0.15</td><td>0.16</td><td>0.30</td></tr><tr><td>TCP Data Offset</td><td>0.16</td><td>0.28</td><td>0.14</td><td>0.50</td></tr><tr><td>Flow Size</td><td>-</td><td>0.05</td><td>-</td><td>0.13</td></tr><tr><td>Packet Size</td><td>0.14</td><td>0.12</td><td>-</td><td>0.28</td></tr></table>

Table 4: Normalized EMD between the original and generated distributions for each sensitive feature. Bolded values indicate the lowest distance (more leakage) for each feature.

<table><tr><td rowspan="2">Traffic Dataset</td><td colspan="2">Degree distribution distance</td></tr><tr><td>MAC-based</td><td>IP-based</td></tr><tr><td>IoT</td><td>0.04</td><td>0.01</td></tr><tr><td>SR</td><td>0.05</td><td>0.04</td></tr><tr><td>VNAT</td><td>0.17</td><td>0.04</td></tr><tr><td>USTC</td><td>0.19</td><td>0.01</td></tr><tr><td>CIC</td><td>0.40</td><td>0.00</td></tr></table>

Table 5: Normalized EMD of node degree distributions across training and generated topologies.

Furthermore, we observe that identifiers appearing with higher frequency in training data are more likely to be memorized (refer to Figure 6 for an example). For example, source IPs appearing more than 1,000 times in the training data show substantially higher memorization rates compared to those with lower frequencies. This pattern reveals a critical privacy vulnerability: frequently occurring network identifiers, which often correspond to important servers, major clients, or central network infrastructure, face disproportionately higher exposure risks.

5.2.2 Network properties leakageThe EMD between training and generated data can be as low as 0.10 or less for four key properties (TTL, ID, Flow Size, and ToS), indicating that these features can remain highly useful for fingerprinting attacks. Note that the EMD for Flow Size is unavailable for NetDifusion, which removes IP addresses used for flow identification, and for TraficLLM, which generates only the first packet. Across all four generative models, NetSSM exhibits the greatest privacy leakage (lowest EMD). For the other three models, leakage varies by feature: some features show substantially higher distances while others remain closely matched to the training distribution. NetShare, a flow-based generative method, exhibits the largest distribution distance overall, suggesting relatively better privacy preservation for sensitive properties compared to packet-based generative models. Refer to Table 4 for details.

![](images/4ad385723849a2837ea9636de193feb4d517897d8c31d09de1b79e50777c044f.jpg)  
Figure 7: Topology overlap rate (nodes and edges) for IP-based and MAC-based communications across diferent datasets for NetSSM.

![](images/ded9197479739c33f60deffc0d7c8d80963e5bb349b5fc124d121e183284e2aa.jpg)  
Figure 8: Distribution of memorized and non- memorized edge as a function of their frequency in the training data for dataset SR. Edges that appear more frequently in the training set (belong to larger flows) are more likely to be memorized and reproduced in the generated output.

## Finding 3: High trafic volume and highly connected nodes are likely to be exposed in generated topologies.

5.2.3 Network topology leakageNetShare demonstrates minimal network topology leakage with very low node and edge overlap rates, which is non-surprising as it does not leak network identifiers (refer to Figure 5). In contrast, trafic generated by NetSSM exhibits substantial topology leakage (see Figure 7 for details). For IP-based topologies, NetSSM achieves node overlap rates up to 0.4 and edge overlap rates up to 0.35. For MAC-based topologies, overlap rates reach 1.0 for both nodes and edges, indicating complete topology reconstruction. The low degree-distribution EMD further suggests that the generated topologies closely preserve the training graph structure.

These high topology overlap rates demonstrate that NetSSM memorizes and reproduces significant portions of the network topology, including key entities and their communication patterns. Manual inspection shows that overlapped IP nodes are high-volume endpoints, such as external CDN, cloud infrastructure servers and a substantial number of pri vate IP addresses linked to high-volume flows. For example, in the SR dataset, we identify multiple private IPs associated with personal devices generating large volume of trafic for applications such as Zoom and Google Meet.

![](images/d2e9f99c51e672c5828b601179985ec4ee4a40f1dc4685d56bc877118a02db9a.jpg)  
(a) White-box vs black-box

![](images/6f82943424297b80460b1332dabead3501100c85919905cc3a2ad9b0af8c8947.jpg)  
(b) Number of training epochs

Figure 9: Impact of diferent experimental conditions on MIA efectiveness.  
![](images/6d4afe7b0da2ad1711b44db5c429978e4bfc686e4ae60c6382396fe2e8b31b99.jpg)  
(a) Number of training epochs

![](images/bfef7e029ae871f5f85e3757f0d95dc9923c65e156a9061716695efe43b0a1f6.jpg)  
(b) Number of outputs  
Figure 10: Impact of diferent experimental conditions on data extraction success.

## 6 Which factors determine the success of privacy attacks?

## 6.1 Factors Afecting MIA

Finding 4: White-box access can substantially increase MIA efectiveness against NetSSM and NetDifusion.

White-box access increases TPR at $\mathrm { F P R } \leq 0 . 0 1$ by an average of 0.15 for NetDifusion and NetSSM, indicating that attacker access level is a significant factor influencing MIA success for these models. In contrast, MIA success for TrafficLLM remains largely unchanged between black-box and white-box settings, suggesting that access level has little influence on attack efectiveness for this model. See Figure 9a for details.

Although training generative models for more epochs can slightly increase MIA success for some models, the overall efect is modest. For NetSSM, TPR at FPR ≤ 0.01 is already about 0.40 after one epoch and increases only marginally to around 0.45 at full convergence. For NetShare, TPR rises from 0.25 at epoch 1 to approximately 0.40 as training completes. TraficLLM shows relatively stable performance, with TPR fluctuating between 0.10 and 0.20 across epochs, while NetDifusion remains resistant to MIA, maintaining TPR below 0.07 throughout training. Overall, although extended training can increase MIA success, the gains are limited, suggesting that models already capture membership signals early in training (Figure 9b).

## 6.2 Factors Afecting Data Extraction

Training for more epochs substantially increases data extraction vulnerability in NetSSM and TraficLLM. From 1 to 10 epochs, extractable rates rise from 0.65 to 1.0 for NetSSM and from 0.27 to 0.73 for TraficLLM, then largely saturate. In contrast, NetDifusion remains near zero across all stages, indicating strong resistance to extraction. Overall, longer training increases extraction risk, particularly for under-trained NetSSM and TraficLLM models (Figure 10a).

![](images/e14e98920e4ae4d4a6739885089d9aece7223373da3cf8da73fb0f5e9f47c021.jpg)  
(a) Precision

![](images/8ee077fd84b7f68bed0ea28870f05b20ec89f7170496736d27799cba91eab31c.jpg)  
(b) Recall  
Figure 11: Impact of the number of training epochs on preci sion and recall scores for source IP address.

Increasing number of generated outputs can also increase data extractability, although to limited extent. For example, for NetSSM, data extractability can increase from 0.52 to 0.73 when number of generated outputs increase from 1 to 50. TraficLLM increases more moderately, from approximately 0.27 to a peak of around 0.42 at 20 outputs, before slightly declining to approximately 0.35 at 50 outputs. In contrast, NetDifusion remains near 0 regardless of the number of outputs, demonstrating consistent resistance to data extraction. Refer to Figure 10b for details.

## 6.3 Factors Afecting Network-specific

NetSSM exhibits high vulnerability to source IP extraction. Starting at epoch 1, its precision score already reaches 0.78 and steadily increases to near-perfect levels by epoch 20. Its recall score also increases substantially, from 0.13 at epoch 1 to around 0.63 at epoch 50. This suggests that additional training epochs not only improve memorization accuracy but also increase the number of identifiers memorized by the model. The precision score for TraficLLM also increases with additional training epochs, rising from 0.27 at epoch 1 to around 0.80 by epoch 10 before stabilizing. In contrast, although both the precision and recall scores for NetShare increase with additional training epochs, they remain low overall, reaching only around 0.10 for precision and 0.18 for recall, indicating strong resistance to source IP extraction. Overall, these results suggest that the degree of model fitting afects not only precision but also recall across all three models. Refer to Figure 11 for more details.

We also found that the number of generated output does not significantly impact network identifier meorization. Refer to Appendix Figure 15 for more details.

## 7 What is the privacy-utility tradeof when applying privacy mitigation techniques?

To address RQ3, we evaluate how privacy mitigation strategies afect both privacy risks and downstream utility. We focus on NetSSM, as it exhibits the strongest leakage across the studied attacks, and evaluate it under both multi-flow and single-flow generation settings. To ensure a fair comparison between these settings, we evaluate mitigation strategies only on the SR and IoT datasets, where labels are available for the single-flow setting.

As described in Section 3.2, we apply three anonymization techniques: Complete Anonymization (CA), Pseudonymization (PS), and Prefix-preserving (PP). For DP-noise mitigation, we consider two privacy budgets, $\epsilon = 0 . 1$ (stronger privacy) and � = 1 (weaker privacy). We evaluate the impact of these mitigation methods on privacy across five datasets, while the impact on utility is assessed only on the IoT and SR datasets.

## 7.1 Impact of Anonymization Techniques

Finding 5: Anonymization techniques significantly reduce MIA and data extraction success.

Across both multi-flow and single-flow settings, all three anonymization strategies eliminate the risks of data extraction and network identifier attacks. The extractability dropping to 0 as network identifiers are removed indicate that header-level memorization is strongly tied to raw identifiers. Interestingly, anonymization also substantially reduces MIA success in both the single-flow (by 0.24–0.37) and multi-flow (0.23–0.44) settings. This likely occurs because the model is trained on anonymized tokens and therefore learns representations aligned with the anonymized distribution rather than the original data. As a result, it produces weaker membership signals with respect to the original data, making training samples harder to distinguish from non-members. Anonymization techniques, however, do not protect sensitive network properties, as reflected by near-zero changes in EMD across all methods (CA, PP, and PS).

With respect to data utility, anonymization techniques reduce both fidelity and downstream accuracy in the multi-flow and single-flow settings. Compared to DP-noise mitigation techniques, anonymization tends to cause a larger drop in fidelity but a smaller reduction in downstream accuracy. One possible explanation is that anonymization mainly alters network identifier distributions which is used to calculate fidelity, while preserving non-identifier fields that are used for downstream tasks.

## 7.2 Impact of Noise-addition Techniques

Finding 6: DP noise protects against network properties inference attack but not other privacy attacks.

In both the single-flow and multi-flow settings, adding DP noise has negligible impact on data extraction success as well as on the precision and recall of source IP address identification, with changes remaining near zero across these attacks. However, DP noise was not applied to IP or MAC address fields; therefore, these extraction and identification results should not be interpreted as evidence that DP protects these identifiers. Although MIA success decreases slightly, the reduction is substantially smaller than that achieved by anonymization-based methods. However, DP-noise is more efective at reducing privacy risks of sensitive network properties. DP-noise reduces EMD for both multi-flow and singleflow setting with lower privacy budget (stronger privacy) generally produce larger EMD reductions.

<table><tr><td rowspan="3">Generation task</td><td rowspan="3">Mitigation strategy</td><td rowspan="3">Detail</td><td colspan="5">Privacy attack (↓ more private)</td><td colspan="2">Utility (↑ more utility)</td></tr><tr><td rowspan="2">MIA</td><td rowspan="2">Extraction</td><td colspan="3">Network</td><td rowspan="2">Fidelity</td><td rowspan="2">Accuracy</td></tr><tr><td>EMD</td><td>Precision</td><td>Recall</td></tr><tr><td rowspan="6">Multi-flow</td><td colspan="2">No-mitigation</td><td>0.81</td><td>0.66</td><td>0.10</td><td>0.94</td><td>0.18</td><td>0.12</td><td>0.64</td></tr><tr><td rowspan="3">Anonymization</td><td>Complete anonymization (CA)</td><td>↓-0.23</td><td>↓-0.66</td><td>↓-0.01</td><td>↓-0.94</td><td>↓-0.18</td><td>-0.05</td><td>-0.03</td></tr><tr><td>Pseudonymization (PS)</td><td>↓-0.44</td><td>↓-0.66</td><td>0.00</td><td>↓-0.94</td><td>↓-0.18</td><td>-0.06</td><td>-0.04</td></tr><tr><td>Prefix-preserving (PP)</td><td>↓-0.37</td><td>↓-0.66</td><td>+0.01</td><td>↓-0.94</td><td>↓-0.18</td><td>0.00</td><td>-0.01</td></tr><tr><td rowspan="2">DP-Noise</td><td>ε = 0.1</td><td>↓-0.06</td><td>↓-0.06</td><td>↓-0.11</td><td>+0.02</td><td>+0.01</td><td>0.00</td><td>-0.08</td></tr><tr><td>ε = 1</td><td>↓-0.06</td><td>↓-0.14</td><td>↓-0.08</td><td>↓-0.01</td><td>0.00</td><td>↑+0.02</td><td>-0.08</td></tr><tr><td rowspan="6">Single-flow</td><td colspan="2">No-mitigation</td><td>0.37</td><td>0.99</td><td>0.12</td><td>0.94</td><td>0.35</td><td>0.18</td><td>0.79</td></tr><tr><td rowspan="3">Anonymization</td><td>Complete anonymization (CA)</td><td>↓-0.37</td><td>↓-0.99</td><td>0.00</td><td>↓-0.94</td><td>↓-0.35</td><td>-0.05</td><td>-0.02</td></tr><tr><td>Pseudonymization (PS)</td><td>↓-0.36</td><td>↓-0.99</td><td>0.00</td><td>↓-0.94</td><td>↓-0.35</td><td>-0.03</td><td>-0.02</td></tr><tr><td>Prefix-preserving (PP)</td><td>↓-0.24</td><td>↓-0.99</td><td>+0.02</td><td>↓-0.94</td><td>↓-0.35</td><td>0.00</td><td>-0.04</td></tr><tr><td rowspan="2">DP-Noise</td><td>ε = 0.1</td><td>↓-0.08</td><td>↓-0.01</td><td>↓-0.10</td><td>0.00</td><td>0.00</td><td>0.00</td><td>-0.07</td></tr><tr><td>ε = 1</td><td>0.01</td><td>↓-0.02</td><td>↓-0.02</td><td>↓-0.06</td><td>↓-0.01</td><td>↑+0.01</td><td>-0.07</td></tr></table>

Table 6: Impact of mitigation techniques on privacy and utility averaged across IoT and SR datasets. For each column, bold values indicate the most ideal case (either biggest drop in privacy risks or lowest drop in data utility). Highlighted values denote the original results before mitigation. Non-highlighted show the absolute change relative to the original results. For EMD and Fidelity, changes are reported in negated form for consistency.

With respect to utility, DP-noise generally has little im pact on fidelity but causes a larger reduction in downstream accuracy compared to anonymization. One possible explanation is that noise addition perturbs non-identifier features that are important for downstream tasks, thereby afecting task accuracy more directly.

## 8 Discussion

Limitations Our extraction analysis identifies contiguous matches of at least 10 tokens in each generator’s native representation, rather than comparing parsed packet fields. Because token granularity difers across models, a 10-token match does not represent the same amount of information; thus, extraction rates indicate within-model memorization and are not directly comparable across architectures. Additionally, our topology analysis does not consider cross-flow correlation attack which could amplify topology leakage by exploiting relationships across flows.

Privacy From Multiple Perspectives Our findings high light the need to evaluate privacy beyond MIA and data extraction. Quantifying real-world privacy risks in network trafic is essential for designing efective mitigations. For example, DP noise alone does not prevent data extraction or identifier memorization, while anonymization alone does not prevent inference of sensitive distributions.

The Dual Nature of Privacy and Fidelity. Beyond privacy, synthetic trafic must retain suficient utility for downstream applications. However, privacy and fidelity are often in tension: features that improve fidelity can also increase privacy risks. For example, accurately reproducing flow durations, packet inter-arrival times, or port usage may benefit intrusion detection and QoS analysis, but can also enable adversaries to infer sensitive network topology and user behavior. Thus, improving fidelity may increase privacy risks, while stronger protections may reduce utility, requiring careful consideration of the use case and threat model.

Context-Aware Privacy-Utility Tradeof. Ultimately, the choice of trafic generators, evaluation metrics, and mitigation techniques should depend on the specific use case, threat model, and sharing context. For internal use in trusted environments, fine-grained models such as NetSSM can preserve rich packet-level features to support comprehensive analysis. In contrast, external or public sharing requires stronger protections, including coarser-grained generators such as NetDifusion and NetShare, anonymization of critical infrastructure, and diferential privacy noise on sensitive features, albeit with reduced utility.

## 9 Conclusion

This paper systematically evaluates privacy risks in synthetic network trafic using membership inference, data extraction, and network-specific attacks. Across four generators and five datasets, we show that synthetic traces can leak membership, memorize training data, and reproduce network identifiers and communication structure. We further examine how attacker access, training duration, data diversity, and mitigations shape these risks and the privacy–utility tradeof. Overall, our findings show that synthetic network traces should be treated as security-sensitive data, not inherently safe substitutes for raw trafic.

## Code Availability

We release our code and evaluation framework to support reproducibility and facilitate future research. The code is available at https://github.com/VanTranHong/IMC-26-privacytrafic-generator.

## Acknowledgement

This work was supported in part by the National Science Foundation ACTION under Grant No. IIS-2229876 and the National Science Foundation and the Faculty of Engineering Interdisciplinary Fund at The University of Hong Kong.

## References

[1] S. E. Coull, C. V. Wright, F. Monrose, M. P. Collins, M. K. Reiter et al., “Playing devil’s advocate: Inferring sensitive information from anonymized network traces.” in Ndss, vol. 7, 2007, pp. 35–47.

[2] Boson, “Netsimtm network simulatortm & router simulator,” https: //www.boson.com/netsim-cisco-network-simulator, n.d, accessed Oct 2, 2025.

[3] Y. Yin, Z. Lin, M. Jin, G. Fanti, and V. Sekar, “Practical gan-based synthetic ip header trace generation using netshare,” in Proceedings of the ACM SIGCOMM 2022 Conference, 2022, pp. 458–472.

[4] X. Jiang, S. Liu, A. Gember-Jacobson, A. N. Bhagoji, P. Schmitt, F. Bronzino, and N. Feamster, “Netdifusion: Network data augmenta tion through protocol-constrained trafic generation,” Proceedings of the ACM on Measurement and Analysis of Computing Systems, vol. 8, no. 1, pp. 1–32, 2024.

[5] M. Endres, A. Mannarapotta Venugopal, and T. S. Tran, “Synthetic data generation: A comparative study,” in Proceedings of the 26th International Database Engineered Applications Symposium, ser. IDEAS ’22. New York, NY, USA: Association for Computing Machinery, 2022, p. 94–102. [Online]. Available: https://doi.org/10.1145/3548785.3548793

[6] Z. Sarwar, V. Tran, A. N. Bhagoji, N. Feamster, B. Y. Zhao, and S. Chakraborty, “Mycroft: Towards efective and eficient external data augmentation,” arXiv preprint arXiv:2410.08432, 2024.

[7] B. Van Breugel, H. Sun, Z. Qian, and M. van der Schaar, “Membership inference attacks against synthetic data through overfitting detection,” arXiv preprint arXiv:2302.12580, 2023.

[8] B. Hilprecht, M. Härterich, and D. Bernau, “Monte carlo and recon struction membership inference attacks against generative models,” Proceedings on Privacy Enhancing Technologies, 2019.

[9] J. Hayes, L. Melis, G. Danezis, and E. De Cristofaro, “Logan: Mem bership inference attacks against generative models,” arXiv preprint arXiv:1705.07663, 2017.

[10] J. Zhou, Y. Chen, C. Shen, and Y. Zhang, “Property inference attacks against gans,” arXiv preprint arXiv:2111.07608, 2021.

[11] A. Chu, X.Jiang, S. Liu, A. Bhagoji, F. Bronzino, P. Schmitt, and N. Feamster, “Netssm: Multi-flow and state-aware network trace generation using state-space models,” arXiv preprint arXiv:2503.22663, 2025.

[12] T. Cui, X. Lin, S. Li, M. Chen, Q. Yin, Q. Li, and K. Xu, “Traficllm: Enhancing large language models for network trafic analysis with generic trafic representation,” arXiv preprint arXiv:2504.04222, 2025.

[13] D. Sun, J. Q. Chen, C. Gong, T. Wang, and Z. Li, “Netdpsyn: synthesizing network traces under diferential privacy,” in Proceedings of the 2024 ACM on Internet Measurement Conference, 2024, pp. 545–554.

[14] M. Jin, H. He, and M. Apostolaki, “Assessing user privacy leakage in synthetic packet traces: An attack-grounded approach,” arXiv preprint arXiv:2508.11742, 2025.

[15] R. Li, Q. Li, T. Lin, Q. Zou, D. Zhao, Y. Huang, G. Tyson, G. Xie, and Y. Jiang, “Deviceradar: Online iot device fingerprinting in isps using programmable switches,” IEEE/ACM Transactions on Networking, vol. 32, no. 5, pp. 3854–3869, 2024.

[16] E. Maali, O. Alrawi, and J. McCann, “Evaluating machine learningbased iot device identification models for security applications,” arXiv preprint, 2025.

[17] Y. Yao, J. Hou, M. Yuan, H. Zhang, Z. Xu, and X.-Y. Li, “Traficdiary: User attribute inference based on smart home trafic traces,” ACM Transactions on Internet Technology, 2025.

[18] H. Hu and J. Pang, “Membership inference of difusion models,” arXiv preprint arXiv:2301.09956, 2023.

[19] M. Duan, A. Suri, N. Mireshghallah, S. Min, W. Shi, L. Zettlemoyer, Y. Tsvetkov, Y. Choi, D. Evans, and H. Hajishirzi, “Do membership inference attacks work on large language models?” arXiv preprint arXiv:2402.07841, 2024.

[20] J. Hayase, A. Liu, Y. Choi, S. Oh, and N. A. Smith, “Data mixture inference attack: Bpe tokenizers reveal training data compositions,” Advances in Neural Information Processing Systems, vol. 37, pp. 8956– 8983, 2024.

[21] Y.-C. Chen, Y. Liao, M. Baldi, S.-J. Lee, and L. Qiu, “Os fingerprinting and tethering detection in mobile networks,” in Proceedings ofthe 2014 Conference on Internet Measurement Conference, 2014, pp. 173–180.

[22] S. Bai, H. Kim, and J. Rexford, “Passive os fingerprinting on commodity switches,” in 2022 IEEE 8th International Conference on Network Softwarization (NetSoft). IEEE, 2022, pp. 264–268.

[23] H. Li, Z. Xu, H. Zhu, D. Ma, S. Li, and K. Xing, “Demographics inference through wi-fi network trafic analysis,” in IEEE INFOCOM 2016 - The 35th Annual IEEE International Conference on Computer Communications. IEEE Press, 2016, p. 1–9. [Online]. Available: https://doi.org/10.1109/INFOCOM.2016.7524528

[24] B. Yao, R. Viswanathan, F. Chang, and D. Waddington, “Topology inference in the presence of anonymous routers,” in IEEE INFOCOM 2003. Twenty-second Annual Joint Conference of the IEEE Computer and Communications Societies (IEEE Cat. No. 03CH37428), vol. 1. IEEE, 2003, pp. 353–363.

[25] H. B. Acharya and M. G. Gouda, “On the hardness of topology inference,” in Proceedings of the 12th International Conference on Distributed Computing and Networking, ser. ICDCN’11. Berlin, Heidelberg: Springer-Verlag, 2011, p. 251–262.

[26] X. Zeng, R. Bagrodia, and M. Gerla, “Glomosim: a library for parallel simulation of large-scale wireless networks,” in Proceedings of the twelfth workshop on Parallel and distributed simulation, 1998, pp. 154– 161.

[27] T. R. Henderson, M. Lacage, G. F. Riley, C. Dowell, and J. Kopena, “Network simulations with the ns-3 simulator,” SIGCOMM demonstration, vol. 14, no. 14, p. 527, 2008.

[28] OMNeT++, “Omnet discreet event simulator,” https://omnetpp.org/, n.d, accessed Oct 2, 2025.

[29] M. Lacage and T. R. Henderson, “Yet another network simulator,” in Proceedings of the 2006 Workshop on ns-3, 2006, pp. 12–es.

[30] Riley, “Large-scale network simulations with gtnets,” in Proceedings of the 2003 Winter Simulation Conference, 2003., vol. 1. IEEE, 2003, pp. 676–684.

[31] A. H. Buss and K. A. Stork, “Discrete-event simulation on the world wide web using java,” in Proceedings of the 28th conference on Winter Simulation, 1996, pp. 780–785.

[32] H. Redžović, A. Smiljanić, and M. Bjelica, “Ip trafic generator based on hidden markov models,” parameters, vol. 1, no. 2, p. 1, 2017.

[33] S. Xu, M. Marwah, M. Arlitt, and N. Ramakrishnan, “Stan: Synthetic network trafic generation with generative neural models,” in International Workshop on Deployable Machine Learning for Security Defense.

Springer, 2021, pp. 3–29.

[34] Z. Lin, A. Jain, C. Wang, G. Fanti, and V. Sekar, “Using gans for sharing networked time series data: Challenges, initial promise, and open questions,” in Proceedings of the ACM internet measurement conference, 2020, pp. 464–483.

[35] P. Wang, S. Li, F. Ye, Z. Wang, and M. Zhang, “Packetcgan: Exploratory study of class imbalance for encrypted trafic classification using cgan,” in ICC 2020-2020 IEEE International Conference on Communications (ICC). IEEE, 2020, pp. 1–7.

[36] S. Zhang, T. Li, D. Jin, and Y. Li, “Netdif: a service-guided hierarchical difusion model for network flow trace generation,” Proceedings ofthe ACM on Networking, vol. 2, no. CoNEXT3, pp. 1–21, 2024.

[37] N. Sivaroopan, D. Bandara, C. Madarasingha, G. Jourjon, A. P. Jaya sumana, and K. Thilakarathna, “Netdifus: Network trafic generation by difusion models through time-series imaging,” Computer Networks, vol. 251, p. 110616, 2024.

[38] N. Kan, S. Yan, J. Zou, W. Dai, X. Gao, C. Li, and H. Xiong, “Gdplan: Gen erative network planning via graph difusion model,” IEEE Transactions on Networking, vol. 33, no. 4, pp. 1422–1437, 2025.

[39] X. Meng, C. Lin, Y. Wang, and Y. Zhang, “Netgpt: Generative pretrained transformer for network trafic,” arXiv preprint arXiv:2304.09513, 2023.

[40] J. Qu, X. Ma, and J. Li, “Traficgpt: Breaking the token barrier for eficient long trafic analysis and generation,” arXiv preprint arXiv:2403.05822, 2024.

[41] A. Jagannatha, B. P. S. Rawat, and H. Yu, “Membership inference attack susceptibility of clinical language models,” arXiv preprint arXiv:2104.08305, 2021.

[42] S. Yeom, I. Giacomelli, M. Fredrikson, and S. Jha, “Privacy risk in machine learning: Analyzing the connection to overfitting,” in 2018 IEEE 31st Computer Security Foundations Symposium (CSF), 2018, pp. 268–282.

[43] Y. Pang and T. Wang, “Black-box membership inference attacks against fine-tuned difusion models,” arXiv preprint arXiv:2312.08207, 2023.

[44] N. Carlini, F. Tramer, E. Wallace, M. Jagielski, A. Herbert-Voss, K. Lee, A. Roberts, T. Brown, D. Song, U. Erlingsson et al., “Extracting training data from large language models,” in 30th USENIX security symposium (USENIX Security 21), 2021, pp. 2633–2650.

[45] M. Meeus, S. Jain, M. Rei, and Y.-A. de Montjoye, “Did the neurons read your book? document-level membership inference for large language models,” in 33rd USENIX Security Symposium (USENIX Security 24). Philadelphia, PA: USENIX Association, Aug. 2024, pp. 2369–2385. [Online]. Available: https://www.usenix.org/conference/ usenixsecurity24/presentation/meeus

[46] R. Shokri, M. Stronati, C. Song, and V. Shmatikov, “Membership infer ence attacks against machine learning models,” in 2017 IEEE symposium on security and privacy (SP). IEEE, 2017, pp. 3–18.

[47] A. Salem, Y. Zhang, M. Humbert, P. Berrang, M. Fritz, and M. Backes, “Ml-leaks: Model and data independent membership inference at tacks and defenses on machine learning models,” arXiv preprint arXiv:1806.01246, 2018.

[48] J. Duan, F. Kong, S. Wang, X. Shi, and K. Xu, “Are difusion models vul nerable to membership inference attacks?” in International Conference on Machine Learning. PMLR, 2023, pp. 8717–8730.

[49] T. Matsumoto, T. Miura, and N. Yanai, “Membership inference attacks against difusion models,” in 2023 IEEE Security and Privacy Workshops (SPW). IEEE, 2023, pp. 77–83.

[50] Z. Song, S. Huang, and Z. Kang, “Em-mias: Enhancing membership in ference attacks in large language models through ensemble modeling,” in ICASSP 2025-2025 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2025, pp. 1–5.

[51] H. Mozafari and V. J. Marathe, “Semantic membership inference attack against large language models,” arXiv preprint arXiv:2406.10218, 2024.

[52] D. Ran, X. He, T. Cong, A. Wang, Q. Li, and X. Wang, “Lora-leak: Membership inference attacks against lora fine-tuned language models,” arXiv preprint arXiv:2507.18302, 2025.

[53] J. Mattern, F. Mireshghallah, Z. Jin, B. Schölkopf, M. Sachan, and T. Berg-Kirkpatrick, “Membership inference attacks against language models via neighbourhood comparison,” arXiv preprint arXiv:2305.18462, 2023.

[54] J. Ren, K. Chen, C. Chen, V. Sehwag, Y. Xing, J. Tang, and L. Lyu, “Selfcomparison for dataset-level membership inference in large (vision-) language model,” in Proceedings of the ACM on Web Conference 2025, 2025, pp. 910–920.

[55] M. Nasr, N. Carlini, J. Hayase, M. Jagielski, A. F. Cooper, D. Ippolito, C. A. Choquette-Choo, E. Wallace, F. Tramèr, and K. Lee, “Scalable extraction of training data from (production) language models,” arXiv preprint arXiv:2311.17035, 2023.

[56] N. Carlini, J. Hayes, M. Nasr, M. Jagielski, V. Sehwag, F. Tramer, B. Balle, D. Ippolito, and E. Wallace, “Extracting training data from difusion models,” in 32nd USENIX security symposium (USENIX Security 23), 2023, pp. 5253–5270.

[57] R. Liu, D. Wang, Y. Ren, Z. Wang, K. Guo, Q. Qin, and X. Liu, “Unstoppable attack: Label-only model inversion via conditional difusion model,” IEEE Transactions on Information Forensics and Security, vol. 19, pp. 3958–3973, 2024.

[58] B. Yan, K. Li, M. Xu, Y. Dong, Y. Zhang, Z. Ren, and X. Cheng, “On protecting the data privacy of large language models (llms): A survey,” arXiv preprint arXiv:2403.05156, 2024.

[59] Y. Zhang, R. Jia, H. Pei, W. Wang, B. Li, and D. Song, “The secret revealer: Generative model-inversion attacks against deep neural networks,” in Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 2020, pp. 253–261.

[60] H. Hu and J. Pang, “Model extraction and defenses on generative adversarial networks,” arXiv preprint arXiv:2101.02069, 2021.

[61] P. Tinsley, A. Czajka, and P. Flynn, “This face does not exist... but it might be yours! identity leakage in generative models,” in Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision (WACV), January 2021, pp. 1320–1328.

[62] K. Ganju, Q. Wang, W. Yang, C. A. Gunter, and N. Borisov, “Property inference attacks on fully connected neural networks using permutation invariant representations,” in Proceedings of the 2018 ACM SIGSAC conference on computer and communications security, 2018, pp. 619–633.

[63] M. Fredrikson, S. Jha, and T. Ristenpart, “Model inversion attacks that exploit confidence information and basic countermeasures,” in Proceedings of the 22nd ACM SIGSAC conference on computer and communications security, 2015, pp. 1322–1333.

[64] L. Wang, J. Wang, J. Wan, L. Long, Z. Yang, and Z. Qin, “Property existence inference against generative models,” in 33rd USENIXSecurity Symposium (USENIX Security 24), 2024, pp. 2423–2440.

[65] J. Powar and A. R. Beresford, “Sok: Managing risks of linkage attacks on data privacy,” Proceedings on Privacy Enhancing Technologies, 2023.

[66] M. Giomi, F. Boenisch, C. Wehmeyer, and B. Tasnádi, “A unified framework for quantifying privacy risk in synthetic data,” arXiv preprint arXiv:2211.10459, 2022.

[67] S. E. Oh, S. Sunkam, and N. Hopper, “p-fp: Extraction, classification, and prediction of website fingerprints with deep learning,” arXiv preprint arXiv:1711.03656, 2017.

[68] V. Mavroudis and J. Hayes, “Adaptive webpage fingerprinting from tls traces,” in 2023 53rd Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN). IEEE, 2023, pp. 445–458.

[69] J. J. M. Ammar and S. Moon, “Prefix-preserving ip address anonymization: Measurement-based security evaluation and a new cryptographybased scheme,” in Proc. IEEE Int’l Conf. Network Protocols, 2002.

[70] M. Foukarakis, D. Antoniades, and M. Polychronakis, “Deep packet anonymization,” in Proceedings of the Second European Workshop on System Security, ser. EUROSEC ’09. New York, NY, USA: Association for Computing Machinery, 2009, p. 16–21. [Online]. Available: https://doi.org/10.1145/1519144.1519147

[71] A. J. Slagell, K. Lakkaraju, and K. Luo, “Flaim: A multi-level anonymiza tion framework for computer and network logs.” in LISA, vol. 6, 2006, pp. 3–8.

[72] A. Aleroud, F. Yang, S. C. Pallaprolu, Z. Chen, and G. Karabatis, “Anonymization of network traces data through condensation-based diferential privacy,” Digital Threats: Research and Practice (DTRAP), vol. 2, no. 4, pp. 1–23, 2021.

[73] ——, “Anonymization of network traces data through condensation based diferential privacy,” Digital Threats: Research and Practice, vol. 2, no. 4, 12 2021.

[74] F. McSherry and R. Mahajan, “Diferentially-private network trace analysis,” ACM SIGCOMM Computer Communication Review, vol. 40, no. 4, pp. 123–134, 2010.

[75] C. Chen, D. E. Asoni, A. Perrig, D. Barrera, G. Danezis, and C. Troncoso, “Taranet: Trafic-analysis resistant anonymity at the network layer,” in 2018 IEEE European Symposium on Security and Privacy (EuroS&P). IEEE, 2018, pp. 137–152.

[76] X. Cai, R. Nithyanand, and R. Johnson, “Cs-buflo: A congestion sensitive website fingerprinting defense,” in Proceedings ofthe 13th Workshop on Privacy in the Electronic Society, 2014, pp. 121–130.

[77] T. Wang and I. Goldberg, “{Walkie-Talkie}: An eficient defense against passive website fingerprinting attacks,” in 26th USENIX Security Symposium (USENIX Security 17), 2017, pp. 1375–1390.

[78] G. Zhu, D. Li, H. Gu, Y. Yao, L. Fan, and Y. Han, “Fedmia: An efec tive membership inference attack exploiting" all for one" principle in federated learning,” in Proceedings of the Computer Vision and Pattern Recognition Conference, 2025, pp. 20 643–20 653.

[79] A. Kowalczuk, J. Dubiński, F. Boenisch, and A. Dziedzic, “Privacy at tacks on image autoregressive models,” arXiv preprint arXiv:2502.02514, 2025.

[80] N. Carlini, S. Chien, M. Nasr, S. Song, A. Terzis, and F. Tramer, “Mem bership inference attacks from first principles,” in 2022 IEEE symposium on security and privacy (SP). IEEE, 2022, pp. 1897–1914.

[81] N. Lukas, A. Salem, R. Sim, S. Tople, L. Wutschitz, and S. Zanella-Béguelin, “Analyzing leakage of personally identifiable information in language models,” in 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 2023, pp. 346–363.

[82] Y. Rubner, C. Tomasi, and L. Guibas, “A metric for distributions with applications to image databases,” in Sixth International Conference on Computer Vision (IEEE Cat. No.98CH36271), 1998, pp. 59–66.

[83] N. Spring, R. Mahajan, D. Wetherall, and T. Anderson, “Measuring isp topologies with rocketfuel,” IEEE/ACM Transactions on Networking, vol. 12, no. 1, pp. 2–16, 2004.

[84] Y. Zhang and V. Paxson, “Detecting stepping stones.” in USENIX Security Symposium, vol. 171, 2000, p. 184.

[85] S. Soltani, A. Amanlou, M. Shojafar, and R. Tafazolli, “Security of topol ogy discovery service in sdn: Vulnerabilities and countermeasures,” IEEE Open Journal ofthe Communications Society, vol. 5, pp. 3410–3450, 2024.

[86] H. Zaw and A. H. Maw, “Trafic management with elephant flow detection in software defined networks (sdn),” International Journal of Electrical and Computer Engineering (IJECE), 2019. [Online]. Available: https://api.semanticscholar.org/CorpusID:208083142

[87] OWASP Foundation, “Owasp machine learning security top 10,” https: //owasp.org/www-project-machine-learning-security-top-10/, 2023, accessed: 2026-05-20.

[88] National Institute of Standards and Technology, “Artificial intelligence risk management framework (ai rmf 1.0),” 2023, accessed: 2026-05-20. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100- 1.pdf

[89] T. D. Nguyen, S. Marchal, M. Miettinen, H. Fereidooni, N. Asokan, and A.-R. Sadeghi, “Dïot: A federated self-learning anomaly detection system for iot,” in 2019 IEEE 39th International conference on distributed computing systems (ICDCS). IEEE, 2019, pp. 756–767.

[90] Y. Meidan, M. Bohadana, A. Shabtai, M. Ochoa, N. O. Tippenhauer, J. D. Guarnizo, and Y. Elovici, “Detection of unauthorized iot devices using machine learning techniques,” arXiv preprint arXiv:1709.04647, 2017.

[91] W. A. Aziz, I. I. Ioannou, M. Lestas, H. K. Qureshi, A. Iqbal, and V. Vassiliou, “Content-aware network trafic prediction framework for quality of service-aware dynamic network resource management,” IEEE Access, vol. 11, pp. 99 716–99 733, 2023.

[92] J. Holland, P. Schmitt, N. Feamster, and P. Mittal, “New directions in automated trafic analysis,” in Proceedings ofthe 2021 ACM SIGSAC Conference on Computer and Communications Security, ser. CCS ’21. New York, NY, USA: Association for Computing Machinery, 2021, p. 3366–3383. [Online]. Available: https://doi.org/10.1145/3460120. 3484758

[93] S. Liu, T. Mangla, T. Shaowang, J. Zhao, J. Paparrizos, S. Krishnan, and N. Feamster, “Amir: Active multimodal interaction recognition from video and network trafic in connected environments,” Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 7, no. 1, pp. 1–26, 2023.

[94] MIT Lincoln Laboratory, “VPN-nonVPN network application traffic dataset (VNAT),” https://www.ll.mit.edu/r-d/datasets/vpnnonvpnnetwork-application-trafic-dataset-vnat, 2017, accessed: 2025-11-18.

[95] W. Wang, M. Zhu, X. Zeng, X. Ye, and Y. Sheng, “Malware trafic classification using convolutional neural network for representation learning,” in 2017 International Conference on Information Networking (ICOIN), 2017, pp. 712–717.

[96] M. MontazeriShatoori, L. Davidson, G. Kaur, and A. Habibi Lashkari, “Detection of doh tunnels using time-series classification of encrypted trafic,” in 2020 IEEE Intl Confon Dependable, Autonomic and Secure Computing, Intl Conf on Pervasive Intelligence and Computing, Intl Conf on Cloud and Big Data Computing, Intl Conf on Cyber Science and Technology Congress (DASC/PiCom/CBDCom/CyberSciTech), 2020, pp. 63–70.

## A Ethics

This work does not raise any ethical issues.

## B Content generated by AI

Various tools, including Copilot, Claude, ChatGPT, and Gemini, supported the preparation of this manuscript through editing, grammar checks, and retrieval of background information. All generated text was reviewed and revised by the authors, and the core ideas, analyses, and conclusions remain entirely the authors’ own. The same tools were also used during code development and early-stage manuscript reviews.

## C Additional topology leakage experiment

<table><tr><td>Traffic Dataset</td><td>Node-overlap</td><td>Edge overlap</td></tr><tr><td>IoT</td><td>33/372 (8.87%)</td><td>29/386 (7.51%)</td></tr><tr><td>SR</td><td>21/70 (30.00%)</td><td>18/73 (24.66%)</td></tr><tr><td>VNAT</td><td>8/26 (30.77%)</td><td>4/19 (21.05%)</td></tr><tr><td>USTC</td><td>10/1349 (0.74%)</td><td>9/1364 (0.66%)</td></tr><tr><td>CIC</td><td>24/1307 (1.84%)</td><td>27/1315 (2.05%)</td></tr></table>

Table 7: Node and edge overlap rates between real and synthetic topologies when topology is constructed from both large and small flows. Results are reported as overlap count / total count (%).

Setting: To evaluate topology leakage across flows of varying sizes, we first identify the top 10 source IP addresses ranked by total packet volume and construct topology graphs using all flows (both large and small) originating from these sources. After generating synthetic trafic (NetSSM is trained for 1 epoch only), we extract flows associated with the same source IPs from the synthetic output and construct corre sponding topologies.

Results: Compared to the setting in Section 3.1.3, where topologies are constructed only from large flows, constructing topologies from both large and small flows results in slightly lower node and edge overlap rates. This reduction is more noticeable for datasets such as IoT, USTC, and CIC, which contain a large number of nodes and edges. Neverthe less, the overlap remains substantial for datasets such as SR and VNAT, which have smaller and simpler topologies that are easier for the model to memorize. Detailed results are shown in Table 7.

We further analyze which edges are more likely to be reconstructed in the generated outputs. Our results show that flows with higher packet counts are more likely to be memorized. Figure 8 illustrates the distribution ofmemorized and non-memorized edges for the SR dataset. In particular, memorized edges typically correspond to flows containing at least 1000 packets in the training data.

## D Additional evidence

![](images/a4aac0ae95c4d6871174fa1380a4f8f30fc148da54339ddf12d03e06ffcde1d5.jpg)  
(a) IoT dataset

![](images/57a02a7c6bd9aaab43f2cfa34a50035263d99d847800af2e2d69d9dc1403765d.jpg)  
(b) USTC dataset

Figure 12: Probability density function (PDF) of the perplexity scores produced by NetSSM on tokens generated from the first packet of each PCAP. For the IoT dataset, the target holdout distribution is more distinguishable from the training and shadow training distributions, whereas in the USTC dataset, the target holdout distribution exhibits greater overlap with the training and shadow training distributions. Consequently, the MIA attack against NetSSM is more successful on the IoT dataset than on the USTC dataset.  
![](images/f78db16a393d4f56da4d0cc16b64caf61589f774b9aafa79c1380d55565777f4.jpg)

(a) IoT dataset  
![](images/715ddc824792a873b1a06c09f4c194ca883d67048272f281932aae6be2024434.jpg)  
(b) USTC dataset  
Figure 13: Probability density function (PDF) of the number of unique source IPs generated by NetShare for each PCAP. For the IoT dataset, the target holdout distribution is highly similar to the training and shadow training distributions, whereas the distributions are more distinguishable in the USTC dataset. Consequently, the MIA attack against Net-Share is less successful on the IoT dataset than on the USTC dataset.

## E Additional results

![](images/5c1162517eb9ec20b39b4328d1ed066fd1d45d62594b1f63c1055fe29a41a526.jpg)

(a) Precision  
![](images/c49aaeff59742113c875e9e8ab38bdcaee6deb23a8b13a46db3e8a846e180ace.jpg)  
(b) Recall (b)  
Figure 14: Precision and recall scores for destination IP ad dresses across diferent models and datasets. Overall, NetSSM has the highest precision and recall scores across datasets, followed by TraficLLM. NetShare does not leak destination IP addresses.

![](images/b07d3e3199a4edb342fb4eeacff39e3c43ec8ee291e411ffe725692a24ea6439.jpg)  
(a) Precision

![](images/aa11e35a8fe234e5aa6e70bd11a6632411f8407116493aed6d776fc1c104c3ea.jpg)  
(b) Recall  
Figure 15: Impact of the number of generated outputs on precision and recall scores for source IP address.
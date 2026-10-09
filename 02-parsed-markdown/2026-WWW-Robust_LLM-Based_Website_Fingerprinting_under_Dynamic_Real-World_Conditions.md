# Robust LLM-Based Website Fingerprinting under Dynamic Real-World Conditions

Xiyuan Zhao Tsinghua University Beijing, China zhaoxy23@mails.tsinghua.edu.cn

Yixiang Zhang Tsinghua University Beijing, China zhangyix24@mails.tsinghua.edu.cn

Xinhao Deng Ant Group Hangzhou, China Tsinghua University Beijing, China dengxinhao@mail.tsinghua.edu.cn

Ke Xu Tsinghua University Beijing, China Zhongguancun Laboratory Beijing, China xuke@tsinghua.edu.cn

Tianyu Cui Zhongguancun Laboratory Beijing, China cuity@zgclab.edu.cn

Qi Li<sup>∗</sup> Tsinghua University Beijing, China Zhongguancun Laboratory Beijing, China qli01@tsinghua.edu.cn

## Abstract

Website Fingerprinting (WF) attacks aim to infer the websites vis ited by Tor users by analyzing patterns in encrypted network trafic. However, most existing WF attacks are evaluated on trafic collected in controlled environments with fixed configurations, failing to re flect the complexity and variability of real-world conditions. In practice, trafic is far more dynamic and diverse due to heterogeneous network conditions, the large number of subpages within individual websites, and continuous evolution of website content. These factors increase intra-class variability and induce temporal feature drift, which ultimately degrades the long-term efectiveness of existing attacks. In this paper, we propose TraVerse, an LLM-based representation learning framework designed to achieve robust WF attacks under real-world conditions. TraVerse applies architectural adaptation and large-scale fine-tuning on diverse un labeled trafic to learn generalizable and resilient representations that remain efective in dynamic and evolving environments. Fur thermore, TraVerse integrates a lightweight classifier atop the LLM derived representations, enabling accurate website identification and eficient few-shot adaptation with minimal model updates. We prototype TraVerse and conduct comprehensive evaluations using real-user trafic. Experimental results show that TraVerse improves Accuracy@3 by an average of 176.3% and weighted F1 by 343.3% over state-of-the-art baselines, while maintaining strong performance throughout a three-month longitudinal evaluation.

## CCS Concepts

• Security and privacy → Network security.

<sup>∗</sup>Corresponding author

![](images/5521ab3a57976357a23e5a8ee82326365518a6d60f78f522629b248b9af74ce7.jpg)

Keywords Tor; privacy; website fingerprinting; LLM fine-tuning; representation learning

ACM Reference Format: Xiyuan Zhao, Xinhao Deng, Tianyu Cui, Yixiang Zhang, Ke Xu, and Qi Li. 2026. Robust LLM-Based Website Fingerprinting under Dynamic Real-World Conditions. In Proceedings ofthe ACM Web Conference 2026 (WWW ’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3774904.3792288

## 1 Introduction

Tor [15] provides anonymity through randomized multi-hop routing and layered encryption. However, it remains vulnerable to Website Fingerprinting (WF) attacks [1, 2, 10–12, 28, 41, 44, 45, 55], where adversaries analyze encrypted trafic patterns to identify visited websites. These attacks extract meta-features like packet directions, sizes, and timings from trafic traces and train models to perform website classification.

Recent WF attacks are primarily evaluated under fixed settings, which fail to reflect the variability of real-world trafic [26]. In practice, network trafic exhibits pronounced intra-class variability and evolves continuously. While state-of-the-art methods can learn discriminative representations from stable datasets, their performance deteriorates in dynamic conditions, where heterogeneous trafic patterns and website evolution cause feature drift and poor adaptability [35, 49]. Although recent studies have attempted to address these issues [1, 6], notable limitations persist. For example, the data augmentation in [1] is environment-specific and lacks generality, whereas the online adaptation approach in [6] continuously retrains classifiers at the exit side but sufers from distortions between the entry and exit relays, resulting in degraded robustness [6, 27].

In this work, we focus on developing practical WF attacks tailored for real-world conditions, where network trafic is highly dynamic and diverse due to heterogeneous network environments, numerous subpages within individual websites, and continuously evolving website content. We introduce a Large Language Model (LLM)-based representation learning paradigm for robust website fingerprinting. LLMs have demonstrated strong capabilities in pattern mining and contextual modeling [7, 50], making them particularly well-suited for capturing complex dependencies in trafic sequences. Furthermore, their powerful generalization abil ity supports learning robust representations from heterogeneous and evolving trafic, a property that is critical for maintaining at tack performance under real-world variability. Building upon these strengths, we leverage LLMs to derive generalizable trafic representations that sustain high identification accuracy and stable performance in dynamic, real-world environments.

However, leveraging LLMs for WF attacks presents several key challenges. First, most decoder-based LLMs adopt causal attention, which restricts each token to attend only to its predecessors and <sub>thus struggles to capture global dependencies across an entire trafic</sub>... Packet disordering sequence. Second, pretrained LLMs lack trafic-domain knowledge,... Packet loss limiting their ability to learn robust and discriminative representations for dynamic real-world trafic. Third, real-world website identification requires continual adaptation to evolving trafic distri butions, yet periodic LLM fine-tuning is computationally expensive and time-consuming, making long-term adaptation impractical.

To this end, we propose TraVerse, a robust and realistic WF framework that customizes LLMs for accurate website identifica tion. Since real-world trafic is inherently dynamic and heteroge neous, with substantial variability even within the same website, TraVerse adapts the LLM architecture to capture robust and dis criminative trafic features, enabling richer sequence understanding to support resilient fingerprinting. Moreover, to cope with tempo ral drift in trafic characteristics, TraVerse combines large-scale unsupervised fine-tuning for generalizable representations with lightweight adaptation that avoids frequent LLM fine-tuning, sus taining performance throughout long-term deployment.

To realize these objectives, TraVerse comprises three key components. First, we introduce a context-aware trafic profiling mechanism based on bidirectional attention to model full-sequence dependencies and facilitate the extraction of global patterns that remain stable under heterogeneous network conditions. Second, we conduct large-scale fine-tuning on massive unlabeled trafic data to imbue the model with domain-specific trafic knowledge, allowing TraVerse to learn generalizable representations across diverse traf fic patterns. Finally, we perform few-shot supervised classification using a lightweight classifier built atop the LLM-derived represen tations to achieve accurate website identification. This classifier requires only a small number of labeled samples for adaptation, enabling eficient updates and long-term robustness under dynamic and evolving network environments.

In summary, this work makes the following contributions:

• We propose TraVerse, a WF attack framework that leverages LLM based trafic representation learning to enable efective website identification under realistic and dynamic browsing scenarios.

• We adapt the LLM architecture and conduct large-scale unsuper vised fine-tuning on massive trafic data, allowing the model to learn robust and generalizable trafic representations that remain efective under dynamic and evolving network conditions.

• We implement and evaluate TraVerse on real-user trafic in both the closed-world and open-world settings. Results from a threemonth study show that TraVerse maintains long-term robustness and consistently outperforms existing methods.

![](images/5dc4dbeddef6877c7b7ee23559c0ab2f3b4f726b680126442e766f6c6762d675.jpg)  
Figure 1: The threat model of TraVerse.

## 2 Background

WF attacks aim to identify the websites visited by users, even when trafic is encrypted on the Tor network. Since encryption prevents direct access to website content, attackers must instead infer websites by analyzing distinctive trafic patterns such as packet timings, direction sequences, and burst structures. Early works employ traditional classifiers like Random Forests and Support Vector Machines to distinguish websites [23, 36, 47], while recent works take advantage of deep learning to automate feature extraction and significantly improve attack performance [42, 44]. Building on these advances, research has extended WF attacks to more realistic settings, such as multi-tab browsing [8, 12, 21, 28, 51, 53], diverse network conditions [1], and fine-grained webpage identification [55]. In addition, eforts have focused on practical challenges, including limited training data [2, 35, 45], incomplete page loading [11, 13], and robustness against trafic obfuscation defenses [13, 17, 41, 43].

Despite these eforts, the majority of existing methods are still evaluated on simulated datasets with relatively homogeneous trafic characteristics. When deployed in real-world environments, their identification capability often deteriorates due to dynamic network conditions, high subpage diversity, and continuous feature drift. In this work, we focus on addressing real-world website identification, where trafic patterns are inherently diverse, evolving, and challenging to model using conventional approaches.

## 3 Threat Model

Figure 1 illustrates the threat model of TraVerse. Consistent with previous works [12, 28, 44, 55], we consider a passive attacker who has the ability to eavesdrop and collect trafic packets on the link between the user and the Tor entry relay. The attacker cannot decrypt, modify, or drop these packets, but can analyze trafic patterns to infer the websites being accessed.

Our threat model aims to reflect the complexities of real-world WF attacks, characterized by three key aspects. (i) Dynamic network conditions: accesses may occur from diferent locations and under diverse network conditions. Real-world fluctuations like packet delays, reordering, or loss introduce variations in trafic characteristics. (ii) Subpage diversity: users can visit arbitrary subpages within a target website, rather than being restricted to the homepage, resulting in high intra-website variability. (iii) Pattern drift: websites are constantly updated with new content and features, causing temporal drift in trafic patterns.

Following prior works [12, 28, 41, 44, 45, 55], we evaluate Tra-Verse in both the closed-world and open-world settings. In the closed-world setting, users browse a fixed set of monitored websites whose trafic is observed during training. In contrast, the open-world setting allows users to access a wide range of unmonitored websites unseen during training, requiring the attacker to distinguish monitored visits from unmonitored background trafic.

## 4 Design of TraVerse

In this section, we first present the key observation for the design of TraVerse, followed by a high-level overview of the framework.

## 4.1 Key Observation

Real-world trafic exhibits substantially greater variability than the controlled traces commonly used in prior studies. In particular, traces collected from real users display high intra-class diversity. We evaluate this diversity using a real-user trafic dataset spanning 13 weeks. As shown in Figure 2a, the intra-class cosine similarity computed from raw-packet direction sequences is skewed toward lower values, with most values concentrated around 0.3. We further analyze temporal dynamics by calculating the similarity of each website’s trafic from Weeks 1–13 relative to Week 1. Figure 2b shows that the similarity displays a clear downward trend, reflect ing temporal feature drift and the continuous evolution of trafic patterns. The fluctuation observed in Week 6 may be attributed to the sampling strategy during dataset construction. These findings underscore the necessity of learning robust trafic representations that can generalize across diverse and evolving conditions.

To address these challenges, we develop a trafic representa tion learning framework grounded in extensive LLM fine-tuning to learn robust representations. After applying trafic representation learning, the intra-class similarity becomes concentrated around 0.6, indicating enhanced consistency within individual websites. Furthermore, the cross-week similarity remains consistently higher after representation, demonstrating improved temporal robustness. Such improvements confirm that the learned representations are both robust and generalizable, enabling accurate and resilient web site identification under dynamic real-world conditions.

![](images/3cc7b317af1fb017f2c7c2a93aeb1584fbc09808300dac477b8f242dde325365.jpg)  
0.1(a) Intra-website similarity

![](images/33cdbef897042f64137cac06e8b969c3aa12463506d32ee53eaf96351a086e27.jpg)  
(b) Similarity trend across weeks  
Figure 2: Analysis of representation learning on real-user trafic.

## 4.2 Design Overview

In this work, we propose TraVerse, a framework that leverages LLM-based trafic representation learning via model architectural adaptation and large-scale fine-tuning to enable practical WF attacks in real-world settings. Through extensive unsupervised fine tuning on unlabeled trafic, TraVerse equips the adapted LLM with trafic-domain knowledge, allowing it to capture global, long-range dependencies across diverse browsing conditions and generate robust, highly generalizable representations for real-world trafic.

As illustrated in Figure 3, TraVerse comprises three main components. First, we propose a context-aware trafic profiling mechanism that captures global trafic patterns and improves robustness under dynamic network conditions. Specifically, we adapt the LLM architecture by introducing bidirectional attention, enabling comprehensive context aggregation across the entire trafic sequence. Second, we conduct unsupervised representation learning by extensively fine-tuning the adapted LLM on a large-scale trafic corpus using a masked pattern reconstruction objective. This objective injects domain-specific knowledge and strengthens the model’s capacity to represent diverse trafic patterns. Despite the diversity and continual evolution of real-world trafic, the fine-tuned LLM produces robust and generalizable representations. Finally, leveraging the representations generated by the LLM, TraVerse performs few-shot supervised classification using a lightweight classifier for accurate website identification. By restricting retraining to this classifier while keeping the LLM frozen, TraVerse can eficiently adapt to distribution shifts with minimal labeled samples, ensuring long-term robustness under real-world drift.

## 5 Design Details

In this section, we present the details of TraVerse, comprising three key components: Context-Aware Trafic Profiling, Unsupervised Representation Learning and Few-Shot Supervised Classification.

## 5.1 Context-Aware Trafic Profiling

TraVerse leverages a context-aware trafic profiling mechanism to improve robustness under dynamic network conditions. Specifically, we adapt large decoder-based LLMs [3, 20, 52] for trafic profiling by modifying their attention mechanisms to enable holistic contextual modeling over trafic sequences.

In real-world environments, trafic patterns often exhibit local variations caused by latency fluctuations, packet reordering, and other transient network dynamics. Such variations disrupt the con sistency of trafic patterns and degrade models that primarily rely on short-range dependencies. Therefore, we employ LLMs to capture long-range and global patterns in trafic sequences. However, decoder-based LLMs are designed for generation tasks and typically employ causal attention, where each token embedding attends solely to preceding tokens. This unidirectional attention can lead to incomplete profiling when applied to dynamic trafic sequences.

To address this limitation, TraVerse modifies the LLM architecture by introducing bidirectional attention, allowing each token to attend to both preceding and succeeding tokens over the sequence. This bidirectional attention, widely used in encoder-based models for sequence understanding, facilitates full-sequence interaction and comprehensive context aggregation throughout the trafic trace. As a result, TraVerse extracts global patterns that remain robust despite local variations caused by dynamic perturbations.

To enable context-aware trafic profiling, TraVerse constructs instruction-guided prompts that combine a natural language instruction with trafic feature inputs. The instruction specifies that the subsequent sequence represents a website browsing session, guiding the model to interpret the trace in the intended context.

![](images/0cd1d9c58445910f9230b55723c17d128066c01875bb4710f8e8c27a7421f118.jpg)  
Figure 3: Design overview of TraVerse.

Real-World DynamicsTrafic features are extracted as burst sequences, which capture higher-level semantics associated with website resources, such as text and images [1], therefore preserving salient structural informa tion critical for trafic modeling. A burst is defined as consecutive packets in the same direction, represented by its length and direction. Finally, the instruction and burst inputs are concatenated into a unified input using the format: <flow>: <burst sequence>. Prompt templates are provided in Appendix B.

After prompt construction, the prompt is tokenized into a token ion<sub>sequence</sub> <sub>of</sub> <sub>length</sub> � $: L = ( L _ { 1 } , L _ { 2 } , . . . , L _ { l } )$ . The LLM then transforms this token sequence into token embeddings $T = [ T _ { 1 } , T _ { 2 } , \dots , T _ { l } ] \in$ $\mathbb { R } ^ { l \times d }$ , where � denotes the embedding dimension. A linear projection is subsequently applied to obtain the query, key, and value matrices:

$$
Q = T W _ {Q}, \quad K = T W _ {K}, \quad V = T W _ {V},\tag{1}
$$

where $W _ { Q } , W _ { K } , W _ { V } \in \mathbb { R } ^ { d \times d _ { o } }$ are trainable matrices and $Q , K , V \in$ $\mathbb { R } ^ { l \times d _ { o } }$ are the projected representations, with $d _ { o }$ denoting the projection dimension. The bidirectional attention score between token � and token � is then formally defined as:

$$
\alpha_ {i j} = \frac {\exp \left(\frac {Q _ {i} K _ {j} ^ {\top}}{\sqrt {d _ {o}}}\right)}{\sum_ {k = 1} ^ {l} \exp \left(\frac {Q _ {i} K _ {k} ^ {\top}}{\sqrt {d _ {o}}}\right)},\tag{2}
$$

where the denominator aggregates over all tokens in the sequence, ensuring full-sequence contextual aggregation. After the stacked attention layers, TraVerse applies position-weighted pooling over the resulting feature token embeddings to aggregate information and produce the final trafic representation. Specifically, earlier tokens are assigned higher weights because the front of a trafic trace typically contains more discriminative features [18].

Overall, the combination of bidirectional attention and position weighted aggregation enables context-aware trafic profiling that captures global trafic patterns and remains resilient to local variations under dynamic network conditions.

## 5.2 Unsupervised Representation Learning

TraVerse leverages unsupervised representation learning to better model diverse trafic patterns. In practice, users access not only index pages but also numerous subpages, increasing intra-website

Pattern Maskingvariability. Moreover, websites continuously evolve, causing feature drift that degrades model stability over time. By fine-tuning the LLM on large-scale unlabeled trafic traces, TraVerse exploits the strong generalization capability of LLMs to capture diverse patterns and generate robust and transferable representations that remain efective under dynamic real-world conditions.

Figure 4 illustrates the details of the unsupervised representation learning. Specifically, TraVerse adopts a masked pattern reconstruction objective by randomly masking a fraction of pattern tokens and training the model to predict the masked pieces by leveraging contextual information in the sequence. We first construct prompts from the trafic corpus by combining a natural language description with trafic features, then tokenize the prompts and apply masking. The adapted LLM, equipped with bidirectional attention, produces contextualized representations for all positions. We train the model to predict masked tokens in a shifted decoder-style manner, where each target token is predicted from the contextualized representation at the previous position. This preserves the decoderbased pretraining paradigm while exploiting bidirectional context, enhancing the model’s ability to interpret trafic patterns and facilitating domain adaptation.

Formally, let $M \subseteq \{ 1 , \dots , l \}$ denote the set of masked positions. The training objective is to maximize the likelihood of recovering the tokens $L _ { i }$ at masked positions $i \in M$ . The loss is defined as:

$$
\mathcal {L} _ {\text { recon }} = - \sum_ {i \in M} \log P (L _ {i} \mid h _ {i - 1}; \theta),\tag{3}
$$

where � denotes the model parameters and $h _ { i - 1 }$ is the contextaware representation at position �−1 produced by multiple bidirectional attention layers over the masked input sequence. The masked tokens are replaced with a special token.

We adopt Low-Rank Adaptation (LoRA) [24], which introduces low-rank trainable matrices into the transformer layers for parametereficient fine-tuning. This significantly reduces the number of trainable parameters and memory costs, enabling eficient adaptation of large pretrained LLMs to trafic-specific tasks without full-scale fine-tuning. The LoRA fine-tuning is detailed in Appendix A.

By fine-tuning on extensive unlabeled trafic, TraVerse learns generalizable representations from diverse browsing conditions, forming a strong foundation for accurate website identification.

![](images/f7faec7a997ac63f4f6a353694188ed176b3b7bff79983cf39b4557a08420464.jpg)  
Figure 4: Details of the unsupervised representation learning.

## 5.3 Few-Shot Supervised Classification

TraVerse employs supervised classification on top of the LLM using few-shot labeled samples to achieve accurate website identification. While unsupervised fine-tuning enables generalization across diverse trafic patterns, real-world website identification further requires long-term adaptability to evolving trafic distributions. Leveraging robust LLM-generated representations, TraVerse trains a lightweight downstream classifier with a small labeled set, enabling eficient updates without frequent LLM fine-tuning.

Specifically, TraVerse constructs prompts combining instructions and trafic features, obtains representations from the fine-tuned LLM, and feeds them into a lightweight classifier for website iden tification. The classifier consists of two fully connected layers with ReLU activation, and incorporates batch normalization to stabilize training. During deployment, the trained classifier predicts the corresponding website for each trafic sample and can be updated using a small labeled set when the trafic characteristics shift.

Formally, given the input matrix $X \in \mathbb { R } ^ { N \times d _ { e } }$ , where � denotes the number of samples and $d _ { e }$ denotes the dimension of the LLM generated representations, the classifier is defined as:

$$
\tilde {Y} = \sigma (\mathrm{BN} (X W _ {1})) W _ {2}\tag{4}
$$

where $W _ { 1 } \in \mathbb { R } ^ { d _ { e } \times d _ { h } }$ and $W _ { 2 } \in \mathbb { R } ^ { d _ { h } \times W }$ are the weight matrices of the linear layers, $d _ { h }$ is the hidden dimension, � is the number of websites, ��(·) denotes batch normalization, and �(·) is the ReLU activation function. During website identification, the classifier outputs the website with the highest predicted probability.

By decoupling representation learning from classification, Tra-Verse fully capitalizes on the robust representations generated by the LLM while ensuring high accuracy and adaptability for website identification under dynamic real-world conditions. This light weight classifier supports eficient few-shot updates, allowing rapid adaptation to new trafic distributions and evolving environments.

## 6 Evaluation

In this section, we evaluate the performance of TraVerse using public datasets collected from real user browsing, and compare it with state-of-the-art methods.

## 6.1 Experimental Setup

Implementation. We implement TraVerse using Python 3.10 and Transformers 4.44.2 and adopt Llama3-8B [20] as the backbone model. We fine-tune the LLM on a single NVIDIA GeForce RTX 4090 GPU, requiring approximately 65 GPU hours and 21 GB of peak memory for 30k steps on 200k traces. The default hyperparameter settings and prompt templates are provided in Appendix B.

Datasets. We evaluate TraVerse using GTT23 [26], a real-user trafic dataset that ofers a more realistic and challenging setting than prior datasets collected under fixed settings [33, 35, 38, 42, 44]. It reflects dynamic network conditions, includes trafic beyond index pages, and spans 13 weeks to capture temporal drift in trafic patterns.

The dataset is collected at the exit relay, which difers from our threat model. However, due to Tor’s design, collecting large-scale labeled entry-side traces from real users is dificult, and [27] demonstrates that training and testing on exit traces yields performance comparable to training and testing on transduced entry traces. This establishes GTT23 as a reliable benchmark for real-world WF evaluation without the cost of trafic transduction. For real-world deployment, TraVerse can be combined with the transduction methods in [25, 27] to approximate entry-side inputs.

We select 200,000 unlabeled traces for LLM fine-tuning to learn diverse trafic patterns, filtering out traces with fewer than 20 packets. For evaluation, we establish a monitored set consisting of 200 websites with suficient samples, where these 200 websites are disjoint from those used for LLM fine-tuning. This separation creates a more challenging and realistic scenario, simulating an attacker with limited prior knowledge of the visited websites.

We use two datasets, $\mathbf { G T T _ { C W } }$ and GTT<sub>OW</sub>, to evaluate Tra-Verse in both the closed-world and open-world settings. We train and validate on Week 1 and test on Weeks 1–13 to assess robustness under temporal drift. For GTT , we additionally include an unmonitored class consisting of trafic from disjoint unmonitored websites, using 2,000 and 100 unmonitored traces for training and validation, and 5,000 unmonitored traces per week for testing, while retaining the monitored samples. We ensure no unmonitored website overlap across LLM fine-tuning, classifier training, and testing. We also synthesize a 2-tab concurrent browsing dataset $\mathbf { G T T _ { M T } }$ from GTT23 to evaluate TraVerse under the multi-tab setting since no real-user multi-tab dataset is publicly available. Details of the datasets are shown in Appendix C.

Baselines. We select nine WF attacks as baselines [1, 2, 12, 13, 28, 41, 43–45], where these baselines cover a representative range of WF attacks. For a fair comparison, all WF baselines are trained with a maximum of 100 epochs, and the best checkpoint is selected based on the validation performance. In addition, we include TrafficLLM [7] as an LLM-based baseline. TraficLLM is trained for 5 epochs and uses the same prompt templates as TraVerse. Baseline details are provided in Appendix D.

Metrics. For the closed-world setting, following prior works [1, 11, 41, 44], we evaluate methods using Accuracy@3, Precision<sub>w</sub>, Recall<sub>w</sub>, and $\mathrm { F } 1 _ { \mathrm { w } } .$ . Accuracy@3 measures whether the ground-truth label appears among the top three predictions, while Precision<sub>w</sub>, Reca ${ \mathrm { l l } } _ { \mathrm { w } } ,$ and $\mathrm { F } 1 _ { \mathrm { w } }$ jointly assess the correctness and completeness under real-world data distributions, where each class is weighted by its proportion in the dataset. For the open-world setting, we follow $[ 1 1 , 4 6 ]$ and use r-precision with $r = 5 ,$ where � denotes the ratio of visits to unmonitored versus monitored websites. For the multi-tab setting, following [55], we adopt Recall@10 and AP@2. Detailed definitions of all metrics are provided in Appendix E.

![](images/156234d2739a0a8895190a76f303c0e475f7c70ee17f1004cbce3308332e92c7.jpg)  
(a) Precision<sub>w</sub>

![](images/2847777a8542d13caf181f44405f60b380d2089d4a065d7522ac1ca894fed496.jpg)  
(b) Recall<sub>w</sub>

![](images/a32f7ee5579c84d5d2669e2acb14a966fad60b8cf9c2be4fd5283129cbd384e4.jpg)  
(c) F1<sub>w</sub>  
<sup>1</sup> <sup>2</sup> <sup>3</sup> <sup>4</sup> <sup>5</sup> <sup>6</sup> <sup>7</sup> <sup>8</sup> <sup>9</sup> <sup>10</sup> <sup>11</sup> <sup>12</sup> <sup>13</sup>Figure 5: Performance of various methods in the closed-world setting.

Table 1: Accuracy@3 of various methods in the closed-world setting.

<table><tr><td>Method</td><td>Week 1</td><td>Week 2</td><td>Week 3</td><td>Week 4</td><td>Week 5</td><td>Week 6</td><td>Week 7</td><td>Week 8</td><td>Week 9</td><td>Week 10</td><td>Week 11</td><td>Week 12</td><td>Week 13</td></tr><tr><td>ARES</td><td>0.206</td><td>0.166</td><td>0.164</td><td>0.160</td><td>0.150</td><td>0.125</td><td>0.150</td><td>0.159</td><td>0.172</td><td>0.154</td><td>0.140</td><td>0.130</td><td>0.156</td></tr><tr><td>DF</td><td>0.419</td><td>0.331</td><td>0.350</td><td>0.334</td><td>0.324</td><td>0.266</td><td>0.306</td><td>0.337</td><td>0.311</td><td>0.279</td><td>0.277</td><td>0.256</td><td>0.287</td></tr><tr><td>NetCLR</td><td>0.472</td><td>0.367</td><td>0.396</td><td>0.383</td><td>0.363</td><td>0.288</td><td>0.336</td><td>0.355</td><td>0.348</td><td>0.328</td><td>0.307</td><td>0.274</td><td>0.334</td></tr><tr><td>RF</td><td>0.414</td><td>0.339</td><td>0.357</td><td>0.362</td><td>0.371</td><td>0.277</td><td>0.327</td><td>0.357</td><td>0.331</td><td>0.312</td><td>0.301</td><td>0.253</td><td>0.324</td></tr><tr><td>TF</td><td>0.239</td><td>0.188</td><td>0.191</td><td>0.194</td><td>0.177</td><td>0.143</td><td>0.160</td><td>0.190</td><td>0.168</td><td>0.161</td><td>0.153</td><td>0.152</td><td>0.168</td></tr><tr><td>TMWF</td><td>0.288</td><td>0.202</td><td>0.195</td><td>0.189</td><td>0.189</td><td>0.189</td><td>0.198</td><td>0.201</td><td>0.171</td><td>0.164</td><td>0.184</td><td>0.207</td><td>0.193</td></tr><tr><td>Tik-Tok</td><td>0.204</td><td>0.163</td><td>0.160</td><td>0.176</td><td>0.201</td><td>0.133</td><td>0.139</td><td>0.189</td><td>0.148</td><td>0.153</td><td>0.159</td><td>0.137</td><td>0.161</td></tr><tr><td>Var-CNN</td><td>0.440</td><td>0.358</td><td>0.357</td><td>0.363</td><td>0.341</td><td>0.265</td><td>0.323</td><td>0.337</td><td>0.301</td><td>0.272</td><td>0.289</td><td>0.297</td><td>0.319</td></tr><tr><td>Countmamba</td><td>0.205</td><td>0.165</td><td>0.143</td><td>0.154</td><td>0.157</td><td>0.128</td><td>0.143</td><td>0.155</td><td>0.157</td><td>0.147</td><td>0.149</td><td>0.140</td><td>0.145</td></tr><tr><td>TraVerse</td><td>0.694</td><td>0.612</td><td>0.625</td><td>0.602</td><td>0.588</td><td>0.513</td><td>0.583</td><td>0.609</td><td>0.608</td><td>0.577</td><td>0.553</td><td>0.517</td><td>0.570</td></tr></table>

## 6.2 Closed-World Evaluation

We first evaluate the performance of TraVerse in the closed-world setting, where both training and test trafic originate from monitored websites. We use the closed-world dataset $\mathbf { G T T _ { C W } }$ for evaluation, and report Accuracy@3, Precision<sub>w</sub>, Recall<sub>w</sub> and $\mathrm { F } 1 _ { \mathrm { w } } .$ . Note that TraficLLM does not support computing Accuracy@3, so we do not report this metric for TraficLLM.

Table 1 and Figure 5 present the results across 13 weeks. Week 1 yields the best performance since the training and test trafic share the highest similarity. In this case, TraVerse is the only method achieving Accuracy@3 close to 0.7, whereas all baselines remain below 0.48. Over time, although performance gradually decreases due to feature drift, TraVerse consistently maintains Accuracy@3 and $\mathrm { F } 1 _ { \mathrm { w } }$ above 0.5 and 0.4 for most weeks, demonstrating strong temporal robustness. In general, TraVerse achieves an average Accuracy@3 improvement of 176.3% over the WF baselines across 13 weeks. It further improves Precisio $^ { 1 } \mathrm { w } \mathrm { , }$ , Recall<sub>w</sub>, and $\mathrm { F } 1 _ { \mathrm { w } }$ by an average of 214.0%, 318.3% and 343.3%, respectively, compared with all baselines. These results confirm that the learned trafic representations generalize well under temporal drift.

We also evaluate TraVerse on $\mathbf { G T T _ { M T } }$ under the multi-tab setting, using binary cross-entropy as the loss function. Excluding TF and TraficLLM, which cannot be directly applied in this scenario, TraVerse improves Recall@10 and AP@2 by 92.8% and 168.4%, demonstrating strong efectiveness under multi-tab browsing.

Remark. TraVerse consistently outperforms all baselines in the closed-world setting, demonstrating resilient website identification under dynamic real-world conditions.

## 6.3 Open-World Evaluation

We then evaluate the performance of TraVerse in the open-world setting, where users can visit a large number of unmonitored websites. The attacker must accurately classify monitored websites while reliably grouping all unmonitored trafic into a single unmonitored class. Experiments are conducted on the open-world dataset $\mathbf { G T T _ { O W } }$ , with performance measured by r-precision with $r = 5 .$

Table 2 reports the performance across 13 weeks. TraVerse achieves its best r-precision in Week 1 at approximately 0.55 and remains above 0.30 in all subsequent weeks. In contrast, all baselines except NetCLR perform poorly, reaching at most 0.26 in Week 1 and typically dropping below 0.20 afterward. NetCLR benefits from data augmentation and self-supervised learning, but it still underperforms TraVerse. Notably, in Week 13, TraVerse maintains r-precision above 0.30, whereas all other methods fall below 0.20. These results indicate that TraVerse yields robust trafic representations that generalize well in the presence of diverse unmonitored trafic.

Remark. TraVerse consistently outperforms prior methods in the open-world evaluation, where the learned representations enable reliable classification of monitored websites in the presence of unmonitored trafic.

## 6.4 Adaptability Analysis

In this section, we evaluate the real-world adaptability of TraVerse. We keep the LLM fine-tuned on Week 1 fixed and test classifier performance on Weeks 2-13. For each week, we split the data into training, validation, and test sets, limiting the training set to fewer than 10 samples per website. Two evaluation settings are considered: (i) Pre-Update, where the classifier trained on Week 1 is directly tested on trafic from Weeks 2–13 without any update; (ii) Post Update, where the classifier is retrained each week using that week’s limited training data and tested on the corresponding test set. We report Precision<sub>w</sub>, Recall<sub>w</sub> and $\mathrm { F } 1 _ { \mathrm { w } }$

Table 2: r-precision of various methods in the open-world setting.

<table><tr><td>Method</td><td>Week 1</td><td>Week 2</td><td>Week 3</td><td>Week 4</td><td>Week 5</td><td>Week 6</td><td>Week 7</td><td>Week 8</td><td>Week 9</td><td>Week 10</td><td>Week 11</td><td>Week 12</td><td>Week 13</td></tr><tr><td>ARES</td><td>0.063</td><td>0.000</td><td>0.008</td><td>0.000</td><td>0.031</td><td>0.053</td><td>0.011</td><td>0.059</td><td>0.029</td><td>0.018</td><td>0.000</td><td>0.000</td><td>0.059</td></tr><tr><td>DF</td><td>0.159</td><td>0.194</td><td>0.053</td><td>0.186</td><td>0.179</td><td>0.077</td><td>0.078</td><td>0.251</td><td>0.071</td><td>0.112</td><td>0.192</td><td>0.280</td><td>0.190</td></tr><tr><td>NetCLR</td><td>0.414</td><td>0.268</td><td>0.279</td><td>0.218</td><td>0.194</td><td>0.151</td><td>0.234</td><td>0.213</td><td>0.205</td><td>0.215</td><td>0.210</td><td>0.200</td><td>0.174</td></tr><tr><td>RF</td><td>0.255</td><td>0.179</td><td>0.183</td><td>0.180</td><td>0.166</td><td>0.130</td><td>0.156</td><td>0.170</td><td>0.160</td><td>0.143</td><td>0.145</td><td>0.128</td><td>0.112</td></tr><tr><td>TF</td><td>0.064</td><td>0.058</td><td>0.055</td><td>0.061</td><td>0.034</td><td>0.028</td><td>0.040</td><td>0.050</td><td>0.038</td><td>0.039</td><td>0.030</td><td>0.029</td><td>0.016</td></tr><tr><td>TMWF</td><td>0.104</td><td>0.063</td><td>0.027</td><td>0.072</td><td>0.093</td><td>0.044</td><td>0.028</td><td>0.109</td><td>0.043</td><td>0.065</td><td>0.115</td><td>0.139</td><td>0.084</td></tr><tr><td>Tik-Tok</td><td>0.105</td><td>0.170</td><td>0.059</td><td>0.114</td><td>0.154</td><td>0.075</td><td>0.054</td><td>0.205</td><td>0.000</td><td>0.095</td><td>0.189</td><td>0.241</td><td>0.173</td></tr><tr><td>Var-CNN</td><td>0.060</td><td>0.098</td><td>0.025</td><td>0.114</td><td>0.168</td><td>0.071</td><td>0.085</td><td>0.155</td><td>0.019</td><td>0.093</td><td>0.106</td><td>0.156</td><td>0.144</td></tr><tr><td>Countmamba</td><td>0.101</td><td>0.012</td><td>0.016</td><td>0.027</td><td>0.008</td><td>0.018</td><td>0.002</td><td>0.007</td><td>0.012</td><td>0.006</td><td>0.013</td><td>0.000</td><td>0.008</td></tr><tr><td>TrafficLLM</td><td>0.063</td><td>0.026</td><td>0.027</td><td>0.022</td><td>0.019</td><td>0.017</td><td>0.026</td><td>0.019</td><td>0.026</td><td>0.018</td><td>0.017</td><td>0.017</td><td>0.017</td></tr><tr><td>TraVerse</td><td>0.549</td><td>0.463</td><td>0.469</td><td>0.444</td><td>0.411</td><td>0.378</td><td>0.443</td><td>0.405</td><td>0.416</td><td>0.408</td><td>0.383</td><td>0.312</td><td>0.347</td></tr></table>

As shown in Figure 6, updating the classifier with a modest num ber of samples yields substantial performance gains. Specifically, Precision<sub>w</sub>, Recall<sub>w</sub> and $\mathrm { F } 1 _ { \mathrm { w } }$ improve by an average of 10.0%, 27.5%, and 24.2%, respectively. Moreover, the post-update performance is comparable to that of Week 1 reported in Section 6.2, indicating that the LLM-generated representations generalizes well to subsequent weeks. This demonstrates that TraVerse can efectively leverage a small number of labeled samples to retrain the lightweight classi fier while keeping the LLM frozen, thereby enhancing adaptability under dynamic conditions. We further evaluate the impact of dif ferent sample sizes in Appendix F, where TraVerse maintains high identification accuracy with limited training data.

Remark. The adaptability analysis shows that the LLM-learned representations ensure temporal robustness as trafic evolves. The light weight classifier supports eficient few-shot updates, enabling long term adaptability and sustained real-world attack performance.

## 6.5 Ablation Study

We also conduct an ablation study to analyze the contribution of each design component. The comparison includes the full TraVerse, the variant without bidirectional attention, and the variant without unsupervised fine-tuning. All methods are evaluated on the closed world dataset GTT<sub>CW</sub>, and we report Accuracy@3.

As shown in Table 3, the full TraVerse consistently outperforms the ablated variants. Removing bidirectional attention causes a substantial performance drop, with Accuracy@3 falling below 0.47 after Week 3. This underscores the importance ofmodeling both pre ceding and subsequent context for comprehensive representations of trafic patterns under dynamic conditions. Likewise, removing unsupervised fine-tuning leads to an even sharper degradation, with Accuracy@3 dropping to below 0.44 after Week 3, indicating that the model fails to learn diverse trafic patterns without large scale domain adaptation. Overall, the full TraVerse improves by 34.5% and 39.5% over the variants without bidirectional attention and without unsupervised fine-tuning, respectively. These results confirm that bidirectional attention and trafic fine-tuning are complementary to support robust representation learning. We further evaluate TraVerse with diferent backbone sizes in Appendix G, where reducing the model size causes only modest degradation. This suggests that the performance gains stem from our design rather than relying solely on model scale.

Remark. Both bidirectional attention and unsupervised fine-tuning are indispensable to enable the generation of robust and generalizable representations for real-world website identification.

## 7 Discussion

Adaptability to Various LLMs. In this work, we adopt Llama3- 8B [20] as the backbone model due to resource constraints. However, our framework is model-agnostic, where larger LLM backbones can be incorporated via the same architectural modification and finetuning procedure on the trafic-learning objective. Furthermore, TraVerse reduces the overhead of frequent LLM fine-tuning by decoupling LLM-based representation learning from lightweight classifier updates, enabling eficient adaptation to feature drift.

Multi-Tab Attacks. In this work, we use a synthetic multi-tab dataset to evaluate the performance of TraVerse, as no real-user multi-tab dataset is currently available. In this setting, we formulate multi-tab identification as a multi-label classification problem. However, synthetic data may deviate from real multi-tab browsing behavior. An important direction is to evaluate diferent methods on real-user multi-tab trafic and explore targeted design improvements for handling concurrent trafic from multiple tabs.

Defense Mechanisms. Numerous WF defenses have been proposed to protect user privacy [4, 5, 9, 16, 18, 19, 29, 32, 48]. Existing defenses obfuscate trafic patterns via packet delays or dummy padding, whereas TraVerse is designed to remain adaptable. When complex defenses are deployed, a modest amount of defense-specific trafic can be collected to retrain the lightweight classifier. Since the fine-tuned LLM produces robust and generalizable trafic representations, retraining only the classifier is expected to sustain strong identification performance under evolving adversarial conditions.

## 8 Related Work

## 8.1 WF Attacks

WF attacks analyze trafic patterns to identify the websites being accessed. Early approaches rely on hand-crafted fingerprints [23, 36, 47], while subsequent methods leverage deep learning to automate feature extraction and enhance performance [42, 44]. Recent research focuses on enhancing attack eficiency and robustness. For instance, architectural innovations [2] and improved training strategies [35, 45] are proposed for data-limited settings, while other works strengthen trafic representations to enhance robustness against defenses [41, 43]. Multi-tab identification has been tackled via techniques such as trafic sectioning [8, 51, 53], attention-based mechanisms [12, 21, 28], and multi-label contrastive learning [55]. Eforts to tackle real-world complexities include NetCLR [1], which uses data augmentation to emulate dynamic conditions, and onlineWF [6], which performs continuous model updates using exit relay trafic. Beyond these, Holmes [11] investigates early-stage attacks via spatio-temporal analysis, and Countmamba [13] uni fies early-stage, multi-tab, and robustness settings by combining coarse-grained representations with fine-grained predictions.

![](images/7cd243be42a71bbe94471bac6b26c6ab5f938502a2a5a1908a8921dfe1dfeed2.jpg)  
(a) Precision<sub>w</sub>

![](images/3676fd7428f5452ea5c58ba3677c72092ac5b6970a334a14232ed358e12220df.jpg)  
Week<sub>(b)</sub> <sub>Recallw</sub>

![](images/3a6ce5768151d009faa0d28d190b8ebbdb7b2554b16a9f48dd3818be91e5dfc7.jpg)  
(c) F1<sub>w</sub>  
Figure 6: Adaptability analysis results of TraVerse.

Table 3: Ablation study results evaluated using Accuracy@3.

<table><tr><td>Method</td><td>Week 1</td><td>Week 2</td><td>Week 3</td><td>Week 4</td><td>Week 5</td><td>Week 6</td><td>Week 7</td><td>Week 8</td><td>Week 9</td><td>Week 10</td><td>Week 11</td><td>Week 12</td><td>Week 13</td></tr><tr><td>w/o Bidirectional Attention</td><td>0.513</td><td>0.459</td><td>0.475</td><td>0.454</td><td>0.428</td><td>0.360</td><td>0.405</td><td>0.461</td><td>0.444</td><td>0.427</td><td>0.387</td><td>0.338</td><td>0.384</td></tr><tr><td>w/o Unsupervised Fine-Tuning</td><td>0.521</td><td>0.424</td><td>0.444</td><td>0.424</td><td>0.408</td><td>0.345</td><td>0.416</td><td>0.431</td><td>0.429</td><td>0.405</td><td>0.386</td><td>0.353</td><td>0.415</td></tr><tr><td>Full TraVerse</td><td>0.694</td><td>0.612</td><td>0.625</td><td>0.602</td><td>0.588</td><td>0.513</td><td>0.583</td><td>0.609</td><td>0.608</td><td>0.577</td><td>0.553</td><td>0.517</td><td>0.570</td></tr></table>

TraVerse departs from prior WF attacks by targeting real-world identification on real-user trafic, addressing high intra-class diver sity and poor adaptability under dynamic, evolving conditions.

## 8.2 LLM for Trafic Classification

LLMs have recently demonstrated remarkable capabilities in traf fic classification. Existing eforts can be broadly categorized into pretraining-based and fine-tuning-based approaches. Pretraining based methods use self-supervised learning over packet- or flowlevel features to capture intrinsic trafic characteristics. For exam ple, ET-BERT [31], TraficFormer [56] and PTU [37] optimize trafic representations and design trafic-tailored pretraining tasks based on BERT [14], while NetGPT [34] and TraficGPT [39] leverage GPT-2 [40] for trafic classification and generation. YaTC [54] and Flow-MAE [22] further employ Masked AutoEncoders (MAE) to achieve efective feature extraction. In contrast, fine-tuning-based approaches adapt pretrained models to downstream trafic tasks via task-specific fine-tuning. TraficLLM [7] uses prompt tuning for trafic detection and generation, and ETooL [30] integrates flowgraph structures for robust detection under non-IID trafic.

However, existing methods primarily rely on packet payloads or datagrams, which provide limited information under the multilayer encrypted trafic of Tor. In this work, we extend LLMs to WF using content-agnostic packet-sequence features, enabling robust modeling under the challenges ofreal-world website fingerprinting.

## 9 Conclusion

In this work, we develop TraVerse, a framework designed to achieve robust WF attacks under dynamic real-world conditions characterized by diverse network environments, substantial intra-website variability, and continuous temporal drift. To address these challenges, TraVerse customizes the LLM through model architectural adaptation and extensive fine-tuning, to learn robust and generalizable representations for real-world trafic. Moreover, the lightweight classifier design allows eficient updates with a modest number of labeled samples, sustaining long-term efectiveness under evolving trafic distributions. Experiments on 13 weeks of real-user trafic show that TraVerse improves Accuracy@3 by 176.3% over state-of-the-art WF baselines in the closed-world setting.

## Acknowledgments

We thank our anonymous reviewers for their helpful comments and feedback. The work is supported in part by National Natural Science Foundation of China under Grant 62132011, National Science Foundation for Distinguished Young Scholars of China under Grant 62425201, the Science Fund for Creative Research Groups of the National Natural Science Foundation of China under Grant 62221003, Fundamental and Interdisciplinary Disciplines Breakthrough Plan of the Ministry of Education of China under Grant JYB2025XDXM114, Beijing-Tianjin-Hebei Natural Science Foundation Cooperation Project under Grant 25JJJJC0003 and Ant Group Postdoctoral Programme.

## References

[1] Alireza Bahramali, Ardavan Bozorgi, and Amir Houmansadr. 2023. Realistic website fingerprinting by augmenting network traces. In Proceedings of the 2023 ACM SIGSAC Conference on Computer and Communications Security. 1035–1049.

[2] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2019. Var-CNN: A data-eficient website fingerprinting attack based on deep learning. Proceedings on Privacy Enhancing Technologies 2019, 4 (2019), 292–310

[3] Tom B. Brown, Benjamin Mann, Nick Ryder, et al. 2020. Language Models are Few-Shot Learners. arXiv:2005.14165 [cs.CL] https://arxiv.org/abs/2005.14165

[4] Xiang Cai, Rishab Nithyanand, and Rob Johnson. 2014. Cs-buflo: A congestion sensitive website fingerprinting defense. In Proceedings ofthe 13th Workshop on Privacy in the Electronic Society. 121–130

[5] Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson, and Ian Goldberg. 2014. A systematic approach to developing and evaluating website fingerprinting defenses. In Proceedings ofthe 2014 ACM SIGSAC Conference on Computer and Communications Security. 227–238.

[6] Giovanni Cherubin, Rob Jansen, and Carmela Troncoso. 2022. Online website fingerprinting: Evaluating website fingerprinting attacks on Tor in the real world. In 31st USENIX Security Symposium (USENIX Security 22). 753–770.

[7] Tianyu Cui, Xinjie Lin, Sijia Li, Miao Chen, Qilei Yin, Qi Li, and Ke Xu. 2025. TraficLLM: Enhancing Large Language Models for Network Trafic Analysis with Generic Trafic Representation. arXiv:2504.04222 [cs.LG] https://arxiv.org/ abs/2504.04222

[8] Weiqi Cui, Tao Chen, Christian Fields, Julianna Chen, Anthony Sierra, and Eric Chan-Tin. 2019. Revisiting assumptions for website fingerprinting attacks. In Proceedings of the 2019 ACM Asia Conference on Computer and Communications Security. 328–339.

[9] Wladimir De la Cadena, Asya Mitseva, Jens Hiller, Jan Pennekamp, Sebastian Reuter, Julian Filter, Thomas Engel, Klaus Wehrle, and Andriy Panchenko. 2020. Traficsliver: Fighting website fingerprinting attacks with trafic splitting. In Proceedings ofthe 2020 ACMSIGSAC Conference on Computerand Communications Security. 1971–1985.

[10] Xinhao Deng, Jingyou Chen, Linxiao Yu, Yixiang Zhang, Zhongyi Gu, Changhao Qiu, Xiyuan Zhao, Ke Xu, and Qi Li. 2025. Beyond a Single Perspective: Towards a Realistic Evaluation of Website Fingerprinting Attacks. arXiv:2510.14283 [cs.CR] https://arxiv.org/abs/2510.14283

[11] Xinhao Deng, Qi Li, and Ke Xu. 2024. Robust and reliable early-stage Website fingerprinting attacks via spatial-temporal distribution analysis. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. 1997–2011.

[12] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust Multi-tab Website Fingerprinting Attacks in the Wild. In IEEE Symposium on Security and Privacy (SP).

[13] Xianwen Deng, Ruijie Zhao, Yanhao Wang, Mingwei Zhan, Zhi Xue, and Yijun Wang. 2025. Countmamba: A Generalized Website Fingerprinting Attack via Coarse-Grained Representation and Fine-Grained Prediction . In 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, Los Alamitos, CA, USA, 1419–1437. doi:10.1109/SP61157.2025.00154

[14] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In Proceedings ofthe 2019Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), Jill Burstein, Christy Doran, and Thamar Solorio (Eds.). Association for Computational Linguistics, Minneapolis, Minnesota, 4171–4186. doi:10.18653 v1/N19-1423

[15] Roger Dingledine, Nick Mathewson, and Paul Syverson. 2004. Tor: The Second Generation Onion Router. In 13th USENIX Security Symposium (USENIX Security 04). USENIX Association, San Diego, CA. https://www.usenix.org/conference/ 13th-usenix-security-symposium/tor-second-generation-onion-router

[16] Kevin P Dyer, Scott E Coull, Thomas Ristenpart, and Thomas Shrimpton. 2012. Peek-a-boo, i still see you: Why eficient trafic analysis countermeasures fail. In 2012 IEEE symposium on security and privacy. IEEE, 332–346.

[17] Jiajun Gong, Wei Cai, Siyuan Liang, Zhong Guan, Tao Wang, and Ee-Chien Chang. 2024. WFCAT: Augmenting Website Fingerprinting with Channel-wise Attention on Timing Features. arXiv preprint arXiv:2412.11487 (2024).

[18] Jiajun Gong and Tao Wang. 2020. Zero-delay lightweight defenses against website fingerprinting. In Proceedings of the 29th USENIX Conference on Security Symposium. 717–734.

[19] Jiajun Gong, Wuqi Zhang, Charles Zhang, and Tao Wang. 2022. Surakav: Generating Realistic Traces for a Strong Website Fingerprinting Defense. In 2022 IEEE Symposium on Security and Privacy (SP). IEEE, 1558–1573.

[20] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, et al. 2024. The Llama 3 Herd of Models. arXiv:2407.21783 [cs.AI] https://arxiv.org/abs/2407.21783

[21] Zhong Guan, Gang Xiong, Gaopeng Gou, Zhen Li, Mingxin Cui, and Chang Liu. 2021. BAPM: Block Attention Profiling Model for Multi-tab Website Finger printing Attacks on Tor. In Annual Computer Security Applications Conference. 248–259.

[22] Zijun Hang, Yuliang Lu, Yongjie Wang, and Yi Xie. 2023. Flow-mae: Leveraging masked autoencoder for accurate, eficient and robust malicious trafic classification. In Proceedings ofthe 26th International Symposium on Research in Attacks, Intrusions and Defenses. 297–314

[23] Jamie Hayes, George Danezis, et al. 2016. k-fingerprinting: A Robust Scalable Website Fingerprinting Technique. In USENIX security symposium. 1187–1203.

[24] Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. LoRA: Low-Rank Adaptation of Large Language Models. arXiv:2106.09685 [cs.CL] https://arxiv.org/abs/2106.09685

[25] Rob Jansen. [n. d.]. CELLSHIFT: RTT-Aware Trace Transduction for Real-World Website Fingerprinting. ([n. d.]).

[26] Rob Jansen, Ryan Wails, and Aaron Johnson. 2024. A measurement of genuine tor traces for realistic website fingerprinting. arXiv preprint arXiv:2404.07892 (2024).

[27] Rob Jansen, Ryan Wails, and Aaron Johnson. 2024. Repositioning Real-World Website Fingerprinting on Tor. In Proceedings ofthe 23rd Workshop on Privacy in the Electronic Society (Salt Lake City, UT, USA) (WPES ’24). Association for Computing Machinery, New York, NY, USA, 124–140. doi:10.1145/3689943.3695047

[28] Zhaoxin Jin, Tianbo Lu, Shuang Luo, and Jiaze Shang. 2023. Transformer-based Model for Multi-tab Website Fingerprinting Attack. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security. 1050–1064.

[29] Marc Juárez, Mohsen Imani, Mike Perry, Claudia Dıaz, and Matthew Wright. 2015. WTF-PAD: toward an eficient website fingerprinting defense for tor. CoRR, abs/1512.00524 (2015).

[30] Xinjie Lin, Gang Xiong, Gaopeng Gou, Wenqi Dong, Jing Yu, Zhen Li, and Wei Xia. 2025. Respond to Change With Constancy: Instruction-Tuning With LLM for Non-I.I.D. Network Trafic Classification. IEEE Transactions on Information Forensics and Security 20 (2025), 5758–5773. doi:10.1109/tifs.2025.3574971

[31] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. Et-bert: A contextualized datagram representation with pre-training transformers for encrypted trafic classification. In Proceedings of the ACM Web Conference 2022. 633–642.

[32] David Lu, Sanjit Bhat, Albert Kwon, and Srinivas Devadas. 2018. Dynaflow: An eficient website fingerprinting defense based on dynamically-adjusting flows. In Proceedings ofthe 2018 Workshop on Privacy in the Electronic Society. 109–113.

[33] Nate Mathews, James K Holland, Se Eun Oh, Mohammad Saidur Rahman, Nicholas Hopper, and Matthew Wright. 2023. Sok: A critical evaluation of eficient website fingerprinting defenses. In 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 969–986.

[34] Xuying Meng, Chungang Lin, Yequan Wang, and Yujun Zhang. 2025. NetGPT: Generative Pretrained Transformer for Network Trafic. arXiv:2304.09513 [cs.NI] https://arxiv.org/abs/2304.09513

[35] Se Eun Oh, Nate Mathews, Mohammad Saidur Rahman, Matthew Wright, and Nicholas Hopper. 2021. GANDaLF: GAN for data-limited fingerprinting. Proceedings on privacy enhancing technologies 2021, 2 (2021).

[36] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zinnen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale. In NDSS.

[37] Lingfeng Peng, Xiaohui Xie, Sijiang Huang, Ziyi Wang, and Yong Cui. 2024. Ptu: Pre-Trained Model for Network Trafic Understanding. In 2024 IEEE 32nd International Conference on Network Protocols (ICNP). IEEE, 1–12.

[38] Tobias Pulls. 2020. Towards efective and eficient padding machines for Tor. arXiv preprint arXiv:2011.13471 (2020).

[39] Jian Qu, Xiaobo Ma, and Jianfeng Li. 2024. TraficGPT: Breaking the Token Barrier for Eficient Long Trafic Analysis and Generation. arXiv:2403.05822 [cs.LG] https://arxiv.org/abs/2403.05822

[40] Alec Radford, Jef Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever. 2019. Language Models are Unsupervised Multitask Learners. https: //api.semanticscholar.org/CorpusID:160025533

[41] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gangadhara, and Matthew Wright. 2019. Tik-Tok: The utility of packet timing in website fingerprinting attacks. arXiv preprint arXiv:1902.06421 (2019).

[42] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. 2017. Automated website fingerprinting through deep learning. arXiv preprint arXiv:1708.06376 (2017).

[43] Meng Shen, Kexin Ji, Zhenbo Gao, Qi Li, Liehuang Zhu, and Ke Xu. 2023. Subvert ing website fingerprinting defenses with robust trafic representation. In 32nd USENIX Security Symposium (USENIX Security 23). 607–624.

[44] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fingerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings ofthe 2018 ACMSIGSAC Conference on Computerand Communications Security. 1928–1943.

[45] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security. 1131–1148.

[46] Tao Wang. 2020. High precision open-world website fingerprinting. In 2020 IEEE Symposium on Security and Privacy (SP). IEEE, 152–167.

Table 4: The default hyperparameter settings of TraVerse.

<table><tr><td>Module</td><td>Hyperparameter</td><td>Value</td></tr><tr><td rowspan="6">Unsupervised Representation Learning</td><td>Burst Dimension</td><td>300</td></tr><tr><td>Max Input Length</td><td>512</td></tr><tr><td>Masked Ratio</td><td>0.2</td></tr><tr><td>LoRA Rank</td><td>8</td></tr><tr><td>Max Training Steps</td><td>30,000</td></tr><tr><td>Output Dimension</td><td>4,096</td></tr><tr><td>Few-Shot Supervised Classification</td><td>Hidden Dimension</td><td>1,024</td></tr></table>

[47] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective attacks and provable defenses for website fingerprinting. In 23rd USENIX Security Symposium (USENIX Security 14). 143–157.

[48] Tao Wang, Ian Goldberg, et al. 2017. Walkie-Talkie: An Eficient Defense Against Passive Website Fingerprinting Attacks. In USENIX Security Symposium. 1375– 1390.

[49] Yanbin Wang, Haitao Xu, Zhenhao Guo, Zhan Qin, and Kui Ren. 2022. snWF: Website Fingerprinting Attack by Ensembling the Snapshot of Deep Learning. IEEE Transactions on Information Forensics and Security 17 (2022), 1214–1226. doi:10.1109/TIFS.2022.3158086

[50] Duo Wu, Xianda Wang, Yaqi Qiao, Zhi Wang, Junchen Jiang, Shuguang Cui, and Fangxin Wang. 2024. Netllm: Adapting large language models for networking. In Proceedings ofthe ACM SIGCOMM 2024 Conference. 661–678.

[51] Yixiao Xu, Tao Wang, Qi Li, Qingyuan Gong, Yang Chen, and Yong Jiang. 2018. A multi-tab website fingerprinting attack. In Proceedings of the 34th Annual Computer Security Applications Conference. 327–341.

[52] An Yang, Anfeng Li, Baosong Yang, et al. 2025. Qwen3 Technical Report. arXiv:2505.09388 [cs.CL] https://arxiv.org/abs/2505.09388

[53] Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, and Yixiao Xu. 2021. An Automated Multi-Tab Website Fingerprinting Attack. IEEE Transactions on Dependable and Secure Computing 19, 6 (2021), 3656–3670.

[54] Ruijie Zhao, Mingwei Zhan, Xianwen Deng, Yanhao Wang, Yijun Wang, Guan Gui, and Zhi Xue. 2023. Yet another trafic classifier: A masked autoencoder based trafic transformer with multi-level flow representation. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 37. 5420–5427.

[55] Xiyuan Zhao, Xinhao Deng, Qi Li, Yunpeng Liu, Zhuotao Liu, Kun Sun, and Ke Xu. 2024. Towards Fine-Grained Webpage Fingerprinting at Scale. In Proceedings of the 2024 on ACM SIGSAC Conference on Computer and Communications Security. 423–436.

[56] Guangmeng Zhou, Xiongwen Guo, Zhuotao Liu, Tong Li, Qi Li, and Ke Xu. 2024. Traficformer: an eficient pre-trained model for trafic data. In 2025 IEEE Symposium on Security and Privacy (SP). IEEE Computer Society, 102–102.

## A Details of LoRA Fine-Tuning

Low-Rank Adaptation (LoRA) [24] is a widely used technique that introduces low-rank trainable matrices into transformer layers to approximate the updates of an LLM while keeping the original pretrained parameters frozen, thereby enabling parameter-eficient fine-tuning. Formally, for a weight matrix $W \in \mathbb { R } ^ { d \times k }$ , instead of updating � directly, LoRA represents the update as a low-rank decomposition:

$$
W ^ {\prime} = W + \Delta W, \quad \Delta W = A B,\tag{5}
$$

where $A \in \mathbb { R } ^ { d \times r } , B \in \mathbb { R } ^ { r \times k }$ , and $r \ll \operatorname* { m i n } ( d , k ) . \ : r$ is the rank hyperparameter that controls the number of additional trainable parameters. During training, only � and � are updated, while � remains frozen. This design substantially reduces the number of trainable parameters and memory consumption, allowing eficient adaptation of large pretrained LLMs to trafic-specific downstream tasks without full-scale fine-tuning.

## B Implementation Details of TraVerse

We prototype TraVerse using Python 3.10 and Transformers 4.44.2, and adopt Llama3-8B [20] as the backbone model. Table 4 summarizes the default hyperparameter settings used throughout our evaluation. Figure 8 and Figure 9 present the prompt templates for unsupervised fine-tuning and supervised classification, respectively.

## C Details of Datasets

Our datasets are derived from GTT23 [26] and cover closed-world, open-world, and multi-tab evaluations.

Closed-World Dataset GTT . For the closed-world evaluation, both training and test trafic are drawn from a total of200 monitored websites. Trafic from Week 1 is used for training and validation, with 10 samples per website for training and 1 sample per website for validation. We also use trafic from Week 1 for testing, with 75 samples per website. To assess the robustness of TraVerse under temporal drift, we further evaluate on trafic from Weeks 2–13, where the test sets are substantially large. Unlike the training and validation sets, the sample number per website in these test sets is not fixed, reflecting the base rate and trafic distribution encountered in the real world. The precise number of test samples for each week is shown in Table 5.

Open-World Dataset GTT<sub>OW</sub>. For the open-world evaluation, trafic can originate from a large number of unmonitored websites, which are collectively treated as the same unmonitored class. In addition to the monitored trafic used in the closed-world setting, we include 2,000 and 100 samples from unmonitored websites for training and validation, with each sample corresponding to a distinct website. For testing, we incorporate 5,000 unmonitored samples per week, also drawn from disjoint websites, ensuring that none of these websites overlap with those used for classifier training or LLM fine-tuning. The number of test samples for each week is shown in Table 5.

Multi-Tab Dataset GTT . Since no real-user multi-tab dataset is publicly available, we follow the method in [21] to synthesize a multi-tab dataset from GTT23. Specifically, we construct a 2-tab scenario and introduce a random inter-tab delay between 3 and 5 seconds. We use the training, validation, and test sets from Week 1 to generate the corresponding multi-tab training, validation, and test samples. The resulting multi-tab dataset contains 4,000 training samples, 200 validation samples, and 5,000 test samples.

## D Details of Baselines

We select nine state-of-the-art WF methods and one LLM-based method to benchmark the performance of TraVerse.

• Single-Tab WF Methods. DF [44] employs deep neural networks composed of CNN blocks trained on packet direction sequences. Tik-Tok [41] extends DF by incorporating both packet direction and timestamp information. Var-CNN [2] improves the model architecture by introducing dilated convolution and other structural enhancements. TF [45] leverages the triplet network to capture inter-website diferences for few-shot identification. RF [43] introduces a trafic representation mechanism, TAM, to improve robustness against defenses. NetCLR [1] integrates data augmentation with self-supervised learning to adapt to diverse network conditions.

(a) Precision<sub>w</sub>

![](images/bb75a3865c5a56aae7d7322181630a2e5c7d0e35e5a5d1e32174f319c4feaa74.jpg)

![](images/92dd5cdce9666623b7404e2b6c2bdbfb32156c473985fa094d2ba1eeed8897cd.jpg)  
Week(b) Recallw

![](images/1247f3afba5993a36c2070870df2a3231afa8e4c899ab059f6ad48a3ca74be75.jpg)  
(c) F1<sub>w</sub>  
Figure 7: Performance of TraVerse with diferent sample numbers.

Table 5: Number of test samples per week in the closed-world and open-world settings.

<table><tr><td>Scenario</td><td>Week 1</td><td>Week 2</td><td>Week 3</td><td>Week 4</td><td>Week 5</td><td>Week 6</td><td>Week 7</td><td>Week 8</td><td>Week 9</td><td>Week 10</td><td>Week 11</td><td>Week 12</td><td>Week 13</td></tr><tr><td>Closed-World</td><td>15,000</td><td>13,930</td><td>15,064</td><td>15,065</td><td>15,763</td><td>15,603</td><td>33,133</td><td>16,413</td><td>15,010</td><td>13,746</td><td>16,531</td><td>15,965</td><td>34,301</td></tr><tr><td>Open-World</td><td>20,000</td><td>18,930</td><td>20,064</td><td>20,065</td><td>20,763</td><td>20,603</td><td>38,133</td><td>21,413</td><td>20,010</td><td>18,746</td><td>21,531</td><td>20,965</td><td>39,301</td></tr></table>

```txt
Unsupervised Fine-Tuning Prompt Template
Input:
Traffic of browsing a website: <flow>: <burst sequence>:
{burst feature}.
```

Figure 8: Prompt template used for unsupervised fine-tuning.  
```txt
Supervised Classification Prompt Template
Instruction:
Given a traffic burst sequence as input, predict the website label.
Input:
<flow>: <burst sequence>: {burst feature}.
```  
Figure 9: Prompt template used for supervised classification.

• Multi-Tab WF Methods. TMWF [28] is a Transformer-based approaches for multi-tab WF attacks. ARES [12] designs a multiclassifier framework for enhanced multi-tab identification. Count mamba [13] enhances feature representations and employs a state-space-oriented classifier to predict websites in the multi tab setting.

• LLM-Based Methods. TraficLLM [7] is an LLM-based method that uses dual-stage tuning pipeline for trafic classification.

## E Metrics

For the closed-world setting, following [1, 11, 41, 44], we use four evaluation metrics: Accuracy@3, Precision $\mathrm { . w } ,$ Recall<sub>w</sub>, and $\mathrm { F } 1 _ { \mathrm { w } }$ Accuracy@3 measures whether the ground-truth label appears among the top three predicted classes, defined per sample as:

$$
\text { Accuracy@ } 3 = \mathbb {I} \big (y _ {i} \in \text { Top - 3 } (\hat {y} _ {i}) \big),\tag{6}
$$

where �� is the ground-truth label of the �-th sample, Top-t(�ˆ�) denotes the t classes with the highest predicted probabilities, and I(·) is an indicator function equal to 1 if the condition holds. Precision<sub>w</sub>, Recall<sub>w</sub>, and F1<sub>w</sub> are the weighted averages of Precision, Recall, and F1-score, respectively, where the weights are proportional to class frequencies in the dataset.

For the open-world setting, following [11, 46], we adopt r-precision as the evaluation metric, which is defined per sample as:

$$
\mathrm{r-precision} = \frac {R _ {T P}}{R _ {T P} + R _ {W P} + r \cdot R _ {F P}},\tag{7}
$$

where $R _ { T P } , R _ { W P }$ and $R _ { F P }$ denote true positive rate, wrong positive rate and false positive rate, respectively. In our evaluation, we set $r = 5 ,$ , where � denotes the ratio of visits to unmonitored websites relative to monitored websites.

For the multi-tab setting, following [55], we use Recall@k with � = 10 and AP@k with $k = 2 ,$ , defined per sample as:

$$
\text { Recall@ } k = \frac {\| y _ {i} \cap \text { Top- } k (\hat {y} _ {i}) \|}{\| y _ {i} \|}.\tag{8}
$$

$$
A P @ k = \frac {1}{\min (k , \| y _ {i} \|)} \sum_ {t = 1} ^ {k} \frac {\| y _ {i} \cap \operatorname{Top-} t (\hat {y} _ {i}) \|}{t}.\tag{9}
$$

## F Performance with Various Sample Numbers

We evaluate the performance of TraVerse across diferent sample sizes to investigate its adaptability in real-world scenarios. As websites are constantly evolving, we test the model’s ability to leverage a modest number of samples for rapid adaptation to feature drift. We conduct this experiment in the closed-world setting, varying the sample number per website from 5, 10, 15, to 20. We use Precision<sub>w</sub>, Recall and $\mathrm { F } 1 _ { \mathrm { w } }$ as metrics.

The results in Figure 7 demonstrate the efectiveness of TraVerse with varying numbers of labeled samples. Specifically, increasing the sample number from 5 to 10, 10 to 15, and 15 to 20 yields F1<sub>w</sub> improvements of 15.5%, 3.7%, and 4.8%, respectively. The largest gain is obtained when increasing the sample number from 5 to

![](images/6eccb997a9bf5fed191d8ed547e500a77819ab0090861514284861d18177ae07.jpg)  
(a) Precision<sub>w</sub>

![](images/cb8cd5e6f28240b6fad7285147c457b7b8856c1e0bd9fbe44e21d0a679717799.jpg)  
Week<sup>(b)</sup> <sup>Recall</sup>w

![](images/29d4a496fd8b201c2313ae198f1761b019f6808d940cb98b76bff04127a45ff4.jpg)  
(c) F1<sub>w</sub>  
Figure 10: Performance of TraVerse with various model sizes.

10, after which the improvements become markedly smaller, in dicating diminishing returns beyond 10 samples. With only 10 samples, TraVerse achieves average Precision<sub>w</sub> , Recall<sub>w</sub> and $\mathrm { F } 1 _ { \mathrm { w } }$ of approximately 0.57, 0.45 and 0.47 across 13 weeks, respectively. This eficiency stems from the robust and transferable trafic repre sentations learned by the fine-tuned LLM, which support accurate website identification with few labeled samples.

Remark. TraVerse requires only a modest number of samples to achieve accurate website identification, underscoring its ability to adapt eficiently under dynamic real-world conditions.

## G Performance with Various Model Sizes

In this section, we study the impact of backbone model size on TraVerse to determine whether its improvements are primarily driven by scaling the LLM. Specifically, we instantiate TraVerse with three backbone sizes, including the 1B, 3B, and 8B variants. All experiments are conducted on the closed-world dataset GTT<sub>CW</sub>, and we report Precision<sub>w</sub>, Recall<sub>w</sub> and $\mathrm { F } 1 _ { \mathrm { w } }$

Figure 10 shows that increasing model size yields only marginal improvements. In particular, the 8B variant achieves an average $\mathrm { F } 1 _ { \mathrm { w } }$ gain of 4.8% over the 1B model and 2.2% over the 3B model. The same trend is observed for Precision<sub>w</sub> and Recall<sub>w</sub>, indicating that the overall benefit from scaling is limited in this setting. These results suggest that the performance of TraVerse is not solely driven by larger model scale. Instead, the proposed domain-specific adaptation plays a critical role in enabling LLMs to generate robust representations for real-world trafic.

Remark. Overall, reducing the model size from 8B to 1B leads to only a modest performance degradation. This indicates that TraVerse is relatively insensitive to model scale and can retain competitive performance even when deployed with smaller backbones.
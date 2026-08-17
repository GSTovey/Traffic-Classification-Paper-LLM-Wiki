# Talk Like a Packet: Rethinking Network Traffic Analysis with Transformer Foundation Models

Samara Mayhoub, Chuan Heng Foh, Senior Member, IEEE, Mahdi Boloursaz Mashhadi, Senior Member, IEEE, Mohammad Shojafar, Senior Member, IEEE, and Rahim Tafazolli, Fellow, IEEE

Abstract—Inspired by the success of Transformer-based models in natural language processing, this paper investigates their potential as foundation models for network traffic analysis. We propose a unified pre-training and fine-tuning pipeline for traffic foundation models. Through fine-tuning, we demonstrate the generalizability of the traffic foundation models in various downstream tasks, including traffic classification, traffic characteristic prediction, and traffic generation. We also compare against non-foundation baselines, demonstrating that the foundationmodel backbones achieve improved performance. Moreover, we categorize existing models based on their architecture, input modality, and pre-training strategy. Our findings show that these models can effectively learn traffic representations and perform well with limited labeled datasets, highlighting their potential in future intelligent network analysis systems.

Index Terms—Transformer, Foundation Models, Network Traffic Analysis, Large Language Models, Pre-training, Fine-tuning.

# INTRODUCTION

Transformer-based Large Language Models (LLMs) such as BERT, GPT, LLaMA, and T5 have revolutionized Natural Language Processing (NLP) by achieving high performance in a wide range of tasks, including question answering and text generation. These models learn to understand human language by pre-training on large unlabeled datasets using selfsupervised objectives, and then adapting to downstream tasks with minimal fine-tuning. In networks, an analogous need exists to understand network traffic for network traffic analysis tasks such as traffic classification and traffic characteristic prediction. Historically, these problems were addressed using port-based identification and Deep Packet Inspection (DPI) and later by supervised machine learning (ML) models trained on handcrafted features. However, increasing encryption, evolving traffic behavior and services, and the high cost of manual labeling have reduced the effectiveness and generalizability of these traditional approaches.

Inspired by the success of Transformer-based LLMs, researchers have begun to explore whether similar models can be applied to a new kind of language: The Language of Network Traffic. In this approach, sequences of packets (referred to as flows) are treated like sentences, enabling Transformerbased architectures to model structural and semantic patterns S. Mayhoub is with Aston University, Birmingham, UK (e-mail: mayhoubs@aston.ac.uk).

C. H. Foh, M. B. Mashhadi, M. Shojafar and R. Tafazolli are with 6GIC, Institute for Communication Systems, University of Surrey, Guildford, GU2 7XH, UK (e-mail: {c.foh, m.boloursazmashhadi, m.shojafar, r.tafazolli}@surrey.ac.uk).

in raw traffic data. This motivates traffic foundation models: Transformer backbones pre-trained on large-scale unlabeled traffic and fine-tuned for multiple downstream tasks.

This paper aims to answer the following questions: Q1) How can Transformer-based foundation models be adapted to learn the Language of Network Traffic? Q2) In what ways do architectural choices, input modalities, and pre-training strategies influence the effectiveness of these models? Q3) Can such models generalize across diverse downstream tasks to improve performance and support future intelligent network analysis systems?

The main contributions of this article are as follows:

• We propose a unified pipeline for pre-training and finetuning Transformer-based Traffic Foundation Models.   
• We present a taxonomy of recent models, categorized by architecture, input modality, and pre-training strategy.   
• We establish structural awareness as a key design principle for modeling traffic and analyze how models incorporate it across different traffic representation strategies.   
• We demonstrate that foundation models generalize effectively across three downstream tasks: classification, prediction of traffic characteristics, and generation, and quantify the benefit of Transformer models via comparisons with non-foundation baselines.

The remainder of this paper is organized as follows. We first outline the key challenges in network traffic analysis. We then provide a taxonomy of traffic foundation models. Next, we describe the proposed unified workflows for pre-training and fine-tuning. Through several use-cases, we present finetuning results, demonstrate model generalization across diverse downstream tasks and compare with non-foundation baselines. Finally, we outline future directions and conclude the paper.

# CHALLENGES IN NETWORK TRAFFIC ANALYSIS

Network Traffic Analysis is essential for network management and cybersecurity, enabling tasks such as traffic classification, intrusion detection, and traffic monitoring [1]. The goal is to extract meaningful insights from raw traffic data, such as identifying applications, detecting attack types, or predicting traffic characteristics like flow volume. However, increasing encryption and emerging services have increased traffic variability, reducing the effectiveness of traditional methods and necessitating more intelligent approaches.

# LIMITATIONS OF TRADITIONAL METHODS

DPI methods have become ineffective due to widespread encryption, which obscures payloads [1]–[3]. Port-based methods struggle, as applications increasingly use dynamic or shared ports, while DPI fails without access to plaintext payloads. As traffic becomes more complex, these methods lose accuracy, prompting a shift toward learning approaches without payload decryption.

# LIMITATIONS OF SUPERVISED MACHINE LEARNING APPROACHES

Supervised ML has emerged as an alternative to traditional traffic analysis by learning from manually selected flow features [2], [3]. However, early methods often depend on handcrafted statistical features, which lack adaptability to diverse traffic conditions [4]. These models also require large volumes of labeled data, which is difficult to obtain, especially due to incomplete handshakes, missing DNS records, or ambiguous server names [5], [6]. Moreover, supervised ML models often generalize poorly to unseen datasets or zero-day attack types [7], making them challenging to deploy in realworld environments [8].

# LIMITATIONS OF SUPERVISED DEEP LEARNING APPROACHES

Supervised Deep Learning (DL) methods, such as Convolutional Neural Networks, have shown success in modeling complex patterns from raw traffic data [9]. They eliminate the need for manual feature selection and are widely applied to encrypted traffic classification. However, their performance depends heavily on large, accurately labeled datasets [4], which are often costly or limited by privacy concerns. These models also tend to generalize poorly to unseen traffic or new protocols [6]. Additionally, they struggle with capturing longrange dependencies. These challenges have driven interest in self-supervised and pre-training-based methods that leverage raw, unlabeled traffic data.

# NEED FOR GENERALIZABLE, DATA-DRIVEN MODELS

Modern networks require models that generalize across multiple tasks such as classification, prediction, and generation, while adapting to evolving traffic patterns. As shown earlier, traditional and supervised methods fall short, relying on manual feature engineering and large labeled datasets, which are costly and inflexible. To overcome these limitations, there is a growing shift toward data-driven models that learn directly from raw traffic without handcrafted features. Pre-training and self-supervised learning enable such models to extract rich representations from raw traffic data, reducing labeling costs. These models also support diverse input modalities, making them ideal for unified, multitask traffic analysis [1]. As a result, generalizable, data-driven models are becoming essential components of next-generation network analysis systems.

# TRANSFORMERS AS A FOUNDATION FOR NETWORK TRAFFIC ANALYSIS

A Transformer consists of an encoder–decoder architecture built from stacked self-attention and feed-forward layers [10]. The encoder generates contextualized representations from input sequences, while the decoder produces outputs conditioned on the previously generated tokens and the encoder’s output. Transformer’s core innovation is the self-attention mechanism, which lets each token incorporate context from other tokens in the sequence via learned query, key, and value projections; multi-head attention performs this in parallel to capture different types of relationships. In practice, a Transformer can be used as an encoder-only, a decoder-only, or an encoder– decoder backbone, depending on the task.

# FOUNDATION MODELS FOR TRAFFIC ANALYSIS MOTIVATION

The limitations of traditional ML/DL models have prompted a shift toward more data-efficient paradigms. Inspired by the success of Transformers in NLP and Computer Vision (CV), researchers have begun developing Transformer-based foundation models that learn rich traffic representations from unlabeled data. These models serve as backbones for diverse downstream tasks such as classification, flow characteristic prediction, and traffic generation.

# KEY CONCEPTS

• Self-Supervised Learning (SSL): In the context of network traffic, SSL learns meaningful representations from unlabeled traffic by solving pseudo tasks like masked byte prediction, packet ordering, or flow reconstruction. These leverage the inherent traffic structure to produce transferable features.   
• Pre-training and Fine-tuning: SSL is often used for pretraining, where models learn general representations from large unlabeled data. These models are then fine-tuned on smaller labeled datasets for downstream tasks.   
• Foundation Models for Network Traffic Analysis: These are large-scale pre-trained models, designed as backbones for diverse traffic analysis tasks. They are often built using SSL on massive traffic datasets, they offer strong generalization on various tasks.

# TAXONOMY OF TRANSFORMER-BASED FOUNDATION MODELS

We categorize recent foundation models for network traffic analysis into five groups (see Fig. 1), based on their underlying Transformer architecture:

Encoder-only Foundation Models (BERT-style): These models are inspired by the success of BERT (Bidirectional Encoder Representations from Transformers) in NLP [11]. They learn contextualized network traffic representations using encoder-only architectures.

PERT [2] (Payload Encoding Representation from Transformer) adapts a lightweight BERT to tokenize payload bytes and learn their contextual distributions through pre-training. PERT is motivated by dynamic word embedding in NLP, based on the belief that communication protocols share characteristics with natural human language that can be modeled with NLP-inspired architectures.

ET-BERT [3] (Encrypted Traffic Bidirectional Encoder Representations from Transformer) is a BERT-based model designed to learn general representations from unlabeled encrypted traffic. Its key innovation lies in tokenizing raw packets into ’language-like tokens’ by extracting BURSTs (unidirectional packet sequences), converting them into hex strings, and applying a bi-gram model with Byte-Pair Encoding. ET-BERT introduces two SSL tasks: Masked BURST Modeling for capturing intra-BURST byte dependencies, and Same-origin BURST Prediction for modeling flow-level context. Compared to PERT, ET-BERT features more advanced tokenization and pre-training strategies.

![](images/79676cbc07d6a43b1f39bd66ff6ed1d5499b3363a77be8a23219c9ddf2aab3f3.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
    A["Traffic Foundation Models"] --> B["GPT/LLaMA Style"]
    A --> C["Hybrid-Style"]
    A --> D["T5-Style"]
    A --> E["ViT-Style"]
    A --> F["BERT-Style"]
    B --> G["NetGPT"]
    B --> H["TrafficLLM"]
    B --> I["TrafficGPT"]
    C --> J["PACKETCLIP"]
    D --> K["Lens"]
    E --> L["Flow-MAE"]
    E --> M["YaTC"]
    F --> N["ET-BERT"]
    F --> O["PERT"]
    F --> P["NetFound"]
    F --> Q["MLETC"]
    F --> R["PEAN"]
```
</details>

Fig. 1: Taxonomy of Transformer-based traffic foundation models.

PEAN [6] (Packet Embedding Attention Network) uses a BERT-style encoder to capture intra- and inter-packet patterns by combining raw byte sequences with packet length statistics. Pre-training is conducted using a masked language modeling objective.

netFound [12] is designed to capture the unique structure and semantics of network data, moving beyond simply treating network traffic as natural language. Its key innovations include: (1) multi-modal embeddings of packet fields and flow metadata; (2) protocol-aware tokenization that segments packets by protocol fields instead of fixed chunks to preserve semantics; and (3) a hierarchical Transformer with skip connections to capture multi-level dependencies. Masked Token Prediction task has been used to pre-train netFound on unlabeled traffic.

MLETC [13] (Multi-Level Encrypted Traffic Classifier) is the first model to explicitly incorporate field-level structure into the pre-training, going beyond byte- and packet-level representations. Built on the DeBERTa architecture, it introduces two SSL strategies: Masked Fields Prediction (MFP) and Same-Origin Flow Prediction (SOFP). MFP masks entire header fields and payload bytes as semantic units, preserving structural integrity. This approach also requires separate models for TCP and UDP due to their distinct header layouts. SOFP, meanwhile, models inter-packet dynamics by predicting whether specific sub-flows originate from the same flow.

Masked Autoencoder-based Foundation Models (ViT-style): These models are inspired by ViT (Vision Transformers), originally developed for CV tasks. They treat network traffic as image-like inputs and often adopt the Masked Autoencoder (MAE) framework for pre-training.

YaTC [1] (Yet Another Traffic Classifier) introduces a ViTbased architecture within an MAE framework. It represents traffic using a Multi-level Flow Representation (MFR) matrix, which encodes byte-, packet-, and flow-level information. By treating bytes as pixels, the model captures structured patterns of network traffic. YaTC defines an SSL strategy: Masked Patch Reconstruction, where a high ratio (90%) of MFR patches are randomly masked, and the model learns to reconstruct the missing content using an encoder–decoder ViT.

Flow-MAE [5] introduces a ViT-based architecture under the MAE framework to improve efficiency in traffic classification. It addresses key limitations of BERT-based models, notably limited input length and reliance on BPE, by replacing it with patch embeddings. Using ”bursts” (packets from a flow) as the fundamental unit, Flow-MAE applies a 1D convolutional layer to convert these into fixed-sized patches. It extracts both packet headers and payloads for richer flow representation. Flow-MAE adopts a single SSL task: Masked Patch Modeling, where input patches are randomly masked and reconstructed to learn contextual representations.

Encoder–Decoder Foundation Models (T5-style): These models follow the T5 architecture [14], leveraging an encoder–decoder for both traffic generation and classification tasks. Lens [4] applies the T5 framework to network traffic, learning generalized representations via WordPiece-tokenized hex inputs. Lens introduces three SSL tasks: Masked Span Prediction to recover masked spans (contiguous sequence of tokens) and learn contextual representations; Packet Order Prediction to capture temporal information by predicting the order of the first three packets in a flow; and Homologous Traffic Prediction to determine whether two sub-flows originate from the same flow.

Decoder-only Foundation Models (GPT/LLaMA style): These models use autoregressive, decoder-only Transformer architectures (e.g., GPT, LLaMA) to support both traffic generation and understanding via prompting.

NetGPT [15] is a GPT-2-based autoregressive model designed for both traffic generation and classification. It encodes network flows as unified hexadecimal sequences, preserving the semantics of both plaintext and ciphertext traffic. NetGPT reformulates traffic understanding as a generative task and adopts three key strategies: (1) header field shuffling for semantic-preserving augmentation, (2) packet segmentation using special tokens and segment embeddings to retain structure, and (3) prompt-based task conditioning to unify multiple tasks. Pre-training involves next-token prediction over the first three packets of each flow.

TrafficGPT [8] adopts a GPT-style autoregressive architecture enhanced with linear attention to support long sequence modeling. It tokenizes network traffic using hexadecimal representations and encodes temporal information via time interval tokens. To enable the generation of realistic traffic, it introduces a reversible tokenization scheme that allows reconstructing flows back into PCAP format. Pre-training is conducted using a next-token prediction objective over tokenized flows.

TrafficLLM [7] is a fine-tuning framework for decoder-only LLMs (such as LLaMA) that enables multimodal learning from text and network traffic via traffic-domain tokenization and instruction-based tuning. It employs a two-stage approach: (1) Natural Language Instruction Tuning to follow expert prompts, and (2) Traffic Tuning for diverse traffic analysis tasks.

![](images/d809f82f5cc8046c6bbd7922b15beabba4f0fbec46cd543ec4b1298225172ea0.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Raw Input"] --> B["Traffic Representations"]
    B --> C["Input Embeddings"]
    C --> D["Transformer-based Foundation Model"]
    D --> E["Pre-training objective"]

    subgraph Raw Input
        A1["01101100 01101111 01110110 01100101"]
        A2["TXT Traffic Flow Description (TrafficLLM, PACKETCLIP, Lens, NetGPT)"]
    end

    subgraph Traffic Representations
        B1["Packet Byte Sequences (ET-BERT, PERT)"]
        B2["Text Sequences (TrafficGPT, NetGPT, Lens)"]
        B3["Hierarchical Structures (NetFound, MLETC, PEAN)"]
        B4["Packet Bytes Patches (YaTC, Flow-MAE)"]
        B5["Multimodal Representations (PACKETCLIP, TrafficLLM)"]
    end

    subgraph Input Embeddings
        C1["Packet Embeddings (All)"]
        C2["Flow metadata Embeddings (NetFound, TrafficLLM, TrafficGPT)"]
        C3["Positional Embeddings (PERT, ET-BERT, NetFound, NetGPT, Lens, Flow-MAE, YaTC)"]
        C4["Text Embeddings (TrafficLLM, PACKETCLIP, Lens)"]
        C5["Graph Embeddings (PACKETCLIP)"]
        C6["Patch Embeddings (Flow-MAE, YaTC)"]
    end

    subgraph Transformer-based Foundation Model
        D1["BERT-Style ET-BERT PERT PEAN NetFound MLETC T5-Style Lens GPT/LLaMA Style TrafficLLM NetGPT TrafficGPT ViT-style Flow-MAE YaTC Hybrid-Style PACKETCLIP"]
    end

    subgraph Pre-training Objective
        E1["Masked Token Prediction (NetFound, ET-BERT, PERT, MLETC, PEAN)"]
        E2["Masked Patch Reconstruction (YaTC, Flow-MAE)"]
        E3["Autoregressive Generation (NetGPT, TrafficGPT, TrafficLLM)"]
        E4["Contrastive Learning (PACKETCLIP)"]
        E5["Same-Origin Prediction (ET-BERT, MLETC)"]
        E6["Packet Order Prediction (Lens)"]
    end
```
</details>

Fig. 2: Pre-training workflow for Transformer-based foundation models for network traffic analysis.

Hybrid Models: These models combine Transformer architectures with other neural network components to process multimodal traffic data. PACKETCLIP [9] is inspired by Contrastive Language–Image Pre-training (CLIP) technique. It aligns packet payloads with natural language in a shared embedding space using contrastive pre-training and simple projection heads with fixed text and packet encoders (LLaMA and ET-BERT). To enhance semantic reasoning, PACKETCLIP incorporates Graph Neural Networks operating on missionspecific Knowledge graphs generated by LLMs.

# PIPELINE OVERVIEW FOR TRAFFIC ANALYSIS WITH FOUNDATION MODELS

# TRAFFIC REPRESENTATION MODALITIES

The reviewed models adopt diverse strategies to represent raw traffic in formats suitable for Transformers. These representation approaches fall into two categories:

Single-Modality: Models with single-modality rely solely on network traffic data without incorporating external semantic sources like natural language descriptions of the traffic data. Byte Sequences: It treats network traffic as a continuous stream of raw bytes. For example, PERT [2] treats payload bytes as words in a sequence and uses dynamic word embeddings inspired by BERT. Also, ET-BERT [3] converts packet bytes into language-like tokens. Hierarchical Structures: It recognizes that network traffic is not merely a stream of bytes but possesses a multi-layered structure, with information organized at byte, field, packet, and flow levels. For example, MLETC [13] and NetFound [12] leverage this structure through protocol-aware tokenization, multilevel embeddings, and hierarchical Transformer architectures, enabling understanding across multiple semantic layers of traffic. Similarly, PEAN [6] combines raw byte sequences with packet length statistics, modeling intra-packet and inter-packet relationships. Image Representation: It transforms network data into 2D matrices, suitable for computer vision models. For example, YaTC [1] constructs a grayscale matrix per flow. Flow-MAE [5] also adopts a similar approach by segmenting bursts—treated as 1D byte sequences—into non-overlapping patches using a 1D convolutional layer, which are then embedded for ViT processing. Textual Representation: It converts packet content into hexadecimal strings for processing by LLM tokenizers. For example, Lens [4] serializes flow fields into hex-based token sequences with special delimiters to retain structure. Also, NetGPT [15] and TrafficGPT [8] encode each byte of the packet into a hexadecimal number.

Multi-Modality: These approaches combine different data types such as raw bytes, and natural language, as input. Packet + Text: PACKETCLIP [9] aligns packet-level data with natural language using contrastive pre-training. It uses ET-BERT to tokenize packets and LLaMA to generate descriptions from flow data. On the other hand, TrafficLLM [7] combines input derived from raw traffic (extracted using TShark) with expertcrafted natural language instructions.

# ENCODING STRUCTURE AWARENESS IN NETWORK TRAFFIC

Transformers are inherently permutation-invariant, meaning they do not understand the order of input tokens. Therefore, auxiliary mechanisms are necessary to capture sequence order and structural information. In network traffic, structural awareness is crucial due to the hierarchical nature of flows: a flow consists of multiple packets, each comprising a header and a payload, with headers containing structured protocol fields. Structural awareness is addressed through a range of modeling approaches:

Standard Positional Embedding: It adds fixed or learned vectors to input tokens to provide the model with information about token order. This approach is a common NLP technique adapted in traffic models like ET-BERT [3], PERT [2], Net-GPT [15], and NetFound [12].

Special Time and Semantic Tokens: uses special tokens like [start] and [time] to represent packet boundaries and time intervals, encoding temporal and structural semantics in inputs. Lens [4] also uses special tokens like [pkt] to mark packet boundaries and [head] to separate header fields from payloads. PEAN [6] uses a [PACKET] token to aggregate byte-level information into a packet-level representation. ET-BERT [3] differentiates sub-bursts using a [SEP] special token and segment embeddings. TrafficLLM [7] uses [packet] as an indicator token to signify the beginning of traffic data. MLETC [13] tokenizes traffic at byte, field, and packet levels using structural markers like [PKT] and [HDR] to denote boundaries, and employs header embeddings to distinguish protocol fields, enabling semantic understanding across protocol layers. NetGPT [15] appends [pck] to each packet as a segment delimiter. TrafficGPT [8] introduces Time Interval Tokens that encode inter-packet delays in exponential format, enriching temporal structure awareness.

![](images/67e0a1fe3e86dcc54c1619b5f1301f4bb6e83401c2cbd6b8066773d4d3daa449.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
    A["Raw Input"] --> B["Traffic Representations"]
    B --> C["Input Embeddings"]
    C --> D["Transformer-based Foundation Model"]
    D --> E["Trainable Heads"]
    E --> F["Downstream Task"]

    subgraph Raw Input
        G["01101100 01101111 011101010 01100101"]
        H["01101100 01101111 011101010 01100101"]
        I["..."]
    end

    subgraph Traffic Representations
        J["{&quot;flow_duration&quot;, &quot;burst_tokens&quot;, &quot;directions&quot;, &quot;bytes&quot;, &quot;iats&quot;, &quot;counts&quot;, &quot;protocol&quot;, 'label&quot;}<br>        K[&quot;Instruction&quot;: &quot;Please generate updates, upload attack traffic.&quot;, &quot;output&quot;: &quot;packet><p>ip.src...&quot;"]
        L["..."]
    end

    subgraph Input Embeddings
        M["Patch and Positional Embeddings (YaTC)"]
        N["Flow metadata, Positional and Packet Embeddings (NetFound)"]
        O["Text and Packet Embeddings (TrafficLLM)"]
        P["..."]
    end

    subgraph Transformer-based Foundation Model
        Q["YaTC"]
        R["NetFoun"]
        S["TrafficLLM"]
        T["..."]
    end

    subgraph Trainable Heads
        U["Classifier Head"]
        V["Regression Head"]
        W["Prefix Encoder"]
        X["..."]
    end

    subgraph Downstream Task
        Y["Classification"]
        Z["Prediction"]
        AA["Generation"]
        AB["..."]
    end
```
</details>

Fig. 3: Fine-tuning workflow for various network traffic analysis tasks.

Hierarchical Embeddings: Beyond simple token order, several models explicitly capture the inherent hierarchical structure of network traffic. For example, YaTC [1] captures multi-level structure by encoding traffic into a matrix with dedicated regions for byte-, packet-, and flow-level features. Moreover, Flow-MAE [5] captures structural awareness by processing traffic bursts as one-dimensional sequences that preserve packet structure.

Graph Embeddings: PACKETCLIP [9] incorporates knowledge graph structures generated from natural language inputs to capture domain-specific semantics across flows and packets, enabling GNN-based processing alongside Transformer embeddings.

# PRE-TRAINING STRATEGIES

Pre-training is crucial for building generalizable and scalable traffic models. Inspired by SSL in NLP and CV, foundation models adopt diverse pre-training strategies, Fig. 2

Masked Language Modeling: Inspired by BERT, this strategy hides parts of the input and trains the model to predict them, enabling learning of contextual and semantic representations. Variants of this approach are used in PERT [2], ET-BERT [3], MLETC [13], PEAN [6] and NetFound [12].

Masked Image Modeling: Inspired by MAE, this strategy masks portions of image-like traffic inputs and reconstructs them to learn spatial and structural patterns. YaTC [1] and Flow-MAE [5] follow this approach.

Contrastive Learning: This approach trains the model to align matching representations from different modalities in a shared embedding space. PACKETCLIP [9] applies this to link packet-level features with their descriptions.

Same-Origin Prediction: This strategy trains the model to determine whether different traffic segments belong to the same flow, capturing flow-level dependencies. ET-BERT [3] and MLETC [13] apply variants of this strategy.

Packet Order Prediction: Introduced by Lens [4], this strategy trains the model to reorder shuffled packets within a flow, reinforcing temporal coherence.

Generative Pre-training: This strategy models traffic as a sequence of tokens and trains the model to generate the next token, learning sequential and generative patterns. Net-GPT [15], TrafficLLM [7] and TrafficGPT [8] apply this approach.

These pre-training strategies equip models with a deep understanding of traffic structure and semantics. Fine-tuning then adapts these models to downstream tasks

# FINE-TUNING ON DOWNSTREAM TASKS

Various foundation models can support downstream tasks, Fig. 3. These tasks can be categorized into the following three general groups:

Traffic Classification: This remains the most widely supported downstream task. This includes tasks such as Encrypted Application and Service Classification, Malicious Traffic and Intrusion Detection, Attack Type Classification and VPN Detection. Models like NetFound [12], Flow-MAE [5], ET-BERT [3], MLETC [13], PERT [2], and PACKETCLIP [9] have been specifically fine-tuned for traffic classification tasks.

Traffic Generation: This emerging task focuses on synthesizing realistic network traffic at different levels, including header field generation (e.g., IP addresses, ports), full packet synthesis, and protocol-specific traffic. Models such as Lens [4], NetGPT [15], TrafficGPT [8], and TrafficLLM [7] support these capabilities. Traffic Generation task is useful in security testing, network simulation, traffic data augmentation (especially when data is sparse or imbalanced), and network digital twins.

Traffic Characteristic Prediction: Although none of the reviewed models were explicitly fine-tuned for prediction tasks, models such as NetFound [12] exhibit the potential to be adapted for predicting traffic characteristics. These include parameters like packet length, inter-arrival time, traffic volume, and throughput. Traffic characteristic prediction tasks are useful in network management and cybersecurity applications.

# DATASETS

Datasets for traffic analysis differ in realism, application/protocol coverage, and release format. For pre-training traffic foundation models, datasets with real, raw PCAP traces are particularly valuable because they preserve packet- and flow-level structure and reflect real traffic dynamics. For finetuning, labeled PCAP-based datasets are preferred because they provide task-specific ground truth for supervised adaptation. Dataset selection is also commonly guided by FAIR principles (Findable, Accessible, Interoperable, Reusable), favoring datasets that are publicly available and well-documented, while also accounting for privacy constraints through appropriate prepossessing (e.g., anonymizing IP addresses).

# USE CASES: GENERALIZABILITY AND FINE-TUNING FOR DOWNSTREAM TASKS

To assess generalization, we fine-tuned three Transformerbased network foundation models on two previously unseen datasets and evaluated them on three key downstream tasks, demonstrating their generalizability to unfamiliar network environments.

We use two public datasets: $C I C I o T 2 0 2 3 ^ { 1 }$ , which provides raw PCAP traces of IoT benign traffic and a broad set of IoTfocused attacks, and $C I C - I D S - 2 { \cal O } I 7 ^ { 2 }$ , which captures five days of benign and attack traffic from a simulated testbed and is released as raw PCAPs and bidirectional flow records.

# GENERALIZATION ACROSS TRAFFIC CLASSIFICATION TASKS

To demonstrate the generalization capabilities of Transformer-based foundation models in traffic classification scenarios for IoT network security applications, we fine-tuned YaTC, as shown in Fig. 3, on CICIoT2023 dataset. While the full dataset includes a broader range of IoT-related attacks, we selected 16 attacks and benign traffic. As CICIoT2023 dataset provides raw PCAP files, we first segmented the traffic into flows and then extracted the packet bytes to construct grayscale images. These images were used for fine-tuning YaTC with a classifier head (a multi-layer perceptron (MLP) with three hidden layers and a softmax output layer). The fine-tuned YaTC encoder with classifier head achieved an overall classification accuracy of 96.9%. The classifier head by itself achieved an overall accuracy of 72.5%. The model demonstrated consistent performance across all attack types, with per-class F1-scores exceeding 0.93 for most categories. Detailed performance metrics per class are summarized in Table I for both YaTC with classifier head and the MLPonly baseline, and clearly shows the superiority of using a Transformer-based foundation model to capture richer traffic structure and semantics for IoT attack classification.

# GENERALIZATION ACROSS TRAFFIC CHARACTERISTIC PREDICTION TASKS

To evaluate the ability of traffic foundation models to perform traffic volume prediction, we fine-tuned NetFound, as shown in Fig. 3, on the benign subset of CIC-IDS-2017 dataset. Each flow was extracted from raw PCAP files, tokenized into burst-level payloads, headers, and metadata (packet size, inter-arrival time, direction, etc.), and labeled with its total transmitted volume in bytes, forming the dataset. The dataset was used for fine-tuning NetFound with a regression head (MLP with three hidden layers and LeakyReLU activations). The fine-tuned model demonstrated strong predictive performance, achieving a low Mean Absolute Percentage Error (0.082%), high $R ^ { 2 }$ score (0.934), and low Mean Absolute Error (MAE) of 18 bytes. On the other hand, the baseline MLP achieved an MAE of 21.63 bytes and an $R ^ { 2 }$ of 0.840. These results highlight the model’s ability to generalize to network traffic characteristic prediction tasks.

TABLE I: Classification performance of fine-tuned YaTC with classifier head vs. classifier head only. 

<table><tr><td rowspan="2">Attack Class</td><td colspan="3">YaTC+MLP</td><td colspan="3">MLP</td></tr><tr><td>Precision</td><td>Recall</td><td>F1</td><td>Precision</td><td>Recall</td><td>F1</td></tr><tr><td>Benign</td><td>0.9950</td><td>0.9910</td><td>0.9930</td><td>0.4802</td><td>0.7870</td><td>0.5965</td></tr><tr><td>DDoS HTTP Flood</td><td>0.9885</td><td>0.9845</td><td>0.9865</td><td>0.9145</td><td>0.7965</td><td>0.8514</td></tr><tr><td>ACK Fragmentation</td><td>0.9900</td><td>0.9905</td><td>0.9903</td><td>0.9950</td><td>0.9920</td><td>0.9935</td></tr><tr><td>Vulnerability Scan</td><td>0.9786</td><td>0.9850</td><td>0.9818</td><td>0.3423</td><td>0.3900</td><td>0.3646</td></tr><tr><td>SQL Injection</td><td>0.9612</td><td>0.9041</td><td>0.9318</td><td>0.5440</td><td>0.1001</td><td>0.1691</td></tr><tr><td>Port Scan</td><td>0.9806</td><td>0.9840</td><td>0.9823</td><td>0.5147</td><td>0.3675</td><td>0.4288</td></tr><tr><td>OS Scan</td><td>0.9819</td><td>0.9745</td><td>0.9782</td><td>0.4196</td><td>0.0470</td><td>0.0845</td></tr><tr><td>Host Discovery</td><td>0.9940</td><td>0.9925</td><td>0.9932</td><td>0.6545</td><td>0.6840</td><td>0.6689</td></tr><tr><td>Mirai UDP Flood</td><td>0.8632</td><td>0.8873</td><td>0.8751</td><td>0.9990</td><td>0.9930</td><td>0.9960</td></tr><tr><td>Mirai-greeth Flood</td><td>0.8689</td><td>0.8167</td><td>0.8420</td><td>0.9949</td><td>0.9820</td><td>0.9884</td></tr><tr><td>Mirai-greip Flood</td><td>0.9539</td><td>0.9673</td><td>0.9606</td><td>0.9856</td><td>0.9955</td><td>0.9905</td></tr><tr><td>MITM-ARP Spoofing</td><td>0.9705</td><td>0.9855</td><td>0.9779</td><td>0.6557</td><td>0.6705</td><td>0.6630</td></tr><tr><td>DNS Spoofing</td><td>0.9790</td><td>0.9785</td><td>0.9787</td><td>0.6840</td><td>0.6765</td><td>0.6802</td></tr><tr><td>Dictionary-BruteForce</td><td>0.9145</td><td>0.9408</td><td>0.9274</td><td>0.5245</td><td>0.5935</td><td>0.5569</td></tr><tr><td>DDoS-UDP Fragmentation</td><td>0.9472</td><td>0.9442</td><td>0.9457</td><td>0.9930</td><td>0.9885</td><td>0.9907</td></tr><tr><td>DDoS-Slowloris</td><td>0.9875</td><td>0.9905</td><td>0.9890</td><td>0.9552</td><td>0.9810</td><td>0.9679</td></tr><tr><td>DoS HTTP Flood</td><td>0.9890</td><td>0.9920</td><td>0.9905</td><td>0.8261</td><td>0.9215</td><td>0.8712</td></tr><tr><td>Average</td><td>0.9614</td><td>0.9593</td><td>0.9602</td><td>0.7343</td><td>0.7039</td><td>0.6978</td></tr></table>

![](images/7eae4949ed73913f84cfe782fb89698d32ff2c70842535713b0ad9c5ec3ad87b.jpg)

<details>
<summary>line</summary>

| TTL Value | Real TTL | Synthetic TTL |
| --------- | -------- | ------------- |
| 0         | 0.0      | 0.0           |
| 50        | 0.6      | 0.6           |
| 100       | 0.7      | 0.6           |
| 150       | 0.8      | 0.7           |
| 200       | 0.9      | 0.8           |
| 250       | 1.0      | 0.9           |
</details>

![](images/d527bcdac207ab29498cd9a42783a54aef042f9fef2c77f50d640803b16ee465.jpg)

<details>
<summary>line</summary>

| Packet Length (bytes) | Real Packet Length | Synthetic Packet Length |
| --------------------- | ------------------ | ----------------------- |
| 0                     | 0.0                | 0.0                     |
| 200                   | 0.8                | 0.8                     |
| 400                   | 0.9                | 0.9                     |
| 600                   | 0.95               | 0.95                    |
| 800                   | 0.98               | 0.98                    |
| 1000                  | 0.99               | 0.99                    |
| 1200                  | 0.995              | 0.995                   |
| 1400                  | 1.0                | 1.0                     |
| 1600                  | 1.0                | 1.0                     |
</details>

Fig. 4: CDF of TTL and packet length for real vs. TrafficLLMgenerated packets.

# GENERALIZATION ACROSS TRAFFIC GENERATION TASKS

To assess the capability of traffic foundation models in generation tasks, especially when training data is sparse or imbalanced, we fine-tuned TrafficLLM on a PCAP trace of Uploading Attack flows from the CICIoT2023 dataset. This attack involves unauthorized file uploads and is underrepresented in the dataset, making it a suitable candidate for synthetic augmentation. We used tshark to extract packet-level summaries, which were reformatted into instruction–output pairs as shown in Fig. 3. Using P-Tuning $\mathbf { v } 2 ,$ we fine-tuned a prefix encoder on top of a frozen ChatGLM2-6B model to autoregressively generate packet-level outputs conditioned on prompts. We then compared the distributions of two packet fields—Time-To-Live (TTL) and IP packet length—between real and generated traffic using Cumulative Distribution Functions (CDFs), as shown in Fig. 4. The close alignment in both plots indicates that the fine-tuned model effectively replicates key packet fields of real network traffic.

# FUTURE RESEARCH DIRECTIONS FOR TRAFFIC FOUNDATION MODELS

While Transformer-based foundation models have shown promise for network traffic analysis, several open research directions remain to realize their full potential.

# COMPUTATIONAL COMPLEXITY AND REAL-TIME CONSTRAINTS

Transformer architectures have a quadratic time and memory complexity with respect to input sequence length, $O ( n ^ { 2 } )$ . This becomes challenging when longer packet flows/bursts are processed. Future work can mitigate this overhead by adopting more efficient attention mechanisms (e.g., sparse or low-rank approximations). In addition, techniques such as knowledge distillation, parameter pruning, and model quantization can be applied to deploy these models on less efficient hardware.

# LATENCY-PERFORMANCE TRADE-OFFS

In practice, network monitoring systems require sub-second inference. Future work should benchmark not just accuracy but the end-to-end inference latency on the target hardware. Speculative inference, computation offloading, and hierarchical processing pipelines can achieve a better accuracy/latency trade-off.

# EXPLAINABILITY AND TRUST

To gain operational trust, more explainable traffic foundation models are required. Explainable AI and LLM models can be applied to provide human-readable explanations in realtime from the Transformer attention weights and structural embeddings provided by the traffic foundation model. These can attribute the model predictions to specific traffic components (e.g., header fields, temporal bursts). This is especially critical for security-sensitive applications.

# REASONING-ENHANCED TRAFFIC ANALYSIS

Future traffic foundation models may support lightweight evidence-based reasoning over packet/flow structure and time, and provide short human-readable justifications, improving robustness under distribution shifts, partial data, and attacks.

# CONCLUSION

In this paper, we introduced the pre-training and finetuning pipeline for Transformer-based traffic foundation models, which can generalize to various categories of downstream tasks. Inspired by advances in NLP, these models treat traffic as a learnable language and leverage self-supervised pretraining to build generalizable representations. We explored various Transformer foundation models for traffic classification, flow characteristic prediction and traffic generation tasks. We categorized the existing models based on their Transformer architecture (e.g., encoder-only, decoder-only, encoder–decoder), input modalities (e.g., packets, flows, images, text), and pre-training strategies (e.g., masked modeling, contrastive learning). Our experimental results further demonstrate the ability of Transformer foundation models to generalize across these tasks. We also compare against non-foundation baselines demonstrating that the foundation-model backbones achieve improved performance. These findings highlight the potential of foundation models for robust, scalable, and dataefficient traffic analysis.

# REFERENCES

[1] R. Zhao et al., “A Novel Self-Supervised Framework Based on Masked Autoencoder for Traffic Classification,” IEEE/ACM Transactions on Networking, vol. 32, no. 3, pp. 2012–2025, 2024.   
[2] H. Y. He et al., “PERT: Payload Encoding Representation from Transformer for Encrypted Traffic Classification,” in 2020 ITU Kaleidoscope: Industry-Driven Digital Transformation (ITU K), 2020, pp. 1–8.   
[3] X. Lin et al., “ET-BERT: A Contextualized Datagram Representation with Pre-training Transformers for Encrypted Traffic Classification,” in Proceedings of the ACM Web Conference 2022, 2022, p. 633–642.   
[4] Q. Wang et al., “Lens: A foundation model for network traffic,” arXiv preprint arXiv:2402.03646, 2024.   
[5] Z. Hang et al., “Flow-MAE: Leveraging Masked AutoEncoder for Accurate, Efficient and Robust Malicious Traffic Classification,” in Proceedings of the 26th International Symposium on Research in Attacks, Intrusions and Defenses, 2023, p. 297–314.   
[6] P. Lin et al., “A Novel Multimodal Deep Learning Framework for Encrypted Traffic Classification,” IEEE/ACM Transactions on Networking, vol. 31, no. 3, pp. 1369–1384, 2023.   
[7] T. Cui et al., “TrafficLLM: Enhancing Large Language Models for Network Traffic Analysis with Generic Traffic Representation,” arXiv preprint arXiv:2504.04222, 2025.   
[8] J. Qu et al., “TrafficGPT: Breaking the token barrier for efficient long traffic analysis and generation,” arXiv preprint arXiv:2403.05822, 2024.   
[9] R. Masukawa et al., “PACKETCLIP: Multi-Modal Embedding of Network Traffic and Language for Cybersecurity Reasoning,” arXiv preprint arXiv:2503.03747, 2025.   
[10] A. Vaswani et al., “Attention is all you need,” in Advances in Neural Information Processing Systems, I. Guyon et al., Eds., vol. 30. Curran Associates, Inc., 2017.   
[11] J. Devlin et al., “BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding,” in Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, J. Burstein et al., Eds., Jun. 2019, pp. 4171–4186.   
[12] S. Guthula et al., “netFound: Foundation model for network security,” arXiv preprint arXiv:2310.17025, 2023.   
[13] J.-T. Park et al., “Multi-Level Pre-Training for Encrypted Network Traffic Classification,” IEEE Access, vol. 13, pp. 68 643–68 659, 2025.   
[14] C. Raffel et al., “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer,” Journal of Machine Learning Research, vol. 21, no. 140, pp. 1–67, 2020.   
[15] X. Meng et al., “NetGPT: Generative pretrained transformer for network traffic,” arXiv preprint arXiv:2304.09513, 2023.

# BIOGRAPHIES

Samara Mayhoub is a Lecturer in Cyber Security at Aston University. She held two postdoc positions: University of Surrey (6GIC, 2024) and Queen’s University Belfast (CSIT, 2025). She received her Ph.D. in Network Security from Samara National Research University in 2022.

Chuan Heng Foh (Senior Member, IEEE) is an Associate Professor in the 6G Innovation Centre at UoS, the Vice Chair of the IEEE VTS Ad Hoc Committee on Mission Critical Communications. He is on the editorial boards of several international journals and a Senior Editor of IEEE ACCESS.

Mahdi Boloursaz Mashhadi (Senior Member, IEEE) is a Lecturer at the 6G Innovation Centre, UoS, and a Surrey AI fellow. His research is focused at the intersection of AI/ML with wireless communications. He is a PI/Co-PI for various government and industry-funded projects including the UKTIN/DSIT 12M£ national project TUDOR.

Mohammad Shojafar (Senior Member, IEEE) is an Associate Professor in the 6G Innovation Centre at UoS, Marie Curie Alumni, an Intel Innovator and Surrey Sustainability Fellow. He has secured more than £2M in research funding as a PI for various EU- and UK-funded projects. He is also a member of the ETSI Intelligent Transportation Systems Group, GSMA Open-Telco LLM Group, and the 3GPP 5G SSA working group.

Rahim Tafazolli (Fellow, IEEE) is a Regius Professor of Electronic Engineering, a Professor of Mobile and Satellite Communications, and the Founder and the Director of 5GIC, 6GIC, and the Institute for Communication Systems, UoS. He has more than 30 years of experience in digital communications research and teaching.
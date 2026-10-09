# AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models

Peishuai Sun Institute of Information Engineering, Chinese Academy of Sciences School of Cyber Security, University of Chinese Academy of Sciences Beijing, China sunpeishuai@iie.ac.cn

Tao Yin Zhongguancun Laboratory Beijing, China yintao@zgclab.edu.cn

Xiaochun Yun<sup>∗</sup> Zhongguancun Laboratory Beijing, China yunxiaochun@zgclab.edu.cn

Chengxiang Si National Computer Network Emergency Response Technical Team/Coordination Center of China Beijing, China sichengxiang@cert.org.cn

Shuhao Li<sup>†</sup> Zhongguancun Laboratory Beijing, China lishuhao@zgclab.edu.cn

Jiang Xie Zhongguancun Laboratory Beijing, China xiejiang@zgclab.edu.cn

## Abstract

Deep learning-based (DL-based) malicious trafic detection models are efective but vulnerable to adversarial attacks. Existing adver sarial attacks have shown promising results when targeting trafic detection models based on statistics and sequence features. However, these attacks are less efective against models that rely on payload analysis. The main reason is the dificulty in generating semantic, compliant, and functional payloads, which limits their practical application.

In this paper, we propose AdvTG, an adversarial trafic generation framework to deceive DL-based malicious trafic based on the large language model (LLM) and reinforcement learning (RL). Specifically, AdvTG is designed to attack various DL-based detection models across diverse payload features and architectures, thereby enhancing the generalization capabilities of the generated adversarial trafic. Moreover, we design a specialized prompt for trafic generation tasks, where functional fields and target types are supplied as input, while non-functional fields are generated to produce the mutated trafic. This fine-tuning endows the LLM with task comprehension and trafic pattern reasoning abilities, al lowing it to generate trafic that remains compliant and functional. Furthermore, leveraging RL, AdvTG automatically selects trafic fields that exhibit more robust adversarial properties. Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

## CCS Concepts

• Security and privacy → Artificial immune systems.

## Keywords

Malicious Trafic Detection, Adversarial Attacks, Large Language Model, Reinforcement Learning

Peishuai Sun, Xiaochun Yun, Shuhao Li, Tao Yin, Chengxiang Si, and Jiang Xie. 2025. AdvTG: An Adversarial Trafic Generation Framework to Deceive DL-Based Malicious Trafic Detection Models. In Proceedings ofthe ACMWeb Conference 2025 (WWW’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 13 pages. https://doi.org/10.1145/3696410.3714876

## 1 Introduction

Malicious trafic detection is an essential approach for detecting malicious activities in networks. Traditional methods extract the key fields of malicious trafic as signature rules [14, 19, 43]. However, as attack tactics continue to evolve, signature-based detection methods are less efective at detecting unknown or mutated malicious trafic. With the development of artificial intelligence, deep learning (DL) has seen widespread adoption in cybersecurity. Most methods train DL-based models with large amounts of trafic to detect trafic automatically [21, 63, 68]. At present, DL-based malicious trafic detection has become a familiar and efective technique in both academic and industrial settings [34, 45].

Unfortunately, DL-based models are vulnerable to adversarial attacks [13, 28, 50, 58, 65]. In network security, adversarial samples have even more severe consequences [2]. Trafic features can be modified to specifically target detection models, causing the models to produce incorrect classification results. Recently, numerous adversarial methods have been developed to exploit vulnerabilities in DL-based trafic detection systems and reveal their weaknesses.

<sup>∗</sup>Both authors contributed equally to this research. <sup>†</sup>Corresponding author. lishuhao@zgclab.edu.cn

Existing adversarial attacks in the trafic domain can be categorized into three types. Statistical feature attacks [18, 35, 53] modify statistical features (e.g., flow duration and average packet size) but cannot be easily mapped back to actual trafic. Sequence feature attacks [23, 32, 41, 52, 54] alter temporal and spatial sequence features (e.g., packet intervals, packet lengths) but payload-based detection models remain efective. Content attacks [11, 37, 55, 64] directly modify trafic packets to evade detection. The first two types of attacks have already achieved considerable success in ad versarial trafic attacks; however, they fail to deceive models which detect based on payload. Compared to these attacks, content attacks pose more significant challenges, but they are also more disruptive. By modifying the payload, these attacks can deceive payload-based detection models [57, 60], allowing malicious activities to go unnoticed. In this study, we focus solely on content attacks, specifically targeting DL-based detection models that rely on payload analysis, and exclude the first two types of attacks from consideration.

Existing adversarial attacks on DL-based trafic detection are limited to specific scenarios and rely on impractical assumptions. Table 1 provides a comparative overview of these adversarial attack methods within the trafic detection domain. The key challenges can be summarized into three categories.

• Generality. Trafic features should be mapped to real-world trafic spaces rather than generating non-existent features. Adversarial attacks should demonstrate generalization, being able to succeed across various extracted features and model architectures.

• Availability. The generated trafic must adhere to strict protocol compliance while maintaining its functionality. Functional fields are those that play a critical role in the execution and routing of trafic packets. These fields directly influence how the server processes the request or how the client inter acts with the server. For example, the request line and the payload that executes malicious commands in HTTP trafic are considered functional fields.

• Payload Generation. This challenge is specific to content attacks. The generated adversarial trafic should consist of complete packets, and remain semantic trafic.

Benefiting from advancements in large language models (LLMs), which significantly enhance both semantic understanding and text generation capabilities. Therefore, we are able to focus on trafic content attacks aimed at generating mutated trafic, which can deceive existing content-based detection models.

In this paper, we propose AdvTG, an adversarial trafic generation framework designed to deceive DL-based detection models. The framework consists of three key stages.

First, we train multiple DL-based models using both image-based and text-based features extracted from payload. These models serve as targets for our adversarial attacks. Simultaneously, these models serve as reward models during the adversarial generation process, providing feedback on how efectively the generated trafic deceives detection. Using diverse features and model architectures improves AdvTG’s ability to generate adversarial trafic with improved gen eralization.

Next, we fine-tune the LLM with a trafic-specific prompt format. Instructions define the trafic categories, and functional fields are provided as input while the LLM generates non-functional fields to create a complete payload. The fine-tuning approach ensures the generated trafic is compliant, functional, and semantically rich.

Finally, reinforcement learning (RL) is applied to optimize the adversarial trafic generation process. The detection models provide feedback on whether each generated trafic sample efectively deceives detection, enabling the LLM to refine and enhance its out puts based on feedback continually. This adaptive process enables the LLM to optimize adversarial non-functional fields, making the generated trafic harder for detection models to detect.

• We propose AdvTG<sup>1</sup>, an adversarial trafic generation framework based on the LLM and RL to deceive DL-based malicious trafic models.

• We introduce a tailored fine-tuning process for the LLM to enhance its understanding of trafic generation tasks, enabling it to generate semantic trafic. Using prompts that specify the expected trafic type and functional fields, the LLM generates trafic by altering non-functional fields while preserving functionality and protocol compliance.

• AdvTG leverages RL to optimize adversarial trafic generation by continuously generating mutated trafic based on feedback from detection models. This adaptive process enables the LLM to improve its outputs iteratively, identifying the optimal adversarial non-functional fields and making the generated trafic increasingly dificult for detection models to identify.

• Experimental results show that AdvTG achieves over 40% attack success rate (ASR) across six detection models on four base datasets and two extended datasets, significantly outperforming other adversarial attack methods.

## 2 Background and Motivation

## 2.1 Scenarios

We clarify our scenarios by answering the following key questions. A. Why are we targeting content adversarial attacks?

Existing adversarial trafic attack methods work by altering the direction of packets or employing techniques such as truncation and padding. These approaches have demonstrated vulnerabilities in many feature-based trafic detection models. However, such changes are easily detected by models that analyze deeper features, such as the payload. Our goal is to generate adversarial mutated trafic, aiming to evaluate the robustness ofpayload-based detection models. Trafic data is structured and frequently contains redundant information; however, upper-layer protocols typically carry more meaningful data compared to lower-layer protocols like IP and TCP. Therefore, we focus content attacks on application-layer protocols.

## B. Why are we focusing on HTTP protocol?

HTTP/HTTPS protocols have long been primary communication protocols on the internet and are key vectors for malicious activities. Many attacks, such as web exploitation, vulnerability exploitation, and C&C communications, are carried out via these protocols. We focus on adversarial attacks on plaintext trafic, excluding encrypted trafic. The main reason is that encrypted data is transformed into unpredictable ciphertext, and any modification can corrupt the data, leading to incorrect plaintext upon decryption. However, plaintext trafic detection can extend to encrypted trafic, as defenders can use decryption techniques for efective monitoring. Security tools like Endpoint Detection and Response (EDR), Web Application Firewalls (WAF), and Internet Information Services (IIS) rely on plaintext analysis to enhance security.

Table 1: The comparison with the existing methods of adversarial attacks in trafic.

<table><tr><td rowspan="2">Attack Types</td><td rowspan="2">Target Models</td><td rowspan="2">Attack Methods</td><td colspan="3">Generality</td><td colspan="2">Availability</td><td colspan="2">Payload-generation</td></tr><tr><td>Mappable Data</td><td>Black-Box Models</td><td>Various Features</td><td>Protocol Compliance</td><td>Remaining Functionality</td><td>Complete Packet</td><td>Semantic Content</td></tr><tr><td rowspan="5">Statistical Feature Attacks</td><td rowspan="2">ML &amp; DL</td><td>IDSGAN [35]</td><td>×</td><td>×</td><td>×</td><td>×</td><td>×</td><td>-</td><td>-</td></tr><tr><td>DIGFuPas [18]</td><td>×</td><td>×</td><td>×</td><td>×</td><td>√</td><td>-</td><td>-</td></tr><tr><td rowspan="3">Multi-Source</td><td>Bars[53]</td><td>×</td><td>√</td><td>×</td><td>×</td><td>√</td><td>-</td><td>-</td></tr><tr><td>Multiple Methods [30]</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td><td>-</td><td>-</td></tr><tr><td>Flow Statistics [39]</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>-</td><td>-</td></tr><tr><td rowspan="5">Sequence Feature Attacks</td><td rowspan="3">ML &amp; DL</td><td>Prism [32]</td><td>√</td><td>×</td><td>√</td><td>√</td><td>√</td><td>-</td><td>-</td></tr><tr><td>RL [52]</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>-</td><td>-</td></tr><tr><td>ProGen [54]</td><td>√</td><td>×</td><td>√</td><td>√</td><td>√</td><td>-</td><td>-</td></tr><tr><td rowspan="2">Multi-Source</td><td>Blanket [41]</td><td>√</td><td>×</td><td>×</td><td>×</td><td>√</td><td>-</td><td>-</td></tr><tr><td>GA+GAN [23]</td><td>√</td><td>√</td><td>×</td><td>×</td><td>√</td><td>-</td><td>-</td></tr><tr><td rowspan="5">Content Attacks</td><td rowspan="2">ML &amp; DL</td><td>Attack-GAN [11]</td><td>×</td><td>√</td><td>×</td><td>×</td><td>×</td><td>√</td><td>×</td></tr><tr><td>GA [64]</td><td>√</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td rowspan="3">Multi-Source</td><td>Text Attack [37]</td><td>√</td><td>√</td><td>×</td><td>×</td><td>√</td><td>×</td><td>×</td></tr><tr><td>Fuzzy Attack [55]</td><td>√</td><td>√</td><td>×</td><td>√</td><td>√</td><td>×</td><td>√</td></tr><tr><td>AdvTG</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td><td>√</td></tr></table>

## C. Where to add perturbations to achieve attacks?

HTTP trafic has a strict header specification with many fields, as shown in Fig. 1. Both benign and malicious trafic exhibit certain regularities in the header fields they utilize, with noticeable differences between the two. These fields are commonly used as key features in malicious trafic detection. We can categorize the packet into functional and non-functional fields based on their necessity, with their diferences detailed in an example in § A. In brief, func tional fields cannot be altered, whereas non-functional fields can be modified. By targeting the non-functional fields, we can attack the detection model without compromising the compliance and functionality of the HTTP trafic.

![](images/04e53c1d0868b987e4673829e4ccfbad77510fe5bb573cfe63dedd74019d6d20.jpg)  
Figure 1: Comparison of header fields between benign trafic and malicious trafic.

## 2.2 THREAT MODEL

We define threat model based on previous work [5].

![](images/ebc8eff58881d0e5c54259e778555524194ca92034cd246d8e06b3b0384f1bf4.jpg)  
Figure 2: The scenarios of adversarial attacks.

Attacker’s Goal. The attacker seeks to generate adversarial trafic to deceive DL-based detection models, leading to misclassification, as shown in Fig. 2. The attacker produces complete payloads while ensuring they remain protocol-compliant and functional.

Attacker’s Knowledge. The attacker has no prior knowledge of the detection model architecture or the extracted features. Instead, the attacker inputs the generated trafic into a black-box detection, which extracts features and outputs classification results. These results serve as a reward signal, enabling the attacker to generate more challenging adversarial trafic based on RL automatically.

Attacker’s Capability. The attacker can only modify the test datas and cannot alter the training data, thus preventing data poisoning attacks [6]. The attacker leverages the advanced LLM to generate adversarial trafic that remains both semantic and functional.

## 3 Overview

In this section, we propose AdvTG, targeting DL-based malicious trafic detection models. Fig. 3 shows three phases of AdvTG. (i) We train multiple DL-based malicious trafic detections with diferent trafic features and model architectures using supervised learning. (ii) The domain-specific LLM is fine-tuned using large amounts of HTTP trafic based on self-supervised learning. (iii) The domainspecific LLM is further fine-tuned to carry out adversarial attacks using RL based on the feedback from the malicious trafic detection in the first stage.

![](images/7ba0aca3dbf54150761a6dc8eba929c6251d1c978be667d825001eeebf2d47a9.jpg)  
Figure 3: The overview of AdvTG.

Detection Model Training. We train multiple malicious trafic detection models as adversarial attack targets. These models are trained on small datasets and demonstrate a certain level of gener alization in detecting malicious HTTP trafic. The detection mod els utilize both image-based and text-based features, incorporating a range of standard DL-based architectures alongside prominent models from the academic field of malicious trafic detection [15, 17, 31, 38, 57, 70].

The trained models are used as reward models for adversarial generation through RL. Specifically, these classification models evaluate the quality of the trafic generated by the LLM. Trafic that successfully deceives the detection model receives a higher score, while easily detected trafic is given a lower score.

Domain-Specific LLMs Fine-tuning. We fine-tune the general purpose LLM using a large set of domain-specific data. This process helps the model learn HTTP trafic patterns and formats, improving its ability to generate and understand data within this domain while also enhancing its distinction between benign and malicious trafic.

We propose a trafic-specific prompt format where instructions define the trafic categories. Functional fields are given as input, while non-functional fields are generated to form a complete trafic packet.

RL-based Adversarial Generation. Reinforcement learning is employed to optimize the adversarial attack generation strategy. The reward model, trained in the first phase, evaluates the outputs of the LLM, and these scores are used to update the LLM’s parameters.

In practice, a batch of prompts is randomly sampled, and the fine-tuned LLM generates trafic packets. The generated trafic is then input into the detection model to receive feedback, where the reward model assigns a reward representing the overall quality of the generated payload. Once the final reward for the word sequence is obtained, it is propagated backwards through the sequence, treating each word as a time step. The objective is to train the LLM to produce high-reward outputs that align with the reward model and represent high-quality responses.

## 4 Detection Model Training

According to the threat model, we train multiple detection models with probabilistic outputs through supervised training. We design multiple feature extractors and models to verify the generalization of adversarial attacks to diferent feature models. The feature extractor converts the trafic into a continuous or discrete numerical sequence that can be input into the model. At present, in the field of deep learning, detection models for trafic payload mainly include two types. One is transforming trafic into images, where the byte stream data of the trafic is converted into a two-dimensional grayscale image. This representation is then classified using deep learning models [38, 57]. The other approach treats trafic as textual data, converting trafic into vector representations using word embedding techniques [27, 56].

## 4.1 Image-based Features

Converting network trafic into images enables the capture of spa tial and local patterns within the data. By representing each byte as a pixel, this method leverages image analysis techniques, such as CNN, to enhance detection accuracy. Eq. 1 and Eq. 2 outline the process of transforming network trafic � into an image. The trafic is first divided into individual bytes and normalized to a continuous sequence $T ^ { \prime }$ between 0 and 1. This sequence is then reshaped into a 2D image of size � × �. If the trafic exceeds the predefined image size, the excess data is truncated; otherwise, padding with zeros is applied to match the required dimensions.

$$
T ^ {\prime} = \frac {T}{2 5 5}, \quad T = [ b _ {1}, b _ {2}, \ldots , b _ {n} ], b _ {i} \in [ 0, 2 5 5 ]\tag{1}
$$

$$
I (i, j) = T _ {(i - 1) \times n + j} ^ {\prime} (i \in [ 1, m ], j \in [ 1, n ])\tag{2}
$$

The extracted features are input into a DL-based model, which outputs classification probability scores. In this work, we utilize various DL-based model architectures, including the classic CNN and other commonly used models in the field of image processing.

## 4.2 Text-based Features

Transforming trafic into text highlights its semantic payload and sequential patterns, aiding detection through semantic analysis. In $\operatorname { E q . }$ 3,� denotes the trafic data, which is tokenized into $\left( w _ { 1 } , w _ { 2 } , . . . , w _ { n } \right)$ Each token ���������(� )<sub>�</sub> is mapped to an index $t _ { k }$ via a vocabu lary function $V ,$ assigning a unique identifier to preprocess the data for input into a DL-based model.

$$
t _ {k} = V (t o k e n i z e r (T) _ {k}), \quad k = 1, 2, \ldots , n\tag{3}
$$

Once the token sequence is processed by the tokenizer, it passes through the complex DL-based model, which outputs classification probabilities. In this paper, we employ various model architectures, including the classic LSTM and BERT [15].

## 4.3 Target Model

The feature models mentioned above serve as target models for our adversarial attacks. This process follows a black-box attack scenario, where the attacker has no knowledge of the target model’s features or architecture and relies solely on the output scores. In the third phase, RL is employed to fine-tune the LLM, using these models as reward models. The reward model guides the LLM to generate payloads that more efectively challenge and deceive the detection model.

## 5 Domain-Specific LLM Fine-Tuning

In this section, we fine-tune a general-purpose LLM using trafic datasets to improve its performance in trafic generation tasks. While advancements in LLMs have significantly enhanced text generation across general language understanding tasks [8, 46, 47], these LLMs often struggle in domain-specific applications due to a lack of specialized knowledge and contextual understanding. Fine tuning on specialized datasets efectively addresses this limitation. The LLM is able to better understand and generate text that fits the specific domain tasks.

We employ the Parameter-Eficient Fine-Tuning (PEFT) [33] to improve eficiency. Specifically, we utilize Low-Rank Adaptation (LoRA) [26], which minimizes the number of trainable parameters by focusing on low-rank matrix adaptation during fine-tuning. As shown in Eq. 4 and Eq. 5, ℎ represents the fine-tuned model parameters, $W _ { 0 }$ denotes the original pre-trained parameters, and matrices � and � serve as the low-rank down-projection and up-projection matrices, respectively, which are updated during fine-tuning. While full-parameter fine-tuning requires updating a large number of parameters, LoRA learns the low-rank matrix �� while keeping the pre-trained weights � frozen, which significantly reduces the trainable parameter counts, and reducing GPU consumption.

As shown in Fig. 3, we design prompts specifically for trafic generation. The instruction set guides the generation of specific trafic categories, with the input consisting of the functional fields. The LLM generates the non-functional fields, forming a complete trafic packet. The prompts are specifically designed to keep the functional fields unchanged while modifying the non-functional fields to create mutated trafic. Having learned the structural patterns of both benign and malicious trafic during fine-tuning, the LLM is able to generate corresponding trafic based on instructions.

$$
B \in \mathbb {R} ^ {d \times r}, A \in \mathbb {R} ^ {r \times k}\tag{4}
$$

$$
h = W _ {0} x + \Delta W x = W _ {0} x + B A x\tag{5}
$$

## 6 RL-Based Adversarial Generation

In this section, we employ Proximal Policy Optimization (PPO) [49] to fine-tune a LLM [42]. We propose a novel approach that builds upon the previously fine-tuned LLM in § 5, applying PPO for further fine-tuning. Specifically, the LLM, already adapted to the generation task, is now tasked with generating adversarial trafic to deceive detection models. This process treats the detection models as black-box systems that only output scores, with the LLM generating payloads and receiving reward scores based on the detection models’ evaluations (§ 4).

As shown in Fig. 3, the prompt set � consists of two parts: an instruction and functional fields. The functional fields are provided as input, while the instruction directs the LLM to generate trafic from the opposite class. For example, when the input consists of functional fields for malicious trafic, the instruction requires the output to be benign trafic. The LLM generates benign trafic � that deviate from the expected behavior based on the prompt �. This allows the attacker to craft complete adversarial trafic tailored to each input’s functional fields.

We design a novel reward mechanism that makes PPO suitable for adversarial attack tasks. The PPO process involves two LLMs: the domain-specific LLM, with frozen parameters, and the RL-Tuned LLM, which is updated during training. The purpose of this setup is to refine the RL-Tuned LLM’s ability to generate adversarial trafic while preserving the foundational behavior learned by the Domain LLM. The RL-Tuned LLM’s outputs are evaluated using multiple reward models trained in the first phase. As shown in Eq. 6, each reward model provides a reward score, $r _ { \theta } ( x , y )$ , which can be interpreted as a variant of the cross-entropy function, referred to as negative cross-entropy. Traditional cross-entropy minimizes the diference between the predicted value $D _ { i } ( y )$ and the label $L _ { x } .$ . In contrast, negative cross-entropy increases the reward as the prediction deviates further from $L _ { x }$ , encouraging the generation of adversarial examples. The final reward score is calculated as the average of multiple reward model $D _ { i } ( y )$ outputs. This aggregation provides a more balanced and comprehensive evaluation, ensuring that the adversarial trafic generated by the RL-Tuned LLM efectively challenges a range of detection models.

In addition to the averaged reward score, the PPO includes a KL divergence penalty. This penalty ensures that while the RL-Tuned LLM is optimized for adversarial performance, its outputs do not deviate excessively from the behavior of the domain-specific LLM. The KL-divergence term helps maintain consistency in the genera tion process, preventing the RL-Tuned LLM from generating trafic that is too diferent from the original model’s behavior. As shown in Eq. 7, the PPO process strikes a balance between generating highly adversarial trafic and retaining the underlying structure and coherence of the original model by combining multiple reward models with the KL-divergence term.

$$
r _ {\theta} (x, y) = - \frac {1}{N} \sum_ {i = 1} ^ {N} \left[ \left(1 - L _ {x}\right) \log (D _ {i} (y)) + L _ {x} \log (1 - D _ {i} (y)) \right]\tag{6}
$$

$$
R (x, y) = r _ {\theta} (x, y) - \beta \log \left[ \pi_ {\phi} ^ {\mathrm{RL}} (y \mid x) / \pi^ {\mathrm{SFT}} (y \mid x) \right]\tag{7}
$$

In general, we leverage a novel reward mechanism and balance it with a KL-divergence penalty, enabling the RL-Tuned LLM to generate mutated trafic that detection models struggle to detect.

## 7 Experimental Evaluation

## 7.1 Experiment Setup

Testbed. We deploy AdvTG in Ubuntu 22.04.1 with Python3.11 based on a testbed built upon Supermicro servers with one AMD EPYC 7532 CPU, one NVIDIA 4090, 256GB MEM.

Datasets. We mainly use a variety of open-source malicious trafic datasets and self-collected datasets. The details of the datasets are introduced in § C.

Targeted Detection Models. We construct three diferent detection models, each applied separately to both image-based and text based feature extraction methods. The details of the datasets are introduced in § D.

LLM Architecture. We select Meta-Llama-3-8B as the base LLM for fine-tuning and adversarial sample generation [1].

Attack Baselines. We select text-based adversarial attack mod els and do not consider image domain, including some methods mentioned in § 1. This is because these attacks introduce byte-level perturbations that either violate network protocol specifications or fail to generate complete trafic. Therefore, we compare three text-based adversarial attack methods.

• TextFooler (T-F) [29] generates adversarial attacks by replacing key words with semantically similar alternatives to change model predictions.

• WordLevel (W-L) [67] optimizes word substitutions to mislead models, preserving the text’s meaning and fluency.

• BAE [22] uses BERT to generate adversarial examples through word substitution and insertion, maintaining the text’s original semantics.

In addition to the text adversarial attack methods, we employ the Random Substitution (R-S) method. Specifically, we randomly se lect unrelated fields from diferent categories to replace the original non-functional fields. For instance, non-functional fields in malicious trafic are substituted with those from benign trafic, thereby deceiving the detection model. Metrics. We evaluate our approach primarily from both detection efectiveness and attack efectiveness perspectives.

• Detection Efectiveness. We mainly use precision (P), recall (R), and F1 score which they are most widely used in the literature [7, 20, 40]

• Attack Efectiveness. We use the attack success rate (ASR) as the primary metric to evaluate the efectiveness of attacks [4, 9, 59], measuring the proportion of successful attacks in deceiving the detection model as shown in Eq. 8.

$$
A S R = \frac {N _ {\mathrm{success}}}{N _ {\mathrm{total}}}\tag{8}
$$

## 7.2 Evaluation

The following sections present a comprehensive evaluation ofdetection models and adversarial attack methods across several datasets. First, we evaluate the efectiveness of six detection models using both text and image features, and evaluate attack performance based on ASR. Then, we evaluate the adversarial trafic compliance before and after fine-tuning using a compliance evaluation algorithm. In addition, ablation studies are conducted to analyze the impact of RL on improving ASR. Finally, extended datasets are used to verify the generalization capabilities of AdvTG.

Table 2 summarizes the performance of detection models and attack methods. The left three columns (P, R, F1) evaluate the detection accuracy of six models across two feature types, while the right five columns present the attack success rate (ASR) to evaluate the efectiveness of various attack methods.

Detection Efectiveness. We train image-based and text-based models on the training sets and evaluate their detection performance on the test sets. As shown in Table 2, the F1 score on the test set is higher than 0.96 regardless of the characteristics of the model used. Noteworthy, the text-based models all reach above 0.98, which is better than the image-based models. This shows that the text feature is more efective at detecting the plaintext payload and can better identify the relevant patterns.

Attack Efectiveness on the Base Datasets. We evaluate the impact of adversarial trafic on detection models by measuring the ASR offour trafic. As shown in Table 2, AdvTG consistently achieve over 40% ASR across four datasets, whereas text-based attacks result in less than 10% ASR. This is because traditional methods focus on altering a few keywords, which is insuficient to evade detection. Our approach, leveraging LLM, modifies multiple fields while ensuring the trafic remains both semantic and functional, producing a diverse range of mutated trafic templates that deceive detection models.

Additionally, since text-based adversarial attacks are limited to text domains, they cannot target models relying on image features. In contrast, AdvTG provides general adversarial attacks, efective across models with any content-based features. Furthermore, the R-S attack also shows a low ASR, below 22.27%, indicating that replacing non-functional fields alone is not enough to mislead the models. This underscores the generalization capability of detection models. By using RL with multiple reward feedback loops, our approach identifies fields most likely to deceive the model, resulting in a higher ASR.

Table 2: The adversarial efectiveness of DL-based trafic detection on the base datasets.

<table><tr><td rowspan="2">Feature Extractor</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td></tr><tr><td rowspan="3">Text</td><td>TextCNN</td><td>0.99</td><td>1</td><td>0.99</td><td>0.07%</td><td>0.13%</td><td>0.60%</td><td>0.84%</td><td>69.53%</td><td>TextCNN</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.13%</td><td>0.74%</td><td>0.60%</td><td>1.08%</td><td>69.53%</td></tr><tr><td>DeepLog</td><td>0.99</td><td>0.99</td><td>0.99</td><td>2.01%</td><td>2.02%</td><td>2.61%</td><td>5.25%</td><td>66.41%</td><td>DeepLog</td><td>0.98</td><td>0.99</td><td>0.99</td><td>2.41%</td><td>2.43%</td><td>3.02%</td><td>7.44%</td><td>66.41%</td></tr><tr><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.24%</td><td>0.08%</td><td>2.42%</td><td>3.94%</td><td>67.18%</td><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0%</td><td>0.35%</td><td>2.69%</td><td>5.33%</td><td>67.19%</td></tr><tr><td rowspan="3">Image</td><td>MalTraffic</td><td>0.98</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>20.13%</td><td>42.78%</td><td>MalTraffic</td><td>0.96</td><td>0.99</td><td>0.97</td><td>-</td><td>-</td><td>-</td><td>20.87%</td><td>66.99%</td></tr><tr><td>RBRN</td><td>0.98</td><td>0.99</td><td>0.99</td><td>-</td><td>-</td><td>-</td><td>20.08%</td><td>42.17%</td><td>RBRN</td><td>0.96</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>20.68%</td><td>64.08%</td></tr><tr><td>DeepMal</td><td>0.98</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>16.68%</td><td>43.69%</td><td>DeepMal</td><td>0.96</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>20.87%</td><td>64.56%</td></tr><tr><td></td><td colspan="9">(c) Malware</td><td colspan="9">(d) APT</td></tr><tr><td rowspan="2">Feature Extractor</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td></tr><tr><td rowspan="3">Text</td><td>TextCNN</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.20%</td><td>0.68%</td><td>0.40%</td><td>1.18%</td><td>65.62%</td><td>TextCNN</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.11%</td><td>0.79%</td><td>0.14%</td><td>0.76%</td><td>48.43%</td></tr><tr><td>DeepLog</td><td>0.98</td><td>0.99</td><td>0.99</td><td>5.35%</td><td>5.35%</td><td>6.38%</td><td>7.26%</td><td>59.37%</td><td>DeepLog</td><td>0.99</td><td>0.99</td><td>0.99</td><td>2.64%</td><td>2.98%</td><td>2.64%</td><td>5.28%</td><td>41.41%</td></tr><tr><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.41%</td><td>0.36%</td><td>2.80%</td><td>5.53%</td><td>61.71%</td><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.10%</td><td>0%</td><td>1.60%</td><td>3.87%</td><td>50.29%</td></tr><tr><td rowspan="3">Image</td><td>MalTraffic</td><td>0.95</td><td>0.99</td><td>0.97</td><td>-</td><td>-</td><td>-</td><td>20.87%</td><td>67.47%</td><td>MalTraffic</td><td>0.98</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>14.20%</td><td>47.57%</td></tr><tr><td>RBRN</td><td>0.96</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>22.27%</td><td>67.96%</td><td>RBRN</td><td>0.98</td><td>0.99</td><td>0.99</td><td>-</td><td>-</td><td>-</td><td>15.42%</td><td>49.18%</td></tr><tr><td>DeepMal</td><td>0.96</td><td>0.98</td><td>0.97</td><td>-</td><td>-</td><td>-</td><td>19.32%</td><td>66.50%</td><td>DeepMal</td><td>0.97</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>15.09%</td><td>49.51%</td></tr></table>

Table 3: Proportion of Compliance in Generated Trafic Before and After Fine-tuning.

<table><tr><td>Datasets</td><td>Before Fine-tuning</td><td>After Fine-tuning</td></tr><tr><td>CICIDS2017</td><td>29.68%</td><td>89.16%</td></tr><tr><td>CICIoT2023</td><td>16.40%</td><td>82.75%</td></tr><tr><td>Malware</td><td>39.06%</td><td>87.54%</td></tr><tr><td>APT</td><td>28.90%</td><td>88.67%</td></tr></table>

Trafic Compliance. We develope an algorithm, detailed in § E, to evaluate the compliance of generated trafic. We compare the compliance proportion of trafic generated by the general-purpose LLM with that of the fine-tuned LLM. As shown in Table 3, trafic generated before fine-tuning has a compliance proportion ofaround 20% across the four datasets. After fine-tuning, this proportion increases significantly to over 80%, demonstrating that the methods proposed in § 5 efectively improve trafic compliance for real-world applications.

Ablation Experiments. As shown in Fig. 4, we conduct adversarial generation experiments on a general-purpose LLM without fine-tuning, a fine-tuned domain-specific LLM, and an RL-Tuned LLM. The domain-specific LLM shows weak adversarial capabili ties. However, after applying RL, the ASR significantly improves, demonstrating the efectiveness of RL. Additionally, while some general-purpose LLMs without fine-tuning achieve relatively high ASR, their generated trafic often fails to meet compliance, as previously mentioned.

Attack Efectiveness on the Extended Datasets. We evaluate the generalization capabilities of AdvTG on two extended datasets, CICAPT-IoT2024 and APT2024. The two datasets are used solely for testing and not involved in training or LLM fine-tuning. As shown in Table 4, the detection models demonstrate strong performance, with F1 consistently above 0.92 across both text-based and imagebased detection. After applying adversarial attacks, our method, AdvTG, consistently achieves higher ASR compared to other attacks, with over 40% ASR on CICAPT-IoT2024 and over 50% on APT2024. This indicates that AdvTG generalizes well across diferent datasets, maintaining a high level of adversarial efectiveness.

## 8 Discussion

In this section, we discuss some potential limitations of AdvTG. Adversarial Attacks against LLMs. LLMs have been applied to cybersecurity, with their language understanding capabilities ofer ing an advantage in analyzing payloads. We conducted experiments using general-purpose models, ChatGPT 3.5 and ChatGPTs, on APT and malware datasets. Details are provided in § F.1.

Encrypted Trafic Detection. Encrypted trafic detection is an important direction [12, 16]. Many encrypted detection models [25, 34, 61] combine the analysis of sequence features, such as packet size, with an encrypted payload. Therefore, further investigation is needed to determine whether adversarial trafic generated by AdvTG retains its evasive properties after encryption. Exploring the potential to deceive encrypted trafic detection models by manipulating both sequence features and payload presents a valuable avenue for future exploration.

## 9 Related Work

There are several related works in the fields of malicious trafic detection and adversarial attacks.

Malicious Trafic Detection. Malicious trafic detection based on deep learning has become a widely used technology. Based on content features, HSTF-Model extracts information from payload [60], and HMCD-Model adds GAN-based enhancement technology for more scenarios [66]. Based on sequence features, ContraMTD uses contrastive learning to learn the relationship between local/global interaction features [24] and Trident transforms known/new class recognition problems into multiple independent single-class learn ing tasks in trafic detection [69].

Table 4: The adversarial efectiveness of DL-based trafic detection on the extended datasets.

<table><tr><td>FeatureExtractor</td></tr><tr><td>Text</td></tr><tr><td>Image</td></tr></table>

(a) CICAPT-IIoT2024

<table><tr><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)—higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td></tr><tr><td>TextCNN</td><td>0.99</td><td>0.99</td><td>0.99</td><td>1.35%</td><td>2.45%</td><td>1.69%</td><td>0.69%</td><td>46.87%</td></tr><tr><td>DeepLog</td><td>0.99</td><td>1</td><td>0.99</td><td>1.91%</td><td>1.74%</td><td>3.45%</td><td>5.15%</td><td>33.59%</td></tr><tr><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>0.55%</td><td>0.14%</td><td>1.56%</td><td>4.58%</td><td>43.75%</td></tr><tr><td>MalTraffic</td><td>0.98</td><td>0.99</td><td>0.99</td><td>-</td><td>-</td><td>-</td><td>17.64%</td><td>45.31%</td></tr><tr><td>RBRN</td><td>0.98</td><td>0.99</td><td>0.99</td><td>-</td><td>-</td><td>-</td><td>18.79%</td><td>43.75%</td></tr><tr><td>DeepMal</td><td>0.98</td><td>0.99</td><td>0.98</td><td>-</td><td>-</td><td>-</td><td>15.08%</td><td>42.18%</td></tr></table>

(b) APT2024

<table><tr><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>T-F</td><td>W-L</td><td>BAE</td><td>R-S</td><td>AdvTG</td></tr><tr><td>TextCNN</td><td>0.98</td><td>0.99</td><td>0.99</td><td>0.30%</td><td>0.60%</td><td>0.60%</td><td>1.40%</td><td>53.97%</td></tr><tr><td>DeepLog</td><td>0.98</td><td>0.91</td><td>0.94</td><td>1.07%</td><td>1.72%</td><td>2.79%</td><td>7.63%</td><td>39.70%</td></tr><tr><td>BERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>1.11%</td><td>1.61%</td><td>2.32%</td><td>4.64%</td><td>50.78%</td></tr><tr><td>MalTraffic</td><td>0.95</td><td>0.90</td><td>0.92</td><td>-</td><td>-</td><td>-</td><td>16.52%</td><td>54.31%</td></tr><tr><td>RBRN</td><td>0.97</td><td>0.97</td><td>0.97</td><td>-</td><td>-</td><td>-</td><td>20.68%</td><td>52.73%</td></tr><tr><td>DeepMal</td><td>0.95</td><td>0.94</td><td>0.95</td><td>-</td><td>-</td><td>-</td><td>14.37%</td><td>50.52%</td></tr></table>

![](images/71ea1804f46fba14a2befa7883ee8cca426088310e0461fa6a659c07c1ba6dce.jpg)  
(a) ASR on CICIDS2017

![](images/54c717b216b009c5bb7e821d270230ac4b748305763a2e9acbf354e982946be7.jpg)  
(b) ASR on CICIoT2023

![](images/33e0093db136aff12bc7268bf444e6219b35074beba3b76caa2011df2e4c0b7d.jpg)  
(c) ASR on Malware

![](images/93832b366a5eb73ca85f0818645bd38ecf207e7e3f15c2647fb7d5e3e842dc1b.jpg)  
(d) ASR on APT  
Figure 4: Adversarial efectiveness across diferent LLMs on various datasets and detection models.

Adversarial Attacks on Trafic Detection. As shown in Table 1, these methods mainly involve three types of technologies: statisti cal feature attacks, sequence feature attacks, and content attacks. (i) Statistical feature attacks [18, 35, 53] modify statistical features (flow duration and average packet size). These methods typically sufer from limitations in handling various features and generaliz ing across diferent attack scenarios. (ii) Sequence feature attacks [23, 32, 41, 52, 54] alter temporal and spatial sequence features (e.g., packet intervals, packet lengths) but payload-based detection mod els remain efective. While they ofer improvements in maintaining protocol compliance, they cannot often generate trafic content. (iii) Content attacks [11, 37, 55, 64] directly modify trafic packets to evade detection. These methods focus on generating trafic pack ets directly, but they struggle to produce trafic that is semantic, compliant, and functional.

## 10 Conclusion

In this paper, we propose AdvTG, a framework that uses LLMs and RL to generate adversarial trafic and deceive DL-based detection models that analyze malicious payloads. The adversarial trafic generated by AdvTG maintains both semantic coherence and protocol compliance. We introduce perturbations in the nonfunctional space to ensure the core functionality of the mutated trafic remains intact. Extensive experiments across various model architectures and feature sets demonstrate that AdvTG achieves a high ASR against DL-based models, highlighting the inherent weakness in these detection models.

## Acknowledgments

This work is supported by the Scaling Program of Institute of Information Engineering, CAS (Grant No. E3Z0041101).

## References

[1] AI@Meta. 2024. Llama 3 Model Card. (2024). https://github.com/meta-llama/ llama3/blob/main/MODEL\_CARD.md

[2] Afnan Alotaibi and Murad A Rassam. 2023. Adversarial machine learning attacks against intrusion detection systems: A survey on strategies and defense. Future Internet 15, 2 (2023), 62.

[3] Any.run. [n. d.]. ANY.RUN - Interactive Online Malware Sandbox. https://app. any.run/. Accessed: October 9, 2024.

[4] Anish Athalye, Nicholas Carlini, and David Wagner. 2018. Obfuscated gradients give a false sense of security: Circumventing defenses to adversarial examples. In International conference on machine learning. PMLR, 274–283

[5] Battista Biggio, Igino Corona, Davide Maiorca, Blaine Nelson, Nedim Šrndić, Pavel Laskov, Giorgio Giacinto, and Fabio Roli. 2013. Evasion attacks against machine learning at test time. In Machine Learning and Knowledge Discovery in Databases: European Conference, ECML PKDD 2013, Prague, Czech Republic, September 23-27, 2013, Proceedings, Part III 13. Springer, 387–402.

[6] Battista Biggio, Blaine Nelson, and Pavel Laskov. 2012. Poisoning Attacks against Support Vector Machines. (2012).

[7] Leyla Bilge, Davide Balzarotti, William Robertson, Engin Kirda, and Christopher Kruegel. 2012. Disclosure: detecting botnet command and control servers through large-scale netflow analysis. In Proceedings ofthe 28th Annual Computer Security Applications Conference. 129–138.

[8] Tom B Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. In Proceedings ofthe 34th International Conference on Neural Information Processing Systems. 1877– 1901.

[9] Nicholas Carlini and David Wagner. 2017. Towards evaluating the robustness of neural networks. In 2017 ieee symposium on security and privacy (sp). Ieee, 39–57.

[10] Yangyi Chen, Hongcheng Gao, Ganqu Cui, Lifan Yuan, Dehan Kong, Hanlu Wu, Ning Shi, Bo Yuan, Longtao Huang, Hui Xue, et al. 2023. From Adversarial Arms Race to Model-centric Evaluation Motivating a Unified Automatic Robustness Evaluation Framework. In 61st Annual Meeting of the Association for Computational Linguistics, ACL 2023. Association for Computational Linguistics (ACL), 9607–9632.

[11] Qiumei Cheng, Shiying Zhou, Yi Shen, Dezhang Kong, and Chunming Wu. 2021. Packet-Level Adversarial Network Trafic Crafting using Sequence Generative Adversarial Networks. arXiv e-prints (2021), arXiv–2103.

[12] Susu Cui, Cong Dong, Meng Shen, Yuling Liu, Bo Jiang, and Zhigang Lu. 2023. CBSeq: A Channel-Level Behavior Sequence for Encrypted Malware Trafic Detection. 18 (2023), 5011–5025.

[13] Luca Demetrio, Battista Biggio, Giovanni Lagorio, Fabio Roli, and Alessandro Armando. 2021. Functionality-preserving black-box optimization of adversarial windows malware. IEEE Transactions on Information Forensics and Security 16 (2021), 3469–3478.

[14] Luca Deri, Maurizio Martinelli, Tomasz Bujlow, and Alfredo Cardigliano. 2014. ndpi: Open-source high-speed deep packet inspection. In 2014 International Wireless Communications and Mobile Computing Conference (IWCMC). IEEE, 617–622.

[15] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In Proceedings ofthe 2019Conference ofthe North American Chapter ofthe Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers). Association for Computational Linguistics, 4171–4186.

[16] Cong Dong, Zhigang Lu, Zelin Cui, Baoxu Liu, and Kai Chen. 2021. MBTree: Detecting Encryption RATs Communication Using Malicious Behavior Tree. 16 (2021), 3589–3603.

[17] Min Du, Feifei Li, Guineng Zheng, and Vivek Srikumar. 2017. DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning. In Proceedings ofthe 2017 ACM SIGSAC Conference on Computer and Communications Security (CCS). ACM, 1285–1298.

[18] Phan The Duy, Nghi Hoang Khoa, Anh Gia-Tuan Nguyen, Van-Hau Pham, et al. 2021. DIGFuPAS: Deceive IDS with GAN and function-preserving on adversarial samples in SDN-enabled networks. Computers & Security 109 (2021), 102367.

[19] Michael Finsterbusch, Chris Richter, Eduardo Rocha, Jean-Alexander Muller, and Klaus Hanssgen. 2013. A survey of payload-based trafic classification approaches. IEEE Communications Surveys & Tutorials 16, 2 (2013), 1135–1156.

[20] Chuanpu Fu, Qi Li, Meng Shen, and Ke Xu. 2021. Realtime robust malicious trafic detection via frequency domain analysis. In Proceedings of the 2021 ACM SIGSAC Conference on Computer and Communications Security. 3431–3446.

[21] Chuanpu Fu, Qi Li, Meng Shen, and Ke Xu. 2022. Frequency domain feature based robust malicious trafic detection. IEEE/ACM Transactions on Networking 31, 1 (2022), 452–467.

[22] Shivam Garg, Ganesh Ramakrishnan, and Animesh Saha. 2020. BAE: BERT-based Adversarial Examples for Text Classification. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP). Association for Computational Linguistics, 6174–6181.

[23] Dongqi Han, Zhiliang Wang, Ying Zhong, Wenqi Chen, Jiahai Yang, Shuqiang Lu, Xingang Shi, and Xia Yin. 2021. Evaluating and improving adversarial robustness of machine learning-based network intrusion detectors. IEEE Journal on Selected Areas in Communications 39, 8 (2021), 2632–2647.

[24] Xueying Han, Susu Cui, Jian Qin, Song Liu, Bo Jiang, Cong Dong, Zhigang Lu, and Baoxu Liu. 2024. ContraMTD: An Unsupervised Malicious Network Trafic Detection Method based on Contrastive Learning. In Proceedings ofthe ACM on Web Conference 2024. 1680–1689.

[25] Jordan Holland, Paul Schmitt, Nick Feamster, and Prateek Mittal. 2021. New Directions in Automated Trafic Analysis. 3366–3383.

[26] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. Lora: Low-rank adaptation of large language models. arXiv preprint arXiv:2106.09685 (2021)

[27] Ren-Hung Hwang, Min-Chun Peng, Van-Linh Nguyen, and Yu-Lun Chang. 2019. An LSTM-based deep learning approach for classifying malicious trafic at the packet level. Applied Sciences 9, 16 (2019), 3414.

[28] Andrew Ilyas, Logan Engstrom, Anish Athalye, and Jessy Lin. 2018. Blackbox adversarial attacks with limited queries and information. In International conference on machine learning. PMLR, 2137–2146

[29] Di Jin, Zhijing Jin, Joey Tianyi Zhou, and Peter Szolovits. 2020. Is BERT really robust? A strong baseline for natural language attack on text classification and entailment. In Proceedings ofthe AAAI conference on artificial intelligence, Vol. 34. 8018–8025.

[30] Houda Jmila and Mohamed Ibn Khedher. 2022. Adversarial machine learning for network intrusion detection: A comparative study. Computer Networks 214 (2022), 109073.

[31] Yoon Kim. 2014. Convolutional Neural Networks for Sentence Classification. In Proceedings ofthe 2014 Conference on Empirical Methods in Natural Language Processing (EMNLP). 1746–1751.

[32] Wenhao Li, Xiao-Yu Zhang, Huaifeng Bao, Binbin Yang, Zhaoxuan Li, Haichao Shi, and Qiang Wang. 2023. Prism: Real-Time Privacy Protection Against Temporal Network Trafic Analyzers. IEEE Transactions on Information Forensics and Security 18 (2023), 2524–2537.

[33] Xiang Lisa Li and Percy Liang. 2021. Prefix-tuning: Optimizing continuous prompts for generation. arXiv preprint arXiv:2101.00190 (2021).

[34] Xinjie Lin, Gang Xiong, Gaopeng Gou, Zhen Li, Junzheng Shi, and Jing Yu. 2022. Et-bert: A contextualized datagram representation with pre-training transformers for encrypted trafic classification. In Proceedings ofthe ACM Web Conference 2022. 633–642.

[35] Zilong Lin, Yong Shi, and Zhi Xue. 2022. Idsgan: Generative adversarial networks for attack generation against intrusion detection. In Pacific-asia conference on knowledge discovery and data mining. Springer, 79–91.

[36] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa: A Robustly Optimized BERT Pretraining Approach. arXiv preprint arXiv:1907.11692 (2019).

[37] Siyang Lu, Mingquan Wang, Dongdong Wang, Xiang Wei, Sizhe Xiao, Zhiwei Wang, Ningning Han, and Liqiang Wang. 2023. Black-box attacks against log anomaly detection with adversarial examples. Information Sciences 619 (2023), 249–262.

[38] Gabriel Marín, Pedro Casas, and German Capdehourat. 2021. DeepMAL: Deep Learning Models for Malware Trafic Detection and Classification. In Data Science–Analytics and Applications: Proceedings ofthe 3rd International Data Science Conference–IDSC2020. Springer Fachmedien Wiesbaden, 105–112

[39] Andrew McCarthy, Essam Ghadafi, Panagiotis Andriotis, and Phil Legg. 2022. Functionality-preserving adversarial machine learning for robust classification in cybersecurity and intrusion detection domains: A survey. Journal ofCybersecurity and Privacy 2, 1 (2022), 154–190.

[40] Yisroel Mirsky, Tomer Doitshman, Yuval Elovici, and Asaf Shabtai. 2018. Kitsune: an ensemble of autoencoders for online network intrusion detection. arXiv preprint arXiv:1802.09089 (2018).

[41] Milad Nasr, Alireza Bahramali, and Amir Houmansadr. 2021. Defeating {DNN-Based} trafic analysis systems in {Real-Time} with blind adversarial perturbations. In 30th USENIX Security Symposium (USENIX Security 21). 2705–2722.

[42] Long Ouyang, Jefrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. Advances in neural information processing systems 35 (2022), 27730–27744.

[43] Eva Papadogiannaki, Constantinos Halevidis, Periklis Akritidis, and Lazaros Koromilas. 2018. Otter: A scalable high-resolution encrypted trafic identification engine. In Research in Attacks, Intrusions, and Defenses: 21st International Symposium, RAID 2018, Heraklion, Crete, Greece, September 10-12, 2018, Proceedings 21. Springer, 315–334.

[44] Nicolas Papernot, Patrick McDaniel, and Ian Goodfellow. 2016. Transferability in machine learning: from phenomena to black-box attacks using adversarial samples. arXiv preprint arXiv:1605.07277 (2016)

[45] Antonio Paya, Sergio Arroni, Vicente García-Díaz, and Alberto Gómez. 2024. Apollon: a robust defense system against adversarial machine learning attacks in

intrusion detection systems. Computers & Security 136 (2024), 103546.

[46] Alec Radford. 2018. Improving language understanding by generative pretraining. (2018).

[47] Alec Radford, Jefrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. Language models are unsupervised multitask learners. OpenAI blog 1, 8 (2019), 9.

[48] Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf. 2019. Dis tilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv preprint arXiv:1910.01108 (2019).

[49] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017. Proximal policy optimization algorithms. arXiv preprint arXiv:1707.06347 (2017).

[50] C Szegedy. 2013. Intriguing properties of neural networks. arXiv preprint arXiv:1312.6199 (2013).

[51] VirusTotal. [n. d.]. VirusTotal - Free Online Virus, Malware and URL Scanner. https://www.virustotal.com/gui/home/upload. Accessed: October 9, 2024

[52] Junnan Wang, Liu Qixu, Wu Di, Ying Dong, and Xiang Cui. 2021. Crafting adversarial example to bypass flow-&ML-based botnet detector via RL. In Proceedings ofthe 24th international symposium on research in attacks, intrusions and defenses. 193–204.

[53] Kai Wang, Zhiliang Wang, Dongqi Han, Wenqi Chen, Jiahai Yang, Xingang Shi, and Xia Yin. 2023. BARS: Local Robustness Certification for Deep Learning based Trafic Analysis Systems.. In NDSS.

[54] Minxiao Wang, Ning Yang, Nicolas J Forcade-Perkins, and Ning Weng. 2024. Pro Gen: Projection-based Adversarial Attack Generation against Network Intrusion Detection. IEEE Transactions on Information Forensics and Security (2024).

[55] Qiuhua Wang, Hui Yang, Guohua Wu, Kim-Kwang Raymond Choo, Zheng Zhang, Gongxun Miao, and Yizhi Ren. 2022. Black-box adversarial attacks on XSS attack detection model. Computers & Security 113 (2022), 102554

[56] Shanshan Wang, Qiben Yan, Zhenxiang Chen, Bo Yang, Chuan Zhao, and Mauro Conti. 2017. Detecting android malware leveraging text semantics of network flows. IEEE Transactions on Information Forensics and Security 13, 5 (2017), 1096– 1109.

[57] Wei Wang, Miao Zhu, Xiang Zeng, Xiaofeng Ye, Ying Sheng, and Zhuo Chen. 2017. Malware trafic classification using convolutional neural network for rep resentation learning. In 2017 International Conference on Information Networking (ICOIN). IEEE, 712–717.

[58] Zimu Wang, Wei Wang, Qi Chen, Qiufeng Wang, and Anh Nguyen. 2024. Generating valid and natural adversarial examples with large language models. In 2024 27th International Conference on Computer Supported Cooperative Work in Design (CSCWD). IEEE, 1716–1721.

[59] Rey Reza Wiyatno, Anqi Xu, Ousmane Dia, and Archy De Berker. 2019. Ad versarial examples in modern machine learning: A review. arXiv preprint arXiv:1911.05268 (2019).

[60] Jiang Xie, Shuhao Li, Xiaochun Yun, Yongzheng Zhang, and Peng Chang. 2020. Hstf-model: An http-based trojan detection model via the hierarchical spatio temporal features of trafics. Computers & Security 96 (2020), 101923.

[61] Hongbo Xu, Zhenyu Cheng, Shuhao Li, Chenxu Wang, Peishuai Sun, Jiang Xie, and Qingyun Liu. 2024. ProxyKiller: an Anonymous Proxy Trafic Attack Model Based on Trafic Behavior Graphs. (2024), 162–181.

[62] Zhilin Yang, Zihang Dai, Yiming Yang, Jaime Carbonell, Ruslan Salakhutdinov, and Quoc V Le. 2019. XLNet: Generalized Autoregressive Pretraining for Lan guage Understanding. In Advances in Neural Information Processing Systems, Vol. 32. 5753–5763.

[63] Tao Yi, Xingshu Chen, Yi Zhu, Weijing Ge, and Zhenhui Han. 2023. Review on the application of deep learning in network attack detection. Journal ofNetwork and Computer Applications 212 (2023), 103580.

[64] Peng Yuan, Shanshan Wang, Chuan Zhao, Wenyue Wang, Daokuan Bai, Lizhi Peng, and Zhenxiang Chen. 2023. Adversarial Attack with Genetic Algorithm against IoT Malware Detectors. In ICC 2023-IEEE International Conference on Communications. IEEE, 1413–1418.

[65] Ying Yuan, Qingying Hao, Giovanni Apruzzese, Mauro Conti, and Gang Wang. 2024. " Are Adversarial Phishing Webpages a Threat in Reality?" Understanding the Users’ Perception of Adversarial Webpages. In Proceedings of the ACM on Web Conference 2024. 1712–1723.

[66] Xiaochun Yun, Jiang Xie, Shuhao Li, Yongzheng Zhang, and Peishuai Sun. 2022. Detecting unknown HTTP-based malicious communication behavior via gener ated adversarial flows and hierarchical trafic features. Computers & Security 121 (2022), 102834.

[67] Weihao Zang, Yang Du, Junyu Luo, Jizhi Zhang, Zhiyuan Liu, and Maosong Sun. 2020. Word-level Textual Adversarial Attacking as Combinatorial Optimization. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, 6066–6080. doi:10.18653/ v1/2020.acl-main.540

[68] Pei Zhang, Fangzhou He, Han Zhang, Jiankun Hu, Xiaohong Huang, Jilong Wang, Xia Yin, Huahong Zhu, and Yahui Li. 2023. Real-time malicious trafic detec tion with online isolation forest over sd-wan. IEEE Transactions on Information Forensics and Security 18 (2023), 2076–2090.

![](images/1cc5d03340e9e10421dce4a0e15702ed016c7bdba757b9f7aafa2a402ccdbb88.jpg)  
Figure 5: Cobalt Strike HTTP trafic.

[69] Ziming Zhao, Zhaoxuan Li, Zhuoxue Song, Wenhao Li, and Fan Zhang. 2024. Tri dent: A Universal Framework for Fine-Grained and Class-Incremental Unknown Trafic Detection. In Proceedings ofthe ACM on Web Conference 2024. 1608–1619.

[70] W. Zheng, C. Gou, L. Yan, et al. 2020. Learning to classify: A flow-based relation network for encrypted trafic classification. In Proceedings of The Web Conference 2020. 13–22.

## Appendix

## A Malicious HTTP Packet Case

We use an example of Cobalt Strike’s HTTP trafic to illustrate the distinction between functional and non-functional fields, as shown in Fig. 5. Cobalt Strike is a penetration testing tool often repurposed by attackers for malicious activities. The red-highlighted parts represent the core functional fields of the HTTP trafic, including the URI header, Host field, and payload. These are essential for maintaining trafic functionality and are dificult to modify without risking the disruption of network activity. While non-functional fields carry less significance compared to functional fields, they often contain inherent characteristics of trafic. As a result, non-functional fields are also frequently used as features to detect malicious trafic rather than solely relying on functional fields. The italicized parts show the User-Agent field (Mozilla/5.0 (compatible:MSIE 9.0;Windows NT 6.1:WOW64:Trident/5.0:MATP:MATP)) commonly used by Cobalt Strike and the Content-Type field (application/octet-stream), which is fixed features ofCobalt Strike. These are examples ofnon-functiona features exploited by defenders for detection. Defenders can detect these features using rule-based methods or detection models. Similarly, attackers can modify non-functional fields to evade detection, especially DL-based detection.

## B An Example of of Deceiving DL-Based Detection Using AdvTG

This example demonstrates the efectiveness of AdvTG in deceiving a DL-based malicious trafic detection. Initially, as shown in Fig. 6, the trafic packet on the left is classified with 97.85% confidence as malicious by the detection model. The packet includes a User-Agent field (Go-http-client/1.1), which is a known indicator of potentially malicious activity often associated with automated tools or attacks.

Through the application of AdvTG, modifications are made to certain non-functional fields of trafic, ensuring that the trafic remains its original structure and functionality. Unlike traditional adversarial attack methods that often rely on manual feature manipulation, AdvTG leverages the ability of the LLM and RL to automate the generation of the most efective adversarial fields. By continu ously refining the trafic through RL, AdvTG identifies and alters the non-functional fields that are most likely to deceive the detection model.

Table 5: Trafic datasets.

<table><tr><td>Dataset Group</td><td>Datasets</td><td>Attacks Types (Examples)</td><td># Test Pkts (Malicious)</td><td># Training Pkts</td></tr><tr><td rowspan="4">Base Dataset</td><td>CICIDS2017</td><td>Botnet, Web Attack, Infiltration</td><td>10,000 (5,132)</td><td rowspan="4">100,000(50,000 benign &amp; 50,000 malicious)</td></tr><tr><td>CICIoT2023</td><td>Recon, Web attack, DDoS</td><td>10,000 (3,045)</td></tr><tr><td>Malware</td><td>Trickbot, Qakbot, Emotet</td><td>10,000 (2,670)</td></tr><tr><td>APT</td><td>APT27, APT28, APT37</td><td>10,000 (4,813)</td></tr><tr><td rowspan="2">Extended Dataset</td><td>CIC-APT-IIoT2024</td><td>APT29, APT28, APT32</td><td>5,000 (2,500)</td><td rowspan="2">-</td></tr><tr><td>APT2024</td><td>Lazarus, Kimsuky, Bitter</td><td>1,000 (384)</td></tr></table>

![](images/3c60319bd19300f887281e4d832f9f92927664bf57fbd9721b00ed68ba62dded.jpg)  
Figure 6: A case of deceiving DL-based detection using AdvTG.

In the altered trafic packet (right side of the figure), the User-Agent field has been replaced with a more commonly used and benign browser identifier: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36. This modification makes the trafic appear to be from a legitimate web browser, thus reducing the likelihood of detection. After this adversarial transformation, the classification confidence of the detection model changed dramatically. The modified packet is classified as 66.61% benign, a stark contrast to the initial malicious classification. This reduction in malicious probability highlights how adversarial attacks can successfully deceive well-trained DL based models by subtly altering trafic fields that are commonly relied upon for detection.

## C Details of Dataset

Table 5 summarizes the information about the trafic datasets used in this study, including the base dataset and extended database.

## C.1 Base Dataset

We utilize three publicly accessible, open-source datasets, along with an additional dataset that we collected independently as part of the base dataset.

• CICIDS2017 <sup>2</sup> contains benign and the most up-to-date common attacks, which resembles real-world data. We extracted HTTP trafic from it, including Web Attack, Infiltration, Botnet, and others.

• CICIoT2023 <sup>3</sup> is a novel and extensive IoT attack dataset to promote the development of security analytics applications in real IoT operations. The dataset contains a number of HTTP-based malicious attacks, including Recon, Web attack, DDoS, and others.

• Malware <sup>4</sup> is sourced from a prominent website specialized in malware, containing trafic captured from popular malware between 2021 and 2023. HTTP trafic packets are extracted from 30 diferent categories of malware, including Trickbot, Qakbot, Emotet, and others.

• APT is the trafic generated by real APT organizations independently collected by our research team. First, we extract malicious sample hashes from 5000 APT reports, which include data from 256 diferent APT groups. Then these hashes are used to obtain the original trafic generated by these sample hashes from open-source sandbox intelligence such as Virustotal [51] and Anyrun [3]. We get a total of 10 gigabytes of trafic and filter out the HTTP trafic. Since this dataset is taken from a real sandbox, it more accurately reflects realworld conditions than open-source datasets.

• Benign consists of benign trafic extracted from several of the datasets above, as well as trafic we decrypted from the 300 most popular websites listed in the Alexa Top rankings.

## C.2 Extended Dataset

The extended dataset is not involved in any model training or finetuning; it is solely used for testing purposes.

• CICAPT-IIoT2024 <sup>5</sup> is designed to provide cybersecurity researchers focusing on APT detection tasks with a comprehensive dataset specifically collected from an APT campaign in an Industrial Internet of Things (IIoT) environment. This dataset comprises a total of 19 APT groups, including well known organizations such as APT28, APT29, APT32, and others.

• APT2024 is a dataset we gathered from open-source sandbox environments, representing APT trafic data from the year 2024. This dataset consists of trafic patterns from 8 APT groups, such as Lazarus, Kimsuky, Bitter, and several others. These APT campaigns are critical for researchers aiming to enhance detection and mitigation strategies against advanced threats.

```python
Algorithm 1: HTTP Traffic Compliance
Input: HTTP traffic: http_traffic
Output: Validation result: is_valid, Errors: errors
1 errors ← []
2 parts ← Split http_traffic by "\r\n\r\n"
3 headers_part ← parts[0]
4 body_part ← if exists, parts[1]
5 headers_lines ← Split headers_part by "\r\n"
6 request_line ← headers_lines[0]
7 if Invalid request line format then
8    errors.append("Invalid request line")
9 foreach header in headers_lines[1:] do
10    if Invalid header format then
11    errors.append("Invalid header")
12 if Missing separating line between headers and body then
13    errors.append("Missing separator")
14 if errors is not empty then
15    return False, errors
16 return True, "Valid HTTP traffic"
```

## D Details of Target Models

## D.1 Image-based Detection Models

• MalTrafic [57] first maps trafic to grayscale images and trains it based on the CNN model.

• RBRN [70] learns the deep features of trafic through coding and relational networks and detects malicious trafic by calculating the similarity of trafic pairs.

• DeepMal [38] leverages a combination of CNN and LSTM, enabling better detection of malware trafic.

## D.2 Text-based Detection Models

• TextCNN [31] applies CNN to text data. It works by sliding convolution filters over word embeddings to detect text.

• DeepLog [17] is commonly used as an anomaly detection model in the cybersecurity field, and it uses LSTM-based deep learning to detect anomalous logs.

• BERT [15] is a transformer-based model designed specifically for NLP tasks and is advantageous for long text classi fication tasks.

## E HTTP Trafic Compliance

As shown in algorithm 1, we define the compliance for HTTP trafic based on the RFC document. In simple terms, HTTP trafic should consist of the following parts: (i) Request Line: Includes the method (e.g., GET, POST, HEAD), the request URI, and the HTTP version. (ii) Headers: Key-value pairs providing additional information about the request. (iii) Blank Line: Separates the headers from the body. (iv) Payload: Contains the data being sent. Through the above meth ods, we verify whether the generated trafic complies with the specifications. In addition, the generated HTTP trafic should remain functional. So we define something like the red part in Fig. 5 as unchangeable, and we force that part not to be changed.

## F Extra Experiments

## F.1 Adversarial Attacks against LLMs

As shown in Table 6, we conducted experiments using general purpose models, ChatGPT 3.5 and ChatGPTs, on APT and malware datasets. Due to the lack of fine-tuning, the F1-scores of both detection models were around 0.6. After generating adversarial samples with AdvTG, the ASR reached only 15%. LLMs possess stronger robustness than DL-based models, because of their better interpretability. In the future, it will be necessary to train detection models specifically based on LLMs rather than relying on generalpurpose models and to further verify the robustness of LLMs.

Table 6: Efectiveness of adversarial attacks against LLMbased detection models.

<table><tr><td>Detection Model</td><td>Datasets</td><td>P</td><td>R</td><td>F1</td><td>ASR</td></tr><tr><td rowspan="2">ChatGPT</td><td>Malware</td><td>0.71</td><td>0.54</td><td>0.61</td><td>16.35%</td></tr><tr><td>APT</td><td>0.89</td><td>0.42</td><td>0.57</td><td>16.64%</td></tr><tr><td rowspan="2">ChatGPTs</td><td>Malware</td><td>0.79</td><td>0.56</td><td>0.66</td><td>16.03%</td></tr><tr><td>APT</td><td>0.90</td><td>0.43</td><td>0.58</td><td>15.57%</td></tr></table>

![](images/541f8bbb42f80ac53dff12fd9bbd99ee9231866b15b618d5e5b25f42ac0d812e.jpg)  
Figure 7: Transferability of adversarial samples across Text-Based and Image-Based models.

## F.2 Transferability

We evaluate the transferability [44] of adversarial attacks by generating adversarial samples on image-based models and testing them on text-based models, and vice versa. As shown in Fig. 7, each heat map represents the attack success rates (ASR) across four datasets: CICIDS2017, CICIoT2023, Malware, and APT. The horizontal and vertical axes denote the target and test models, categorized into text-based and image-based models.

The diagonal values reflect the average ASR when adversarial samples are tested on the same type of model, while the of-diagonal values represent cross-modal transferability. The relatively high ASR values in the of-diagonal positions indicate that adversarial samples maintain efectiveness even when transferred to models with diferent feature extraction methods. This demonstrates that adversarial perturbations exhibit strong transferability across text and image modalities.

Table 7: The adversarial efectiveness of recent detection models.  
(a) CICIDS2017  
(b) CICIoT2023

<table><tr><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>R-T(0.05)</td><td>R-T(0.1)</td><td>R-T(0.2)</td><td>R-S</td><td>AdvTG</td><td>P</td><td>R</td><td>F1</td><td>R-T(0.05)</td><td>R-T(0.1)</td><td>R-T(0.2)</td><td>R-S</td><td>AdvTG</td></tr><tr><td>RoBERTa</td><td>0.99</td><td>1</td><td>0.99</td><td>8.17%</td><td>29.56%</td><td>48.86%</td><td>5.53%</td><td>58.26%</td><td>RoBERTa</td><td>0.99</td><td>1</td><td>0.99</td><td>8.34%</td><td>28.68%</td><td>50.30%</td><td>8.04%</td><td>69.69%</td></tr><tr><td>DistilBERT</td><td>0.99</td><td>1</td><td>0.99</td><td>8.21%</td><td>29.69%</td><td>49.19%</td><td>6.15%</td><td>59.05%</td><td>DistilBERT</td><td>0.99</td><td>1</td><td>0.99</td><td>8.98%</td><td>30.74%</td><td>50.42%</td><td>9.18%</td><td>68.68%</td></tr><tr><td>XLNet</td><td>0.99</td><td>0.99</td><td>0.99</td><td>8.43%</td><td>30.70%</td><td>49.05%</td><td>5.14%</td><td>56.37%</td><td>XLNet</td><td>0.99</td><td>0.99</td><td>0.99</td><td>8.65%</td><td>30.45%</td><td>48.81%</td><td>7.37%</td><td>68.90%</td></tr><tr><td colspan="9">(c)Malware</td><td colspan="9">(d)APT</td></tr><tr><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td><td rowspan="2">DLClassifier</td><td colspan="3">Detection</td><td colspan="5">Attack (ASR)-higher is better</td></tr><tr><td>P</td><td>R</td><td>F1</td><td>R-T(0.05)</td><td>R-T(0.1)</td><td>R-T(0.2)</td><td>R-S</td><td>AdvTG</td><td>P</td><td>R</td><td>F1</td><td>R-T(0.05)</td><td>P</td><td>R-T(0.1)</td><td>R-T(0.2)</td><td>R-S</td></tr><tr><td>RoBERTa</td><td>0.99</td><td>0.99</td><td>0.99</td><td>7.56%</td><td>27.87%</td><td>45.76%</td><td>8.58%</td><td>50.78%</td><td>RoBERTa</td><td>0.99</td><td>0.99</td><td>0.99</td><td>7.33%</td><td>28.15%</td><td>47.89%</td><td>7.49%</td><td>67.33%</td></tr><tr><td>DistilBERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>8.74%</td><td>25.42%</td><td>45.90%</td><td>7.41%</td><td>51.56%</td><td>DistilBERT</td><td>0.99</td><td>0.99</td><td>0.99</td><td>7.46%</td><td>25.46%</td><td>48.61%</td><td>9.15%</td><td>66.55%</td></tr><tr><td>XLNet</td><td>0.98</td><td>0.96</td><td>0.97</td><td>7.83%</td><td>27.93%</td><td>46.72%</td><td>7.11%</td><td>52.34%</td><td>XLNet</td><td>0.99</td><td>0.99</td><td>0.99</td><td>7.85%</td><td>28.56%</td><td>49.27%</td><td>7.26%</td><td>69.34%</td></tr></table>

## F.3 New Baseline

We further introduce recent baseline models for both malicious traf fic detection and adversarial attack generation. This helps to provide a more robust and comprehensive assessment of our method. In addition to the existing detection models, we incorporate three advanced transformer-based architectures: RoBERTa, DistilBERT, and XLNet [36, 48, 62]. These models are adapted for malicious trafic detection by fine-tuning network trafic, leveraging their strong feature extraction and classification capabilities. For adversarial attack generation, we introduce RobTest (R-T)[10], a novel framework designed to craft adversarial samples that target deep learning-based detection models.

As shown in Table 7, AdvTG significantly outperforms R-T across all datasets and detection models. These results highlight the superior efectiveness of AdvTG in generating transferable adversarial samples. The perturbation thresholds for R-T are set to 0.05, 0.1, and 0.2, with higher thresholds leading to slower generation speeds. Although R-T achieves reasonable ASR at the 0.2 threshold, its efficiency is significantly lower, with generation speed only about one-tenth of AdvTG. Overall, AdvTG outperforms R-T in both ASR and eficiency across all datasets and models.
# Beyond Single Tabs: A Transformative Few-Shot Approach to Multi-Tab Website Fingerprinting Atacks

Wenwen Meng Nanjing University of Science and Technology Nanjing, Jiangsu, China mengwenwen@njust.edu.cn

Chunpeng Ge Shandong University and Quan Cheng Laboratory Jinan, Shandong, China chunpeng\_ge@sdu.edu.cn

Chuan Ma<sup>∗</sup> Chongqing University Chongqing, China chuan.ma@cqu.edu.cn

Yuwen Qian Nanjing University of Science and Technology Nanjing, Jiangsu, China admon@njust.edu.cn

Ming Ding Data 61, CSIRO, Sydney Sydney, Australia ming.ding@data61.csiro.au

Tao Xiang Chongqing University Chongqing, China txiang@cqu.edu.cn

## Abstract

Website Fingerprinting (WF) attacks allow passive eavesdroppers to deduce the websites a user visits by analyzing encrypted trafic, threatening user privacy. While current WF attacks achieve high ac curacy, they typically assume single-tab browsing, which is unrealis tic as users often open multiple tabs, creating mixed trafic. Existing multi-tab WF approaches require large datasets and frequent retraining due to evolving website content, limiting their practicality. In this paper, we introduce Few-shot Multi-tab Website Fingerprint ing (FMWF), a novel approach designed to address the limitations of existing multi-tab WF attacks. FMWF directly tackles the chal lenges of mixed, overlapping trafic traces generated from multi-tab browsing, leveraging two key innovations: (1) an advanced data augmentation technique that synthesizes realistic multi-tab trafic sequences from easily collected single-tab traces, thereby dramati cally reducing the need for large-scale real-world trafic data; and (2) a powerful fine-tuning algorithm based on transfer learning that adapts pre-trained models to new, multi-tab environments with minimal additional data. This two-stage framework enables FMWF to capture the complex efectively, overlapping trafic patterns in herent in multi-tab browsing while maintaining a high level of flexibility and significantly lowering computational and data collec tion burdens. Our experiments, conducted using real trafic traces collected from three widely-used browsers—Microsoft Edge, Google Chrome, and Tor Browser—highlight the superior performance of FMWF in both closed-world and open-world scenarios. Notably,

<sup>∗</sup>Corresponding author

FMWF achieves a minimum 12.3% improvement in accuracy compared to ARES (SP’23) [7], TMWF (CCS’23) [13], and BAPM (AC-SAC’21) [10] in the open-world scenario. The code with related datasets is available at https://github.com/WW-Meng/FMWF.

## CCS Concepts

• Security and privacy → Privacy-preserving protocols; • Networks → Network privacy and anonymity.

## Keywords

Multi-tab Website fingerprinting, Few-shot learning, Deep learning, Tor

## ACM Reference Format:

Wenwen Meng, Chuan Ma, Ming Ding, Chunpeng Ge, Yuwen Qian, and Tao Xiang. 2025. Beyond Single Tabs: A Transformative Few-Shot Approach to Multi-Tab Website Fingerprinting Attacks. In Proceedings of the ACM Web Conference 2025 (WWW ’25), April 28-May 2, 2025, Sydney, NSW, Australia. ACM, New York, NY, USA, 10 pages. https://doi.org/10.1145/3696410.3714811

## 1 INTRODUCTION

As the internet continues to evolve and permeate daily activities such as online shopping, emailing, and social networking, browsers have become essential tools [12]. With this increased reliance, user concerns about privacy have also intensified. When a client accesses a website, routers along the communication path can observe or collect browsing data, potentially leading to privacy breaches for commercial exploitation or surveillance [17, 28, 33]. To safeguard privacy, users often obscure their online activity, with Tor [6] being the most popular anonymous network. Tor enhances privacy by rerouting data through multiple nodes, frequently changing IP addresses, and applying layered encryption to trafic, thereby thwarting trafic tracking eforts. Despite the privacy protections ofered by networks like Tor, trafic analysis techniques, such as Website Fingerprinting (WF) attacks [3, 6, 23], can still deduce the websites that Tor users visit by scrutinizing trafic patterns, including packet size, transmission direction, and timing intervals.

WF attacks leverage Machine Learning (ML) and Deep Learning (DL) models to extract distinct trafic patterns from websites’ traces, with state-of-the-art DL-based methods [1, 11, 18, 20, 21, 27] achieving outstanding accuracy, often exceeding 95%, in identifying the websites users visit. However, these attacks frequently operate un der the single-page assumption, which presumes that users browse only one webpage per session. In reality, browsing habits often involve opening multiple tabs in rapid succession [8, 25], creating mixed and overlapping trafic patterns that are more dificult to distinguish. Research has shown that traditional WF attacks sufer from significant performance degradation in such multi-tab scenar ios [14], which has spurred the development of new multi-tab WF techniques aimed at addressing this challenge.

Most existing multi-tab WF attacks [5, 29, 31, 32] adhere to a common architecture that segments browsing sessions into isolated trafic chunks associated with individual websites. However, this approach faces several critical drawbacks. First, these methods presuppose knowledge of the number of opened tabs, as exemplified by [31], which is designed for a fixed 2-tab setting. This assumption leads to significant performance degradation when the number of tabs is unknown or fluctuates dynamically—conditions that better reflect real-world browsing behaviors. Second, even un der controlled conditions, these models are highly susceptible to WF defense mechanisms such as trafic padding and packet delays, both of which substantially reduce their accuracy [32]. Lastly, their performance worsens as the number of open tabs increases, making it more challenging to extract clean and distinct trafic chunks from the increasingly mixed trafic streams. The noise introduced by overlapping trafic becomes more pronounced, ultimately resulting in a notable decline in identification accuracy.

In response to these challenges, more recent multi-tab WF attack methods [7, 10, 13] have been designed to address the limitations introduced by overlapping trafic traces specifically. These cutting edge approaches, often employing Transformer-based architectures, achieve high website identification accuracy but at a high cost—they require vast amounts of multi-tab trafic data for training. The dy namic nature of websites further complicates this, as trafic patterns frequently change with content updates, making it dificult to keep these models up-to-date. Research [13, 20] has shown that models trained on trafic data collected just two weeks prior can experience a sharp drop in accuracy due to outdated patterns. This necessitates the constant collection of fresh, large-scale multi-tab trafic data, which is both costly and increases the risk of exposure. These limitations prompt an essential research question: Can we devise a simplified, yet efective approach to conduct multi-tab website fingerprinting attacks that eliminates the need for prior knowledge of tab counts and large-scale training data?

Therefore, in this paper, we introduce a novel approach to multi tab website fingerprinting attacks that leverages transfer learning to overcome the limitations of existing methods. Unlike previous approaches, our method eliminates the need for complex trafic segmentation and extensive multi-tab trafic data collection, significantly reducing the bootstrapping time for WF attacks and enhancing feasibility in real-world scenarios. Our approach consists of two key stages:

(1) Pre-training with Augmented Trafic Sequences: We employ a carefully designed data augmentation method to synthesize a multi-tab dataset from single-tab trafic traces, enabling the model to build efective feature extractors and classifiers. By artificially combining trafic from individual websites into multi-tab trafic sequences, this stage reduces the dependency on large-scale real-world multi-tab datasets while still capturing essential trafic patterns for multi-tab environments.

(2) Few-shot fine-tuning: We adapt the pre-trained model from the previous stage to real-world conditions by finetuning it using a small amount of real-world multi-tab trafic data. This allows the model to further adjust to the overlapping and mixed nature of multi-tab trafic traces without requiring vast amounts of fresh data collection. Through transfer learning, this few-shot approach enables the model to achieve high accuracy and generalization in multi-tab WF attacks, even in dynamic or changing trafic environments.

This two-stage framework not only enables our model to efectively handle mixed and overlapping trafic from multiple tabs but also eliminates the need for prior knowledge of the number of open tabs, a common assumption in previous studies.

The main contributions of this paper are as follows:

• To the best of our knowledge, we propose the first few-shot multi-tab WF attack method named FMWF. By utilizing a novel data augmentation method specifically designed for multi-tab website fingerprinting attacks, FMWF removes the need for a large number of real-world multi-tab trafic traces.

• In the few-shot scenario, we move away from using large models, such as Transformers, which are typically resourceintensive and data-hungry. Instead, we implement lightweight neural networks as feature extractors and classifiers, which, through a well-crafted fine-tuning transfer learning algorithm, are capable of achieving competitive performance. This approach significantly reduces the model complexity while maintaining accuracy, making it more eficient and practical for real-world applications where data and computational resources are limited.

• To demonstrate the robust performance of our model, we conduct comprehensive tests on Tor, Microsoft Edge, and Google Chrome datasets. On the Tor dataset, it achieves a top-k accuracy of 0.910 in the 5-tab setting using just 25- shot learning samples per label. On the Microsoft Edge and Google Chrome datasets, which include rich features such as packet sizes, FMWF reaches a top-k accuracy of 0.885 in the 5-tab setting with only 3-shot learning samples per label.

• In the more challenging open-world scenario, we observe a remarkable minimum improvement of 12.3% compared to ARES (SP’23) [7], TMWF (CCS’23) [13], and BAPM (AC-SAC’21) [10] when testing on non-monitored websites.

## 2 BACKGROUND

## 2.1 Threat Model

Our threat model involves a passive adversary capable of observing encrypted network trafic, similar to previous WF attack studies [7, 10, 12, 13, 21, 30]. As shown in Figure 1, users access websites through anonymous systems like Tor, which safeguard privacy via multi-layer encryption and relay nodes. The attacker, potentially an ISP or a device between the ISP and the first Tor node, passively monitors trafic without altering it, unlike active attackers who can delay or drop packets. Though unable to modify the trafic, the adversary observes encrypted packet metadata (size, direction, timing) to infer the websites visited by the user. Using machine learning models trained on trafic patterns, the attacker can associate observed trafic with specific websites, even in multi-tab browsing scenarios where trafic from multiple websites may intermingle within a session.

![](images/82a9a4948c88dab87371fd31fe3e77dda45a95419faa5988e29e1b380ef01b4a.jpg)  
Figure 1: Threat model of FMWF.

## 2.2 Single-tab WF Attacks

Deep-learning-based WF: Deep learning was first applied to web site fingerprinting attacks on Tor by Abe et al. [1], who utilized stacked auto-encoders, achieving results comparable to traditional feature extraction methods on simple direction sequences. This marked a shift from manually crafted features to automated feature extraction, with the performance of deep learning models improving as more complex network structures were introduced.

Rimmer et al. [20] demonstrated that deep learning models are robust against changes in website content, showcasing the feasibility of automated feature learning in WF attacks. Building on this, Siri nam et al. [21] proposed the convolutional neural network (CNN) model Deep Fingerprinting (DF), specifically designed for WF attacks. DF improved the model’s ability to capture subtle patterns in encrypted trafic by incorporating multiple advanced convolutional blocks, achieving an accuracy of 98.3% in a closed-world scenario and establishing CNNs as powerful tools for WF attacks. Following this, Bhat et al. [2] introduced Var-CNN, a framework that combines semi-automated feature extraction and demonstrated better perfor mance with smaller datasets, addressing the common bottleneck of deep learning models that typically require large amounts of labeled data.

Transfer-learning-based WF: Supervised learning methods [4, 34] often require extensive labeled data, which is time-consuming and costly. Transfer learning [24, 35] provides a solution by lever aging previously learned knowledge for new tasks. In recent WF attacks [22, 26, 30], transfer learning has been applied in few-shot learning scenarios. This typically involves pre-training on a dataset with abundant labeled data, fine-tuning with limited samples, and testing.

Recent works, such as Triplet Fingerprinting (TF) [22], Adaptive Fingerprinting (AF) [26], and Contrastive Fingerprinting (CF) [30], aim to refine feature extraction for few-shot scenarios. CF integrates contrastive learning and data augmentation for a more eficient WF attack, improving representation quality and training eficiency. TF enhances feature distinction through a triplet network, while AF employs adversarial domain adaptation to learn domain-invariant features. However, the efectiveness of these WF attacks relies on the strong assumption that only a single website is visited during a browsing session, a scenario that does not always hold as users often open multiple websites simultaneously or within a short period [9, 14, 29, 31].

## 2.3 Multi-tab WF Attacks

Recent studies have begun to address the challenges associated with multi-tab website fingerprinting (WF) attacks, aiming to improve website identification accuracy in complex mixed-trafic scenarios. Notably, models such as Transformer-based Multi-tab Website Fingerprinting [7, 10, 13] have introduced innovative strategies to efectively handle overlapping and mixed trafic segments. These approaches frame multi-tab browsing as either a multi-label classification task or a sequence prediction problem, utilizing advanced neural network architectures like transformers. By doing so, these models can extract both local and global trafic patterns from the data, thereby enhancing the accuracy of website identification in scenarios where multiple tabs are open simultaneously.

These advancements represent a significant step forward in the field of WF, yet they also reveal inherent challenges. The reliance on large amounts of labeled data and the assumption of static tab counts in existing models limit their practical application, particularly in dynamic real-world environments. As user behavior becomes increasingly complex, the need for robust and adaptable models that can generalize across varying trafic conditions and tab configurations becomes paramount.

We propose the Few-shot Multi-tab Website Fingerprinting attack (FMWF), which leverages transfer learning and data augmentation to achieve high identification accuracy with minimal training data. This eliminates the need for extensive data collection and constant retraining. FMWF handles complex, overlapping trafic traces without relying on prior knowledge of tab counts, making it highly flexible and practical in real-world settings, while also reducing computational demands and data requirements typically seen in multi-tab WF models.

## 3 METHOD

In this section, we present the detailed structure and the workflow of FMWF. Before delving into the various components of FMWF, we first provide an overview of the framework.

## 3.1 Overview

Previous Transformer-based multi-tab WF attacks have achieved high website identification accuracy by utilizing extensive multitab trafic traces. However, the characteristics of website trafic can fluctuate due to variations in website content and user network conditions. Maintaining high attack accuracy often necessitates the frequent collection of substantial amounts of new trafic traces to retrain the attack model. This process can be both costly and impractical, posing significant challenges to the real-world applicability of website fingerprinting attacks.

To address the limitations of existing multi-tab WF attacks, we propose FMWF, a novel multi-tab website fingerprinting attack method based on transfer learning that is efective in few-shot scenarios. As illustrated in Figure 2, the FMWF attack consists of two main stages with a testing phase:

![](images/d3436eac3f86adeb212498b91588bf02ac4a847a39d65e45b6a452692d3dc7c0.jpg)  
Figure 2: Our lightweight WF attack, FMWF, consists of two key components: a feature extractor and a classifier, both built using lightweight neural networks. These components work in tandem with a fine-tuning algorithm derived from transfer learning, enabling eficient and accurate multi-tab website fingerprinting with minimal training data.

(1) Pre-training with Augmented Trafic Sequences: In the pre-training stage, we introduce a novel data augmentation method to simulate the behavior of users accessing multiple websites simultaneously. This method generates synthetic multi-tab browsing sessions by combining individual trafic patterns from various websites, allowing FMWF to learn critical features related to multi-tab trafic traces. The pre training stage leverages the knowledge obtained from syn thetic data to enhance the model’s ability to recognize and classify real-world multi-tab trafic eficiently.

(2) Few-shot Fine-tuning for Real-world Adaptation: After pre-training, the model enters the fine-tuning stage, adapting to real-world multi-tab trafic using few-shot labeled data. This fine-tuning process refines the learned features, adjusting the model to handle real-world complex, mixed trafic patterns typical of multi-tab browsing sessions. By fo cusing on a few-shot learning method, this stage enables the model to generalize to real-world multi-tab quickly and dy namically changing trafic environments, without requiring continuous large-scale retraining.

(3) Testing on Dynamic Trafic: Once fine-tuned, FMWF is evaluated on diverse datasets to assess its performance in close and open-world scenarios.

## 3.2 Pre-training with Augmented Trafic Sequences

In the pre-training stage of the attack model, three main components are involved: the pre-training dataset, the feature extractor, and the classifier.

Pre-training dataset. For the pre-training dataset, we propose a data augmentation method. Instead of collecting multi-tab trafic traces directly from the real world, we manually synthesize a multitab dataset by combining single-tab trafic sequences. This method achieves data augmentation and mitigates the challenges associated with collecting multi-tab datasets.

![](images/bfab869c66758b56ecfaf581810704d3de6cab57e174fea78c198d41902ea36e.jpg)  
Figure 3: Three basic situations of 2-tab trafic traces. Depending on whether a user accesses Site B via a new tab before Site A finishes loading, 2-tab trafic patterns can be categorized into these three types.

Collecting multi-tab datasets is more challenging than single-tab datasets due to the exponential increase in the size of the label set. For example, monitoring one hundred websites generates over four thousand labels for two-tab trafic, making it dificult for an attacker to gather and frequently update a large-scale dataset. However, one can easily generate large-scale datasets by manually synthesizing multi-tab trafic sequences. This data augmentation strategy enables the pre-training of attack models on multi-tab trafic without the need to collect real-world multi-tab datasets.

In [29], multi-tab trafic traces are categorized into three fundamental types based on their time interval relationships: positive, zero, and negative. Figure 3 illustrates these scenarios for 2-tab trafic traces. As shown in Figure 4, to ensure a complete characterization of each website’s trafic, we manually synthesize multi-tab trafic traces specifically using the zero time interval type. This strategy allows the feature extractor to more efectively learn the trafic characteristics of each website, leading to a more robust pre trained attack model. Additionally, we employ all three types of time intervals for data augmentation, rather than limiting the exper iments to only the zero-time interval type. A detailed experimental analysis is provided in Appendix A.

Specifically, let (�, �) represent a trafic instance generated by a user browsing websites, where � is the trafic sequence consisting of � packets, and � is the label indicator vector for that instance. We use multi-hot encoding to represent the label vector, denoted as $y = [ y _ { 0 } , y _ { 1 } , \dotsc , y _ { 9 9 } ]$ . If the user visits the �-th and �-th websites among the 100 monitored websites, �� and �<sub>�</sub> are set to 1, while all other label positions are set to 0. In the pre-training dataset, we concatenate the single-tab trafic sequences generated by a user vis iting websites � and � separately to form a multi-tab trafic sequence, $\tilde { t } = A u g ( t _ { i } , t _ { j } )$ . This allows us to obtain a manually synthesized instance (�,˜ �˜), where the augmented instance shares the same label as a real-world instance, i.e., $\tilde { y } = y .$

![](images/eb165ebc9bc40be4ee485b36f7d4ff05b25b6d7737f6ed89d31c8f8edbbbfa73.jpg)  
Figure 4: Manually Synthesized Multi-Label Trafic Traces from sing-table sessions for the Pre-Training Stage.

Feature extractor and Classifier. The FMWF attack model employs a specialized feature extractor and classifier to tackle critical challenges in multi-tab website fingerprinting. The feature extrac tor is built upon a convolutional neural network (CNN) architecture that efectively addresses noise reduction from overlapping traffic segments [21], [19], adapts to dynamic website trafic patterns and maintains flexibility in processing variable-length input sequences. Key techniques such as batch normalization and dropout are utilized to enhance the robustness of feature representations and prevent overfitting, ensuring that the model can accurately capture the relevant characteristics of user browsing behavior even when the number of open tabs varies.

The classifier, a multi-layer perceptron (MLP), operates on the feature embeddings generated by the extractor to predict the labels of visited websites. It incorporates a weighted loss function to mitigate data imbalance in few-shot learning scenarios, ensuring that underrepresented classes are adequately represented in the model’s predictions. Designed for real-time processing eficiency, the classifier utilizes fully connected layers combined with batch normalization and ReLU activations, concluding with a softmax layer for probability distribution over potential labels. Together, these components of the FMWF model enhance its accuracy and robustness and can be quickly adapted to real-world datasets during the fine-tuning phase of the few-shot classification task.

## 3.3 Few-shot Fine-tuning for Real-world Adaptation

During the fine-tuning stage of the FMWF model, we leverage a support set derived from real-world multi-tab trafic to enhance the feature extractor and classifier. The primary aim of this process is to improve the model’s accuracy in identifying labels corresponding to actual user trafic patterns. As highlighted in previous research [16], fine-tuning algorithms have demonstrated significant eficacy in transfer learning, allowing models to adapt quickly to new data.

One of the key challenges in feature extraction for multi-tab traffic is the blending of trafic from various websites, which introduces substantial noise that can obscure the unique characteristics of individual sites. To address this, we initiate fine-tuning by feeding a limited number of real-world multi-tab trafic sequences into the pre-trained feature extractor. This generates robust feature embeddings that encapsulate the trafic patterns of each website. These embeddings serve as input for the multi-layer perceptron (MLP) classifier, which is then fine-tuned to enhance its predictive performance before being tested with the query set. This two-step process ensures that the FMWF model remains adaptable and efective, even in the dynamic environment of real-world web trafic.

## 3.4 Testing on Dynamic Trafic

In the testing phase of the Few-shot Multi-tab Website Fingerprinting (FMWF) model, we utilize a query set designed for a k-way 1-shot scenario, meaning it consists of k distinct labels, each represented by only a single sample. The testing process involves analyzing unlabeled multi-tab trafic traces captured from anonymous networks, such as Tor, as well as from mainstream browsers like Microsoft Edge and Google Chrome.

## 3.5 Algorithm Summary

FMWF presents a groundbreaking approach to multi-tab website fingerprinting by utilizing transfer learning and few-shot fine-tuning. This method efectively overcomes the limitations of traditional WF techniques that either assume single-tab browsing or require extensive collections of real-world multi-tab trafic traces. Instead of relying on large-scale datasets and frequent retraining, FMWF synthesizes multi-tab trafic sequences through data augmentation during the pre-training phase, enabling the model to capture essential trafic features from artificially combined single-tab traces.

The architecture of FMWF incorporates a streamlined design, utilizing a CNN as the feature extractor and an MLP for classification. This innovative integration of synthetic data generation and few-shot fine-tuning enhances the model’s eficiency and adaptability in dynamic real-world scenarios. By establishing a robust and practical solution for multi-tab WF attacks, FMWF demonstrates significant advancements in accuracy and operational feasibility, making it a valuable contribution to website fingerprinting.

## 4 EXPERIMENTAL EVALUATIONS

In this section, we conduct comprehensive experiments on realworld multi-tab datasets to address the following research questions regarding FMWF:

![](images/ea51b185b70109c589bed984ac9fc3412ede0a11bd2b5cbbe47e7b21a00c696f.jpg)  
(a) 2-tab setting (A@2)

![](images/4f080e687d05778c1131ffb34d70e8fe2bb9601a1a17a9a338e553e212043cc2.jpg)  
(b) 3-tab setting (A@3)

![](images/b68552cc85d1cbbff816d9e7285608a547905d5ad5e19a598fedc97920cb8da6.jpg)  
(c) 4-tab setting (A@4)

![](images/840a9cdec052cf5a46838f94bbe7475e96c946cbb87b72dcef1f41d41e1a5205.jpg)  
(d) 5-tab setting (A@5)  
Figure 5: Comparison of FMWF with state-of-the-art multi-tab WF attacks, where A@K represents the top-k Accuracy.

• RQ I: How does the number of fine-tuning traces � influence top-K accuracy (A@K), Precision, Recall, and F1-Score across diferent tab settings in few-shot multi-tab scenarios compared to state-of-the-art models?

• RQ II: How efective is FMWF in real-world scenarios with out prior knowledge of the number of opened tabs?

• RQ III: How does the number of labels (�) during the fewshot fine-tuning stage influence the generalization perfor mance of FMWF in multi-tab classification tasks?

• RQ IV: How does FMWF perform on diverse browser datasets (Google Chrome and Microsoft Edge), especially with limited fine-tuning samples per label?

• RQ V: How efective is FMWF in the open-world scenario?

## 4.1 Experiment Setup

4.1.1 Dataset. In this study, we collected three datasets by using three major browsers to access target websites and capture trafic data: the Tor browser, Microsoft Edge, and Google Chrome.

Tor Dataset. Using the method outlined in [7], we collected Tor trafic data over two months, leveraging 15 Alibaba Cloud servers with varying hardware configurations, located across the US and Singapore. This setup allowed us to simulate diferent user scenarios, incorporating variations in device performance, network conditions, and periods. Based on the website trafic rankings<sup>1</sup>, we selected the top 100 most popular URLs. For each site, we collected 100 single-tab trafic samples by repeatedly accessing these websites via the Tor Browser. To collect multi-tab datasets, we randomly combined these 100 websites to generate 2-tab, 3-tab, 4-tab, and 5-tab scenarios, also using the Tor Browser. In the open-world scenario, we used the Tor open-world dataset provided by [7].

Microsoft Edge & Google Chrome Dataset. We adopted a dataset collection method similar to previous research [12]. Trafic data was captured using Tshark, while Python and PyAutoGUI were employed for automation. Using these two major browsers, we collected trafic data by repeatedly accessing 100 monitored websites <sup>2</sup>, capturing 50 trafic samples per website. We randomly combined the 100 target websites to collect 2-tab, 3-tab, 4-tab, and 5-tab datasets.

4.1.2 Metrics. To evaluate the performance of our multi-tab WF attack, we adopt the metrics commonly used in related studies [7, 15]. In the closed-world scenario, multi-tab WF attacks are framed as a multi-tab multi-class classification problem. For this, we employ the multi-tab-specific metric, Top-k Accuracy (A@K), and traditional multi-class metrics such as Precision, Recall, and F1-score. These metrics comprehensively evaluate the model’s performance by assessing the prediction outcomes for each website across all instances.

In the open-world scenario, we assess the proposed method by following established practices from previous studies [20, 21]. In this context, all non-monitored websites are aggregated into a single category, enabling us to evaluate the model’s performance in accurately identifying the websites a user visits, even amidst a vast array of potentially unseen sites. This approach not only tests the adaptability and robustness of FMWF but also reflects more realistic browsing conditions, where users interact with a mix of known and unknown websites. We present the details of the metrics in Appendix A.

## 4.2 Closed-world Evaluation

In the closed-world scenario, we selected the current state-of-the-art end-to-end multi-tab website fingerprinting attack methods, ARES (SP’23) [7], TMWF (CCS’23) [13], and BAPM (ACSAC’21) [10], as comparative methods for evaluating the FMWF attack model in the following experiments. To assess the robustness ofFMWF, we tested it using datasets collected from three mainstream browsers—Google Chrome, Microsoft Edge, and Tor Browser. We used 5 diferent validation sets for each experiment and calculated the average as the final result. Except for Experiment AQ IV, all other experiments were conducted using the Tor dataset.

AQ I-1: Evaluating the Influence of � on Top-K Accuracy (A@K) Performance. In this experiment, we investigate the impact of varying the number of fine-tuning traces (�) per label on the performance of our multi-tab WF attack model across diferent tab settings during the few-shot fine-tuning stage. We conduct experiments using a 100-way �-shot fine-tuning dataset, where �=10,15,20,25,30,35,40. The primary evaluation metric is A@K, which is widely used in similar studies [7, 15], to assess the model’s generalization capability in multi-tab browsing scenarios. A@K measures the model’s ability to correctly identify the actual visited websites within the top K predictions.

Table 1: Comparison of FMWF with prior arts in Precision, Recall, and F1-Score across diferent tabs and sample numbers (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="3">2-tab</td><td colspan="3">3-tab</td><td colspan="3">4-tab</td><td colspan="3">5-tab</td></tr><tr><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">BAPM (ACSAC&#x27;21)</td><td>10</td><td>0.605</td><td>0.730</td><td>0.634</td><td>0.571</td><td>0.647</td><td>0.587</td><td>0.538</td><td>0.668</td><td>0.582</td><td>0.431</td><td>0.560</td><td>0.476</td></tr><tr><td>20</td><td>0.691</td><td>0.805</td><td>0.727</td><td>0.688</td><td>0.760</td><td>0.711</td><td>0.648</td><td>0.770</td><td>0.692</td><td>0.634</td><td>0.686</td><td>0.645</td></tr><tr><td>30</td><td>0.734</td><td>0.800</td><td>0.746</td><td>0.749</td><td>0.790</td><td>0.746</td><td>0.695</td><td>0.808</td><td>0.737</td><td>0.679</td><td>0.760</td><td>0.710</td></tr><tr><td>40</td><td>0.738</td><td>0.825</td><td>0.761</td><td>0.749</td><td>0.820</td><td>0.774</td><td>0.736</td><td>0.793</td><td>0.746</td><td>0.797</td><td>0.848</td><td>0.813</td></tr><tr><td rowspan="4">TMWF (CCS&#x27;23)</td><td>10</td><td>0.676</td><td>0.725</td><td>0.684</td><td>0.528</td><td>0.493</td><td>0.573</td><td>0.471</td><td>0.493</td><td>0.469</td><td>0.605</td><td>0.656</td><td>0.623</td></tr><tr><td>20</td><td>0.783</td><td>0.775</td><td>0.770</td><td>0.647</td><td>0.717</td><td>0.665</td><td>0.612</td><td>0.623</td><td>0.597</td><td>0.702</td><td>0.768</td><td>0.726</td></tr><tr><td>30</td><td>0.820</td><td>0.835</td><td>0.818</td><td>0.708</td><td>0.780</td><td>0.729</td><td>0.687</td><td>0.760</td><td>0.710</td><td>0.806</td><td>0.862</td><td>0.826</td></tr><tr><td>40</td><td>0.838</td><td>0.860</td><td>0.844</td><td>0.706</td><td>0.763</td><td>0.714</td><td>0.702</td><td>0.818</td><td>0.747</td><td>0.830</td><td>0.880</td><td>0.849</td></tr><tr><td rowspan="4">AERS (SP&#x27;23)</td><td>10</td><td>0.857</td><td>0.805</td><td>0.812</td><td>0.776</td><td>0.720</td><td>0.727</td><td>0.855</td><td>0.793</td><td>0.811</td><td>0.837</td><td>0.778</td><td>0.790</td></tr><tr><td>20</td><td>0.865</td><td>0.855</td><td>0.847</td><td>0.873</td><td>0.827</td><td>0.832</td><td>0.909</td><td>0.883</td><td>0.890</td><td>0.926</td><td>0.890</td><td>0.902</td></tr><tr><td>30</td><td>0.887</td><td>0.885</td><td>0.880</td><td>0.898</td><td>0.877</td><td>0.877</td><td>0.928</td><td>0.903</td><td>0.911</td><td>0.928</td><td>0.904</td><td>0.908</td></tr><tr><td>40</td><td>0.903</td><td>0.880</td><td>0.884</td><td>0.935</td><td>0.897</td><td>0.905</td><td>0.934</td><td>0.908</td><td>0.912</td><td>0.921</td><td>0.918</td><td>0.918</td></tr><tr><td rowspan="4">FMWF (Ours)</td><td>10</td><td>0.885</td><td>0.800</td><td>0.794</td><td>0.779</td><td>0.725</td><td>0.724</td><td>0.890</td><td>0.770</td><td>0.775</td><td>0.849</td><td>0.740</td><td>0.757</td></tr><tr><td>20</td><td>0.883</td><td>0.865</td><td>0.849</td><td>0.867</td><td>0.840</td><td>0.835</td><td>0.930</td><td>0.893</td><td>0.889</td><td>0.929</td><td>0.892</td><td>0.894</td></tr><tr><td>30</td><td>0.894</td><td>0.896</td><td>0.879</td><td>0.893</td><td>0.881</td><td>0.875</td><td>0.935</td><td>0.918</td><td>0.909</td><td>0.927</td><td>0.908</td><td>0.912</td></tr><tr><td>40</td><td>0.916</td><td>0.920</td><td>0.904</td><td>0.902</td><td>0.926</td><td>0.909</td><td>0.928</td><td>0.920</td><td>0.914</td><td>0.925</td><td>0.920</td><td>0.915</td></tr></table>

Benefits from the fine-tuning algorithm, our lightweight WF attack model demonstrates strong competitiveness against current state-of-the-art Transformer-based large WF attack models. As illustrated in Figure 5, FMWF consistently surpasses the advanced models (TMWF and BAPM) across all tab settings. For instance, in the 2-tab scenario, when �=20, the A@2 score of FMWF exceeds 0.8, significantly outperforming TMWF and BAPM, whose A@2 scores remain below 0.70. This trend continues in the 3-tab and 4-tab settings, where FMWF sustains a clear advantage in top-k accuracy. While ARES, a state-of-the-art multi-tab WF attack model based on a sophisticated transformer architecture, performs closely to FMWF due to its ability to capture trafic fea tures from pre-trained datasets, FMWF remains competitive with its lightweight model structure. As � increases, A@K scores remain consistently high, showcasing FMWF’s robustness in handling com plex multi-tab scenarios, all while leveraging few-shot learning to maintain strong identification accuracy even in the most challeng ing multi-tab environments.

AQ I-2: Impact of �, the Number of Fine-Tuning Traces on Precision, Recall, and F1-Score Across Varying Numbers of Tabs in the Few-Shot Fine-Tuning Stage. As shown in Table 1, FMWF consistently surpasses other state-of-the-art multi-tab WF attacks across most configurations in terms of Precision, Recall, and F1-Score. For instance, in the 100-way 40-shot setting, FMWF attains an impressive F1-Score of 0.904 in the 2-tab scenario, substantially outperforming BAPM and TMWF, which achieve F1-Scores of 0.744 and 0.751, respectively. This trend continues in the 3-tab and 4-tab settings, where FMWF maintains superior and stable results.

Additionally, FMWF demonstrates exceptional stability as the number of shots increases, ensuring consistent performance across various scenarios. For example, even with just 30 fine-tuning traces per label in the 5-tab scenario, FMWF achieves an F1-Score of 0.912, outperforming ARES (0.908), BAPM (0.710), and TMWF (0.826). This consistency is observed across all tab settings and shot numbers, underscoring FMWF’s robustness in navigating complex multi-tab environments with limited fine-tuning data.

AQ II: Evaluating the Performance ofFMWF Without Prior Knowledge of the Number of Tabs. We further evaluate the performance of FMWF in a scenario where the number of opened tabs is unknown to the adversary. We tested using a dataset with an equal proportion mixture of 2-tab, 3-tab, 4-tab, and 5-tab trafic traces. This dynamic setting is more practical and challenging as it simulates real-world browsing behavior where users may open multiple tabs simultaneously without revealing the exact number of tabs. To assess the performance of our model under these conditions, we use Precision, Recall, and F1-score metrics, as shown in Table 2 FMWF demonstrates strong performance across all values of �. For instance, with �=25, it achieves a Precision of 0.877, Recall of 0.849, and F1-score of 0.835. Notably, the model exhibits consistent and robust performance as � increases, indicating that FMWF can efectively handle multi-tab trafic even without prior knowledge of the number of tabs. This showcases the adaptability and efectiveness of FMWF in real-world browsing environments.

Table 2: Performance of FMWF without prior knowledge of the number of tabs, across sample numbers (N).

<table><tr><td>The value of N</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>10</td><td>0.820</td><td>0.660</td><td>0.675</td></tr><tr><td>15</td><td>0.849</td><td>0.758</td><td>0.764</td></tr><tr><td>20</td><td>0.872</td><td>0.818</td><td>0.811</td></tr><tr><td>25</td><td>0.877</td><td>0.849</td><td>0.835</td></tr><tr><td>30</td><td>0.882</td><td>0.866</td><td>0.855</td></tr><tr><td>35</td><td>0.890</td><td>0.882</td><td>0.870</td></tr><tr><td>40</td><td>0.905</td><td>0.907</td><td>0.890</td></tr></table>

AQ III: Impact of �, the Number of Labels in the Few-Shot Fine-Tuning Stage. For this experiment, we collected 2-tab trafic traces corresponding to 400 labels using Tor browser versions V12.5.6 and V13.5. We then evaluated the impact of � (the number of labels) during the few-shot fine-tuning stage, alongside assessing the robustness of FMWF across diferent browser versions. The model is tested across diferent settings, with �=200,300,400 and N=10,20,30,40 (representing the number of samples per label). As shown in Table 3, increasing the number of labels (�) consistently results in strong performance. For example, in the 400-way task, the model achieves a top-2 accuracy of 0.883 and an F1-score of 0.887. This demonstrates that increasing the number of labels (�) during fine-tuning allows FMWF to maintain its ability to generalize efectively in complex, multi-tab classification tasks.

Table 3: Performance Evaluation Across Diferent Label Quantities (M) in Few-Shot Fine-Tuning.

<table><tr><td rowspan="2">The value of N</td><td colspan="4">200-way</td><td colspan="4">300-way</td><td colspan="4">400-way</td></tr><tr><td>A@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>A@2</td><td>Precision</td><td>Recall</td><td>F1-score</td><td>A@2</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td>10</td><td>0.732</td><td>0.805</td><td>0.826</td><td>0.818</td><td>0.711</td><td>0.770</td><td>0.800</td><td>0.767</td><td>0.645</td><td>0.779</td><td>0.753</td><td>0.744</td></tr><tr><td>20</td><td>0.838</td><td>0.874</td><td>0.905</td><td>0.878</td><td>0.822</td><td>0.859</td><td>0.882</td><td>0.855</td><td>0.804</td><td>0.836</td><td>0.849</td><td>0.828</td></tr><tr><td>30</td><td>0.890</td><td>0.911</td><td>0.937</td><td>0.918</td><td>0.873</td><td>0.889</td><td>0.922</td><td>0.896</td><td>0.815</td><td>0.861</td><td>0.893</td><td>0.863</td></tr><tr><td>40</td><td>0.914</td><td>0.929</td><td>0.955</td><td>0.934</td><td>0.901</td><td>0.906</td><td>0.940</td><td>0.916</td><td>0.883</td><td>0.887</td><td>0.909</td><td>0.887</td></tr></table>

AQ IV: Performance of FMWF on Google Chrome and Microsoft Edge Datasets. In this experiment, we evaluate the efectiveness of FMWF on two widely used but less explored non anonymous browsers, Google Chrome and Microsoft Edge, which capture a richer set of network features such as packet sizes and di rections. In contrast to the anonymous Tor browser, FMWF requires significantly fewer samples to achieve high accuracy. We compare FMWF against three state-of-the-art models (ARES, TMWF, and BAPM) across 2-tab, 3-tab, 4-tab, and 5-tab scenarios, utilizing varying numbers ofsamples per label (�). We present a detailed analysis of the performance of FMWF on the Google Chrome and Microsoft Edge datasets in Appendix A.

Table 4: Performance Evaluation ofFMWF in the Open-World Scenario with Diferent Numbers of Traces (N) for Few-Shot Fine-Tuning.

<table><tr><td rowspan="2">Method</td><td colspan="5">Number of Traces (N)</td></tr><tr><td>N=1</td><td>N=3</td><td>N=5</td><td>N=7</td><td>N=10</td></tr><tr><td>BAPM (ACSAC&#x27;21)</td><td>0.568</td><td>0.685</td><td>0.703</td><td>0.725</td><td>0.738</td></tr><tr><td>TMWF (CCS&#x27;23)</td><td>0.355</td><td>0.579</td><td>0.657</td><td>0.708</td><td>0.855</td></tr><tr><td>ARES (SP&#x27;23)</td><td>0.364</td><td>0.485</td><td>0.533</td><td>0.578</td><td>0.655</td></tr><tr><td>FMWF(Ours)</td><td>0.925</td><td>0.943</td><td>0.949</td><td>0.954</td><td>0.960</td></tr></table>

## 4.3 AQ V: Open-world Evaluation

In the open-world scenario, FMWF is assessed on its ability to dif ferentiate between monitored and non-monitored websites. As in previous studies [7, 10, 13], all non-monitored websites are treated as a single broad category, while each monitored website is consid ered a distinct class. To mitigate data imbalance, we adopt the same strategy as earlier works [7, 30] by combining closed-world and open-world instances under the same tab settings. For instance, the

2-tab closed and open-world instances are merged to conduct the 2-tab open-world experiment.

We use � = 1, 3, 5, 7, 10 to represent the number of traces per monitored website in the support set for few-shot fine-tuning. In the query set, we test the model with 100 monitored and 1000 unmonitored traces. As shown in Table 4, FMWF consistently achieves over 90% top-2 accuracy across all settings. FMWF exhibits competitive performances against transformer-based large models, further highlighting its eficiency and robustness in more complex open-world scenarios.

## 5 Conclusion and Future Work

In this work, we have introduced FMWF, a novel few-shot multi-tab website fingerprinting (WF) attack method that leverages transfer learning to address the limitations of existing WF approaches. Unlike traditional methods that depend on extensive datasets and prior knowledge of the number of open tabs, FMWF employs a twostage framework that integrates data augmentation and few-shot fine-tuning. This design enables the eficient handling of multi-tab trafic traces while requiring minimal real-world data, making it more adaptable to realistic browsing behaviors.

Looking ahead, we plan to investigate potential defense mechanisms against multi-tab WF attacks and explore how our method can be enhanced to counteract these defenses. Common strategies in website fingerprinting include trafic obfuscation techniques, such as packet padding, trafic morphing, and random delays, which aim to obscure trafic traces and make them less distinguishable. Given that multi-tab trafic is already challenging to analyze due to inherent overlaps, incorporating defenses will introduce an additional layer of complexity, presenting a valuable avenue for future research in enhancing both attack and defense methodologies in this domain.

## Acknowledgments

This work is supported by the National Key R&D Program of China (2022YFB3103500), the National Natural Science Foundation of China (62076125, 62172258, U21A20467), and the Shenzhen Science and Technology Program (JCYJ20210324134810028).

## References

[1] Kota Abe and Shigeki Goto. 2016. Fingerprinting attack on Tor anonymity using deep learning. Proceedings of the Asia-Pacific Advanced Network 42, 0 (2016), 15–20.

[2] Sanjit Bhat, David Lu, Albert Kwon, and Srinivas Devadas. 2018. Var-CNN: A data-eficient website fingerprinting attack based on deep learning. arXiv preprint arXiv:1802.10215 (2018).

[3] Xiang Cai, Rishab Nithyanand, Tao Wang, Rob Johnson, and Ian Goldberg. 2014. A systematic approach to developing and evaluating website fingerprinting defenses. In Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security. 227–238.

[4] Raghavendra Chalapathy and Sanjay Chawla. 2019. Deep learning for anomaly detection: A survey. arXiv preprint arXiv:1901.03407 (2019).

[5] Weiqi Cui, Tao Chen, Christian Fields, Julianna Chen, Anthony Sierra, and Eric Chan-Tin. 2019. Revisiting assumptions for website fingerprinting attacks. In Proceedings ofthe 2019 ACM asia conference on computer and communications security. 328–339.

[6] Xinhao Deng, Qi Li, and Ke Xu. 2024. Robust and reliable early-stage Website fingerprinting attacks via spatial-temporal distribution analysis. arXiv preprint arXiv:2407.00918 (2024).

[7] Xinhao Deng, Qilei Yin, Zhuotao Liu, Xiyuan Zhao, Qi Li, Mingwei Xu, Ke Xu, and Jianping Wu. 2023. Robust multi-tab website fingerprinting attacks in the wild. In 2023 IEEE Symposium on Security and Privacy (SP). IEEE, 1005–1022.

[8] Xiaodan Gu, Ming Yang, and Junzhou Luo. 2015. A novel website fingerprinting attack against multi-tab browsing behavior. In 2015 IEEE 19th international conference on computer supported cooperative work in design (CSCWD). IEEE, 234–239.

[9] Xiaodan Gu, Ming Yang, Bingchen Song, Wei Lan, and Zhen Ling. 2023. A practical multi-tab website fingerprinting attack. Journal of Information Security and Applications 79 (2023), 103627.

[10] Zhong Guan, Gang Xiong, Gaopeng Gou, Zhen Li, Mingxin Cui, and Chang Liu. 2021. BAPM: block attention profiling model for multi-tab website fingerprinting attacks on tor. In Proceedings ofthe 37th Annual Computer Security Applications Conference. 248–259.

[11] Jamie Hayes and George Danezis. 2016. k-fingerprinting: A robust scalable website fingerprinting technique. In 25th USENIX Security Symposium (USENIX Security 16). 1187–1203.

[12] Guodong Huang, Chuan Ma, Ming Ding, Yuwen Qian, Chunpeng Ge, Liming Fang, and Zhe Liu. 2023. Eficient and low overhead website fingerprinting attacks and defenses based on TCP/IP trafic. In Proceedings ofthe ACM Web Conference 2023. 1991–1999.

[13] Zhaoxin Jin, Tianbo Lu, Shuang Luo, and Jiaze Shang. 2023. Transformer-based Model for Multi-tab Website Fingerprinting Attack. In Proceedings ofthe 2023 ACM SIGSAC Conference on Computer and Communications Security. 1050–1064.

[14] Marc Juarez, Sadia Afroz, Gunes Acar, Claudia Diaz, and Rachel Greenstadt. 2014. A critical evaluation of website fingerprinting attacks. In Proceedings ofthe 2014 ACM SIGSAC conference on computer and communications security. 263–274.

[15] Jingzhou Liu, Wei-Cheng Chang, Yuexin Wu, and Yiming Yang. 2017. Deep learning for extreme multi-label text classification. In Proceedings ofthe 40th international ACM SIGIR conference on research and development in information retrieval. 115–124.

[16] Xu Luo, Hao Wu, Ji Zhang, Lianli Gao, Jing Xu, and Jingkuan Song. 2023. A closer look at few-shot classification again. In International Conference on Machine Learning. PMLR, 23103–23123.

[17] Akshaya Mani, T Wilson-Brown, Rob Jansen, Aaron Johnson, and Micah Sherr. 2018. Understanding tor usage with privacy-preserving measurement. In Proceedings of the Internet Measurement Conference 2018. 175–187.

[18] Andriy Panchenko, Fabian Lanze, Jan Pennekamp, Thomas Engel, Andreas Zin nen, Martin Henze, and Klaus Wehrle. 2016. Website Fingerprinting at Internet Scale.. In NDSS.

[19] Mohammad Saidur Rahman, Payap Sirinam, Nate Mathews, Kantha Girish Gangadhara, and Matthew Wright. 2019. Tik-tok: The utility of packet timing in website fingerprinting attacks. arXiv preprint arXiv:1902.06421 (2019).

[20] Vera Rimmer, Davy Preuveneers, Marc Juarez, Tom Van Goethem, and Wouter Joosen. 2017. Automated website fingerprinting through deep learning. arXiv preprint arXiv:1708.06376 (2017).

[21] Payap Sirinam, Mohsen Imani, Marc Juarez, and Matthew Wright. 2018. Deep fin gerprinting: Undermining website fingerprinting defenses with deep learning. In Proceedings ofthe 2018 ACM SIGSAC conference on computer and communications security. 1928–1943.

[22] Payap Sirinam, Nate Mathews, Mohammad Saidur Rahman, and Matthew Wright. 2019. Triplet fingerprinting: More practical and portable website fingerprinting with n-shot learning. In Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security. 1131–1148.

[23] Xueliang Sun, Anxin Huang, Xiapu Luo, and Yi Xie. 2021. Webpage fingerprinting identification on tor: a survey. Journal of Computer Research and Development 58, 8 (2021), 1773–1788.

[24] Chuanqi Tan, Fuchun Sun, Tao Kong, Wenchang Zhang, Chao Yang, and Chunfang Liu. 2018. A survey on deep transfer learning. In Artificial Neural Networks and Machine Learning–ICANN 2018: 27th International Conference on Artificial Neural Networks, Rhodes, Greece, October 4-7, 2018, Proceedings, Part III 27. Springer, 270–279.

[25] Christian von der Weth and Manfred Hauswirth. 2013. Dobbs: Towards a comprehensive dataset to study the browsing behavior of online users. In 2013 IEEE/WIC/ACM International Joint Conferences on Web Intelligence (WI) and Intelligent Agent Technologies (IAT), Vol. 1. IEEE, 51–56.

[26] Chenggang Wang, Jimmy Dani, Xiang Li, Xiaodong Jia, and Boyang Wang. 2021. Adaptive fingerprinting: Website fingerprinting over few encrypted trafic. In Proceedings ofthe Eleventh ACM Conference on Data and Application Security and Privacy. 149–160.

[27] Tao Wang, Xiang Cai, Rishab Nithyanand, Rob Johnson, and Ian Goldberg. 2014. Efective attacks and provable defenses for website fingerprinting. In 23rd USENIX Security Symposium (USENIX Security 14). 143–157.

[28] Tao Wang and Ian Goldberg. 2013. Improved website fingerprinting on tor. In Proceedings of the 12th ACM workshop on Workshop on privacy in the electronic society. 201–212.

[29] Tao Wang and Ian Goldberg. 2016. On realistically attacking tor with website fingerprinting. Proceedings on Privacy Enhancing Technologies (2016).

[30] Yi Xie, Jiahao Feng, Wenju Huang, Yixi Zhang, Xueliang Sun, Xiaochou Chen, and Xiapu Luo. 2024. Contrastive Fingerprinting: A Novel Website Fingerprinting Attack over Few-shot Traces. In Proceedings ofthe ACM on Web Conference 2024. 1203–1214.

[31] Yixiao Xu, Tao Wang, Qi Li, Qingyuan Gong, Yang Chen, and Yong Jiang. 2018. A multi-tab website fingerprinting attack. In Proceedings of the 34th Annual Computer Security Applications Conference. 327–341.

[32] Qilei Yin, Zhuotao Liu, Qi Li, Tao Wang, Qian Wang, Chao Shen, and Yixiao Xu. 2021. An automated multi-tab website fingerprinting attack. IEEE Transactions on Dependable and Secure Computing 19, 6 (2021), 3656–3670

[33] Qingfeng Zhang, Zhiyang Teng, Xuebin Wang, Yue Gao, Qingyun Liu, andJinqiao Shi. 2024. HSDirSniper: A New Attack Exploiting Vulnerabilities in Tor’s Hidden Service Directories. In Proceedings ofthe ACMon Web Conference 2024. 1812–1823.

[34] Ziwei Zhang, Peng Cui, and Wenwu Zhu. 2020. Deep learning on graphs: A survey. IEEE Transactions on Knowledge and Data Engineering 34, 1 (2020), 249–270.

[35] Fuzhen Zhuang, Zhiyuan Qi, Keyu Duan, Dongbo Xi, Yongchun Zhu, Hengshu Zhu, Hui Xiong, and Qing He. 2020. A comprehensive survey on transfer learning. Proc. IEEE 109, 1 (2020), 43–76.

## A Experimental Settings and Supplementary Experiments

## A.1 Parameter Settings

We conducted an extensive search of the hyperparameter space to evaluate and select the optimal hyperparameters for TMWF. Table 5 lists the key hyperparameters we tuned, the range of candidate values, and the final selected values.

Table 5: Hyperparameter selection for the FMWF

<table><tr><td>Parameters</td><td>Search Space</td><td>Selected Value</td></tr><tr><td>Feature Extractor</td><td>GoogleNet, ResNet, DF</td><td>DF</td></tr><tr><td>Classifier</td><td>MLP, Linear</td><td>MLP</td></tr><tr><td>Optimizer</td><td>SGD, Adam</td><td>Adam</td></tr><tr><td>Batch Size</td><td>[32,64,128]</td><td>32</td></tr><tr><td>Embedded Vector&#x27;s Size</td><td>[64,128,256,512]</td><td>512</td></tr></table>

## A.2 Metrics

We evaluate the performance of our multi-tab WF attack using standard metrics from related studies [7, 15]. In the closed-world scenario, we treat multi-tab WF as a multi-class classification prob lem, using Top-k Accuracy (A@K), Precision, Recall, and F1-score to comprehensively assess the model’s performance across all websites. Let � denote the true label vector for an instance �, where $y _ { i } = 1$ indicates that � visited the �-th website, and $y _ { i } = 0$ otherwise. Similarly, �ˆ represents the predicted label vector, where each element corresponds to the predicted probability that � visited a specific website. A@K is used to measure how many of them visited websites appear in the top-k predicted websites based on ${ \hat { y } } .$ The formulation of A@K is as follows:

Table 6: Comparison of FMWF with prior arts in A@K across diferent tabs and sample numbers (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">The value of N</td><td colspan="2">2-tab (A@2)</td><td colspan="2">3-tab (A@3)</td><td colspan="2">4-tab (A@4)</td><td colspan="2">5-tab (A@5)</td></tr><tr><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td><td>Google</td><td>Microsoft</td></tr><tr><td rowspan="3">BAPM (ACSAC&#x27;21)</td><td>1</td><td>0.586</td><td>0.638</td><td>0.491</td><td>0.573</td><td>0.457</td><td>0.442</td><td>0.338</td><td>0.352</td></tr><tr><td>2</td><td>0.744</td><td>0.783</td><td>0.654</td><td>0.726</td><td>0.635</td><td>0.617</td><td>0.525</td><td>0.518</td></tr><tr><td>3</td><td>0.783</td><td>0.822</td><td>0.712</td><td>0.779</td><td>0.695</td><td>0.663</td><td>0.603</td><td>0.635</td></tr><tr><td rowspan="3">TMWF (CCS&#x27;23)</td><td>1</td><td>0.356</td><td>0.491</td><td>0.221</td><td>0.352</td><td>0.184</td><td>0.247</td><td>0.124</td><td>0.208</td></tr><tr><td>2</td><td>0.542</td><td>0.706</td><td>0.484</td><td>0.606</td><td>0.408</td><td>0.534</td><td>0.318</td><td>0.410</td></tr><tr><td>3</td><td>0.637</td><td>0.794</td><td>0.613</td><td>0.674</td><td>0.583</td><td>0.639</td><td>0.467</td><td>0.563</td></tr><tr><td rowspan="3">AERS (SP&#x27;23)</td><td>1</td><td>0.816</td><td>0.818</td><td>0.871</td><td>0.690</td><td>0.706</td><td>0.658</td><td>0.607</td><td>0.601</td></tr><tr><td>2</td><td>0.924</td><td>0.944</td><td>0.900</td><td>0.892</td><td>0.821</td><td>0.870</td><td>0.830</td><td>0.822</td></tr><tr><td>3</td><td>0.960</td><td>0.958</td><td>0.922</td><td>0.910</td><td>0.903</td><td>0.901</td><td>0.852</td><td>0.890</td></tr><tr><td rowspan="3">FMWF (Ours)</td><td>1</td><td>0.782</td><td>0.826</td><td>0.732</td><td>0.694</td><td>0.715</td><td>0.672</td><td>0.588</td><td>0.614</td></tr><tr><td>2</td><td>0.933</td><td>0.940</td><td>0.904</td><td>0.857</td><td>0.840</td><td>0.868</td><td>0.824</td><td>0.841</td></tr><tr><td>3</td><td>0.964</td><td>0.972</td><td>0.915</td><td>0.913</td><td>0.895</td><td>0.904</td><td>0.867</td><td>0.885</td></tr></table>

$$
\mathrm{A@k} = \frac {1}{k} \sum_ {l \in r _ {k} (\hat {y})} y _ {l},\tag{1}
$$

where $r _ { k } ( \hat { y } )$ denotes the set of websites with the top-k highest probabilities in the predicted label vector �ˆ. This metric evaluates the efectiveness of the model in ranking the true websites among the top predictions. Additionally, we compute Precision, Recall, and F1-score to assess the performance of our model further. These metrics are calculated based on the number of true positives (TP), false positives (FP), true negatives (TN), and false negatives (FN) for each website. The formulas for these metrics are given as: Precision $\begin{array} { r } { \mathbf { \tau } = \frac { T P } { T P + F P } , \mathrm { R e c a l l } \mathbf { \tau } = \frac { T P } { T P + F N } } \end{array}$ , and $\begin{array} { r } { \mathrm { F 1 - S c o r e } = \frac { 2 \times \mathrm { P r e c i s i o n } \times \mathrm { R e c a l l } } { \mathrm { P r e c i s i o n } + \mathrm { R e c a l l } } } \end{array}$ . The average values of these metrics are computed across all websites to provide an overall performance measure.

In the open-world scenario, we evaluate the proposed method following established practices [20, 21]. Non-monitored websites are grouped into a single category, allowing us to test FMWF’s ability to identify visited sites among numerous unseen ones. This approach assesses the model’s adaptability and robustness in more realistic browsing conditions.

## A.3 AQ IV: Performance of FMWF on Google Chrome and Microsoft Edge Datasets.

As shown in Table 6, FMWF consistently outperforms the other models in terms of top-k accuracy across most tab settings. For example, in the 2-tab scenario, with just 3 samples per label, FMWF achieves a remarkable top-2 accuracy score of 0.964 on Google Chrome and 0.972 on Microsoft Edge when �=3, surpassing ARES (0.960 on Chrome and 0.958 on Edge), TMWF (0.637 on Chrome and 0.794 on Edge), and BAPM (0.783 on Chrome and 0.822 on Edge). This strong performance persists in more complex multitab scenarios, where FMWF continues to deliver high A@K scores, highlighting its robustness and adaptability across diferent browser environments.

## A.4 Data Augmentation with Multiple Time Interval Types and Experimental Analysis.

Enriching data augmentation instances will enhance system performance. To validate this, we have newly conducted experiments incorporating all three types of time intervals. As shown in Table 7, we conducted experiments in the 2-tab scenario based on the enhancement data augmentation method: top-2 accuracy increased by up to 8.4%, F1 scores improved by up to 3.9%, and the model achieved optimal performance at least 30 epochs earlier. The experimental results indicate that the revised attack model has shown significant improvement in performance.

Table 7: Performance of Revised FMWF with Diferent Numbers of Traces (N).

<table><tr><td rowspan="2">Method</td><td rowspan="2">N</td><td colspan="4">Performance Metrics</td></tr><tr><td>A@2</td><td>Precision</td><td>Recall</td><td>F1-score</td></tr><tr><td rowspan="4">Revised FMWF</td><td>10</td><td>0.790</td><td>0.880</td><td>0.855</td><td>0.833</td></tr><tr><td>20</td><td>0.835</td><td>0.892</td><td>0.910</td><td>0.874</td></tr><tr><td>30</td><td>0.871</td><td>0.903</td><td>0.905</td><td>0.889</td></tr><tr><td>40</td><td>0.904</td><td>0.919</td><td>0.930</td><td>0.910</td></tr></table>